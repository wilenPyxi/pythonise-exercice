# Règles de pythonisation PyxiScience — Base de connaissances

> Document destiné à être injecté dans un prompt système Claude Code modifiant le générateur d'exercices pythonisés. Chaque règle est dérivée de bugs réels rencontrés en production sur les annales Bac (Métropole J2 18/06/2025, exos 2 à 4) et de leur correction validée par l'équipe contenu.

---

## 0. Objectif

Le générateur prend en entrée :
- un énoncé APMEP (PDF/LaTeX/image)
- une version PyxiScience non pythonisée déjà validée par Chabane

Et produit en sortie une version pythonisée MyST (`.md`) prête pour soumission à la plateforme.

Les règles ci-dessous codifient les invariants à respecter. Tout livrable qui les enfreint sera rejeté par l'audit.

---

## 1. Conventions PyxiScience (rappel)

Ces conventions sont préalables et non négociables. Le générateur les respecte par défaut.

- **Variables Python** : camelCase uniquement. Les underscores (`p_a`, `coef_t`) provoquent des erreurs de subscript LaTeX dans certains contextes.
- **Bloc Python** : ouvert avec **4 backticks** (vérifié sur 222/222 exemples livrés — constante `PYTHON_FENCE_BACKTICKS` dans `app/config.py`), terminé par `globals()` pour exposer les variables au moteur de rendu MyST (accès via `{{var}}`). Enveloppe `{exercise}` = 5 backticks.
- **Bilingue** : rôles inline `` {fr}`...`{en}`...` `` UNIQUEMENT (aucun bloc `:::{fr}`/`:::{en}` dans les 222 exemples livrés — ne pas en produire).
- **Math display** : `\begin{equation*}...\end{equation*}` avec `&` pour alignement. Ne JAMAIS utiliser `\[ \]` ni `$$ $$`.
- **Espacement** : `\phantom{-}\\` pour saut vertical en math, `%` avant la première équation d'un bloc.
- **Interdits** : `\textbf{}` (utiliser `**...**`), `\begin{itemize}` (utiliser `$\bullet$` ou tirets MyST), `\bbRac` (n'existe pas), variable nommée `total` (réservée), `if pxs_variation_number` (vaut toujours 1).
- **Niveaux de difficulté** : `Advanced` = avancé, `Intermediate` = intermédiaire.
- **`pxsl_format_number` ne fait PAS d'arrondi** — c'est purement un formattage (virgule française). Toujours arrondir AVANT.

### RÈGLE 1.1 — `$` collé à un chiffre : préfixer par `${}` (casse silencieuse)

Ajoutée 2026-06-12 (cas réel : 1413 occurrences dans les lots livrés ; motif interdit du harnais).

**❌ FAUTIF** :
```latex
Calculer $4\bigl(g(\sqrt{x})\bigr)^2$. Le prix est ${{prixAff}}$ €.
```

**✅ CORRIGÉ** :
```latex
Calculer ${}4\bigl(g(\sqrt{x})\bigr)^2$. Le prix est ${}{{prixAff}}$ €.
```

**POURQUOI** : un `$` immédiatement suivi d'un chiffre est lu par le moteur comme un MONTANT en devise, pas comme une ouverture de math inline ; le `$…$` se désynchronise et toute la directive part en texte brut. Le groupe vide `{}` est invisible au rendu. Préfixer par `${}` TOUTE injection inline `${{…}}` susceptible de rendre un nombre. (L'app applique un auto-correctif déterministe dans `app/pipeline/postprocess.py::fix_dollar_digit`.)

---

## 2. Métadonnées du fichier

### RÈGLE 2.1 — `:id:` en première ligne, vide

```
`````{exercise}
:id:
:title:...
:modules: ...
...
```

**❌ FAUTIF**
```
`````{exercise}
:title:...
:id: 7dd83aee-26e1-11f1-828c-0ed8d3b012a9
```

**✅ CORRIGÉ**
```
`````{exercise}
:id:
:title:...
```

**POURQUOI** : la plateforme génère un nouvel ID à la soumission. Tout ID hardcodé sera réutilisé et provoquera un conflit.

### RÈGLE 2.2 — Toutes les autres métadonnées sont conservées strictement à l'identique

Aucun ajout, aucune modification de `:title:`, `:modules:`, `:level:`, `:involvedConcepts:`, `:originalSource:`, etc.

---

## 3. Architecture du bloc Python — UN SEUL BLOC PRINCIPAL

### RÈGLE 3.1 — Tous les paramètres aléatoires et calculs sont dans UN bloc Python en début d'exercice

**❌ FAUTIF** (cas vu dans la version pythonisée fournie de l'exo 4)
```python
# Bloc 1 (début exo)
v0 = rd.randint(10, 15)
k = round(rd.uniform(0.4, 0.8), 1)
...

# Bloc 2 (avant Q3)
k_val = round(rd.uniform(0.4, 0.8), 1)  # REDÉFINIT k !
t_A = round(rd.uniform(4.0, 6.0), 1)
...

# Bloc 3 (avant Q5)
v0 = rd.randint(10, 15)  # REDÉFINIT v0 !
k_val = round(rd.uniform(0.4, 0.8), 1)
...
```

**✅ CORRIGÉ**
```python
# UN SEUL bloc en début d'exercice
import random as rd
import math
import numpy as np
import matplotlib.pyplot as plt
from sympy import Rational, latex
from pyxiscience.Mes_fctions_generalistes_bis import pxs_config, pxsl_format_number

config_std = pxs_config()

# Tirage initial
v0 = rd.choice([11, 12, 13])
k_num = rd.choice([5, 6])
k_coef = Rational(k_num, 10)

# Toutes les variables dérivées calculées ici
inv_k = Rational(10, k_num)
asymptote = v0 * inv_k + inv_k**2
alpha = ...
# etc.

