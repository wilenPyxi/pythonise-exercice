`````{exercise}
:title: {fr}`Équations exponentielles et logarithmiques`{en}`Exponential and Logarithmic Equations`
:modules: 
:recommendedExecutionTime: 15
:level: Elementary
:chap: chap_expLogFunctions_solvingExpLogEquations_ESCP
:involvedConcepts: Domain_of_function, solving_equ_with_ln, propers_of_log_and_exp
:originalSource: % Exercise source
:visibility: All
:comment: % Exercise comment (optional)
:originalExerciseId: b41f6b56-65a4-11f1-a8a1-0ed8d3b012a9
:id: 91f28cdc-74bf-11f1-a8a1-0ed8d3b012a9

```{python}
import random as rd
from sympy import Symbol, Rational, ln, exp, latex, simplify
from pyxiscience.Mes_fctions_generalistes_bis import pxs_config, pxsl_latex_coefficient as lc
config_standard = pxs_config()

# ═══════════════════════════════════════════════════════════════════════════
# MÉTHODE CONSTRUCTIVE — partir de la réponse
# ═══════════════════════════════════════════════════════════════════════════

# Question 1 : e^x = a1
# Réponse : x = ln(a1) avec a1 > 0, a1 ≠ 1
# On tire d'abord la réponse (ln(a1)), puis on fabrique l'énoncé (e^x = a1)
a1 = rd.choice([i for i in range(2, 11) if i != 1])
sol1 = ln(a1)
sol1Aff = latex(sol1, **config_standard)
a1Aff = latex(a1, **config_standard)

# Question 2 : e^(coef_exp·x) = a2
# Réponse : x = ln(a2)/coef_exp avec a2 > 0, a2 ≠ 1, coef_exp ≥ 2
# On tire d'abord coef_exp et a2, puis on calcule la réponse
coefExp = rd.randint(2, 5)
a2 = rd.choice([i for i in range(2, 11) if i != 1])
sol2 = ln(a2) / coefExp
sol2Aff = latex(sol2, **config_standard)
a2Aff = latex(a2, **config_standard)
coefExpAff = latex(coefExp, **config_standard)

# Affichage de l'exposant dans l'énoncé (2x, 3x, etc.)
x = Symbol('x')
expExprAff = latex(coefExp * x, **config_standard)

globals()
```

{fr}`Résoudre dans`{en}`Solve in` $\mathbb{R}$ {fr}`les équations suivantes :`{en}`the following equations:`

:::::{question}
:questionType: FGQ
:solution: [["ord","${{ sol1Aff }}$"],["0"]]

::::{questionStatement}
$e^x = {{ a1Aff }}$

$x =$ {input}`||150`
::::

::::{questionHint}
{fr}`Appliquer l'équivalence fondamentale entre exponentielle et logarithme.`{en}`Apply the fundamental equivalence between exponential and logarithm.`
::::

::::{displayedSolution}
$x = {{ sol1Aff }}$
::::

::::{detailedSolution}
{fr}`On rappelle l'équivalence fondamentale : pour tout`{en}`Recall the fundamental equivalence: for all` $x \in \mathbb{R}$ {fr}`et tout`{en}`and all` $y > 0$,

\begin{equation*}
e^x = y \iff x = \ln y.
\end{equation*}

{fr}`De même, pour`{en}`Similarly, for` $u > 0$ : $\ln u = k \iff u = e^k$.

{fr}`L'équation`{en}`The equation` $e^x = {{ a1Aff }}$ {fr}`est définie pour tout`{en}`is defined for all` $x \in \mathbb{R}$. {fr}`Par l'équivalence fondamentale :`{en}`By the fundamental equivalence:`

\begin{equation*}
e^x = {{ a1Aff }} \iff x = \ln {{ a1Aff }}.
\end{equation*}

{fr}`La solution est`{en}`The solution is` $x = {{ sol1Aff }}$.
::::

::::{weightDistribution}
:reasoning: 20
:logic: 30
:abstraction: 20
:calculation: 30
::::
:::::

:::::{question}
:questionType: FGQ
:solution: [["ord","${{ sol2Aff }}$"],["0"]]

::::{questionStatement}
$e^{ {{ expExprAff }} } = {{ a2Aff }}$

$x =$ {input}`||150`
::::

