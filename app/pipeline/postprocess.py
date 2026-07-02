"""
postprocess.py
──────────────
Tous les traitements DÉTERMINISTES (sans LLM) appliqués à l'exercice assemblé.

Déplacés depuis routes/pythonise_routes_v2.py :
  • inject_config_standard_in_pair_block (AST : **config_standard sur latex())
  • dedupe questions / blocs python, force_empty_id
  • diff des solutions validées, décimales hardcodées

Nouveaux (alignement sur les conventions réelles de la plateforme,
vérifiées sur 222 exemples : fences {python} à 4 backticks, injections
= variables nues camelCase suffixe Aff, préfixe ${} anti-devise) :
  • normalize_python_fences      — fences {python} → PYTHON_FENCE_BACKTICKS
  • fix_dollar_digit             — `$`+chiffre / `${{` → `${}` (auto-correctif)
  • auto_lift_injections         — TOUTE injection non nue ({{latex(x)}},
                                   {{lc(a)}}, {{obj.print()}}, {{a*b}}) remontée
                                   en variable pré-calculée du bloc principal
  • rename_underscore_injections — variables injectées avec `_` → camelCase
  • detect_languages / strip_language / check_decimals_for_lang
"""

from __future__ import annotations

import ast
import difflib
import logging
import re
from typing import Optional

from app.config import PYTHON_FENCE_BACKTICKS

logger = logging.getLogger(__name__)

PY_FENCE = "`" * PYTHON_FENCE_BACKTICKS

# Fence {python} à 3 OU 4 backticks (lecture tolérante ; l'écriture est
# toujours normalisée à PYTHON_FENCE_BACKTICKS via normalize_python_fences).
PYTHON_FENCE_RE = re.compile(
    r"(?ms)^(?P<open>`{3,4})\{python\}[ \t]*\n(?P<code>.*?)\n(?P=open)[ \t]*$"
)

INJECTION_RE = re.compile(r"\{\{(.*?)\}\}", re.DOTALL)
BARE_IDENT_RE = re.compile(r"^[A-Za-z][A-Za-z0-9]*$")


# ─────────────────────────────────────────────────────────────────────────────
# Utilitaires génériques
# ─────────────────────────────────────────────────────────────────────────────

def strip_fences(text: str) -> str:
    """Retire un wrapper markdown EXTERNE (``` ou ```lang) d'une sortie LLM,
    sans toucher aux fences qui font partie du contenu (```{python}, `````)."""
    text = text.strip()
    if text.startswith("`````"):
        return text
    text = re.sub(r"^```\w*\s*\n", "", text)
    text = re.sub(r"\n```\s*$", "", text)
    return text.strip()


def extract_python_blocks(text: str) -> list[str]:
    """Tous les corps de blocs {python}, dans l'ordre du document."""
    return [m.group("code") for m in PYTHON_FENCE_RE.finditer(text)]


def mask_python_blocks(text: str) -> tuple[str, list[str]]:
    """Remplace chaque bloc {python} par un sentinel ; retourne (masqué, blocs)."""
    blocks: list[str] = []

    def _sub(m: re.Match) -> str:
        blocks.append(m.group(0))
        return f"\x00PYBLOCK{len(blocks) - 1}\x00"

    return PYTHON_FENCE_RE.sub(_sub, text), blocks


def unmask_python_blocks(text: str, blocks: list[str]) -> str:
    for i, b in enumerate(blocks):
        text = text.replace(f"\x00PYBLOCK{i}\x00", b)
    return text


def normalize_python_fences(text: str) -> str:
    """Réécrit toute fence {python} (3 ou 4 backticks) avec exactement
    PYTHON_FENCE_BACKTICKS backticks — convention plateforme (4)."""
    def _sub(m: re.Match) -> str:
        return f"{PY_FENCE}{{python}}\n{m.group('code')}\n{PY_FENCE}"
    return PYTHON_FENCE_RE.sub(_sub, text)


def insert_python_lines(exercise: str, lines: list[str]) -> str:
    """Insère des lignes juste avant le `globals()` du PREMIER bloc {python}
    (bloc principal — les expressions injectées référencent ses variables).
    Les lignes déjà présentes dans l'exercice ne sont pas dupliquées."""
    todo = [l for l in lines if l and l not in exercise]
    if not todo:
        return exercise
    m = PYTHON_FENCE_RE.search(exercise)
    if not m:
        return exercise
    code = m.group("code")
    idx = code.rfind("globals()")
    if idx == -1:
        new_code = code + "\n" + "\n".join(todo)
    else:
        new_code = code[:idx] + "\n".join(todo) + "\n" + code[idx:]
    start, end = m.span()
    return exercise[:start] + f"{m.group('open')}{{python}}\n{new_code}\n{m.group('open')}" + exercise[end:]


