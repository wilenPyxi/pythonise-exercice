"""
translate.py
────────────
Étape langue cible (NOUVEAU — chantier E) : FR / EN / les deux.

Stratégie (sécurité d'abord) :
  • détection déterministe de la/des langue(s) source (rôles {fr}`…`{en}`…`,
    sinon heuristique de mots-outils) ;
  • cible == source → aucun appel LLM ;
  • bilingue → mono : réduction DÉTERMINISTE (on déballe la langue gardée,
    on supprime l'autre — zéro LLM, zéro risque) ;
  • mono → autre langue ou bilingue : appel LLM sur le corps avec les blocs
    Python MASQUÉS par sentinelles (le Python ne passe jamais par le LLM),
    puis garde-fous : sentinelles intactes, MÊME ensemble de {{placeholders}},
    même nombre de blocs :::::{question}. En cas d'écart → on garde la
    version non traduite + warning (jamais de sortie corrompue).
"""

from __future__ import annotations

import logging
import re

from app.llm.client import process_with_openrouter
from app.pipeline.postprocess import (
    INJECTION_RE,
    detect_languages,
    mask_python_blocks,
    strip_language,
    unmask_python_blocks,
)
from app.pipeline.prompts import (
    TRANSLATE_FORMAT_BOTH,
    TRANSLATE_FORMAT_MONO,
    TRANSLATE_PROMPT,
)

logger = logging.getLogger(__name__)

_LABELS = {"fr": "le FRANÇAIS", "en": "l'ANGLAIS", "both": "le BILINGUE FR+EN"}


def _placeholders(text: str) -> set[str]:
    return {tok.strip() for tok in INJECTION_RE.findall(text)}


def ensure_language(
    exercise: str,
    target: str,
    model_idx: int,
    model: str | None = None,
) -> tuple[str, list[dict], dict]:
    """
    Amène l'exercice dans la langue cible. Retourne
    (exercice, warnings, info={"source": …, "target": …, "action": …}).
    """
    warnings: list[dict] = []
    source = detect_languages(exercise)
    info = {"source": source, "target": target, "action": "aucune"}

    if target not in ("fr", "en", "both") or target == source:
        return exercise, warnings, info

    # Bilingue → mono : déterministe.
    if source == "both" and target in ("fr", "en"):
        info["action"] = f"réduction déterministe bilingue → {target}"
        return strip_language(exercise, keep=target), warnings, info

    # Mono → autre mono, ou mono → bilingue : LLM sur la prose seule.
    # Les sentinelles internes \x00PYBLOCKn\x00 (caractère NUL) sont
    # intransmissibles à un LLM — on les convertit en sentinelles texte
    # copiables, puis on reconvertit au retour.
    masked, blocks = mask_python_blocks(exercise)
    for i in range(len(blocks)):
        masked = masked.replace(f"\x00PYBLOCK{i}\x00", f"<<<PYBLOCK_{i}>>>")
    fmt = (TRANSLATE_FORMAT_BOTH if target == "both"
           else TRANSLATE_FORMAT_MONO.format(target_label=_LABELS[target]))
    try:
        raw = process_with_openrouter(
            prompt=TRANSLATE_PROMPT.format(
                source_label=_LABELS.get(source, source),
                target_label=_LABELS[target],
                body=masked,
                format_directive=fmt,
            ),
            model_idx=model_idx,
            model=model,
            temperature=0.0,
            max_tokens=24000,
        )
    except (RuntimeError, ValueError, OSError) as e:
        warnings.append({
            "rule": "langue",
            "message": f"Étape de traduction en échec ({e}) — sortie laissée en {source}.",
        })
        return exercise, warnings, info

    translated = raw.strip()
    translated = re.sub(r"^```\w*\s*\n", "", translated)
    translated = re.sub(r"\n```\s*$", "", translated)
    for i in range(len(blocks)):
        translated = translated.replace(f"<<<PYBLOCK_{i}>>>", f"\x00PYBLOCK{i}\x00")

    # Garde-fous structurels — si l'un casse, on n'applique PAS la traduction.
    checks = []
    for i in range(len(blocks)):
        if f"\x00PYBLOCK{i}\x00" not in translated:
            checks.append(f"sentinelle PYBLOCK{i} perdue")
    if _placeholders(translated) != _placeholders(masked):
        missing = _placeholders(masked) - _placeholders(translated)
        added = _placeholders(translated) - _placeholders(masked)
        checks.append(f"placeholders modifiés (perdus: {sorted(missing)[:4]}, ajoutés: {sorted(added)[:4]})")
    if translated.count(":::::{question}") != masked.count(":::::{question}"):
        checks.append("nombre de blocs question modifié")

    if checks:
        warnings.append({
            "rule": "langue",
            "message": ("Traduction rejetée par les garde-fous (" + " ; ".join(checks)
                        + ") — sortie laissée en " + source + "."),
        })
        return exercise, warnings, info

    info["action"] = f"traduction LLM {source} → {target}"
    return unmask_python_blocks(translated, blocks), warnings, info
