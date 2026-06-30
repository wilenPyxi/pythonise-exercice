"""
harness.py — porte de qualité déterministe du pipeline.

Miroir importable du harnais de référence
(.claude/skills/validation-harness/harness.py) : mêmes contrôles, même
sévérité, mais API Python (validate_text) au lieu d'un CLI. Toute sortie du
pipeline DOIT passer ici avant d'être rendue ; un verdict rouge déclenche
une (1) boucle de réparation LLM puis, à défaut, un warning fort.

Contrôles :
  1. STATIQUE   — {{ }} = identifiant nu camelCase sans _ ; questionId/Index
                  uniques et contigus dès 0 ; bloc {python} présent.
  2. EXEC       — tous les blocs {python} (concaténés) s'exécutent sur N
                  graines, 0 exception. Stubs pyxiscience légers.
  3. INJECTION  — chaque {{ var }} se résout dans le namespace, 0 inconnue.
  4. INTERDITS  — motifs interdits sur le corps rendu (skill §6).
"""

from __future__ import annotations

import io
import logging
import random
import re
import sys
import traceback
import types
import warnings as _warnings
from contextlib import redirect_stdout

logger = logging.getLogger(__name__)

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as _plt
    _HAS_MPL = True
except Exception:
    _plt = None
    _HAS_MPL = False


# ── Stubs pyxiscience (identiques au harnais de référence) ───────────────────

def install_pyxiscience_stubs() -> None:
    if "pyxiscience" in sys.modules:
        return

    class _Universal:
        def __init__(self, *a, **k): pass
        def __call__(self, *a, **k): return _Universal()
        def __getattr__(self, _): return _Universal()
        def __getitem__(self, _): return _Universal()
        def __iter__(self): return iter(())
        def __str__(self): return ""
        def __repr__(self): return ""
        def __mul__(self, o): return self
        __rmul__ = __add__ = __radd__ = __sub__ = __rsub__ = __mul__

    def _passthrough(*a, **k):
        return str(a[0]) if a else ""

    def _pxs_config(*a, **k):
        # dict VIDE : utilisable comme **config_standard sans faire planter
        # sympy.latex (qui rejette toute clé inconnue).
        return {}

    def _make_module(name: str) -> types.ModuleType:
        mod = types.ModuleType(name)

        def __getattr__(attr):  # PEP 562
            if attr == "pxs_config":
                return _pxs_config
            # Classe si CamelCase OU motif pxs_Xxx (pxs_Interval, pxs_Plotable…)
            if attr and (attr[0].isupper() or re.match(r"pxs_[A-Z]", attr)):
                return _Universal
            return _passthrough

        mod.__getattr__ = __getattr__
        return mod

    root = _make_module("pyxiscience")
    sys.modules["pyxiscience"] = root
    for sub in (
        "Mes_fctions_generalistes_bis",
        "Mes_fctions_d_analyse_bis",
        "Mes_fctions_d_alg_lineaire_bis",
        "Mes_fctions_probabilistes_bis",
        "Classes_Extensions",
    ):
        full = f"pyxiscience.{sub}"
        sys.modules[full] = _make_module(full)
        setattr(root, sub, sys.modules[full])


# ── Extraction (fences 3 ou 4 backticks, lecture tolérante) ──────────────────

PY_FENCE_ANY_RE = re.compile(r"(?ms)^(`{3,4})\{python\}[ \t]*\n(.*?)\n\1[ \t]*$")
INJECTION_RE = re.compile(r"\{\{(.*?)\}\}", re.DOTALL)
VALID_TOKEN_RE = re.compile(r"^[A-Za-z][A-Za-z0-9]*$")


def extract_python_code(text: str) -> str | None:
    """Concatène TOUS les blocs {python} (namespace partagé, ordre document)."""
    blocks = [m.group(2) for m in PY_FENCE_ANY_RE.finditer(text)]
    return "\n\n".join(blocks) if blocks else None


def strip_python_blocks(text: str) -> str:
    return PY_FENCE_ANY_RE.sub("", text)


# ── Contrôles statiques ──────────────────────────────────────────────────────

def check_injection_tokens(text: str) -> list[str]:
    errs: list[str] = []
    if "{{{" in text:
        errs.append("triple-accolade `{{{` détectée (casse la substitution)")
    for raw in INJECTION_RE.findall(strip_python_blocks(text)):
        tok = raw.strip()
        if not tok:
            errs.append("injection vide `{{ }}`")
            continue
        if VALID_TOKEN_RE.match(tok):
            continue
        why = []
        if "_" in tok:
            why.append("underscore")
        if "(" in tok or ")" in tok:
            why.append("appel de fonction")
        if any(c in tok for c in "+*/\\,"):
            why.append("calcul/opérateur")
        if "." in tok:
            why.append("attribut")
        if " " in tok:
            why.append("espace / plusieurs tokens")
        if not why:
            why.append("pas un identifiant nu")
        errs.append(f"injection invalide `{{{{ {tok} }}}}` : {', '.join(why)}")
    return errs


def check_question_ids(text: str) -> list[str]:
    errs: list[str] = []
    for field in ("questionId", "questionIndex"):
        ids = [int(x) for x in re.findall(rf":{field}:\s*(\d+)", text)]
        if not ids:
            continue
        if len(ids) != len(set(ids)):
            errs.append(f":{field}: contient des doublons : {ids}")
        if sorted(ids) != list(range(len(ids))):
            errs.append(f":{field}: non contigu à partir de 0 : {ids}")
    return errs