# ─────────────────────────────────────────────────────────────────────────────
# **config_standard automatique sur latex(...) — AST, idempotent
# ─────────────────────────────────────────────────────────────────────────────

class LatexTransformer(ast.NodeTransformer):
    def visit_Call(self, node):
        self.generic_visit(node)
        if isinstance(node.func, ast.Name) and node.func.id == "latex":
            has_config = any(
                isinstance(kw, ast.keyword) and kw.arg is None
                and isinstance(kw.value, ast.Name) and kw.value.id == "config_standard"
                for kw in node.keywords
            )
            if not has_config:
                node.keywords.append(
                    ast.keyword(arg=None, value=ast.Name(id="config_standard", ctx=ast.Load()))
                )
        return node


def add_config_standard(code: str) -> str:
    tree = ast.parse(code)
    tree = LatexTransformer().visit(tree)
    ast.fix_missing_locations(tree)
    return ast.unparse(tree)


def inject_config_standard_in_pair_block(block: str) -> str:
    """Applique add_config_standard à chaque bloc {python} d'un bloc de paire.
    Un bloc non parsable (rare) est laissé intact plutôt que de planter."""
    def _sub(m: re.Match) -> str:
        try:
            transformed = add_config_standard(m.group("code"))
        except SyntaxError:
            return m.group(0)
        return f"{m.group('open')}{{python}}\n{transformed}\n{m.group('open')}"
    return PYTHON_FENCE_RE.sub(_sub, block)


# ─────────────────────────────────────────────────────────────────────────────
# Dédoublonnage questions / blocs python
# ─────────────────────────────────────────────────────────────────────────────

_QUESTION_BLOCK_RE = re.compile(r"(:::::\{question\}.*?:::::)", re.DOTALL)


def dedupe_question_blocks(exercise: str) -> tuple[str, int]:
    """Supprime les blocs :::::{question} dont le questionStatement est
    identique (la paire N+1 régénère parfois une question de la paire N)."""
    blocks = list(_QUESTION_BLOCK_RE.finditer(exercise))
    if len(blocks) < 2:
        return exercise, 0

    qstmt_re = re.compile(r"::::\{questionStatement\}\s*\n?(.*?)\n?::::", re.DOTALL)
    seen: set[str] = set()
    to_remove: list[tuple[int, int]] = []
    for m in blocks:
        qm = qstmt_re.search(m.group(1))
        if not qm:
            continue
        key = re.sub(r"\s+", " ", qm.group(1)).strip().lower()
        if key in seen:
            to_remove.append((m.start(), m.end()))
        else:
            seen.add(key)

    if not to_remove:
        return exercise, 0
    new_exercise = exercise
    for start, end in reversed(to_remove):
        new_exercise = new_exercise[:start] + new_exercise[end:]
    return re.sub(r"\n{3,}", "\n\n", new_exercise), len(to_remove)


def dedupe_python_blocks(exercise: str) -> tuple[str, int]:
    """Supprime les blocs {python} identiques (modulo espaces)."""
    blocks = list(PYTHON_FENCE_RE.finditer(exercise))
    if len(blocks) < 2:
        return exercise, 0
    seen: set[str] = set()
    to_remove: list[tuple[int, int]] = []
    for m in blocks:
        key = re.sub(r"\s+", " ", m.group("code")).strip()
        if key in seen:
            to_remove.append((m.start(), m.end()))
        else:
            seen.add(key)
    if not to_remove:
        return exercise, 0
    new_exercise = exercise
    for start, end in reversed(to_remove):
        new_exercise = new_exercise[:start] + new_exercise[end:]
    return re.sub(r"\n{3,}", "\n\n", new_exercise), len(to_remove)


def fix_orphan_python_openers(exercise: str) -> tuple[str, int]:
    """Supprime un opener {python} immédiatement suivi (à blanc près) d'un
    autre opener — malformation LLM observée qui fait avaler un bloc entier
    par la regex de fence et casse l'extraction du code."""
    new, n = re.subn(
        r"(?m)^`{3,4}\{python\}[ \t]*\n\s*(?=`{3,4}\{python\}[ \t]*$)",
        "",
        exercise,
    )
    return new, n


