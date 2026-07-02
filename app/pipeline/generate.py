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

from app.config import EXERCISE_FENCE_BACKTICKS, USE_REASONING
from app.llm.client import process_with_openrouter
from app.pipeline.postprocess import (
    PYTHON_FENCE_RE,
    normalize_python_fences,
    strip_fences,
)
from app.pipeline.prompts import (
    FGQ_SPEC,
    MCQ_SPEC,
    STEP_DECLINAISON_PROMPT,
    STEP_PAIR_PROMPT,
    SYSTEM_PROMPT,
)

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


# Le sélecteur UI envoie ""/"Intermediate"/"Advanced"/"Elementary" ; la
# plateforme attend Elementary/Intermediary/Advanced (noter Intermediary).
_LEVEL_MAP = {
    "": "",
    "elementary": "Elementary",
    "intermediate": "Intermediary",
    "intermediary": "Intermediary",
    "advanced": "Advanced",
}

# Ordre canonique des options de l'en-tête {exercise} (gabarit plateforme).
_HEADER_FIELDS = [
    "id", "title", "modules", "recommendedExecutionTime", "level",
    "chap", "involvedConcepts", "originalSource", "visibility",
]


def _parse_source_options(metadata: str) -> dict:
    """Extrait les `:option: valeur` de l'en-tête source (s'il en a un)."""
    opts: dict[str, str] = {}
    for m in re.finditer(r"^[ \t]*:([A-Za-z_][\w-]*):[ \t]*(.*?)[ \t]*$",
                         metadata or "", re.MULTILINE):
        opts[m.group(1)] = m.group(2).strip()
    return opts


def _norm_level(value: str) -> str:
    return _LEVEL_MAP.get((value or "").strip().lower(), (value or "").strip())


def build_exercise_metadata(
    metadata: str,
    lists_of_notions: str,
    analysis: dict | None = None,
    level: str = "",
    decl_type: str | None = None,
) -> str:
    """Construit TOUJOURS un en-tête `{exercise}` complet et bien formé
    (5 backticks englobant tout l'exercice — le bloc Python à 4 backticks vient
    juste après). Règles par champ (consigne utilisateur) :
      • :id: vide (auto-attribution plateforme)
      • :title: titre de la source sinon titre déduit de l'analyse
      • :modules: / :chap: repris de la source si présents, sinon vides
      • :recommendedExecutionTime: source sinon défaut (≈ 3 min/question)
      • :level: selon le niveau SÉLECTIONNÉ dans l'UI (mappé Intermediary),
        sinon niveau de la source, sinon Elementary
      • :involvedConcepts: notions retrouvées (RAG) sinon concepts de la source
      • :originalSource: repris de la source si présent
      • :visibility: All par défaut
    Reprend le MAXIMUM des métadonnées présentes dans la source."""
    analysis = analysis or {}
    src = _parse_source_options(metadata)

    title = src.get("title") or analysis.get("exercise_title") or "Exercice"
    if decl_type:
        # Suffixe de traçabilité (convention des exemples validés : « - MCQ »).
        suffix = " - MCQ" if decl_type == "qcm" else " - QAT"
        if not title.rstrip().endswith(suffix.strip()):
            title = title.rstrip() + suffix

    nb_q = analysis.get("nb_questions") or 0
    try:
        nb_q = int(nb_q)
    except (TypeError, ValueError):
        nb_q = 0
    ret = src.get("recommendedExecutionTime") or str(max(5, nb_q * 3) if nb_q else 10)

    lvl = _norm_level(level) or _norm_level(src.get("level", "")) or "Elementary"

    concepts = (lists_of_notions or "").strip() or src.get("involvedConcepts", "")
    # "TYPE_BAC" est un placeholder de gabarit, pas un vrai concept → on l'ôte.
    concepts = concepts.replace("TYPE_BAC,", "").replace("TYPE_BAC", "").strip().strip(",")

    values = {
        "id": "",                                   # vide → la plateforme l'attribue
        "title": title,
        "modules": src.get("modules", ""),          # repris si présent, sinon vide
        "recommendedExecutionTime": ret,
        "level": lvl,
        "chap": src.get("chap", ""),                # repris si présent, sinon vide
        "involvedConcepts": concepts,
        "originalSource": src.get("originalSource", ""),
        "visibility": src.get("visibility") or "All",
    }

    fence = "`" * EXERCISE_FENCE_BACKTICKS
    lines = [f"{fence}{{exercise}}"]
    for k in _HEADER_FIELDS:
        lines.append(f":{k}: {values[k]}".rstrip())
        # Déclinaison d'un exercice existant : tracer l'id source juste après :id:
        # (convention des exemples validés : :originalExerciseId:).
        if k == "id" and decl_type and src.get("id"):
            lines.append(f":originalExerciseId: {src['id']}")
    return "\n".join(lines)


