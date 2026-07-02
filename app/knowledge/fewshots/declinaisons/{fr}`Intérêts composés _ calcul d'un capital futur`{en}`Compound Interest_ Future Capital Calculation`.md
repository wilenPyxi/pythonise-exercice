`````{exercise}
:title: {fr}`Intérêts composés : calcul d'un capital futur`{en}`Compound Interest: Future Capital Calculation`
:modules: 
:recommendedExecutionTime: 10
:level: Elementary
:chap: chap_expLogFunctions_exponentialFunctions_ESCP
:involvedConcepts: 
:originalSource: 
:visibility: All
:variations: 
:comment: Appliqué (économie & gestion) : capitalisation annuelle S(n)=P(1+r)^n, évaluation à plusieurs dates et monotonie (base 1,03>1).
:id: 9378268f-74d9-11f1-a8a1-0ed8d3b012a9
:originalExerciseId: 7265a5b6-6597-11f1-a8a1-0ed8d3b012a9

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

def num_fr(v, maxdec=4):
    f = Fraction(v)
    d = (Decimal(f.numerator) / Decimal(f.denominator)).quantize(Decimal(1).scaleb(-maxdec), rounding=ROUND_HALF_UP)
    s = format(abs(d), 'f'); ip, _, fp = s.partition('.'); fp = fp.rstrip('0')
    return ('-' if d < 0 else '') + _grp(ip) + (('{,}' + fp) if fp else '')

# Construction déterministe, arithmétique exacte (Fraction)
P = rd.choice([3000, 4000, 5000, 6000, 7000, 8000, 10000])
rPourcent = rd.choice([Fraction(2), Fraction(5, 2), Fraction(3), Fraction(7, 2),
                       Fraction(4), Fraction(9, 2), Fraction(5)])
base = 1 + rPourcent / 100
nLong = rd.randint(8, 15)

S0 = Fraction(P)
S1 = P * base
S2 = P * base**2
SNLong = P * base**nLong

# Rendus
PAff = money_fr(P, 0)
rPourcentAff = num_fr(rPourcent, 2)
baseAff = num_fr(base, 4)
baseMonoAff = num_fr(base, 2)
nLongAff = str(nLong)
baseCarreAff = num_fr(base**2, 4)
basePuissNLongAff = num_fr(base**nLong, 4)
s0Aff = money_fr(S0, 2)
s1Aff = money_fr(S1, 2)
s2Aff = money_fr(S2, 2)
sNLongAff = money_fr(SNLong, 2)

# === Ajouts conversion FGQ ===
def _solnum(s):
    return s.replace("\\,", "").replace("{,}", ".")
PSol = _solnum(PAff)
s1Sol = _solnum(s1Aff)
s2Sol = _solnum(s2Aff)
sNLongSol = _solnum(sNLongAff)
globals()
````

:::::{question}
:questionType: FGQ
:questionId: 0
:questionIndex: 0
:solution: [["ord","${{ PSol }}$","${{ s1Sol }}$","${{ s2Sol }}$"],["0","0","0"]]

::::{questionStatement}
{fr}`Un épargnant place`{en}`A saver invests` ${{ PAff }}$ € {fr}`à un taux annuel de`{en}`at an annual rate of` ${{ rPourcentAff }}\,\%$, {fr}`capitalisation annuelle :`{en}`annual compounding:` $S(n)={{ PAff }}\times({{ baseAff }})^{n}$. {fr}`Calculer`{en}`Calculate` $S(0)$, $S(1)$ {fr}`et`{en}`and` $S(2)$, {fr}`puis interpréter`{en}`then interpret` $S(0)$.

$S(0) =$ {input}`||80` $\qquad S(1) =$ {input}`||80` $\qquad S(2) =$ {input}`||80`
::::

::::{questionHint}
{fr}`Appliquer la formule avec`{en}`Apply the formula with` $n=0,1,2$ ; {fr}`rappeler que toute base élevée à la puissance`{en}`recall that any base raised to the power` $0$ {fr}`vaut`{en}`equals` $1$.
::::

