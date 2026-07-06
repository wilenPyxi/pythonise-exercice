"""
prompts.py
──────────
Tous les prompts LLM du pipeline.

# v1 → les versions antérieures (STEP1_PROMPT, STEP_PAIR_PROMPT, SYSTEM_PROMPT,
# STEP_AUDIT_PROMPT) sont archivées VERBATIM dans
# app/knowledge/prompts_v1_archive.md (extraites de routes/pythonise_routes_v2.py
# avant la refonte du 2026-06-12).
#
# Changements majeurs v1 → v2 (alignement sur les conventions RÉELLES de la
# plateforme, vérifiées sur les 222 exemples pythonisés livrés + skill
# pyxiscience-pythonisation) :
#   • Injections {{ }} = UNIQUEMENT des noms de variables nus, camelCase,
#     suffixe Aff, sans underscore. La v1 enseignait {{latex(expr)}},
#     {{lc(a, sign=True)}}, {{pxsl_res_num(...)}} — tous absents des exemples
#     validés et refusés par le harnais.
#   • Bloc {python} à 4 backticks (la v1 montrait 3) ; enveloppe exercise à 5.
#   • Bilingue = rôles inline {fr}`…`{en}`…` UNIQUEMENT (aucun bloc
#     :::{fr}/:::{en} dans les 222 exemples — la v1 les enseignait).
#   • Règle du `$` collé à un chiffre (préfixe ${}) — absente de la v1.
#   • Fraction (module fractions) interdit en sortie de formateur ;
#     pxsl_format_number SANS kwargs ; décimales localisées FR/EN.
#   • Few-shot du type détecté injecté ({fewshot}) au lieu de 5 exemples
#     génériques pavés dans le prompt.
#   • SYSTEM_PROMPT raccourci (le dump de 180 lignes du source de
#     pxsl_res_num doublonnait le catalogue RAG).
"""

# ─────────────────────────────────────────────────────────────────────────────
# STEP 1 — Analyse (variables + règles à risque + invariants)
# v1 → app/knowledge/prompts_v1_archive.md §STEP1_PROMPT
# (v2 : typo needs_matplolib corrigée → needs_matplotlib ; mention du type
#  pour la sélection de few-shot ; sinon structure conservée)
# ─────────────────────────────────────────────────────────────────────────────
STEP1_PROMPT = """\
Tu es un expert en analyse d'exercices mathématiques & détection des variables Python pour PyxiScience,
pour passer d'un exercice à valeurs statiques à un exercice à valeurs aléatoires **correctes**.

EXERCICE :
{content}

─────────────────────────────────────────────────────
MISSION : analyse cet exercice et identifie **TOUTES** les entités mathématiques
qui devront être générées aléatoirement en Python.

Couvre TOUS les types possibles : scalaires entiers/réels, fractions, listes,
vecteurs, matrices, ensembles, polynômes, fonctions, pourcentages, angles, intervalles…

Pour chaque variable :
  • nom           : nom Python valide court (ex: a, b, n, matA, listeNotes),
                    partageable entre questions
  • type_python   : "int"|"float"|"Fraction"|"list"|"matrix"|"set"|"vector"|"other"
  • description   : rôle dans l'énoncé (1 phrase)
  • contraintes   : contraintes mathématiques (ex: a ≠ 0, n ∈ [2,10])
  • plage_python  : expression Python exacte de génération aléatoire
  • location      : "énoncé"|"inter-question"|"question"|"solution 1"|…|"solution 5"
  • valeur_exemple: valeur typique

─────────────────────────────────────────────────────
RÈGLES DE PYTHONISATION (catalogue) — choisis dans "target_rules" celles qui
sont LE PLUS À RISQUE pour CET exercice (5 à 12 IDs maximum).

{available_rules_menu}

─────────────────────────────────────────────────────
Réponds UNIQUEMENT en JSON valide :
{{
  "exercise_type": "...",
  "exercise_title": "...",
  "exercise_summary": "...",
  "suggested_concepts": ["..."],
  "nb_questions": 1,
  "variables": [
    {{
      "nom": "...",
      "type_python": "...",
      "description": "...",
      "contraintes": "...",
      "location": "énoncé|question|solution 1",
      "plage_python": "...",
      "valeur_exemple": "..."
    }}
  ],
  "needs_fraction": false,
  "needs_sympy": false,
  "needs_numpy": false,
  "needs_matplotlib": false,
  "mathematical_structure": "...",
  "target_rules": ["3.1", "4.1", "6.1"],
  "property_constraints": [
    "<invariant mathématique en français — ex: w_n ≥ n pour tout n>"
  ],
  "has_validated_solution_in_input": false
}}

Notes :
  • "exercise_type" : type court et standard (ex: "équation linéaire",
    "trinôme/discriminant", "fonction avec figure", "logarithme/exponentielle",
    "système linéaire", "intégration par parties", "probabilités/binomiale",
    "suites", "finance/intérêts") — il sert à choisir un exemple canonique.
  • "target_rules" : uniquement des IDs du catalogue ci-dessus (top 5-12 à risque).
  • "property_constraints" : invariants à préserver au tirage (règle 4.3). Liste vide si aucun.
  • "has_validated_solution_in_input" : true SI l'énoncé contient déjà des
    blocs `::::{{detailedSolution}}` rédigés (règles 8.1–8.3).
"""


# ─────────────────────────────────────────────────────────────────────────────
# SYSTEM — rôle + sémantique du runtime {{ }}
# v1 → app/knowledge/prompts_v1_archive.md §SYSTEM_PROMPT
# ─────────────────────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """\
Tu es professeur de mathématiques, expert en Python scientifique (sympy, random,
math, matplotlib, numpy) et en exercices PyxiScience randomisés (MyST + KaTeX).

Le code Python vit dans UN bloc ````{python} … ```` (4 backticks) terminé par
`globals()`. Les variables y définies sont injectées dans le MyST via `{{ var }}`.

⚠️ La syntaxe `{{ var }}` est exécutée par un runtime Python maison — PAS du
Jinja. RÈGLE ABSOLUE : `{{ … }}` contient UNIQUEMENT un nom de variable nu,
en camelCase, SANS underscore, généralement suffixé `Aff` pour les affichages
(ex: `{{coefAAff}}`). JAMAIS d'appel de fonction, de calcul, de filtre ni de
logique dans `{{ }}` — tout est pré-calculé dans le bloc Python.

Deux règles d'or :
1. Tout ce qui s'affiche est PRÉ-CALCULÉ dans une variable puis injecté tel quel.
2. On ne code JAMAIS en dur une réponse vraie seulement pour les valeurs de la
   source : si un paramètre est randomisé, la réponse affichée est RECALCULÉE.

Priorité aux helpers du catalogue PyxiScience (pxsl_latex_coefficient/lc,
pxsl_res_num, pxsl_format_number, pxsl_matrix, pxs_Interval, pxs_config…) —
appelés DANS le bloc Python, résultat stocké dans une variable `…Aff`.
Ne jamais réimplémenter un helper existant.

