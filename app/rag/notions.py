"""
PyxiScience — LLM Notion Retriever  (OpenRouter backend)
=========================================================
Selects relevant notions from the PyxiScience taxonomy (notions.xlsx) for a
given exercise by asking an LLM judge — replacing the FAISS/cosine retriever.

All LLM calls go through OpenRouter (https://openrouter.ai), which exposes an
OpenAI-compatible API. Any OpenRouter-hosted model is usable by setting
`DEFAULT_LLM_MODEL` or the `model=` kwarg, e.g.:
    "openai/gpt-4o"
    "openai/gpt-4o-mini"
    "anthropic/claude-sonnet-4.5"
    "anthropic/claude-opus-4.1"
    "google/gemini-2.5-pro"

Why LLM over cosine?
    • Short bilingual strings ("Mean Value Theorem" / "Théorème des
      accroissements finis") don't give embedding models enough lexical
      signal to rank precisely.
    • The LLM can reason about *which notion is actually exercised* rather
      than which string is most surface-similar.
    • Bonus: it can suggest GENERAL notions that the exercise covers but
      the catalogue is missing — a prerequisite for evolving the taxonomy.

Public API (drop-in compatible with the previous retriever):
    retrieve_notions(text, ...)                -> List[Dict[str, str]]
    retrieve_notions_for_exercise(myst, ...)   -> List[Dict[str, str]]
    enrich_exercise_with_notions(myst, ...)    -> (block, csv_ids)

Extra:
    retrieve_notions_llm(text, ...)            -> rich dict with suggestions

Author: PyxiScience Team
Version: 1.0
"""

from __future__ import annotations

import json
import logging
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import pandas as pd
from openai import OpenAI

from app.keys import OPENROUTER_API_KEY

logger = logging.getLogger(__name__)


# =============================================================================
# 1. CONFIGURATION
# =============================================================================

from app.config import NOTIONS_XLSX as DEFAULT_NOTIONS_XLSX, NOTIONS_MODEL

COL_FR = "FR_Name"
COL_EN = "EN_Name"
COL_ID = "Name_ID"

# Default LLM. Any model hosted on OpenRouter works — use `provider/model` form.
# See https://openrouter.ai/models for the full list.
DEFAULT_LLM_MODEL       = NOTIONS_MODEL
DEFAULT_TOP_K           = 5
DEFAULT_MAX_SUGGESTIONS = 2
DEFAULT_TEMPERATURE     = 0.0

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# Optional OpenRouter attribution headers (shown on their leaderboards + dashboard).
# Safe to leave as-is; override in your own deployment if you want.
OPENROUTER_HEADERS = {
    "HTTP-Referer": "https://pyxiscience.com",
    "X-Title":      "PyxiScience Notion Retriever",
}


# =============================================================================
# 2. CATALOGUE LOADING (cached in memory per xlsx path)
# =============================================================================

_catalogue_cache: Dict[Path, Tuple[str, Dict[str, Dict[str, str]]]] = {}


def load_notions_catalogue(
    xlsx_path: str | Path = DEFAULT_NOTIONS_XLSX,
) -> Tuple[str, Dict[str, Dict[str, str]]]:
    """
    Read the notions Excel file.

    Returns
    -------
    catalogue_text : str
        One line per notion, formatted as `ID | FR | EN`. This is the
        exact text shipped to the LLM.
    id_map : dict
        {name_id: {"fr_name": ..., "en_name": ...}} — used to validate
        returned IDs and enrich the LLM response.
    """
    xlsx_path = Path(xlsx_path)
    if xlsx_path in _catalogue_cache:
        return _catalogue_cache[xlsx_path]

    df = pd.read_excel(xlsx_path, dtype=str).fillna("")

    missing = [c for c in (COL_FR, COL_EN, COL_ID) if c not in df.columns]
    if missing:
        raise ValueError(
            f"Missing columns in '{xlsx_path}': {missing}\n"
            f"Found: {list(df.columns)}"
        )

    lines: List[str] = []
    id_map: Dict[str, Dict[str, str]] = {}

    for _, row in df.iterrows():
        nid = row[COL_ID].strip()
        fr  = row[COL_FR].strip()
        en  = row[COL_EN].strip()
        if not nid:
            continue
        lines.append(f"{nid} | {fr} | {en}")
        id_map[nid] = {"fr_name": fr, "en_name": en}

    catalogue_text = "\n".join(lines)
    _catalogue_cache[xlsx_path] = (catalogue_text, id_map)
    logger.info(f"  📋 Loaded {len(id_map)} notions from '{xlsx_path.name}'")
    return catalogue_text, id_map


# =============================================================================
# 3. PROMPT
# =============================================================================

