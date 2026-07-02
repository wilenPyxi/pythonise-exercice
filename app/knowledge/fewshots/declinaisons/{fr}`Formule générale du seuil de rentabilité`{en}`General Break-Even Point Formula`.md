`````{exercise}
:title: {fr}`Formule générale du seuil de rentabilité`{en}`General Break-Even Point Formula`
:modules: 
:recommendedExecutionTime: 15
:level: Elementary
:chap: chap_lines_Systems_economicEquilibriumBreakeven_ESCP
:involvedConcepts: 
:originalSource: Session 4 — Erwan Lamy, ESCP Business School
:visibility: All
:variations: 
:comment: Synthèse (gestion) : établissement de la formule q* = yFC/(p - c), condition p > c, application numérique et analyse de sensibilité aux coûts fixes.
:id: 60088df7-74c0-11f1-a8a1-0ed8d3b012a9
:originalExerciseId: 27f935cf-64e3-11f1-a8a1-0ed8d3b012a9

````{python}
import random as rd
# --- Helpers PyxiScience (definis inline, autonomes : aucun import externe) ---
def pxs_config():
    return {}
def pxsl_format_number(n):
    f = float(n)
    if abs(f - round(f)) < 1e-9:
        return "%d" % round(f)
    s = ("%.10f" % f).rstrip("0").rstrip(".")
    return s.replace(".", "{,}")
def pxsl_latex_coefficient(coef, ones=False, sign=False):
    coef = int(coef)
    if coef == 0:
        return "+0" if sign else "0"
    if not ones:
        if coef == 1:
            return "+" if sign else ""
        if coef == -1:
            return "-"
    if sign:
        return ("+%d" % coef) if coef > 0 else ("%d" % coef)
    return "%d" % coef
lc = pxsl_latex_coefficient
config_standard = pxs_config()

# Contraintes : p > c (marge strictement positive, et p - c >= 2 pour eviter un
# denominateur d'affichage egal a 1) ; yFc et yFcNouv multiples de (p - c) pour
# des seuils entiers ; yFcNouv > yFc.
for _ in range(2000):
    p = rd.randint(15, 25)
    c = rd.randint(4, 10)
    diff = p - c
    if diff < 2:
        continue
    multFc = [k * diff for k in range(1, 200) if 240 <= k * diff <= 480]
    multFcNouv = [k * diff for k in range(1, 200) if 480 <= k * diff <= 720]
    if not (multFc and multFcNouv):
        continue
    yFc = rd.choice(multFc)
    candNouv = [x for x in multFcNouv if x > yFc]
    if not candNouv:
        continue
    yFcNouv = rd.choice(candNouv)
    break

qStarNum = yFc // diff
qStarNouv = yFcNouv // diff
augmentation = qStarNouv - qStarNum

# --- Affichage precalcule ---
qStarAff = r"\dfrac{y_{FC}}{p - c}"
yFcAff = pxsl_format_number(yFc)
yFcNouvAff = pxsl_format_number(yFcNouv)
pMinusCAff = str(diff)
qStarNumAff = str(qStarNum)
qStarNouvAff = str(qStarNouv)
augmentationAff = str(augmentation)

globals()
````

:::::{question}
:questionType: MCQ

::::{questionStatement}
{fr}`Une entreprise vend un produit au prix unitaire`{en}`A company sells a product at unit price` $p${fr}`, avec un coût variable unitaire`{en}`, with a unit variable cost` $c$ {fr}`(avec`{en}`(with` $c < p${fr}`) et des coûts fixes`{en}`) and fixed costs` $y_{FC}${fr}`. Écrire le revenu total`{en}`. Write the total revenue` $y_{TR}(q)$ {fr}`et le coût total`{en}`and the total cost` $y_{TC}(q)${fr}`.`{en}`.`
::::

::::{questionHint}
{fr}`Reprendre les définitions générales du revenu et du coût total.`{en}`Use the general definitions of revenue and total cost.`
::::

::::{mcqAnswer}
:isRightAnswer: true
$y_{TR}(q) = p\,q$ {fr}`et`{en}`and` $y_{TC}(q) = c\,q + y_{FC}$
::::

::::{mcqAnswer}
:isRightAnswer: false
$y_{TR}(q) = p\,q + y_{FC}$ {fr}`et`{en}`and` $y_{TC}(q) = c\,q$
::::

::::{mcqAnswer}
:isRightAnswer: false
$y_{TR}(q) = (p-c)\,q$ {fr}`et`{en}`and` $y_{TC}(q) = c\,q + y_{FC}$
::::

::::{mcqAnswer}
:isRightAnswer: false
$y_{TR}(q) = p\,q$ {fr}`et`{en}`and` $y_{TC}(q) = c\,q$
::::

::::{mcqAnswer}
:isRightAnswer: false
{fr}`Aucune de ces réponses n'est correcte`{en}`None of these answers are correct`
::::

