"""
Client LLM OpenRouter — appels texte (+ multimodal) avec retries et tracking
des coûts. Fusion de l'ancien utils/llm_client.py et de la variante
« reasoning » (utils/llm_client_with_reasoning.py, jamais branchée) : le
raisonnement est désormais un simple paramètre `reasoning=` contrôlé par
config.USE_REASONING.
"""

import logging
import os
import random
import time
from typing import Optional, Tuple

import requests

from app.config import AVAILABLE_MODELS, REASONING_CONFIG
from app.llm.cost import get_cost_tracker, CostTracker

logger = logging.getLogger(__name__)

SYSTEM_MSG = "Vous êtes un assistant pour la génération d'exercices MystMarkdown dynamiques."


class LLMClient:
    """Client pour les appels LLM via OpenRouter avec tracking des coûts."""

    def __init__(self, track_costs: bool = True):
        self.api_key = os.getenv("OPENROUTER_API_KEY", "")
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY not found in environment variables")

        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": "http://localhost:5000",
            "Content-Type": "application/json",
        }
        self.max_retries = 3
        self.retry_delay = 2
        self.track_costs = track_costs
        self._cost_tracker: Optional[CostTracker] = None

    @property
    def cost_tracker(self) -> CostTracker:
        if self._cost_tracker is None:
            self._cost_tracker = get_cost_tracker()
        return self._cost_tracker

    def call_llm(self, prompt: str, model_idx: int = 0, temperature: float = 0.0,
                 max_tokens: int = 4096, system_prompt: str = SYSTEM_MSG,
                 reasoning: bool = False, model: str | None = None) -> str:
        """Appel LLM standard avec gestion des erreurs et retry.
        `model` (ID OpenRouter en chaîne, ex. "anthropic/claude-sonnet-5")
        court-circuite `model_idx` — c'est la voie de la policy par rôle."""
        model = model or AVAILABLE_MODELS.get(model_idx)
        if model is None:
            raise ValueError(f"model_idx {model_idx} inexistant dans AVAILABLE_MODELS")

        payload = {
            "model": model,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
        }
        if reasoning:
            payload["reasoning"] = dict(REASONING_CONFIG)

        content, generation_id = self._make_request(payload)

        if self.track_costs and generation_id:
            self.cost_tracker.track_cost(
                generation_id=generation_id,
                model=model,
                is_image=False,
                prompt=prompt,
                response=content,
            )
        return content

    def call_llm_multimodal(self, image_b64: str, prompt: str, model_idx: int,
                            temperature: float = 0.0, max_tokens: int = 4096,
                            system_prompt: str = SYSTEM_MSG) -> str:
        """Appel LLM multimodal avec image."""
        model = AVAILABLE_MODELS.get(model_idx)
        if model is None:
            raise ValueError(f"model_idx {model_idx} inexistant dans AVAILABLE_MODELS")

        payload = {
            "model": model,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": f"data:image/png;base64,{image_b64}"},
                ]},
            ],
        }
        content, generation_id = self._make_request(payload, is_multimodal=True)

        if self.track_costs and generation_id:
            self.cost_tracker.track_cost(
                generation_id=generation_id,
                model=model,
                is_image=True,
                prompt=prompt,
                response=content,
            )
        return content

    def _make_request(self, payload: dict, is_multimodal: bool = False) -> Tuple[str, Optional[str]]:
        """Requête POST avec retries (backoff exponentiel + jitter, gestion 429)."""
        for attempt in range(self.max_retries):
            try:
                resp = requests.post(self.base_url, json=payload, headers=self.headers, timeout=180)

                if resp.status_code == 429:
                    wait = self.retry_delay * (2 ** attempt) + random.uniform(0, 5)
                    logger.warning("Rate-limited (%s) ; attente %.1fs (retry %d/%d)",
                                   "multimodal" if is_multimodal else "standard",
                                   wait, attempt + 1, self.max_retries)
                    time.sleep(wait)
                    continue

                resp.raise_for_status()
                data = resp.json()

                if "error" in data:
                    raise RuntimeError(f"API error : {data['error']}")

                content = data["choices"][0]["message"]["content"]
                # Certains fournisseurs renvoient content:null (réponse vide,
                # reasoning seul…) : jamais exploitable en aval → retry, puis
                # RuntimeError propre (gérée par les appelants) au lieu d'un
                # AttributeError sur .strip().
                if not isinstance(content, str) or not content.strip():
                    raise RuntimeError(
                        f"Réponse vide du modèle {payload['model']} "
                        f"(content={content!r})")
                generation_id = data.get("id")
                return content, generation_id

            except (requests.RequestException, RuntimeError) as e:
                if attempt == self.max_retries - 1:
                    raise
                wait = self.retry_delay * (2 ** attempt) + random.uniform(0, 5)
                logger.warning("Erreur LLM : %s — retry dans %.1fs", e, wait)
                time.sleep(wait)

        raise RuntimeError("Échec après plusieurs tentatives")


_llm_client: Optional[LLMClient] = None


def get_llm_client() -> LLMClient:
    global _llm_client
    if _llm_client is None:
        _llm_client = LLMClient()
    return _llm_client


def process_with_openrouter(prompt: str, model_idx: int = 0, temperature: float = 0.0,
                            max_tokens: int = 4096, image_b64: str = None,
                            system_prompt: str = SYSTEM_MSG, reasoning: bool = False,
                            model: str | None = None) -> str:
    """Point d'entrée unique du pipeline pour tous les appels LLM.
    `model` (chaîne) prime sur `model_idx` (legacy)."""
    if image_b64:
        return get_llm_client().call_llm_multimodal(
            image_b64, prompt, model_idx, temperature, max_tokens, system_prompt)
    return get_llm_client().call_llm(
        prompt, model_idx, temperature, max_tokens, system_prompt,
        reasoning=reasoning, model=model)