globals()
```

**POURQUOI** : `random.seed` n'est pas réinitialisé entre blocs Python. Redéfinir `v0`, `k_coef`, etc. dans des blocs ultérieurs fait que les valeurs **diffèrent entre questions** : Q4 dit "y' + 0,6y = e^(-0,6t)" puis Q7 dit "v(t) = (12+t)e^(-0,4t)" → exercice incohérent.

### RÈGLE 3.2 — Imports uniquement dans le premier bloc

Tous les `import numpy as np`, `import matplotlib.pyplot as plt`, etc. sont factorisés. Les blocs ultérieurs (typiquement le bloc graphique) réutilisent les imports via `globals()`.

### RÈGLE 3.3 — Le bloc graphique réutilise les variables du bloc principal

Si un bloc Python séparé est nécessaire pour le graphique (placement après l'intro de la partie A par exemple), il doit utiliser les variables déjà calculées, pas les re-tirer.

```python
# Bloc graphique (après l'énoncé de la partie A)
fig, ax = plt.subplots(figsize=(7, 5))
t_graph = np.linspace(0, 16.5, 2000)
y_graph = np.array([d_num(x) for x in t_graph])  # d_num défini dans bloc principal
ax.plot(t_graph, y_graph, color="blue")
# ...
plt.show()
```

---

## 4. Tirage des paramètres — Cohérence mathématique

### RÈGLE 4.1 — Tirages en Rational exact, pas en flottant arrondi

**❌ FAUTIF**
```python
k = round(rd.uniform(0.4, 0.8), 1)
k_coef = Rational(int(k * 10), 10)  # int(7.0) peut donner 6 à cause des flottants
```

**✅ CORRIGÉ**
```python
k_num = rd.choice([5, 6, 7, 8])
k_coef = Rational(k_num, 10)
```

**POURQUOI** : `round(rd.uniform(0.4, 0.8), 1)` peut produire `0.6999999999999...`, et `int(0.6999... * 10) = 6` au lieu de 7. Bug d'arrondi flottant classique. Tirer directement les entiers numérateurs/dénominateurs.

**TOLÉRANCE** : `round(rd.uniform(...), N)` est ACCEPTABLE pour une **probabilité d'affichage** dont la précision n'est pas critique (par ex. `p = round(rd.uniform(0.05, 0.25), 3)` pour un coefficient binomial affiché à 0.001 près). À ne PAS utiliser pour des valeurs entrant dans des calculs sympy exacts, des bornes d'intervalles, ou des paramètres de récurrence.

### RÈGLE 4.2 — Les paramètres dérivés sont COHÉRENTS avec les paramètres tirés

Tout paramètre qui apparaît dans l'énoncé ET qui dépend mathématiquement d'autres paramètres ne doit pas être tiré indépendamment.

**❌ FAUTIF** (vu dans exo 4)
```python
v0 = rd.randint(10, 15)
k = round(rd.uniform(0.4, 0.8), 1)
L_min = rd.randint(20, 25)  # tirage indépendant
d_15 = rd.randint(12, 18)   # tirage indépendant
```

Conséquences :
- `L_min` peut être inférieur à l'asymptote `v0/k + 1/k²` → la zone de freinage est trop petite, l'énoncé est faux.
- `d_15` n'a aucun lien avec la valeur de `d(2)` à lire sur le graphique → la "lecture graphique" donne un résultat incohérent.

**✅ CORRIGÉ**
```python
v0 = rd.choice([11, 12, 13])
k_num = rd.choice([5, 6])
k_coef = Rational(k_num, 10)

# Paramètres DÉRIVÉS
asymptote = v0 * Rational(10, k_num) + Rational(10, k_num)**2
L_min = math.ceil(float(asymptote))           # garanti > asymptote
d_lecture = round(d_num(2))                   # cohérent avec graphique
```

**POURQUOI** : un paramètre qui doit satisfaire une contrainte mathématique se calcule, il ne se tire pas.

### RÈGLE 4.3 — Les paramètres aléatoires PRÉSERVENT la propriété démontrée

Si l'exercice démontre une propriété (ex: `w_n ≥ n`), les paramètres tirés doivent la rendre vraie pour TOUS les seeds.

**❌ FAUTIF** (vu dans exo 3)
```python
w0 = rd.randint(-2, 3)
alpha = rd.randint(2, 4)
beta = rd.randint(-3, -1)
gamma = rd.randint(1, 5)
```

Sur 1000 seeds testés :
- 36% ont `w0 < 0` → l'initialisation `w_0 ≥ 0` est fausse.
- 34% ont `α + β ≤ 0` → la récurrence `w_n ≥ n` est mathématiquement fausse (testé : `α=2, β=-3, γ=1, w_0=1` donne `w_4 = -2 < 4`).

**✅ CORRIGÉ**
```python
# Contrainte : w_0 >= 0, alpha + beta = 1, gamma >= 1
w0 = rd.randint(0, 3)
ab_pairs = [(2, -1), (3, -2), (4, -3)]   # alpha + beta = 1 garanti
alpha, beta = rd.choice(ab_pairs)
gamma = rd.randint(1, 5)
```

**POURQUOI** : pythoniser ne signifie pas randomiser sans contrainte. La propriété démontrée doit rester vraie sur 100% des variantes. Si nécessaire, restreindre la plage ou utiliser une boucle `while` pour rejeter les tirages invalides.

**EXTENSION — calculs intermédiaires dans `detailedSolution`** : si une variable aléatoire change (ex. `p ∈ {0.7, 0.8, 0.9}`), TOUS les calculs intermédiaires affichés dans les `detailedSolution` doivent être recalculés à partir de cette variable. **Aucune valeur dérivée ne peut être hardcodée en littéral.**

```
❌ FAUTIF : `= 0{,}81 + 0{,}01 = 0{,}82` (vrai uniquement pour p=0.9)
✅ CORRIGÉ : `= {{p_fidele_carre_str}} + {{p_contraire_carre_str}} = {{p_V3_str}}`
```

L'audit doit lister TOUS les nombres décimaux apparaissant dans les `detailedSolution` et vérifier qu'ils proviennent d'une variable Python, pas d'une chaîne littérale.

### RÈGLE 4.5 — Détection des invariants Vrai/Faux dépendants des paramètres

Pour les exercices "Vrai ou Faux", la réponse V/F dépend souvent de valeurs numériques précises. **Avant de tirer aléatoirement un paramètre**, vérifier algébriquement pour quelles valeurs la réponse V/F annoncée par la solution reste correcte.

Exemples typiques :
- `∫₀^a x² dx = a²` (aire d'un carré) ⟺ `a = 3`
- `f(x) = e^x + e^(cx)` solution de `y' = cy - e^x` ⟺ `c = 2`
- `A(n, k) = C(m, p)` ⟺ couples (n, k, m, p) précis