::::{detailedSolution}
{fr}`Par définition :`{en}`By definition:`

\begin{equation*}
y_{TR}(q) = p\,q, \qquad y_{TC}(q) = c\,q + y_{FC}.
\end{equation*}
::::

::::{weightDistribution}
:logic: 20
:abstraction: 30
:reasoning: 30
:calculation: 20
::::
:::::

:::::{question}
:questionType: MCQ

::::{questionStatement}
{fr}`En résolvant`{en}`By solving` $y_{TR}(q) = y_{TC}(q)${fr}`, établir la formule générale du seuil`{en}`, establish the general break-even formula` $q^{*} = \dfrac{y_{FC}}{p - c}${fr}`. Justifier pourquoi la condition`{en}`. Justify why the condition` $p > c$ {fr}`est nécessaire.`{en}`is necessary.`
::::

::::{questionHint}
{fr}`Regrouper les termes en`{en}`Group the terms in` $q${fr}`, factoriser par`{en}`, factor by` $q${fr}`, puis diviser par`{en}`, then divide by` $p - c${fr}`.`{en}`.`
::::

::::{mcqAnswer}
:isRightAnswer: true
$q^{*} = \dfrac{y_{FC}}{p-c}$, {fr}`valable si`{en}`valid if` $p > c$
::::

::::{mcqAnswer}
:isRightAnswer: false
$q^{*} = \dfrac{y_{FC}}{p+c}$, {fr}`valable si`{en}`valid if` $p > c$
::::

::::{mcqAnswer}
:isRightAnswer: false
$q^{*} = \dfrac{y_{FC}}{c-p}$, {fr}`valable si`{en}`valid if` $c > p$
::::

::::{mcqAnswer}
:isRightAnswer: false
$q^{*} = \dfrac{p-c}{y_{FC}}$, {fr}`valable si`{en}`valid if` $p > c$
::::

::::{mcqAnswer}
:isRightAnswer: false
{fr}`Aucune de ces réponses n'est correcte`{en}`None of these answers are correct`
::::

::::{detailedSolution}
{fr}`On résout`{en}`We solve` $y_{TR}(q) = y_{TC}(q)$ {fr}`:`{en}`:`

\begin{equation*}
p\,q = c\,q + y_{FC} \implies (p - c)\,q = y_{FC}.
\end{equation*}

{fr}`Comme`{en}`Since` $p > c${fr}`, on a`{en}`, we have` $p - c > 0${fr}`, et la division est licite :`{en}`, and the division is valid:`

\begin{equation*}
q^{*} = {{qStarAff}}.
\end{equation*}

{fr}`La condition`{en}`The condition` $p > c$ {fr}`est nécessaire : si`{en}`is necessary: if` $p \leq c${fr}`, alors`{en}`, then` $p - c \leq 0$ {fr}`et l'équation`{en}`and the equation` $(p - c)\,q = y_{FC}$ {fr}`n'a pas de solution positive (car`{en}`has no positive solution (since` $y_{FC} > 0${fr}`). L'entreprise ne pourrait jamais couvrir ses coûts fixes.`{en}`). The company could never cover its fixed costs.`
::::

