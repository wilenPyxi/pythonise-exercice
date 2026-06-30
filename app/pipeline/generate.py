"""
generate.py
───────────
Découpage de l'exercice source (métadonnées / énoncé / segments de questions)
et génération par paires de questions (LLM). Code déplacé par blocs depuis
routes/pythonise_routes_v2.py ; les paires restent SÉQUENTIELLES (contexte
partagé : chaque appel reçoit les blocs déjà générés).
"""

from __future__ import annotations

import json
import logging
import re
from typing import Callable, Optional

from app.config import USE_REASONING
from app.llm.client import process_with_openrouter
from app.pipeline.postprocess import (
    PYTHON_FENCE_RE,
    normalize_python_fences,
    strip_fences,
)
from app.pipeline.prompts import STEP_PAIR_PROMPT, SYSTEM_PROMPT

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────────────────────
# Découpage du source MyST
# ─────────────────────────────────────────────────────────────────────────────

def strip_python_block_from_text(text: str) -> str:
    """Retire les blocs {python} d'un texte (le Python est régénéré par paire)."""
    cleaned = PYTHON_FENCE_RE.sub("", text)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return cleaned.strip()


def split_metadata_and_enonce(header: str) -> tuple[str, str]:
    """Sépare l'en-tête en (métadonnées directives, énoncé libre)."""
    lines = header.splitlines()
    OPTION_RE = re.compile(r"^\s*:[A-Za-z_][\w-]*:")
    DIRECTIVE_OPEN_RE = re.compile(r"^\s*(?:`{3,}|:{3,}|\\begin)")

    metadata_end = 0
    found_enonce = False
    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped:
            metadata_end = i + 1
            continue
        if (OPTION_RE.match(line) or DIRECTIVE_OPEN_RE.match(line)
                or stripped in ("}", "{")):
            metadata_end = i + 1
            continue
        found_enonce = True
        break

    if not found_enonce:
        return header.rstrip(), ""

    while metadata_end > 0 and not lines[metadata_end - 1].strip():
        metadata_end -= 1
    return "\n".join(lines[:metadata_end]), "\n".join(lines[metadata_end:]).strip()


def split_original_questions(content: str) -> tuple[str, str, list[str]]:
    """
    Découpe l'exercice en (métadonnées, énoncé, segments de questions).
    Chaque segment = [texte inter-question éventuel] + bloc :::::{question}.
    Entrée non-MyST (pas de :::::{question}) → ("", content, []).
    """
    if ":::::{question}" not in content:
        return "", content, []

    first_q = content.index(":::::{question}")
    metadata, enonce = split_metadata_and_enonce(content[:first_q])
    enonce = strip_python_block_from_text(enonce)
    body_part = content[first_q:]

    pattern = re.compile(r":::::\{question\}.*?:::::", re.DOTALL)
    segments: list[str] = []
    last_end = 0
    for m in pattern.finditer(body_part):
        inter_text = strip_python_block_from_text(body_part[last_end:m.start()].strip())
        segments.append(f"{inter_text}\n\n{m.group(0)}" if inter_text else m.group(0))
        last_end = m.end()
    return metadata, enonce, segments


def build_exercise_metadata(metadata: str, lists_of_notions: str) -> str:
    """En-tête déterministe (aucun LLM) — injecte les notions à côté de
    :involvedConcepts: TYPE_BAC."""
    cleaned = strip_python_block_from_text(metadata)
    if lists_of_notions and lists_of_notions not in cleaned:
        cleaned = re.sub(
            r":involvedConcepts:\s*TYPE_BAC(?![\w,])",
            f":involvedConcepts: TYPE_BAC,{lists_of_notions}",
            cleaned,
            count=1,
        )
    return cleaned.rstrip()


