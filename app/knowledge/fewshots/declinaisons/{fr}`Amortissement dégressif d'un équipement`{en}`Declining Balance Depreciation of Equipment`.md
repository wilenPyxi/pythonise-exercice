`````{exercise}
:title: {fr}`Amortissement dégressif d'un équipement`{en}`Declining Balance Depreciation of Equipment`
:modules: 
:recommendedExecutionTime: 10
:level: Elementary
:chap: chap_expLogFunctions_exponentialFunctions_ESCP
:involvedConcepts: 
:originalSource: 
:visibility: All
:variations: 
:comment: Appliqué (économie & gestion) : valeur résiduelle V(n)=V0·(1−d)^n d'un actif, décroissance exponentielle (base 0,8∈(0,1)) et interprétation.
:id: c70b202b-74d9-11f1-a8a1-0ed8d3b012a9
:originalExerciseId: 773a7c51-6597-11f1-a8a1-0ed8d3b012a9

````{python}
import random as rd
from fractions import Fraction
from decimal import Decimal, ROUND_HALF_UP

def _grp(ip):
    neg = ip.startswith('-'); ip = ip.lstrip('-'); g = []
    while len(ip) > 3:
        g.insert(0, ip[-3:]); ip = ip[:-3]
    g.insert(0, ip)
    return ('-' if neg else '') + '\\,'.join(g)

def money_fr(v, dec=2):
    f = Fraction(v)
    d = (Decimal(f.numerator) / Decimal(f.denominator)).quantize(Decimal(1).scaleb(-dec), rounding=ROUND_HALF_UP)
    s = format(abs(d), 'f'); ip, _, fp = s.partition('.')
    return ('-' if d < 0 else '') + _grp(ip) + (('{,}' + fp) if dec > 0 else '')

def num_fr(v, maxdec=5):
    f = Fraction(v)
    d = (Decimal(f.numerator) / Decimal(f.denominator)).quantize(Decimal(1).scaleb(-maxdec), rounding=ROUND_HALF_UP)
    s = format(abs(d), 'f'); ip, _, fp = s.partition('.'); fp = fp.rstrip('0')
    return ('-' if d < 0 else '') + _grp(ip) + (('{,}' + fp) if fp else '')

# Construction déterministe, arithmétique exacte
V0 = rd.choice([5000, 8000, 10000, 12000, 15000, 18000, 20000])
taux = rd.choice([Fraction(7, 10), Fraction(3, 4), Fraction(4, 5), Fraction(17, 20), Fraction(9, 10)])

V1val = V0 * taux
V2val = V0 * taux**2
V3val = V0 * taux**3
n5 = rd.randint(4, 7)
V5val = V0 * taux**n5
pourcentageRestant = taux**n5 * 100
pourcentagePerdu = 100 - pourcentageRestant

# Rendus
V0Aff = money_fr(V0, 0)
V1Aff = money_fr(V1val, 2)
V2Aff = money_fr(V2val, 2)
V3Aff = money_fr(V3val, 2)
V5valAff = money_fr(V5val, 2)
tauxAff = num_fr(taux, 2)
taux2Aff = num_fr(taux**2, 4)
taux3Aff = num_fr(taux**3, 5)
n5Aff = str(n5)
tauxPuissanceN5Aff = num_fr(taux**n5, 5)
pourcentageRestantAffQ3 = num_fr(pourcentageRestant, 2)
pourcentagePerduAffQ3 = num_fr(pourcentagePerdu, 2)

# === Ajouts conversion FGQ ===
def _solnum(s):
    return s.replace("\\,", "").replace("{,}", ".")
V0Sol = _solnum(V0Aff)
V1Sol = _solnum(V1Aff)
V2Sol = _solnum(V2Aff)
V3Sol = _solnum(V3Aff)
V5Sol = _solnum(V5valAff)
globals()
````

:::::{question}
:questionType: FGQ
:questionId: 0
:questionIndex: 0
:solution: [["ord","${{ V0Sol }}$","${{ V1Sol }}$","${{ V2Sol }}$","${{ V3Sol }}$"],["0","0","0","0"]]

::::{questionStatement}
{fr}`Une entreprise acquiert un serveur pour`{en}`A company acquires a server for` ${{ V0Aff }}$ €. {fr}`Sa valeur résiduelle après`{en}`Its residual value after` $n$ {fr}`années est`{en}`years is` $V(n)={{ V0Aff }}\times({{ tauxAff }})^{n}$. {fr}`Calculer`{en}`Calculate` $V(0)$, $V(1)$, $V(2)$ {fr}`et`{en}`and` $V(3)$ {fr}`(valeurs exactes).`{en}`(exact values).`

$V(0) =$ {input}`||80` $\quad V(1) =$ {input}`||80` $\quad V(2) =$ {input}`||80` $\quad V(3) =$ {input}`||80`
::::

