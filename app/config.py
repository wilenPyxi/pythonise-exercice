"""
config.py
─────────
Configuration centrale de l'app « Pythonise Exercice v2 ».
Toutes les constantes réglables vivent ici — une seule source de vérité.
"""

import os
from pathlib import Path

# ── Chemins ──────────────────────────────────────────────────────────────────
PACKAGE_DIR   = Path(__file__).resolve().parent          # …/pythonisation_app/app
BASE_DIR      = PACKAGE_DIR.parent                       # …/pythonisation_app
DATA_DIR      = BASE_DIR / "data"
NOTIONS_XLSX  = DATA_DIR / "notions.xlsx"
FAISS_CACHE   = DATA_DIR / "faiss_cache" / "sources"
CORPUS_DIR    = PACKAGE_DIR / "corpus"                   # 5 fichiers de fonctions PyxiScience
KNOWLEDGE_DIR = PACKAGE_DIR / "knowledge"
RULES_MD      = KNOWLEDGE_DIR / "pythonisation_rules.md"
FEWSHOTS_DIR  = KNOWLEDGE_DIR / "fewshots"
TEMPLATES_DIR = PACKAGE_DIR / "web" / "templates"

# ── Convention MyST (vérifiée empiriquement : 222/222 exemples plateforme) ───
# Bloc {python} = 4 backticks ; enveloppe {exercise} = 5 backticks.
PYTHON_FENCE_BACKTICKS = 4
EXERCISE_FENCE_BACKTICKS = 5

# ── Modèles LLM (IDs vérifiés sur l'API OpenRouter le 2026-06-12) ────────────
AVAILABLE_MODELS = {
    0: "anthropic/claude-opus-4.8",
    1: "anthropic/claude-sonnet-4.6",
    2: "anthropic/claude-fable-5",
    3: "anthropic/claude-haiku-4.5",
    4: "google/gemini-2.5-pro",
    5: "openai/gpt-5.2",
}
DEFAULT_MODEL_IDX = 1            # claude-sonnet-4.6

# Modèle de l'étape d'analyse : None = suivre le modèle choisi par l'utilisateur
# (corrige le model_idx=2 codé en dur de l'ancienne version) ; un int force un
# modèle dédié pour l'analyse.
ANALYSIS_MODEL_IDX: int | None = None

# Modèle du juge de notions (appel léger, JSON court). DOIT supporter
# response_format=json_object côté OpenRouter (modèles OpenAI — les Claude
# le rejettent et le retriever dégrade en contexte vide).
NOTIONS_MODEL = "openai/gpt-5-mini"

# Prix $/M tokens (fallback si l'API generation ne renvoie pas le coût réel).
# Relevés sur openrouter.ai le 2026-06-12.
MODEL_PRICING = {
    "anthropic/claude-opus-4.8":   {"input": 5.0,  "output": 25.0},
    "anthropic/claude-sonnet-4.6": {"input": 3.0,  "output": 15.0},
    "anthropic/claude-fable-5":    {"input": 10.0, "output": 50.0},
    "anthropic/claude-haiku-4.5":  {"input": 1.0,  "output": 5.0},
    "google/gemini-2.5-pro":       {"input": 1.25, "output": 10.0},
    "openai/gpt-5.2":              {"input": 1.75, "output": 14.0},
}

# ── Pipeline ─────────────────────────────────────────────────────────────────
RAG_TOP_K            = 10        # catalogue RAG (était 3 — trop étroit)
RAG_EMBEDDING_MODEL  = "openai-3-small"
MAX_AUDIT_ITERATIONS = 2
USE_REASONING        = False     # extended thinking sur les appels de génération
REASONING_CONFIG     = {"max_tokens": 4000}   # utilisé seulement si USE_REASONING
MULTI_SEED_NUM       = 100       # graines de la validation d'invariants (règle 4.3)
HARNESS_GATE_SEEDS   = 100       # graines de la porte harnais en fin de pipeline
HARNESS_REPAIR_MAX   = 2         # boucles de réparation LLM si la porte est rouge

# ── Langue cible ─────────────────────────────────────────────────────────────
DEFAULT_LANG = "fr"              # "fr" | "en" | "both"

# ── Serveur / jobs ───────────────────────────────────────────────────────────
JOB_TTL = 1800                   # s avant purge d'un job terminé
# HOST/PORT pilotables par l'environnement (déploiement). En local : 127.0.0.1.
# En conteneur (Hugging Face Spaces) : HOST=0.0.0.0, PORT=7860 (imposé par HF).
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "5000"))