::::{questionHint}
{fr}`Isoler l'exposant en appliquant le logarithme népérien des deux côtés, puis diviser par le coefficient de`{en}`Isolate the exponent by applying the natural logarithm to both sides, then divide by the coefficient of` $x$.
::::

::::{displayedSolution}
$x = {{ sol2Aff }}$
::::

::::{detailedSolution}
{fr}`L'équation`{en}`The equation` $e^{ {{ expExprAff }} } = {{ a2Aff }}$ {fr}`est définie pour tout`{en}`is defined for all` $x \in \mathbb{R}$. {fr}`On applique l'équivalence fondamentale :`{en}`We apply the fundamental equivalence:`

\begin{equation*}
e^{ {{ expExprAff }} } = {{ a2Aff }} &\iff {{ expExprAff }} = \ln {{ a2Aff }} \\
&\iff x = \dfrac{\ln {{ a2Aff }} }{ {{ coefExpAff }} }.
\end{equation*}

{fr}`La solution est`{en}`The solution is` $x = {{ sol2Aff }}$.
::::

::::{weightDistribution}
:reasoning: 25
:logic: 25
:abstraction: 20
:calculation: 30
::::
:::::

```{python}
import random as rd
from sympy import Symbol, Rational, ln, exp, latex, simplify
from pyxiscience.Mes_fctions_generalistes_bis import pxs_config, pxsl_latex_coefficient as lc
config_standard = pxs_config()

# ═══════════════════════════════════════════════════════════════════════════
# MÉTHODE CONSTRUCTIVE — partir de la réponse
# ═══════════════════════════════════════════════════════════════════════════

# Question 3 : ln(x) = k
# Réponse : x = e^k avec k entier ≥ 2
# On tire d'abord k (qui détermine la réponse), puis on fabrique l'énoncé
k = rd.randint(2, 6)
sol3 = exp(k)
sol3Aff = latex(sol3, **config_standard)
kAff = latex(k, **config_standard)

# Question 4 : ln(coefLn·x - constLn) = valLn
# Réponse : x = (e^valLn + constLn) / coefLn
# On tire d'abord coefLn, valLn, puis constLn tel que la solution soit > constLn/coefLn
# (pour garantir le domaine de définition)
coefLn = rd.randint(2, 5)
valLn = rd.choice([0, 1, -1])
# Pour que x > constLn/coefLn, on tire constLn puis on vérifie que la solution construite
# satisfait automatiquement cette condition (construction directe)
# Solution : x = (e^valLn + constLn) / coefLn
# Domaine : coefLn·x - constLn > 0 ⟺ x > constLn/coefLn
# On choisit constLn < coefLn·e^valLn pour garantir que la solution est dans le domaine
constLn = rd.randint(1, min(4, coefLn - 1))

# Calcul de la solution
sol4Num = exp(valLn) + constLn
sol4Den = coefLn
# Simplification si possible
from math import gcd
g = gcd(int(sol4Num) if sol4Num == int(sol4Num) else 1, sol4Den)
sol4NumSimp = sol4Num / g
sol4DenSimp = sol4Den / g

# Calcul de la borne du domaine
borneNum = constLn
borneDen = coefLn
gBorne = gcd(borneNum, borneDen)
borneNumSimp = borneNum // gBorne
borneDenSimp = borneDen // gBorne

# Affichage de la borne du domaine
if borneDenSimp == 1:
    borneAff = latex(borneNumSimp, **config_standard)
else:
    borneAff = latex(Rational(borneNumSimp, borneDenSimp), **config_standard)

# Affichage de la solution
if valLn == 0:
    # e^0 = 1, donc solution = (1 + constLn) / coefLn
    solNum = 1 + constLn
    gSol = gcd(solNum, coefLn)
    solNumFinal = solNum // gSol
    solDenFinal = coefLn // gSol
    if solDenFinal == 1:
        sol4Aff = latex(solNumFinal, **config_standard)
    else:
        sol4Aff = latex(Rational(solNumFinal, solDenFinal), **config_standard)
else:
    # Solution générale avec e^valLn
    sol4Aff = r"\dfrac{e^{" + latex(valLn, **config_standard) + r"} + " + latex(constLn, **config_standard) + r"}{" + latex(coefLn, **config_standard) + r"}"

# Affichage de l'argument du logarithme
x = Symbol('x')
argLn = coefLn * x - constLn
argLnAff = latex(argLn, **config_standard)

# Affichage de valLn
valLnAff = latex(valLn, **config_standard)

# Affichage des étapes intermédiaires pour la solution 4
# Étape 1 : coefLn·x - constLn = e^valLn
if valLn == 0:
    etape1Aff = latex(coefLn, **config_standard) + r" x - " + latex(constLn, **config_standard) + r" = 1"
else:
    etape1Aff = latex(coefLn, **config_standard) + r" x - " + latex(constLn, **config_standard) + r" = e^{" + latex(valLn, **config_standard) + r"}"

# Étape 2 : coefLn·x = e^valLn + constLn
if valLn == 0:
    etape2Aff = latex(coefLn, **config_standard) + r" x = " + latex(1 + constLn, **config_standard)
else:
    etape2Aff = latex(coefLn, **config_standard) + r" x = e^{" + latex(valLn, **config_standard) + r"} + " + latex(constLn, **config_standard)

# Affichage de coefLn pour l'inégalité du domaine
coefLnAff = latex(coefLn, **config_standard)
constLnAff = latex(constLn, **config_standard)

globals()
```

