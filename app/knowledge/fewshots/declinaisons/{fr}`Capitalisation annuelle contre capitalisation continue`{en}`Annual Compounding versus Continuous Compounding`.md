`````{exercise}
:title: {fr}`Capitalisation annuelle contre capitalisation continue`{en}`Annual Compounding versus Continuous Compounding`
:modules: 
:recommendedExecutionTime: 12
:level: Elementary
:chap: chap_expLogFunctions_exponentialFunctions_ESCP
:involvedConcepts: 
:originalSource: 
:visibility: All
:variations: 
:comment: Appliqué (économie & gestion) : comparaison d'un placement en capitalisation annuelle S=P(1+r)^n et en capitalisation continue S=P·e^(rn), évaluations numériques (e fourni) et interprétation de l'écart.
:id: daf335a0-74d9-11f1-a8a1-0ed8d3b012a9
:originalExerciseId: 5c4c10be-6598-11f1-a8a1-0ed8d3b012a9

````{python}
import random as rd
import math
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

# Paramètres financiers (déterministe). Annuel exact ; continu approché (e).
P = rd.choice([5000, 10000, 15000, 20000, 25000, 30000, 40000, 50000])
n = rd.randint(3, 10)
rPct = rd.choice([Fraction(2), Fraction(5, 2), Fraction(3), Fraction(7, 2), Fraction(4),
                  Fraction(9, 2), Fraction(5), Fraction(11, 2), Fraction(6), Fraction(13, 2),
                  Fraction(7), Fraction(15, 2), Fraction(8)])
r = rPct / 100

# Placement A : capitalisation annuelle (exact)
baseComp = 1 + r
puissance = baseComp ** n
sA = P * puissance

# Placement B : capitalisation continue (e^(r n), approché)
exposant = r * n
expVal = Fraction(math.exp(float(exposant)))
sB = P * expVal
ecart = sB - sA

# Rendus
pAff = money_fr(P, 0)
nAff = str(n)
rPctStr = num_fr(rPct, 1)
baseCompStr = num_fr(baseComp, 4)
puissanceApproxStr = num_fr(puissance, 4)
saAff = money_fr(sA, 2)
exposantContStr = num_fr(exposant, 2)
expApproxStr = num_fr(expVal, 4)
sbAff = money_fr(sB, 2)
ecartAff = money_fr(ecart, 2)

# === Ajouts conversion FGQ ===
def _solnum(s):
    return s.replace("\\,", "").replace("{,}", ".")
saSol = _solnum(saAff)
sbSol = _solnum(sbAff)
ecartSol = _solnum(ecartAff)
globals()
````

:::::{question}
:questionType: FGQ
:questionId: 0
:questionIndex: 0
:solution: [["ord","${{ saSol }}$"],["0"]]

::::{questionStatement}
{fr}`Un investisseur place`{en}`An investor invests` ${{ pAff }}$ € {fr}`sur`{en}`over` ${{ nAff }}$ {fr}`ans au taux de`{en}`years at a rate of` ${{ rPctStr }}\,\%$ {fr}`par an. Placement A (capitalisation annuelle) :`{en}`per year. Investment A (annual compounding):`  $S_{A}={{ pAff }}\times({{ baseCompStr }})^{ {{ nAff }} }$. {fr}`Calculer`{en}`Calculate` $S_{A}$ {fr}`(arrondir au centime). On donne`{en}`(round to the nearest cent). We are given` $({{ baseCompStr }})^{ {{ nAff }} }\approx {{ puissanceApproxStr }}$.

$S_{A} =$ {input}`||80`
::::

::::{questionHint}
{fr}`Multiplier`{en}`Multiply` ${{ pAff }}$ {fr}`par la valeur fournie.`{en}`by the given value.`
::::

::::{displayedSolution}
$S_{A} = {{ saAff }}$ €
::::

::::{detailedSolution}
{fr}`On applique la formule de capitalisation annuelle :`{en}`We apply the annual compounding formula:`

\begin{equation*}
S_{A} &= {{ pAff }} \times ({{ baseCompStr }})^{ {{ nAff }} } \approx {{ pAff }} \times {{ puissanceApproxStr }} \\
&= {{ saAff }}.
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
:questionType: FGQ
:questionId: 1
:questionIndex: 1
:solution: [["ord","${{ sbSol }}$"],["0"]]

::::{questionStatement}
{fr}`Placement B (capitalisation continue) :`{en}`Investment B (continuous compounding):` $S_{B}={{ pAff }}\times e^{r\times {{ nAff }}}$ {fr}`où`{en}`where` $r=\dfrac{ {{ rPctStr }} }{100}$, {fr}`avec`{en}`with` $e\approx 2{,}718$. {fr}`Calculer`{en}`Calculate` $S_{B}$ {fr}`(arrondir au centime). On donne`{en}`(round to the nearest cent). We are given` $e^{ {{ exposantContStr }} }\approx {{ expApproxStr }}$.

$S_{B} =$ {input}`||80`
::::

::::{questionHint}
{fr}`L'exposant vaut`{en}`The exponent equals` $r\times {{ nAff }}=\dfrac{ {{ rPctStr }} }{100}\times {{ nAff }}={{ exposantContStr }}$ ; {fr}`utiliser`{en}`use` $e^{ {{ exposantContStr }} }\approx {{ expApproxStr }}$.
::::