# ── Motifs interdits (corps rendu — skill §6) ────────────────────────────────

FORBIDDEN = [
    (r"(?<!\\)\$[0-9]",              r"`$` (non échappé) collé à un chiffre — préfixer par ${} ou passer en display"),
    (r"\{\{\{",                      r"triple-accolade `{{{`"),
    (r"\^\{\s*0\s*\}",               r"`^{0}`"),
    (r"\^\{\s*1\s*\}",               r"`^{1}`"),
    (r"\\sqrt\[1\]",                 r"`\sqrt[1]`"),
    (r"\\sqrt\[2\]",                 r"`\sqrt[2]` (utiliser `\sqrt`)"),
    (r"\\frac\{\s*\}\{",             r"`\frac{}{…}` (numérateur vide)"),
    (r"\\frac\{[^{}]*\}\{\s*1\s*\}", r"`\frac{…}{1}`"),
    (r"\blatex\(",                   r"`latex(` ayant fui dans le rendu"),
    (r"\bround\(",                   r"`round(` dans le rendu"),
    (r"\bpxsl_matrix\b",             r"`pxsl_matrix` dans le rendu"),
    (r"-\s*\+",                      r"double signe `- +`"),
    (r"\+\s*-",                      r"double signe `+ -`"),
]
FORBIDDEN = [(re.compile(p), msg) for p, msg in FORBIDDEN]


def scan_forbidden(body: str) -> list[str]:
    errs = []
    for rx, msg in FORBIDDEN:
        m = rx.search(body)
        if m:
            start = max(0, m.start() - 30)
            ctx = body[start:m.end() + 30].replace("\n", " ")
            errs.append(f"{msg}  …{ctx}…")
    return errs


# ── Rendu (substitution des injections) ──────────────────────────────────────

def render_body(body_tmpl: str, env: dict) -> tuple[str, list[str]]:
    unresolved: list[str] = []

    def repl(m):
        name = m.group(1).strip()
        if name in env:
            try:
                return str(env[name])
            except Exception:
                return f"<<ERR:{name}>>"
        unresolved.append(name)
        return f"<<{name}>>"

    return INJECTION_RE.sub(repl, body_tmpl), unresolved


# ── Validation principale ────────────────────────────────────────────────────

def validate_text(text: str, seeds: int = 100) -> dict:
    """
    Valide un exercice pythonisé (texte MyST complet).

    Retourne :
      {
        "ok": bool,
        "seeds": int,
        "static_errors": [str],
        "n_exec_errors": int, "n_unresolved": int, "n_forbidden": int,
        "first_failures": [str],     # ≤ 8, lisibles
      }
    """
    static_errors = check_injection_tokens(text) + check_question_ids(text)
    code = extract_python_code(text)
    if code is None:
        static_errors.append("aucun bloc `{python}` trouvé")

    report = {
        "ok": False,
        "seeds": seeds,
        "static_errors": static_errors,
        "n_exec_errors": 0,
        "n_unresolved": 0,
        "n_forbidden": 0,
        "first_failures": [],
    }
    if code is None:
        return report

    body_tmpl = strip_python_blocks(text)
    install_pyxiscience_stubs()
    failures: list[str] = []

    for s in range(seeds):
        random.seed(s)
        env: dict = {"rd": random, "random": random}
        try:
            with redirect_stdout(io.StringIO()), _warnings.catch_warnings():
                _warnings.simplefilter("ignore")   # plt.show() sous Agg, etc.
                exec(code, env)  # noqa: S102 — sandbox stubs + contenu maison
        except Exception:
            report["n_exec_errors"] += 1
            if len(failures) < 5:
                tb = traceback.format_exc().strip().splitlines()
                failures.append(f"seed {s} : exception — {tb[-1]}")
            if _HAS_MPL:
                _plt.close("all")
            continue
        if _HAS_MPL:
            _plt.close("all")

        rendered, unresolved = render_body(body_tmpl, env)
        if unresolved:
            report["n_unresolved"] += 1
            if len(failures) < 8:
                failures.append(f"seed {s} : variable(s) non résolue(s) : {sorted(set(unresolved))}")
        fb = scan_forbidden(rendered)
        if fb:
            report["n_forbidden"] += 1
            if len(failures) < 8:
                failures.append(f"seed {s} : motif interdit : {fb[0]}")

    report["first_failures"] = failures
    report["ok"] = (
        not static_errors
        and report["n_exec_errors"] == 0
        and report["n_unresolved"] == 0
        and report["n_forbidden"] == 0
    )
    return report


def format_report(report: dict) -> str:
    """Résumé texte court (pour warnings / prompt de réparation)."""
    lines = []
    for e in report["static_errors"]:
        lines.append(f"[STATIQUE] {e}")
    n = report["seeds"]
    if report["n_exec_errors"]:
        lines.append(f"[EXEC] {report['n_exec_errors']}/{n} graines en exception")
    if report["n_unresolved"]:
        lines.append(f"[INJECTION] {report['n_unresolved']}/{n} graines avec variables non résolues")
    if report["n_forbidden"]:
        lines.append(f"[INTERDITS] {report['n_forbidden']}/{n} graines avec motif interdit")
    lines.extend(f"  • {f}" for f in report["first_failures"])
    return "\n".join(lines) if lines else "VERT"