::::{displayedSolution}
$S(0) = {{ PAff }}$ € $\qquad S(1) = {{ s1Aff }}$ € $\qquad S(2) = {{ s2Aff }}$ €
::::

::::{detailedSolution}
{fr}`On applique la formule. Pour`{en}`We apply the formula. For` $n=0$, {fr}`la base élevée à la puissance`{en}`the base raised to the power` $0$ {fr}`vaut`{en}`equals` $1$, {fr}`donc`{en}`so` $S(0)={{ PAff }}$.

\begin{equation*}
S(1) &= {{ PAff }} \times {{ baseAff }} \\
&= {{ s1Aff }}.
\end{equation*}

\begin{equation*}
S(2) &= {{ PAff }} \times ({{ baseAff }})^{2} \\
&= {{ PAff }} \times {{ baseCarreAff }} \\
&= {{ s2Aff }}.
\end{equation*}

$S(0)={{ PAff }}$ € {fr}`est le capital initial : aucun intérêt n'a encore été versé.`{en}`is the initial capital: no interest has been paid yet.`
::::

::::{weightDistribution}
:logic: 10
:abstraction: 20
:reasoning: 25
:calculation: 45
::::
:::::

:::::{question}
:questionType: FGQ
:questionId: 1
:questionIndex: 1
:solution: [["ord","${{ sNLongSol }}$"],["0"]]

::::{questionStatement}
{fr}`Calculer`{en}`Calculate` $S({{ nLongAff }})$. {fr}`On donne`{en}`We are given` $({{ baseAff }})^{ {{ nLongAff }} }\approx {{ basePuissNLongAff }}$.

$S({{ nLongAff }}) =$ {input}`||80`
::::

::::{questionHint}
{fr}`Multiplier`{en}`Multiply` ${{ PAff }}$ {fr}`par la valeur fournie.`{en}`by the provided value.`
::::

::::{displayedSolution}
$S({{ nLongAff }}) = {{ sNLongAff }}$ €
::::

::::{detailedSolution}
{fr}`En utilisant la valeur fournie :`{en}`Using the provided value:`

\begin{equation*}
S({{ nLongAff }}) &= {{ PAff }} \times ({{ baseAff }})^{ {{ nLongAff }} } \approx {{ PAff }} \times {{ basePuissNLongAff }} \\
&= {{ sNLongAff }}.
\end{equation*}
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
:questionId: 2
:questionIndex: 2

::::{questionStatement}
{fr}`Déterminer si`{en}`Determine whether` $S$ {fr}`est croissante ou décroissante, et justifier à partir de la base.`{en}`is increasing or decreasing, and justify from the base.`
::::

::::{questionHint}
{fr}`La base est`{en}`The base is` ${{ baseMonoAff }}>1$.
::::

::::{mcqAnswer}
:isRightAnswer: true
{fr}`Strictement croissante (base $> 1$)`{en}`Strictly increasing (base $> 1$)`
::::

::::{mcqAnswer}
:isRightAnswer: false
{fr}`Strictement décroissante (base $< 1$)`{en}`Strictly decreasing (base $< 1$)`
::::

::::{mcqAnswer}
:isRightAnswer: false
{fr}`Constante`{en}`Constant`
::::

::::{detailedSolution}
{fr}`La base est`{en}`The base is` $b={{ baseMonoAff }}>1$, {fr}`donc`{en}`so` $S$ {fr}`est strictement croissante : le capital augmente chaque année. C'est cohérent avec`{en}`is strictly increasing: the capital increases each year. This is consistent with` ${{ s0Aff }}<{{ s1Aff }}<{{ s2Aff }}<\dots<{{ sNLongAff }}$.
::::

::::{weightDistribution}
:logic: 25
:abstraction: 35
:reasoning: 30
:calculation: 10
::::
:::::

`````