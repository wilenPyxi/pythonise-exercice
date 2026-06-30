"""
audit.py
────────
Passe d'audit LLM (≤ MAX_AUDIT_ITERATIONS) + filet de sécurité des patches.
Code déplacé depuis routes/pythonise_routes_v2.py avec deux corrections :
  • un patch sûr est appliqué à TOUTES les occurrences identiques de
    `location` (la v1 ne corrigeait que la première — un problème répété
    subsistait N-1 fois) ;
  • gestion d'erreurs ciblée (plus d'`except (json.JSONDecodeError, Exception)`).
"""

from __future__ import annotations

import json
import logging
import re
from typing import Callable, Optional

from app.config import MAX_AUDIT_ITERATIONS
from app.knowledge.rules_digest import AUDIT_RULES_ALWAYS, build_rules_digest
from app.llm.client import process_with_openrouter
from app.pipeline.postprocess import insert_python_lines, strip_fences
from app.pipeline.prompts import STEP_AUDIT_PROMPT, SYSTEM_PROMPT

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────────────────────
# Filet de sécurité des patches (déplacé tel quel, noms inchangés)
# ─────────────────────────────────────────────────────────────────────────────

_KNOWN_FREE_NAMES = frozenset({
    "True", "False", "None", "and", "or", "not", "in", "is", "if", "else",
    "elif", "for", "while", "def", "class", "return", "lambda", "yield",
    "with", "as", "from", "import", "pass", "break", "continue", "try",
    "except", "finally", "raise", "global", "nonlocal", "assert", "del",
    "self", "cls",
    "pi", "e", "oo", "abs", "min", "max", "sum", "range", "len", "int",
    "float", "str", "bool", "list", "tuple", "dict", "set", "round", "pow",
    "all", "any", "map", "filter", "zip", "enumerate", "sorted", "reversed",
    "print", "isinstance", "type", "repr", "hash",
    "x", "y", "z", "t", "n", "config_standard",
})


def _patch_introduces_unbound_name(
    myst_exercise: str,
    location: str,
    fix: str,
    python_insert: Optional[str],
) -> Optional[str]:
    """Nom INJECTÉ ({{var}}) introduit par `fix` qui ne serait lié nulle part
    après patch (NameError au rendu). None = sûr sur ce critère.
    Volontairement limité aux placeholders : les autres mots d'un patch
    markdown sont de la prose/du LaTeX, pas des variables Python (la v2 du
    filet flaguait à tort `id`, `f`, `align`… dans des patches purement texte)."""
    fix_names = set(re.findall(r"\{\{\s*([a-zA-Z_]\w*)\s*\}\}", fix))
    loc_names = set(re.findall(r"\{\{\s*([a-zA-Z_]\w*)\s*\}\}", location))
    new_names = (fix_names - loc_names) - _KNOWN_FREE_NAMES
    if not new_names:
        return None

    after_patch = myst_exercise.replace(location, fix)
    if python_insert:
        after_patch += "\n" + python_insert

    for name in new_names:
        patterns = (
            rf"\b{re.escape(name)}\s*=(?!=)",
            rf"\bdef\s+{re.escape(name)}\b",
            rf"\bclass\s+{re.escape(name)}\b",
            rf"\bfor\s+{re.escape(name)}\b",
            rf"\bas\s+{re.escape(name)}\b",
            rf"\bimport\s+(?:\w+\s*,\s*)*{re.escape(name)}\b",
            rf"\bfrom\s+[\w.]+\s+import\s+(?:[^,\n]*,\s*)*{re.escape(name)}\b",
            rf"\bdef\s+\w+\([^)]*\b{re.escape(name)}\b[^)]*\)",
        )
        if not any(re.search(p, after_patch) for p in patterns):
            return name
    return None


