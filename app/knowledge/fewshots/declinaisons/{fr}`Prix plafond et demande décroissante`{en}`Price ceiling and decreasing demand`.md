`````{exercise}
:originalExerciseId: 84168f40-6340-11f1-a8a1-0ed8d3b012a9
:title: {fr}`Prix plafond et demande décroissante`{en}`Price ceiling and decreasing demand`
:modules: 
:recommendedExecutionTime: 10
:level: Elementary
:chap: 
:involvedConcepts: Solving_inequalities
:originalSource: 
:visibility: All
:variations: 
:comment: Version QCM — division par un coefficient négatif (inversion du sens), ensemble en intervalle.
:id: f2cc923d-6e47-11f1-a8a1-0ed8d3b012a9

````{python}
import random as rd
from sympy import oo
from pyxiscience.Mes_fctions_generalistes_bis import pxs_config, pxsl_latex_coefficient as lc, pxsl_format_number
from pyxiscience.Classes_Extensions import pxs_Interval

config_standard = pxs_config()

# Tirage contraint : a divise (p_max - p_plafond)
for _ in range(2000):
    p_max = rd.randint(80, 200)
    p_plafond = rd.randint(max(40, p_max // 3), p_max - 20)
    diviseurs = [d for d in range(2, 11) if (p_max - p_plafond) % d == 0]
    if diviseurs:
        a = rd.choice(diviseurs)
        break

q_min = (p_max - p_plafond) // a
intermediaire = p_plafond - p_max

q_verif_ok = q_min
q_verif_ko = q_min - 1
p_verif_ko = p_max - a * q_verif_ko
intervalAff = pxs_Interval(q_min, oo, False, True).print()

# Rendus
negASignAff = lc(-a, sign=True)
pMax = p_max
pPlafond = p_plafond
negAAff = lc(-a)
qMinAff = pxsl_format_number(q_min)
qVerifOk = q_verif_ok
qVerifKo = q_verif_ko
pVerifKo = p_verif_ko

# === Distracteurs MCQ (ajouts ; le code ci-dessus est inchangé) ===
intervalCorrect = intervalAff
intD1 = pxs_Interval(q_min, oo, True, True).print()
intD2 = pxs_Interval(-oo, q_min, True, False).print()
intD3 = pxs_Interval(0, q_min, False, False).print()

globals()
````

:::::{question}
:questionType: MCQ

::::{questionStatement}
{fr}`Sur un marché, la fonction de demande inverse est`{en}`In a market, the inverse demand function is` 
\begin{equation*}
p(q) = {{ pMax }} {{ negASignAff }}q
\end{equation*}
{fr}`Le prix est en euros,`{en}`The price is in euros,` $q$ {fr}`en milliers d'unités. Un régulateur impose un prix plafond`{en}`in thousands of units. A regulator imposes a price ceiling` $p \leq {{ pPlafond }}$ €.\
\
{fr}`En traduisant cette contrainte par une inéquation sur`{en}`Translating this constraint into an inequality involving` $q$ {fr}`et en la résolvant, quel est l'ensemble des quantités compatibles ?`{en}`and solving it, what is the set of compatible quantities?`
::::

::::{questionHint}
{fr}`Substituer`{en}`Substitute` $p(q)$ {fr}`dans`{en}`into` $p \leq {{ pPlafond }}${fr}`, puis isoler`{en}`, then isolate` $q$ {fr}`en divisant par`{en}`by dividing by` ${{ negAAff }} < 0$ {fr}`: le sens s'inverse.`{en}`: the direction reverses.`
::::

::::{mcqAnswer}
:isRightAnswer: true
$S = {{ intervalCorrect }}$
::::

::::{mcqAnswer}
:isRightAnswer: false
$S = {{ intD1 }}$
::::

::::{mcqAnswer}
:isRightAnswer: false
$S = {{ intD2 }}$
::::

::::{mcqAnswer}
:isRightAnswer: false
$S = {{ intD3 }}$
::::

::::{mcqAnswer}
:isRightAnswer: false
{fr}`Aucune de ces réponses n'est correcte`{en}`None of these answers are correct`
::::

::::{detailedSolution}
{fr}`On soustrait d'abord une quantité, le sens de l'inégalité est alors conservé, puis on divise par un réel strictement négatif, qui inverse le sens de l'inégalité.`{en}`We first subtract a quantity, the direction of the inequality is then preserved, then we divide by a strictly negative real number, which reverses the direction of the inequality.`

\begin{equation*}
{{ pMax }} {{ negASignAff }}q \leq {{ pPlafond }} &\implies {{ negAAff }}q \leq {{ intermediaire }}\\[10pt]
&\implies \frac{ {{ negAAff }}q }{ {{ negAAff }} } \geq \frac{ {{ intermediaire }} }{ {{ negAAff }} }\\[10pt]
&\implies q \geq {{ qMinAff }}.
\end{equation*}

{fr}`L'ensemble des solutions est donc`{en}`The solution set is therefore`

\begin{equation*}
S = {{ intervalAff }}.
\end{equation*}

{fr}`Pour que le prix soit au plus`{en}`For the price to be at most` ${{ pPlafond }}$ €{fr}`, la quantité offerte doit être d'au moins`{en}`, the quantity supplied must be at least` ${{ qMinAff }}$ {fr}`milliers d'unités. Ceci est cohérent car la demande étant décroissante, un prix plus bas correspond à une quantité plus grande.`{en}`thousands of units. This is consistent because since demand is decreasing, a lower price corresponds to a larger quantity.`
::::

::::{weightDistribution}
:logic: 20
:abstraction: 25
:reasoning: 35
:calculation: 20
::::
:::::

`````
