"""
PyxiScience RAG Pipeline — Source-Based, Corrected Edition
===========================================================

What changed vs the legacy `rag.py`:

  1. FIXED — Method `import_line`. Legacy code emitted
         from pyxiscience.Classes_Extensions import pxsl_solution
     which is unimportable (pxsl_solution is a *method* of pxs_Poly).
     Each method Document now carries:
         import_line  = "from <module> import <parent_class>"
         parent_class = "<ClassName>"
         qualname     = "<ClassName>.<method_name>"

  2. FIXED — Class/method grouping. Each class Document now carries a
     serialised `methods` list in its metadata. When a class is
     retrieved, it renders as ONE grouped block (class header + all
     method signatures + one-line summaries) via the compact formatter.

  3. FIXED — De-duplication at render time. If both a class AND some of
     its own methods are retrieved, the methods are absorbed into the
     class's rendered block instead of being emitted as duplicate
     standalone blocks underneath.

  4. INTEGRATED — Compact LLM-optimized formatter (rag_formatter.py)
     replaces the legacy 4-section verbose catalogue. Leverages the
     :pxs_trigger: / :pxs_returns: / :pxs_example: / :pxs_antipattern:
     meta-tags embedded in PyxiScience docstrings.

  5. SCHEMA — CACHE_SCHEMA_VERSION bumped 2 → 3. Old FAISS caches are
     auto-invalidated on first load (see `_is_cache_stale`).

  6. EXTENDED — ALWAYS_INCLUDE now includes `pxs_Interval` (class) and
     `pxsl_pow` (function). These are ubiquitous in analysis exercises
     (domains, solution sets, variation tables) and polynomial display
     (safe coefficient parenthesisation) but were systematically missed
     by semantic retrieval because their trigger words don't appear in
     exercise statements. `build_always_include_context` now emits
     kind-aware diagnostics so missing/malformed baseline entries are
     loud at startup.

     ⚠️  After enriching docstrings (`:pxs_trigger:` / etc.), call
     `clear_cache(<model_key>)` once — the embedded `page_content` has
     changed but `CACHE_SCHEMA_VERSION` did not, so caches won't
     auto-invalidate on content-only changes.

Public entry points (unchanged names):

    retrieve_functions_context(exercise, ...)
        Pure retrieval + compact catalogue. NO LLM call. This is what a
        downstream code-generation prompt should inject as `{functions}`.

    retrieve_raw(exercise, ...)
        Just the ranked top-k hits with scores.

    retrieve_functions(exercise, model=..., ...)
        retrieve_functions_context + an LLM hop. Standalone Q&A only.
"""

from __future__ import annotations

import logging
import os
import re
import ast
import time
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple

from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

# HuggingFaceEmbeddings tire torch + sentence-transformers (~1 Go). Il n'est
# nécessaire QUE pour les embeddings locaux ; le défaut `openai-3-small` passe
# par l'API. Import PARESSEUX → l'app (et le déploiement slim) tourne sans torch.
def _load_hf_embeddings_cls():
    from langchain_huggingface import HuggingFaceEmbeddings
    return HuggingFaceEmbeddings


try:
    from langchain_openai import OpenAIEmbeddings
    _OPENAI_AVAILABLE = True
except ImportError:
    _OPENAI_AVAILABLE = False

from app.rag.formatter import build_catalogue, build_imports_block

logger = logging.getLogger(__name__)


# =============================================================================
# 1. CONFIGURATION
# =============================================================================

from app.config import CORPUS_DIR, FAISS_CACHE

from app.keys import OPENROUTER_API_KEY, OPENAI_API_KEY

OPENROUTER_MODELS = {
    "claude-haiku":  "anthropic/claude-3-haiku",
    "gpt-4o-mini":   "openai/gpt-4o-mini",
    "deepseek":      "deepseek/deepseek-chat",
    "gemini-flash":  "google/gemini-flash-1.5",
    "claude-sonnet": "anthropic/claude-4.5-sonnet",
}

SCRIPTS_DIR = CORPUS_DIR

PYXISCIENCE_SOURCE_FILES = {
    "Classes_Extensions":             "pyxiscience.Classes_Extensions",
    "Mes_fctions_d_alg_lineaire_bis": "pyxiscience.Mes_fctions_d_alg_lineaire_bis",
    "Mes_fctions_d_analyse_bis":      "pyxiscience.Mes_fctions_d_analyse_bis",
    "Mes_fctions_generalistes_bis":   "pyxiscience.Mes_fctions_generalistes_bis",
    "Mes_fctions_probabilistes_bis":  "pyxiscience.Mes_fctions_probabilistes_bis",
}

