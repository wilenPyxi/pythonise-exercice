`````{exercise}
:originalExerciseId: ccace217-633f-11f1-a8a1-0ed8d3b012a9
:title: {fr}`Plafond budgétaire`{en}`Budget cap`
:modules: 
:recommendedExecutionTime: 10
:level: Elementary
:chap: 
:involvedConcepts: Solving_inequalities
:originalSource: Session 2: Equations and Inequalities - Applications of Linear Inequalities (Erwan Lamy, ESCP Business School)
:visibility: All
:variations: 
:comment: Version QCM — contrainte « ne pas dépasser », résolution et intervalle.
:id: c8218be2-6e47-11f1-a8a1-0ed8d3b012a9

````{python}
import random as rd
from pyxiscience.Mes_fctions_generalistes_bis import pxs_config
from pyxiscience.Classes_Extensions import pxs_Interval

config_standard = pxs_config()

# Tirage aléatoire des paramètres
for _ in range(200):
    budget = rd.randint(80, 200)
    spent = rd.randint(20, budget - 10)
    if spent < budget:
        break

# Calcul de la solution
xMax = budget - spent

# === Distracteurs MCQ (ajouts ; le code ci-dessus est inchangé) ===
from sympy import oo
interCorrect = pxs_Interval(0, xMax, False, False).print()
interD1 = pxs_Interval(0, xMax, True, True).print()
interD2 = pxs_Interval(0, budget, False, False).print()
interD3 = pxs_Interval(xMax, oo, False, True).print()

globals()
````

:::::{question}
:questionType: MCQ

::::{questionStatement}
{fr}`Une étudiante dispose d'un budget hebdomadaire de {{budget}} € pour son alimentation. Elle a déjà dépensé {{spent}} € cette semaine. On note $x$ le montant supplémentaire (en euros) qu'elle peut encore dépenser. Quelle inéquation traduit que sa dépense totale ne doit pas dépasser {{budget}} € ?`{en}`A student has a weekly budget of €{{budget}} for food. She has already spent €{{spent}} this week. Let $x$ denote the additional amount (in euros) she may still spend. Which inequality expresses that her total spending must not exceed €{{budget}}?`
::::

::::{questionHint}
{fr}`« Ne doit pas dépasser » se traduit par $\leq$. La dépense totale est ${{spent}} + x$.`{en}`"Must not exceed" translates to $\leq$. The total spending is ${{spent}} + x$.`
::::

::::{mcqAnswer}
:isRightAnswer: true
${{spent}} + x \leq {{budget}}$
::::

::::{mcqAnswer}
:isRightAnswer: false
${{spent}} + x \geq {{budget}}$
::::

::::{mcqAnswer}
:isRightAnswer: false
${{spent}} + x = {{budget}}$
::::

::::{mcqAnswer}
:isRightAnswer: false
${{budget}} + x \leq {{spent}}$
::::

::::{mcqAnswer}
:isRightAnswer: false
{fr}`Aucune de ces réponses n'est correcte`{en}`None of these answers are correct`
::::

::::{detailedSolution}
{fr}`La dépense totale est ${{spent}} + x$ euros. La contrainte « dépense totale $\leq {{budget}}$ » donne :`{en}`The total spending is ${{spent}} + x$ euros. The constraint "total spending $\leq {{budget}}$" gives:`

\begin{equation*}
{{spent}} + x \leq {{budget}}.
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
{fr}`Résoudre l'inéquation ${{spent}} + x \leq {{budget}}$ (on rappelle que $x \geq 0$ puisque $x$ est un montant). Quel est l'ensemble des solutions sous forme d'intervalle ?`{en}`Solve the inequality ${{spent}} + x \leq {{budget}}$ (recall that $x \geq 0$ since $x$ is an amount of money). What is the solution set as an interval?`
::::

::::{questionHint}
{fr}`Soustraire {{spent}} aux deux membres : ajouter ou retrancher une constante ne change pas le sens de l'inégalité.`{en}`Subtract {{spent}} from both sides: adding or subtracting a constant does not change the direction of the inequality.`
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
{fr}`On soustrait {{spent}} aux deux membres (le sens est conservé) :`{en}`Subtract {{spent}} from both sides (the direction is preserved):`

\begin{equation*}
x \leq {{budget}} - {{spent}} = {{xMax}}.
\end{equation*}

{fr}`Comme $x \geq 0$, l'ensemble des solutions est :`{en}`Since $x \geq 0$, the solution set is:`

\begin{equation*}
x \in {{pxs_Interval(0, xMax, False, False).print()}}.
\end{equation*}

{fr}`**Conclusion.** L'étudiante peut encore dépenser au plus {{xMax}} € cette semaine.`{en}`**Conclusion.** The student may spend at most €{{xMax}} more this week.`
::::

::::{weightDistribution}
:logic: 10
:abstraction: 15
:reasoning: 25
:calculation: 50
::::
:::::

`````
