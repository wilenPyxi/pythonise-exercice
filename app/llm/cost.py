"""
Suivi des coûts des appels OpenRouter (ex utils/cost_estimator.py).
Coûts RÉELS récupérés via GET /api/v1/generation?id=… (tokens + coût exacts) ;
estimation len//4 utilisée uniquement en fallback temporaire, remplacée dès
que la réponse de l'API arrive.
"""

import logging
import os
import threading
import time
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Optional

import requests

from app.config import MODEL_PRICING

logger = logging.getLogger(__name__)

IMAGE_COST_PER_IMAGE = 0.002  # ~$0.002 par image pour la plupart des modèles


@dataclass
class CostRecord:
    """Enregistrement d'un coût pour une génération."""
    generation_id: str
    model: str
    timestamp: datetime
    input_tokens: int = 0
    output_tokens: int = 0
    total_cost: float = 0.0
    is_estimated: bool = True
    is_image: bool = False
    raw_stats: Dict = field(default_factory=dict)


class CostEstimator:
    """Estime et enregistre les coûts des appels LLM."""

    def __init__(self):
        self.actual_costs: Dict[str, CostRecord] = {}
        self.estimated_costs: Dict[str, CostRecord] = {}
        self.session_total: float = 0.0
        self.session_start: datetime = datetime.now()
        self._lock = threading.Lock()

    def estimate_tokens(self, text: str) -> int:
        """Approximation ~4 caractères/token (fallback uniquement)."""
        if not text:
            return 0
        return max(1, len(text) // 4)

    def get_model_pricing(self, model: str) -> Dict[str, float]:
        return MODEL_PRICING.get(model, {"input": 1.0, "output": 3.0})

    def estimate_cost(self, model: str, prompt: str, response: str,
                      is_image: bool = False) -> CostRecord:
        input_tokens = self.estimate_tokens(prompt)
        output_tokens = self.estimate_tokens(response)
        pricing = self.get_model_pricing(model)
        total_cost = (
            (input_tokens / 1_000_000) * pricing["input"]
            + (output_tokens / 1_000_000) * pricing["output"]
        )
        if is_image:
            total_cost += IMAGE_COST_PER_IMAGE

        record = CostRecord(
            generation_id=f"est_{int(time.time() * 1000)}",
            model=model,
            timestamp=datetime.now(),
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_cost=total_cost,
            is_estimated=True,
            is_image=is_image,
        )
        with self._lock:
            self.estimated_costs[record.generation_id] = record
            self.session_total += total_cost
        return record

    def record_actual_cost(self, model: str, generation_id: str,
                           stats: Dict, is_image: bool = False) -> bool:
        try:
            usage = stats.get("usage", stats.get("data", {}))
            input_tokens = usage.get("prompt_tokens", 0) or usage.get("tokens_prompt", 0)
            output_tokens = usage.get("completion_tokens", 0) or usage.get("tokens_completion", 0)
            total_cost = (
                stats.get("total_cost")
                or stats.get("cost")
                or usage.get("total_cost")
                or 0.0
            )
            if total_cost == 0 and (input_tokens > 0 or output_tokens > 0):
                pricing = self.get_model_pricing(model)
                total_cost = (
                    (input_tokens / 1_000_000) * pricing["input"]
                    + (output_tokens / 1_000_000) * pricing["output"]
                )
                if is_image:
                    total_cost += IMAGE_COST_PER_IMAGE

            record = CostRecord(
                generation_id=generation_id,
                model=model,
                timestamp=datetime.now(),
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                total_cost=total_cost,
                is_estimated=False,
                is_image=is_image,
                raw_stats=stats,
            )
            with self._lock:
                # Remplacer l'estimation provisoire la plus proche dans le temps.
                for est_id, est_record in list(self.estimated_costs.items()):
                    if est_record.model == model and abs(
                        (est_record.timestamp - record.timestamp).total_seconds()
                    ) < 60:
                        del self.estimated_costs[est_id]
                        self.session_total -= est_record.total_cost
                        break
                self.actual_costs[generation_id] = record
                self.session_total += total_cost
            return True

        except (KeyError, TypeError, ValueError) as e:
            logger.warning("Enregistrement du coût réel impossible : %s", e)
            return False

    def get_session_summary(self) -> Dict[str, Any]:
        with self._lock:
            costs_by_model: Dict[str, Dict] = {}
            for record in list(self.actual_costs.values()) + list(self.estimated_costs.values()):
                entry = costs_by_model.setdefault(record.model, {
                    "requests": 0, "input_tokens": 0, "output_tokens": 0, "total_cost": 0.0,
                })
                entry["requests"] += 1
                entry["input_tokens"] += record.input_tokens
                entry["output_tokens"] += record.output_tokens
                entry["total_cost"] += record.total_cost

            return {
                "session_start": self.session_start.isoformat(),
                "total_requests": len(self.actual_costs) + len(self.estimated_costs),
                "actual_costs_count": len(self.actual_costs),
                "estimated_costs_count": len(self.estimated_costs),
                "total_cost_usd": round(self.session_total, 6),
                "total_cost_eur": round(self.session_total * 0.92, 6),
                "costs_by_model": costs_by_model,
            }

    def reset_session(self):
        with self._lock:
            self.actual_costs.clear()
            self.estimated_costs.clear()
            self.session_total = 0.0
            self.session_start = datetime.now()


class CostTracker:
    """Tracker de coûts avec récupération asynchrone des stats réelles."""

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        self.cost_estimator = CostEstimator()
        self.base_url = "https://openrouter.ai/api/v1"
        self._pending_fetches: Dict[str, threading.Thread] = {}

    def fetch_generation_stats(self, generation_id: str) -> Optional[Dict]:
        """Stats réelles (tokens + coût) d'une génération via l'API OpenRouter."""
        if not generation_id:
            return None
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }
            url = f"{self.base_url}/generation?id={generation_id}"
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                return response.json()
            logger.debug("API stats %s : %s", response.status_code, response.text[:200])
            return None
        except requests.RequestException as e:
            logger.debug("Récupération des stats impossible : %s", e)
            return None

    def _schedule_generation_stats_fetch(self, generation_id: str, model: str, is_image: bool):
        """Récupération asynchrone différée (les stats arrivent avec ~2 s de retard)."""
        def fetch_delayed():
            time.sleep(2)
            try:
                stats = self.fetch_generation_stats(generation_id)
                if stats:
                    self.cost_estimator.record_actual_cost(
                        model=model, generation_id=generation_id,
                        stats=stats, is_image=is_image,
                    )
            finally:
                self._pending_fetches.pop(generation_id, None)

        thread = threading.Thread(target=fetch_delayed, daemon=True)
        self._pending_fetches[generation_id] = thread
        thread.start()

    def track_cost(self, generation_id: str, model: str, is_image: bool,
                   prompt: str = "", response: str = "") -> bool:
        """Coût réel si dispo immédiatement, sinon estimation + fetch async."""
        try:
            stats = self.fetch_generation_stats(generation_id)
            if stats and ("data" in stats or "cost" in stats
                          or "total_cost" in stats or "usage" in stats):
                if self.cost_estimator.record_actual_cost(
                    model=model, generation_id=generation_id,
                    stats=stats, is_image=is_image,
                ):
                    return True
        except Exception as e:
            logger.debug("Fetch immédiat du coût raté : %s", e)

        self._schedule_generation_stats_fetch(generation_id, model, is_image)
        if generation_id not in self.cost_estimator.actual_costs:
            self.cost_estimator.estimate_cost(
                model=model, prompt=prompt, response=response, is_image=is_image)
        return False

    def get_summary(self) -> Dict[str, Any]:
        return self.cost_estimator.get_session_summary()

    def reset(self):
        self.cost_estimator.reset_session()


_cost_tracker: Optional[CostTracker] = None


def get_cost_tracker() -> CostTracker:
    global _cost_tracker
    if _cost_tracker is None:
        _cost_tracker = CostTracker()
    return _cost_tracker


def cost_snapshot() -> dict:
    """Photo des totaux de session — l'orchestrateur fait before/after pour
    attribuer un coût par job (mono-poste : pas de jobs LLM concurrents)."""
    s = get_cost_tracker().get_summary()
    return {"usd": s["total_cost_usd"], "requests": s["total_requests"]}


def cost_delta(before: dict) -> dict:
    """Coût (USD/EUR) et nb de requêtes depuis `before` (cf. cost_snapshot)."""
    after = cost_snapshot()
    usd = max(0.0, round(after["usd"] - before["usd"], 6))
    return {
        "usd": usd,
        "eur": round(usd * 0.92, 6),
        "requests": after["requests"] - before["requests"],
    }