Exercices applicatifs : contexte ÉCONOMIE/GESTION (finance, comptabilité,
marketing, microéconomie — registre école de commerce), jamais physique/chimie.
"""


# ─────────────────────────────────────────────────────────────────────────────
# STEP 2+ — Génération par paires
# v1 → app/knowledge/prompts_v1_archive.md §STEP_PAIR_PROMPT
# ─────────────────────────────────────────────────────────────────────────────
STEP_PAIR_PROMPT = """\
Tu pythonises un exercice PyxiScience MyST, niveau {niveau}.
Transformer l'exercice statique (valeurs fixes) en version randomisée
(paramètres tirés en Python + injectés dans le MyST), EN respectant à la
lettre les conventions de la plateforme ci-dessous.

═══════════════════════════════════════════════════════════════════════════
 CONVENTIONS PLATEFORME (vérifiées sur les exercices livrés — NON NÉGOCIABLES)
═══════════════════════════════════════════════════════════════════════════

STRUCTURE :
  • Enveloppe exercice : 5 backticks `````{{exercise}} … ````` (déjà gérée).
  • UN bloc Python principal : 4 backticks ````{{python}} … ```` terminé par
    `globals()`. Imports en tête (`import random as rd`, sympy ciblé,
    `from pyxiscience.Mes_fctions_generalistes_bis import pxs_config,
    pxsl_latex_coefficient as lc` …) puis `config_standard = pxs_config()`.
  • Chaque question : `:::::{{question}}` (5 deux-points) avec
    `:questionType:`, `:questionId:`, `:questionIndex:` (contigus depuis 0) ;
    sous-blocs `::::{{questionStatement}}`, `::::{{questionHint}}`,
    `::::{{detailedSolution}}`, `::::{{weightDistribution}}` (4 deux-points).
  • `:weightDistribution:` : recopier les poids de la source VERBATIM
    (somme = 100 par question).