# ---------------------------------------------------------------------------
# ALWAYS_INCLUDE
# ---------------------------------------------------------------------------
# Entities injected into every prompt regardless of retrieval score.
# These are "ubiquitous utilities": functions/classes that the expert
# reaches for in ≥70% of exercises but whose trigger words rarely appear
# in the exercise statement itself, so semantic retrieval misses them.
#
# Ordering is preserved in the final catalogue (ALWAYS first, then
# retrieved entities).
#
# ─ Core formatting (present from v3) ─
#   pxsl_latex_coefficient  — signed coefficient "+ 3x", "- x", ""
#   pxsl_format_number      — bilingual thousands separator + \infty
#   pxsl_res_num            — " = "/" \approx " result formatting
#   pxsl_matrix             — LaTeX matrix with auto delimiters
#   pxs_config              — sympy.latex kwargs (FR/EN, ln_notation, …)
#
# ─ Analysis & polynomial display (added v3.1) ─
#   pxs_Interval  — classe ubiquitaire pour domaines, ensembles solution,
#                   tableaux de variations, image d'intervalle par TVI.
#                   La classe porte ses méthodes (.print, .from_Interval)
#                   dans sa metadata → rendues groupées dans le catalogue.
#   pxsl_pow      — affichage sécurisé coeff^n avec parenthèses auto sur
#                   coeff négatif/rationnel/composé. Indispensable dans
#                   tout corrigé pédagogique avec substitution numérique.
# ---------------------------------------------------------------------------
ALWAYS_INCLUDE = [
    "pxsl_latex_coefficient",
    "pxsl_format_number",
    "pxsl_res_num",
    "pxsl_matrix",
    "pxs_config",
    # Added v3.1 — ubiquitous in analysis & polynomial display
    "pxs_Interval",
    "pxsl_pow",
]

SOURCES_CACHE_ROOT   = FAISS_CACHE
CACHE_SCHEMA_VERSION = 3                   # bumped (method import fix)

# FAISS L2 on normalised embeddings ∈ [0, 2]; lower = better.
DEFAULT_SCORE_THRESHOLD = 1.6
DEFAULT_MODEL_KEY       = "openai-3-small"


# =============================================================================
# 2. EMBEDDING MODELS REGISTRY
# =============================================================================

EMBEDDING_MODELS: Dict[str, Dict] = {
    "codesearch-distilroberta": {
        "model_name": "flax-sentence-embeddings/st-codesearch-distilroberta-base",
        "description": "Code-search DistilRoBERTa — optimized for code retrieval (EN)",
        "normalize": True, "prefix": None, "backend": "huggingface", "cost_per_1k": None,
    },
    "minilm-multilingual": {
        "model_name": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        "description": "Multilingual MiniLM — fast, decent FR/EN",
        "normalize": True, "prefix": None, "backend": "huggingface", "cost_per_1k": None,
    },
    "mpnet-multilingual": {
        "model_name": "sentence-transformers/paraphrase-multilingual-mpnet-base-v2",
        "description": "Multilingual MPNet — strong FR/EN, good default",
        "normalize": True, "prefix": None, "backend": "huggingface", "cost_per_1k": None,
    },
    "distiluse-multilingual": {
        "model_name": "sentence-transformers/distiluse-base-multilingual-cased-v2",
        "description": "Distilled USE multilingual",
        "normalize": True, "prefix": None, "backend": "huggingface", "cost_per_1k": None,
    },
    "labse": {
        "model_name": "sentence-transformers/LaBSE",
        "description": "LaBSE — 109 languages, strong cross-lingual",
        "normalize": True, "prefix": None, "backend": "huggingface", "cost_per_1k": None,
    },
    "e5-multilingual-small": {
        "model_name": "intfloat/multilingual-e5-small",
        "description": "Multilingual E5 small",
        "normalize": True, "prefix": "query: ", "backend": "huggingface", "cost_per_1k": None,
    },
    "e5-multilingual-base": {
        "model_name": "intfloat/multilingual-e5-base",
        "description": "Multilingual E5 base — top HF retrieval",
        "normalize": True, "prefix": "query: ", "backend": "huggingface", "cost_per_1k": None,
    },
    "e5-multilingual-large": {
        "model_name": "intfloat/multilingual-e5-large",
        "description": "Multilingual E5 large — slow",
        "normalize": True, "prefix": "query: ", "backend": "huggingface", "cost_per_1k": None,
    },
    "all-mpnet-base": {
        "model_name": "sentence-transformers/all-mpnet-base-v2",
        "description": "English MPNet",
        "normalize": True, "prefix": None, "backend": "huggingface", "cost_per_1k": None,
    },
    "all-minilm-l6": {
        "model_name": "sentence-transformers/all-MiniLM-L6-v2",
        "description": "English MiniLM L6",
        "normalize": True, "prefix": None, "backend": "huggingface", "cost_per_1k": None,
    },
    "openai-3-small": {
        "model_name": "text-embedding-3-small",
        "description": "OpenAI 3-small — 1536-dim, cheap, multilingual",
        "normalize": True, "prefix": None, "backend": "openai",
        "cost_per_1k": 0.00002, "dimensions": 1536,
    },
    "openai-3-large": {
        "model_name": "text-embedding-3-large",
        "description": "OpenAI 3-large — 3072-dim",
        "normalize": True, "prefix": None, "backend": "openai",
        "cost_per_1k": 0.00013, "dimensions": 3072,
    },
    "openai-ada-002": {
        "model_name": "text-embedding-ada-002",
        "description": "OpenAI ada-002 — legacy",
        "normalize": True, "prefix": None, "backend": "openai",
        "cost_per_1k": 0.00010, "dimensions": 1536,
    },
}


# =============================================================================
# 3. SOURCE FILE PARSER — CORRECTED
# =============================================================================

