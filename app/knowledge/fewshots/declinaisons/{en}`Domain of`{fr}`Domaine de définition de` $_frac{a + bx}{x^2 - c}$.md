`````{exercise}
:originalExerciseId: 22d960b8-d57e-46d2-8ebd-09d8bed0a1fb
:title: {en}`Domain of`{fr}`Domaine de définition de` $\frac{a + bx}{x^2 - c}$
:modules: Analyse_I_EFREI, Calc_1_Pyx
:recommendedExecutionTime: 0
:level: Elementary
:chap: chap_realFunctions_Graphs_functionsFundamentalDefinitions_ESCP, Second_chap_VIII, chap_I_fonction_reel_EFREI, Calculus_I_Functions_and_their_Representations_1_1
:involvedConcepts: 
:originalSource: Selin
:visibility: All
:variations: 
:comment: 
:id: 91465036-709e-11f1-a8a1-0ed8d3b012a9

```{python}

import random as rd
from sympy import *
from pyxiscience.Mes_fctions_d_analyse import pxs_config

from pyxiscience.Classes_Extensions import pxs_Interval

config_standard = pxs_config()

import random as rd

x = symbols('x')
a, b, c = rd.sample(range(1, 10), 3)


f_num = (a*x+b)
f_den =(x**2 - c)
f = f_num/f_den
domaine1 = pxs_Interval(-oo, -sqrt(c), True, True)
domaine2 = pxs_Interval(sqrt(c), +oo, True, True)

# === Ajouts conversion FGQ ===
b_inf = latex(-sqrt(c))
b_sup = latex(sqrt(c))
```

:::::{question}
:questionType: FGQ
:solution: [["ord","${{ b_inf }}$","${{ b_sup }}$"],["0.000001","0.000001"]]

::::{questionStatement}
{en}`Find the domain of the function`{fr}`Donner le domaine de la fonction` 
\begin{equation*}
\ds f(x) = {{ latex(f, **config_standard) }}.
\end{equation*}
{en}`The function is defined for every real number except the two values that cancel the denominator. Give these two excluded values`{fr}`La fonction est définie pour tout réel sauf aux deux valeurs qui annulent le dénominateur. Donner ces deux valeurs exclues` $x_1 < x_2$ :

$x_1 =$ {input}`||120` {en}`and`{fr}`et` $x_2 =$ {input}`||120`
::::

::::{questionHint}
{en}`A rational function is defined whenever its denominator is not zero. Start by solving`{fr}`Une fonction rationnelle est définie lorsque son dénominateur n’est pas nul. Commencez par résoudre` $x^2-c=0$.
::::

::::{displayedSolution}
$x_1 = {{ b_inf }}$ {en}`and`{fr}`et` $x_2 = {{ b_sup }}$
::::

::::{detailedSolution}

{en}`The denominator cannot be zero, therefore:`{fr}`Le dénominateur doit être différent de zéro :` 
\begin{equation*}
{{ latex(f_den, **config_standard) }}\neq 0 \implies x \neq \pm {{ latex(sqrt(c)) }}.
\end{equation*}
{en}`Thus we have`{fr}`On a donc`
\begin{equation*}
\boxed{
\text{{en}`Domain:`{fr}`Domaine de définition :` }{{ domaine1.print() }} \cup {{ domaine2.print() }}}.
\end{equation*}
::::

::::{weightDistribution}
:reasoning: 20
:logic: 35
:abstraction: 30
:calculation: 15
::::
:::::
`````