**Deux stratégies acceptables** :
1. **Fixer les paramètres** sur la valeur source (pas de variation aléatoire)
2. **Adapter dynamiquement la conclusion V/F** selon le tirage (cf. règle 8.4)

### RÈGLE 4.6 — Arrondi nul à supprimer

Quand une probabilité ou un résultat est exprimé en notation scientifique (valeur `< 10⁻³`), ne pas afficher l'arrondi `≈ 0,000` qui n'apporte aucune information.

**✅ PATTERN**
```python
if round(float(proba), 3) == 0:
    proba_final = proba_exact_str           # ex: "8,1 × 10⁻⁵"
else:
    proba_final = f"{proba_exact_str} \\approx {proba_str}"
```

### RÈGLE 4.7 — Cohérence des formules développées avec les paramètres

Si une solution développe une formule pas à pas (ex. `n × (n-1) × (n-2)` pour un arrangement à `k=3`), le paramètre `k` DOIT être fixé OU le développement DOIT être généré dynamiquement.

**✅ PATTERN — helpers à inclure dans le bloc `{python}`**
```python
def develop_chain(start, length):
    """start × (start-1) × ... (length facteurs)"""
    return " \\times ".join(str(start - i) for i in range(length))

def develop_chain_to(start, end_inclusive):
    """start × (start-1) × ... × end_inclusive"""
    return " \\times ".join(str(i) for i in range(start, end_inclusive - 1, -1))
```

### RÈGLE 4.8 — Pas d'assertion sur les distances numériques

Quand on tire une variable "presque égale" à une valeur cible (typiquement pour créer un piège dans un Vrai/Faux), NE PAS imposer un seuil de distance strict — l'inégalité mathématique structurelle (ex: rationnel vs irrationnel) suffit.

```
❌ FAUTIF : assert abs(float(frac) - J_approx) > 1e-4
            # plante pour 7/11 (différence ≈ 7×10⁻⁵) qui est pourtant
            # le piège le plus crédible

✅ CORRIGÉ : pas d'assertion sur la distance — la distinction structurelle
            (rationnel vs irrationnel) garantit l'inégalité.
```

### RÈGLE 4.4 — Identifier les contraintes mathématiques avant de pythoniser

Avant de transformer une constante en variable aléatoire, vérifier qu'elle peut varier sans casser :
- l'initialisation d'une récurrence
- les conditions d'une inégalité
- les hypothèses d'un théorème invoqué dans la solution
- le sens d'une asymptote / limite

Si une contrainte existe, soit borner le tirage, soit ne pas pythoniser ce paramètre.

---

## 5. Calculs — Rational exact, pas de double approximation

### RÈGLE 5.1 — Tous les calculs intermédiaires en Rational/Fraction exacte

**❌ FAUTIF**
```python
p_A = round(rd.uniform(0.4, 0.8) / 0.05) * 0.05   # produit 0.35000000000000003
```

**✅ CORRIGÉ**
```python
num_pA = rd.randint(8, 16)         # 0,40 à 0,80 par pas de 0,05
p_A = Fraction(num_pA, 20)
```

### RÈGLE 5.2 — Conversion `float()` UNIQUEMENT au moment de l'affichage

```python
# Calculs : tout en Rational
asymptote = v0 * inv_k + inv_k**2

# Affichage : convertir avec arrondi explicite
asymptote_disp = pxsl_format_number(round(float(asymptote), 2), **config_std)
```

### RÈGLE 5.3 — Pas de fractions reconstruites par double `limit_denominator`

**❌ FAUTIF**
```python
frac = Fraction(p_float).limit_denominator(1000) / Fraction(q_float).limit_denominator(1000)
frac = frac.limit_denominator(100)
```

**✅ CORRIGÉ**
```python
# Calculer la fraction exacte directement à partir des Rational initiaux
frac_exact = p_inter_q / p_total
```

### RÈGLE 5.4 — Centième inférieur via `math.floor`, pas via formule arithmétique

**❌ FAUTIF**
```python
seuil_arrondi = round(seuil * 100 - 5) / 100   # donne 0,73 au lieu de 0,77
```

**✅ CORRIGÉ**
```python
seuil_arrondi = math.floor(seuil * 100) / 100
```

### RÈGLE 5.5 — Vérifier les opérations sur les coefficients

Si la solution simplifie `αn + βn`, le coefficient résultant est `α + β`, pas `α - β`.

**❌ FAUTIF** (vu dans exo 3)
```python
# Dans la solution :
{{alpha}} w_n {{beta}} n + {{gamma}} &\geqslant {{alpha - beta}} n + {{gamma}}
```

Avec `α=3, β=-2`, le code calcule `α - β = 5` au lieu de `α + β = 1`. Bug critique de simplification.

**✅ CORRIGÉ**
```python
{{alpha}} w_n {{beta_n_str}} + {{gamma}} &\geqslant n + {{gamma}}    # car alpha + beta = 1
```

---

## 6. Interpolation MyST `{{...}}` — Pièges critiques

### RÈGLE 6.1 — INTERDIT : appels de fonction avec `**kwargs` dans `{{...}}`

**❌ FAUTIF**
```
La suite converge vers ${{latex(limite_proposee, **config_standard)}}$.
```

**Le rendu produit `latex(limite_proposee, **config_standard)` en clair**, pas la valeur. Cause : MyST parse `**config_standard` comme du gras markdown, ce qui casse l'expression.

**✅ CORRIGÉ**
```python
# Dans le bloc Python
limite_proposee_tex = latex(limite_proposee, **config_standard)
```
```
La suite converge vers ${{limite_proposee_tex}}$.
```

**POURQUOI** : tout appel `f(x, **kwargs)` dans `{{...}}` est interprété par MyST comme markdown avant interpolation Python. Toujours stocker le résultat dans une variable string en amont.

### RÈGLE 6.2 — `pxsl_format_number(...)` dans `{{...}}` : créer la string en amont

**❌ FAUTIF**
```
Le coefficient vaut ${{pxsl_format_number(round(float(coef), 2), **config_standard)}}$.
```

**✅ CORRIGÉ**
```python
coef_disp = pxsl_format_number(round(float(coef), 2), **config_std)
```
```
Le coefficient vaut ${{coef_disp}}$.
```

### RÈGLE 6.3 — Pré-calculer toutes les variables d'affichage dans le bloc Python

