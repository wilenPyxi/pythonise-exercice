`````{exercise}
:id: ff0cf9ac-7067-11f1-a8a1-0ed8d3b012a9
:originalExerciseId: dd834157-3f2f-11f1-a8a1-0ed8d3b012a9
:title: {fr}`Discontinuité d'une fraction rationnelle`{en}`Discontinuity of a Rational Fraction`
:modules: CalcI, Calc_1_Pyx
:recommendedExecutionTime: 5
:level: Intermediate
:chap: chap_limitsContinuity_continuity_ESCP, Calculus_I_Continuity_1_5
:involvedConcepts: Continuity_at_a_point, Domain_of_function, Rational_Function
:originalSource: Selin
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

x = symbols('x')
a,b,c,d = rd.sample(range(1, 11), 4)
p = rd.randint(2, 6)
q = Rational(1,rd.randint(2, 6))
f = 1/(a*x+b)

x0 = Rational(-b,a)

l = f.subs(x,x0)
```

:::::{question}
:questionType: MCQ

::::{questionStatement}
{fr}`Pour quelle raison la fonction`{en}`Why is the function` $\ds f(x) = {{latex(f)}}$ {fr}`est-elle discontinue en`{en}`discontinuous at` $\ds a = {{latex(x0)}}$ ?
::::

::::{questionHint}
{fr}`Évaluer le dénominateur de la fonction au point indiqué.`{en}`Evaluate the denominator of the function at the given point.`
::::

::::{mcqAnswer}
:isRightAnswer: true
{fr}`Car $\ds f\left({{latex(x0)}}\right)$ n'est pas définie : le dénominateur s'annule en $\ds {{latex(x0)}}$.`{en}`Because $\ds f\left({{latex(x0)}}\right)$ is undefined: the denominator vanishes at $\ds {{latex(x0)}}$.`
::::

::::{mcqAnswer}
:isRightAnswer: false
{fr}`Car le numérateur s'annule en $\ds {{latex(x0)}}$.`{en}`Because the numerator vanishes at $\ds {{latex(x0)}}$.`
::::

::::{mcqAnswer}
:isRightAnswer: false
{fr}`Car $\ds \lim_{x \to {{latex(x0)}}} f(x) = 0$.`{en}`Because $\ds \lim_{x \to {{latex(x0)}}} f(x) = 0$.`
::::

::::{mcqAnswer}
:isRightAnswer: false
{fr}`Car $f$ n'est pas dérivable en $\ds {{latex(x0)}}$, bien qu'elle y soit continue.`{en}`Because $f$ is not differentiable at $\ds {{latex(x0)}}$, although it is continuous there.`
::::

::::{detailedSolution}
{fr}`La fonction est discontinue en`{en}`The function is discontinuous at` $\ds a = {{latex(x0)}}$ {fr}`car`{en}`because` $\ds f\left({{latex(x0)}}\right)$ {fr}`n'est pas définie (le dénominateur devient zéro).`{en}`is undefined (the denominator becomes zero).`
::::

::::{weightDistribution}
:reasoning: 35
:logic: 25
:abstraction: 20
:calculation: 20
::::
:::::
`````
