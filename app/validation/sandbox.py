"""
exec_validator.py
─────────────────
Sandboxed execution of the Python block produced by the pythonisation pipeline,
used to validate at runtime the rules that cannot be checked statically :

  • règle 4.3  — la propriété démontrée doit être vraie sur 100 % des seeds
                 (validation multi-seed avec assertions Python).
  • règle 11.1 — toute variable de tirage utilisée dans l'énoncé doit être
                 utilisée dans le tracé matplotlib (analyse AST).
  • règle 11.4 — pas de mélange Rational(sympy) * np.array (analyse AST).
  • règle 11.3 — labels du graphique dans la fenêtre [xlim, ylim] (matplotlib
                 backend Agg + extraction des Text/Line objects).

Toutes les exécutions sont :
  • Isolées dans un namespace neuf (pas de leak entre seeds)
  • Pré-seedées via `random.seed(N)` (déterministe par seed)
  • Time-boxées (signal.alarm, défaut 5 s par exec)
  • Avec PyxiScience mocké via `sys.modules` (le vrai package n'est pas
    installé localement et n'est de toute façon pas nécessaire pour la
    validation des tirages / contraintes math / position des labels).
"""

from __future__ import annotations

import ast
import builtins
import re
import signal
import sys
import threading
import types
from typing import Any, Optional


# ─────────────────────────────────────────────────────────────────────────────
# 1. PyxiScience stubs (the real package isn't installed locally)
# ─────────────────────────────────────────────────────────────────────────────

_STUBS_INSTALLED = False


def _passthrough(*args, **kwargs):
    """Universal callable stub: returns first arg cast to str if any, else ''."""
    if not args:
        return ""
    # latex(...) and pxsl_* helpers all return strings; mirror that shape.
    return str(args[0])


def _config_stub(*args, **kwargs):
    """
    Stub for `pxs_config()`. Must return a `dict` so that downstream code
    like `latex(expr, **config_standard)` (where `config_standard = pxs_config()`)
    doesn't crash with "argument of type 'str' is not iterable".
    """
    return {}


class _StubObject:
    """Universal class stub with arbitrary attribute access."""

    def __init__(self, *args, **kwargs):
        self._args = args
        self._kwargs = kwargs

    def print(self):
        return ""

    def __call__(self, *args, **kwargs):
        return _StubObject(*args, **kwargs)

    def __getattr__(self, name):
        # Any method access returns a no-op callable
        return _passthrough

    def __repr__(self):
        return f"_StubObject({self._args!r})"


# Liste CANONIQUE des helpers connus (catalogue curé + corpus 222 + 33 exemples
# déclinaisons). Sert au `__all__` des modules stub : `from X import *` ne
# passe PAS par __getattr__ (PEP 562), il lit __all__. Partagée avec
# validation/harness.py — NE PAS dupliquer ailleurs.
KNOWN_PXS_HELPERS = [
    "pxs_config", "pxsl_latex", "pxsl_sign", "pxsl_format_number",
    "pxsl_latex_with_formatting", "pxsl_latex_avec_formatage",
    "pxsl_latex_coefficient", "pxsl_to_rational_or_symbol",
    "pxsl_solve_general_inequality", "pxsl_Rational",
    "pxs_is_reductible_sqrt", "pxs_separate_factors",
    "pxs_explain_IBP", "pxsl_par", "pxsl_final_sentence",
    "pxsl_pow", "pxsl_matrix", "pxsl_mat", "pxsl_sum_matrix",
    "pxsl_prod_scalar_matrix", "pxsl_prod_matrix", "pxsl_ax",
    "pxsl_system_lin", "pxsl_double_matrix", "pxsl_lines_op",
    "pxsl_resol_system", "pxs_steps_invert_matrix", "pxs_compute_ech",
    "pxs_compute_ech_reduite", "pxs_system_simpl", "pxs_commute_matrix",
    "pxsl_pow_matrix", "pxs_invertible_matrix", "pxs_diag_matrix",
    "randmatrixrect", "pxs_finiterv", "pxsl_law", "pxsl_moment",
    "pxsl_scalar_product", "pxs_simul_law", "pxs_fct_finiterv",
    "pxsl_res_num", "pxsl_sum_vector", "pxs_nvirgzero", "pxsl_num",
    "pxs_gauss_jordan", "pxs_construct_RREF",
    "pxs_repeat_generate_sys", "pxs_break_all_colinear_rows",
    "pxsl_mult", "pxsl_choose_udv", "pxs_lang", "myst",
    "pxs_variation_number",
    "pxs_Interval", "pxs_Plotable",
]
_STUB_CLASS_NAMES = ("pxs_Interval", "pxs_Plotable")


