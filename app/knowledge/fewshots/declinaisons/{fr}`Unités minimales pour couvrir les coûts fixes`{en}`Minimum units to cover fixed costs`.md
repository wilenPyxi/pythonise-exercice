`````{exercise}
:originalExerciseId: 7629a255-634b-11f1-a8a1-0ed8d3b012a9
:title: {fr}`Unités minimales pour couvrir les coûts fixes`{en}`Minimum units to cover fixed costs`
:modules: 
:recommendedExecutionTime: 10
:level: Elementary
:chap: 
:involvedConcepts: Solving_inequalities, Modeling_with_Functions  
:originalSource: Session 2: Equations and Inequalities - Applications of Linear Inequalities (Erwan Lamy, ESCP Business School)
:visibility: All
:variations: 
:comment: Version QCM — condition de non-perte, résolution et arrondi entier.
:id: a3e299b2-6e47-11f1-a8a1-0ed8d3b012a9

````{python}
import random as rd
from sympy import Rational, ceiling, oo, Integer
from pyxiscience.Mes_fctions_generalistes_bis import pxs_config, pxsl_format_number, pxsl_num
from pyxiscience.Classes_Extensions import pxs_Interval

config_standard = pxs_config()

# Coûts fixes entiers, marge unitaire décimale (k/10), quotient non entier -> arrondi utile
for _ in range(300):
    fixedCost = rd.randint(400, 1000)
    k = rd.randint(5, 30)
    if (10 * fixedCost) % k != 0:
        break

margin = Rational(k, 10)
qExact = Rational(fixedCost * 10, k)
qMin = int(ceiling(qExact))

# Précalcul de l'affichage
marginAff = pxsl_num(margin, dec=2)
fixedCostAff = pxsl_format_number(fixedCost)
qApproxAff = pxsl_num(qExact, dec=2)
qMinAff = pxsl_format_number(qMin)
margeFoisQminAff = pxsl_num(margin * qMin, dec=2)

# === Distracteurs MCQ (ajouts ; le code ci-dessus est inchangé) ===
def _dedl(correct_l, cands, n=3):
    seen = {correct_l}; out = []
    for s in cands:
        if s not in seen:
            seen.add(s); out.append(s)
        if len(out) == n:
            break
    return out

if isinstance(qExact, Integer):
    borne = qExact
else:
    borne = int(qExact) + 1

# Q2 : entier minimal
repBorne = pxsl_format_number(int(borne))
_cB = [pxsl_format_number(int(borne) - 1),
       pxsl_format_number(int(ceiling(Rational(fixedCost, k)))),
       pxsl_format_number(int(borne) + 1),
       pxsl_format_number(int(2 * borne))]
_d = _dedl(repBorne, _cB)
b1, b2, b3 = _d[0], _d[1], _d[2]

# Q1 : intervalles
def _ival(lo, hi, ol, oh):
    s = pxs_Interval(lo, hi, ol, oh).print()
    if pxs_lang == "fr":
        s = s.replace(".", ",")
    return s

_qa = round(float(qExact), 2)
interCorrect = _ival(_qa, oo, False, True)
interD1 = _ival(_qa, oo, True, True)
interD2 = _ival(-oo, _qa, True, False)
interD3 = _ival(0, _qa, False, False)

globals()
````

:::::{question}
:questionType: MCQ

::::{questionStatement}
{fr}`Une petite boulangerie a des coûts fixes hebdomadaires de`{en}`A small bakery has weekly fixed costs of` ${{fixedCostAff}}$ {fr}`€ (loyer, salaires, etc.). Chaque pain vendu génère une marge de contribution de`{en}`€ (rent, salaries, etc.). Each loaf of bread sold generates a contribution margin of` ${{marginAff}}$ {fr}`€ (prix de vente moins coût variable unitaire). On note`{en}`€ (selling price minus unit variable cost). Let` $q$ {fr}`le nombre de pains vendus par semaine. Quelle inéquation traduit que la marge de contribution totale couvre les coûts fixes (la boulangerie ne fait pas de perte) ?`{en}`be the number of loaves sold per week. Which inequality expresses that the total contribution margin covers the fixed costs (the bakery does not make a loss)?`
::::

::::{questionHint}
{fr}`La marge de contribution totale est égale à`{en}`The total contribution margin is equal to` ${{marginAff}}\,q$. {fr}`La condition de non-perte correspond à une marge au moins égale aux coûts fixes.`{en}`The break-even condition corresponds to a margin at least equal to the fixed costs.`
::::

::::{mcqAnswer}
:isRightAnswer: true
${{marginAff}}\,q \geq {{fixedCostAff}}$
::::

::::{mcqAnswer}
:isRightAnswer: false
${{marginAff}}\,q \leq {{fixedCostAff}}$
::::

::::{mcqAnswer}
:isRightAnswer: false
${{marginAff}}\,q = {{fixedCostAff}}$
::::

::::{mcqAnswer}
:isRightAnswer: false
${{fixedCostAff}}\,q \geq {{marginAff}}$
::::

::::{mcqAnswer}
:isRightAnswer: false
${{fixedCostAff}}\,q \leq {{marginAff}}$
::::

::::{mcqAnswer}
:isRightAnswer: false
{fr}`Aucune de ces réponses n'est correcte`{en}`None of these answers are correct`
::::