_ENVELOPE_FENCE_RE = re.compile(r"(?m)^`{5,}(\{exercise\})?[ \t]*$")


def assemble_exercise(metadata_header: str, pair_blocks: list[str]) -> str:
    """En-tête `{exercise}` (posé par build_exercise_metadata) + blocs de paires
    + fence finale 5 backticks qui referme l'enveloppe APRÈS la dernière question.
    Les fences {python} sont normalisées à 4 backticks (convention plateforme).
    Filet : on retire toute ligne d'enveloppe 5-backticks que le LLM aurait
    reproduite dans un bloc (on possède l'enveloppe nous-mêmes) — sinon on
    obtiendrait une double enveloppe / des backticks non décroissants."""
    parts = [metadata_header.rstrip()]
    for block in pair_blocks:
        cleaned = _ENVELOPE_FENCE_RE.sub("", block).strip()
        if cleaned:
            parts.append(cleaned)
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


_DECL_LABELS = {"qcm": "QCM (MCQ)", "qat": "QAT (FGQ)"}
_DECL_SPECS = {"qcm": MCQ_SPEC, "qat": FGQ_SPEC}


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
    decl_type: Optional[str] = None,
    model: Optional[str] = None,
) -> list[str]:
    """Boucle de génération par paires (séquentielle). Retourne les blocs.
    `decl_type` (qcm|qat) bascule sur le prompt Déclinaisons — même mécanique
    par paires, 1 question source → 1 question déclinée."""
    nb_questions = analysis.get("nb_questions", max(1, len(question_segments)))
    lang_directive = _LANG_DIRECTIVES.get(lang, _LANG_DIRECTIVES["auto"])
    if decl_type:
        prompt_tmpl = STEP_DECLINAISON_PROMPT
        common = dict(
            analysis=json.dumps(analysis, ensure_ascii=False, indent=2),
            functions=functions_ctx or "Aucune fonction spécifique détectée.",
            niveau=level or "non précisé",
            fewshot=fewshot,
            lang_directive=lang_directive,
            nb_total=nb_questions,
            decl_label=_DECL_LABELS[decl_type],
            decl_spec=_DECL_SPECS[decl_type],
        )
    else:
        prompt_tmpl = STEP_PAIR_PROMPT
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
            prompt=prompt_tmpl.format(
                content=content,
                previous_blocks="(aucun — première génération)",
                nb_current=nb_questions,
                range_label=f"1–{nb_questions}",
                current_segment=content,
                **common,
            ),
            model_idx=model_idx,
            model=model,
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
            prompt=prompt_tmpl.format(
                content=exercise_header,
                previous_blocks=("\n\n".join(generated) if generated
                                 else "(aucun — première paire)"),
                nb_current=len(pair),
                range_label=range_label,
                current_segment=current_segment,
                **common,
            ),
            model_idx=model_idx,
            model=model,
            temperature=0.4,
            max_tokens=16384,
            system_prompt=SYSTEM_PROMPT,
            reasoning=USE_REASONING,
        )
        generated.append(strip_fences(raw_pair))

    return generated