def renumber_question_ids(exercise: str) -> tuple[str, int]:
    """Renumérote :questionId: et :questionIndex: en séquence 0..N-1 dans
    l'ordre du document (invariant plateforme : uniques et contigus). Le LLM
    se trompe parfois sur les exercices longs — la renumérotation d'office
    est toujours correcte."""
    changed = {"n": 0}

    def _renum(field: str, text: str) -> str:
        counter = {"i": -1}

        def _sub(m: re.Match) -> str:
            counter["i"] += 1
            if m.group(1) != str(counter["i"]):
                changed["n"] += 1
            return f":{field}: {counter['i']}"

        return re.sub(rf":{field}:\s*(\d+)", _sub, text)

    new = _renum("questionId", exercise)
    new = _renum("questionIndex", new)
    return new, changed["n"]


def fix_superscript_double_brace(exercise: str) -> tuple[str, int]:
    """`^{{\\frac…}}` / `_{{\\sqrt…}}` : le `{` LaTeX collé au `{` du
    superscript simule une ouverture d'injection `{{`. On insère un espace
    (`^{ {\\frac…} }`) UNIQUEMENT quand le contenu commence par une commande
    LaTeX — jamais quand c'est une vraie injection `^{{var}}`."""
    masked, blocks = mask_python_blocks(exercise)
    new, n = re.subn(r"([\^_])\{\{(?=\s*\\)", r"\1{ {", masked)
    if not n:
        return exercise, 0
    return unmask_python_blocks(new, blocks), n


def unwrap_latex_injections(exercise: str) -> tuple[str, int]:
    """`{{ \\frac{\\pi}{ {{xAff}} } }}` → `\\frac{\\pi}{ {{xAff}} }` :
    quand le LLM enveloppe du LaTeX (ou une injection imbriquée) dans des
    `{{ }}`, on retire la paire EXTERNE (scan à accolades équilibrées) —
    l'injection interne reste la vraie."""
    masked, blocks = mask_python_blocks(exercise)
    out: list[str] = []
    i, n, removed = 0, len(masked), 0
    while i < n:
        if masked.startswith("{{", i):
            # contenu commence-t-il par du LaTeX (\) ou une injection imbriquée ?
            j = i + 2
            while j < n and masked[j] in " \t":
                j += 1
            if j < n and (masked[j] == "\\" or masked.startswith("{{", j)):
                # scan équilibré depuis i+2 (profondeur 2)
                depth, k = 2, i + 2
                while k < n and depth > 0:
                    if masked[k] == "{":
                        depth += 1
                    elif masked[k] == "}":
                        depth -= 1
                    k += 1
                if depth == 0 and k - 2 >= i + 2 and masked[k - 2:k] == "}}":
                    inner = masked[i + 2:k - 2]
                    out.append(inner)
                    removed += 1
                    i = k
                    continue
        out.append(masked[i])
        i += 1
    if not removed:
        return exercise, 0
    return unmask_python_blocks("".join(out), blocks), removed


def drop_empty_python_blocks(exercise: str) -> tuple[str, int]:
    """Supprime les blocs {python} VIDES (rien, ou seulement `globals()` /
    commentaires) — la génération par paires en insère parfois un entre deux
    questions ; le skill exige UN SEUL bloc utile (relecture 2026-06-12)."""
    removed = {"n": 0}

    def _sub(m: re.Match) -> str:
        body = "\n".join(
            l for l in m.group("code").splitlines()
            if l.strip() and not l.strip().startswith("#") and l.strip() != "globals()"
        )
        if body.strip():
            return m.group(0)
        removed["n"] += 1
        return ""

    new = PYTHON_FENCE_RE.sub(_sub, exercise)
    if removed["n"]:
        new = re.sub(r"\n{3,}", "\n\n", new)
    return new, removed["n"]


def force_empty_id(exercise: str) -> tuple[str, bool]:
    """Règle 2.1 — vide la valeur de `:id:` si elle est renseignée."""
    new = re.sub(r"^(\s*:id:)[ \t]+[^\n]+$", r"\1", exercise, flags=re.MULTILINE)
    return new, (new != exercise)