def _make_stub_module(name: str) -> types.ModuleType:
    """Module stub PEP 562 : tout attribut inconnu est fourni (passthrough /
    classe universelle), et `__all__` couvre les helpers connus pour que
    `from X import *` fonctionne."""
    import re as _re
    mod = types.ModuleType(name)

    def __getattr__(attr):
        if attr == "pxs_config":
            return _config_stub
        if attr == "pxs_variation_number":
            return 1                          # règle 13.2 : vaut toujours 1
        if attr and (attr[0].isupper() or _re.match(r"pxs_[A-Z]", attr)):
            return _StubObject                # ressemble à une classe
        return _passthrough

    mod.__getattr__ = __getattr__
    mod.__all__ = list(KNOWN_PXS_HELPERS)
    return mod


def install_pyxiscience_stubs() -> None:
    """
    Register stub modules for `pyxiscience.*` in sys.modules so that generated
    Python blocks can `import` PyxiScience helpers without crashing. Idempotent.
    UNIFIÉ avec validation/harness.py (même factory PEP 562 + __all__) : les
    deux systèmes partagent sys.modules, le premier installé sert aux deux.
    """
    global _STUBS_INSTALLED
    if _STUBS_INSTALLED:
        return

    if "pyxiscience" in sys.modules:
        _STUBS_INSTALLED = True
        return

    pyxiscience = _make_stub_module("pyxiscience")
    sys.modules["pyxiscience"] = pyxiscience

    submodules = [
        "Mes_fctions_generalistes_bis",
        "Classes_Extensions",
        "Mes_fctions_d_analyse_bis",
        "Mes_fctions_d_analyse",       # alias without _bis (cf. Exo 2 Am. Sud)
        "Mes_fctions_d_alg_lineaire_bis",
        "Mes_fctions_probabilistes_bis",
        "Mes_fctions_generalistes",    # alias historiques
        "Mes_fctions_probabilistes",
        "Mes_fctions_d_alg_lineaire",
    ]
    for sub in submodules:
        m = _make_stub_module(f"pyxiscience.{sub}")
        sys.modules[f"pyxiscience.{sub}"] = m
        setattr(pyxiscience, sub, m)

    # Top-level convenience attribute (some code does `import pyxiscience`)
    pyxiscience.pxs_variation_number = 1  # règle 13.2

    # Stub `src.scripts.pxs_runtime` for `myst()` helper used in conditional text.
    # Observed in real exos like the binomiale exercise:
    #   from src.scripts.pxs_runtime import myst
    #   shot_name = myst(r"{fr}`...`{en}`...`")
    src_mod = types.ModuleType("src")
    scripts_mod = types.ModuleType("src.scripts")
    runtime_mod = types.ModuleType("src.scripts.pxs_runtime")
    runtime_mod.myst = _passthrough
    sys.modules["src"] = src_mod
    sys.modules["src.scripts"] = scripts_mod
    sys.modules["src.scripts.pxs_runtime"] = runtime_mod
    src_mod.scripts = scripts_mod
    scripts_mod.pxs_runtime = runtime_mod

    _STUBS_INSTALLED = True


# ─────────────────────────────────────────────────────────────────────────────
# 2. Extract the main python block from an assembled exercise
# ─────────────────────────────────────────────────────────────────────────────

