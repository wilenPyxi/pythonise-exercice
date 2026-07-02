"""
client.py — adaptateur fournisseur unifié (§3.1).

Une seule interface :
    ModelClient().complete(system, messages, model_key, **opts)
      -> {"text", "usage_in", "usage_out", "latency_ms", "route"}

Dispatch par entrée de catalogue : {api_format ∈ {anthropic, openai}, base_url,
api_key_env, model_id, openrouter_id}. Résolution de route :
  1. clé DIRECTE du fournisseur présente (api_key_env) → endpoint natif ;
  2. sinon OPENROUTER_API_KEY présente → route OpenRouter (format openai) ;
  3. sinon MissingKeyError — le banc marque « non testé (clé absente) »,
     jamais une erreur bloquante.
"""

from __future__ import annotations

import logging
import os
import random
import time

import requests

from app.models.catalog import model_info

logger = logging.getLogger(__name__)

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


class MissingKeyError(RuntimeError):
    """Aucune clé disponible pour ce modèle (direct + OpenRouter absents)."""


def resolve_route(model_key: str) -> dict:
    """Route effective pour un modèle : direct si sa clé est là, sinon
    OpenRouter. Lève MissingKeyError si aucune clé."""
    info = model_info(model_key)
    direct_key = os.getenv(info["api_key_env"], "")
    if direct_key:
        return {"kind": "direct", "api_format": info["api_format"],
                "base_url": info["base_url"], "model": info["model_id"],
                "key": direct_key}
    or_key = os.getenv("OPENROUTER_API_KEY", "")
    if or_key:
        return {"kind": "openrouter", "api_format": "openai",
                "base_url": OPENROUTER_URL, "model": info["openrouter_id"],
                "key": or_key}
    raise MissingKeyError(
        f"{model_key}: ni {info['api_key_env']} ni OPENROUTER_API_KEY présente")


def is_available(model_key: str) -> bool:
    try:
        resolve_route(model_key)
        return True
    except (MissingKeyError, KeyError):
        return False


class ModelClient:
    """Client fin multi-fournisseurs avec retries (backoff + jitter, 429)."""

    def __init__(self, max_retries: int = 3, timeout: int = 180):
        self.max_retries = max_retries
        self.timeout = timeout

    def complete(self, system: str, messages: list, model_key: str,
                 temperature: float = 0.0, max_tokens: int = 4096) -> dict:
        route = resolve_route(model_key)
        t0 = time.time()
        if route["api_format"] == "anthropic" and route["kind"] == "direct":
            out = self._anthropic(route, system, messages, temperature, max_tokens)
        else:
            out = self._openai(route, system, messages, temperature, max_tokens)
        out["latency_ms"] = int((time.time() - t0) * 1000)
        out["route"] = route["kind"]
        return out

    # ── formats ──────────────────────────────────────────────────────────────

    def _anthropic(self, route, system, messages, temperature, max_tokens) -> dict:
        url = route["base_url"].rstrip("/") + "/messages"
        headers = {"x-api-key": route["key"],
                   "anthropic-version": "2023-06-01",
                   "content-type": "application/json"}
        payload = {"model": route["model"], "system": system,
                   "messages": messages, "temperature": temperature,
                   "max_tokens": max_tokens}
        data = self._post(url, headers, payload)
        text = "".join(b.get("text", "") for b in data.get("content", [])
                       if b.get("type") == "text")
        usage = data.get("usage", {})
        return {"text": text,
                "usage_in": usage.get("input_tokens", 0),
                "usage_out": usage.get("output_tokens", 0)}

    def _openai(self, route, system, messages, temperature, max_tokens) -> dict:
        url = (route["base_url"] if route["kind"] == "openrouter"
               else route["base_url"].rstrip("/") + "/chat/completions")
        headers = {"Authorization": f"Bearer {route['key']}",
                   "Content-Type": "application/json"}
        payload = {"model": route["model"],
                   "messages": [{"role": "system", "content": system}] + messages,
                   "temperature": temperature, "max_tokens": max_tokens}
        data = self._post(url, headers, payload)
        text = data["choices"][0]["message"]["content"]
        usage = data.get("usage", {})
        return {"text": text,
                "usage_in": usage.get("prompt_tokens", 0),
                "usage_out": usage.get("completion_tokens", 0)}

    def _post(self, url, headers, payload) -> dict:
        for attempt in range(self.max_retries):
            try:
                resp = requests.post(url, json=payload, headers=headers,
                                     timeout=self.timeout)
                if resp.status_code == 429:
                    wait = 2 * (2 ** attempt) + random.uniform(0, 4)
                    logger.warning("429 sur %s — retry dans %.1fs", url, wait)
                    time.sleep(wait)
                    continue
                resp.raise_for_status()
                data = resp.json()
                if "error" in data:
                    raise RuntimeError(f"API error: {data['error']}")
                return data
            except (requests.RequestException, RuntimeError) as e:
                if attempt == self.max_retries - 1:
                    raise
                wait = 2 * (2 ** attempt) + random.uniform(0, 4)
                logger.warning("Erreur %s — retry dans %.1fs", e, wait)
                time.sleep(wait)
        raise RuntimeError("Échec après retries")