::::{weightDistribution}
:logic: 25
:abstraction: 30
:reasoning: 35
:calculation: 10
::::
:::::

:::::{question}
:questionType: FGQ
:solution: [["ord","${{ qStarNumAff }}$"],["0"]]

::::{questionStatement}
{fr}`Une boutique d'accessoires vend des coques de téléphone à`{en}`An accessories shop sells phone cases at` $p = {{p}}$ {fr}`€, avec`{en}`€, with` $c = {{c}}$ {fr}`€ et`{en}`€ and` $y_{FC} = {{yFcAff}}$ {fr}`€/mois. Appliquer la formule pour trouver`{en}`€/month. Apply the formula to find` $q^{*}${fr}`.`{en}`.`\
\
$q^{*}$ = {input}`||80`
::::

::::{questionHint}
{fr}`Remplacer directement dans`{en}`Substitute directly into` $q^{*} = \dfrac{y_{FC}}{p - c}${fr}`.`{en}`.`
::::

::::{displayedSolution}
$q^{*} = {{ qStarNumAff }}$
::::

::::{detailedSolution}
{fr}`On applique la formule :`{en}`We apply the formula:`

\begin{equation*}
q^{*} = \dfrac{ {{yFcAff}} }{ {{p}} - {{c}} } = \dfrac{ {{yFcAff}} }{ {{pMinusCAff}} } = {{qStarNumAff}} \text{ {fr}`unités/mois`{en}`units/month`}.
\end{equation*}
::::

::::{weightDistribution}
:logic: 15
:abstraction: 20
:reasoning: 25
:calculation: 40
::::
:::::

:::::{question}
:questionType: FGQ
:questionId: 3
:questionIndex: 3
:solution: [["ord","${{ augmentationAff }}$"],["0"]]

::::{questionStatement}
{fr}`Si les coûts fixes passent à`{en}`If the fixed costs increase to` $y_{FC} = {{yFcNouvAff}}$ {fr}`€ (nouveau bail), de combien d'unités le seuil augmente-t-il ? Interpréter le résultat.`{en}`€ (new lease), by how many units does the break-even point increase? Interpret the result.`\
\
{fr}`Augmentation du seuil (unités/mois) :`{en}`Increase in break-even (units/month):` {input}`||80`.
::::

::::{questionHint}
{fr}`Recalculer`{en}`Recalculate` $q^{*}$ {fr}`avec le nouveau`{en}`with the new` $y_{FC}${fr}`, puis faire la différence.`{en}`, then compute the difference.`
::::

::::{displayedSolution}
{fr}`Augmentation :`{en}`Increase:` ${{ augmentationAff }}$
::::

::::{detailedSolution}
{fr}`Avec`{en}`With` $y_{FC} = {{yFcNouvAff}}$ {fr}`€ :`{en}`€:`

\begin{equation*}
q^{*} = \dfrac{ {{yFcNouvAff}} }{ {{pMinusCAff}} } = {{qStarNouvAff}} \text{ {fr}`unités/mois`{en}`units/month`}.
\end{equation*}

{fr}`Le seuil augmente de`{en}`The break-even point increases by` ${{qStarNouvAff}} - {{qStarNumAff}} = {{augmentationAff}}$ {fr}`unités : la boutique doit vendre`{en}`units: the shop must sell` {{augmentationAff}} {fr}`coques de plus chaque mois uniquement pour absorber le loyer plus élevé, sans gagner de profit supplémentaire.`{en}`more cases each month just to absorb the higher rent, without earning any additional profit.`
::::

::::{weightDistribution}
:logic: 20
:abstraction: 25
:reasoning: 30
:calculation: 25
::::
:::::

`````