# Fence {python} à 3 OU 4 backticks (l'app émet 4 — convention plateforme —
# mais la lecture reste tolérante pour les contenus legacy).
_PYTHON_FENCE_RE = re.compile(r"(?ms)^(`{3,4})\{python\}[ \t]*\n(.*?)\n\1[ \t]*$")


def extract_main_python_block(exercise: str) -> Optional[str]:
    """
    Return the contents of the FIRST {python} block in the assembled
    exercise (which by convention holds the imports + random sampling +
    main computations — règle 3.1). Returns None if absent.
    """
    m = _PYTHON_FENCE_RE.search(exercise)
    return m.group(2) if m else None


def extract_all_python_blocks(exercise: str) -> list[str]:
    """Return all {python} block bodies, in order."""
    return [m.group(2) for m in _PYTHON_FENCE_RE.finditer(exercise)]


# ─────────────────────────────────────────────────────────────────────────────
# 3. Sandboxed exec with timeout
# ─────────────────────────────────────────────────────────────────────────────

class ExecTimeout(Exception):
    """Raised when exec exceeds its time budget."""


class _ExecKill(BaseException):
    """Escalade du timeout : BaseException pour percer les `except Exception`
    avaleurs du code généré (seul un `except:` nu peut encore l'attraper)."""


def run_with_timeout(fn, timeout: float):
    """
    Run `fn()` under a timeout — utilisé pour l'exec sandboxé ET pour le
    rendu/scan par graine du harnais (un `str()` sympy sur une expression
    géante peut mouliner des heures : vu au banc du 2026-07-02).

    Two strategies:
      • Main thread → `signal.SIGALRM` avec re-tir périodique (interval) :
        1er tir = ExecTimeout ; tirs suivants = _ExecKill (BaseException),
        car un `try/except Exception` du code généré avale ExecTimeout mais
        ne peut pas attraper une BaseException. Seul un `except:` nu résiste.
      • Background thread (Flask worker) → daemon thread + `Event.wait`.
        The daemon thread can't actually be killed in Python; it survives the
        timeout but doesn't block subsequent execs since each call spawns a
        fresh daemon. Acceptable for short math-only workloads.
    """
    if threading.current_thread() is threading.main_thread():
        fired = {"n": 0}

        def _handler(signum, frame):
            fired["n"] += 1
            if fired["n"] == 1:
                raise ExecTimeout("exec exceeded its time budget")
            raise _ExecKill

        old_handler = signal.signal(signal.SIGALRM, _handler)
        signal.setitimer(signal.ITIMER_REAL, timeout, 0.5)
        try:
            return fn()
        except _ExecKill:
            raise ExecTimeout(
                f"exec tué après {timeout}s (timeout avalé par le code ?)"
            ) from None
        finally:
            signal.setitimer(signal.ITIMER_REAL, 0)
            signal.signal(signal.SIGALRM, old_handler)

    # Background-thread variant: run in a daemon child thread.
    captured: dict[str, object] = {"exc": None, "ret": None}
    done = threading.Event()

    def _target() -> None:
        try:
            captured["ret"] = fn()
        except BaseException as e:  # noqa: BLE001 — re-raised below
            captured["exc"] = e
        finally:
            done.set()

    worker = threading.Thread(target=_target, daemon=True)
    worker.start()
    if not done.wait(timeout):
        raise ExecTimeout(f"exec exceeded {timeout}s")
    if captured["exc"] is not None:
        raise captured["exc"]  # type: ignore[misc]
    return captured["ret"]


def _exec_with_timeout(code: str, namespace: dict, timeout: float) -> None:
    compiled = compile(code, "<sandbox>", "exec")
    run_with_timeout(lambda: exec(compiled, namespace), timeout)