INJECTIONS `{{{{ }}}}` — LA règle qui fait tout casser si violée :
  • UNIQUEMENT un nom de variable NU : `{{{{coefAAff}}}}`, `{{{{resQ1Aff}}}}`.
    camelCase, SANS underscore, suffixe `Aff` pour tout affichage.
  • INTERDIT dans `{{{{ }}}}` : appel de fonction (`latex(...)`, `lc(...)`,
    `pxsl_…(...)`, `obj.print()`), calcul (`a*b`), `round(...)`, `**kwargs`.
    → TOUT se pré-calcule dans le bloc Python :
      `eqAff = latex(a*x**2 + b*x + c, **config_standard)` puis `{{{{eqAff}}}}`.
  • `**config_standard` est réservé à `sympy.latex(...)` DANS le bloc Python.
    `pxsl_format_number()` n'accepte AUCUN kwarg. `pxsl_res_num(x, dec=…,
    egal=False)` s'appelle dans le bloc Python, résultat dans une variable Aff.
  • Espaces contre la triple-accolade : `x^{{ {{{{expAff}}}} }}` ✅,
    jamais `x^{{{{{{expAff}}}}}}` ❌.

RÈGLE DU `$` COLLÉ À UN CHIFFRE (casse silencieuse) :
  Un `$` immédiatement suivi d'un chiffre est lu comme un MONTANT en devise et
  désynchronise tout le `$…$`. Préfixer par un groupe vide : `${{}}3 \\times 2$`,
  et SURTOUT `${{}}{{{{nAff}}}}$` pour toute injection inline qui rend un nombre.
  Pour un vrai pourcentage affiché : `\\%` partout (jamais `%` nu dans le texte) ;
  ne JAMAIS échapper les `%` à l'intérieur du bloc Python (chaînes "%.2f").

TIRAGES — exclure les cas dégénérés (boucle de rejet ou énumération) :
  • `for _ in range(300): … ; break` ou liste de candidats + `rd.choice(...)`
    (contraintes croisées → TOUJOURS énumération en compréhension, jamais
    une boucle qui peut sortir invalide).
  • Exclure : exposant 0 ou 1 affiché (`^{{0}}`, `^{{1}}`), dénominateur 1
    (`\\frac{{…}}{{1}}`), `\\sqrt[1]`, `\\sqrt[2]` (→ `\\sqrt`), double signe
    (`+ -`), division par zéro, Δ de signe inattendu, intervalle vide.
  • Exactitude : `sympy.Rational(1, 2)`, JAMAIS `1/2` flottant ni `round()`
    pour une valeur exacte. Le module `fractions.Fraction` PLANTE les
    formateurs plateforme — ne jamais le passer à un helper pxsl_*.
  • Coefficients signés : ne JAMAIS concaténer un signe à une valeur ;
    utiliser `lc(coef, sign=True, ones=True)` (pxsl_latex_coefficient) dans
    le bloc Python → variable Aff.

DÉCIMALES SELON LA LANGUE : FR = virgule (`0{{,}}18`, `4,12`), milliers `\\,` ;
EN = point (`0.18`), milliers virgule. {lang_directive}

BILINGUE (si l'exercice l'est) : rôles INLINE uniquement :
  {{fr}}`Calculer …`{{en}}`Compute …`
  Jamais de bloc :::{{fr}}/:::{{en}}. Les injections `{{{{var}}}}` se placent
  HORS des rôles : {{fr}}`Il y a `{{en}}`There are `{{{{nAff}}}}.
  Symétrie totale FR/EN (même détail, mêmes placeholders). Si un nombre
  décimal s'affiche, prévoir des variables séparées par langue
  (`prixAffFr` virgule / `prixAffEn` point) et injecter la bonne dans chaque rôle.

FIDÉLITÉ À LA SOURCE (directive Chabane — INTOUCHABLE) :
  • Même énoncé, même méthode, même structure de solution, mêmes poids.
  • Ne JAMAIS AJOUTER de phrase d'énoncé, de transition ou de rappel de règle
    absent de la source (même « pour aider ») — on pythonise, on n'enrichit pas.
  • Conserver les commentaires utiles du bloc Python source s'il en a.
  • Si la source contient des `detailedSolution` validées : INTERDICTION de
    reformuler la prose — seules les valeurs littérales deviennent `{{{{var}}}}`.
  • Conserver tels quels : `\\ds`, `\\dfrac`, `\\inftys` (macro maison, ne
    JAMAIS la « corriger »), `\\begin{{equation*}}` avec `&=` direct,
    `\\phantom{{-}}\\\\`. Pas de `$$…$$`, pas de `\\[…\\]`, pas de `\\begin{{align}}`.
  • Géométrie pure : ne pas pythoniser (valeurs statiques conservées).

FIGURES matplotlib (si l'exo en a) : construites dans LE bloc Python unique,
variables du tirage réellement utilisées dans le tracé, labels DANS la fenêtre,
pas de mélange Rational+numpy (passer par float()), UN SEUL `plt.show()` final —
jamais `savefig`, jamais `matplotlib.use(...)`.

═══════════════════════════════════════════════════════════════════════════
 CATALOGUE PyxiScience (helpers à utiliser DANS le bloc Python)
═══════════════════════════════════════════════════════════════════════════
RÈGLE D'OR DU CATALOGUE : avant d'écrire le moindre LaTeX à la main, CHERCHE
ici un helper qui fait le travail et UTILISE-LE (résultat dans une variable
`…Aff` injectée nue). Coder à la main ce qu'un helper sait faire = REJET.
  • Matrices → `pxsl_matrix` (jamais `\\begin{{pmatrix}}` à la main) ; sommes/
    produits/scalaires détaillés → `pxsl_sum_matrix`/`pxsl_prod_matrix`/
    `pxsl_prod_scalar_matrix` ; système `Ax=B` → `pxsl_system_lin` ; résolution
    pas à pas / inversion → `pxsl_resol_system` / `pxs_steps_invert_matrix` ;
    échelon/RREF → `pxs_compute_ech`/`pxs_compute_ech_reduite`.
  • Proba (v.a. finie) → `pxs_finiterv`, tableau de loi `pxsl_law`, moment
    `pxsl_moment`, transformation `pxs_fct_finiterv`.
  • Intégration par parties → `pxs_explain_IBP` (rédaction complète, injectée
    via `{{{{ipp}}}}`).
  • Coefficients signés → `pxsl_latex_coefficient`/`lc` ; puissances →
    `pxsl_pow` ; résultat numérique → `pxsl_res_num` ; inéquation rédigée →
    `pxsl_solve_general_inequality`.
  • Voie par défaut pour une expression : `latex(expr, **config_standard)`.
    `**config_standard` est réservé à `latex()` — JAMAIS sur un helper `pxsl_*`.
  • N'appelle PAS un helper marqué « runtime à vérifier » (indi_l_r_symb,
    pxs_round, Poly_with_random_coef) sans certitude qu'il est chargé.

{functions}

═══════════════════════════════════════════════════════════════════════════
 EXEMPLE CANONIQUE DU MÊME TYPE (extrait d'un exercice livré et validé —
 imite sa structure, ses conventions d'affichage et son niveau de détail)
═══════════════════════════════════════════════════════════════════════════
{fewshot}

═══════════════════════════════════════════════════════════════════════════
 CONTEXTE
═══════════════════════════════════════════════════════════════════════════

EN-TÊTE déjà finalisé (NE PAS reproduire) :
{content}

VARIABLES DÉTECTÉES :
{analysis}

BLOCS PRÉCÉDENTS (ne pas redéfinir leurs variables, ne pas les répéter) :
{previous_blocks}

SECTION À PYTHONISER ({range_label} / {nb_total}) :
{current_segment}

═══════════════════════════════════════════════════════════════════════════
 RÈGLES D'ASSEMBLAGE PAR PAIRE
═══════════════════════════════════════════════════════════════════════════

⚠️ TU PRODUIS UNIQUEMENT LE CONTENU DE CETTE PAIRE — jamais celui des paires
précédentes (concaténées mécaniquement avant ta sortie).

⚠️ EXACTEMENT {nb_current} bloc(s) `:::::{{question}}` — pas plus, pas moins.
`questionId`/`questionIndex` CONTINUS depuis la paire précédente.

⚠️ PAIRE 1 UNIQUEMENT : tu produis le bloc ````{{python}}```` principal
(imports + tirages + calculs + variables Aff + `globals()`) puis l'énoncé
général réécrit avec injections, AVANT la première question.

⚠️ PAIRES SUIVANTES : ni énoncé, ni questions précédentes, ni ré-imports.
Si de NOUVELLES variables sont nécessaires (ex. figure d'une partie C), un
PETIT bloc ````{{python}}```` additionnel SANS imports, terminé par `globals()`.

Format paire 1 :

````{{python}}
<imports + tirages (cas dégénérés exclus) + calculs sympy exacts
 + TOUTES les variables d'affichage …Aff ; AUCUN texte pédagogique>
globals()
````

<énoncé général avec valeurs → {{{{varAff}}}}>

:::::{{question}}
:questionType: STQ
:questionId: N
:questionIndex: N

::::{{questionStatement}} … ::::
::::{{questionHint}} … ::::
::::{{detailedSolution}} … ::::
::::{{weightDistribution}}
:logic: …
:abstraction: …
:reasoning: …
:calculation: …
::::
:::::

═══════════════════════════════════════════════════════════════════════════
 RÈGLES CIBLÉES POUR CET EXERCICE (depuis la base de règles)
═══════════════════════════════════════════════════════════════════════════
{targeted_rules}

INVARIANTS MATHÉMATIQUES à préserver lors des tirages :
{property_constraints}

═══════════════════════════════════════════════════════════════════════════
 CHECKLIST FINALE (vérifie chaque point avant de répondre)
═══════════════════════════════════════════════════════════════════════════
  □ Bloc ````{{python}}```` (4 backticks) terminé par `globals()`
  □ CHAQUE `{{{{ }}}}` = nom de variable NU camelCase sans underscore
  □ Aucun appel/calcul/`**kwargs` dans `{{{{ }}}}` — tout pré-calculé en `…Aff`
  □ Aucun `$` collé à un chiffre — `${{}}` devant toute injection inline numérique
  □ Tirages sans cas dégénéré (^{{1}}, ^{{0}}, frac{{}}{{1}}, sqrt[2], double signe)
  □ Coefficients signés via lc(...) pré-calculé ; décimales localisées
  □ weightDistribution = poids source verbatim (somme 100) ; IDs contigus
  □ Solutions validées : prose INTACTE, valeurs → {{{{var}}}}
  □ {{fr}}`…`{{en}}`…` symétriques si bilingue ; `\\%` pour les pourcentages
"""


# ─────────────────────────────────────────────────────────────────────────────
# AUDIT — vérification ciblée + patches textuels
# v1 → app/knowledge/prompts_v1_archive.md §STEP_AUDIT_PROMPT
# (v2 : ajout des contrôles injections nues / $+chiffre / fences 4 backticks ;
#  les patches sont désormais appliqués à TOUTES les occurrences identiques)
# ─────────────────────────────────────────────────────────────────────────────
STEP_AUDIT_PROMPT = """\
Tu es l'auditeur PyxiScience. Tu reçois l'exercice pythonisé final et tu vérifies
UNIQUEMENT les règles listées ci-dessous (chacune avec son cas FAUTIF/CORRECT),
plus les 4 invariants plateforme :
  (a) toute injection `{{{{ }}}}` est un nom de variable NU camelCase sans underscore ;
  (b) aucun `$` non échappé collé à un chiffre (préfixe `${{}}` requis) ;
  (c) bloc {{python}} à 4 backticks terminé par `globals()` ;
  (d) questionId/questionIndex contigus depuis 0, weightDistribution somme 100.

RÈGLES À VÉRIFIER :

{audit_rules}

EXERCICE À AUDITER :
{exercise}

═══════════════════════════════════════════════════════════════════════════
 MISSION
═══════════════════════════════════════════════════════════════════════════

Pour chaque règle violée, renvoie une "issue" :
  • rule           : ID de la règle (ex: "6.1") ou "(a)"…"(d)"
  • location       : snippet EXACT (1 ligne, ≤ 200 caractères), copié VERBATIM —
                     utilisé tel quel par str.replace() côté Python.
                     Si la même violation apparaît à N endroits IDENTIQUES,
                     une seule issue suffit (toutes les occurrences seront
                     remplacées).
  • fix            : remplacement EXACT.
  • python_insert  : (OPTIONNEL) ligne(s) Python à insérer avant le `globals()`
                     du bloc principal (ex: "eqAff = latex(eq, **config_standard)").
  • can_patch      : true si la correction est sûre, false sinon (warning seul).
  • message        : phrase explicative en français.

Ne liste PAS les règles respectées ni celles hors liste. Ne « corrige » JAMAIS
`\\inftys`, `\\ds`, `\\dfrac`, ni la prose d'une solution validée.
Un exercice MONOLINGUE (tout FR ou tout EN, sans rôles {{fr}}`…`{{en}}`…`) est
LÉGITIME — ne le signale pas ; n'exige le bilingue que s'il est déjà partiel.
Les espaces internes `{{{{ var }}}}` sont tolérés (le moteur trim) — ne les
signale pas.

Réponds UNIQUEMENT en JSON valide, sans markdown :
{{
  "verdict": "OK" ou "PATCH_REQUIRED",
  "issues": [
    {{
      "rule": "6.1",
      "location": "{{{{latex(fDev, **config_standard)}}}}",
      "fix": "{{{{fDevTex}}}}",
      "python_insert": "fDevTex = latex(fDev, **config_standard)",
      "can_patch": true,
      "message": "Appel avec **kwargs dans {{{{…}}}} — variable pré-calculée."
    }}
  ]
}}
"""


# ─────────────────────────────────────────────────────────────────────────────
# Traduction de contraintes FR → assertions Python (règle 4.3)
# (inchangé v1 — déplacé depuis routes/pythonise_routes_v2.py)
# ─────────────────────────────────────────────────────────────────────────────
TRANSLATE_CONSTRAINTS_PROMPT = """\
Tu reçois un bloc de code Python qui tire des variables aléatoires et calcule
des grandeurs dérivées, et une liste de contraintes mathématiques en français
à vérifier sur les variables produites.

CODE PYTHON :
```python
{code}
```

CONTRAINTES (français) :
{constraints}

MISSION :
Pour chaque contrainte, écris une expression Python booléenne qui, évaluée
dans le namespace résultant de l'exécution du code, retourne True si la
contrainte est respectée.

Règles :
  • Contrainte universelle ("pour tout n") → échantillonner n = 0..10 max et
    combiner avec `all(...)` (5 à 10 valeurs, pas plus).
  • Notations math (≤, ≥, ≠) → `<=`, `>=`, `!=`.
  • Contrainte intestable (variable absente du code) → `"assertion": null`.
  • AUCUN import supplémentaire — seulement les variables du namespace + builtins.

Réponds UNIQUEMENT en JSON valide :
[
  {{"description": "<contrainte originale>", "assertion": "<expression Python>" }},
  {{"description": "<autre contrainte>",     "assertion": null }}
]
"""


# ─────────────────────────────────────────────────────────────────────────────
# Substitution des solutions validées (règle 8.1)
# (inchangé v1 — déplacé depuis routes/pythonise_routes_v2.py)
# ─────────────────────────────────────────────────────────────────────────────
SOLUTION_SUBSTITUTION_PROMPT = """\
Tu reçois UNE solution mathématique rédigée avec des VALEURS LITTÉRALES (nombres,
fractions, expressions concrètes), et une liste de VARIABLES PYTHON disponibles
dans le bloc `{{python}}` de l'exercice pythonisé.

SOLUTION ORIGINALE (source MyST, à préserver mot à mot) :
─────────────────────────────────
{original_solution}
─────────────────────────────────

VARIABLES PYTHON DISPONIBLES (chaque var a une valeur d'exemple ; substitue
chaque occurrence numérique par le placeholder MyST {{{{var}}}}) :
{variables_table}

═══════════════════════════════════════════════════════════════════════════
 MISSION
═══════════════════════════════════════════════════════════════════════════

Remplace CHAQUE valeur littérale (nombre entier, fraction, expression numérique)
qui correspond à une variable Python par son placeholder MyST `{{{{nomVar}}}}`.

⚠️ STRICTES INTERDICTIONS :
  • NE PAS ajouter de mots (Initialisation, Hérédité, Conclusion, Soit, Donc, etc.)
  • NE PAS ajouter de **gras** ou *italique* si pas dans la source
  • NE PAS reformuler la moindre phrase ; NE PAS modifier la ponctuation
  • NE PAS ajouter de paragraphes ou de blocs equation*
  • Si la source utilise déjà des `{{{{var}}}}`, les PRÉSERVER tels quels.

EXEMPLE :
  Source     : `On a $f(0) = 3$ et $f(2) = -1$.`
  Variables  : x0=0, x2=2, fx0=3, fx2=-1
  Sortie     : `On a $f({{{{x0}}}}) = {{{{fx0}}}}$ et $f({{{{x2}}}}) = {{{{fx2}}}}$.`

Réponds UNIQUEMENT avec le texte modifié, SANS préambule, SANS wrapper markdown,
SANS guillemets ajoutés. Si tu ne peux pas substituer, recopie la source telle quelle.
"""


# ─────────────────────────────────────────────────────────────────────────────
# Traduction / bilinguisation (NOUVEAU — chantier langue cible)
# ─────────────────────────────────────────────────────────────────────────────
TRANSLATE_PROMPT = """\
Tu traduis la PROSE d'un exercice PyxiScience MyST, de {source_label} vers {target_label}.

TEXTE (les blocs Python ont été remplacés par des sentinelles <<<PYBLOCK_n>>> — à RECOPIER TELLES QUELLES) :
─────────────────────────────────
{body}
─────────────────────────────────

RÈGLES ABSOLUES :
  • Traduire UNIQUEMENT la prose (énoncés, indications, solutions, titres).
  • PRÉSERVER À L'IDENTIQUE : toutes les sentinelles <<<PYBLOCK_n>>>, tous les
    placeholders `{{{{var}}}}` (mêmes noms, mêmes positions logiques), tout le
    LaTeX/maths ($…$, \\begin{{equation*}}…), la structure des fences MyST
    (`````, :::::, ::::), toutes les options `:clé: valeur` (dont
    :questionId:, :weightDistribution: et leurs valeurs), `\\ds`, `\\dfrac`,
    `\\inftys`, `\\%`.
  • {format_directive}
  • Décimales : virgule en FR (`0{{,}}5`), point en EN (`0.5`) — adapte les
    décimales LITTÉRALES de la prose à la langue de chaque segment ; ne touche
    pas aux `{{{{var}}}}`.
  • Terminologie mathématique scolaire exacte ; même niveau de détail.

