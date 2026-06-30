"""
rules_digest.py (ex utils/rules_digest.py)
──────────────────────────────────────────
Parser de `pythonisation_rules.md` + construction de digests ciblés injectés
dans les prompts. Parsé une fois à l'import, caché en module.

API publique :
  RULES_BY_ID         dict[str, Rule]
  ALL_RULE_IDS        list[str]
  build_rules_digest(rule_ids)  → markdown compact
  AUDIT_RULES_ALWAYS  list[str]
"""

from __future__ import annotations

import re
from typing import Optional, TypedDict

from app.config import RULES_MD


class Rule(TypedDict, total=False):
    id:       str
    title:    str
    section:  str
    bad:      Optional[str]
    good:     Optional[str]
    why:      Optional[str]


_RULE_HEADING = re.compile(
    r"^### RÈGLE (?P<id>\d+\.\d+(?:\.\d+)?)\s*—\s*(?P<title>.+?)\s*$",
    re.MULTILINE,
)
_SECTION_HEADING = re.compile(
    r"^## (?P<num>\d+)\.\s*(?P<title>.+?)\s*$",
    re.MULTILINE,
)
_BAD_BLOCK = re.compile(
    r"\*\*❌\s*FAUTIF\*\*[^\n]*\n```(?:[a-zA-Z]*)\n(.+?)\n```",
    re.DOTALL,
)
_GOOD_BLOCK = re.compile(
    r"\*\*✅\s*CORRIG(?:É|EE?|É?)\*\*[^\n]*\n```(?:[a-zA-Z]*)\n(.+?)\n```",
    re.DOTALL,
)
_WHY = re.compile(
    r"\*\*POURQUOI\*\*\s*:\s*(.+?)(?=\n{2,}|\n#{2,3}\s|\Z)",
    re.DOTALL,
)


def _parse_rules(content: str) -> dict[str, Rule]:
    sections: list[tuple[int, str]] = []
    for m in _SECTION_HEADING.finditer(content):
        sections.append((m.start(), f"{m.group('num')}. {m.group('title').strip()}"))

    rule_matches = list(_RULE_HEADING.finditer(content))
    rules: dict[str, Rule] = {}

    for i, m in enumerate(rule_matches):
        rule_id = m.group("id")
        title = m.group("title").strip()
        body_start = m.end()
        body_end = rule_matches[i + 1].start() if i + 1 < len(rule_matches) else len(content)
        body = content[body_start:body_end].strip()

        section_title = ""
        for off, label in sections:
            if off < m.start():
                section_title = label

        bad_m = _BAD_BLOCK.search(body)
        good_m = _GOOD_BLOCK.search(body)
        why_m = _WHY.search(body)

        rules[rule_id] = Rule(
            id=rule_id,
            title=title,
            section=section_title,
            bad=bad_m.group(1).rstrip() if bad_m else None,
            good=good_m.group(1).rstrip() if good_m else None,
            why=why_m.group(1).strip() if why_m else None,
        )
    return rules


_RULES_CACHE: Optional[dict[str, Rule]] = None


def _load_rules() -> dict[str, Rule]:
    global _RULES_CACHE
    if _RULES_CACHE is None:
        _RULES_CACHE = _parse_rules(RULES_MD.read_text(encoding="utf-8"))
    return _RULES_CACHE


RULES_BY_ID: dict[str, Rule] = _load_rules()
ALL_RULE_IDS: list[str] = sorted(
    RULES_BY_ID.keys(),
    key=lambda s: tuple(int(p) for p in s.split(".")),
)


def build_rules_digest(rule_ids: list[str]) -> str:
    """Digest markdown compact des règles demandées (IDs inconnus ignorés)."""
    if not rule_ids:
        return ""
    parts: list[str] = []
    for rid in rule_ids:
        rule = RULES_BY_ID.get(rid)
        if rule is None:
            continue
        parts.append(f"### Règle {rule['id']} — {rule['title']}")
        if rule.get("bad"):
            parts.append("❌ FAUTIF :")
            parts.append(f"```\n{rule['bad']}\n```")
        if rule.get("good"):
            parts.append("✅ CORRECT :")
            parts.append(f"```\n{rule['good']}\n```")
        if rule.get("why"):
            parts.append(f"→ {' '.join(rule['why'].split())}")
        parts.append("")
    return "\n".join(parts).rstrip() + "\n"


# Règles vérifiables sur le texte assemblé seul (pas d'exec) — passe d'audit.
AUDIT_RULES_ALWAYS: list[str] = [
    "2.1",   # :id: vide en première ligne
    "3.1",   # un seul bloc Python principal
    "6.1",   # pas d'appels **kwargs dans {{...}}
    "6.2",   # pas de pxsl_format_number(**kwargs) dans {{...}}
    "6.3",   # variables d'affichage pré-calculées
    "7.1",   # pas de concaténation signe + valeur
    "9.1",   # paragraphes contextuels hors questionStatement
    "9.4",   # pas de doublons d'énoncés
    "11.5",  # plt.show() (pas savefig)
]