SYSTEM_PROMPT = """You are a mathematical content classifier for PyxiScience, a bilingual (FR/EN) math education platform.

TASK
Given a math exercise and a CATALOGUE of notions (format per line: `ID | FR name | EN name`),
identify which notions are actually *exercised* by the problem — not merely mentioned.

RULES
1. Return ONLY a valid JSON object matching the schema below. No markdown fences, no commentary.
2. `selected_notion_ids` must contain IDs that EXACTLY appear in the catalogue (copy them verbatim).
   Do NOT invent, paraphrase, or alter IDs. If a concept is missing from the catalogue, put it in
   `suggested_new_notions` — never in `selected_notion_ids`.
3. Rank `selected_notion_ids` from most to least relevant. Keep only notions whose content is
   genuinely needed to solve the exercise. Quality > quantity — it is fine to return fewer than
   the requested top_k if the exercise only exercises one or two notions.
4. `relevance` ∈ [0, 1]. Reserve ≥ 0.8 for central notions, 0.4–0.7 for supporting ones.
5. `rationale` must be a short, concrete sentence (FR or EN) explaining the link.
6. `suggested_new_notions` are GENERAL mathematical concepts that:
     (a) are clearly exercised by the problem,
     (b) are NOT already in the catalogue — check both IDs AND FR/EN names,
     (c) are broad enough to be reused across many exercises (avoid hyper-specific tricks,
         avoid renaming existing notions).
   Be conservative: 0–2 suggestions is ideal, never more than 3. If nothing is missing, return [].
7. `proposed_id` follows PyxiScience convention: `Capitalised_Words_In_Snake_Case`
   (e.g. `Polar_Equation_Conversion`, `Partial_Fraction_Decomposition`).

OUTPUT JSON SCHEMA
{
  "selected_notion_ids": [
    {
      "name_id":   "<exact ID from catalogue>",
      "relevance": <float in [0,1]>,
      "rationale": "<one short sentence>"
    }
  ],
  "suggested_new_notions": [
    {
      "proposed_id": "<Snake_Case_Id>",
      "fr_name":     "<FR label>",
      "en_name":     "<EN label>",
      "rationale":   "<why it's missing AND why it's relevant>"
    }
  ]
}
"""


def _build_user_prompt(
    exercise_text:   str,
    catalogue_text:  str,
    top_k:           int,
    max_suggestions: int,
) -> str:
    n_notions = len(catalogue_text.splitlines())
    return (
        f"CATALOGUE ({n_notions} notions)\n"
        f"═══════════════════════════════════════════════════════════════\n"
        f"{catalogue_text}\n"
        f"═══════════════════════════════════════════════════════════════\n\n"
        f"EXERCISE\n"
        f"═══════════════════════════════════════════════════════════════\n"
        f"{exercise_text}\n"
        f"═══════════════════════════════════════════════════════════════\n\n"
        f"Return up to {top_k} selected notions (ranked best→worst) and up to "
        f"{max_suggestions} suggested new notions.\n"
        f"Reminder: every `name_id` in `selected_notion_ids` MUST appear verbatim "
        f"in the catalogue above."
    )


# =============================================================================
# 4. LLM CLIENT
# =============================================================================

_client: Optional[OpenAI] = None


def _get_client() -> OpenAI:
    """
    Return a cached OpenAI-compatible client pointed at OpenRouter.
    """
    global _client
    if _client is None:
        if not OPENROUTER_API_KEY or len(OPENROUTER_API_KEY) < 20:
            raise RuntimeError(
                "OPENROUTER_API_KEY is missing or invalid. Set it in core.ld."
            )
        _client = OpenAI(
            api_key=OPENROUTER_API_KEY,
            base_url=OPENROUTER_BASE_URL,
            default_headers=OPENROUTER_HEADERS,
        )
    return _client


def _call_llm(
    system:      str,
    user:        str,
    model:       str,
    temperature: float = DEFAULT_TEMPERATURE,
) -> Dict:
    """Single LLM call via OpenRouter, forcing JSON-object output."""
    client = _get_client()
    response = client.chat.completions.create(
        model=model,
        temperature=temperature,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": system},
            {"role": "user",   "content": user},
        ],
    )
    raw = response.choices[0].message.content or "{}"
    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        raise RuntimeError(
            f"LLM returned non-JSON content despite json_object mode.\n"
            f"Model: {model}\n"
            f"Raw:   {raw[:500]}\n"
            f"Error: {e}"
        )


# =============================================================================
# 5. PUBLIC API — rich version
# =============================================================================