def exec_python_block(
    code: str,
    seed: int = 0,
    extra_globals: Optional[dict] = None,
    timeout: float = 5.0,
) -> dict:
    """
    Execute `code` once, pre-seeding `random` with `seed`.
    Returns:
        {"success": bool, "ns": dict | None, "error": str | None}
    On success, `ns` contains the namespace after exec (variables available
    for assertion evaluation).

    Stubs `pyxiscience.*` and disallows obvious filesystem / network builtins
    by stripping them from the namespace.
    """
    install_pyxiscience_stubs()

    namespace: dict[str, Any] = {
        "__name__": "__sandbox__",
        "__builtins__": _safe_builtins(),
    }
    if extra_globals:
        namespace.update(extra_globals)

    # Pre-seed both random and numpy.random (cheap; ignored if numpy not used).
    preamble = (
        f"import random as _rnd_internal; _rnd_internal.seed({seed})\n"
        f"try:\n"
        f"    import numpy as _np_internal; _np_internal.random.seed({seed})\n"
        f"except Exception:\n"
        f"    pass\n"
    )
    full_code = preamble + code

    try:
        _exec_with_timeout(full_code, namespace, timeout)
        return {"success": True, "ns": namespace, "error": None}
    except ExecTimeout as e:
        return {"success": False, "ns": None, "error": f"timeout ({timeout}s)"}
    except Exception as e:
        return {"success": False, "ns": None, "error": f"{type(e).__name__}: {e}"}


def _safe_builtins() -> dict:
    """
    Return a copy of builtins with dangerous filesystem/network names removed.
    The sandboxed code is generated by an LLM operating on math content; we
    don't want it to accidentally `open(...)` or `__import__('subprocess')`.
    """
    blocked = {
        "open", "input", "exit", "quit", "compile", "eval", "exec",
        "__import__",  # block dynamic imports — explicit imports in code still work via the import statement
    }
    safe: dict[str, Any] = {}
    for name in dir(builtins):
        if name in blocked:
            continue
        safe[name] = getattr(builtins, name)
    # `__import__` we restore but wrap to whitelist
    safe["__import__"] = _safe_import
    return safe


_ALLOWED_TOP_LEVEL_MODULES = {
    "random", "math", "sympy", "numpy", "fractions", "pandas",
    "matplotlib", "scipy", "itertools", "functools", "collections",
    "decimal", "statistics", "operator", "copy", "re", "json",
    "pyxiscience",  # stubbed
    "src",          # stubbed (for `from src.scripts.pxs_runtime import myst`)
}


def _safe_import(name, *args, **kwargs):
    top = name.split(".")[0]
    if top not in _ALLOWED_TOP_LEVEL_MODULES:
        raise ImportError(f"import of {name!r} blocked in sandbox")
    return builtins.__import__(name, *args, **kwargs)


# ─────────────────────────────────────────────────────────────────────────────
# 4. Multi-seed validation for règle 4.3
# ─────────────────────────────────────────────────────────────────────────────

def multi_seed_validate(
    code: str,
    assertions: list[dict],
    num_seeds: int = 100,
    timeout_per_seed: float = 3.0,
) -> dict:
    """
    Run `code` num_seeds times with seeds 0..num_seeds-1 and evaluate each
    assertion in the resulting namespace. Each assertion is a dict with:
        {"description": "...", "assertion": "<python boolean expression>"}

    Returns:
        {
            "num_seeds": int,
            "num_exec_errors": int,
            "violations": [
                {"seed": int, "assertion": "...", "description": "...", "value": "False" | "<exception>"},
                ...  # capped at 5 per assertion
            ],
            "summary_per_assertion": {assertion_str: {"violations": int, "errors": int}}
        }
    """
    summary: dict[str, dict[str, int]] = {
        a["assertion"]: {"violations": 0, "errors": 0}
        for a in assertions if "assertion" in a
    }
    violations: list[dict] = []
    num_exec_errors = 0
    first_exec_error: Optional[str] = None
    capped_assertions: set[str] = set()

    for seed in range(num_seeds):
        res = exec_python_block(code, seed=seed, timeout=timeout_per_seed)
        if not res["success"]:
            num_exec_errors += 1
            if first_exec_error is None:
                first_exec_error = res["error"]
            continue
        ns = res["ns"]
        for a in assertions:
            assertion = a.get("assertion")
            description = a.get("description", "")
            if not isinstance(assertion, str) or not assertion.strip():
                continue
            try:
                ok = bool(eval(assertion, ns))
                if not ok:
                    summary[assertion]["violations"] += 1
                    if assertion not in capped_assertions and len(
                        [v for v in violations if v["assertion"] == assertion]
                    ) < 5:
                        violations.append({
                            "seed": seed,
                            "assertion": assertion,
                            "description": description,
                            "value": "False",
                        })
            except Exception as e:
                summary[assertion]["errors"] += 1
                if assertion not in capped_assertions and len(
                    [v for v in violations if v["assertion"] == assertion]
                ) < 5:
                    violations.append({
                        "seed": seed,
                        "assertion": assertion,
                        "description": description,
                        "value": f"{type(e).__name__}: {e}",
                    })

    return {
        "num_seeds": num_seeds,
        "num_exec_errors": num_exec_errors,
        "first_exec_error": first_exec_error,
        "violations": violations,
        "summary_per_assertion": summary,
    }