def _extract_signature(node: ast.AST) -> str:
    """Signature like 'f(x, y=0, **kwargs)' via ast.unparse (Py ≥ 3.9)."""
    try:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            return f"{node.name}({ast.unparse(node.args)})"
        if isinstance(node, ast.ClassDef):
            # Prefer __init__ signature; fallback to generic "..."
            for item in node.body:
                if (isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef))
                        and item.name == "__init__"):
                    args_src = ast.unparse(item.args)
                    args_src = re.sub(r"^self\s*,?\s*", "", args_src)
                    return f"{node.name}({args_src})"
            return f"{node.name}(...)"
    except Exception:
        pass
    return f"{getattr(node, 'name', '?')}(...)"


def _method_signature(node: ast.AST) -> str:
    """Method signature with leading `self` stripped."""
    try:
        args_src = ast.unparse(node.args)
        args_src = re.sub(r"^self\s*,?\s*", "", args_src)
        return f"({args_src})"
    except Exception:
        return "(...)"


def _summary_from_docstring(docstring: str) -> str:
    """
    One-line purpose extracted from the first non-trivial line of the
    docstring, up to the first :pxs_*: tag. Used to annotate methods
    in a class-grouped block.
    """
    if not docstring:
        return ""
    cut = re.search(r"^\s*:pxs_\w+:", docstring, flags=re.MULTILINE)
    head = docstring[: cut.start()] if cut else docstring
    for raw in head.splitlines():
        line = raw.strip()
        if not line or line.startswith(("Args:", "Returns:", "Paramètres", "Retourne",
                                        "Lève", "Exemples", "---", "===")):
            continue
        return line[:90]
    return ""


def _page_content_for_embedding(doc_meta: Dict[str, Any], docstring: str,
                                source_snippet: str) -> str:
    """
    Text fed to the embedder. Keep it dense in retrieval signal: qualname,
    signature, the full docstring (incl. :pxs_*: tags — triggers matter a
    lot for semantic match), and a trimmed source snippet.
    """
    head = (
        f"NAME     : {doc_meta['qualname']}\n"
        f"SIGNATURE: {doc_meta['signature']}\n"
        f"IMPORT   : {doc_meta['import_line']}\n"
        f"KIND     : {doc_meta['kind']}\n"
    )
    body = head
    if docstring:
        body += f"\nDESCRIPTION:\n{docstring}\n"
    body += f"\nSOURCE:\n{source_snippet}"
    return body


def parse_python_source(filepath: str, module_name: str) -> List[Document]:
    """
    AST-walk a Python source file and emit one Document per top-level
    function, class, and method.

    Key fix: methods' `import_line` references the PARENT CLASS, not
    the method name. Classes carry a serialised `methods` list so the
    renderer can group them.
    """
    with open(filepath, "r", encoding="utf-8") as fh:
        source = fh.read()
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        logger.info(f"  ⚠️  SyntaxError in {filepath}: {e}")
        return []

    lines = source.splitlines()

    def get_source_block(node, limit: int = 1200) -> str:
        start = node.lineno - 1
        end   = getattr(node, "end_lineno", start + 40)
        block = "\n".join(lines[start:end])
        return block[:limit] + ("\n..." if len(block) > limit else "")

    docs: List[Document] = []

    for node in ast.iter_child_nodes(tree):

        # ── Top-level function ────────────────────────────────────────
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            name      = node.name
            docstring = ast.get_docstring(node) or ""
            signature = _extract_signature(node)
            meta = {
                "schema_version": CACHE_SCHEMA_VERSION,
                "qualname":       name,
                "base_name":      name,
                "parent_class":   "",
                "module_name":    module_name,
                "import_line":    f"from {module_name} import {name}",
                "signature":      signature.replace(name, "", 1),   # "(...)" only
                "kind":           "function",
                "docstring":      docstring,
                "filepath":       filepath,
                "methods":        [],          # unused for functions
            }
            # Keep full signature string alongside for downstream convenience
            meta["signature"] = re.sub(r"^[^(]*", "", signature) or "(...)"
            snippet = get_source_block(node)
            docs.append(Document(
                page_content=_page_content_for_embedding(meta, docstring, snippet),
                metadata=meta,
            ))
            continue

        # ── Class ─────────────────────────────────────────────────────
        if isinstance(node, ast.ClassDef):
            cls_name      = node.name
            cls_docstring = ast.get_docstring(node) or ""
            cls_signature = _extract_signature(node)   # e.g. "pxs_Poly(x, ...)"
            cls_signature = re.sub(r"^[^(]*", "", cls_signature) or "(...)"

            # Collect methods first so we can stash them on the class doc.
            method_nodes = [
                item for item in node.body
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef))
            ]

            methods_meta: List[Dict[str, str]] = []
            for m in method_nodes:
                msig = _method_signature(m)
                mdoc = ast.get_docstring(m) or ""
                methods_meta.append({
                    "name":      m.name,
                    "signature": msig,
                    "summary":   _summary_from_docstring(mdoc),
                })

            # Class Document (retrievable on its own; renders grouped).
            cls_meta = {
                "schema_version": CACHE_SCHEMA_VERSION,
                "qualname":       cls_name,
                "base_name":      cls_name,
                "parent_class":   "",
                "module_name":    module_name,
                "import_line":    f"from {module_name} import {cls_name}",
                "signature":      cls_signature,
                "kind":           "class",
                "docstring":      cls_docstring,
                "filepath":       filepath,
                "methods":        methods_meta,
            }
            docs.append(Document(
                page_content=_page_content_for_embedding(
                    cls_meta, cls_docstring, get_source_block(node, limit=600)
                ),
                metadata=cls_meta,
            ))

            # Method Documents (retrievable individually; FIXED import line).
            for m in method_nodes:
                m_name    = m.name
                m_doc     = ast.get_docstring(m) or ""
                m_sig     = _method_signature(m)
                m_qual    = f"{cls_name}.{m_name}"
                m_meta = {
                    "schema_version": CACHE_SCHEMA_VERSION,
                    "qualname":       m_qual,
                    "base_name":      m_name,
                    "parent_class":   cls_name,
                    "module_name":    module_name,
                    # ⚠️  Methods are not importable on their own — import the class.
                    "import_line":    f"from {module_name} import {cls_name}",
                    "signature":      m_sig,
                    "kind":           "method",
                    "docstring":      m_doc,
                    "filepath":       filepath,
                    "methods":        [],
                }
                docs.append(Document(
                    page_content=_page_content_for_embedding(
                        m_meta, m_doc, get_source_block(m)
                    ),
                    metadata=m_meta,
                ))

    return docs


