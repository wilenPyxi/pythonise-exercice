`````{exercise}
:title: {fr}`Résolution de`{en}`Resolution of` $|ax+b| = k$ {fr}`avec`{en}`with` $k > 0$
:modules: 
:recommendedExecutionTime: 5
:level: Elementary
:chap: chap_equations_Inequalities_absoluteValue_ESCP
:involvedConcepts: Abs_Val, Simplifying_Algebraic_Expressions, Solving_equalities
:originalSource: Erwan Lamy, ESCP Business School
:visibility: All
:variations: 
:comment: Échauffement 2/10 — résolution d'une équation à valeur absolue, cas k > 0 (deux cas).
:id: dafee084-70aa-11f1-a8a1-0ed8d3b012a9
:originalExerciseId: 004ee5bb-634d-11f1-a8a1-0ed8d3b012a9

````{python}
import random as rd
from math import gcd
from sympy import Rational, latex
from pyxiscience.Mes_fctions_generalistes_bis import pxs_config, pxsl_latex_coefficient as lc
config_standard = pxs_config()

# Équation |b - a x| = k, k > 0.
#   Cas 1 : b - a x =  k  ->  x = (b - k)/a   (fraction irréductible, dénominateur >= 2)
#   Cas 2 : b - a x = -k  ->  x = (b + k)/a   (entier par construction)
for _ in range(200):
    a = rd.randint(2, 9)
    b = rd.randint(5, 15)
    k = rd.randint(2, min(10, b - 1))
    if (b + k) % a == 0 and (b - k) != 0 and gcd(b - k, a) == 1:
        break

sol1 = Rational(b - k, a)              # exact, irréductible, q >= 2
sol2 = (b + k) // a                    # entier

aAff = str(a)
bAff = str(b)
kAff = str(k)
negKAff = str(-k)
coefAff = lc(-a, sign=True)            # coefficient signé du terme en x : "- a"
sol1Aff = latex(sol1)                  # fraction irréductible
sol1NumAff = str(b - k)
sol1DenAff = str(a)
sol2Aff = str(sol2)
bPlusKAff = str(b + k)                 # = a * sol2
aTimesSol1Aff = str(b - k)             # a * sol1
bMinusASol2Aff = str(b - a * sol2)     # = -k

globals()
````

:::::{question}
:questionType: FGQ
:questionId: 0
:questionIndex: 0
:solution: [["notord","${{ sol1Aff }}$","${{ sol2Aff }}$"],["0","0"]]

::::{questionStatement}
{fr}`**Résolution d'une équation $|ax + b| = k$ avec $k > 0$.**` {en}`**Solving an equation $|ax + b| = k$ with $k > 0$.**`

{fr}`Résoudre l'équation suivante et donner ses deux solutions :` {en}`Solve the following equation and give its two solutions:`

\begin{equation*}
|{{ bAff }} {{ coefAff }}x| = {{ kAff }}.
\end{equation*}

$x =$ {input}`||120` {fr}`ou`{en}`or` $x =$ {input}`||120`
::::

::::{questionHint}
{fr}`Lorsque $k > 0$, l'équation $|f(x)| = k$ se scinde en deux cas : $f(x) = k$ ou $f(x) = -k$.`

{en}`When $k > 0$, the equation $|f(x)| = k$ splits into two cases: $f(x) = k$ or $f(x) = -k$.`
::::

::::{displayedSolution}
$\ds x = {{ sol1Aff }}$ {fr}`ou`{en}`or` $\ds x = {{ sol2Aff }}$
::::

::::{detailedSolution}
{fr}`L'équation proposée est $|{{bAff}} {{coefAff}}x| = {{kAff}}$ avec ${{kAff}} > 0$.`

{en}`The given equation is $|{{bAff}} {{coefAff}}x| = {{kAff}}$ with ${{kAff}} > 0$.`

{fr}`Par définition de la valeur absolue, cette équation se décompose en deux situations distinctes :`{en}`By definition of absolute value, this equation splits into two distinct cases:`

$\phantom{-}$

{fr}`$\bullet$ **Premier cas :** ${{bAff}} {{coefAff}}x = {{kAff}}$`

{en}`$\bullet$ **First case:** ${{bAff}} {{coefAff}}x = {{kAff}}$`

{fr}`On isole $x$ en regroupant les termes constants :`
{en}`We isolate $x$ by grouping the constant terms:`

\begin{equation*}
{{bAff}} {{coefAff}}x = {{kAff}} \quad &\Longleftrightarrow \quad {{aAff}}x = {{sol1NumAff}} \quad \\[6pt]
&\Longleftrightarrow \quad x = \frac{{{sol1NumAff}}}{{{sol1DenAff}}}.
\end{equation*}

{fr}`$\bullet$ **Deuxième cas :** ${{bAff}} {{coefAff}}x = {{negKAff}}$`

{en}`$\bullet$ **Second case:** ${{bAff}} {{coefAff}}x = {{negKAff}}$`

{fr}`On isole $x$ de la même façon :`
{en}`We isolate $x$ in the same way:`

\begin{equation*}
{{bAff}} {{coefAff}}x = {{negKAff}} \quad &\Longleftrightarrow \quad {{aAff}}x = {{bPlusKAff}} \quad \\[6pt]
&\Longleftrightarrow \quad x = {{sol2Aff}}.
\end{equation*}

{fr}`**Vérification des deux solutions.**`

{en}`**Verification of both solutions.**`

{fr}`Pour $x = \dfrac{{{sol1NumAff}}}{{{sol1DenAff}}}$ :`
{en}`For $x = \dfrac{{{sol1NumAff}}}{{{sol1DenAff}}}$:`

\begin{equation*}
\left|{{bAff}} {{coefAff}}\times\frac{{{sol1NumAff}}}{{{sol1DenAff}}}\right| &= \left|{{bAff}} - {{aAff}}\times\frac{{{sol1NumAff}}}{{{sol1DenAff}}}\right| \\[10pt]
&= \left|{{bAff}} - {{aTimesSol1Aff}}\right| \\[10pt]
&= {{kAff}}.
\end{equation*}

{fr}`Pour $x = {{sol2Aff}}$ :`
{en}`For $x = {{sol2Aff}}$:`

\begin{equation*}
\left|{{bAff}} {{coefAff}}\times{{sol2Aff}}\right| &= \left|{{bAff}} - {{aAff}}\times{{sol2Aff}}\right| \\[10pt]
&= \left|{{bMinusASol2Aff}}\right| \\[10pt]
&= {{kAff}}.
\end{equation*}

{fr}`Les deux valeurs vérifient l'équation initiale.`

{en}`Both values satisfy the original equation.`

{fr}`**Conclusion :** L'ensemble des solutions est $\boxed{\left\{\dfrac{{{sol1NumAff}}}{{{sol1DenAff}}},\, {{sol2Aff}}\right\}}$.`

{en}`**Conclusion:** The solution set is $\boxed{\left\{\dfrac{{{sol1NumAff}}}{{{sol1DenAff}}},\, {{sol2Aff}}\right\}}$.`
::::

::::{weightDistribution}
:logic: 10
:abstraction: 15
:reasoning: 25
:calculation: 50
::::
:::::

`````