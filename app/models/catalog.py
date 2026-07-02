"""
catalog.py — catalogue des modèles candidats par rôle. SANS Fable
(claude-fable-5 retiré volontairement de toute liste utilisable — §7).

Chaque entrée décrit sa route DIRECTE fournisseur (api_format anthropic|openai,
base_url, api_key_env) ET sa route de repli OpenRouter (openrouter_id). La
résolution effective (app/models/client.py) prend la clé directe si présente,
sinon OPENROUTER_API_KEY — un modèle sans aucune clé est « non testé ».

⚠️ IDs vérifiés sur l'API OpenRouter le 2026-07-02. Écarts vs la spec §3.2 :
  • gemini-3-1-pro / gemini-3-flash absents → mappés sur gemini-2.5-pro/flash ;
  • magistral-medium indisponible sur OpenRouter → retiré des candidats audit ;
  • grok-4-1-fast inexistant → retiré des candidats mécanique.
"""

ROLES = ("generate", "audit", "mecanique")

_ANTHROPIC = dict(provider="anthropic", api_format="anthropic",
                  base_url="https://api.anthropic.com/v1",
                  api_key_env="ANTHROPIC_API_KEY")
_OPENAI = dict(provider="openai", api_format="openai",
               base_url="https://api.openai.com/v1",
               api_key_env="OPENAI_API_KEY")
_GEMINI = dict(provider="google", api_format="openai",
               base_url="https://generativelanguage.googleapis.com/v1beta/openai",
               api_key_env="GEMINI_API_KEY")
_XAI = dict(provider="x-ai", api_format="openai",
            base_url="https://api.x.ai/v1", api_key_env="XAI_API_KEY")
_DEEPSEEK = dict(provider="deepseek", api_format="openai",
                 base_url="https://api.deepseek.com/v1",
                 api_key_env="DEEPSEEK_API_KEY")
_MOONSHOT = dict(provider="moonshot", api_format="anthropic",
                 base_url="https://api.moonshot.ai/anthropic",
                 api_key_env="MOONSHOT_API_KEY")
_ZAI = dict(provider="z-ai", api_format="openai",
            base_url="https://api.z.ai/api/paas/v4",
            api_key_env="ZAI_API_KEY")
_MISTRAL = dict(provider="mistral", api_format="openai",
                base_url="https://api.mistral.ai/v1",
                api_key_env="MISTRAL_API_KEY")
_MINIMAX = dict(provider="minimax", api_format="openai",
                base_url="https://api.minimax.io/v1",
                api_key_env="MINIMAX_API_KEY")


def _m(key, base, direct_id, openrouter_id, roles, cache=True, batch=True):
    return key, {**base, "model_id": direct_id, "openrouter_id": openrouter_id,
                 "roles": tuple(roles), "supports_cache": cache, "supports_batch": batch}


CATALOG: dict = dict([
    # ── GENERATE (frontière + quasi-frontière) ───────────────────────────────
    _m("claude-sonnet-5", _ANTHROPIC, "claude-sonnet-5",
       "anthropic/claude-sonnet-5", ("generate",)),
    _m("claude-opus-4-8", _ANTHROPIC, "claude-opus-4-8",
       "anthropic/claude-opus-4.8", ("generate", "audit")),
    _m("gpt-5-4", _OPENAI, "gpt-5.4", "openai/gpt-5.4", ("generate",)),
    _m("gemini-3-1-pro", _GEMINI, "gemini-2.5-pro",       # mappé (3.1 absent)
       "google/gemini-2.5-pro", ("generate", "audit")),
    _m("grok-4-3", _XAI, "grok-4.3", "x-ai/grok-4.3", ("generate", "audit")),
    _m("kimi-k2-6", _MOONSHOT, "kimi-k2.6",
       "moonshotai/kimi-k2.6", ("generate", "audit")),
    _m("glm-5-2", _ZAI, "glm-5.2", "z-ai/glm-5.2", ("generate",)),
    _m("deepseek-v4-pro", _DEEPSEEK, "deepseek-v4-pro",
       "deepseek/deepseek-v4-pro", ("generate", "audit")),
    _m("mistral-large-3", _MISTRAL, "mistral-large-2512",
       "mistralai/mistral-large-2512", ("generate",)),
    # ── MECANIQUE (rapide / bon marché) ──────────────────────────────────────
    _m("claude-haiku-4-5", _ANTHROPIC, "claude-haiku-4-5",
       "anthropic/claude-haiku-4.5", ("mecanique",)),
    _m("mistral-small", _MISTRAL, "mistral-small-3.2",
       "mistralai/mistral-small-3.2-24b-instruct", ("mecanique",), cache=False),
    _m("deepseek-v4-flash", _DEEPSEEK, "deepseek-v4-flash",
       "deepseek/deepseek-v4-flash", ("mecanique",)),
    _m("glm-4-7-flash", _ZAI, "glm-4.7-flash",
       "z-ai/glm-4.7-flash", ("mecanique",)),
    _m("gemini-3-flash", _GEMINI, "gemini-2.5-flash",     # mappé (3-flash absent)
       "google/gemini-2.5-flash", ("mecanique",)),
    _m("gpt-5-4-nano", _OPENAI, "gpt-5.4-nano",
       "openai/gpt-5.4-nano", ("mecanique",)),
    # minimax-m3 : catalogue §3.3, candidat d'appoint générique.
    _m("minimax-m3", _MINIMAX, "minimax-m3",
       "minimax/minimax-m3", ("mecanique",), cache=False),
])

# Candidats par rôle (ordre indicatif ; le banc trie par ses mesures).
CANDIDATES = {
    role: [k for k, v in CATALOG.items() if role in v["roles"]]
    for role in ROLES
}


def model_info(key: str) -> dict:
    if key not in CATALOG:
        raise KeyError(f"Modèle inconnu au catalogue : {key!r}")
    return CATALOG[key]
