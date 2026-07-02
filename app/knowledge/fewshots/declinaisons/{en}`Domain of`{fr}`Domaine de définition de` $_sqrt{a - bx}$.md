`````{exercise}
:originalExerciseId: e8559359-32c0-4394-94be-daf9a701cb6a
:title: {en}`Domain of`{fr}`Domaine de définition de` $\sqrt{a - bx}$
:modules: Analyse_I_EFREI, Calc_1_Pyx
:recommendedExecutionTime: 0
:level: Elementary
:chap: chap_realFunctions_Graphs_functionsFundamentalDefinitions_ESCP, Second_chap_VIII, chap_I_fonction_reel_EFREI, Calculus_I_Functions_and_their_Representations_1_1
:involvedConcepts: 
:originalSource: Selin
:visibility: All
:variations: 
:comment: 
:id: 8f0a1b0c-709e-11f1-a8a1-0ed8d3b012a9

```{python}

import random as rd
from sympy import *
from pyxiscience.Mes_fctions_d_analyse import pxs_config
from pyxiscience.Classes_Extensions import pxs_Interval

config_standard = pxs_config()

import random as rd

x = symbols('x')
a, b = rd.sample(range(1, 10), 2)

arg = a - b*x
f = sqrt(arg)

domaine = pxs_Interval(-oo, Rational(a,b), True, False)

# === Ajouts conversion FGQ ===
borne = latex(Rational(a, b))
```

:::::{question}
:questionType: FGQ
:solution: [["ord","${{ borne }}$"],["0.000001"]]

::::{questionStatement}
{en}`Find the domain of the function`{fr}`Trouver le domaine de définition de la fonction` $f(x) = {{ latex(f) }}$. {en}`Its domain is an interval of the form`{fr}`Son domaine de définition est un intervalle de la forme` $(-\infty,\ \alpha]$. {en}`Give the value of`{fr}`Donner la valeur de` $\alpha$ :

$\alpha =$ {input}`||120`
::::

::::{questionHint}
{en}`A square root is defined only when its radicand is nonnegative. Start by solving`{fr}`Une racine carrée est définie seulement lorsque son radical est positif ou nul. Commencez par résoudre` ${{ latex(arg) }} \ge 0$.
::::

::::{displayedSolution}
$\alpha = {{ borne }}$
::::

::::{detailedSolution}

{en}`For the square root to be defined,`{fr}`Pour que la racine carrée soit définie, il faut que` ${{ latex(arg) }}\geq 0$. {en}`Solving for $x$ gives`{fr}`En résolvant l'inéquation, nous obtenons` ${{ a }} \geq {{ latex(b*x) }}$, {en}`or`{fr}`ou` $x \leq {{ latex(Rational(a,b)) }}$. 
\begin{equation*}
\boxed{
\text{{en}`Domain:`{fr}`Domaine :` }{{ domaine.print() }}}.
\end{equation*}

::::

::::{weightDistribution}
:reasoning: 30
:logic: 25
:abstraction: 30
:calculation: 15
::::
:::::
`````
