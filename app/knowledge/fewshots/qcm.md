`````{exercise}
:id:
:title: {fr}`Exemple QCM — dérivée d'un monôme`{en}`MCQ example — derivative of a monomial`
:modules:
:recommendedExecutionTime: 3
:level: Elementary
:chap:
:involvedConcepts:
:originalSource:
:visibility: All

````{python}
import random as rd
from sympy import symbols, diff, latex
x = symbols('x')

a = rd.randint(2, 9)          # coefficient (>= 2, jamais 1)
n = rd.choice([k for k in range(2, 7) if k != a])   # exposant >= 2, ET n != a
f  = a*x**n
fp = diff(f, x)               # bonne réponse : n a x^(n-1)

fAff       = latex(f)
correctAff = latex(fp)
d1Aff = latex(a*x**(n-1))     # oubli du facteur n (dérivée)
d2Aff = latex(a*n*x**n)       # exposant non décrémenté
d3Aff = latex(n*x**(n-1))     # oubli du coefficient a
# distincts par construction : a != n garantit d1 != d3 (sinon a x^(n-1) == n x^(n-1)),
# a,n >= 2 garantit correct != d1/d2/d3 — collision impossible sur toute graine.

globals()
````

{fr}`Soit la fonction`{en}`Let the function` $f(x) = {{fAff}}$.

:::::{question}
:questionType: MCQ
:questionId: 0
:questionIndex: 0

::::{questionStatement}
{fr}`Quelle est la dérivée`{en}`What is the derivative` $f'(x)$ ?
::::

::::{questionHint}
{fr}`Règle de la puissance :`{en}`Power rule:` $\dfrac{d}{dx}\left(x^{p}\right) = p\,x^{p-1}$.
::::

::::{mcqAnswer}
:isRightAnswer: true
$f'(x) = {{correctAff}}$
::::

::::{mcqAnswer}
:isRightAnswer: false
$f'(x) = {{d1Aff}}$
::::

::::{mcqAnswer}
:isRightAnswer: false
$f'(x) = {{d2Aff}}$
::::

::::{mcqAnswer}
:isRightAnswer: false
$f'(x) = {{d3Aff}}$
::::

::::{mcqAnswer}
:isRightAnswer: false
{fr}`Aucune de ces réponses n'est correcte`{en}`None of these answers are correct`
::::

::::{detailedSolution}
{fr}`Par la règle de la puissance,`{en}`By the power rule,` $\dfrac{d}{dx}\left(a x^{n}\right) = n\,a\,x^{n-1}$, {fr}`donc`{en}`so` $f'(x) = {{correctAff}}$.
::::

::::{weightDistribution}
:logic: 20
:abstraction: 20
:reasoning: 20
:calculation: 40
::::
:::::

`````