# ─────────────────────────────────────────────────────────────────────────────
# 5. Static AST checks for règles 11.1 (unused random vars in plot)
#    and 11.4 (Rational sympy * numpy array)
# ─────────────────────────────────────────────────────────────────────────────

# Names of plotting functions to look for (matplotlib API used in PyxiScience).
_PLOT_FN_NAMES = {
    "plot", "scatter", "fill_between", "fill", "vlines", "hlines",
    "axhline", "axvline", "text", "annotate", "errorbar", "stem",
    "step", "imshow", "contour", "contourf", "quiver", "stairs",
}


def static_check_unused_random_vars(
    code: str,
    random_var_names: list[str],
    markdown_text: str = "",
) -> list[str]:
    """
    Règle 11.1 : any variable sampled randomly should be referenced either
    in the rest of the Python code (Load context) OR somewhere in the MyST
    markdown (`{{var}}` placeholder). Otherwise it's dead code.

    `markdown_text` should be the assembled exercise WITHOUT the Python
    blocks (or the whole exercise — both work because the regex looks for
    `{{var}}` patterns which only appear in MyST sections).

    Returns the list of names that have ZERO references anywhere. Empty
    list = règle respectée.
    """
    if not random_var_names:
        return []

    referenced: set[str] = set()

    # 1) References in the Python code (Load context).
    try:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
                if node.id in random_var_names:
                    referenced.add(node.id)
    except SyntaxError:
        pass  # leniency: don't false-positive on parse failures

    # 2) References in the MyST markdown ({{var}} or {{var.foo}} or {{f(var)}}).
    if markdown_text:
        for name in random_var_names:
            if name in referenced:
                continue
            if re.search(rf"\{{\{{[^}}]*\b{re.escape(name)}\b[^}}]*\}}\}}", markdown_text):
                referenced.add(name)

    return [v for v in random_var_names if v not in referenced]


def static_check_rational_numpy_mix(code: str) -> list[dict]:
    """
    Règle 11.4 : detect `Rational(...) * <np.array_expr>` or similar
    sympy-Rational ↔ numpy mixes that crash at runtime.

    Detection is intentionally narrow to avoid false positives. We flag:
      Rational(...) * <expr_referencing_np>
      <expr_referencing_np> * Rational(...)
    where `<expr_referencing_np>` contains a `np.something` or a name we
    recognise as a numpy array (heuristic: contains `_graph` suffix).
    """
    issues: list[dict] = []
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return issues

    def _is_rational_call(node: ast.AST) -> bool:
        return (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "Rational"
        )

    def _references_numpy(node: ast.AST) -> bool:
        for sub in ast.walk(node):
            if isinstance(sub, ast.Attribute) and isinstance(sub.value, ast.Name):
                if sub.value.id in {"np", "numpy"}:
                    return True
            if isinstance(sub, ast.Name) and (
                sub.id.endswith("_graph") or sub.id.endswith("_arr")
            ):
                return True
        return False

    for node in ast.walk(tree):
        if isinstance(node, ast.BinOp) and isinstance(node.op, (ast.Mult, ast.Add, ast.Sub)):
            left, right = node.left, node.right
            if (_is_rational_call(left) and _references_numpy(right)) or (
                _is_rational_call(right) and _references_numpy(left)
            ):
                issues.append({
                    "rule": "11.4",
                    "message": (
                        "Mélange Rational(sympy) ↔ numpy détecté à la ligne "
                        f"{getattr(node, 'lineno', '?')} — convertir Rational en float() "
                        "AVANT toute opération numpy."
                    ),
                })
    return issues


