`````{exercise}
:id: 73dd633c-70a7-11f1-a8a1-0ed8d3b012a9
:originalExerciseId: d140e232-68cb-11f1-a8a1-0ed8d3b012a9
:title: {fr}`Valeurs absolues élémentaires 2`{en}`Elementary Absolute Values 2`
:modules: fund_of_math_I_ESCP
:recommendedExecutionTime: 20
:level: Elementary
:chap: chap_equations_Inequalities_absoluteValue_ESCP
:involvedConcepts: Abs_Val
:originalSource: ESCP
:visibility: All
:variations: 
:comment: 

```{python}

import random as rd
from sympy import *
from pyxiscience.Mes_fctions_generalistes_bis import pxs_config
from pyxiscience.Classes_Extensions import pxs_Interval
from pyxiscience.Mes_fctions_d_analyse import pxsl_pow
from pyxiscience.Mes_fctions_generalistes_bis import pxsl_latex_avec_formatage
from pyxiscience.Mes_fctions_probabilistes_bis import pxsl_res_num

from pyxiscience.Mes_fctions_generalistes_bis import  pxs_config

config_standard = pxs_config()

n, x, u = symbols('n x u')

e1 = rd.randint(-10,-1)

e2 = rd.randint(1,11)

e31, e32 = rd.randint(1,11), rd.randint(-10,-1)
e3 = Add(e31, e32, evaluate = False)
e3_eval = Add(e31, e32, evaluate = True)

e41 = rd.randint(1,11)
e42 = rd.randint(-10,-1)
e43 = rd.randint(2, 11)
e4 = Mul(Rational(1,e43), Add(e41, e42, evaluate = False), evaluate = False) 
e4_eval = Mul(Rational(1,e43), Add(e41, e42, evaluate = True), evaluate = True) 

e51 = rd.choice([3, 5, 7])
e52 = rd.choice([-2, -4, -8])
e5 = Mul(e51, Rational(e52, e51), evaluate = False)
e5_eval = Mul(e51, Rational(e52, e51), evaluate = True)

e611, e612 = rd.randint(1,11), rd.randint(-10,-1)
e61 = Add(e611, e612, evaluate = False)
e621, e622 = rd.randint(1,11), rd.randint(-10,-1)
e62 = Add(e621, e622, evaluate = False)
e61_eval = Add(e611, e612, evaluate = True)
e62_eval = Add(e621, e622, evaluate = True)

e7 = rd.randint(1,11)

e8 = rd.randint(1,11)

a9 = rd.choice([2, 3, 5])
if a9 == 2:
    b9 = rd.choice([5, 7, 10])
elif a9 == 3:
    b9 = rd.choice([10, 11, 13])
else:
    b9 = rd.choice([26, 29, 31])

a9, b9 = Min(a9, b9), Max(a9, b9)
e9 = a9 - sqrt(b9)

a10, b10 = Max(a9, b9), Min(a9, b9)
e10 = sqrt(b10) - a10