Réponds UNIQUEMENT avec le texte transformé, sans préambule ni wrapper.
"""

TRANSLATE_FORMAT_MONO = (
    "Sortie MONOLINGUE en {target_label} : remplace chaque texte source par sa "
    "traduction, sans rôles {{fr}}/{{en}}."
)
TRANSLATE_FORMAT_BOTH = (
    "Sortie BILINGUE : chaque segment de prose devient une paire de rôles inline "
    "{fr}`texte français`{en}`english text` (JAMAIS de bloc :::{fr}/:::{en}). "
    "Les injections {{var}} et le LaTeX restent HORS des rôles, partagés par les "
    "deux langues : {fr}`Il y a `{en}`There are `{{nAff}}."
)


# ─────────────────────────────────────────────────────────────────────────────
# DÉCLINAISONS QCM / QAT (NOUVEAU 2026-07 — mode `declinaisons`)
# Spécification normative fournie par l'équipe (PROMPT_declinaisons_QCM_QAT §4-§6),
# calibrée sur les 33 exemples validés de knowledge/fewshots/declinaisons/.
# Divergences wx ↔ conventions strictes (corpus 222) tranchées : format
# plateforme des wx (mcqAnswer/:solution:/{input}) + conventions strictes de
# l'app (fences 4, globals(), injections nues camelCase Aff, IDs contigus).
# v1 → v2 (2026-07-02) : MCQ_SPEC + section « DISTRACTEURS EN MIROIR » (règle
# enseignante : grille symétrique, bonne réponse jamais devinable par la forme).
# v2 → v3 (2026-07-06) : intégration du prompt système QCM affiné —
# distracteurs cohérents (erreur réelle, near-miss même famille, flip jamais sur
# entrée nulle, swap sûr en symbolique), formulation directe, matrices d'option
# en \small (anti-scrollbar), éclatement avec solution partitionnée. Écart
# assumé vs le prompt fourni : questionHint reste REMPLI (35/35 dans les 33
# exemples validés qui font foi), pas vide.
# ─────────────────────────────────────────────────────────────────────────────

MCQ_SPEC = """\
FORMAT QCM (questionType MCQ) — NORMATIF :