À la fin du bloc Python principal, créer un bloc dédié au formattage. Seul `sympy.latex(...)` accepte `**config_standard` — les helpers PyxiScience (`pxsl_format_number`, `pxsl_res_num`, etc.) ont leurs propres kwargs spécifiques (cf. règle 6.4).

```python
# === Variables d'affichage prêtes ===
k_disp        = pxsl_format_number(float(k_coef))                    # PAS de **config_std
coef_const_disp = pxsl_format_number(float(coef_const))
inv_k_tex     = latex(inv_k, **config_standard)                      # OK ici
asymptote_tex = latex(asymptote, **config_standard)                  # OK ici
alpha_disp    = pxsl_format_number(alpha)
# etc.

globals()
```

Le markdown ne contient alors plus que `{{var}}` simples, sans appel de fonction.

### RÈGLE 6.4 — `**config_standard` réservé à `sympy.latex`

Le résultat de `pxs_config()` contient des clés (`ln_notation`, `mat_str`, etc.) destinées **uniquement à `sympy.latex()`**. Les helpers PyxiScience (`pxsl_format_number`, `pxsl_res_num`, `pxsl_matrix`, etc.) ont leurs propres kwargs et **plantent** si on leur passe `**config_standard`.

```
❌ FAUTIF : pxsl_format_number(aire_carre, **config_standard)
            → TypeError: got an unexpected keyword argument 'ln_notation'

✅ CORRECT : pxsl_format_number(aire_carre)                    ← pas de splat
✅ CORRECT : pxsl_res_num(proba, dec=4, egal=False)            ← kwargs explicites
✅ CORRECT : latex(p_fidele, **config_standard)                ← seul sympy.latex
```

Liste explicite : **NE PAS** splat `**config_standard` sur `pxsl_format_number`, `pxsl_res_num`, `pxsl_matrix`, `pxsl_pow`, `pxsl_latex_coefficient` (alias `lc`), `pxsl_par`, `pxsl_mult`, `pxsl_choose_udv`, `pxs_Interval(...).print()`. **TOUJOURS** splat sur `sympy.latex(...)`.

### RÈGLE 6.5 — `{{ }}` ne contient QU'UN nom de variable nu (camelCase, suffixe `Aff`)

Ajoutée 2026-06-12 (convention vérifiée sur 222/222 exemples livrés : 0 appel de fonction, 0 underscore, 2563 injections `…Aff` ; contrôle STATIQUE du harnais).

**❌ FAUTIF** :
```latex
$T(x) = {{latex(T)}}$, coefficient {{lc(a, sign=True)}}, sur {{dom.print()}}, p = {{p_str}}
```

**✅ CORRIGÉ** :
```python
# Dans le bloc Python :
tTex = latex(T, **config_standard)
coefAAff = lc(a, sign=True)
domAff = dom.print()
pStr = str(p)
```
```latex
$T(x) = {{tTex}}$, coefficient {{coefAAff}}, sur {{domAff}}, p = {{pStr}}
```

**POURQUOI** : le runtime de la plateforme ne substitue de façon fiable que des identifiants nus ; un appel/calcul dans `{{ }}` peut fuir tel quel dans le rendu, et un underscore crée des indices LaTeX parasites. Tout s'évalue dans le bloc Python, dans des variables d'affichage camelCase suffixées `Aff`. (Auto-lift déterministe : `app/pipeline/postprocess.py::auto_lift_injections` + `rename_underscore_injections`.)

---

## 7. Affichage des coefficients signés — Anti-concaténation

### RÈGLE 7.1 — NE JAMAIS concaténer un signe à une valeur dans le markdown

**❌ FAUTIF**
```
w_{n+1} = {{alpha}} w_n {{beta}} n + {{gamma}}
```

Avec `β = -1`, le rendu donne `2 w_n -1 n + 3` (moche : `-1n` au lieu de `-n`).

**✅ CORRIGÉ**
```python
# Dans le bloc Python
if beta == -1:
    beta_n_str = "- n"
elif beta < 0:
    beta_n_str = f"- {-beta}n"
else:
    beta_n_str = f"+ {beta}n"
```
```
w_{n+1} = {{alpha}} w_n {{beta_n_str}} + {{gamma}}
```

### RÈGLE 7.2 — Pour tout coefficient pouvant être ±, générer une string complète avec signe intégré

```python
# Pour v'(t) = (coef_const + coef_t * t) e^(-kt)
# coef_const < 0 toujours → latex(coef_const) commence par "-"
# coef_t < 0 toujours → on construit explicitement
coef_t_signed = f"- {pxsl_format_number(float(-coef_t), **config_std)}"
# Affichage : ({{coef_const_disp}} {{coef_t_signed}} t)
# → "(-6,2 - 0,6 t)"
```

### RÈGLE 7.3 — Cas typiques de coefficients à traiter explicitement