def load_all_sources(scripts_dir: str | Path = SCRIPTS_DIR) -> List[Document]:
    all_docs: List[Document] = []
    for filename, module_name in PYXISCIENCE_SOURCE_FILES.items():
        candidates = [
            os.path.join(scripts_dir, filename),
            os.path.join(scripts_dir, filename + ".py"),
        ]
        filepath = next((p for p in candidates if os.path.exists(p)), None)
        if filepath is None:
            logger.info(f"  ⚠️  Not found: {filename}  (skipping)")
            continue
        logger.info(f"  📄 Parsing {filename} → {module_name}")
        docs = parse_python_source(filepath, module_name)
        all_docs.extend(docs)
        logger.info(f"      → {len(docs)} functions/classes/methods indexed")
    return all_docs


def build_always_include_context(all_docs: List[Document]) -> List[Document]:
    """
    Resolve ALWAYS_INCLUDE names → Documents. We match on `qualname` (which
    equals the bare name for top-level functions and classes).

    Kind-aware diagnostics:
      - A missing entry is a hard warning (the entity won't be injected).
      - A class with no methods is a soft warning (likely a parser
        regression — its methods won't be listed in the catalogue block).
      - Duplicate base_names across modules (e.g. `pxsl_pow` defined in
        two source files) are flagged so the user can dedupe canonically.
    """
    # Detect duplicates across modules BEFORE dedup-by-qualname.
    base_name_locations: Dict[str, List[str]] = {}
    for d in all_docs:
        if d.metadata.get("parent_class"):
            continue  # skip methods (their name collides with siblings by design)
        base = d.metadata["base_name"]
        base_name_locations.setdefault(base, []).append(d.metadata["module_name"])

    for name in ALWAYS_INCLUDE:
        locs = base_name_locations.get(name, [])
        if len(locs) > 1:
            logger.info(
                f"  ⚠️  ALWAYS_INCLUDE '{name}' defined in MULTIPLE modules: "
                f"{locs} — last one wins in the index, consider deduping."
            )

    # The actual resolution index — one doc per top-level qualname
    # (duplicates get clobbered; that's the existing behaviour).
    index = {d.metadata["qualname"]: d for d in all_docs if not d.metadata["parent_class"]}

    result: List[Document] = []
    for name in ALWAYS_INCLUDE:
        doc = index.get(name)
        if doc is None:
            logger.info(
                f"  ⚠️  ALWAYS_INCLUDE '{name}' not found in sources — "
                f"check PYXISCIENCE_SOURCE_FILES and that the symbol is "
                f"defined at module top-level."
            )
            continue

        kind = doc.metadata.get("kind", "?")
        if kind == "class" and not doc.metadata.get("methods"):
            logger.info(
                f"  ⚠️  ALWAYS_INCLUDE class '{name}' has no methods in its "
                f"metadata — likely a parser issue. Catalogue will show the "
                f"class header only."
            )

        logger.info(f"  ✓ ALWAYS_INCLUDE '{name}' → {kind} "
              f"({doc.metadata['module_name']})")
        result.append(doc)

    return result


# =============================================================================
# 4. EMBEDDINGS + VECTORSTORE
# =============================================================================

_vs_cache:    Dict[str, FAISS]       = {}
_emb_cache:   Dict[str, object]      = {}
_always_docs: List[Document]         = []


def _resolve_openai_key() -> str:
    if not _OPENAI_AVAILABLE:
        raise RuntimeError("pip install langchain-openai")
    key = OPENAI_API_KEY
    if not key or len(key) < 20:
        raise RuntimeError("OpenAI embedding models require OPENAI_API_KEY.")
    return key