def _is_patch_safe(
    myst_exercise: str,
    location: str,
    fix: str,
    python_insert: Optional[str] = None,
) -> tuple[bool, str]:
    """Validation défensive avant application d'un patch d'audit."""
    # 1) Alias d'import supprimé mais encore utilisé.
    alias_re = re.compile(r"\bimport\b[^\n]*?\bas\s+(\w+)")
    dropped = set(alias_re.findall(location)) - set(alias_re.findall(fix))
    if dropped:
        rest = myst_exercise.replace(location, "", 1)
        for alias in dropped:
            if re.search(rf"\b{re.escape(alias)}\s*\(", rest):
                return False, f"Alias `{alias}` est utilisé ailleurs dans le code — patch refusé."

    # 1bis) Import supprimé mais encore référencé.
    def _extract_imported_names(text: str) -> set[str]:
        names: set[str] = set()
        for m in re.finditer(r"^\s*import\s+([\w.]+)(?:\s+as\s+(\w+))?", text, re.MULTILINE):
            names.add(m.group(2) or m.group(1).split(".")[0])
        for m in re.finditer(r"^\s*from\s+[\w.]+\s+import\s+(.+?)\s*$", text, re.MULTILINE):
            for piece in m.group(1).split(","):
                am = re.match(r"^(\w+)(?:\s+as\s+(\w+))?$", piece.strip())
                if am:
                    names.add(am.group(2) or am.group(1))
        return names

    dropped_imports = _extract_imported_names(location) - _extract_imported_names(fix)
    if dropped_imports:
        rest = myst_exercise.replace(location, fix, 1)
        for name in dropped_imports:
            if re.search(rf"\b{re.escape(name)}\b(?:\s*[(.])", rest):
                return False, (f"L'import `{name}` est encore utilisé ailleurs après le patch "
                               "— refus pour éviter une NameError au runtime.")

    # 2) Suppression de globals().
    if "globals()" in location and "globals()" not in fix:
        return False, "Le patch supprimerait `globals()` (requis en fin de bloc python)."

    # 2bis) Règle 6.4 — **config_standard sur un helper PyxiScience (réservé à
    #       sympy.latex). Liste alignée sur le catalogue curé app/knowledge.
    _PYXISCIENCE_HELPERS = (
        "pxsl_format_number", "pxsl_res_num", "pxsl_matrix", "pxsl_pow",
        "pxsl_latex_coefficient", "pxsl_par", "pxsl_mult", "pxsl_choose_udv", "lc",
        "pxsl_latex", "pxsl_sign", "pxsl_latex_with_formatting", "pxsl_Rational",
        "pxsl_sum_matrix", "pxsl_prod_matrix", "pxsl_prod_scalar_matrix",
        "pxsl_ax", "pxsl_system_lin", "pxsl_double_matrix", "pxsl_lines_op",
        "pxsl_resol_system", "pxsl_pow_matrix", "pxsl_law", "pxsl_moment",
        "pxsl_scalar_product", "pxsl_sum_vector", "pxs_explain_IBP",
    )

    def _splat_pattern(name: str) -> str:
        return (rf"\b{re.escape(name)}\s*\("
                r"(?:[^()]|\([^()]*\))*"
                r"\*\*\s*config_standard"
                r"(?:[^()]|\([^()]*\))*\)")

    for helper in _PYXISCIENCE_HELPERS:
        pat = _splat_pattern(helper)
        if re.search(pat, fix) and not re.search(pat, location):
            return False, (f"Le patch ajoute `**config_standard` à `{helper}(...)` — "
                           "ce helper PyxiScience ne l'accepte pas et plante (règle 6.4). "
                           "Réserve `**config_standard` à `sympy.latex(...)` uniquement.")

    # 3) Variable jamais définie.
    unbound = _patch_introduces_unbound_name(myst_exercise, location, fix, python_insert)
    if unbound:
        return False, (f"Le patch introduit la variable `{unbound}` qui n'est définie nulle part "
                       "(NameError à l'exécution). Si une définition Python est nécessaire, "
                       "utilise `python_insert` dans l'audit.")
    return True, ""


