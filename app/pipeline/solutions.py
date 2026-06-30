"""
solutions.py
────────────
Substitution déterministe des solutions validées (règle 8.1 — directive
Chabane) : chaque ::::{detailedSolution} générée est remplacée par la version
SOURCE dont seules les valeurs littérales deviennent des {{var}}.
Déplacé depuis routes/pythonise_routes_v2.py (logique inchangée ; gestion
d'erreurs ciblée).
"""

from __future__ import annotations

import logging
import re
from typing import Optional

from app.llm.client import process_with_openrouter
from app.pipeline.postprocess import extract_detailed_solutions, strip_fences
from app.pipeline.prompts import SOLUTION_SUBSTITUTION_PROMPT, SYSTEM_PROMPT

logger = logging.getLogger(__name__)

_DETAILED_SOLUTION_RE = re.compile(
    r"::::\{detailedSolution\}\s*\n(.*?)\n::::",
    re.DOTALL,
)


def _substitute_solution_via_llm(
    source_text: str,
    analysis: dict,
    model_idx: int,
) -> Optional[str]:
    """Appel LLM ciblé : valeurs littérales de la solution source → {{var}}.
    None en cas d'échec (l'appelant garde alors la solution générée)."""
    variables = analysis.get("variables") or []
    if not variables or not source_text.strip():
        return None

    variables_table = "\n".join(
        f"  • `{v['nom']}` (valeur exemple: `{v.get('valeur_exemple', '?')}`)"
        f" — {v.get('description', '')[:60]}"
        for v in variables
        if isinstance(v, dict) and v.get("nom")
    )
    if not variables_table:
        return None

    try:
        raw = process_with_openrouter(
            prompt=SOLUTION_SUBSTITUTION_PROMPT.format(
                original_solution=source_text,
                variables_table=variables_table,
            ),
            model_idx=model_idx,
            temperature=0.0,
            max_tokens=4096,
            system_prompt=SYSTEM_PROMPT,
        )
    except (RuntimeError, ValueError, OSError) as e:
        logger.warning("Substitution de solution en échec : %s", e)
        return None

    text = strip_fences(raw).strip()
    return text or None


def replace_gen_solutions_with_source(
    myst_exercise: str,
    source_content: str,
    analysis: dict,
    model_idx: int,
) -> tuple[str, list[dict]]:
    """Remplace chaque detailedSolution générée par la version source
    substituée (correspondance positionnelle). Retourne (exercice, patches)."""
    source_solutions = extract_detailed_solutions(source_content)
    if not source_solutions:
        return myst_exercise, []

    patches: list[dict] = []
    idx = {"i": 0}

    def _sub(match):
        i = idx["i"]
        idx["i"] += 1
        if i >= len(source_solutions):
            return match.group(0)
        src = source_solutions[i]
        if not src.strip():
            return match.group(0)
        substituted = _substitute_solution_via_llm(src, analysis, model_idx)
        if not substituted:
            return match.group(0)

        new_block = f"::::{{detailedSolution}}\n{substituted}\n::::"
        if substituted.strip() != match.group(1).strip():
            patches.append({
                "rule": "8.1",
                "location": f"detailedSolution Q{i + 1}",
                "fix": "substitution déterministe (source préservée)",
                "message": (f"Question {i + 1}: detailedSolution remplacée par la version "
                            "source (valeurs littérales → {{var}}), pédagogie préservée "
                            "(règle 8.1)."),
                "iteration": 0,
            })
        return new_block

    return _DETAILED_SOLUTION_RE.sub(_sub, myst_exercise), patches