:::::{question}
:questionType: MCQ
:questionId: N
:questionIndex: N

::::{questionStatement}
<énoncé auto-suffisant ; maths et {{ }} HORS des rôles bilingues>
::::

::::{questionHint}
<indice de DÉMARRAGE qui ne révèle pas la réponse ; VERBATIM si repris de la source>
::::

::::{mcqAnswer}
:isRightAnswer: true
<BONNE réponse — TOUJOURS en slot 1>
::::

::::{mcqAnswer}
:isRightAnswer: false
<distracteur 1 — erreur type>
::::

::::{mcqAnswer}
:isRightAnswer: false
<distracteur 2 — erreur type>
::::

::::{mcqAnswer}
:isRightAnswer: false
<distracteur 3 — erreur type>
::::

::::{mcqAnswer}
:isRightAnswer: false
{fr}`Aucune de ces réponses n'est correcte`{en}`None of these answers are correct`
::::

::::{detailedSolution}
<solution détaillée ; VERBATIM de la source si elle existe, sinon rédigée>
::::

::::{weightDistribution}
:logic: 25
:abstraction: 25
:reasoning: 25
:calculation: 25
::::
:::::

RÈGLES MCQ DURES :
  • EXACTEMENT UNE option `:isRightAnswer: true`, EN SLOT 1 (l'affichage est
    mélangé côté plateforme — ne PAS randomiser l'ordre dans le fichier).
  • 5 options par défaut (1 correcte + 3 distracteurs + « None » EN DERNIER).
    Ensembles fermés (vrai/faux, intervalles exhaustifs) : « None » omis
    autorisé (⇒ 4 options ; jamais moins de 3).
  • PAS de `:solution:`, PAS de `{input}`, PAS de displayedSolution en MCQ.
  • Ordre des blocs : questionStatement → questionHint → mcqAnswer×N →
    detailedSolution → weightDistribution.
  • L'option « None » et toute option textuelle sont bilingues si la cible l'est.

DISTRACTEURS — ERREURS TYPES UNIQUEMENT (aucune valeur au hasard) :
  • Algèbre : erreur de signe ; coefficient inversé ; terme oublié ; distribution partielle.
  • Dérivées : oubli du facteur de la règle de chaîne ; exposant non décrémenté ;
    primitive au lieu de dérivée ; quotient sans v² ; produit sans la 2e moitié.
  • Intégrales : oubli du +1 sur l'exposant ; oubli du 1/a ; dérivée au lieu de
    primitive ; oubli de |x| dans ln.
  • Matrices : transposée ; colonnes/lignes échangées ; entrée non dérivée ;
    matrice opposée ; oubli du terme +b.
  • Compositions affines : oubli de b_f ; ordre inversé (g∘f vs f∘g) ; signe opposé.
  • Limites : mauvaise forme indéterminée ; mauvais signe d'infini.

DISTRACTEURS COHÉRENTS & INDEVINABLES (règle enseignante, 2026-07-02) —
un distracteur = une ERREUR RÉELLE que l'élève peut commettre, jamais une
variante trivialement éliminable :

  INTERDITS (trop faciles à deviner) :
  • Garder une partie IDENTIQUE dans toutes les options alors qu'un seul bloc
    change (ex. matrice A identique partout, seul b varie) → l'élève ignore A
    et devine sur b. Fais VARIER la partie qui teste vraiment (ici A).
  • ÉTIQUETER la classification qui trahit la réponse (« f is linear, b=0 »
    quand des constantes sont visibles → écarté sans réfléchir). Ne nomme PAS
    linear/affine dans les options : demande directement « quels A et b ? » et
    montre les paires.
  • Distracteurs ARTIFICIELS (−A tout entier, 2b…) sans erreur pédagogique
    derrière.
  • Variations « une seule chose à la fois » autour de la bonne réponse
    (2x+3 / 2x−3 / 2x−4 / −2x+3) → le motif commun « 2x+3 » se devine.

  À PRIVILÉGIER (erreurs pédagogiques réelles, en grille refermée) :
  • Signe mal lu sur UNE entrée précise de A ou de b (ex. −4x lu +4x).
  • Transposée de A (colonnes ↔ lignes) — erreur de lecture classique.
  • Constante oubliée (b = 0, NON étiquetée « linear »).
  • Oubli/inversion d'un terme (+b oublié, b soustrait au lieu d'ajouté).
  • Encadrement/bornes : décalage ±1 (off-by-one).
  • Combinaisons SYMÉTRIQUES qui referment la grille (signe × signe,
    ordre × signe) plutôt que des erreurs indépendantes autour d'un gabarit :
      ✓ 2x+3 / 2x−3 / −2x+3 / −2x−3 (grille de signes : l'intuition ne trie
        plus, il faut CALCULER).
  • La bonne réponse n'est JAMAIS structurellement unique : ni la seule avec
    radical/fraction/facteur, ni la plus longue/courte, ni la seule simplifiée
    — TOUTES au même niveau de simplification (jamais de fraction réductible).
  • Test avant de rendre : masque mentalement la bonne réponse — si sa place
    se retrouve par la seule FORME (motif majoritaire, symétrie incomplète,
    singularité, bloc figé), reconstruis les distracteurs.

  DISTINCTION GARANTIE SUR TOUTES LES DÉCLINAISONS :
  • Construis chaque distracteur par une modification à DELTA NON NUL GARANTI,
    chacun sur une ENTRÉE/POSITION DIFFÉRENTE. Techniques sûres :
      – Flip de signe d'une entrée : SEULEMENT sur une entrée GARANTIE ≠ 0
        (flipper un 0 redonne l'original → collision). Tire ces entrées dans un
        domaine excluant 0, ou choisis une position structurellement non nulle.
      – Interversion de colonnes/variables (∂x↔∂y) : SÛRE sur entrées
        SYMBOLIQUES (une colonne dépend de x, l'autre de y → jamais égales) ;
        DANGEREUSE sur entrées entières (deux colonnes peuvent coïncider) → dans
        ce cas, préférer 3 flips de signe sur des entrées distinctes non nulles.
      – Décalage ±1 (bornes entières) ; multiple/omission (b oublié, −b, 2b).
  • Vérifie en Python : sur ≥300 tirages, `assert` que les options sont deux à
    deux distinctes (chaînes rendues). Aucune collision tolérée.

ANTI-COLLISION (le piège n°1 des QCM randomisés — un distracteur peut devenir
ÉGAL à la bonne réponse sur certaines graines) — dans CET ordre :
  1. DISTINCT PAR CONSTRUCTION (préféré) : distracteurs de type différent,
     tirages qui garantissent la non-nullité/non-égalité (coefficients >= 2,
     exposants >= 2, entrées non nulles…). Documente-le en commentaire Python.
  2. TIRAGE AVEC REJET dans le bloc Python : reboucler tant que les chaînes
     RENDUES (latex) de toutes les options ne sont pas toutes distinctes.
  3. Le harnais vérifie l'unicité sur 100 graines — un doublon = REJET.
  ⚠️ La collision est aussi SÉMANTIQUE : deux options formulées différemment
  mais mathématiquement ÉQUIVALENTES (« divise x par 2 » ≡ « multiplie x par
  1/2 » ; « T_{1/a,1/b} » ≡ « division par a et b ») comptent comme un doublon
  pour l'élève. Vérifie l'équivalence MATHÉMATIQUE de chaque paire d'options
  sur TOUT l'espace des tirages (ex. b == 1/a possible ? → l'exclure au tirage).

UN SEUL bloc {python} au total : JAMAIS de re-tirage (`rd.`/`random`) hors du
bloc principal — un second tirage rendrait les valeurs incohérentes entre les
questions. Les variables des paires suivantes s'ajoutent SANS aléa nouveau.

FORMATAGE : STRICTEMENT IDENTIQUE entre bonne réponse et distracteurs (même
style LaTeX, mêmes helpers, même nombre de décimales, même notation
matricielle, MÊME LONGUEUR) — sinon la bonne réponse se devine.
  • JAMAIS d'exemple/parenthèse explicative sur la SEULE bonne réponse
    (« … (e.g. A<B donne x) ») : soit tout le monde a l'ajout, soit personne.
  • JAMAIS d'annotation d'erreur visible dans une option (« (signe oublié) »,
    « (forgot +b) ») — ça vit UNIQUEMENT dans la solution détaillée.

FORMULATION DIRECTE (QCM) : on demande le RÉSULTAT à cocher. Retire les consignes
de méthode/rédaction qui n'ont de sens qu'en réponse libre — « calcule de deux
façons », « vos deux réponses doivent coïncider », « montre que… », « trace /
esquisse… », « justifie… ». Ex. : « Compute (f∘g)(x) in two ways… should
agree! » → « Compute (f∘g)(x). »

RENDU DES MATRICES DANS LES OPTIONS (anti-scrollbar) : une `bmatrix` pleine dans
une case d'option fait apparaître un ascenseur. Si une OPTION contient une
matrice, réduis-la : `{\\small \\begin{bmatrix}…\\end{bmatrix}}` (échelle si
besoin : smallmatrix < \\scriptsize < \\footnotesize < \\small ; défaut \\small).
Garde les `bmatrix` PLEINES dans la detailedSolution (fidélité + place).

ÉCLATEMENT (autorisé) : si UNE question porte sur N cas indépendants (par
ellipse, par sous-fonction…), tu peux l'éclater en N questions — le contexte
commun monte dans l'énoncé global, et la detailedSolution source est PARTITIONNÉE
par cas (**(i)**, **(ii)**…) puis rattachée à chaque question. Contrainte dure :
la CONCATÉNATION des morceaux doit être IDENTIQUE à la solution source. Par
défaut (pas de cas multiples), garde le MÊME nombre de questions que la source.

questionHint : indice de DÉMARRAGE qui ne révèle jamais la réponse (cf. exemples
validés — tous en fournissent un) ; VERBATIM si la source en a un ; vide
seulement si aucun indice pertinent.

L'ÉNONCÉ NE DONNE JAMAIS LA RÉPONSE (l'énoncé définit, la question interroge).
"""  # noqa: E501 — texte normatif verbatim (valeur injectée telle quelle, accolades SIMPLES)

FGQ_SPEC = """\
FORMAT QAT (questionType FGQ — question à champ(s) libre(s) ordonné(s)) — NORMATIF :