# ─────────────────────────────────────────────────────────────────────────────
# Auto-correctif `$` collé à un chiffre (règle du skill §1) — casse silencieuse
# ─────────────────────────────────────────────────────────────────────────────

def fix_dollar_digit(exercise: str) -> tuple[str, list[dict]]:
    """Hors blocs {python} :
       • `$` non échappé immédiatement suivi d'un chiffre  → `${}` + chiffre
       • `$` non échappé immédiatement suivi de `{{`       → `${}{{`
    Le groupe vide {} est invisible au rendu mais empêche la lecture
    « montant en devise » qui désynchronise tout le `$…$`.
    EXCLUSION : les lignes `:solution:` (FGQ) — c'est un motif de
    correspondance de réponse, pas du texte affiché ; un `${}` y casserait
    la correction automatique."""
    masked, blocks = mask_python_blocks(exercise)
    # Masque les lignes :solution: (elles ne doivent pas être réécrites).
    sol_lines: list[str] = []

    def _mask_sol(m: re.Match) -> str:
        sol_lines.append(m.group(0))
        return f"\x00SOLLINE{len(sol_lines) - 1}\x00"

    masked = re.sub(r"(?m)^:solution:.*$", _mask_sol, masked)
    patches: list[dict] = []

    def _digit(m: re.Match) -> str:
        patches.append({
            "rule": "$+chiffre",
            "location": m.group(0),
            "fix": "${}" + m.group(1),
            "message": "Auto-correctif : `$` collé à un chiffre préfixé par un groupe vide {} (anti-devise).",
            "iteration": 0,
        })
        return "${}" + m.group(1)

    def _inj(m: re.Match) -> str:
        patches.append({
            "rule": "$+chiffre",
            "location": "${{",
            "fix": "${}{{",
            "message": "Auto-correctif : injection inline `${{…}}` préfixée par {} (le rendu peut commencer par un chiffre).",
            "iteration": 0,
        })
        return "${}{{"

    masked = re.sub(r"(?<!\\)\$(?!\{)(\d)", _digit, masked)
    masked = re.sub(r"(?<!\\)\$\{\{", _inj, masked)
    for i, line in enumerate(sol_lines):
        masked = masked.replace(f"\x00SOLLINE{i}\x00", line)
    return unmask_python_blocks(masked, blocks), patches


def fix_triple_braces(exercise: str) -> tuple[str, list[dict]]:
    """`x^{{{exp}}}` (triple accolade, motif interdit) → `x^{ {{exp}} }`.
    Sans cette normalisation, le découpage des injections est ambigu et
    l'auto-lift peut produire du Python invalide."""
    masked, blocks = mask_python_blocks(exercise)
    patches: list[dict] = []
    n = 0
    while "{{{" in masked or "}}}" in masked:
        masked = masked.replace("{{{", "{ {{", 1) if "{{{" in masked else masked
        masked = masked.replace("}}}", "}} }", 1) if "}}}" in masked else masked
        n += 1
        if n > 500:   # garde-fou anti-boucle
            break
    if n:
        patches.append({
            "rule": "6.1",
            "location": "{{{ / }}}",
            "fix": "{ {{ / }} }",
            "message": f"Triple-accolade normalisée avec espaces ({n} remplacement(s)) — motif interdit qui casse la substitution.",
            "iteration": 0,
        })
    return unmask_python_blocks(masked, blocks), patches


# ─────────────────────────────────────────────────────────────────────────────
# Auto-lift GÉNÉRALISÉ : toute injection non nue → variable pré-calculée
# (les 222 exemples plateforme n'ont AUCUN appel/expr dans {{ }} — uniquement
#  des noms nus camelCase ; le harnais le vérifie en statique)
# ─────────────────────────────────────────────────────────────────────────────

_LIFT_SUFFIX = {"latex": "Tex"}


def _camel(name: str) -> str:
    parts = [p for p in name.split("_") if p]
    if not parts:
        return name
    return parts[0] + "".join(p[:1].upper() + p[1:] for p in parts[1:])


