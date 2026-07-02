"""
policy.py — politique de sélection de modèle par rôle (§5).

Modes :
  auto   (défaut) : échelle ordonnée par coût croissant des modèles qui
                    tiennent SEUIL_VERT, plafonnée par `best`. Départ choisi
                    par un pré-classifieur de difficulté ; escalade d'un
                    échelon à chaque échec harnais après réparations.
  best   : modèle `best` du rôle (qualité max, coût ignoré).
  cheap  : modèle `cheap` (le moins cher qui tient le seuil).
  manual : IDs explicites par rôle (config ou requête API).

Alimentation : app/models/recommended.json (écrit par le banc). Fallback si
absent : routage par défaut ci-dessous — SANS Fable (retiré volontairement).
"""

from __future__ import annotations

import json
import logging
import re

from app.config import MODEL_AUDIT, MODEL_GENERATE, MODEL_MECANIQUE, RECOMMENDED_PATH
from app.models.catalog import CATALOG, model_info
from app.models.client import is_available

logger = logging.getLogger(__name__)

POLICIES = ("auto", "best", "cheap", "manual")

# Fallback §5.2 (si recommended.json absent) — generate = Sonnet 5 avec
# escalade Opus 4.8 ; audit = Opus 4.8 ; mécanique = Haiku 4.5. Fable exclu.
DEFAULT_RECOMMENDED = {
    "generate": {"best": "claude-opus-4-8", "cheap": "claude-sonnet-5",
                 "ladder": ["claude-sonnet-5", "claude-opus-4-8"]},
    "audit": {"best": "claude-opus-4-8", "cheap": "claude-opus-4-8",
              "ladder": ["claude-opus-4-8"]},
    "mecanique": {"best": "claude-haiku-4-5", "cheap": "claude-haiku-4-5",
                  "ladder": ["claude-haiku-4-5"]},
}


def load_recommended() -> dict:
    """recommended.json s'il existe (produit par le banc), sinon fallback."""
    try:
        data = json.loads(RECOMMENDED_PATH.read_text(encoding="utf-8"))
        roles = data.get("roles") or {}
    except (OSError, json.JSONDecodeError, AttributeError, TypeError):
        return {k: dict(v) for k, v in DEFAULT_RECOMMENDED.items()}
    try:
        merged = {}
        for role, fb in DEFAULT_RECOMMENDED.items():
            r = roles.get(role) or {}
            merged[role] = {
                "best": r.get("best") or fb["best"],
                "cheap": r.get("cheap") or fb["cheap"],
                "ladder": r.get("ladder") or fb["ladder"],
            }
        return merged
    except (OSError, json.JSONDecodeError):
        return {k: dict(v) for k, v in DEFAULT_RECOMMENDED.items()}


def _usable(keys: list) -> list:
    """Filtre : au catalogue (sans Fable, par construction) ET clé dispo."""
    out = []
    for k in keys:
        if k not in CATALOG:
            logger.warning("Modèle recommandé hors catalogue (ignoré) : %s", k)
            continue
        if not is_available(k):
            logger.warning("Modèle sans clé disponible (ignoré) : %s", k)
            continue
        out.append(k)
    return out


def ladder(role: str) -> list:
    """Échelle `auto` du rôle, coût croissant. Le plafonnement vit dans la
    DÉCISION du banc (report.decide) : l'échelle écrite dans recommended.json
    fait foi telle quelle — elle peut dépasser `best` quand des modèles de
    qualité ÉGALE existent (redondance légitime : si l'échelon `best` échoue
    sur UN exercice, un pair de même taux VERT peut réussir)."""
    rec = load_recommended()[role]
    keys = _usable(list(dict.fromkeys(rec["ladder"] + [rec["best"]])))
    if not keys:
        # Fallback élargi : tout candidat du rôle avec une clé disponible.
        from app.models.catalog import CANDIDATES
        keys = _usable(CANDIDATES[role])
    if not keys:
        raise RuntimeError(
            f"Aucun modèle utilisable pour le rôle {role!r} : "
            "aucune clé API disponible (OPENROUTER_API_KEY ou clé fournisseur).")
    return keys


# ── Pré-classifieur de difficulté (heuristique légère, zéro LLM) ─────────────

_HARD_HINTS = re.compile(
    r"Matrix|matrice|bmatrix|pmatrix|jacobien|système|systeme|"
    r"int[ée]gra|\bipp\b|r[ée]currence|dimension", re.IGNORECASE)


def classify_difficulty(content: str) -> str:
    score = 0
    if content.count(":::::{question}") >= 5:
        score += 1
    if len(content) > 6000:
        score += 1
    if _HARD_HINTS.search(content):
        score += 1
    if content.count("````{python}") + content.count("```{python}") > 1:
        score += 1
    return "difficile" if score >= 2 else "simple"


def start_rung(role: str, difficulty: str) -> int:
    """simple → échelon le moins cher ; difficile → échelon plus haut."""
    steps = ladder(role)
    if difficulty == "difficile" and len(steps) > 1:
        return min(len(steps) - 1, len(steps) // 2 if len(steps) > 2 else 1)
    return 0


# ── Résolution par rôle / tentative ──────────────────────────────────────────

def resolve(role: str, policy: str = "auto", manual: dict | None = None,
            rung: int = 0) -> str:
    """Clé catalogue du modèle à utiliser pour `role` (échelon `rung` en auto)."""
    rec = load_recommended()[role]
    if policy == "manual":
        manual = manual or {}
        key = (manual.get(role)
               or {"generate": MODEL_GENERATE, "audit": MODEL_AUDIT,
                   "mecanique": MODEL_MECANIQUE}[role])
        if key in CATALOG and is_available(key):
            return key
        logger.warning("Choix manuel %r indisponible pour %s — repli cheap.", key, role)
        policy = "cheap"
    if policy == "best":
        keys = _usable([rec["best"]]) or ladder(role)
        return keys[-1] if keys else rec["best"]
    if policy == "cheap":
        keys = _usable([rec["cheap"]]) or ladder(role)
        return keys[0] if keys else rec["cheap"]
    # auto
    steps = ladder(role)
    if not steps:
        return rec["best"]
    return steps[min(rung, len(steps) - 1)]


def openrouter_id(model_key: str) -> str:
    """Pont vers le client pipeline (route OpenRouter)."""
    return model_info(model_key)["openrouter_id"]