:::::{question}
:questionType: FGQ
:solution: [["ord","${{ sol3Aff }}$"],["0"]]

::::{questionStatement}
$\ln x = {{ kAff }}$  {fr}`(on précisera le domaine de définition)`{en}`(specify the domain of definition)`

$x =$ {input}`||150`
::::

::::{questionHint}
{fr}`Utiliser la définition du logarithme népérien comme réciproque de la fonction exponentielle.`{en}`Use the definition of the natural logarithm as the inverse of the exponential function.`
::::

::::{displayedSolution}
$x = {{ sol3Aff }}$
::::

::::{detailedSolution}
{fr}`La fonction`{en}`The function` $\ln$ {fr}`est définie sur`{en}`is defined on` $\mathbb{R}_{+}^{*}$, {fr}`donc l'équation`{en}`so the equation` $\ln x = {{ kAff }}$ {fr}`impose`{en}`requires` $x > 0$. {fr}`Par définition du logarithme comme réciproque de l'exponentielle :`{en}`By definition of the logarithm as the inverse of the exponential:`

\begin{equation*}
\ln x = {{ kAff }} \iff x = {{ sol3Aff }}.
\end{equation*}

{fr}`La solution est`{en}`The solution is` $x = {{ sol3Aff }}$.
::::

::::{weightDistribution}
:reasoning: 20
:logic: 30
:abstraction: 25
:calculation: 25
::::
:::::

:::::{question}
:questionType: FGQ
:solution: [["ord","${{ sol4Aff }}$"],["0"]]

::::{questionStatement}
$\ln({{ argLnAff }}) = {{ valLnAff }}$  {fr}`(on précisera le domaine de définition)`{en}`(specify the domain of definition)`

$x =$ {input}`||200`
::::

::::{questionHint}
{fr}`Déterminer le domaine de définition en résolvant une inégalité, puis appliquer l'exponentielle aux deux membres pour éliminer le logarithme.`{en}`Determine the domain of definition by solving an inequality, then apply the exponential to both sides to eliminate the logarithm.`
::::

::::{displayedSolution}
$x = {{ sol4Aff }}$
::::

::::{detailedSolution}
{fr}`La fonction`{en}`The function` $\ln({{ argLnAff }})$ {fr}`est définie si et seulement si`{en}`is defined if and only if` ${{ argLnAff }} > 0$, {fr}`c'est-à-dire`{en}`that is` ${{ coefLnAff }} x > {{ constLnAff }}$, {fr}`soit`{en}`i.e.` $x > {{ borneAff }}$. {fr}`Sur ce domaine :`{en}`On this domain:`

\begin{equation*}
\ln({{ argLnAff }}) = {{ valLnAff }} &\iff {{ etape1Aff }} \\
&\iff {{ etape2Aff }} \\
&\iff x = {{ sol4Aff }}.
\end{equation*}

{fr}`On vérifie que`{en}`We verify that` $\ds {{ sol4Aff }} > {{ borneAff }}$ : {fr}`la condition de domaine est bien satisfaite. La solution est`{en}`the domain condition is indeed satisfied. The solution is` $x = {{ sol4Aff }}$.
::::

::::{weightDistribution}
:reasoning: 30
:logic: 25
:abstraction: 25
:calculation: 20
::::
:::::

`````