def auto_lift_injections(exercise: str) -> tuple[str, list[dict]]:
    """Remplace chaque `{{ <expr non nue> }}` par `{{ <varAff> }}` et insère
    `<varAff> = <expr>` avant le globals() du bloc principal.

    Couvre : appels ({{latex(f)}}, {{lc(a, sign=True)}}, y compris avec
    **config_standard), attributs ({{dom.print()}}), opérations ({{a*b}}).
    Idempotent : expressions identiques → même variable ; lignes déjà
    présentes non dupliquées."""
    masked, blocks = mask_python_blocks(exercise)
    patches: list[dict] = []
    lifted: dict[str, str] = {}      # expr normalisée → nom de variable
    used_names: set[str] = set(re.findall(r"\b([A-Za-z_]\w*)\s*=", exercise))
    counter = {"n": 0}

    def _make_name(expr: str) -> str:
        m = re.match(r"^([A-Za-z_]\w*)\s*\(\s*([A-Za-z_]\w*)\s*(?:,\s*\*\*\s*config_standard\s*)?\)$", expr)
        if m:
            func, arg = m.group(1), m.group(2)
            base = _camel(arg) + _LIFT_SUFFIX.get(func, "Aff")
        else:
            counter["n"] += 1
            base = f"injAff{counter['n']}"
        name, i = base, 2
        while name in used_names:
            name = f"{base}{i}"
            i += 1
        used_names.add(name)
        return name

    def _sub(m: re.Match) -> str:
        expr = m.group(1).strip()
        if not expr or BARE_IDENT_RE.match(expr):
            return m.group(0)                      # déjà nu (ou vide → harnais)
        if re.match(r"^[A-Za-z][A-Za-z0-9_]*$", expr):
            return m.group(0)                      # identifiant avec _ → renommage dédié
        if "{" in expr or "}" in expr or "\n" in expr:
            return m.group(0)                      # découpage ambigu → on ne lifte pas
        try:                                       # l'insert DOIT être du Python valide
            compile(f"_x = {expr}", "<lift>", "exec")
        except SyntaxError:
            logger.warning("Auto-lift refusé (expression non compilable) : %r", expr[:80])
            return m.group(0)
        key = re.sub(r"\s+", " ", expr)
        if key in lifted:
            name = lifted[key]
            insert = None
        else:
            name = _make_name(expr)
            lifted[key] = name
            insert = f"{name} = {expr}"
        patches.append({
            "rule": "6.1",
            "location": m.group(0),
            "fix": "{{" + name + "}}",
            "python_insert": insert,
            "message": "Auto-lift déterministe : expression dans {{…}} pré-calculée en variable d'affichage.",
            "iteration": 0,
        })
        return "{{" + name + "}}"

    new_masked = INJECTION_RE.sub(_sub, masked)
    if not patches:
        return exercise, []
    new_exercise = unmask_python_blocks(new_masked, blocks)
    new_exercise = insert_python_lines(
        new_exercise, [p["python_insert"] for p in patches if p.get("python_insert")]
    )
    return new_exercise, patches


def rename_underscore_injections(exercise: str) -> tuple[str, list[dict]]:
    """Les `_` dans une variable injectée cassent la substitution plateforme
    (indices LaTeX parasites). Renomme p_str → pStr partout (corps + python)."""
    masked, blocks = mask_python_blocks(exercise)
    names = {
        tok.strip() for tok in INJECTION_RE.findall(masked)
        if re.match(r"^[A-Za-z][A-Za-z0-9_]*$", tok.strip()) and "_" in tok
    }
    if not names:
        return exercise, []

    taken = set(re.findall(r"\b([A-Za-z_]\w*)\b", exercise))
    patches: list[dict] = []
    new_exercise = exercise
    for old in sorted(names, key=len, reverse=True):
        new = _camel(old)
        i = 2
        while new in taken:
            new = f"{_camel(old)}{i}"
            i += 1
        taken.add(new)
        new_exercise = re.sub(rf"\b{re.escape(old)}\b", new, new_exercise)
        patches.append({
            "rule": "6.3",
            "location": f"{{{{{old}}}}}",
            "fix": f"{{{{{new}}}}}",
            "message": f"Variable injectée renommée {old} → {new} (underscore interdit dans {{{{…}}}}).",
            "iteration": 0,
        })
    return new_exercise, patches


# ─────────────────────────────────────────────────────────────────────────────
# Solutions validées : extraction / diff pédagogique (règle 8.1)
# ─────────────────────────────────────────────────────────────────────────────

_DETAILED_SOLUTION_RE = re.compile(
    r"::::\{detailedSolution\}\s*\n(.*?)\n::::",
    re.DOTALL,
)