::::{displayedSolution}
$S_{B} = {{ sbAff }}$ €
::::

::::{detailedSolution}
{fr}`L'exposant vaut`{en}`The exponent equals` $r\times {{ nAff }}=\dfrac{ {{ rPctStr }} }{100}\times {{ nAff }}={{ exposantContStr }}$, {fr}`donc :`{en}`so:`

\begin{equation*}
S_{B} &= {{ pAff }} \times e^{ {{ exposantContStr }} } \approx {{ pAff }} \times {{ expApproxStr }} \\
&= {{ sbAff }}.
\end{equation*}
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
:questionId: 2
:questionIndex: 2
:solution: [["ord","${{ ecartSol }}$"],["0"]]

::::{questionStatement}
{fr}`Comparer`{en}`Compare` $S_{A}$ {fr}`et`{en}`and` $S_{B}$, {fr}`et interpréter l'écart dans le contexte financier.`{en}`and interpret the difference in the financial context.`

$S_{B} - S_{A} =$ {input}`||80`
::::

::::{questionHint}
{fr}`Calculer`{en}`Calculate` $S_{B}-S_{A}$.
::::

::::{displayedSolution}
$S_{B} - S_{A} = {{ ecartAff }}$ €
::::

::::{detailedSolution}
{fr}`On compare les deux montants :`{en}`We compare the two amounts:`

\begin{equation*}
S_{B} - S_{A} &\approx {{ sbAff }} - {{ saAff }} \\
&= {{ ecartAff }}.
\end{equation*}

{fr}`À taux affiché identique (`{en}`At the same stated rate (` ${{ rPctStr }}\,\%$ ), {fr}`la capitalisation continue`{en}`continuous compounding` $S_{B}\approx {{ sbAff }}$ € {fr}`rapporte un peu plus que la capitalisation annuelle`{en}`yields slightly more than annual compounding` $S_{A}\approx {{ saAff }}$ €, {fr}`l'écart étant d'environ`{en}`the difference being approximately` ${{ ecartAff }}$ €. {fr}`La capitalisation continue réinvestit les intérêts à chaque instant, alors que la capitalisation annuelle ne les réinvestit qu'une fois par an.`{en}`Continuous compounding reinvests interest at every instant, whereas annual compounding reinvests it only once per year.`
::::

::::{weightDistribution}
:logic: 20
:abstraction: 25
:reasoning: 35
:calculation: 20
::::
:::::

`````