def _get_embeddings(model_key: str = DEFAULT_MODEL_KEY) -> object:
    if model_key in _emb_cache:
        return _emb_cache[model_key]
    cfg = EMBEDDING_MODELS.get(model_key)
    if cfg is None:
        raise ValueError(
            f"Unknown model key '{model_key}'. "
            f"Available: {list(EMBEDDING_MODELS.keys())}"
        )
    backend = cfg.get("backend", "huggingface")
    logger.info(f"  🔧 Loading embedding model [{backend}]: {cfg['model_name']} ...")
    if backend == "openai":
        emb = OpenAIEmbeddings(
            model=cfg["model_name"],
            openai_api_key=_resolve_openai_key(),
        )
    else:
        HuggingFaceEmbeddings = _load_hf_embeddings_cls()
        emb = HuggingFaceEmbeddings(
            model_name=cfg["model_name"],
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": cfg["normalize"]},
        )
    _emb_cache[model_key] = emb
    return emb


def _cache_path_for(model_key: str) -> Path:
    return SOURCES_CACHE_ROOT / model_key


def _is_cache_stale(vs: FAISS) -> Tuple[bool, str]:
    """Detect old caches built with a prior metadata schema."""
    try:
        if not vs.index_to_docstore_id:
            return True, "empty index"
        first_id  = vs.index_to_docstore_id[0]
        first_doc = vs.docstore.search(first_id)
        if not isinstance(first_doc, Document):
            return True, f"docstore returned {type(first_doc)}"
        meta = first_doc.metadata or {}
        version = meta.get("schema_version", 0)
        if version < CACHE_SCHEMA_VERSION:
            return True, f"schema v{version} < current v{CACHE_SCHEMA_VERSION}"
        # Sanity: v3 requires 'qualname' and 'parent_class' in every doc.
        if "qualname" not in meta or "parent_class" not in meta:
            return True, "missing qualname/parent_class metadata"
        return False, ""
    except Exception as e:
        return True, f"inspection failed: {e}"


def setup_vectorstore(
    scripts_dir:   str | Path = SCRIPTS_DIR,
    model_key:     str        = DEFAULT_MODEL_KEY,
    use_cache:     bool       = True,
    force_rebuild: bool       = False,
) -> FAISS:
    global _always_docs

    if model_key in _vs_cache and not force_rebuild:
        if not _always_docs:
            _always_docs = build_always_include_context(load_all_sources(scripts_dir))
        return _vs_cache[model_key]

    cache_path = _cache_path_for(model_key)
    emb        = _get_embeddings(model_key)

    # Try cache.
    if use_cache and not force_rebuild and cache_path.exists():
        try:
            logger.info(f"📦 Loading sources vectorstore from cache ({model_key})...")
            vs = FAISS.load_local(
                str(cache_path), emb, allow_dangerous_deserialization=True
            )
            stale, reason = _is_cache_stale(vs)
            if stale:
                logger.info(f"♻️  Cache stale ({reason}) — rebuilding")
            else:
                logger.info(f"✅ Loaded {vs.index.ntotal} vectors (schema v{CACHE_SCHEMA_VERSION})")
                _vs_cache[model_key] = vs
                _always_docs = build_always_include_context(load_all_sources(scripts_dir))
                return vs
        except Exception as e:
            logger.info(f"⚠️  Cache load failed, rebuilding: {e}")

    # Rebuild.
    logger.info(f"🔨 Building sources vectorstore with '{model_key}'...")
    all_docs     = load_all_sources(scripts_dir)
    _always_docs = build_always_include_context(all_docs)

    if not all_docs:
        raise RuntimeError(f"No documents found in {scripts_dir}.")

    # E5-style models want a 'passage: ' prefix on indexed docs,
    # 'query: ' on the query.
    cfg = EMBEDDING_MODELS[model_key]
    if cfg.get("prefix"):
        passage_prefix = cfg["prefix"].replace("query: ", "passage: ")
        for d in all_docs:
            d.page_content = passage_prefix + d.page_content

    logger.info(f"🧮 Embedding {len(all_docs)} entities with '{model_key}'...")
    vs = FAISS.from_documents(all_docs, emb)
    _vs_cache[model_key] = vs

    if use_cache:
        cache_path.mkdir(parents=True, exist_ok=True)
        vs.save_local(str(cache_path))
        logger.info(f"💾 Cache saved → {cache_path}")

    return vs


# =============================================================================
# 5. DEDUPLICATION + ENTITY CONVERSION
# =============================================================================

def _doc_to_entity(doc: Document) -> Dict[str, Any]:
    """Document → entity dict understood by rag_formatter.build_catalogue."""
    m = doc.metadata
    return {
        "qualname":    m["qualname"],
        "signature":   m.get("signature", "(...)"),
        "import_line": m["import_line"],
        "kind":        m["kind"],
        "docstring":   m.get("docstring", ""),
        "methods":     list(m.get("methods", [])) if m["kind"] == "class" else [],
        # Extra fields preserved for debugging/telemetry:
        "module_name":   m["module_name"],
        "parent_class":  m.get("parent_class", ""),
    }


def _merge_docs(retrieved_docs: List[Document],
                always_docs:    List[Document]) -> List[Document]:
    """
    Merge ALWAYS_INCLUDE + retrieved, de-duplicated by qualname,
    preserving ALWAYS order first.
    """
    seen: set = set()
    merged: List[Document] = []
    for doc in always_docs + retrieved_docs:
        q = doc.metadata["qualname"]
        if q in seen:
            continue
        seen.add(q)
        merged.append(doc)
    return merged