:::::{question}
:questionType: FGQ
:questionId: N
:questionIndex: N
:solution: [["ord","${{v1Aff}}$","${{v2Aff}}$"],["0","0"]]

::::{questionStatement}
<énoncé auto-suffisant>

<LIGNE VIDE obligatoire avant le premier {input}>
$x_1 =$ {input}`||110` $\\qquad x_2 =$ {input}`||110`
::::

::::{questionHint}
<indice — vide ou verbatim source>
::::

::::{displayedSolution}
$x_1 = {{v1Aff}}$, $\\quad x_2 = {{v2Aff}}$
::::

::::{detailedSolution}
<solution détaillée>
::::

::::{weightDistribution}
:logic: 15
:abstraction: 20
:reasoning: 20
:calculation: 45
::::
:::::

RÈGLES FGQ DURES :
  • `:solution:` DIRECTEMENT dans le champ (jamais construite dans une variable
    Python), juste après `:questionIndex:`. Format [["ord","<v1>",…],["0",…]].
  • ARITÉ STRICTE : nb de {input} == nb de valeurs dans "ord" == nb de
    tolérances. Tolérance TOUJOURS "0" (exacte).
  • Un `{{varAff}}` par valeur dynamique dans `:solution:` (variable NUE).
  • ORDRE : les valeurs de "ord" suivent l'ordre d'apparition des {input}
    dans l'énoncé. Plusieurs solutions (racines…) → ÉNONCER l'ordre (« de la
    plus petite à la plus grande ») et le respecter dans "ord" ET dans
    displayedSolution.
  • Chaque {input} est INTRODUIT PAR UN LABEL ($x =$ {input}`||110`),
    jamais nu, jamais collé à la prose ; LIGNE VIDE avant le premier {input}.
  • Ordre des blocs : questionStatement → questionHint → displayedSolution →
    detailedSolution → weightDistribution.
  • Valeurs EXACTES (fractions, \\ln, \\sqrt, +\\infty…) — JAMAIS de décimales
    approchées dans `:solution:`.
  • REPLI MCQ : si une question n'est PAS auto-corrigeable en champ libre
    (réponse avec fonction abstraite, vrai/faux, matrice à dimension VARIABLE),
    produis cette question en MCQ (format ci-contre) — une sortie QAT peut être
    mixte FGQ + MCQ. Ne force JAMAIS un champ libre ingérable.