# ─────────────────────────────────────────────────────────────────────────────
# 6. Dynamic matplotlib check for règle 11.3 (labels in plot window)
# ─────────────────────────────────────────────────────────────────────────────

def dynamic_check_matplotlib(code: str, timeout: float = 8.0) -> list[dict]:
    """
    Execute `code` with a headless matplotlib backend, then inspect every
    Text artist on every axis and flag any whose position falls outside
    [xlim, ylim] (règle 11.3).

    Notes:
      • Only runs if `matplotlib` is imported in the code (avoid pointless exec).
      • Uses `matplotlib.use("Agg", force=True)` BEFORE the user code imports
        matplotlib — this is achieved by pre-importing pyplot in the namespace
        with the Agg backend already set.
      • `plt.show()` becomes a no-op under Agg, so the user code runs to
        completion without opening a window.
    """
    if "matplotlib" not in code:
        return []

    import matplotlib
    matplotlib.use("Agg", force=True)
    import matplotlib.pyplot as plt

    # Reset figure state to isolate runs (close any leftovers).
    plt.close("all")

    # Inject `plt`/`matplotlib` already set up into the namespace so the user
    # code's `import matplotlib.pyplot as plt` finds the Agg backend.
    extra = {}

    res = exec_python_block(code, seed=0, extra_globals=extra, timeout=timeout)
    issues: list[dict] = []
    if not res["success"]:
        # Don't fault the user; runtime errors are caught elsewhere.
        plt.close("all")
        return []

    for fig_num in plt.get_fignums():
        fig = plt.figure(fig_num)
        for ax in fig.get_axes():
            try:
                xmin, xmax = ax.get_xlim()
                ymin, ymax = ax.get_ylim()
            except Exception:
                continue
            for text_artist in ax.texts:
                try:
                    x, y = text_artist.get_position()
                except Exception:
                    continue
                # Numeric only; skip annotations with non-numeric positions.
                if not (isinstance(x, (int, float)) and isinstance(y, (int, float))):
                    continue
                out_of_bounds = (x < xmin or x > xmax or y < ymin or y > ymax)
                if out_of_bounds:
                    label = text_artist.get_text()
                    snippet = label.strip()[:40].replace("\n", " ")
                    issues.append({
                        "rule": "11.3",
                        "message": (
                            f"Label « {snippet} » à ({x:.2f}, {y:.2f}) sort de la fenêtre "
                            f"[{xmin:.1f}, {xmax:.1f}] × [{ymin:.1f}, {ymax:.1f}]. "
                            "Matplotlib va étendre l'axe et compresser le graphique."
                        ),
                    })
    plt.close("all")
    return issues


# ─────────────────────────────────────────────────────────────────────────────
# 7. Smoke test (run module directly: `python utils/exec_validator.py`)
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    code = """
import random as rd
from sympy import Rational
a = rd.randint(1, 10)
b = rd.choice([2, 3, 4])
result = Rational(a, b)
"""
    print("[smoke] running 10 seeds with simple code...")
    out = multi_seed_validate(
        code,
        assertions=[
            {"description": "a est positif", "assertion": "a > 0"},
            {"description": "b est dans {2,3,4}", "assertion": "b in (2, 3, 4)"},
            {"description": "a < b (BUG attendu sur certains seeds)", "assertion": "a < b"},
        ],
        num_seeds=10,
    )
    print(out)
