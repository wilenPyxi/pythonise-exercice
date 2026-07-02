`````{exercise}
:originalExerciseId: df9c98f5-633f-11f1-a8a1-0ed8d3b012a9
:title: {fr}`Contrainte de budget publicitaire`{en}`Advertising budget constraint`
:modules: 
:recommendedExecutionTime: 10
:level: Elementary
:chap: 
:involvedConcepts: Solving_inequalities, Sets
:originalSource: 
:visibility: All
:variations: 
:comment: Version QCM — contrainte de budget, nombre maximal d'insertions et ensemble admissible.
:id: 0f2a4c67-6e48-11f1-a8a1-0ed8d3b012a9

````{python}
import random as rd
from pyxiscience.Mes_fctions_generalistes_bis import pxs_config, pxsl_format_number
from pyxiscience.Classes_Extensions import pxs_Interval

config_standard = pxs_config()

# Contrainte : budget multiple du coût d'insertion, nMax entier >= 5
for _ in range(2000):
    cout_insertion = rd.choice([40, 50, 60, 80, 100, 120, 150])
    budget = cout_insertion * rd.randint(10, 50)
    nMax = budget // cout_insertion
    if nMax >= 5 and 800 <= budget <= 3000:
        break

verif_max = cout_insertion * nMax
verif_exclu = cout_insertion * (nMax + 1)

# Rendus
budgetAff = pxsl_format_number(budget)
coutInsertion = cout_insertion
nMaxPlusUn = nMax + 1
verifMaxAff = pxsl_format_number(verif_max)
verifExcluAff = pxsl_format_number(verif_exclu)

# === Distracteurs MCQ (ajouts ; le code ci-dessus est inchangé) ===
interCorrect = pxs_Interval(0, nMax, False, False).print()
interD1 = pxs_Interval(0, budget, True, False).print()
interD2 = pxs_Interval(0, nMax, True, False).print()
interD3 = pxs_Interval(0, budget, False, False).print()

globals()
````

:::::{question}
:questionType: MCQ

::::{questionStatement}
{fr}`Une start-up dispose d'un budget de communication de`{en}`A start-up has a communication budget of` ${{ budgetAff }}$ €. {fr}`Chaque insertion publicitaire coûte`{en}`Each advertising insertion costs` ${{ coutInsertion }}$ €. {fr}`On note`{en}`Let` $n$ {fr}`le nombre d'insertions. Quel est l'ensemble des valeurs admissibles de`{en}`be the number of insertions. What is the set of admissible values of` $n$ {fr}`en notation intervalle ?`{en}`in interval notation?`
::::

::::{questionHint}
{fr}`Traduire la contrainte de budget par`{en}`Translate the budget constraint as` ${{ coutInsertion }}n\leq {{ budgetAff }}$, {fr}`puis diviser par`{en}`then divide by` ${{ coutInsertion }}>0$ {fr}`(sens conservé). Ne pas oublier`{en}`(inequality sign preserved). Do not forget` $n\geq 0$.
::::

::::{mcqAnswer}
:isRightAnswer: true
$S = {{ interCorrect }}$
::::

::::{mcqAnswer}
:isRightAnswer: false
$S = {{ interD1 }}$
::::

::::{mcqAnswer}
:isRightAnswer: false
$S = {{ interD2 }}$
::::

::::{mcqAnswer}
:isRightAnswer: false
$S = {{ interD3 }}$
::::

::::{mcqAnswer}
:isRightAnswer: false
{fr}`Aucune de ces réponses n'est correcte`{en}`None of these answers are correct`
::::

::::{detailedSolution}
{fr}`La dépense totale`{en}`The total expenditure` ${{ coutInsertion }}n$ {fr}`ne doit pas dépasser le budget, d'où une inéquation résolue par division par un réel positif.`{en}`must not exceed the budget, hence an inequality solved by division by a positive real number.`

\begin{equation*}
{{ coutInsertion }}n \leq {{ budgetAff }}&\implies \frac{ {{ coutInsertion }}n }{ {{ coutInsertion }} } \leq \frac{ {{ budgetAff }} }{ {{ coutInsertion }} } \\[10pt]
&\implies n \leq {{ nMax }}.
\end{equation*}

{fr}`Comme`{en}`Since` $n$ {fr}`est un nombre d'insertions,`{en}`is a number of insertions,` $n\geq 0$. {fr}`L'ensemble admissible est donc :`{en}`The admissible set is therefore:`

\begin{equation*}
S = {{pxs_Interval(0, nMax, False, False).print()}}.
\end{equation*}

{fr}`La start-up peut financer au maximum`{en}`The start-up can finance at most` ${{ nMax }}$ {fr}`insertions.`{en}`insertions.`
::::

::::{weightDistribution}
:logic: 15
:abstraction: 20
:reasoning: 30
:calculation: 35
::::
:::::

`````
