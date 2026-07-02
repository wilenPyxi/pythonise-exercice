`````{exercise}
:title: {fr}`Règle des exposants : simplification et calcul`{en}`Exponent Rules: Simplification and Calculation`
:modules: 
:recommendedExecutionTime: 8
:level: Elementary
:chap: chap_expLogFunctions_exponentialFunctions_ESCP
:involvedConcepts: 
:originalSource: 
:visibility: All
:variations: 
:comment: Échauffement (thème pur) : application de la règle b^(x+y)=b^x·b^y et b^(x−y)=b^x/b^y, en simplification littérale et en vérification numérique.
:id: 7dff868d-74d9-11f1-a8a1-0ed8d3b012a9
:originalExerciseId: 6da31517-6597-11f1-a8a1-0ed8d3b012a9

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

def num_fr(v, maxdec=5):
    f = Fraction(v)
    d = (Decimal(f.numerator) / Decimal(f.denominator)).quantize(Decimal(1).scaleb(-maxdec), rounding=ROUND_HALF_UP)
    s = format(abs(d), 'f'); ip, _, fp = s.partition('.'); fp = fp.rstrip('0')
    return ('-' if d < 0 else '') + _grp(ip) + (('{,}' + fp) if fp else '')

# Q1 : simplification symbolique (exposants >= 2 partout)
sommeA = rd.randint(5, 10)
diffB = rd.randint(3, 6)
exp1 = rd.randint(2, sommeA - 2)
exp2 = sommeA - exp1
exp4 = rd.randint(2, 5)
exp3 = exp4 + diffB
aAff = 'b^{%d}' % sommeA
bAff = 'b^{%d}' % diffB

# Q2 : vérification numérique
baseC = rd.choice([2, 3])
sommeC = rd.randint(5, 8)
exp5 = rd.randint(2, sommeC - 2)
exp6 = sommeC - exp5
baseDNum = rd.choice([3, 5])               # base_D = 3/2 ou 5/2
baseD = Fraction(baseDNum, 2)
diffD = rd.randint(2, 4)
exp8 = rd.randint(2, 4)
exp7 = exp8 + diffD

cVal = baseC ** sommeC
dVal = baseD ** diffD

# Rendus
baseDAff = '%d{,}5' % (baseDNum // 2)       # 3/2 -> 1{,}5 ; 5/2 -> 2{,}5
dValAff = num_fr(dVal, 5)

# === Ajouts conversion FGQ ===
def _solnum(x):
    return x.replace("\\,", "").replace("{,}", ".")
dValSol = _solnum(dValAff)
globals()
````

:::::{question}
:questionType: FGQ
:questionId: 0
:questionIndex: 0
:solution: [["ord","$b^{ {{ sommeA }} }$","$b^{ {{ diffB }} }$"],["0","0"]]

::::{questionStatement}
{fr}`Soit`{en}`Let` $b>0$, $b\neq 1$. {fr}`Simplifier`{en}`Simplify` $A=b^{ {{exp1}} }\cdot b^{ {{exp2}} }$ {fr}`et`{en}`and` $B=\dfrac{b^{ {{exp3}} }}{b^{ {{exp4}} }}$ {fr}`à l'aide de la règle des exposants.`{en}`using the exponent rules.`

{fr}`$A$ se simplifie en`{en}`$A$ simplifies to` {input}`||110` {fr}`et $B$ en`{en}`and $B$ to` {input}`||110`
::::

::::{questionHint}
$b^{x}\cdot b^{y}=b^{x+y}$ {fr}`et`{en}`and` $\dfrac{b^{x}}{b^{y}}=b^{x-y}$.
::::

::::{displayedSolution}
$A = b^{ {{ sommeA }} }$ $\qquad B = b^{ {{ diffB }} }$
::::

::::{detailedSolution}
{fr}`Par addition des exposants pour le produit, et soustraction pour le quotient :`{en}`By adding exponents for the product, and subtracting for the quotient:`

\begin{equation*}
A &= b^{ {{exp1}} }\cdot b^{ {{exp2}} } \\
&= b^{ {{exp1}} + {{exp2}} } \\
&= {{ aAff }}.
\end{equation*}

\begin{equation*}
B &= \frac{b^{ {{exp3}} }}{b^{ {{exp4}} }} \\
&= b^{ {{exp3}} - {{exp4}} } \\
&= {{ bAff }}.
\end{equation*}
::::

::::{weightDistribution}
:logic: 20
:abstraction: 30
:reasoning: 25
:calculation: 25
::::
:::::

:::::{question}
:questionType: FGQ
:questionId: 1
:questionIndex: 1
:solution: [["ord","${{ cVal }}$","${{ dValSol }}$"],["0","0"]]

::::{questionStatement}
{fr}`Calculer numériquement`{en}`Compute numerically` $C={{ baseC }}^{ {{exp5}} }\cdot {{ baseC }}^{ {{exp6}} }$ {fr}`et vérifier que`{en}`and verify that` $C={{ baseC }}^{ {{sommeC}} }$, {fr}`puis`{en}`then` $D=\dfrac{({{ baseDAff }})^{ {{exp7}} }}{({{ baseDAff }})^{ {{exp8}} }}$ {fr}`et vérifier que`{en}`and verify that` $D=({{ baseDAff }})^{ {{diffD}} }$.

$C =$ {input}`||80` $\qquad D =$ {input}`||80`
::::

::::{questionHint}
{fr}`Calculer chaque puissance, puis comparer au résultat attendu par la règle des exposants.`{en}`Compute each power, then compare to the expected result using the exponent rules.`
::::

::::{displayedSolution}
$C = {{ cVal }}$ $\qquad D = {{ dValAff }}$
::::

::::{detailedSolution}
{fr}`Pour`{en}`For` $C$ :

\begin{equation*}
C &= {{ baseC }}^{ {{exp5}} }\cdot {{ baseC }}^{ {{exp6}} } \\
&= {{ baseC }}^{ {{exp5}} + {{exp6}} } \\
&= {{ baseC }}^{ {{sommeC}} } \\
&= {{ cVal }}.
\end{equation*}

{fr}`Pour`{en}`For` $D$ :

\begin{equation*}
D &= \frac{({{ baseDAff }})^{ {{exp7}} }}{({{ baseDAff }})^{ {{exp8}} }} \\
&= ({{ baseDAff }})^{ {{exp7}} - {{exp8}} } \\
&= ({{ baseDAff }})^{ {{diffD}} } \\
&= {{ dValAff }}.
\end{equation*}

{fr}`Les deux vérifications sont cohérentes avec la règle des exposants.`{en}`Both verifications are consistent with the exponent rules.`
::::

::::{weightDistribution}
:logic: 15
:abstraction: 25
:reasoning: 25
:calculation: 35
::::
:::::

`````