_STOPWORDS = frozenset({
    # FR
    "des", "les", "une", "est", "que", "qui", "par", "pour", "avec", "sur", "dans",
    "ces", "son", "ses", "leur", "leurs", "cette", "donc", "ainsi", "alors", "plus",
    "moins", "tout", "tous", "toute", "toutes", "aussi", "mais", "comme", "puis",
    "soit", "deux", "trois", "fois",
    # EN
    "the", "and", "are", "for", "with", "from", "then", "this", "that", "these",
    "those", "have", "has", "been", "their", "there", "where", "when", "which",
    "also", "but", "more", "less", "than", "into", "only", "thus", "such", "very",
})


def extract_detailed_solutions(myst_text: str) -> list[str]:
    return [m.group(1).strip() for m in _DETAILED_SOLUTION_RE.finditer(myst_text)]


def _extract_pedagogical_words(text: str) -> list[str]:
    """Mots porteurs de sens pédagogique (hors placeholders, nombres, LaTeX)."""
    cleaned = re.sub(r"\{\{[^}]*\}\}", " ", text)
    cleaned = re.sub(r"\\[a-zA-Z]+\*?\s*\{[^}]*\}", " ", cleaned)
    cleaned = re.sub(r"\\[a-zA-Z]+\*?", " ", cleaned)
    cleaned = re.sub(r"-?\d+(?:[.,]\d+)?", " ", cleaned)
    cleaned = re.sub(r"\{[a-zA-Z*]+\}", " ", cleaned)
    cleaned = cleaned.replace("`", " ")
    tokens = re.findall(r"[a-zA-ZÀ-ÿ]{3,}", cleaned)
    return [t.lower() for t in tokens if t.lower() not in _STOPWORDS]


def diff_solutions(original_content: str, generated_exercise: str) -> list[dict]:
    """Compare les detailedSolution source ↔ sortie (mots pédagogiques seuls).
    Warning si divergence (similarité < 95 %) — règle 8.1."""
    orig = extract_detailed_solutions(original_content)
    gen = extract_detailed_solutions(generated_exercise)
    warnings: list[dict] = []
    if not orig:
        return warnings
    if len(orig) != len(gen):
        warnings.append({
            "rule": "8.1",
            "message": (f"Nombre de detailedSolution différent : {len(orig)} dans la source, "
                        f"{len(gen)} dans la sortie."),
        })
    for i, (o, g) in enumerate(zip(orig, gen)):
        o_words = _extract_pedagogical_words(o)
        g_words = _extract_pedagogical_words(g)
        if o_words == g_words:
            continue
        ratio = difflib.SequenceMatcher(None, o_words, g_words).ratio()
        if ratio >= 0.95:
            continue
        severity = "FORTE divergence" if ratio < 0.70 else "divergence"
        missing = [w for w in o_words if w not in g_words][:5]
        added = [w for w in g_words if w not in o_words][:5]
        hint = ""
        if missing:
            hint += f" Mots disparus : {', '.join(missing)}."
        if added:
            hint += f" Mots ajoutés : {', '.join(added)}."
        warnings.append({
            "rule": "8.1",
            "message": (f"Question {i + 1} : detailedSolution {severity} vs source "
                        f"(similarité pédagogique = {ratio:.0%}).{hint} "
                        "Vérifier que le raisonnement original est préservé (règle 8.1)."),
        })
    return warnings


_DECIMAL_LITERAL_RE = re.compile(r"\b\d+\{,\}\d+\b")
_DECIMAL_DOT_RE = re.compile(r"(?<![\\\w])\d+\.\d+(?!\w)")
_INTERP_RE = re.compile(r"\{\{[^}]*\}\}")


def check_hardcoded_decimals_in_solutions(exercise: str) -> list[dict]:
    """Règle 4.3 (ext.) : décimale littérale hors {{…}} dans une solution
    → probable valeur codée en dur qui ne suivra pas la randomisation."""
    warnings: list[dict] = []
    for i, m in enumerate(_DETAILED_SOLUTION_RE.finditer(exercise)):
        stripped = _INTERP_RE.sub(" ", m.group(1))
        hits = list(_DECIMAL_LITERAL_RE.finditer(stripped)) + list(_DECIMAL_DOT_RE.finditer(stripped))
        seen: set[str] = set()
        unique: list[str] = []
        for h in hits:
            text = h.group(0)
            if text in seen or text.startswith("10.") or text.endswith("e"):
                continue
            seen.add(text)
            unique.append(text)
            if len(unique) >= 3:
                break
        if unique:
            warnings.append({
                "rule": "4.3",
                "message": (f"Question {i + 1} : detailedSolution contient des décimales littérales "
                            f"({', '.join(repr(h) for h in unique)}) hors `{{{{var}}}}`. Si l'exo "
                            "randomise un paramètre dont elles dérivent, elles ne suivront pas la "
                            "variation. Vérifier qu'elles sont injectées."),
            })
    return warnings


