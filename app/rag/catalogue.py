"""
catalogue.py
────────────
Catalogue CURÉ des helpers PyxiScience (app/knowledge/functions_catalogue.md),
injecté par TRANCHE DE DOMAINE dans le prompt de génération.

Complète le RAG FAISS (app/rag/functions.py) : FAISS donne des hits sémantiques
sur le code réel (signatures/docstrings) ; ce catalogue donne la couche
« quel helper pour quel besoin » + les domaines que le corpus livré ne couvre
pas (matrices, proba, IBP). Les sections §0 (conventions) et §2 (briques
essentielles) sont toujours incluses ; la/les section(s) de domaine sont
choisies selon le type détecté à l'analyse.
"""

from __future__ import annotations

import logging
import re
from functools import lru_cache

from app.config import KNOWLEDGE_DIR

logger = logging.getLogger(__name__)

_CATALOGUE_MD = KNOWLEDGE_DIR / "functions_catalogue.md"

# Sections toujours injectées (numéros de header `## N.`).
_ALWAYS = ("0", "2")

# Domaine → (sections, motif de déclenchement sur type/title/concepts).
_DOMAINS: list[tuple[str, tuple[str, ...], str]] = [
    ("algebre_lineaire", ("6",),
     r"matric|système|systeme|déterminant|determinant|gauss|invers|"
     r"échelon|echelon|rref|vecteur|alg[eè]bre lin|linear algebra|pivot"),
    ("probabilites", ("7",),
     r"probabilit|variable al[ée]atoire|loi\b|espérance|esperance|variance|"
     r"moment|binomial|distribution|tirage al[ée]atoire de v\.?a"),
    ("integration", ("5",),
     r"int[ée]gra|primitive|\bipp\b|parties|\bibp\b"),
]
# §4 (généralistes) : injecté par défaut quand aucun domaine spécialisé ne sort
# (inéquations, coefficients, fractions, polynômes — le cas courant).
_DEFAULT_SECTIONS = ("4",)

_SECTION_RE = re.compile(r"(?m)^## (?P<num>\d+)\.\s.*$")


@lru_cache(maxsize=1)
def _sections() -> dict[str, str]:
    """Découpe le catalogue en {num_section: texte (header inclus)}."""
    if not _CATALOGUE_MD.exists():
        logger.warning("Catalogue de fonctions absent : %s", _CATALOGUE_MD)
        return {}
    text = _CATALOGUE_MD.read_text(encoding="utf-8")
    # Retire le commentaire HTML de vérification en tête.
    text = re.sub(r"^<!--.*?-->\s*", "", text, count=1, flags=re.DOTALL)
    matches = list(_SECTION_RE.finditer(text))
    out: dict[str, str] = {}
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        out[m.group("num")] = text[m.start():end].strip()
    return out


def select_sections(analysis: dict) -> list[str]:
    """Numéros de sections à injecter pour cet exercice (ordre stable)."""
    haystack = " ".join([
        str(analysis.get("exercise_type", "")),
        str(analysis.get("exercise_title", "")),
        str(analysis.get("mathematical_structure", "")),
        " ".join(str(c) for c in (analysis.get("suggested_concepts") or [])),
    ]).lower()

    domains = [secs for _name, secs, pat in _DOMAINS if re.search(pat, haystack)]
    chosen = list(_ALWAYS)
    if domains:
        for secs in domains:
            chosen.extend(secs)
    else:
        chosen.extend(_DEFAULT_SECTIONS)
    # dédup en préservant l'ordre
    return list(dict.fromkeys(chosen))


def catalogue_for(analysis: dict) -> str:
    """Tranche curée du catalogue pour le type détecté (chaîne prête à injecter)."""
    sections = _sections()
    if not sections:
        return ""
    wanted = select_sections(analysis)
    parts = [sections[n] for n in wanted if n in sections]
    logger.info("Catalogue curé : sections %s injectées", wanted)
    return "\n\n".join(parts)
