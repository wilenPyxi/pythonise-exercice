`````{exercise}
:id: c84654fa-70a6-11f1-a8a1-0ed8d3b012a9
:originalExerciseId: 834b79ee-fc00-47e7-921b-83e4524d24b0
:title: {fr}`Valeurs absolues élémentaires`{en}`Elementary Absolute Values`
:modules: fund_of_math_I_ESCP
:recommendedExecutionTime: 20
:level: Elementary
:chap: chap_equations_Inequalities_absoluteValue_ESCP
:involvedConcepts: Solving_inequalities, Abs_Val
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
:solution: [["ord","${{ Abs(e1) }}$"],["0"]]

::::{questionStatement}
\begin{equation*}
|{{ e1 }}|
\end{equation*}

{fr}`Cette expression vaut :` {en}`This expression equals:` {input}`||120`
::::

::::{questionHint}
{fr}`Rappel : la valeur absolue d'un nombre négatif est son opposé.`{en}`Remember: the absolute value of a negative number is its opposite.`
::::

::::{displayedSolution}
${{ Abs(e1) }}$
::::

::::{detailedSolution}
{fr}`La valeur absolue d'un nombre réel est sa distance à zéro sur la droite réelle, elle est donc toujours positive ou nulle.`{en}`The absolute value of a real number is its distance from zero on the real line, hence it is always non–negative.`\
{fr}`Puisque`{en}`Since` ${{e1}}$ {fr}`est négatif, on change son signe :`{en}`is negative, one changes its sign:`

\begin{equation*}
|{{e1}}| &= -({{e1}}) \\[6pt]
&=  {{ Abs(e1) }}.
\end{equation*}
::::

::::{weightDistribution}
:reasoning: 10
:logic: 20
:abstraction: 10
:calculation: 60
::::
:::::

:::::{question}
:questionType: FGQ
:solution: [["ord","${{ Abs(e2) }}$"],["0"]]

::::{questionStatement}
\begin{equation*}
|{{ e2 }}|
\end{equation*}

{fr}`Cette expression vaut :` {en}`This expression equals:` {input}`||120`
::::

::::{questionHint}
{fr}`La valeur absolue d'un nombre positif est le nombre lui-même.`{en}`The absolute value of a positive number is the number itself.`
::::

::::{displayedSolution}
${{ Abs(e2) }}$
::::

::::{detailedSolution}
{fr}`Le nombre`{en}`The number` ${{e2}}$ {fr}`est positif, donc sa valeur absolue est égale à lui-même :`{en}`is positive, therefore its absolute value equals itself:`

\begin{equation*}
|{{e2}}| = {{ Abs(e2) }}.
\end{equation*}
::::

::::{weightDistribution}
:reasoning: 10
:logic: 20
:abstraction: 10
:calculation: 60
::::
:::::

:::::{question}
:questionType: FGQ
:solution: [["ord","${{ Abs(e3) }}$"],["0"]]

::::{questionStatement}
\begin{equation*}
|{{ e3 }}|
\end{equation*}

{fr}`Cette expression vaut :` {en}`This expression equals:` {input}`||120`
::::

::::{questionHint}
{fr}`Additionnez d'abord les deux entiers, puis prenez la valeur absolue du résultat.`{en}`First add the two integers, then take the absolute value of the result.`
::::

::::{displayedSolution}
$\ds {{ Abs(e3) }}$
::::

::::{detailedSolution}
{fr}`On calcule d'abord la somme à l'intérieur de la valeur absolue :`{en}`First one computes the sum inside the absolute value:`

\begin{equation*}
{{ e3 }} = {{ e3_eval }}.
\end{equation*}

{fr}`La valeur absolue de ce résultat est donc`{en}`The absolute value of this result is therefore`

\begin{equation*}
\left|{{ e3_eval }}\right| = {{ Abs(e3) }}.
\end{equation*}
::::

::::{weightDistribution}
:reasoning: 15
:logic: 15
:abstraction: 15
:calculation: 55
::::
:::::

:::::{question}
:questionType: FGQ
:solution: [["ord","${{ latex(Abs(e4)) }}$"],["0"]]

::::{questionStatement}
\begin{equation*}
\left|{{ latex(e4) }}\right|
\end{equation*}

{fr}`Cette expression vaut :` {en}`This expression equals:` {input}`||120`
::::

::::{questionHint}
{fr}`Calculez la somme entre parenthèses avant de diviser par le dénominateur, puis appliquez la valeur absolue.`{en}`Compute the sum in parentheses before dividing by the denominator, then apply the absolute value.`
::::

::::{displayedSolution}
$\ds {{ latex(Abs(e4)) }}$
::::

::::{detailedSolution}
{fr}`On commence par évaluer l'expression à l'intérieur de la valeur absolue :`{en}`Begin by evaluating the expression inside the absolute value:`

\begin{equation*}
\frac{1}{{{ e43 }}}\big({{ e42 }}+{{ e41 }}\big) &= \frac{1}{{{ e43 }}}\cdot {{ pxsl_pow(e41+e42) }} \\[10pt]
&= {{ latex(e4_eval) }}.
\end{equation*}

{fr}`La valeur absolue est alors`{en}`The absolute value is then`

\begin{equation*}
\Big|\frac{1}{{{ e43 }}}\big({{ e42 }}+{{ e41 }}\big)\Big| &= \left|{{ latex(e4_eval) }}\right| \\[10pt]
&= {{ latex(Abs(e4)) }}.
\end{equation*}
::::

::::{weightDistribution}
:reasoning: 20
:logic: 20
:abstraction: 20
:calculation: 40
::::
:::::

:::::{question}
:questionType: FGQ
:solution: [["ord","${{ latex(Abs(e5)) }}$"],["0"]]

::::{questionStatement}
\begin{equation*}
\Big|{{ latex(e5) }}\Big|
\end{equation*}

{fr}`Cette expression vaut :` {en}`This expression equals:` {input}`||120`
::::

::::{questionHint}
{fr}`Le facteur commun au numérateur et au dénominateur se simplifie complètement.`{en}`The common factor in numerator and denominator cancels out completely.`
::::

::::{displayedSolution}
${{ latex(Abs(e5)) }}$
::::

::::{detailedSolution}
{fr}`La fraction se simplifie d'abord :`{en}`The fraction simplifies first:`

\begin{equation*}
\frac{{{ e51 }}\cdot {{ pxsl_pow(e52) }}}{{{ e51 }}} = {{ e5_eval }}.
\end{equation*}

{fr}`La valeur absolue devient donc`{en}`Hence the absolute value becomes`

\begin{equation*}
\Big|\frac{{{ e51 }}\cdot {{ pxsl_pow(e52) }}}{{{ e51 }}}\Big| &= \left|{{ e5_eval }}\right| \\[10pt]
&= {{ latex(Abs(e5)) }}.
\end{equation*}
::::

::::{weightDistribution}
:reasoning: 20
:logic: 20
:abstraction: 20
:calculation: 40
::::
:::::


`````