```

{en}`Evaluate the absolute value expressions:`{fr}`Evaluer les valeurs abolues suivantes :`



:::::{question}
:questionType: FGQ
:questionId: 5
:questionIndex: 5
:solution: [["ord","${{ latex(Abs(e61_eval) - Abs(e62_eval)) }}$"],["0"]]

::::{questionStatement}
\begin{equation*}
\Big|{{ latex(e61) }}\Big| - \Big|{{ latex(e62) }}\Big| 
\end{equation*}

{fr}`Cette expression vaut :` {en}`This expression equals:` {input}`||120`
::::

::::{questionHint}
{fr}`Calculez chaque valeur absolue séparément avant de soustraire.`{en}`Compute each absolute value separately before subtracting.`
::::

::::{displayedSolution}
${{ latex(Abs(e61_eval) - Abs(e62_eval)) }}$
::::

::::{detailedSolution}
{fr}`On calcule chaque valeur absolue séparément :`{en}`Compute each absolute value separately:`

\begin{equation*}
|{{ latex(e61) }}| &= |{{ e61_eval }}| \\[6pt]
&= {{ Abs(e61_eval) }}
\end{equation*}

{fr}`et`{en}`and`

\begin{equation*}
|{{ latex(e62) }}| &= |{{ e62_eval }}| \\[6pt]
&= {{ Abs(e62_eval) }}.
\end{equation*}

{fr}`La soustraction donne`{en}`Subtracting gives`

\begin{equation*}
|{{ latex(e61) }}| - |{{ latex(e62) }}| &= {{ Abs(e61_eval) }} - {{ Abs(e62_eval) }} \\[6pt]
&={{ latex(Abs(e61_eval) - Abs(e62_eval)) }}.
\end{equation*}
::::

::::{weightDistribution}
:reasoning: 25
:logic: 25
:abstraction: 15
:calculation: 35
::::
:::::

:::::{question}
:questionType: FGQ
:questionId: 8
:questionIndex: 8
:solution: [["ord","${{ latex(Abs(e9)) }}$"],["0"]]

::::{questionStatement}
\begin{equation*}
|{{ latex(e9) }}|
\end{equation*}

{fr}`Cette expression vaut :` {en}`This expression equals:` {input}`||120`
::::

::::{questionHint}
{fr}`Comparez l'entier avec $\sqrt{b}$ pour déterminer le signe de l'expression à l'intérieur de la valeur absolue.`{en}`Compare the integer with $\sqrt{b}$ to decide the sign of the expression inside the absolute value.`
::::

::::{displayedSolution}
${{ latex(Abs(e9)) }}$
::::

::::{detailedSolution}
{fr}`L'expression à l'intérieur de la valeur absolue est`{en}`The expression inside the absolute value is` ${{ latex(e9) }}$.\
{fr}`Puisque`{en}`Since` ${{ a9 }} < \sqrt{{{ b9 }}}$, {fr}`la quantité`{en}`the quantity` ${{ latex(e9) }}$ {fr}`est négative.`{en}`is negative.`\
{fr}`Par conséquent`{en}`Therefore`

\begin{equation*}
|{{ latex(e9) }}| &= -\big({{ latex(e9) }}\big) \\[6pt]
&= {{ latex(Abs(e9)) }}.
\end{equation*}
::::

::::{weightDistribution}
:reasoning: 25
:logic: 25
:abstraction: 25
:calculation: 25
::::
:::::

:::::{question}
:questionType: FGQ
:questionId: 9
:questionIndex: 9
:solution: [["ord","${{ latex(Abs(e10)) }}$"],["0"]]

::::{questionStatement}
\begin{equation*}
|{{ latex(e10) }}|
\end{equation*}

{fr}`Cette expression vaut :` {en}`This expression equals:` {input}`||120`
::::

::::{questionHint}
{fr}`Déterminez si $\sqrt{b}$ est plus petit ou plus grand que l'entier devant lui.`{en}`Determine whether $\sqrt{b}$ is smaller or larger than the integer in front of it.`
::::

::::{displayedSolution}
${{ latex(Abs(e10)) }}$
::::

::::{detailedSolution}
{fr}`À l'intérieur de la valeur absolue on a`{en}`Inside the absolute value one has` ${{ latex(e10) }}$.\
{fr}`Puisque`{en}`Because` ${{ a10 }} > \sqrt{{{ b10 }}}$, {fr}`l'expression`{en}`the expression` ${{ latex(e10) }}$ {fr}`est négative.`{en}`is negative.`\
{fr}`En conséquence`{en}`Consequently`

\begin{equation*}
|{{ latex(e10) }}| &= -\big({{ latex(e10) }}\big) \\[6pt]
&= {{ latex(Abs(e10)) }}.
\end{equation*}
::::

::::{weightDistribution}
:reasoning: 25
:logic: 25
:abstraction: 25
:calculation: 25
::::
:::::
`````