MATRICES EN QAT (PIÈGE plateforme) :
  • `pxsl_matrix` est INTERDIT dans un champ `:solution:` (le rendu
    \\left[\\begin{array}… ne matche pas le widget). Si champ unique matrice :
    variable calculée avec latex(M, mat_delim='', mat_str='pmatrix') (FR)
    ou mat_str='bmatrix' (EN), injectée nue.
  • Dimension variable ⇒ repli MCQ pour cette question.

L'ÉNONCÉ NE DONNE JAMAIS LA RÉPONSE (l'énoncé définit, la question interroge).
"""  # noqa: E501 — texte normatif verbatim (valeur injectée telle quelle, accolades SIMPLES)

# Prompt de génération d'une déclinaison (QCM ou QAT) — même mécanique par
# paires que la pythonisation ; le champ {decl_spec} reçoit MCQ_SPEC ou FGQ_SPEC.
STEP_DECLINAISON_PROMPT = """\
Tu déclines un exercice PyxiScience MyST en version {decl_label}, niveau {niveau}.
L'exercice source (statique OU déjà pythonisé) est fourni ; tu produis la
déclinaison RANDOMISÉE (bloc Python terminé par `globals()` + injections),
au format plateforme EXACT ci-dessous.

═══════════════════════════════════════════════════════════════════════════
 CONVENTIONS PLATEFORME (identiques à la pythonisation — NON NÉGOCIABLES)
═══════════════════════════════════════════════════════════════════════════
  • Bloc Python : 4 backticks ````{{python}} … ```` terminé par `globals()`.
  • Injections `{{{{ }}}}` : UNIQUEMENT des noms de variables NUS camelCase
    suffixe `Aff` — JAMAIS d'appel de fonction, de calcul, d'underscore, ni
    d'accès dict. Tout se pré-calcule dans le bloc Python.
  • `{{{{ }}}}` et les maths TOUJOURS HORS des rôles {{fr}}`…`{{en}}`…` (un
    placeholder dans un rôle ne s'évalue PAS — texte cassé).
  • Règle du `$` collé à un chiffre : préfixe `${{}}`. Décimales localisées
    (virgule FR / point EN). `latex(expr, **config_standard)`.
  • `:questionId:`/`:questionIndex:` contigus dès 0.
  • Interdits : \\py{{}}, \\qcm, \\qat, \\qcl, \\right/\\wrong (légacy),
    \\begin{{align*}}, \\displaystyle, \\[ \\], $$.

FIDÉLITÉ À LA SOURCE :
  • 1 question source → 1 question déclinée. NE JAMAIS inventer de
    sous-questions ni enrichir l'énoncé.
  • L'énoncé ne doit JAMAIS donner la réponse (l'énoncé définit, la question
    interroge).
  • detailedSolution : VERBATIM de la source si elle existe (seules les valeurs
    littérales deviennent des {{{{varAff}}}}), sinon rédigée sobrement.
  • Source DÉJÀ PYTHONISÉE : recopie son bloc Python À L'IDENTIQUE (octet pour
    octet), puis ajoute `# === Ajouts déclinaison {decl_label} ===` suivi des
    NOUVELLES variables (distracteurs/solutions), AVANT le `globals()` final.
  • weightDistribution : repris de la question source si présent, sinon le
    barème par défaut du format ci-dessous (somme = 100 TOUJOURS).

═══════════════════════════════════════════════════════════════════════════
 SPÉCIFICATION DU FORMAT {decl_label}
═══════════════════════════════════════════════════════════════════════════
{decl_spec}

═══════════════════════════════════════════════════════════════════════════
 EXEMPLE CANONIQUE COMPLET (structure et conventions à imiter)
═══════════════════════════════════════════════════════════════════════════
{fewshot}

═══════════════════════════════════════════════════════════════════════════
 CATALOGUE PyxiScience (helpers à utiliser DANS le bloc Python)
═══════════════════════════════════════════════════════════════════════════
{functions}

═══════════════════════════════════════════════════════════════════════════
 CONTEXTE
═══════════════════════════════════════════════════════════════════════════

EN-TÊTE déjà finalisé (NE PAS reproduire) :
{content}

VARIABLES DÉTECTÉES :
{analysis}

BLOCS PRÉCÉDENTS (ne pas redéfinir leurs variables, ne pas les répéter) :
{previous_blocks}

SECTION À DÉCLINER ({range_label} / {nb_total}) :
{current_segment}

{lang_directive}

═══════════════════════════════════════════════════════════════════════════
 RÈGLES D'ASSEMBLAGE PAR PAIRE
═══════════════════════════════════════════════════════════════════════════
⚠️ TU PRODUIS UNIQUEMENT LE CONTENU DE CETTE PAIRE (les paires précédentes
sont concaténées mécaniquement avant ta sortie).
⚠️ EXACTEMENT {nb_current} bloc(s) `:::::{{question}}` — questionId/questionIndex
CONTINUS depuis la paire précédente.
⚠️ PAIRE 1 UNIQUEMENT : le bloc ````{{python}}```` (source recopiée si déjà
pythonisée + ajouts déclinaison + `globals()`) puis l'énoncé général VERBATIM,
AVANT la première question.
⚠️ PAIRES SUIVANTES : ni énoncé, ni ré-imports ; petit bloc ````{{python}}````
additionnel possible pour les nouvelles variables seulement.

═══════════════════════════════════════════════════════════════════════════
 CHECKLIST FINALE
═══════════════════════════════════════════════════════════════════════════
  □ Bloc ````{{python}}```` (4 backticks) terminé par `globals()`
  □ CHAQUE `{{{{ }}}}` = variable NUE camelCase (Aff) — aucun appel/underscore
  □ Aucun `{{{{ }}}}` NI maths à l'intérieur d'un rôle {{fr}}`…`/{{en}}`…`
  □ MCQ : 1 seule bonne réponse (slot 1), « None » en dernier, options toutes
    distinctes SUR TOUTES LES GRAINES, formatage identique
  □ FGQ : arité #input == #valeurs == #tolérances ("0"), :solution: littérale,
    ordre énoncé/"ord"/displayedSolution cohérents, labels devant chaque {{input}}
  □ 1 question source → 1 question ; solutions source VERBATIM ; poids repris
  □ IDs contigus dès 0 ; aucun motif interdit ; `\\%` pour les pourcentages
"""


# ─────────────────────────────────────────────────────────────────────────────
# Réparation post-harnais (NOUVEAU — 1 itération max)
# ─────────────────────────────────────────────────────────────────────────────
REPAIR_PROMPT = """\
Le harnais de validation PyxiScience a REJETÉ l'exercice pythonisé ci-dessous.
Corrige-le en changeant LE MINIMUM (ne réécris pas l'exercice, ne reformule
aucune prose, ne change pas la structure ni les poids).

ÉCHECS DU HARNAIS :
{failures}

EXERCICE ACTUEL :
{exercise}

