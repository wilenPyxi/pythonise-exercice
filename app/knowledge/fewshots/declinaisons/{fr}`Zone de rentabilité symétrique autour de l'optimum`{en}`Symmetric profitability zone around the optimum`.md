`````{exercise}
:title: {fr}`Zone de rentabilité symétrique autour de l'optimum`{en}`Symmetric profitability zone around the optimum`
:modules: 
:recommendedExecutionTime: 15
:level: Elementary
:chap: chap_realFunctions_Graphs_graphSymmetries_ESCP
:involvedConcepts: 
:originalSource: 
:visibility: All
:variations: 
:comment: Appliqué (économie & gestion) : axe de symétrie et maximum d'une parabole de profit, seuils de rentabilité par factorisation, et symétrie des seuils par rapport à l'optimum (sans discriminant ni Viète).
:id: df8f8e47-7480-11f1-a8a1-0ed8d3b012a9
:originalExerciseId: e1c9656e-6409-11f1-a8a1-0ed8d3b012a9

````{python}
import random as rd
from sympy import symbols, latex
from pyxiscience.Mes_fctions_generalistes_bis import pxs_config, pxsl_latex_coefficient as lc

config_standard = pxs_config()
q = symbols('q')

# qStar entier, q1 < qStar < q2 symétriques, a<0, racines q1,q2
# coefficient négatif
a = rd.choice([-5, -4, -3, -2, -1])

# choisir q_star directement compatible avec 20 <= b <= 60
# b = -2 a q_star
# donc q_star = b / (-2a)

possible_qstars = []

for q in range(3, 16):
    b = -2 * a * q
    if 20 <= b <= 60:
        possible_qstars.append(q)

qStar = rd.choice(possible_qstars)

# construction des racines symétriques
q1 = rd.randint(1, qStar - 2)
q2 = 2 * qStar - q1

# coefficients
b = -2 * a * qStar
c = a * q1 * q2

Pi = a*q**2 + b*q + c
profitMax = a * qStar**2 + b * qStar + c
somme_racines = q1 + q2
produit_racines = q1 * q2
factAff = f"(q-{q1})(q-{q2})"
distance = qStar - q1

# Rendus
aLcAff = lc(a)
aMulAff = lc(a, ones=True)
bSignAff = lc(b, sign=True)
cSignAff = lc(c, ones=True, sign=True)
twoAAff = latex(2*a)
aQStarSqAff = latex(a*qStar**2)
bQStarSignAff = lc(b*qStar, ones=True, sign=True)
sommeRacines = somme_racines
produitRacines = produit_racines
negSommeSignAff = lc(-somme_racines, sign=True)
produitSignAff = lc(produit_racines, ones=True, sign=True)
q1PlusQ2 = q1 + q2

globals()
````

{fr}`Une entreprise modélise son profit (en milliers d'euros) par`{en}`A company models its profit (in thousands of euros) by` $\Pi(q)={{ aLcAff }}q^2{{ bSignAff }}q{{ cSignAff }}$, $q\geq 0$ {fr}`(quantité en centaines d'unités).`{en}`(quantity in hundreds of units).`

:::::{question}
:questionType: FGQ
:solution: [["ord","${{ qStar }}$"],["0"]]
:questionId: 0
:questionIndex: 0

::::{questionStatement}
{fr}`Déterminer l'axe de symétrie`{en}`Determine the axis of symmetry` $q^*$ {fr}`de la parabole.`{en}`of the parabola.`

$q^* =$ {input}`||90`
::::

::::{questionHint}
{fr}`Appliquer`{en}`Apply` $q^*=-\dfrac{b}{2a}$ {fr}`avec`{en}`with` $a={{ a }}$, $b={{ b }}$.
::::

::::{displayedSolution}
$q^* = {{ qStar }}$
::::

::::{detailedSolution}
{fr}`Règle utilisée : axe de symétrie`{en}`Rule used: axis of symmetry` $q^*=-\dfrac{b}{2a}$.

\begin{equation*}
q^* &= -\frac{ {{ b }} }{2\times({{ a }})} \\
&= -\frac{ {{ b }} }{ {{ twoAAff }} } \\
&= {{ qStar }}.
\end{equation*}

{fr}`L'axe de symétrie est`{en}`The axis of symmetry is` $q={{ qStar }}$.
::::

::::{weightDistribution}
:logic: 15
:abstraction: 25
:reasoning: 30
:calculation: 30
::::
:::::

:::::{question}
:questionType: FGQ
:solution: [["ord","${{ profitMax }}$"],["0"]]
:questionId: 1
:questionIndex: 1

::::{questionStatement}
{fr}`Calculer le profit maximal`{en}`Calculate the maximum profit` $\Pi(q^*)$.

$\Pi(q^*) =$ {input}`||90`
::::

::::{questionHint}
{fr}`Substituer`{en}`Substitute` $q={{ qStar }}$ {fr}`dans`{en}`in` $\Pi(q)$ ; {fr}`comme`{en}`since` $a<0$, {fr}`c'est un maximum.`{en}`it is a maximum.`
::::

::::{displayedSolution}
$\Pi(q^*) = {{ profitMax }}$
::::

