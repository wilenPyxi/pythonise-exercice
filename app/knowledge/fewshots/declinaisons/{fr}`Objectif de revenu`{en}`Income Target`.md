`````{exercise}
:originalExerciseId: 3fb67117-634b-11f1-a8a1-0ed8d3b012a9
:title: {fr}`Objectif de revenu`{en}`Income Target`
:modules: 
:recommendedExecutionTime: 10
:level: Elementary
:chap: 
:involvedConcepts: Solving_inequalities, Modeling_with_Functions  
:originalSource: Session 2: Equations and Inequalities - Applications of Linear Inequalities (Erwan Lamy, ESCP Business School)
:visibility: All
:variations: 
:comment: Version QCM — inéquation « au moins », résolution et intervalle.
:id: b3ceb29c-6e47-11f1-a8a1-0ed8d3b012a9

````{python}
import random as rd
from pyxiscience.Mes_fctions_generalistes_bis import pxs_config, pxsl_format_number
from pyxiscience.Classes_Extensions import pxs_Interval

config_standard = pxs_config()

# Tarif horaire (multiple de 5) et heures cibles ; revenu = rate * hMin (entier)
rate = rd.choice([50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 110, 120, 125, 150])
hMin = rd.randint(15, 50)
target = rate * hMin

# Précalcul de l'affichage
rateAff = pxsl_format_number(rate)
hMinAff = pxsl_format_number(hMin)
targetAff = pxsl_format_number(target)

inter = pxs_Interval(hMin, 168, False, False)

# === Distracteurs MCQ (ajouts ; le code ci-dessus est inchangé) ===
from sympy import oo
interCorrect = inter.print()
interD1 = pxs_Interval(hMin, 168, True, True).print()
interD2 = pxs_Interval(0, hMin, False, False).print()
interD3 = pxs_Interval(hMin, oo, False, True).print()

globals()
````

{fr}`Une consultante indépendante facture`{en}`An independent consultant charges` ${{rateAff}}$ € {fr}`de l'heure. Elle souhaite que son revenu hebdomadaire soit d'au moins`{en}`per hour. She wants her weekly income to be at least` ${{targetAff}}$ €. {fr}`On note`{en}`Let` $h$ {fr}`le nombre d'heures travaillées par semaine.`{en}`be the number of hours worked per week.`

:::::{question}
:questionType: MCQ

::::{questionStatement}
{fr}`Quelle inéquation traduit son objectif de revenu ?`{en}`Which inequality represents her income target?`
::::

::::{questionHint}
{fr}`« Au moins » se traduit par`{en}`"At least" translates to` $\geq$. {fr}`Son revenu hebdomadaire est`{en}`Her weekly income is` ${{rateAff}}\,h$.
::::

::::{mcqAnswer}
:isRightAnswer: true
${{rateAff}}\,h \geq {{targetAff}}$
::::

::::{mcqAnswer}
:isRightAnswer: false
${{rateAff}}\,h \leq {{targetAff}}$
::::

::::{mcqAnswer}
:isRightAnswer: false
${{rateAff}}\,h = {{targetAff}}$
::::

::::{mcqAnswer}
:isRightAnswer: false
${{targetAff}}\,h \geq {{rateAff}}$
::::

::::{mcqAnswer}
:isRightAnswer: false
${{targetAff}}\,h \leq {{rateAff}}$
::::

::::{mcqAnswer}
:isRightAnswer: false
{fr}`Aucune de ces réponses n'est correcte`{en}`None of these answers are correct`
::::

::::{detailedSolution}
{fr}`Le revenu hebdomadaire est`{en}`The weekly income is` ${{rateAff}}\,h$ {fr}`euros. L'objectif « revenu`{en}`euros. The target "income` $\geq {{targetAff}}$ {fr}`» donne :`{en}`" gives:`

\begin{equation*}
{{rateAff}}\,h \geq {{targetAff}}.
\end{equation*}
::::

::::{weightDistribution}
:logic: 15
:abstraction: 30
:reasoning: 35
:calculation: 20
::::
:::::

:::::{question}
:questionType: MCQ

::::{questionStatement}
{fr}`Résoudre l'inéquation`{en}`Solve the inequality` ${{rateAff}}\,h \geq {{targetAff}}$ {fr}`(sachant qu'une semaine compte 168 heures). Quel est l'ensemble des solutions sous forme d'intervalle ?`{en}`(knowing a week has 168 hours). What is the solution set in interval form?`
::::

::::{questionHint}
{fr}`Diviser les deux membres par`{en}`Divide both sides by` ${{rateAff}}$, {fr}`qui est positif : le sens de l'inégalité est conservé.`{en}`which is positive: the inequality sign is preserved.`
::::

::::{mcqAnswer}
:isRightAnswer: true
${{interCorrect}}$
::::

::::{mcqAnswer}
:isRightAnswer: false
${{interD1}}$
::::

::::{mcqAnswer}
:isRightAnswer: false
${{interD2}}$
::::

::::{mcqAnswer}
:isRightAnswer: false
${{interD3}}$
::::

::::{mcqAnswer}
:isRightAnswer: false
{fr}`Aucune de ces réponses n'est correcte`{en}`None of these answers are correct`
::::

::::{detailedSolution}
{fr}`On divise les deux membres par`{en}`We divide both sides by` ${{rateAff}} > 0$ {fr}`(sens conservé) :`{en}`(sign preserved):`

\begin{equation*}
h \geq \dfrac{ {{targetAff}} }{ {{rateAff}} } = {{hMinAff}}.
\end{equation*}

{fr}`L'ensemble des solutions est :`{en}`The solution set is:`

\begin{equation*}
h \in {{inter.print()}}.
\end{equation*}

{fr}`**Conclusion.** La consultante doit travailler au moins`{en}`**Conclusion.** The consultant must work at least` ${{hMinAff}}$ {fr}`heures par semaine pour atteindre son objectif de revenu. Elle ne peut pas travailler plus de 168 heures car cela correspond au nombre d'heures dans une semaine.`{en}`hours per week to reach her income target. She cannot work more than 168 hours as this corresponds to the number of hours in a week.`
::::

::::{weightDistribution}
:logic: 10
:abstraction: 15
:reasoning: 25
:calculation: 50
::::
:::::

`````