def _absorb_methods_into_classes(docs: List[Document]) -> List[Document]:
    """
    If a class Document AND some of its methods are both in `docs`, keep
    the class and drop the loose methods (the class block already lists
    them). Standalone methods whose class is NOT retrieved stay as-is.
    """
    retrieved_classes = {
        d.metadata["qualname"] for d in docs if d.metadata["kind"] == "class"
    }
    if not retrieved_classes:
        return docs
    return [
        d for d in docs
        if not (d.metadata["kind"] == "method"
                and d.metadata.get("parent_class") in retrieved_classes)
    ]


def _flatten_metadata(docs: List[Document]) -> List[Dict[str, Any]]:
    return [
        {
            "qualname":     d.metadata["qualname"],
            "import_line":  d.metadata["import_line"],
            "signature":    d.metadata.get("signature", ""),
            "docstring":    (d.metadata.get("docstring") or "")[:300],
            "kind":         d.metadata["kind"],
            "module_name":  d.metadata["module_name"],
            "parent_class": d.metadata.get("parent_class", ""),
        }
        for d in docs
    ]


# =============================================================================
# 6. PUBLIC API — retrieval-only (NO LLM)
# =============================================================================

def retrieve_functions_context(
    exercise:        str,
    embedding_model: str   = DEFAULT_MODEL_KEY,
    top_k:           int   = 12,
    score_threshold: float = DEFAULT_SCORE_THRESHOLD,
    force_rebuild:   bool  = False,
    verbose:         bool  = True,
) -> Dict[str, Any]:
    """
    Retrieve relevant PyxiScience entities and build a prompt-ready catalogue.

    NO LLM CALL. Drop `result["catalogue"]` into your downstream prompt's
    `{functions}` slot.

    Returns:
        {
            "catalogue":       str,          # drop-in for {functions}
            "imports_block":   str,          # importable header
            "entities":        List[dict],   # formatted entity dicts (ordered)
            "retrieved":       List[dict],   # flat meta for retrieved hits
            "always_included": List[dict],   # flat meta for baseline
            "embedding_model": str,
            "top_k":           int,
            "kept":            int,          # survived score_threshold
        }
    """
    if embedding_model not in EMBEDDING_MODELS:
        raise ValueError(
            f"Unknown embedding_model '{embedding_model}'. "
            f"Available: {list(EMBEDDING_MODELS.keys())}"
        )

    t0 = time.time()
    vs = setup_vectorstore(model_key=embedding_model, force_rebuild=force_rebuild)

    cfg        = EMBEDDING_MODELS[embedding_model]
    query_text = (cfg.get("prefix") or "") + exercise

    hits = vs.similarity_search_with_score(query_text, k=top_k)
    retrieved_docs = [doc for doc, score in hits if score < score_threshold]

    if verbose:
        logger.info("\n" + "═" * 70)
        logger.info(f"🔍 RETRIEVAL [{embedding_model}, top-{top_k}, thr<{score_threshold}]")
        logger.info("═" * 70)
        for doc, score in hits:
            if   score < 1.2:              label = "✅"
            elif score < score_threshold:  label = "⚠️ "
            else:                           label = "❌"
            qn = doc.metadata.get("qualname", "?")
            logger.info(f"  {label}  score={score:.3f}  →  {qn}")
        logger.info(f"\n  → kept {len(retrieved_docs)} / {len(hits)}")
        logger.info("═" * 70)

    # Merge with ALWAYS_INCLUDE → absorb methods into retrieved classes.
    merged  = _merge_docs(retrieved_docs, _always_docs)
    merged  = _absorb_methods_into_classes(merged)

    entities  = [_doc_to_entity(d) for d in merged]
    catalogue = build_catalogue(entities)
    imports   = build_imports_block(entities)

    out = {
        "catalogue":        catalogue,
        "imports_block":    imports,
        "entities":         entities,
        "retrieved":        _flatten_metadata(retrieved_docs),
        "always_included":  _flatten_metadata(_always_docs),
        "embedding_model":  embedding_model,
        "top_k":            top_k,
        "kept":             len(retrieved_docs),
    }

    if verbose:
        logger.info(f"⏱️  retrieve_functions_context in {time.time() - t0:.2f}s")

    return out


def retrieve_raw(
    exercise:        str,
    embedding_model: str  = DEFAULT_MODEL_KEY,
    top_k:           int  = 12,
    force_rebuild:   bool = False,
) -> List[Dict[str, Any]]:
    """Lightweight retrieval — just the ranked list of hits with scores."""
    if embedding_model not in EMBEDDING_MODELS:
        raise ValueError(
            f"Unknown embedding_model '{embedding_model}'. "
            f"Available: {list(EMBEDDING_MODELS.keys())}"
        )
    vs = setup_vectorstore(model_key=embedding_model, force_rebuild=force_rebuild)
    cfg        = EMBEDDING_MODELS[embedding_model]
    query_text = (cfg.get("prefix") or "") + exercise
    hits = vs.similarity_search_with_score(query_text, k=top_k)
    return [
        {
            "rank":         i + 1,
            "score":        float(score),
            "qualname":     d.metadata["qualname"],
            "signature":    d.metadata.get("signature", ""),
            "import_line":  d.metadata["import_line"],
            "module_name":  d.metadata["module_name"],
            "kind":         d.metadata["kind"],
            "parent_class": d.metadata.get("parent_class", ""),
            "docstring":    (d.metadata.get("docstring") or "")[:200],
        }
        for i, (d, score) in enumerate(hits)
    ]


