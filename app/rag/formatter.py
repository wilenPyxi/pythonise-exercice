"""
rag_formatter.py
────────────────
Compact, LLM-optimized formatter for retrieved PyxiScience entities.

Replaces the legacy 4-section verbose catalogue (imports / signatures /
names / detailed) with a single structured block per entity, driven by
the :pxs_trigger: / :pxs_returns: / :pxs_example: / :pxs_antipattern:
meta-tags embedded in PyxiScience docstrings.

Entity dict schema expected by `build_catalogue`:

    {
        "qualname":    "pxs_Poly.pxsl_solution",
        "signature":   "(mult='\\times', formula=True)",
        "import_line": "from pyxiscience.Classes_Extensions import pxs_Poly",
        "kind":        "function" | "method" | "class",
        "docstring":   "<raw docstring, :pxs_*: tags intact>",
        # for classes, optionally:
        "methods":     [{"name": str, "signature": str, "summary": str}, ...],
    }

Functions and methods go through `_format_function_entity`.
Classes with a non-empty `methods` list go through `_format_class_entity`.
"""

from __future__ import annotations

import re
import textwrap
from typing import Dict, List


# Regex patterns for the :pxs_*: meta-tags.
# Each one matches non-greedily up to the next :pxs_*: tag or end-of-string,
# so multi-line values are preserved.
_META_TAGS = {
    "trigger":     r":pxs_trigger:\s*(.+?)(?=\n\s*:pxs_|\Z)",
    "returns":     r":pxs_returns:\s*\|?\s*\n?(.+?)(?=\n\s*:pxs_|\Z)",
    "example":     r":pxs_example:\s*\|?\s*\n?(.+?)(?=\n\s*:pxs_|\Z)",
    "antipattern": r":pxs_antipattern:\s*(.+?)(?=\n\s*:pxs_|\Z)",
}


def _extract_meta_tags(docstring: str) -> Dict[str, str]:
    """Parse :pxs_*: tags from an enriched docstring into a flat dict."""
    if not docstring:
        return {}
    meta: Dict[str, str] = {}
    for key, pattern in _META_TAGS.items():
        m = re.search(pattern, docstring, flags=re.DOTALL)
        if m:
            # Normalise indentation & trim trailing whitespace.
            meta[key] = textwrap.dedent(m.group(1)).strip()
    return meta


def _first_useful_line(docstring: str) -> str:
    """
    Fallback summary when no :pxs_trigger: is present.

    Pulls the first non-trivial line BEFORE any :pxs_*: tag, strips
    bilingual prefixes ('Fr :', '\\fr{', 'En :', etc.) and truncates.
    """
    if not docstring:
        return ""
    # Only look at the human-readable head (before the first meta-tag).
    cut = re.search(r"^\s*:pxs_\w+:", docstring, flags=re.MULTILINE)
    head = docstring[: cut.start()] if cut else docstring

    for raw in head.splitlines():
        line = raw.strip()
        if not line or line.startswith((":", "---", "===", "Args:", "Returns:", "Paramètres")):
            continue
        # Strip bilingual markers.
        line = re.sub(r"^(Fr|En|\\fr|\\en)\s*[:{]?\s*", "", line)
        line = line.rstrip("}").strip()
        if len(line) > 10:
            return line[:140]
    return ""


def _indent(text: str, prefix: str = "  ") -> str:
    """Indent every line of a block with a constant prefix."""
    return "\n".join(prefix + line if line else line for line in text.splitlines())


# ────────────────────────────────────────────────────────────────────────
# Per-entity formatters
# ────────────────────────────────────────────────────────────────────────