# ─────────────────────────────────────────────────────────────────────────────
# Déclinaisons QCM/QAT — filets déterministes (mode `declinaisons`)
# ─────────────────────────────────────────────────────────────────────────────

QUESTION_BLOCK_RE = _QUESTION_BLOCK_RE          # réutilisé par le harnais étendu
MCQ_ANSWER_RE = re.compile(
    r"::::\{mcqAnswer\}\s*\n:isRightAnswer:\s*(true|false)\s*\n(.*?)\n::::",
    re.DOTALL,
)
_NONE_OPTION_RE = re.compile(r"Aucune de ces réponses|None of these answers", re.IGNORECASE)


def fix_none_option_last(exercise: str) -> tuple[str, int]:
    """MCQ : l'option « Aucune de ces réponses / None » doit être le DERNIER
    mcqAnswer de sa question — on la déplace si besoin (filet déterministe)."""
    moved = {"n": 0}

    def _fix_question(qm: re.Match) -> str:
        block = qm.group(0)
        answers = list(MCQ_ANSWER_RE.finditer(block))
        if len(answers) < 2:
            return block
        none_idx = [i for i, a in enumerate(answers) if _NONE_OPTION_RE.search(a.group(2))]
        if not none_idx or none_idx[-1] == len(answers) - 1:
            return block
        i = none_idx[-1]
        none_text = answers[i].group(0)
        # retire l'option None puis la réinsère après le dernier mcqAnswer
        block2 = block.replace(none_text + "\n\n", "", 1).replace(none_text, "", 1)
        last = list(MCQ_ANSWER_RE.finditer(block2))[-1]
        block2 = block2[:last.end()] + "\n\n" + none_text + block2[last.end():]
        moved["n"] += 1
        return block2

    new = QUESTION_BLOCK_RE.sub(_fix_question, exercise)
    return new, moved["n"]


def fix_mcq_answer_aliases(exercise: str) -> tuple[str, int]:
    """Normalise les blocs d'options MCQ mal nommés/incomplets (vus en prod) :
      • `::::{mcqOption}` / `::::{mcqChoice}` → `::::{mcqAnswer}` ;
      • bloc mcqAnswer SANS ligne `:isRightAnswer:` → insère `false` (défaut)."""
    fixed = {"n": 0}
    out, n_alias = re.subn(r"(?m)^::::\{mcq(?:Option|Choice)\}", "::::{mcqAnswer}", exercise)
    fixed["n"] += n_alias

    def _ensure_flag(m: re.Match) -> str:
        head, rest = m.group(1), m.group(2)
        if rest.lstrip().startswith(":isRightAnswer:"):
            return m.group(0)
        fixed["n"] += 1
        return f"{head}:isRightAnswer: false\n{rest}"

    out = re.sub(r"(?ms)^(::::\{mcqAnswer\}\n)(.*?)(?=^::::$)",
                 lambda m: _ensure_flag(m), out)
    return out, fixed["n"]


def merge_decl_python_blocks(exercise: str) -> tuple[str, int]:
    """DÉCLINAISONS : la spec impose UN SEUL bloc {python}. Fusionne les blocs
    additionnels dans le bloc principal (ordre préservé, un seul `globals()`
    final) — SAUF si un bloc ultérieur RE-TIRE de l'aléatoire (`rd.`/`random.`) :
    re-tirage = bug sémantique (valeurs incohérentes entre questions), on le
    laisse en place pour que le harnais le signale et que la réparation LLM
    corrige à la source."""
    blocks = list(PYTHON_FENCE_RE.finditer(exercise))
    if len(blocks) < 2:
        return exercise, 0
    extras = blocks[1:]
    if any(re.search(r"\brd\.|(?<!_)\brandom\.", m.group("code")) for m in extras):
        return exercise, 0          # re-tirage suspect → laisser le harnais trancher

    main = blocks[0]
    parts = [re.sub(r"(?m)^\s*globals\(\)\s*$", "", main.group("code")).rstrip()]
    for m in extras:
        code = re.sub(r"(?m)^\s*globals\(\)\s*$", "", m.group("code")).strip()
        if code:
            parts.append(code)
    merged_code = "\n\n".join(parts) + "\n\nglobals()"

    # Supprime les blocs additionnels (indices inversés), puis remplace le principal.
    out = exercise
    for m in reversed(extras):
        out = out[:m.start()] + out[m.end():]
    m0 = PYTHON_FENCE_RE.search(out)
    out = (out[:m0.start()]
           + f"{m0.group('open')}{{python}}\n{merged_code}\n{m0.group('open')}"
           + out[m0.end():])
    return re.sub(r"\n{3,}", "\n\n", out), len(extras)


