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

# ── Version applicative (exposée par /health pour vérifier un déploiement) ───
# Bumper à chaque déploiement significatif : permet de répondre « à jour ? »
# sans se connecter (curl /health → champ "version").
APP_VERSION = "2026-07-07c — QCM (qualitatif/bilingue/objet complet) + skip quota OpenAI"

# ── Convention MyST (vérifiée empiriquement : 222/222 exemples plateforme) ───
# Bloc {python} = 4 backticks ; enveloppe {exercise} = 5 backticks.
PYTHON_FENCE_BACKTICKS = 4
EXERCISE_FENCE_BACKTICKS = 5

# ── Modèles LLM (IDs vérifiés sur l'API OpenRouter le 2026-07-02) ────────────
# NOTE : claude-fable-5 retiré volontairement (§7 du prompt banc multi-modèles).
AVAILABLE_MODELS = {
    0: "anthropic/claude-opus-4.8",
    1: "anthropic/claude-sonnet-5",
    2: "anthropic/claude-haiku-4.5",
    3: "google/gemini-2.5-pro",
    4: "openai/gpt-5.4",
}
DEFAULT_MODEL_IDX = 1            # claude-sonnet-5

# Modèle de l'étape d'analyse : None = suivre le modèle choisi par l'utilisateur
# (corrige le model_idx=2 codé en dur de l'ancienne version) ; un int force un
# modèle dédié pour l'analyse.
ANALYSIS_MODEL_IDX: int | None = None

# Modèle du juge de notions (appel léger, JSON court). DOIT supporter
# response_format=json_object côté OpenRouter (modèles OpenAI — les Claude
# le rejettent et le retriever dégrade en contexte vide).
NOTIONS_MODEL = "openai/gpt-5-mini"

# Prix $/M tokens (fallback si l'API generation ne renvoie pas le coût réel).
# Relevés sur openrouter.ai le 2026-07-02. Source détaillée (cache/batch) :
# app/models/prices.json — à re-vérifier avant prod, ça bouge chaque semaine.
MODEL_PRICING = {
    "anthropic/claude-opus-4.8":   {"input": 5.0,   "output": 25.0},
    "anthropic/claude-sonnet-5":   {"input": 2.0,   "output": 10.0},
    "anthropic/claude-haiku-4.5":  {"input": 1.0,   "output": 5.0},
    "google/gemini-2.5-pro":       {"input": 1.25,  "output": 10.0},
    "google/gemini-2.5-flash":     {"input": 0.3,   "output": 2.5},
    "openai/gpt-5.4":              {"input": 2.5,   "output": 15.0},
    "openai/gpt-5.4-nano":         {"input": 0.2,   "output": 1.25},
    "x-ai/grok-4.3":               {"input": 1.25,  "output": 2.5},
    "moonshotai/kimi-k2.6":        {"input": 0.55,  "output": 3.2},
    "z-ai/glm-5.2":                {"input": 0.93,  "output": 3.0},
    "z-ai/glm-4.7-flash":          {"input": 0.06,  "output": 0.4},
    "deepseek/deepseek-v4-pro":    {"input": 0.435, "output": 0.87},
    "deepseek/deepseek-v4-flash":  {"input": 0.089, "output": 0.18},
    "mistralai/mistral-large-2512": {"input": 0.5,  "output": 1.5},
    "mistralai/mistral-small-3.2-24b-instruct": {"input": 0.075, "output": 0.2},
    "minimax/minimax-m3":          {"input": 0.3,   "output": 1.2},
}

# ── Politique de sélection de modèle (banc multi-modèles, §5) ────────────────
DEFAULT_POLICY = "auto"          # auto | best | cheap | manual
SEUIL_VERT = 0.90                # taux VERT minimal pour qu'un modèle « tienne »
MAX_ESCALADES = 3                # plafond d'échelons gravis en mode auto
PRICES_PATH = PACKAGE_DIR / "models" / "prices.json"
RECOMMENDED_PATH = PACKAGE_DIR / "models" / "recommended.json"
# Choix explicites du mode `manual` (clés du catalogue app/models/catalog.py).
MODEL_GENERATE = "claude-sonnet-5"
MODEL_AUDIT = "claude-opus-4-8"
MODEL_MECANIQUE = "claude-haiku-4-5"

# ── Pipeline ─────────────────────────────────────────────────────────────────
RAG_TOP_K            = 10        # catalogue RAG (était 3 — trop étroit)
RAG_EMBEDDING_MODEL  = "openai-3-small"
MAX_AUDIT_ITERATIONS = 2
USE_REASONING        = False     # extended thinking sur les appels de génération
REASONING_CONFIG     = {"max_tokens": 4000}   # utilisé seulement si USE_REASONING
MULTI_SEED_NUM       = 100       # graines de la validation d'invariants (règle 4.3)
HARNESS_GATE_SEEDS   = 100       # graines de la porte harnais en fin de pipeline
HARNESS_REPAIR_MAX   = 2         # boucles de réparation LLM si la porte est rouge

# ── Audit pédagogique des déclinaisons (au-delà du harnais mécanique) ────────
# Juge LLM de la QUALITÉ (distracteurs cohérents, indevinabilité, consignes)
# après une sortie VERTE au harnais. Coût : +1 appel LLM/déclinaison (+1 si
# réparation). Mettre PEDAGO_AUDIT_ENABLED=False pour revenir au harnais seul.
PEDAGO_AUDIT_ENABLED    = True
PEDAGO_REPAIR_MAX       = 1      # réparations pédagogiques ciblées (structure préservée)
PEDAGO_ESCALATE_IN_AUTO = True   # mode auto : escalade de modèle si qualité insuffisante
# Modèle du JUGE pédagogique (constant, indépendant du modèle de génération qui
# escalade). Exige un fort raisonnement ET un JSON fiable — deepseek-v4-pro (rôle
# audit) renvoyait content=null sur ce prompt (2026-07-06). Repli = NOTIONS_MODEL
# (OpenAI, JSON garanti) si le primaire échoue encore. IDs OpenRouter en chaîne.
PEDAGO_AUDIT_MODEL      = "openai/gpt-5.4"

# ── Langue cible ─────────────────────────────────────────────────────────────
DEFAULT_LANG = "fr"              # "fr" | "en" | "both"

# ── Modes (pythonisation / déclinaisons QCM-QAT) ─────────────────────────────
DEFAULT_MODE = "pythonise"       # "pythonise" | "declinaisons"
DECLINAISON_TYPES = ("qcm", "qat")
MCQ_NUM_OPTIONS = 5              # 1 correcte + 3 distracteurs + « None » en dernier
QAT_FALLBACK_TO_MCQ = True       # question non auto-corrigeable en champ libre → MCQ

# ── Serveur / jobs ───────────────────────────────────────────────────────────
JOB_TTL = 1800                   # s avant purge d'un job terminé
# HOST/PORT pilotables par l'environnement (déploiement). En local : 127.0.0.1.
# En conteneur (Hugging Face Spaces) : HOST=0.0.0.0, PORT=7860 (imposé par HF).
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "5000"))