::::{detailedSolution}
{fr}`La marge de contribution totale est`{en}`The total contribution margin is` ${{marginAff}}\,q$. {fr}`La condition de non-perte s'écrit :`{en}`The break-even condition is written as:`

\begin{equation*}
{{marginAff}}\,q \geq {{fixedCostAff}}.
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
{fr}`Résoudre l'inéquation`{en}`Solve the inequality` ${{marginAff}}\,q \geq {{fixedCostAff}}$ {fr}`(pour`{en}`(for` $q \geq 0${fr}`). Quel est l'ensemble des solutions sous forme d'intervalle ?`{en}`). What is the solution set in interval form?`
::::

::::{questionHint}
{fr}`Diviser les deux membres par la marge unitaire, qui est positive : le sens est conservé.`{en}`Divide both sides by the unit margin, which is positive: the direction is preserved.`
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
{fr}`On divise les deux membres par`{en}`We divide both sides by` ${{marginAff}} > 0$, {fr}`le sens est conservé :`{en}`the direction is preserved:`

\begin{equation*}
q \geq \dfrac{ {{fixedCostAff}} }{ {{marginAff}} } \approx {{qApproxAff}}.
\end{equation*}

{fr}`L'ensemble des solutions (pour`{en}`The solution set (for` $q \geq 0${fr}`) est`{en}`) is` ${{interCorrect}}$.
::::

::::{weightDistribution}
:logic: 10
:abstraction: 15
:reasoning: 25
:calculation: 50
::::
:::::

:::::{question}
:questionType: MCQ

::::{questionStatement}
{fr}`Quel est le nombre minimal de pains entiers que la boulangerie doit vendre pour atteindre le seuil de rentabilité ?`{en}`What is the minimum number of whole loaves that the bakery must sell to reach the break-even point?`
::::

::::{questionHint}
{fr}`Le nombre de pains est un entier. Arrondir la solution à l'entier supérieur.`{en}`The number of loaves is an integer. Round the solution up to the next integer.`
::::

::::{mcqAnswer}
:isRightAnswer: true
${{repBorne}}$
::::

::::{mcqAnswer}
:isRightAnswer: false
${{b1}}$
::::

::::{mcqAnswer}
:isRightAnswer: false
${{b2}}$
::::

::::{mcqAnswer}
:isRightAnswer: false
${{b3}}$
::::

::::{mcqAnswer}
:isRightAnswer: false
{fr}`Aucune de ces réponses n'est correcte`{en}`None of these answers are correct`
::::

::::{detailedSolution}
{fr}`La quantité`{en}`The quantity` $q$ {fr}`doit être un entier. Comme`{en}`must be an integer. Since` $\dfrac{ {{fixedCostAff}} }{ {{marginAff}} } \approx {{qApproxAff}}$, {fr}`on arrondit à l'entier supérieur :`{en}`we round up to the next integer:` $q = {{borne}}$.

{fr}`La boulangerie doit vendre au moins`{en}`The bakery must sell at least` ${{borne}}$ {fr}`pains par semaine pour ne pas faire de perte.`{en}`loaves per week to avoid making a loss.`
::::

::::{weightDistribution}
:logic: 20
:abstraction: 20
:reasoning: 35
:calculation: 25
::::
:::::

`````
