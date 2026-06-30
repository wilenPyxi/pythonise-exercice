<!--
VÉRIFICATION (2026-06-12, contre app/corpus/*.py + 222 exemples livrés) :
 • Les 41 fonctions _bis de ce catalogue sont TOUTES présentes dans le corpus
   embarqué (généralistes / analyse / alg. lin. / proba) ✅.
 • pxs_Interval (Classes_Extensions.py), pxs_construct_RREF, pxs_gauss_jordan
   sont présents (le catalogue en doutait) ✅.
 • NON présents dans le corpus embarqué (runtime plateforme uniquement —
   à n'utiliser que si la plateforme les charge) : myst, pxsl_mat (alias),
   indi_l_r_symb, pxs_round, Poly_with_random_coef.
 • ⚠️ DIVERGENCE catalogue ↔ corpus livré : le §0 recommande `pxsl_latex` et
   « jamais latex() brut ». Or les 222 exemples LIVRÉS de la plateforme
   utilisent `latex(expr, **config_standard)` 126 fois et `pxsl_latex(` 0 fois.
   → L'app garde `latex(expr, **config_standard)` comme voie PAR DÉFAUT pour
   toute sortie scalaire/expression (c'est la forme prouvée VERTE au harnais et
   celle que produit l'auto-lift). `pxsl_latex` reste disponible mais n'est PAS
   le défaut. Pour les MATRICES / SYSTÈMES / PROBA / IBP : utiliser les helpers
   dédiés ci-dessous (le corpus livré ne contient aucun exemple de ces domaines,
   donc le LLM doit s'appuyer sur ces signatures plutôt que coder à la main).
 • Doc en ligne : https://scripts.doc.pyxiscience.com/
-->

# PyxiScience — Catalogue des fonctions (helpers à utiliser DANS le bloc Python)

> Workflow : scanner l'exercice → identifier le domaine (analyse / algèbre
> linéaire / proba / formatage) → récupérer ici les fonctions utiles et leur
> signature exacte AVANT d'écrire du code. **Tout affichage passe par un helper
> du catalogue appelé dans le bloc Python, résultat rangé dans une variable
> `…Aff` injectée nue.** Ne jamais réimplémenter une fonction qui existe ici.

## 0. Conventions critiques

- **Expression/scalaire → `latex(expr, **config_standard)`** (voie par défaut,
  prouvée sur le corpus livré). `pxsl_latex(expr)` existe (convention maison,
  réordonne si `reverse=True`) mais n'est pas le défaut. **Matrice →
  `pxsl_matrix(...)`. Résultat numérique → `pxsl_res_num(...)`.**
- **`config_standard = pxs_config()`** en tête de bloc, puis `**config_standard`
  passé à `latex(...)` (notation `ln`, séparateur FR `,`, ordre des termes).
  `**config_standard` est réservé à `latex()` — **jamais** sur un helper `pxsl_*`.
- **Nom Python réservé** : `total` interdit → `nb_total`.
- **Ne jamais concaténer un signe** : construire la chaîne complète
  (`pxsl_latex_coefficient(c, sign=True)`) puis injecter la variable seule.

## 2. Briques quasi toujours utiles

1. `pxs_config()` → `config_standard`.
2. `latex(expr, **config_standard)` → toute sortie scalaire/expression.
3. `pxsl_latex_coefficient(c, sign=, ones=)` → coefficients signés sans `1·x`/`+0`.
4. `pxsl_res_num(x, dec=, egal=)` → résultat numérique formaté (`= 0,2354`, `23,54 %`).
5. `pxsl_pow(x, n)` → puissance avec parenthèses si base négative/irrationnelle.

## 4. Généralistes — formatage & LaTeX  (`Mes_fctions_generalistes_bis.py`)

- **`pxs_config()`** → dict d'options LaTeX (ln, virgule FR, ordre). `**config_standard`.
- **`latex(expr, **config_standard)`** — voie par défaut. `pxsl_latex(expr, reverse=False)`
  = variante maison (réordonne du degré faible au fort si `reverse=True`).
- **`pxsl_sign(expr)`** → `'+'` / `'-'` / `''`. Construire un signe à part AVANT injection.
- **`pxsl_format_number(n)`** → milliers en espaces fines, gère `±∞`. (Aucun kwarg — pas d'arrondi, arrondir avant.) `pxsl_format_number(1234)`→`'1\ 234'`.
- **`pxsl_latex_with_formatting(expr, sign=False, display=True)`** → `latex()` + milliers (≥1000), y compris dans les fractions.
- **`pxsl_latex_coefficient(coeff, variable=None, sign=False, zeros=True, ones=False, display=True)`** → gère `1`→`''`, `-1`→`'-'` (ou `'-1'` si `ones=True`), signe explicite. Alias `lc`.
- **`pxsl_to_rational_or_symbol(value)`** → `Rational` SymPy précis (via Fraction) ; laisse un Symbol.
- **`pxsl_solve_general_inequality(a=1, b=0, c=0, variable='x', inequality='>=', domain='R', power=1, sign_a=None)`** → résout `a·x^p+b ⋛ c` (p=1 ou 2) + rédaction LaTeX complète. Retour `(solution_set, latex_reasoning)`.
- **`pxsl_Rational(num, den, orientation='v', display=True)`** → fraction « propre » `π/2`, `x/2` (simplifie le numérique, garde le symbolique). ⚠️ ZeroDivisionError si den=0.
- **`pxs_is_reductible_sqrt(x)`** → bool (carré parfait sous la racine).
- **`pxs_separate_factors(expr, var)`** → `(indépendants de var, dépendants de var)`.

## 5. Analyse — intégration par parties  (`Mes_fctions_d_analyse_bis.py`)

- **`pxs_explain_IBP(var=Symbol('x'), f1=None, f2=None, type_int='udv', a=None, b=None, nb_IBP=1, intro=True, conclude=True)`** → **rédaction LaTeX complète** d'un calcul par IPP (intégrale définie `a,b` ou primitive ; une ou deux IPP). Pour « calculer ∫ u·v′ par IPP ». `type_int='udv'`/`'vdu'`. Retour `str` LaTeX prêt à injecter.
  Ex. `ipp = pxs_explain_IBP(f1=x, f2=exp(x), type_int='udv', a=0, b=1)` → `{{ipp}}`.
- **`pxsl_par(expr, minus=False, add=False)`** → parenthèses si l'expression commence par `-` ou est une somme (`Add`). Sécurise un facteur.
- **`pxsl_final_sentence(sol, a, b, var, mult, *args)`** → phrase finale d'une IPP multi-étapes.

## 6. Algèbre linéaire — matrices & systèmes  (`Mes_fctions_d_alg_lineaire_bis.py`)

> `pxsl_*` AFFICHENT (LaTeX) ; `pxs_*` GÉNÈRENT/CALCULENT. `sepG`/`sepD` =
> délimiteurs (`'('`/`')'` défaut ; `'|'`/`'|'` pour un déterminant).

- **`pxsl_pow(x, n=1, opt=0, displaystyle=True)`** → `x^n` avec parenthèses si base négative/irrationnelle. `pxsl_pow(-3,2)`→`'\left(-3\right)^{2}'`.
- **`pxsl_matrix(A, sepG='(', sepD=')', display=False)`** → matrice LaTeX (nombres alignés à droite) ; `'|','|'` → déterminant.
- **`pxsl_sum_matrix(A, B, s='+')`** → détail case par case de `A±B`.
- **`pxsl_prod_scalar_matrix(lamb, A, mult='times')`** → détail de `λ·A`.
- **`pxsl_prod_matrix(A, B, mult='times')`** → détail du produit `A·B`.
- **`pxsl_ax(a, x=Symbol('x'), sign=' ', frac=True)`** → `ax` en gérant `a=0/1/−1` ; `x` symbole quelconque (`L_{1}`).
- **`pxsl_system_lin(A, B, x='x')`** → système `Ax=B` en forme accolade.
- **`pxsl_double_matrix(A, B, opt='sep')`** → `A` et `B` côte à côte (`'sep'`) ou matrice augmentée (`'ext'`).
- **`pxsl_lines_op(n, listOp, opt='sys')`** → opération `L_{i} ← a·L_{i}+b·L_{j}` depuis `listOp=[a,i,b,j]`.
- **`pxsl_resol_system(listA, listB=[], listOp=[], x='x', method='sys', view='sep')`** → chaque étape d'une élimination (`method` : `'sys'`/`'mat'`/`'ech'`).
- **`pxs_steps_invert_matrix(A, B, method='sys')`** → résolution de système (`B`) ou **inversion** (`B=eye(n)`, `method='mat'`), rédaction LaTeX complète.
- **`pxs_compute_ech(A)` / `pxs_compute_ech_reduite(A)`** → forme échelonnée / **RREF** avec étapes en LaTeX. (Équivalents de `pxs_construct_RREF`.)
- **`pxs_system_simpl(n=3, opt='sys', max_coef=2, limit_sum=15)`** → génère `(A, B)` d'un système `Ax=B` à solution entière simple.
- **`pxs_commute_matrix(n, opt='')`** → `(A,B)` qui commutent et `(A,C)` qui non.
- **`pxsl_pow_matrix(A, k)`** → chaque coefficient élevé à la puissance `k`.
- **`pxs_invertible_matrix(n)`** / **`pxs_diag_matrix(p, a, b)`** / **`randmatrixrect(p, q, a, b)`** → matrice inversible / diagonale / rectangulaire aléatoire (coeffs entiers).

## 7. Probabilités — variables aléatoires finies  (`Mes_fctions_probabilistes_bis.py`)

> v.a. finies SymPy (`stats.FiniteRV`). `pxsl_*` affichent ; `pxs_*` construisent.

- **`pxs_finiterv(x, val, prob)`** → v.a. `x` de valeurs `val` et probas `prob`. Ex. `X = pxs_finiterv('X', [0,1,2], [Rational(1,4),Rational(1,2),Rational(1,4)])`.
- **`pxsl_law(textx, textprob, X, frac='', nzero=True)`** → tableau de loi (valeurs / probas) en LaTeX. `textx`/`textprob` = en-têtes.
- **`pxsl_moment(X, n=1, prod='times')`** → calcul détaillé de `E[Xⁿ]` (espérance/variance).
- **`pxsl_scalar_product(a, b, prod='times')`** → calcul de `a·b = Σ aᵢbᵢ`.
- **`pxs_simul_law(n, type_proba='dec', prec=0.01)`** → simule une loi discrète de taille n.
- **`pxs_fct_finiterv(f, X)`** → v.a. `Y = f(X)`. Ex. `Y = pxs_fct_finiterv(lambda t: t**2, X)`.
- **`pxsl_res_num(x, dec=4, pourc=False, text=False, egal=True, dot=True)`** → résultat numérique (`= 0,2354`, `23,54 %`). `egal=False` retire le préfixe.
- **`pxsl_sum_vector(x)`** → `Σ xᵢ` en LaTeX.
- **`pxs_nvirgzero(x)`** → supprime `.0` d'un float entier (tolérance 1e-10).
- **`pxsl_pow(...)`** aussi présent ici (identique à §6).

## 8. Utilitaires complémentaires (présence runtime à vérifier)

⚠️ NON présents dans le corpus embarqué — ne les utiliser que si la plateforme
les charge au runtime (sinon coder l'équivalent à la main) :
- **`indi_l_r_symb(l, alpha, beta, r)`** → fonction indicatrice symbolique `1_{[α,β]}`. `f = indi_l_r_symb('[',0,1,']'); f(x)`.
- **`pxs_round(x, ndigits=0)`** → arrondi « calculatrice » (half-up, pas banker's). `pxs_round(0.125,2)`→`0.13`.
- **`Poly_with_random_coef(symbol, deg, constant_coef)`** → polynôme aléatoire (coeffs `[-9,9]`) + LaTeX croissant/décroissant.

## 3. Primitives plateforme (référencées, non dans ces modules)

- **`{{ var }}`** — interpolation MyST (un nom de variable nu, voir règles).
- **`myst(...)`** — rendu plateforme (stubbé en local). Les `\fr{}\en{}` legacy ne
  rendent pas → utiliser `` {fr}`…`{en}`…` ``.
- **`pxsl_mat(...)`** — alias plateforme ; équivalent présent = **`pxsl_matrix`**.
- **`pxs_Interval(...)`** — affichage d'intervalle (présent dans Classes_Extensions.py).