- Coefficient devant `t`, `n`, `x` (terme variable d'un polynôme)
- Constante d'intégration ajoutée
- Reste d'une factorisation
- Termes dans une somme avec signes alternés

### RÈGLE 7.4 — Format des décimales à 3 chiffres fixes

Pour les arrondis à 10⁻³ près (consigne fréquente en Bac), utiliser un format à **3 décimales fixes** plutôt que `str(round(...))` qui tronque les zéros.

```
❌ FAUTIF : str(round(0.6561, 3))  →  '0.656'  (OK)
            str(round(0.6, 3))     →  '0.6'    (manque "00" final attendu)

✅ CORRECT : f"{x:.3f}".replace('.', '{,}')
            # 0.6561 → '0{,}656'
            # 0.6    → '0{,}600'
```

---

## 8. Solutions validées — Directive Chabane

### RÈGLE 8.1 — INTERDICTION ABSOLUE de modifier les solutions validées

Le générateur ne doit pas :
- ajouter des listes à puces qui n'existaient pas
- ajouter des préambules redondants en début de solution
- ajouter des étapes intermédiaires de calcul non validées
- reformuler des phrases (changer "factoriser" en "diviser", etc.)
- ajouter de la pédagogie ("Les quatre conditions de la loi binomiale sont vérifiées...")

**❌ FAUTIF** (vu dans exo 3)
```
{fr}`On divise le numérateur et le dénominateur par {{b1}}^n :`
```

Alors que la version validée disait :
```
{fr}`On factorise le numérateur par 5^n et le dénominateur par 3^n :`
```

(La manipulation est en réalité une **factorisation séparée** au numérateur et au dénominateur, pas une division commune.)

**✅ CORRIGÉ**
```
{fr}`On factorise le numérateur par {{b1}}^n et le dénominateur par {{d1}}^n :`
```

### RÈGLE 8.2 — En cas de doute, copier-coller la solution validée

Le générateur ne doit jamais "améliorer" ou "compléter" une solution validée. Si la pythonisation impose une adaptation (variable au lieu de constante), substituer mécaniquement et rien d'autre.

### RÈGLE 8.3 — Si la pythonisation a touché à une solution validée, signaler avant correction

L'audit doit demander confirmation explicite avant de restaurer. Le générateur ne doit pas le faire silencieusement.

### RÈGLE 8.4 — Conclusions Vrai/Faux adaptatives

Pour les exos "Vrai ou Faux" où on veut faire varier des paramètres qui peuvent changer la réponse, préparer la conclusion en Python comme variable conditionnelle :

```python
if condition_vraie:
    conclusion_fr = "... L'affirmation est vraie."
    conclusion_en = "... Statement is true."
else:
    conclusion_fr = f"... (détail spécifique). L'affirmation est fausse."
    conclusion_en = f"... (specific detail). Statement is false."
```

Puis injecter via `{{conclusion_fr}}` / `{{conclusion_en}}` dans la `detailedSolution`. La structure du raisonnement reste identique, seul le verdict final s'adapte au tirage.

---

## 9. Structure MyST — Paragraphes contextuels

### RÈGLE 9.1 — Les paragraphes contextuels (intro de partie, intro de question groupée) sont HORS `questionStatement`

**❌ FAUTIF**
```
:::::{question}
:questionType: STQ

::::{questionStatement}
$\underline{\textbf{Partie A}}$

{fr}`Le centre propose aux personnes...`{en}`...`

{fr}`Question 1...`{en}`...`
::::
```

**✅ CORRIGÉ**
```
$\underline{\textbf{Partie A}}$

{fr}`Le centre propose aux personnes...`{en}`...`

(exo1-q1)=

:::::{question}
:questionType: STQ

::::{questionStatement}
{fr}`Question 1...`{en}`...`
::::
```

**POURQUOI** : `questionStatement` doit contenir UNIQUEMENT la consigne de la question. Tout contexte commun à plusieurs questions est un paragraphe libre entre les blocs `:::::{question}`.

### RÈGLE 9.2 — Les paragraphes contextuels qui utilisent des variables `{{var}}` viennent APRÈS le bloc Python qui les définit

```
```{python}
v0 = ...
k_coef = ...
globals()
```

{fr}`On considère la fonction $v$ avec $v(0) = {{v0}}$.`{en}`...`
```

### RÈGLE 9.3 — Phrase "Dans cette question, on étudie..." (regroupement APMEP)

L'APMEP utilise parfois "Dans cette question, on étudie X" pour introduire un groupe de sous-questions (2.a, 2.b, 2.c, 2.d). En PyxiScience, les sous-questions sont éclatées en questions distinctes.

**RÈGLE** : reformuler en précisant le périmètre exact pour ne pas inclure les questions hors groupe.

```
{fr}`Dans les quatre questions qui suivent, on étudie la fonction $v$ sur $[0~;~+\infty[$.`
```

Le **nombre est explicite** (`les quatre questions`) pour éviter d'englober la question suivante (numérotée séparément en APMEP).

### RÈGLE 9.4 — Pas de doublons d'énoncés

L'énoncé de chaque question apparaît UNE SEULE FOIS, dans son `questionStatement`. Ne pas le répéter en paragraphe libre avant le bloc question.

**❌ FAUTIF** (vu dans exo 4)
```
{fr}`Que vaut $d'(t_A)$ ? Interpréter ce résultat.`

:::::{question}
::::{questionStatement}
{fr}`Que vaut $d'(t_A)$ ? Interpréter ce résultat.`   # DOUBLON
::::
```

### RÈGLE 9.5 — Variables Python dans les blocs matplotlib

Les substitutions `{{...}}` ne fonctionnent que dans le **texte MyST**, **PAS** à l'intérieur des blocs ```` ```{python} ```` . Dans un bloc Python, utiliser les vraies variables Python (f-string ou concaténation).

```
❌ FAUTIF : probs = r"${{p_fidele_str}}$"
            # matplotlib reçoit littéralement "${{p_fidele_str}}$"
            # mathtext rend "p_fidele_str" en italique math (incompréhensible)

✅ CORRECT : probs = f"${p_fidele_str}$"
            # Python interpole d'abord → matplotlib reçoit "$0{,}9$"
```

Pareil pour les `ax.set_title(...)`, `ax.text(...)`, `ax.legend(...)` : utiliser des f-strings Python, jamais `{{...}}`.

---

## 10. Bilinguisme FR/EN — Symétrie

### RÈGLE 10.1 — FR et EN doivent être équivalents en niveau de détail

**❌ FAUTIF** (vu dans exo 2 Q6, exo 4 Q9)
- FR détaille le changement de variable `X = 0,6t` puis applique les croissances comparées (5 lignes)
- EN saute directement à "by comparison of growth rates" puis le boxed (2 lignes)

**✅ CORRIGÉ** : les deux versions ont le même squelette de raisonnement, mêmes étapes, mêmes formules.

### RÈGLE 10.2 — Notation math identique en FR et EN

**❌ FAUTIF**
```
{fr}`...l'intervalle $[0\,;\,1]$.`{en}`...the interval [0\,;\,1].`
                                                  ^^^^^^^^^^^ pas en mode math
```

**✅ CORRIGÉ**
```
{fr}`...l'intervalle $[0\,;\,1]$.`{en}`...the interval $[0\,;\,1]$.`
```

### RÈGLE 10.3 — Si l'utilisateur a modifié l'énoncé, effacer la version EN

Si la version pythonisée modifie le contenu de l'énoncé (pas seulement réagencement structurel), le générateur efface tous les blocs `{en}` pour permettre passage en retraduction par l'app dédiée. Le réagencement (séparation a/b/c en questions distinctes) n'est PAS une modification.

### RÈGLE 10.4 — Format auto fraction / décimal selon la nature

Pour les valeurs qui peuvent être rationnelles non-décimales (ex. `0,5 / 0,6 = 5/6`), créer un helper qui choisit automatiquement entre forme décimale finie et fraction LaTeX :

```python
def _frac_to_latex(f):
    """Fraction Python → décimal LaTeX si fini, sinon \\frac{a}{b}."""
    if f.denominator == 1:
        return str(f.numerator)
    d = f.denominator
    while d % 2 == 0: d //= 2
    while d % 5 == 0: d //= 5
    if d == 1:
        return str(float(f)).replace('.', '{,}')
    return f"\\frac{{{f.numerator}}}{{{f.denominator}}}"
```

Exemples :
- `_frac_to_latex(Fraction(5, 8))` → `'0{,}625'` (décimal fini)
- `_frac_to_latex(Fraction(5, 6))` → `'\\frac{5}{6}'` (décimal infini)
- `_frac_to_latex(Fraction(5, 4))` → `'1{,}25'` (décimal fini)

### RÈGLE 10.5 — Notation scientifique française pour valeurs très petites

Pour les valeurs `< 10⁻⁴`, basculer en notation scientifique LaTeX plutôt qu'afficher `0{,}000081`.

```python
import math

def _frac_to_str_smart(f, sci_threshold=1e-4):
    """Décimal pour valeurs raisonnables, sinon notation scientifique."""
    fl = float(f)
    if 0 < abs(fl) < sci_threshold:
        exp = int(math.floor(math.log10(abs(fl))))
        mant = fl / (10 ** exp)
        mant_str = f"{mant:.2f}".rstrip('0').rstrip('.').replace('.', '{,}') or "1"
        return f"{mant_str} \\times 10^{{{exp}}}"
    return _frac_to_latex(f)
```

---

## 11. Rendu graphique matplotlib

### RÈGLE 11.1 — Toute variable utilisée dans l'énoncé DOIT être utilisée dans le tracé

**❌ FAUTIF** (vu dans exo 3)
```python
x_tangente_horiz = rd.randint(1, 3)   # tirée

# Énoncé : "tangente horizontale en x = {{x_tangente_horiz}}"

# Mais le code matplotlib trace une fonction f(x) = K * (x^c - 1) * ln(x)
# qui a SA tangente horizontale FIGÉE en x=1 (par construction f(1)=0, f'(1)=0).
```

Le graphique montre la tangente horizontale en x=1 alors que l'énoncé annonce x=2 ou x=3. Incohérent dans 66% des seeds.

**✅ CORRIGÉ**
- Soit fixer `x_tangente_horiz = 1` (constante), soit modifier la fonction tracée pour que sa tangente horizontale soit effectivement en `x_tangente_horiz`.

### RÈGLE 11.2 — La tangente tracée DOIT être la vraie tangente analytique

**❌ FAUTIF**
```python
slope = f(x_A) / (x_A + 0.3)   # heuristique arbitraire
```

**✅ CORRIGÉ**
```python
def f_prime(x):
    c = coeff_puissance
    return facteur * (c * x**(c-1) * np.log(x) + (x**c - 1)/x)

slope = f_prime(x_A)
b_intercept = f(x_A) - slope * x_A
```

### RÈGLE 11.3 — Les labels (Cf, T, Δ, A) doivent rester DANS la fenêtre du graphique

**Symptôme** : si un label est positionné à `(x, y)` avec `y > ylim_max`, matplotlib étend automatiquement la zone d'affichage pour l'inclure, ce qui **compresse** le graphique.

**❌ FAUTIF**
```python
ax.set_ylim(-1.2, 8)
ax.text(11, f(11) - 0.4, r"$\mathcal{C}_f$", ...)   # f(11) peut être > 8
ax.text(11, slope*11 + b_intercept + 0.15, "T", ...)  # idem
```

**✅ CORRIGÉ**
```python
# Borner les paramètres pour que f(x_max_visible) reste sous le plafond
y_label_target = 6.5
denom_y_max = (x_max**coeff_puissance - 1) * np.log(x_max)
facteur_max = min(70, int(y_label_target / denom_y_max))
facteur_echelle = rd.randint(30, max(30, facteur_max))

# Placer les labels dans une zone garantie sûre
x_label = max(x_A + 1, x_max - 1.5)
x_label = min(x_label, x_max)
y_lab_cf = f(x_label) - 0.3
y_lab_t  = min(slope * x_label + b_intercept + 0.5, ylim_max - 0.5)
```

### RÈGLE 11.4 — Pas de mélange Rational sympy + numpy array

**❌ FAUTIF**
```python
d_vals = Rational(5, 3) * t_graph + asymptote   # Rational * np.array casse
```

**✅ CORRIGÉ**
```python
d_vals = float(Rational(5, 3)) * t_graph + float(asymptote)
# ou
inv_k_float = 1.0 / float(k_coef)
d_vals = -(v0 + t_graph) * inv_k_float * np.exp(-float(k_coef) * t_graph) + ...
```

### RÈGLE 11.5 — `plt.show()`, jamais `plt.savefig`

```python
# ❌ Le chemin local n'est pas résolu côté plateforme
plt.savefig('arbre.png')
# puis dans le markdown : ![](arbre.png)

# ✅
plt.show()
```

### RÈGLE 11.6 — Pas d'éléments parasites dans le graphique

- Pas de `ax.text(8.5, 22.2, "Fig. 2", ...)` à l'intérieur du graphique. La référence "Fig. 2" est une légende externe APMEP, pas un élément du tracé.
- Pas de doubles labels "1" sur les axes si les ticks par défaut sont déjà annotés.
- Pas de titre auto matplotlib.

---

## 12. Fidélité APMEP

### RÈGLE 12.1 — L'énoncé pythonisé est strictement conforme à l'APMEP, modulo paramètres

- Toutes les phrases-clés de l'énoncé original sont présentes textuellement.
- Toutes les valeurs numériques sont identiques (modulo pythonisation).
- L'ordre des questions est respecté.

### RÈGLE 12.2 — Sous-questions APMEP a/b/c → questions PyxiScience distinctes

Convention PyxiScience : chaque sous-question APMEP devient une question distincte (`q1`, `q2`, ...) avec son propre `questionStatement` / `questionHint` / `detailedSolution`. Ce réagencement n'est PAS une modification d'énoncé au sens de la directive 2.

### RÈGLE 12.3 — Géométrie : pythonisation autorisée à condition de préserver le niveau

La pythonisation des exercices de géométrie dans l'espace (vecteurs, droites, plans, projections, orthocentres) est **autorisée** (cf. exos validés Amérique du Sud 13 novembre 2025, Amérique du Nord 22 mai 2025). Convention observée :

- **Représenter les points/vecteurs en `sympy.Matrix([x, y, z])`** pour calculs symboliques.
- **Vérifier l'orthogonalité via `.dot()` = 0** au lieu de calculer par projection.
- **Pour une projection orthogonale**, paramétrer la droite (`K = A + lam*(B-A)`), construire `CK.dot(AB) = 0`, résoudre via `solve(...)`.
- **Distances via `sqrt(vec.dot(vec))`** (norme).

⚠️ **NE PAS changer le niveau pédagogique** : si l'APMEP demande une démonstration géométrique (collinéarité, coplanarité, équation cartésienne d'un plan), la version pythonisée doit conserver cette difficulté — on randomise les coefficients, pas la nature du raisonnement.

**❌ FAUTIF** (mauvaise pythonisation)
```python
# Donner les coordonnées du point projeté directement
A = Matrix([1, 0, 0]); B = Matrix([0, 1, 0]); C = Matrix([0, 0, 1])
K = Matrix([0.5, 0.5, 0])  # hardcodé — élève n'a plus à calculer
```

**✅ CORRIGÉ**
```python
# Le tirage des sommets randomise les valeurs, mais l'élève DOIT calculer la projection
alpha, beta, gamma = rd.sample(range(1, 4), 3)
A = Matrix([alpha, 0, 0]); B = Matrix([0, beta, 0]); C = Matrix([0, 0, gamma])
lam = Symbol('lam', real=True)
K = A + lam*(B - A)
sol = solve((K - C).dot(B - A), lam)[0]
# K_proj = A + sol*(B - A)  # ← l'élève le démontre dans sa solution
```

### RÈGLE 12.4 — Coquilles APMEP corrigées silencieusement

Si l'APMEP contient une coquille (ex: "au activités" sans "x"), la version PyxiScience peut la corriger silencieusement. Ce n'est pas une modification d'énoncé.

---

## 13. Pièges spécifiques par type d'exercice

### 13.1 — Probabilités

- Tirages de probabilités : `rd.randint(a, b) / 20` + `Fraction`, jamais `round(uniform/0.05)*0.05`.
- Variables conditionnelles : ne pas écraser `p_non_B_sachant_non_A` (P_{Ā}(B̄)) par `p_non_A_sachant_non_B` (P_{B̄}(Ā)). Ce sont des conditionnelles inversées (Bayes), pas la même quantité.
- Loi binomiale : `scipy.stats.binom.cdf(k, n, p)` pour `P(X ≤ k)`.
- Bienaymé-Tchebychev : `math.floor(seuil*100)/100` pour le centième inférieur.

### 13.2 — Suites

- Variation `\case1`/`\case2` : à mettre INSIDE `\right{}`/`\wrong{}`, jamais autour.
- `pxs_variation_number` toujours = 1 dans le code Python — calculer toutes les variations en parallèle.
- Récurrence : voir RÈGLE 4.3 (préserver la propriété par contraintes sur les paramètres).

### 13.3 — Analyse / Intégration

- Constante d'intégration : ajouter `\py{C_new}` ou demander explicitement à l'utilisateur.
- Pas de concaténation `\py{sg(x)}` : créer une variable complète `signe_coeff_x = "+ val"` ou `"- val"` (RÈGLE 7.1).

### 13.4 — Tracés matplotlib

- Voir section 11 complète.

---

## 16bis. Patterns récurrents observés en production

(Section issue de l'analyse des exos validés de mai/novembre 2025. À ne pas confondre avec la section 16 (Anti-patterns), qui liste les BUGS — ici on liste des CONVENTIONS positives à reproduire.)

### RÈGLE 16.1 — Tirage de paramètres avec contraintes : préférer la list comprehension

Quand plusieurs paramètres doivent satisfaire une contrainte couplée (ex: `p_vv > p_nv` et `denominator(1/(1-(p_vv-p_nv))) <= 6`), ne PAS faire de `for _ in range(100): ... if cond: break` qui peut échouer silencieusement. Préférer une **list comprehension qui énumère toutes les combinaisons valides**, puis `rd.choice()`.

**❌ FAUTIF**
```python
for _ in range(100):
    p_vv = rd.choice(valeurs)
    p_nv = rd.choice(valeurs)
    if p_vv > p_nv and Rational(1, 1-(p_vv-p_nv)).denominator <= 6:
        break  # peut sortir sans break, valeurs invalides en silence
```

**✅ CORRIGÉ**
```python
couples_valides = [
    (p_vv, p_nv) for p_vv in valeurs for p_nv in valeurs
    if p_vv > p_nv and Rational(1, 1 - (p_vv - p_nv)).denominator <= 6
]
p_vv, p_nv = rd.choice(couples_valides)  # garanti valide
```

**POURQUOI** : la list comprehension échoue de manière visible (IndexError si liste vide), au lieu de laisser passer des paramètres invalides. Pattern observé dans les exos validés Amérique du Sud 13 novembre 2025.

### RÈGLE 16.2 — Loi binomiale : utiliser scipy.stats.binom (sf / cdf / pmf)

Pour les calculs `P(X ≥ k)`, `P(X ≤ k)`, `P(X = k)` d'une binomiale, **toujours** utiliser `scipy.stats.binom`.

**❌ FAUTIF** (calcul à la main, lent et fragile)
```python
prob_inf = sum(binomial(n, i) * p**i * (1-p)**(n-i) for i in range(k+1))
```

**✅ CORRIGÉ**
```python
from scipy.stats import binom
prob_inf       = binom.cdf(k, n, p)      # P(X ≤ k)
prob_sup_strict = binom.sf(k - 1, n, p)  # P(X ≥ k)   (sf = 1 - cdf(k-1))
prob_egal      = binom.pmf(k, n, p)      # P(X = k)
```

**Astuce conditionnelle** : si `(X ≥ nb) ⊂ (X ≥ ne)` (donc `nb ≥ ne`), alors `P(X ≥ nb | X ≥ ne) = binom.sf(nb-1, n, p) / binom.sf(ne-1, n, p)`. Garantir `ne < nb` au tirage pour que le quotient soit ≤ 1.

**POURQUOI** : `binom.sf` (survival function) évite les sommes manuelles de coefficients binomiaux qui sont coûteuses en sympy et peuvent dériver numériquement. Pattern dans Exo 2 Amérique du Sud, exo binomiale randomisée.

### RÈGLE 16.3 — Matplotlib : axes "zero spines" pour la convention math française

Pour les graphes de fonction (style scolaire FR), positionner les axes sur l'origine et masquer les spines droite/haute. C'est la convention attendue par les enseignants.

**✅ PATTERN STANDARD**
```python
fig, ax = plt.subplots(figsize=(6, 5))
# ... ax.plot(...) ...
ax.spines['left'].set_position('zero')
ax.spines['bottom'].set_position('zero')
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_label_coords(1.02, -0.05)  # label "x" en bout d'axe
ax.yaxis.set_label_coords(-0.05, 1.02)  # label "y" en haut d'axe
plt.show()
```

À utiliser pour **toute étude de fonction** (Bac, terminale). Ne PAS utiliser pour les graphes de distribution / histogrammes (cadre classique avec spines complètes mieux adapté). Pattern observé dans Exos 3 + 4 Amérique du Sud.

---

## 14. Checklist pre-flight avant livraison

Le générateur n'envoie pas le fichier tant que les points suivants ne sont pas cochés :

### Métadonnées
- [ ] `:id:` est en première ligne et vide
- [ ] Toutes les autres métadonnées sont identiques à la version non pythonisée

### Architecture Python
- [ ] UN SEUL bloc Python principal en début d'exercice
- [ ] Imports uniquement dans le premier bloc
- [ ] Tous les blocs Python se terminent par `globals()`
- [ ] Aucune redéfinition de variable entre blocs
- [ ] Bloc graphique (s'il existe) réutilise les variables du bloc principal

### Tirages aléatoires
- [ ] Calculs en `Rational` exact, conversion `float()` uniquement à l'affichage
- [ ] Pas de `int(x * 10)` sur des flottants
- [ ] Tous les paramètres dérivés sont **calculés**, pas tirés indépendamment
- [ ] La propriété démontrée par l'exercice est vraie sur 100% des seeds (testée sur ≥ 200 seeds)
- [ ] Pas de valeurs négatives quand l'énoncé exige des entiers naturels (ex: `w_0 ≥ 0`)

### Affichage / interpolation
- [ ] Aucun `{{f(x, **kwargs)}}` dans le markdown — toutes les strings d'affichage pré-calculées dans le bloc Python
- [ ] Coefficients signés générés explicitement (pas de `{{a}}{{b}}t` avec `b` négatif)
- [ ] `pxsl_format_number` reçoit toujours des valeurs déjà arrondies (`round(float(x), n)` en amont)

### Solutions
- [ ] Toutes les solutions validées Chabane sont conformes textuellement (modulo paramètres)
- [ ] Aucun ajout pédagogique non sollicité (listes à puces, préambules, étapes intermédiaires)
- [ ] Pas de reformulation ("factoriser" reste "factoriser", pas "diviser")

### Structure MyST
- [ ] Paragraphes contextuels HORS `questionStatement`
- [ ] Pas de doublons d'énoncés (chaque énoncé apparaît une seule fois)
- [ ] Phrases "Dans cette question, on étudie..." reformulées avec périmètre explicite
- [ ] Ancres `(exoN-qK)=` présentes avant chaque bloc question

### Bilinguisme
- [ ] FR et EN équivalents en niveau de détail
- [ ] Notation math identique (`$[0\,;\,1]$` dans les deux versions)
- [ ] Si l'énoncé est modifié → blocs `{en}` effacés (sinon conservés intacts)

### Rendu graphique
- [ ] Toutes les variables aléatoires utilisées dans l'énoncé sont effectivement utilisées dans le tracé
- [ ] Tangentes calculées analytiquement (`f'(x_A)`), pas par heuristique
- [ ] Tous les labels (Cf, T, Δ, A) restent dans la fenêtre `[xlim, ylim]`
- [ ] Paramètres bornés pour que les courbes ne sortent pas du cadre
- [ ] `plt.show()` (pas `plt.savefig`)
- [ ] Pas de Rational sympy mélangé à des array numpy

### Tests automatiques
- [ ] Simulation sur ≥ 100 seeds : aucune erreur de rendu
- [ ] Simulation sur ≥ 100 seeds : aucun artefact flottant (`0.35000000000000003`, `0.44999999999999996`)
- [ ] Simulation sur ≥ 100 seeds : toutes les contraintes mathématiques de l'exercice sont respectées
- [ ] Aucune valeur affichée hors plage attendue (probabilité > 1, distance négative, etc.)

---

## 15. Convention de nommage des fichiers

- Version non pythonisée corrigée : `exoN_corrige.md`
- Version pythonisée corrigée : `exoN_pythonise_corrige.md`
- Version FR-only (après modif d'énoncé) : `*_FR_only.md`
- Toujours dans `/mnt/user-data/outputs/`
- Pas de longues chaînes descriptives dans le nom

---

## 16. Anti-patterns récurrents — résumé

Les 10 erreurs les plus fréquentes vues sur les pythonisations livrées :

1. **`{{latex(x, **config_standard)}}`** dans le markdown → casse à cause des `**`. Stocker en variable.
2. **Variables redéfinies entre blocs Python** → valeurs incohérentes entre questions.
3. **Tirages indépendants de paramètres mathématiquement liés** → énoncé faux (ex: `L_min < asymptote`).
4. **Paramètres aléatoires qui invalident la propriété démontrée** → solution dit "vrai" alors que c'est faux.
5. **`int(x * 10)` sur flottant** → bugs d'arrondi (ex: `int(4.7 * 10) = 46`).
6. **Heuristique de tangente** au lieu de `f'(x_A)` analytique.
7. **`x_paramètre` aléatoire mais ignoré dans le tracé matplotlib** → graphique incohérent avec l'énoncé.
8. **Labels matplotlib qui sortent de la fenêtre** → graphique compressé.
9. **Solutions validées modifiées** (listes à puces ajoutées, reformulations, étapes ajoutées) → directive Chabane violée.
10. **Doublons d'énoncés** (même phrase en paragraphe libre + dans `questionStatement`).
