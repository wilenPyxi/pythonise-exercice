`````{exercise}
:title: {fr}`Inéquation linéaire en deux étapes`{en}`Linear Inequality in Two Steps`
:modules: 
:recommendedExecutionTime: 6
:level: Elementary
:chap: chap_equations_Inequalities_linearInequalitiesIntervals_ESCP
:involvedConcepts: 
:originalSource: 
:visibility: All
:variations: 
:comment: Échauffement : résolution en deux étapes (addition puis division par un réel positif), ensemble solution en intervalle, borne exclue.
:originalExerciseId: d40ec55f-633f-11f1-a8a1-0ed8d3b012a9
:id: e8a23848-7098-11f1-a8a1-0ed8d3b012a9

````{python}
import random as rd
from sympy import oo
from pyxiscience.Mes_fctions_generalistes_bis import pxs_config, pxsl_latex_coefficient as lc
from pyxiscience.Classes_Extensions import pxs_Interval

config_standard = pxs_config()

# Contrainte : (c - b) divisible par a pour une solution entière
a = rd.randint(2, 9)
k = rd.randint(2, 9)
somme  = k * a
b = rd.randint(-15, -1)
c = somme + b

x_sol = somme // a
x_test_exclu = x_sol
x_test_inclus = x_sol + 1
verif_exclu = a * x_test_exclu + b
verif_inclus = a * x_test_inclus + b
intervalAff = pxs_Interval(x_sol, oo, True, True).print()

# Rendus
aAff = lc(a)
bSignAff = lc(b, ones=True, sign=True)
negBAff = str(-b)
xSol = x_sol
xTestExclu = x_test_exclu
xTestInclus = x_test_inclus
verifExclu = verif_exclu
verifInclus = verif_inclus

globals()
````

:::::{question}
:questionType: FGQ
:solution: [["ord","${{ xSol }}$","$+\infty$"],["0","0"]]

::::{questionStatement}
{fr}`Résoudre l'inéquation`{en}`Solve the inequality` ${{ aAff }}x {{ bSignAff }} > {{ c }}$ {fr}`et soit`{en}`and let` $S$ {fr}`son ensemble solution. Écrire`{en}`be its solution set. Write` $S$ {fr}`sous forme d'intervalle (choisir le crochet adapté au caractère strict ou large de l'inégalité) :`{en}`as an interval (choose the bracket matching the strict or non-strict nature of the inequality):`

$S =$ {select}`[|]||]||45` {input}`||120` $;$ {input}`||120` {select}`]|[||[||45`
::::

::::{questionHint}
{fr}`Isoler`{en}`Isolate` $x$ {fr}`en deux étapes : ajouter`{en}`in two steps: add` ${{ negBAff }}${fr}`, puis diviser par`{en}`, then divide by` ${{ a }} > 0$ {fr}`(le sens est conservé).`{en}`(the inequality sign is preserved).`
::::

::::{displayedSolution}
$S = \left] {{ xSol }} ;\ +\infty \right[$
::::

::::{detailedSolution}
{fr}`L'addition puis la division par un réel strictement positif conserve le sens de l'inégalité.`{en}`Addition followed by division by a strictly positive real number preserves the inequality sign.`

\begin{equation*}
{{ aAff }}x {{ bSignAff }} + {{ negBAff }} > {{ c }} + {{ negBAff }} &\implies {{ aAff }}x > {{ somme }}\\[10pt]
&\implies \frac{ {{ aAff }}x }{ {{ a }} } > \frac{ {{ somme }} }{ {{ a }} } \\[10pt]
&\implies x > {{ xSol }}.
\end{equation*}

{fr}`L'ensemble des solutions est donc`{en}`The solution set is therefore`

\begin{equation*}
S = {{ intervalAff }}.
\end{equation*}

{fr}`La borne`{en}`The bound` ${{ xSol }}$ {fr}`est exclue (inégalité stricte`{en}`is excluded (strict inequality` $>${fr}`), d'où la parenthèse ouverte.`{en}`), hence the open parenthesis.`
::::

::::{weightDistribution}
:logic: 15
:abstraction: 20
:reasoning: 30
:calculation: 35
::::
:::::

`````