def assemble_exercise(metadata_header: str, pair_blocks: list[str]) -> str:
    """Header + blocs de paires + fence finale 5 backticks. Les fences {python}
    sont normalisées à la convention plateforme (4 backticks)."""
    parts = [metadata_header.rstrip()]
    parts.extend(block.strip() for block in pair_blocks)
    parts.append("`````")
    assembled = "\n\n".join(parts)
    assembled = assembled.replace("{align*}", "{equation*}")
    return normalize_python_fences(assembled)


# ─────────────────────────────────────────────────────────────────────────────
# Génération par paires
# ─────────────────────────────────────────────────────────────────────────────

_LANG_DIRECTIVES = {
    "fr":   "Langue cible de CETTE sortie : FRANÇAIS uniquement (décimales à virgule).",
    "en":   "Langue cible de CETTE sortie : ANGLAIS uniquement (décimales à point).",
    "both": ("Langue cible de CETTE sortie : BILINGUE — chaque prose en rôles "
             "{fr}`…`{en}`…` symétriques (cf. règle bilingue ci-dessus)."),
    "auto": "Langue cible : MÊME langue(s) que la source (ne traduis rien).",
}


def generate_pair_blocks(
    content: str,
    exercise_header: str,
    enonce: str,
    question_segments: list[str],
    analysis: dict,
    functions_ctx: str,
    fewshot: str,
    targeted_rules_digest: str,
    property_constraints_text: str,
    level: str,
    model_idx: int,
    lang: str = "auto",
    set_step: Optional[Callable[[str], None]] = None,
) -> list[str]:
    """Boucle de génération par paires (séquentielle). Retourne les blocs."""
    nb_questions = analysis.get("nb_questions", max(1, len(question_segments)))
    lang_directive = _LANG_DIRECTIVES.get(lang, _LANG_DIRECTIVES["auto"])
    common = dict(
        analysis=json.dumps(analysis, ensure_ascii=False, indent=2),
        functions=functions_ctx or "Aucune fonction spécifique détectée.",
        niveau=level or "non précisé",
        targeted_rules=targeted_rules_digest,
        property_constraints=property_constraints_text,
        fewshot=fewshot,
        lang_directive=lang_directive,
        nb_total=nb_questions,
    )

    generated: list[str] = []

    if not question_segments:
        # Entrée texte brut → une seule génération.
        if set_step:
            set_step("Génération (bloc Python + toutes les questions)…")
        raw = process_with_openrouter(
            prompt=STEP_PAIR_PROMPT.format(
                content=content,
                previous_blocks="(aucun — première génération)",
                nb_current=nb_questions,
                range_label=f"1–{nb_questions}",
                current_segment=content,
                **common,
            ),
            model_idx=model_idx,
            max_tokens=30000,
            system_prompt=SYSTEM_PROMPT,
            reasoning=USE_REASONING,
        )
        return [strip_fences(raw)]

    pairs = [question_segments[i: i + 2] for i in range(0, len(question_segments), 2)]
    for pair_idx, pair in enumerate(pairs):
        q_start = pair_idx * 2 + 1
        q_end = min(pair_idx * 2 + len(pair), nb_questions)
        range_label = str(q_start) if q_start == q_end else f"{q_start}–{q_end}"
        if set_step:
            set_step(f"Génération questions {range_label} / {nb_questions}…")

        current_segment = "\n\n".join(pair)
        if pair_idx == 0 and enonce:
            current_segment = enonce + "\n\n" + current_segment

        raw_pair = process_with_openrouter(
            prompt=STEP_PAIR_PROMPT.format(
                content=exercise_header,
                previous_blocks=("\n\n".join(generated) if generated
                                 else "(aucun — première paire)"),
                nb_current=len(pair),
                range_label=range_label,
                current_segment=current_segment,
                **common,
            ),
            model_idx=model_idx,
            temperature=0.4,
            max_tokens=16384,
            system_prompt=SYSTEM_PROMPT,
            reasoning=USE_REASONING,
        )
        generated.append(strip_fences(raw_pair))

    return generated