def retrieve_notions_llm(
    exercise_text:   str,
    xlsx_path:       str | Path = DEFAULT_NOTIONS_XLSX,
    top_k:           int  = DEFAULT_TOP_K,
    max_suggestions: int  = DEFAULT_MAX_SUGGESTIONS,
    model:           str  = DEFAULT_LLM_MODEL,
    temperature:     float = DEFAULT_TEMPERATURE,
    verbose:         bool = True,
) -> Dict:
    """
    Retrieve relevant notions for an exercise using an LLM judge.

    Returns
    -------
    {
      "selected":  [ {rank, name_id, fr_name, en_name, relevance, rationale}, ... ],
      "suggested": [ {proposed_id, fr_name, en_name, rationale}, ... ],
      "elapsed_s": float,
      "model":     str,
    }
    """
    t0 = time.time()

    catalogue_text, id_map = load_notions_catalogue(xlsx_path)
    user_prompt = _build_user_prompt(
        exercise_text, catalogue_text, top_k, max_suggestions
    )
    data = _call_llm(SYSTEM_PROMPT, user_prompt, model=model, temperature=temperature)

    # -------- Validate & enrich `selected` --------
    selected: List[Dict] = []
    for rank, item in enumerate(data.get("selected_notion_ids", [])[:top_k], start=1):
        nid = (item.get("name_id") or "").strip()
        if nid not in id_map:
            if verbose:
                logger.info(f"  ⚠️  LLM returned unknown notion_id '{nid}' — dropping")
            continue
        meta = id_map[nid]
        selected.append({
            "rank":      rank,
            "name_id":   nid,
            "fr_name":   meta["fr_name"],
            "en_name":   meta["en_name"],
            "relevance": float(item.get("relevance", 0.0) or 0.0),
            "rationale": (item.get("rationale") or "").strip(),
        })
    # Re-rank in case of drops so ranks stay contiguous
    for i, s in enumerate(selected, start=1):
        s["rank"] = i

    # -------- Validate & dedupe `suggested` --------
    existing_ids      = set(id_map.keys())
    existing_names_fr = {v["fr_name"].lower() for v in id_map.values()}
    existing_names_en = {v["en_name"].lower() for v in id_map.values()}

    suggested: List[Dict] = []
    for item in data.get("suggested_new_notions", [])[:max_suggestions]:
        pid = (item.get("proposed_id") or "").strip()
        fr  = (item.get("fr_name") or "").strip()
        en  = (item.get("en_name") or "").strip()
        if not (pid and fr and en):
            continue
        if pid in existing_ids:
            if verbose:
                logger.info(f"  ⚠️  Suggested ID '{pid}' already exists — skipping")
            continue
        if fr.lower() in existing_names_fr or en.lower() in existing_names_en:
            if verbose:
                logger.info(f"  ⚠️  Suggested name '{fr} / {en}' duplicates an existing notion — skipping")
            continue
        suggested.append({
            "proposed_id": pid,
            "fr_name":     fr,
            "en_name":     en,
            "rationale":   (item.get("rationale") or "").strip(),
        })

    result = {
        "selected":  selected,
        "suggested": suggested,
        "elapsed_s": round(time.time() - t0, 2),
        "model":     model,
    }

    if verbose:
        _print_result(result)

    return result


# =============================================================================
# 6. DROP-IN REPLACEMENTS for the old API
# =============================================================================

def retrieve_notions(
    text:      str,
    xlsx_path: str | Path = DEFAULT_NOTIONS_XLSX,
    top_k:     int  = DEFAULT_TOP_K,
    model:     str  = DEFAULT_LLM_MODEL,
    verbose:   bool = True,
    **_ignored,   # swallows old kwargs: model_key, use_cache, force_rebuild
) -> List[Dict[str, str]]:
    """
    Old-shape output for backward compatibility with the FAISS retriever:
        [{"rank", "name_id", "fr_name", "en_name", "score"}, ...]
    where `score` is the LLM relevance (higher = more relevant, unlike
    the cosine distance returned by the old retriever).
    """
    result = retrieve_notions_llm(
        exercise_text=text,
        xlsx_path=xlsx_path,
        top_k=top_k,
        model=model,
        verbose=verbose,
    )
    return [
        {
            "rank":    str(s["rank"]),
            "name_id": s["name_id"],
            "fr_name": s["fr_name"],
            "en_name": s["en_name"],
            "score":   f"{s['relevance']:.4f}",
        }
        for s in result["selected"]
    ]


def retrieve_notions_for_exercise(
    exercise_myst: str,
    xlsx_path:     str | Path = DEFAULT_NOTIONS_XLSX,
    top_k:         int = DEFAULT_TOP_K,
    model:         str = DEFAULT_LLM_MODEL,
    **kwargs,
) -> List[Dict[str, str]]:
    """Pass the raw MyST exercise block — the LLM handles markup natively."""
    return retrieve_notions(
        exercise_myst, xlsx_path=xlsx_path, top_k=top_k, model=model, **kwargs
    )