def _format_function_entity(entity: Dict) -> str:
    """Compact block for a standalone function or (unattached) method."""
    meta = _extract_meta_tags(entity.get("docstring", ""))
    lines: List[str] = []

    # Header: qualified name + signature, then the import line.
    lines.append(f"▸ {entity['qualname']}{entity.get('signature', '(...)')}")
    lines.append(f"  {entity['import_line']}")
    lines.append("")

    trigger = meta.get("trigger") or _first_useful_line(entity.get("docstring", ""))
    if trigger:
        lines.append("QUAND UTILISER")
        lines.append(_indent(trigger))
        lines.append("")

    if meta.get("returns"):
        lines.append("CE QUE ÇA RETOURNE")
        lines.append(_indent(meta["returns"]))
        lines.append("")

    if meta.get("example"):
        lines.append("EXEMPLE D'APPEL")
        lines.append(_indent(meta["example"]))
        lines.append("")

    if meta.get("antipattern"):
        lines.append("NE PAS RÉIMPLÉMENTER MANUELLEMENT")
        lines.append(f"  ✗ {meta['antipattern']}")
        lines.append(f"  ✓ Utiliser {entity['qualname']}")

    while lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines)


def _format_class_entity(entity: Dict) -> str:
    """
    Compact block for a class + its methods. Expects entity['methods'] to be
    a non-empty list of {name, signature, summary} dicts.
    """
    meta = _extract_meta_tags(entity.get("docstring", ""))
    lines: List[str] = []

    lines.append(f"▸ {entity['qualname']} (classe)")
    lines.append(f"  {entity['import_line']}")
    lines.append("")

    lines.append("MÉTHODES DISPONIBLES")
    for m in entity["methods"]:
        sig     = m.get("signature", "(...)")
        summary = (m.get("summary") or "").strip()
        suffix  = f"  — {summary}" if summary else ""
        lines.append(f"  .{m['name']}{sig}{suffix}")
    lines.append("")

    trigger = meta.get("trigger") or _first_useful_line(entity.get("docstring", ""))
    if trigger:
        lines.append("QUAND UTILISER (la classe)")
        lines.append(_indent(trigger))
        lines.append("")

    if meta.get("example"):
        lines.append("EXEMPLE D'USAGE TYPIQUE")
        lines.append(_indent(meta["example"]))
        lines.append("")

    if meta.get("antipattern"):
        lines.append("NE PAS RÉIMPLÉMENTER MANUELLEMENT")
        lines.append(f"  ✗ {meta['antipattern']}")
        lines.append(f"  ✓ Utiliser {entity['qualname']}")

    while lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines)


def _format_entity_for_llm(entity: Dict) -> str:
    """Dispatch: class with methods → grouped block; else → function block."""
    if entity.get("kind") == "class" and entity.get("methods"):
        return _format_class_entity(entity)
    return _format_function_entity(entity)


# ────────────────────────────────────────────────────────────────────────
# Public API
# ────────────────────────────────────────────────────────────────────────

_SEP = "━" * 55


def build_catalogue(entities: List[Dict]) -> str:
    """
    Assemble the full catalogue string from an ordered list of retrieved
    entity dicts. Use this as the `{functions}` injection in a downstream
    code-generation prompt.
    """
    if not entities:
        return "Aucune fonction PyxiScience pertinente détectée pour cet exercice."

    header = [
        "FONCTIONS PYXISCIENCE DISPONIBLES — USAGE OBLIGATOIRE",
        "",
        "Les entités ci-dessous ont été sélectionnées comme pertinentes",
        "pour cet exercice. Utilise-les plutôt que de réimplémenter",
        "leur logique à la main — c'est la différence entre du code",
        "PyxiScience et du code générique qui sera rejeté.",
        "",
    ]

    blocks = [_format_entity_for_llm(e) for e in entities]
    body   = f"\n{_SEP}\n".join([_SEP] + blocks + [_SEP])

    return "\n".join(header) + body


def build_imports_block(entities: List[Dict]) -> str:
    """
    Produce a de-duplicated 'from X import a, b, c' block from the entities,
    grouped by module. For methods, we import the PARENT CLASS (not the
    method itself — that's unimportable).
    """
    by_module: Dict[str, set] = {}
    for e in entities:
        import_line = e.get("import_line", "")
        m = re.match(r"from\s+(\S+)\s+import\s+(.+)", import_line)
        if not m:
            continue
        module, names = m.group(1), m.group(2)
        by_module.setdefault(module, set()).update(
            n.strip() for n in names.split(",") if n.strip()
        )
    if not by_module:
        return "# (aucun import)"
    return "\n".join(
        f"from {mod} import {', '.join(sorted(names))}"
        for mod, names in sorted(by_module.items())
    )