# =============================================================================
# 7. LLM WRAPPER — retrieve_functions (standalone Q&A)
# =============================================================================

_llm: Optional[ChatOpenAI] = None


def get_llm(model_key: str = "gpt-4o-mini") -> ChatOpenAI:
    global _llm
    if _llm is None:
        _llm = ChatOpenAI(
            model=OPENROUTER_MODELS.get(model_key, model_key),
            openai_api_key=OPENROUTER_API_KEY,
            openai_api_base="https://openrouter.ai/api/v1",
            temperature=0,
            timeout=60,
            max_retries=2,
            default_headers={
                "HTTP-Referer": "http://localhost:8501",
                "X-Title":      "PyxiScience RAG",
            },
        )
    return _llm


def retrieve_functions(
    exercise:        str,
    model:           str  = "gpt-4o-mini",
    embedding_model: str  = DEFAULT_MODEL_KEY,
    top_k:           int  = 12,
    force_rebuild:   bool = False,
    verbose:         bool = True,
) -> Dict[str, Any]:
    """
    Standalone Q&A: retrieve + ask an LLM which functions to use and how.

    If you already have your own downstream code-generation prompt, use
    `retrieve_functions_context` instead and skip this LLM hop.
    """
    global _llm

    t0 = time.time()
    logger.info(f"🤖 LLM:        {model}")
    logger.info(f"🧠 Embeddings: {embedding_model}")
    _llm = get_llm(model)

    ctx = retrieve_functions_context(
        exercise=exercise,
        embedding_model=embedding_model,
        top_k=top_k,
        force_rebuild=force_rebuild,
        verbose=verbose,
    )

    prompt = f"""Tu es un expert Python / mathématiques pour la bibliothèque **PyxiScience**.

Ta mission : résoudre l'exercice ci-dessous **en utilisant le catalogue de
fonctions PyxiScience fourni**. Tu n'as pas le droit de réimplémenter ce qui
existe déjà dans le catalogue.

═══════════════════════════════════════════════════════════════════════════
 RÈGLES IMPÉRATIVES
═══════════════════════════════════════════════════════════════════════════

1. **USAGE OBLIGATOIRE** — Dès qu'une fonction du catalogue couvre un
   besoin, tu DOIS l'utiliser.
2. **INTERDICTION DE RÉIMPLÉMENTER** — Si tu écris une fonction qui existe
   déjà dans le catalogue, STOP, importe celle du catalogue.
3. **IMPORTS EXACTS** — Recopie les lignes d'import EXACTES du catalogue.
   Pour une méthode, tu importes la CLASSE et tu l'appelles via une instance.
4. **SIGNATURES EXACTES** — Appelle chaque fonction avec la signature
   EXACTE donnée.
5. **pxs_config() EN PREMIER** — `config = pxs_config()` en tête du script,
   puis `**config` aux `latex(...)` et aux `pxsl_*` qui l'acceptent.
6. **BIBLIOTHÈQUES EXTERNES EN DERNIER RECOURS** — sympy / numpy /
   matplotlib uniquement si rien dans le catalogue ne convient.

═══════════════════════════════════════════════════════════════════════════
 CATALOGUE
═══════════════════════════════════════════════════════════════════════════
{ctx['catalogue']}

═══════════════════════════════════════════════════════════════════════════
 EXERCICE
═══════════════════════════════════════════════════════════════════════════
{exercise}

═══════════════════════════════════════════════════════════════════════════
 FORMAT DE RÉPONSE
═══════════════════════════════════════════════════════════════════════════

### 1. Plan d'attaque
étape → `nom_fonction(signature)` — justification.
Étape sans fonction adéquate → `(aucune — fallback sympy/numpy)`.

### 2. Imports
```python
{ctx['imports_block']}
```

### 3. Code complet
```python
config = pxs_config()
# ... code appelant EFFECTIVEMENT les fonctions du catalogue ...
```

### 4. Vérification
Pour chaque fonction PyxiScience utilisée :
- [ ] importée (classe pour une méthode) ?
- [ ] appelée ?
- [ ] signature respectée ?

Génère maintenant ta réponse :"""

    response = _llm.invoke(prompt)
    answer   = response.content

    logger.info(f"⏱️  Total (retrieve + LLM): {time.time() - t0:.1f}s")

    if verbose:
        logger.info("\n" + "═" * 70)
        logger.info("📝 RÉPONSE FINALE:")
        logger.info("═" * 70)
        logger.info(answer)
        logger.info("═" * 70)

    return {**ctx, "answer": answer, "llm_model": model}


# =============================================================================
# 8. UTILITIES (cache + benchmark)
# =============================================================================

def list_embedding_models() -> None:
    logger.info(f"\n{'═'*92}")
    logger.info("  Available Embedding Models")
    logger.info(f"{'═'*92}")
    logger.info(f"  {'Key':<28} {'Backend':<14} {'Dims':<6} {'Cost/1k':<12} {'Model'}")
    logger.info(f"  {'─'*28} {'─'*14} {'─'*6} {'─'*12} {'─'*36}")
    for k, v in EMBEDDING_MODELS.items():
        star    = " ★" if k == DEFAULT_MODEL_KEY else ""
        backend = v.get("backend", "huggingface")
        dims    = str(v.get("dimensions", "—"))
        cost    = f"${v['cost_per_1k']:.5f}" if v.get("cost_per_1k") else "free"
        icon    = "💰" if backend == "openai" else "🤗"
        logger.info(f"  {k:<28} {icon} {backend:<12} {dims:<6} {cost:<12} {v['model_name']}{star}")
    logger.info(f"\n  ★ = default   💰 = OPENAI_API_KEY required   🤗 = local/free\n")