def enrich_exercise_with_notions(
    exercise_myst:   str,
    xlsx_path:       str | Path = DEFAULT_NOTIONS_XLSX,
    top_k:           int = DEFAULT_TOP_K,
    max_suggestions: int = DEFAULT_MAX_SUGGESTIONS,
    model:           str = DEFAULT_LLM_MODEL,
) -> Tuple[str, str]:
    """
    Same signature/return as before: (formatted_block, comma_separated_ids).
    The formatted block now also lists any SUGGESTED new notions, so you
    can feed them back into your taxonomy pipeline.
    """
    result = retrieve_notions_llm(
        exercise_text=exercise_myst,
        xlsx_path=xlsx_path,
        top_k=top_k,
        max_suggestions=max_suggestions,
        model=model,
        verbose=False,
    )

    lines = ["═" * 70]
    lines.append(
        f" NOTIONS RETRIEVED via LLM  "
        f"[{result['model']}  ·  {result['elapsed_s']}s]"
    )
    lines.append("═" * 70)
    for s in result["selected"]:
        lines.append(
            f"  [{s['rank']}] {s['name_id']:<32}  relevance={s['relevance']:.2f}\n"
            f"        → {s['fr_name']} / {s['en_name']}\n"
            f"        ↳ {s['rationale']}"
        )

    if result["suggested"]:
        lines.append("─" * 70)
        lines.append(" ★ SUGGESTED NEW NOTIONS (not in catalogue)")
        lines.append("─" * 70)
        for g in result["suggested"]:
            lines.append(
                f"  + {g['proposed_id']}\n"
                f"        → {g['fr_name']} / {g['en_name']}\n"
                f"        ↳ {g['rationale']}"
            )

    lines.append("═" * 70)
    lines.append("Utilise ces notions comme :involvedConcepts: si pertinent.")

    ids_csv = ", ".join(s["name_id"] for s in result["selected"])
    return "\n".join(lines), ids_csv


# =============================================================================
# 7. PRETTY PRINTER
# =============================================================================

def _print_result(result: Dict) -> None:
    w = 72
    logger.info(f"\n{'═'*w}")
    logger.info(f"  🏷️  LLM NOTION RETRIEVAL  "
          f"[model: {result['model']}  ·  {result['elapsed_s']}s]")
    logger.info("═" * w)
    logger.info(f"  {'Rank':<5} {'Rel.':<6} {'Name_ID':<32} FR / EN")
    logger.info(f"  {'─'*5} {'─'*6} {'─'*32} {'─'*25}")
    for s in result["selected"]:
        label = f"{s['fr_name']} / {s['en_name']}"
        if len(label) > 25:
            label = label[:22] + "..."
        logger.info(f"  {s['rank']:<5} {s['relevance']:<6.2f} {s['name_id']:<32} {label}")
        if s["rationale"]:
            logger.info(f"         ↳ {s['rationale']}")

    if result["suggested"]:
        logger.info(f"\n  ★ SUGGESTED NEW NOTIONS")
        for g in result["suggested"]:
            logger.info(f"   + {g['proposed_id']}  —  {g['fr_name']} / {g['en_name']}")
            if g["rationale"]:
                logger.info(f"         ↳ {g['rationale']}")
    logger.info(f"{'═'*w}\n")


# =============================================================================
# 8. DEMO
# =============================================================================

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="LLM-based notion retriever")
    parser.add_argument("--xlsx",    default=str(DEFAULT_NOTIONS_XLSX))
    parser.add_argument("--model",   default=DEFAULT_LLM_MODEL)
    parser.add_argument("--topk",    type=int, default=DEFAULT_TOP_K)
    parser.add_argument("--suggest", type=int, default=DEFAULT_MAX_SUGGESTIONS)
    parser.add_argument("--query",   default=None, help="Raw exercise text or MyST block")
    args = parser.parse_args()

    demo_query = args.query or r"""
`````{exercise}
:id: 9dfb0461-1ece-4f6d-b24d-26564e3f12ba
:title: Polar Coordinates - exo 20
:chap: Polar_Coordinates

:::::{question}
:questionType: STQ
::::{questionStatement}
Find a polar equation for the curve represented by the given Cartesian equation
$3 y^2 = x$.
::::
::::{detailedSolution}
Substitute $x = r \cos(\theta)$ and $y = r \sin(\theta)$, then solve for $r$.
Result:  $r = \tfrac{1}{3} \cot(\theta)\csc(\theta)$.
::::
:::::
`````
"""

    retrieve_notions_llm(
        exercise_text=demo_query,
        xlsx_path=Path(args.xlsx),
        top_k=args.topk,
        max_suggestions=args.suggest,
        model=args.model,
    )