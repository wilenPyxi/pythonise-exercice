"""
fewshots.py
───────────
Banque de few-shots par type d'exercice, tirée des exemples pythonisés LIVRÉS
de la plateforme (Exemples d'exercices/master_all → app/knowledge/fewshots/).
Seuls des exemples VERTS au harnais sont admis comme modèles positifs.

Sélection : mots-clés sur (exercise_type + title + concepts) de l'analyse.
Injection : version ÉLAGUÉE (bloc python + énoncé + 1re question) pour
limiter le coût en contexte.
"""

from __future__ import annotations

import logging
import re
from functools import lru_cache

from app.config import FEWSHOTS_DIR

logger = logging.getLogger(__name__)

# Ordre = priorité (premier motif qui matche gagne).
_TYPE_KEYWORDS: list[tuple[str, str]] = [
    ("figure",      r"figure|graph|matplotlib|trac[ée]|courbe|repr[ée]sent|parabole.*dessin"),
    ("integration", r"int[ée]gra|primitive|\bipp\b|parties"),
    ("systemes",    r"syst[èe]me"),
    ("logexp",      r"\blog\b|logarithm|exponentiel|exposant|puissance"),
    ("quadratique", r"trin[ôo]me|quadrat|second degr[ée]|discriminant|racine|factoris"),
    ("equations",   r"[ée]quation|in[ée]quation|lin[ée]aire|affine|int[ée]r[êe]t|seuil|finance|proportion"),
]
_DEFAULT_KEY = "equations"

_Q_BLOCK_RE = re.compile(r":::::\{question\}.*?:::::", re.DOTALL)
_PY_BLOCK_RE = re.compile(r"(?ms)^(`{3,4})\{python\}[ \t]*\n.*?\n\1[ \t]*$")


def pick_fewshot_key(analysis: dict) -> str:
    """Choisit la clé de few-shot selon le type détecté par l'analyse."""
    haystack = " ".join([
        str(analysis.get("exercise_type", "")),
        str(analysis.get("exercise_title", "")),
        " ".join(str(c) for c in (analysis.get("suggested_concepts") or [])),
    ]).lower()
    if analysis.get("needs_matplotlib"):
        return "figure"
    for key, pattern in _TYPE_KEYWORDS:
        if re.search(pattern, haystack):
            return key
    return _DEFAULT_KEY


@lru_cache(maxsize=None)
def load_fewshot(key: str) -> str:
    """Few-shot élagué : bloc python + énoncé + 1re question de l'exemple
    canonique. Chaîne vide si le fichier manque (le prompt reste valable)."""
    path = FEWSHOTS_DIR / f"{key}.md"
    if not path.exists():
        logger.warning("Few-shot absent : %s", path)
        return ""
    text = path.read_text(encoding="utf-8")

    py = _PY_BLOCK_RE.search(text)
    first_q = _Q_BLOCK_RE.search(text)
    if not py or not first_q:
        return ""

    # Énoncé = texte entre la fin du bloc python et la 1re question.
    enonce = text[py.end():first_q.start()].strip()
    parts = [py.group(0)]
    if enonce:
        parts.append(enonce)
    parts.append(first_q.group(0))
    return "\n\n".join(parts)


def fewshot_for(analysis: dict) -> str:
    key = pick_fewshot_key(analysis)
    shot = load_fewshot(key)
    logger.info("Few-shot sélectionné : %s (%d caractères)", key, len(shot))
    return shot or "(aucun exemple canonique disponible pour ce type)"


@lru_cache(maxsize=None)
def fewshot_for_declinaison(decl_type: str) -> str:
    """Exemple canonique COMPLET pour une déclinaison (qcm|qat) — fichiers
    stricts (conventions corpus 222) calibrés sur les 33 exemples validés de
    fewshots/declinaisons/. Complet (pas élagué) : la structure mcqAnswer /
    :solution:/displayedSolution est le cœur de ce qu'il faut imiter."""
    path = FEWSHOTS_DIR / f"{decl_type}.md"
    if not path.exists():
        logger.warning("Few-shot déclinaison absent : %s", path)
        return "(aucun exemple canonique disponible)"
    return path.read_text(encoding="utf-8")
