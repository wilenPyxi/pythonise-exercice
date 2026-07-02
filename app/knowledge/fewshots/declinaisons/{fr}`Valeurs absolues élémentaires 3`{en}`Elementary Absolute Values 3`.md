`````{exercise}
:id: 9af8828d-70a7-11f1-a8a1-0ed8d3b012a9
:originalExerciseId: 2ce83c2b-68cc-11f1-a8a1-0ed8d3b012a9
:title: {fr}`Valeurs absolues élémentaires 3`{en}`Elementary Absolute Values 3`
:modules: fund_of_math_I_ESCP
:recommendedExecutionTime: 5
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
:questionId: 6
:questionIndex: 6
:solution: [["ord","${{ -e7 }}$","${{ e7 }}$"],["0","0"]]

::::{questionStatement}
\begin{equation*}
|x| < {{ e7 }}
\end{equation*}

{fr}`Compléter l'encadrement donnant l'ensemble des solutions :` {en}`Complete the bounds giving the solution set:`\
\
{input}`||80` $< x <$ {input}`||80`
::::

::::{questionHint}
{fr}`$|x|<a$ signifie que $x$ se trouve strictement entre $-a$ et $a$.`{en}`$|x|<a$ means $x$ lies strictly between $-a$ and $a$.`
::::

::::{displayedSolution}
$-{{ e7 }} < x < {{ e7 }}$
::::

::::{detailedSolution}
{fr}`L'inéquation`{en}`The inequality` $|x| < {{ e7 }}$ {fr}`signifie que`{en}`states that` $x$ {fr}`se trouve strictement entre`{en}`lies strictly between` $-{{ e7 }}$ {fr}`et`{en}`and` ${{ e7 }}$.\
{fr}`Ainsi`{en}`Thus`

\begin{equation*}
-{{ e7 }} < x < {{ e7 }}.
\end{equation*}
::::

::::{weightDistribution}
:reasoning: 30
:logic: 30
:abstraction: 30
:calculation: 10
::::
:::::

:::::{question}
:questionType: FGQ
:questionId: 7
:questionIndex: 7
:solution: [["ord","${{ -e8 }}$","${{ e8 }}$"],["0","0"]]

::::{questionStatement}
\begin{equation*}
|x| \leq {{ e8 }}
\end{equation*}

{fr}`Compléter l'encadrement donnant l'ensemble des solutions :` {en}`Complete the bounds giving the solution set:`\
\
{input}`||80` $\leq x \leq$ {input}`||80`
::::

::::{questionHint}
{fr}`$|x|\le a$ permet à $x$ d'être égal à $-a$ ou $a$.`{en}`$|x|\le a$ allows $x$ to equal $-a$ or $a$.`
::::

::::{displayedSolution}
$-{{ e8 }} \leq x \leq {{ e8 }}$
::::

::::{detailedSolution}
{fr}`L'inéquation large`{en}`The non-strict inequality` $|x| \leq {{ e8 }}$ {fr}`inclut les bornes, donc`{en}`includes the endpoints, hence`

\begin{equation*}
-{{ e8 }} \leq x \leq {{ e8 }}.
\end{equation*}
::::

::::{weightDistribution}
:reasoning: 30
:logic: 30
:abstraction: 30
:calculation: 10
::::
:::::


`````