# (Les contrôles statiques MCQ/FGQ — {{}} dans un rôle, :solution:, résidus
#  légacy — vivent dans validation/harness.py::check_declinaison_static :
#  une seule source de vérité pour le verdict.)


# ─────────────────────────────────────────────────────────────────────────────
# Langues : détection, réduction bilingue → mono, contrôle des décimales
# ─────────────────────────────────────────────────────────────────────────────

_ROLE_RE = {
    "fr": re.compile(r"\{fr\}`([^`]*)`"),
    "en": re.compile(r"\{en\}`([^`]*)`"),
}
_FR_HINTS = (" le ", " la ", " les ", " une ", " des ", " est ", " que ", " pour ",
             "Calculer", "Montrer", "Déterminer", "Résoudre", "On considère", "définie")
_EN_HINTS = (" the ", " a ", " an ", " is ", " that ", " for ", " of ",
             "Compute", "Show", "Determine", "Solve", "We consider", "defined")


def detect_languages(text: str) -> str:
    """Retourne 'both' si les rôles {fr}`…`/{en}`…` sont présents, sinon
    'fr' ou 'en' par heuristique de mots-outils sur la prose."""
    body, _ = mask_python_blocks(text)
    if _ROLE_RE["fr"].search(body) and _ROLE_RE["en"].search(body):
        return "both"
    fr_score = sum(body.count(h) for h in _FR_HINTS)
    en_score = sum(body.count(h) for h in _EN_HINTS)
    return "fr" if fr_score >= en_score else "en"


def strip_language(text: str, keep: str) -> str:
    """Réduction déterministe d'un exercice bilingue (rôles {fr}`…`{en}`…`)
    vers une seule langue : déballe la langue gardée, supprime l'autre."""
    drop = "en" if keep == "fr" else "fr"
    masked, blocks = mask_python_blocks(text)
    masked = _ROLE_RE[drop].sub("", masked)
    masked = _ROLE_RE[keep].sub(lambda m: m.group(1), masked)
    masked = re.sub(r"[ \t]+\n", "\n", masked)
    masked = re.sub(r"  +", " ", masked)
    return unmask_python_blocks(masked, blocks)


def check_decimals_for_lang(exercise: str, lang: str) -> list[dict]:
    """Décimales conformes à la langue : FR = virgule ({,}), EN = point.
    En bilingue, chaque rôle est contrôlé séparément."""
    body, _ = mask_python_blocks(exercise)
    body = _INTERP_RE.sub(" ", body)   # les valeurs injectées sont contrôlées par ailleurs
    warnings: list[dict] = []

    def _scan(segment: str, seg_lang: str, where: str):
        if seg_lang == "fr":
            hits = [h.group(0) for h in _DECIMAL_DOT_RE.finditer(segment)
                    if not h.group(0).startswith("10.")]
            if hits:
                warnings.append({
                    "rule": "décimales",
                    "message": (f"Décimales à POINT dans du texte FR ({where}) : "
                                f"{', '.join(sorted(set(hits))[:4])} — attendu virgule `{{,}}`."),
                })
        else:
            hits = [h.group(0) for h in _DECIMAL_LITERAL_RE.finditer(segment)]
            if hits:
                warnings.append({
                    "rule": "décimales",
                    "message": (f"Décimales à VIRGULE dans du texte EN ({where}) : "
                                f"{', '.join(sorted(set(hits))[:4])} — attendu point décimal."),
                })

    if lang == "both":
        _scan(" ".join(_ROLE_RE["fr"].findall(body)), "fr", "rôles {fr}")
        _scan(" ".join(_ROLE_RE["en"].findall(body)), "en", "rôles {en}")
    else:
        _scan(body, lang, "corps")
    return warnings