::::{questionHint}
{fr}`Appliquer la formule ; on a`{en}`Apply the formula; we have` $({{ tauxAff }})^{2}={{ taux2Aff }}$ {fr}`et`{en}`and` $({{ tauxAff }})^{3}={{ taux3Aff }}$.
::::

::::{displayedSolution}
$V(0) = {{ V0Aff }}$ € $\quad V(1) = {{ V1Aff }}$ € $\quad V(2) = {{ V2Aff }}$ € $\quad V(3) = {{ V3Aff }}$ €
::::

::::{detailedSolution}
{fr}`On applique la formule en augmentant`{en}`We apply the formula by increasing` $n$. {fr}`La base élevée à la puissance`{en}`The base raised to the power` $0$ {fr}`vaut`{en}`equals` $1$, {fr}`donc`{en}`so` $V(0)={{ V0Aff }}$. {fr}`Ensuite :`{en}`Then:`

$V(1)={{ V0Aff }}\times{{ tauxAff }}={{ V1Aff }}$, $\quad V(2)={{ V0Aff }}\times{{ taux2Aff }}={{ V2Aff }}$, $\quad V(3)={{ V0Aff }}\times{{ taux3Aff }}={{ V3Aff }}$.
::::

::::{weightDistribution}
:logic: 10
:abstraction: 20
:reasoning: 25
:calculation: 45
::::
:::::

:::::{question}
:questionType: MCQ
:questionId: 1
:questionIndex: 1

::::{questionStatement}
{fr}`Déterminer si`{en}`Determine whether` $V$ {fr}`est croissante ou décroissante, et justifier à partir de la base.`{en}`is increasing or decreasing, and justify from the base.`
::::

::::{questionHint}
{fr}`La base est`{en}`The base is` ${{ tauxAff }}\in(0,1)$.
::::

::::{mcqAnswer}
:isRightAnswer: true
{fr}`Strictement décroissante (base dans $(0,1)$)`{en}`Strictly decreasing (base in $(0,1)$)`
::::

::::{mcqAnswer}
:isRightAnswer: false
{fr}`Strictement croissante (base $> 1$)`{en}`Strictly increasing (base $> 1$)`
::::

::::{mcqAnswer}
:isRightAnswer: false
{fr}`Constante`{en}`Constant`
::::

::::{detailedSolution}
{fr}`La base est`{en}`The base is` $b={{ tauxAff }}\in(0,1)$, {fr}`donc`{en}`so` $V$ {fr}`est strictement décroissante : la valeur du serveur diminue chaque année. On vérifie :`{en}`is strictly decreasing: the server's value decreases each year. We verify:` ${{ V0Aff }}>{{ V1Aff }}>{{ V2Aff }}>{{ V3Aff }}$.
::::

::::{weightDistribution}
:logic: 25
:abstraction: 35
:reasoning: 30
:calculation: 10
::::
:::::

:::::{question}
:questionType: FGQ
:questionId: 2
:questionIndex: 2
:solution: [["ord","${{ V5Sol }}$"],["0"]]

::::{questionStatement}
{fr}`Calculer`{en}`Calculate` $V({{ n5Aff }})$ {fr}`(on donne`{en}`(given` $({{ tauxAff }})^{ {{ n5Aff }} }={{ tauxPuissanceN5Aff }}$), {fr}`puis interpréter le résultat dans le contexte de l'entreprise.`{en}`then interpret the result in the company's context.`

$V({{ n5Aff }}) =$ {input}`||80`
::::

::::{questionHint}
{fr}`Multiplier`{en}`Multiply` ${{ V0Aff }}$ {fr}`par la valeur fournie, puis comparer à la valeur d'achat.`{en}`by the given value, then compare to the purchase value.`
::::

::::{displayedSolution}
$V({{ n5Aff }}) = {{ V5valAff }}$ €
::::

::::{detailedSolution}
{fr}`On évalue`{en}`We evaluate` $V$ {fr}`en`{en}`at` $n={{ n5Aff }}$ :

\begin{equation*}
V({{ n5Aff }}) &= {{ V0Aff }} \times {{ tauxPuissanceN5Aff }} \\
&= {{ V5valAff }}.
\end{equation*}

{fr}`Après`{en}`After` ${{ n5Aff }}$ {fr}`ans, le serveur ne vaut plus que`{en}`years, the server is only worth` ${{ V5valAff }}$ €, {fr}`soit environ`{en}`which is approximately` ${{ pourcentageRestantAffQ3 }}\,\%$ {fr}`de sa valeur d'achat : l'entreprise a perdu environ`{en}`of its purchase value: the company has lost approximately` ${{ pourcentagePerduAffQ3 }}\,\%$ {fr}`de la valeur de cet actif en`{en}`of the value of this asset in` {{ n5Aff }} {fr}`ans.`{en}`years.`
::::

::::{weightDistribution}
:logic: 20
:abstraction: 25
:reasoning: 35
:calculation: 20
::::
:::::

`````