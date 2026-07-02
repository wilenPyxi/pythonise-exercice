`````{exercise}
:originalExerciseId: 95586bb6-6340-11f1-a8a1-0ed8d3b012a9
:title: {fr}`Prix admissible entre marge minimale et plafond réglementaire`{en}`Admissible price between minimum margin and regulatory ceiling`
:modules: 
:recommendedExecutionTime: 20
:level: Elementary
:chap: 
:involvedConcepts: upp_and_low, Interval_Notation, Solving_inequalities
:originalSource: 
:visibility: All
:variations: 
:comment: Version QCM — borne inférieure (marge) puis encadrement/intervalle semi-ouvert.
:id: e5eb824f-6e47-11f1-a8a1-0ed8d3b012a9

````{python}
import random as rd
import math
from sympy import Rational
from pyxiscience.Mes_fctions_generalistes_bis import pxs_config, pxs_nvirgzero
from pyxiscience.Classes_Extensions import pxs_Interval

config_standard = pxs_config()

def rat_fr(r):
    r = Rational(r)
    if r.q == 1:
        return str(r.p)
    d, twos, fives = r.q, 0, 0
    while d % 2 == 0:
        d //= 2; twos += 1
    while d % 5 == 0:
        d //= 5; fives += 1
    assert d == 1, f"décimale non finie : {r}"
    k = max(twos, fives)
    scaled = (r.p * 10**k) // r.q
    sign = '-' if scaled < 0 else ''
    s = str(abs(scaled)).rjust(k + 1, '0')
    intpart, frac = s[:-k], s[-k:].rstrip('0')
    return sign + intpart + ('{,}' + frac if frac else '')

# Coût d'achat et taux de marge (rationnels exacts)
for _ in range(2000):
    c = rd.randint(20, 100)
    pct = rd.choice([15, 20, 25, 30, 35, 40, 45, 50])
    taux_marge = Rational(pct, 100)
    coeff_marge = 1 + taux_marge
    borneInf = c * coeff_marge
    lo = math.ceil(borneInf)
    if lo + 5 <= 150:
        plafond = rd.randint(lo + 5, 150)
        break

p_exemple = (lo + plafond) // 2

# Rendus
tauxPct = pct
tauxMargeAff = rat_fr(taux_marge)
coeffMargeAff = rat_fr(coeff_marge)
borneInfAff = rat_fr(borneInf)
pExemple = p_exemple
encadrAff = f"{borneInfAff} \\leq p < {plafond}"
if pxs_lang == "fr":
    SAff = pxs_Interval(pxs_nvirgzero(float(borneInf)), plafond, False, True).print().replace(".",",")
else:
    SAff = pxs_Interval(pxs_nvirgzero(float(borneInf)), plafond, False, True).print()

# === Distracteurs MCQ (ajouts ; le code ci-dessus est inchangé) ===
def _dedl(correct_l, cands, n=3):
    seen = {correct_l}; out = []
    for s in cands:
        if s not in seen:
            seen.add(s); out.append(s)
        if len(out) == n:
            break
    return out

# Q0 : borne inférieure
repBI = borneInfAff
_cand = [Rational(c), c * taux_marge, c + coeff_marge, 2 * c * coeff_marge, c * (1 - taux_marge)]
_cs = [rat_fr(v) for v in _cand]
_d = _dedl(repBI, _cs)
bi1, bi2, bi3 = _d[0], _d[1], _d[2]

# Q1 : intervalle semi-ouvert (ouverture/fermeture des bornes)
def _iv(ol, oh):
    s = pxs_Interval(pxs_nvirgzero(float(borneInf)), plafond, ol, oh).print()
    if pxs_lang == "fr":
        s = s.replace(".", ",")
    return s

SCorrect = SAff
SD1 = _iv(True, False)
SD2 = _iv(False, False)
SD3 = _iv(True, True)

globals()
````

:::::{question}
:questionType: MCQ

::::{questionStatement}
{fr}`Une entreprise de distribution fixe le prix de vente unitaire`{en}`A distribution company sets the unit selling price` $p$ {fr}`(en euros) de sorte que la marge soit au moins`{en}`(in euros) so that the margin is at least` ${{ tauxPct }}\,\%$ {fr}`du coût d'achat`{en}`of the purchase cost` $c={{ c }}$ €, {fr}`et que le prix reste inférieur au plafond réglementaire de`{en}`and that the price remains below the regulatory ceiling of` ${{ plafond }}$ €. {fr}`Quelle est la borne inférieure issue de la contrainte de marge,`{en}`What is the lower bound from the margin constraint,` $p\geq {{ coeffMargeAff }}\times {{ c }}$ ?
::::