::::{detailedSolution}
{fr}`On évalue`{en}`We evaluate` $\Pi$ {fr}`au sommet.`{en}`at the vertex.`

\begin{equation*}
\Pi({{ qStar }}) &= {{ aMulAff }}\times {{ qStar }}^2 {{ bSignAff }}\times {{ qStar }} {{ cSignAff }} \\
&= {{ aQStarSqAff }} {{ bQStarSignAff }} {{ cSignAff }} \\
&= {{ profitMax }}.
\end{equation*}

{fr}`Le profit maximal est de`{en}`The maximum profit is` ${{ profitMax }}$ {fr}`milliers d'euros.`{en}`thousands of euros.`
::::

::::{weightDistribution}
:logic: 15
:abstraction: 25
:reasoning: 30
:calculation: 30
::::
:::::

:::::{question}
:questionType: FGQ
:solution: [["notord","${{ q1 }}$","${{ q2 }}$"],["0","0"]]
:questionId: 2
:questionIndex: 2

::::{questionStatement}
{fr}`Déterminer les deux seuils de rentabilité`{en}`Determine the two break-even thresholds` $q_1$ {fr}`et`{en}`and` $q_2$ ($\Pi(q)=0$) {fr}`par factorisation.`{en}`by factorization.`

$q_1 =$ {input}`||90` {fr}`et`{en}`and` $q_2 =$ {input}`||90`
::::

::::{questionHint}
{fr}`Diviser par`{en}`Divide by` ${{ a }}$ {fr}`pour obtenir`{en}`to obtain` $q^2{{ negSommeSignAff }}q{{ produitSignAff }}=0$, {fr}`puis factoriser (deux nombres de produit`{en}`then factor (two numbers with product` ${{ produitRacines }}$ {fr}`et de somme`{en}`and sum` ${{ sommeRacines }}$).
::::

::::{displayedSolution}
$q_1 = {{ q1 }}$ {fr}`et`{en}`and` $q_2 = {{ q2 }}$
::::

::::{detailedSolution}
{fr}`On résout`{en}`We solve` $\Pi(q)=0$ {fr}`par factorisation (sans discriminant).`{en}`by factorization (without discriminant).`

\begin{equation*}
{{ aLcAff }}q^2 {{ bSignAff }}q {{ cSignAff }} &= 0 \\
q^2 {{ negSommeSignAff }}q {{ produitSignAff }} &= 0 \\
{{ factAff }} &= 0.
\end{equation*}

\begin{equation*}
q_1 &= {{ q1 }} \quad\text{{fr}`et`{en}`and`}\quad q_2 = {{ q2 }}.
\end{equation*}
::::

::::{weightDistribution}
:logic: 20
:abstraction: 25
:reasoning: 30
:calculation: 25
::::
:::::

:::::{question}
:questionType: FGQ
:solution: [["ord","${{ qStar }}$"],["0"]]
:questionId: 3
:questionIndex: 3

::::{questionStatement}
{fr}`Montrer que`{en}`Show that` $q_1$ {fr}`et`{en}`and` $q_2$ {fr}`sont symétriques par rapport à`{en}`are symmetric with respect to` $q^*$, {fr}`puis interpréter : que peut-on dire de la zone de rentabilité de l'entreprise ?`{en}`then interpret: what can be said about the company's profitability zone?`

$\dfrac{q_1+q_2}{2} =$ {input}`||90`
::::

::::{questionHint}
{fr}`Calculer la moyenne`{en}`Calculate the average` $\dfrac{q_1+q_2}{2}$ {fr}`et la comparer à`{en}`and compare it to` $q^*$.
::::

::::{displayedSolution}
$\dfrac{q_1+q_2}{2} = {{ qStar }}$
::::

::::{detailedSolution}
{fr}`Règle utilisée : l'axe de symétrie d'une parabole passe par le milieu de ses deux zéros.`{en}`Rule used: the axis of symmetry of a parabola passes through the midpoint of its two zeros.`

\begin{equation*}
\frac{q_1 + q_2}{2} &= \frac{ {{ q1 }} + {{ q2 }} }{2} \\
&= \frac{ {{ q1PlusQ2 }} }{2} \\
&= {{ qStar }}.
\end{equation*}

{fr}`Les deux seuils sont symétriques par rapport à`{en}`The two thresholds are symmetric with respect to` $q^*={{ qStar }}$. {fr}`L'entreprise est rentable`{en}`The company is profitable` ($\Pi>0$) {fr}`pour`{en}`for` $q$ {fr}`entre`{en}`between` ${{ q1 }}$ {fr}`et`{en}`and` ${{ q2 }}$. {fr}`La zone de rentabilité est symétrique autour de l'optimum : les deux seuils sont à égale distance`{en}`The profitability zone is symmetric around the optimum: the two thresholds are at equal distance` (${{ distance }}$ {fr}`centaines d'unités) de la quantité optimale, donc l'entreprise dispose de la même marge de manœuvre en sous-production ou en surproduction.`{en}`hundreds of units) from the optimal quantity, so the company has the same margin of maneuver in underproduction or overproduction.`
::::

::::{weightDistribution}
:logic: 30
:abstraction: 30
:reasoning: 35
:calculation: 5
::::
:::::

`````