RÈGLES DE CORRECTION :
  • Exception à l'exécution → corrige le bloc Python (tirage dégénéré, import
    manquant, division par zéro…) par la modification la plus locale possible.
  • Variable non résolue `{{{{x}}}}` → définis-la dans le bloc Python (avant
    `globals()`) ou corrige le nom injecté.
  • Motif interdit `$`+chiffre → préfixe `${{}}`.
  • **Double signe `+ -`** (cas le plus fréquent) : un `+` littéral du texte
    est suivi d'une injection qui rend une valeur NÉGATIVE (ex.
    `… + {{{{dfAff}}}}` avec dfAff = "- 4 \\sin(4x)"). Correctif : supprimer le
    `+` littéral ET pré-calculer la chaîne SIGNÉE dans le bloc Python
    (`dfSignAff = latex(df, **config_standard)` rend déjà le signe ; ou
    construire `"+ …"`/`"- …"` selon le signe) puis injecter
    `… {{{{dfSignAff}}}}` sans opérateur devant.
  • **`\\frac{{…}}{{1}}` / `^{{1}}` / `^{{0}}` / `\\sqrt[2]`** : presque toujours un
    TIRAGE DÉGÉNÉRÉ — exclure la valeur fautive à la source
    (ex. `b = rd.randint(2, 5)` au lieu de `randint(1, 5)`, ou boucle de rejet
    `if b == 1: continue`). Ne PAS rafistoler le texte : corriger le tirage.
    **EXCEPTION — texte pédagogique FIXE** qui enseigne précisément la règle de
    l'exposant (`$b^{{0}} = 1$`, `$b^{{1}} = b$`) : réécrire SANS accolades
    (`$b^0 = 1$`, `$b^1 = b$`) — rendu LaTeX identique pour un exposant à un
    seul caractère, et conforme au corpus validé.
  • Injection non nue → pré-calculer en variable camelCase `…Aff`.
  • Le bloc {{python}} reste à 4 backticks et se termine par `globals()`.
  • Ne touche NI à `\\inftys`/`\\ds`/`\\dfrac`, NI à la prose des solutions.
  • **QCM — collision d'options** (deux options rendues identiques sur une
    graine) : contraindre le TIRAGE (rejet `while` sur les chaînes rendues) ou
    changer la CONSTRUCTION du distracteur — jamais rafistoler le texte.
  • **QCM — plusieurs/zéro `:isRightAnswer: true`** : exactement une, en slot 1.
  • **FGQ — arité** : le nb de {{{{input}}}} doit égaler le nb de valeurs de
    `"ord"` et le nb de tolérances ("0") dans `:solution:`.
  • **`{{{{ }}}}` dans un rôle {{fr}}`…`/{{en}}`…`** : sortir l'injection du
    rôle (elle ne s'évalue pas dedans) — découper le rôle autour.

Réponds UNIQUEMENT avec l'exercice complet corrigé (de `````{{exercise}} à `````),
sans préambule ni wrapper markdown.
"""


# ─────────────────────────────────────────────────────────────────────────────
# AUDIT PÉDAGOGIQUE (2026-07-06) — juge la QUALITÉ (au-delà du harnais mécanique).
# Le harnais prouve la conformité structurelle ; ce juge évalue la finesse
# pédagogique et le RESPECT DES CONSIGNES (distracteurs cohérents, indevinabilité,
# énoncé qui ne donne pas la réponse…). Peut déclencher une réparation ciblée et,
# en mode auto, une escalade de modèle.
# ─────────────────────────────────────────────────────────────────────────────

PEDAGOGICAL_AUDIT_PROMPT = """\
Tu es un RELECTEUR PÉDAGOGIQUE senior de PyxiScience. On te donne une déclinaison
{decl_label} DÉJÀ VALIDE au harnais (structure/exécution correctes). Juge
UNIQUEMENT sa QUALITÉ PÉDAGOGIQUE et le respect des consignes — jamais la syntaxe.

CRITÈRES QCM (les plus importants) :
  1. Distracteurs = ERREURS RÉELLES plausibles d'un élève (signe mal lu sur une
     entrée, transposée, terme oublié, off-by-one…), JAMAIS des valeurs
     artificielles ou au hasard, JAMAIS des variantes « une seule chose à la
     fois » autour de la bonne réponse.
  2. INDEVINABILITÉ — la bonne réponse ne doit PAS se repérer par la FORME :
     • pas un bloc identique figé pendant qu'un seul varie (ex. matrice A figée,
       seul b change) ; • pas d'étiquette qui trahit (« linear », « b=0 ») ;
     • pas la seule simplifiée / avec radical / la plus longue ou courte ;
     • pas de parenthèse ou exemple explicatif sur la SEULE bonne réponse ;
     • distracteurs en grille symétrique (signe×signe, ordre×signe).
  3. L'ÉNONCÉ ne donne JAMAIS la réponse ; formulation DIRECTE (retirer « montre
     que », « calcule de deux façons », « trace », « justifie »).
  4. questionHint = amorce de méthode qui NE révèle PAS la réponse.
  5. Format IDENTIQUE entre toutes les options (longueur, style LaTeX, notation).
  6. Fidélité à la source : mêmes notions testées, solution cohérente.

CRITÈRES QAT/FGQ : champs {{input}} pertinents et bien placés ; displayedSolution
lisible ; énoncé qui ne donne pas la réponse ; consignes de saisie claires.

EXERCICE À JUGER :
{exercise}

Réponds UNIQUEMENT en JSON (aucune prose autour, aucun bloc markdown) :
{{"verdict": "OK ou A_REVOIR", "score": 0-100, "issues": [{{"gravite": "haute|moyenne|basse", "ou": "question/option concernée", "probleme": "ce qui cloche", "correction": "quoi faire concrètement"}}]}}
Règles de verdict : « OK » seulement si AUCUNE issue de gravité haute. Sois
EXIGEANT mais JUSTE — signale un vrai défaut d'apprentissage, pas une préférence
de style. Si l'exercice est bon, renvoie verdict « OK » et issues [].
"""  # noqa: E501

PEDAGOGICAL_REPAIR_PROMPT = """\
Un relecteur pédagogique a listé des défauts de QUALITÉ sur cette déclinaison
{decl_label}. La STRUCTURE est déjà correcte (harnais VERT) — NE LA CASSE PAS.
Corrige UNIQUEMENT les défauts listés, avec le minimum de changements.

DÉFAUTS À CORRIGER :
{issues}

CONTRAINTES DURES (ne rien casser) :
  • Ne touche PAS à la structure MyST, aux IDs, aux poids, au format des blocs.
  • UN SEUL bloc {{python}} (4 backticks) terminé par `globals()` ; les
    distracteurs restent construits DANS ce bloc (variables camelCase `…Aff`),
    à DELTA NON NUL garanti (jamais de flip de signe sur une entrée nulle).
  • Exactement UNE `:isRightAnswer: true`, en slot 1 ; « None » en dernier.
  • L'énoncé ne révèle JAMAIS la réponse ; garde la solution fidèle à la source.
  • Injections `{{{{ }}}}` = noms de variables nus camelCase `Aff` uniquement.

EXERCICE ACTUEL :
{exercise}

Réponds UNIQUEMENT avec l'exercice complet corrigé (de `````{{exercise}} à `````),
sans préambule ni wrapper markdown.
"""  # noqa: E501