::::{questionHint}
{fr}`Une marge d'au moins`{en}`A margin of at least` ${{ tauxPct }}\,\%$ {fr}`sur le coût d'achat signifie`{en}`on the purchase cost means` $p\geq c+{{ tauxMargeAff }}\,c={{ coeffMargeAff }}\,c$.
::::

::::{mcqAnswer}
:isRightAnswer: true
${{ repBI }}$
::::

::::{mcqAnswer}
:isRightAnswer: false
${{ bi1 }}$
::::

::::{mcqAnswer}
:isRightAnswer: false
${{ bi2 }}$
::::

::::{mcqAnswer}
:isRightAnswer: false
${{ bi3 }}$
::::

::::{mcqAnswer}
:isRightAnswer: false
{fr}`Aucune de ces réponses n'est correcte`{en}`None of these answers are correct`
::::

::::{detailedSolution}
{fr}`On traduit la contrainte de marge en borne inférieure sur le prix.`{en}`We translate the margin constraint into a lower bound on the price.`

\begin{equation*}
p \geq {{ coeffMargeAff }} \times {{ c }} = {{ borneInfAff }}.
\end{equation*}

{fr}`La borne inférieure est`{en}`The lower bound is` ${{ borneInfAff }}$ €.
::::

::::{weightDistribution}
:logic: 15
:abstraction: 20
:reasoning: 30
:calculation: 35
::::
:::::

:::::{question}
:questionType: MCQ

::::{questionStatement}
{fr}`On combine la double contrainte (marge et plafond). Quel est l'ensemble des prix admissibles en notation intervalle (en tenant compte du type de chaque borne) ?`{en}`We combine the double constraint (margin and ceiling). What is the set of admissible prices in interval notation (taking into account the type of each bound)?`
::::

::::{questionHint}
{fr}`Combiner`{en}`Combine` $p\geq {{ borneInfAff }}$ {fr}`(marge, borne incluse) et`{en}`(margin, included bound) and` $p<{{ plafond }}$ {fr}`(plafond, borne exclue).`{en}`(ceiling, excluded bound).`
::::

::::{mcqAnswer}
:isRightAnswer: true
$S = {{ SCorrect }}$
::::

::::{mcqAnswer}
:isRightAnswer: false
$S = {{ SD1 }}$
::::

::::{mcqAnswer}
:isRightAnswer: false
$S = {{ SD2 }}$
::::

::::{mcqAnswer}
:isRightAnswer: false
$S = {{ SD3 }}$
::::

::::{mcqAnswer}
:isRightAnswer: false
{fr}`Aucune de ces réponses n'est correcte`{en}`None of these answers are correct`
::::

::::{detailedSolution}
{fr}`On rassemble les deux conditions en un encadrement ; aucune opération supplémentaire n'est nécessaire car`{en}`We combine the two conditions into an inequality; no additional operation is necessary since` $p$ {fr}`est déjà isolée.`{en}`is already isolated.`

\begin{equation*}
{{ encadrAff }}.
\end{equation*}

{fr}`L'ensemble des solutions est`{en}`The solution set is`

\begin{equation*}
S = {{ SAff }}.
\end{equation*}

{fr}`La borne`{en}`The bound` ${{ borneInfAff }}$ {fr}`est incluse (un prix de`{en}`is included (a price of` ${{ borneInfAff }}$ € {fr}`satisfait exactement la marge). La borne`{en}`exactly satisfies the margin). The bound` ${{ plafond }}$ {fr}`est exclue (un prix de`{en}`is excluded (a price of` ${{ plafond }}$ € {fr}`violerait le plafond).`{en}`would violate the ceiling).`
::::

::::{weightDistribution}
:logic: 20
:abstraction: 30
:reasoning: 30
:calculation: 20
::::
:::::

`````