def list_cached_models() -> List[str]:
    if not SOURCES_CACHE_ROOT.exists():
        return []
    return [p.name for p in SOURCES_CACHE_ROOT.iterdir() if p.is_dir()]


def clear_cache(embedding_model: Optional[str] = None) -> None:
    import shutil
    if embedding_model:
        p = _cache_path_for(embedding_model)
        if p.exists():
            shutil.rmtree(p)
            logger.info(f"🗑️  Deleted cache for '{embedding_model}'")
        _vs_cache.pop(embedding_model, None)
        _emb_cache.pop(embedding_model, None)
    else:
        if SOURCES_CACHE_ROOT.exists():
            shutil.rmtree(SOURCES_CACHE_ROOT)
            logger.info("🗑️  Deleted all caches")
        _vs_cache.clear()
        _emb_cache.clear()


def benchmark_embedding_models(
    test_queries:  List[str],
    top_k:         int                  = 5,
    model_keys:    Optional[List[str]]  = None,
    force_rebuild: bool                 = False,
) -> Dict[str, Dict[str, List[Dict]]]:
    keys    = model_keys or list(EMBEDDING_MODELS.keys())
    results: Dict[str, Dict[str, List[Dict]]] = {}
    logger.info(f"\n{'═'*72}")
    logger.info(f"  🔬 BENCHMARK — {len(keys)} models × {len(test_queries)} queries")
    logger.info(f"{'═'*72}\n")
    for mk in keys:
        logger.info(f"  ▶ {mk}  ({EMBEDDING_MODELS[mk]['description']})")
        results[mk] = {}
        for q in test_queries:
            t0 = time.time()
            try:
                hits = retrieve_raw(q, embedding_model=mk, top_k=top_k,
                                    force_rebuild=force_rebuild)
                latency = time.time() - t0
                results[mk][q] = hits
                top1 = hits[0]["qualname"] if hits else "—"
                logger.info(f"    ✅  [{latency:.2f}s]  '{q[:50]}...'  → top1={top1}")
            except Exception as e:
                logger.info(f"    ❌  '{q[:50]}...'  → ERROR: {e}")
                results[mk][q] = []
        force_rebuild = False  # only rebuild once, on first model
        logger.info()
    return results


# =============================================================================
# 9. MAIN — smoke test
# =============================================================================

if __name__ == "__main__":
    exercise_text = r"""
`````{exercise}
:id: f1e09b57-8f62-4926-a484-1893f724a627
:title: Exercice 1 Asie J1 5 septembre juin 2025 Fonction exponentielle et équation différentielle
:modules: annales_bac, Analysis
:recommendedExecutionTime: 25
:level: Intermediate
:chap: Fonctions exponentielles et équations différentielles
:involvedConcepts: TYPE_BAC, Dérivation, équation différentielle, convexité, théorème des valeurs intermédiaires, intégration par parties
:originalSource: Baccalauréat - Exercice sur les fonctions exponentielles
:visibility: All
:variations:
:comment: Exercice d'analyse avec affirmations vrai/faux sur une fonction exponentielle

{fr}`Soit $f$ la fonction définie sur $\mathbb{R}$ par $f(x) = x\,\mathrm{e}^{-2x}$.

On admet que $f$ est deux fois dérivable sur $\mathbb{R}$.`

$\textit{Pour chacune des affirmations suivantes, préciser si elle est vraie ou fausse, puis justifier
la réponse donnée. Toute réponse non argumentée ne sera pas prise en compte.}$

(contenu tronqué dans le smoke test — l'exercice complet est transmis en contexte)
`````
"""

    list_embedding_models()

    logger.info("\n>>> retrieve_functions_context (no LLM)")
    ctx = retrieve_functions_context(
        exercise=exercise_text,
        embedding_model="openai-3-large",
        top_k=12,
        force_rebuild=False,
    )
    logger.info("\n── CATALOGUE (injectable as {functions}) ──\n")
    logger.info(ctx["catalogue"] + "\n...")
    logger.info(f"\n── imports_block ──\n{ctx['imports_block']}")
    logger.info(f"\n── {len(ctx['entities'])} entities "
          f"({len(ctx['retrieved'])} retrieved + {len(ctx['always_included'])} always) ──")

    # Sanity checks on the new ALWAYS_INCLUDE entries
    entity_names = [e["qualname"] for e in ctx["entities"]]
    logger.info("\n── SANITY ──")
    logger.info(f"  pxs_Interval present: {'pxs_Interval' in entity_names}")
    logger.info(f"  pxsl_pow present:     {'pxsl_pow' in entity_names}")
    for e in ctx["entities"]:
        if e["qualname"] == "pxs_Interval":
            method_names = [m["name"] for m in e.get("methods", [])]
            logger.info(f"  pxs_Interval methods: {method_names}")
            break