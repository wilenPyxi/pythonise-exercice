"""
analyze.py
──────────
Étape 0 du pipeline : analyse LLM (variables/règles/invariants), retriever de
notions, RAG fonctions — les trois sont INDÉPENDANTS et lancés en parallèle
(gain de latence sans aucun impact sur la correction).

Corrige au passage (vs v1) :
  • model_idx=2 codé en dur → ANALYSIS_MODEL_IDX (None = modèle utilisateur) ;
  • typo needs_matplolib → needs_matplotlib (les deux lues en transition,
    une seule orthographe en sortie) ;
  • top_k=3 → RAG_TOP_K (10).
"""

from __future__ import annotations

import json
import logging
from concurrent.futures import ThreadPoolExecutor

from app.config import ANALYSIS_MODEL_IDX, NOTIONS_XLSX, RAG_EMBEDDING_MODEL, RAG_TOP_K
from app.knowledge.rules_digest import ALL_RULE_IDS, RULES_BY_ID
from app.llm.client import process_with_openrouter
from app.pipeline.postprocess import strip_fences
from app.pipeline.prompts import STEP1_PROMPT
from app.rag.functions import retrieve_functions_context
from app.rag.notions import enrich_exercise_with_notions

logger = logging.getLogger(__name__)

# Garde-fou : dès que les embeddings OpenAI renvoient un quota épuisé (429), on
# arrête d'appeler le RAG fonctions pour le reste de la session (sinon chaque job
# repaie 3 retries + ~10 s pour un catalogue de toute façon vide). Réactivé au
# prochain démarrage (une fois le compte OpenAI rechargé).
_RAG_STATE = {"off": False}


def _is_quota_error(exc: Exception) -> bool:
    s = str(exc).lower()
    return "insufficient_quota" in s or "quota" in s or "429" in s


def _rules_menu() -> str:
    return "\n".join(f"  - {rid} — {RULES_BY_ID[rid]['title']}" for rid in ALL_RULE_IDS)


_ANALYSIS_FALLBACK = {
    "exercise_type": "Général",
    "exercise_title": "Exercice",
    "suggested_concepts": [],
    "nb_questions": 2,
    "variables": [],
    "needs_fraction": False,
    "needs_sympy": False,
    "needs_numpy": False,
    "needs_matplotlib": False,
    "mathematical_structure": "Non déterminé",
    "target_rules": [],
    "property_constraints": [],
    "has_validated_solution_in_input": False,
}


def _parse_analysis(raw: str, content: str) -> dict:
    try:
        analysis = json.loads(strip_fences(raw))
        if not isinstance(analysis, dict):
            raise json.JSONDecodeError("not a dict", raw, 0)
    except json.JSONDecodeError:
        logger.warning("Analyse LLM : JSON invalide — fallback générique utilisé.")
        analysis = dict(_ANALYSIS_FALLBACK)
        analysis["exercise_summary"] = content[:300]
    # Transition typo v1 : accepter needs_matplolib, ne sortir QUE needs_matplotlib.
    if "needs_matplolib" in analysis:
        analysis["needs_matplotlib"] = bool(
            analysis.get("needs_matplotlib") or analysis.pop("needs_matplolib")
        )
    analysis.setdefault("needs_matplotlib", False)
    return analysis


def run_analysis_phase(content: str, model_idx: int,
                       model: str | None = None) -> tuple[dict, str, str, str]:
    """
    Lance EN PARALLÈLE : analyse LLM, notions, RAG fonctions.

    Retourne (analysis, notions_ctx, lists_of_notions, functions_ctx).
    Une erreur sur notions/RAG est dégradée en contexte vide (warning loggé) ;
    une erreur sur l'analyse LLM est propagée (le pipeline n'a pas de sens sans).
    `model` (ID chaîne) prime sur model_idx — sous policy, l'analyse relève du
    rôle `mecanique` (classification, §2 du prompt banc).
    """
    analysis_model = ANALYSIS_MODEL_IDX if ANALYSIS_MODEL_IDX is not None else model_idx

    with ThreadPoolExecutor(max_workers=3, thread_name_prefix="analyse") as pool:
        f_analysis = pool.submit(
            process_with_openrouter,
            prompt=STEP1_PROMPT.format(content=content, available_rules_menu=_rules_menu()),
            model_idx=analysis_model,
            model=model,
            max_tokens=6096,
        )
        f_notions = pool.submit(enrich_exercise_with_notions, content, xlsx_path=NOTIONS_XLSX)
        # RAG fonctions : sauté si les embeddings OpenAI sont déjà « à sec ».
        f_functions = None if _RAG_STATE["off"] else pool.submit(
            retrieve_functions_context,
            exercise=content,
            embedding_model=RAG_EMBEDDING_MODEL,
            top_k=RAG_TOP_K,
            force_rebuild=False,
        )

        raw_analysis = f_analysis.result()

        try:
            notions_ctx, lists_of_notions = f_notions.result()
        except Exception as e:
            logger.warning("Retriever de notions en échec (%s) — contexte vide.", e)
            notions_ctx, lists_of_notions = "", ""

        if f_functions is None:
            functions_ctx = ""      # RAG désactivé (quota OpenAI épuisé plus tôt)
        else:
            try:
                functions_ctx = f_functions.result()["catalogue"]
            except Exception as e:
                functions_ctx = ""
                if _is_quota_error(e):
                    _RAG_STATE["off"] = True
                    logger.warning(
                        "RAG fonctions DÉSACTIVÉ pour la session : quota "
                        "d'embeddings OpenAI épuisé (429). Recharge le compte "
                        "OpenAI (platform.openai.com/billing) pour le réactiver.")
                else:
                    logger.warning("RAG fonctions en échec (%s) — catalogue vide.", e)

    analysis = _parse_analysis(raw_analysis, content)
    logger.info("Analyse : type=%s, %d variables, %d règles ciblées",
                analysis.get("exercise_type"), len(analysis.get("variables") or []),
                len(analysis.get("target_rules") or []))
    return analysis, notions_ctx, lists_of_notions, functions_ctx