def _replace_everywhere(text: str, location: str, fix: str) -> tuple[str, int]:
    """Remplace TOUTES les occurrences de location (1 seule si fix ⊇ location,
    pour éviter la ré-expansion infinie)."""
    if location in fix:
        return text.replace(location, fix, 1), 1
    n = text.count(location)
    return text.replace(location, fix), n


# ─────────────────────────────────────────────────────────────────────────────
# Boucle d'audit
# ─────────────────────────────────────────────────────────────────────────────

def run_audit(
    myst_exercise: str,
    step1_targets: list[str],
    model_idx: int,
    set_step: Optional[Callable[[str], None]] = None,
) -> tuple[str, list[dict], list[dict]]:
    """Audit LLM en boucle (≤ MAX_AUDIT_ITERATIONS). Retourne
    (exercice patché, patches appliqués, warnings)."""
    audit_rule_ids = list(dict.fromkeys(AUDIT_RULES_ALWAYS + step1_targets))
    audit_digest = build_rules_digest(audit_rule_ids)

    patches: list[dict] = []
    warnings: list[dict] = []

    for audit_iter in range(MAX_AUDIT_ITERATIONS):
        if set_step:
            set_step(f"Audit {audit_iter + 1}/{MAX_AUDIT_ITERATIONS}…")
        try:
            audit_raw = process_with_openrouter(
                prompt=STEP_AUDIT_PROMPT.format(
                    audit_rules=audit_digest,
                    exercise=myst_exercise,
                ),
                model_idx=model_idx,
                temperature=0.0,
                max_tokens=8192,
                system_prompt=SYSTEM_PROMPT,
            )
        except (RuntimeError, ValueError, OSError) as audit_err:
            logger.warning("Appel d'audit en échec : %s", audit_err)
            warnings.append({"rule": "?", "message": f"Audit pass failed: {audit_err}"})
            break

        try:
            audit_data = json.loads(strip_fences(audit_raw))
        except json.JSONDecodeError:
            warnings.append({
                "rule": "?",
                "message": "Audit LLM did not return valid JSON; skipping further iterations.",
            })
            break

        if audit_data.get("verdict") == "OK":
            break

        applied_this_iter = 0
        for issue in audit_data.get("issues") or []:
            if not isinstance(issue, dict):
                continue
            rule = str(issue.get("rule", "?"))
            location = issue.get("location") or ""
            fix = issue.get("fix")
            python_insert = issue.get("python_insert")
            can_patch = bool(issue.get("can_patch", True))
            message = issue.get("message") or ""
            applied = False

            if (can_patch and isinstance(location, str) and isinstance(fix, str)
                    and location and location in myst_exercise):
                safe, reason = _is_patch_safe(myst_exercise, location, fix, python_insert)
                if safe:
                    myst_exercise, n_occ = _replace_everywhere(myst_exercise, location, fix)
                    applied = True
                    if n_occ > 1:
                        message += f" ({n_occ} occurrences corrigées)"
                else:
                    warnings.append({
                        "rule": rule,
                        "location": location,
                        "message": f"Patch refusé par filet de sécurité : {reason} (suggestion: {message})",
                    })
                    continue

            if applied and isinstance(python_insert, str) and python_insert.strip():
                myst_exercise = insert_python_lines(myst_exercise, [python_insert.strip()])

            if applied:
                patches.append({
                    "rule": rule,
                    "location": location,
                    "fix": fix,
                    "python_insert": python_insert or None,
                    "message": message,
                    "iteration": audit_iter + 1,
                })
                applied_this_iter += 1
            else:
                warnings.append({
                    "rule": rule,
                    "location": location if isinstance(location, str) else "",
                    "message": message,
                })

        if applied_this_iter == 0:
            break

    return myst_exercise, patches, warnings
