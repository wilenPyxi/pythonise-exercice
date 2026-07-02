`````{exercise}
:id:
:title: {fr}`Exemple QAT — racines d'un trinôme`{en}`QAT example — roots of a quadratic`
:modules:
:recommendedExecutionTime: 4
:level: Elementary
:chap:
:involvedConcepts:
:originalSource:
:visibility: All

````{python}
import random as rd
from sympy import symbols, latex, Poly
x = symbols('x')

r1 = rd.randint(-6, -1)       # plus petite racine (entière)
r2 = rd.randint(1, 6)         # plus grande racine (entière)
p  = -(r1 + r2)
q  = r1*r2
polyAff = latex(Poly(x**2 + p*x + q, x).as_expr())
r1Aff, r2Aff = str(r1), str(r2)

globals()
````

:::::{question}
:questionType: FGQ
:questionId: 0
:questionIndex: 0
:solution: [["ord","${{r1Aff}}$","${{r2Aff}}$"],["0","0"]]

::::{questionStatement}
{fr}`Résoudre l'équation suivante, en donnant les racines de la plus petite à la plus grande :`{en}`Solve the following equation, giving the roots from smallest to largest:`
\begin{equation*}
{{polyAff}} = 0.
\end{equation*}

{fr}`Plus petite racine :`{en}`Smallest root:` {input}`||90` $\qquad$ {fr}`plus grande racine :`{en}`largest root:` {input}`||90`
::::

::::{questionHint}
{fr}`Cherchez deux entiers dont la somme et le produit correspondent aux coefficients.`{en}`Look for two integers whose sum and product match the coefficients.`
::::

::::{displayedSolution}
$x_1 = {{r1Aff}}$, $\quad x_2 = {{r2Aff}}$
::::

::::{detailedSolution}
{fr}`On factorise`{en}`Factoring` ${{polyAff}} = (x - ({{r1Aff}}))(x - ({{r2Aff}}))$, {fr}`d'où les racines`{en}`hence the roots` ${}{{r1Aff}}$ {fr}`et`{en}`and` ${}{{r2Aff}}$.
::::

::::{weightDistribution}
:logic: 15
:abstraction: 15
:reasoning: 20
:calculation: 50
::::
:::::

`````
