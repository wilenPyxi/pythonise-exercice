`````{exercise}
:title: {fr}`Monotonie selon la base et comparaison de valeurs`{en}`Monotonicity according to base and comparison of values`
:modules: 
:recommendedExecutionTime: 10
:level: Elementary
:chap: chap_expLogFunctions_exponentialFunctions_ESCP
:involvedConcepts: 
:originalSource: 
:visibility: All
:variations: 
:comment: Échauffement (thème pur) : reconnaissance de la monotonie de quatre fonctions b^x d'après la base, et comparaison de valeurs par la monotonie (sans calcul exact).
:id: 73274236-74d8-11f1-a8a1-0ed8d3b012a9
:originalExerciseId: 699e40c5-6597-11f1-a8a1-0ed8d3b012a9

````{python}
import random as rd
from fractions import Fraction

def frac_latex(fr):
    fr = Fraction(fr)
    if fr.denominator == 1:
        return str(fr.numerator)
    sign = '-' if fr.numerator < 0 else ''
    return sign + r'\dfrac{%d}{%d}' % (abs(fr.numerator), fr.denominator)

# Construction déterministe : monotonies garanties par les intervalles des bases.
b1 = rd.randint(2, 5)                       # base entière > 1 -> croissante
b2Den = rd.randint(2, 5)
b2 = Fraction(1, b2Den)                     # base dans (0,1) -> décroissante
b3Den = rd.randint(2, 5)
b3Num = rd.randint(b3Den + 1, 9)
b3 = Fraction(b3Num, b3Den)                 # base > 1 -> croissante
b4Dec = rd.randint(6, 9)
b4 = Fraction(b4Dec, 10)                    # base décimale dans (0,1) -> décroissante

# Exposants pour Q2 (>= 2 pour éviter les exposants 0 et 1)
x1 = rd.randint(2, 4)
x2 = rd.randint(x1 + 2, x1 + 4)

# Rendus
b1Aff = str(b1)
b2Aff = frac_latex(b2)
b3Aff = frac_latex(b3)
b4Aff = '0{,}%d' % b4Dec
x1Aff = str(x1)
x2Aff = str(x2)
f1x1Aff = frac_latex(b1**x1)
f1x2Aff = frac_latex(b1**x2)
f2x1Aff = frac_latex(b2**x1)
f2x2Aff = frac_latex(b2**x2)

globals()
````

:::::{question}
:questionType: MCQ
:questionId: 0
:questionIndex: 0

::::{questionStatement}
{fr}`On considère`{en}`Consider` $f_{1}(x)={{ b1Aff }}^{x}$, $f_{2}(x)=\left({{ b2Aff }}\right)^{x}$, $f_{3}(x)=\left({{ b3Aff }}\right)^{x}$ {fr}`et`{en}`and` $f_{4}(x)=({{ b4Aff }})^{x}$. {fr}`Reconnaître lesquelles sont strictement croissantes et lesquelles sont strictement décroissantes, en justifiant à partir de la base.`{en}`Identify which are strictly increasing and which are strictly decreasing, justifying from the base.`
::::

::::{questionHint}
{fr}`Si`{en}`If` $b>1$ {fr}`: croissante ; si`{en}`: increasing; if` $0<b<1$ {fr}`: décroissante.`{en}`: decreasing.`
::::

::::{mcqAnswer}
:isRightAnswer: true
{fr}`$f_{1}$ et $f_{3}$ strictement croissantes ; $f_{2}$ et $f_{4}$ strictement décroissantes`{en}`$f_{1}$ and $f_{3}$ strictly increasing; $f_{2}$ and $f_{4}$ strictly decreasing`
::::

::::{mcqAnswer}
:isRightAnswer: false
{fr}`$f_{1}$ et $f_{2}$ strictement croissantes ; $f_{3}$ et $f_{4}$ strictement décroissantes`{en}`$f_{1}$ and $f_{2}$ strictly increasing; $f_{3}$ and $f_{4}$ strictly decreasing`
::::

::::{mcqAnswer}
:isRightAnswer: false
{fr}`$f_{2}$ et $f_{4}$ strictement croissantes ; $f_{1}$ et $f_{3}$ strictement décroissantes`{en}`$f_{2}$ and $f_{4}$ strictly increasing; $f_{1}$ and $f_{3}$ strictly decreasing`
::::

::::{mcqAnswer}
:isRightAnswer: false
{fr}`Les quatre fonctions sont strictement croissantes`{en}`All four functions are strictly increasing`
::::

::::{mcqAnswer}
:isRightAnswer: false
{fr}`Aucune de ces réponses n'est correcte`{en}`None of these answers are correct`
::::

::::{detailedSolution}
$f_{1}$ {fr}`: base`{en}`: base` ${{ b1Aff }}>1$, {fr}`strictement croissante.`{en}`strictly increasing.` $f_{2}$ {fr}`: base`{en}`: base` ${{ b2Aff }}\in(0,1)$, {fr}`strictement décroissante.`{en}`strictly decreasing.` $f_{3}$ {fr}`: base`{en}`: base` ${{ b3Aff }}>1$, {fr}`strictement croissante.`{en}`strictly increasing.` $f_{4}$ {fr}`: base`{en}`: base` ${{ b4Aff }}\in(0,1)$, {fr}`strictement décroissante.`{en}`strictly decreasing.`
::::

::::{weightDistribution}
:logic: 25
:abstraction: 35
:reasoning: 30
:calculation: 10
::::
:::::

:::::{question}
:questionType: MCQ
:questionId: 1
:questionIndex: 1

::::{questionStatement}
{fr}`Comparer`{en}`Compare` $f_{1}({{ x1Aff }})$ {fr}`et`{en}`and` $f_{1}({{ x2Aff }})$, {fr}`puis`{en}`then` $f_{2}({{ x1Aff }})$ {fr}`et`{en}`and` $f_{2}({{ x2Aff }})$, {fr}`sans calculer les valeurs exactes.`{en}`without calculating the exact values.`
::::

::::{questionHint}
{fr}`Utiliser la monotonie :`{en}`Use monotonicity:` ${{ x1Aff }}<{{ x2Aff }}$.
::::

::::{mcqAnswer}
:isRightAnswer: true
$f_{1}({{ x1Aff }}) < f_{1}({{ x2Aff }})$ {fr}`et`{en}`and` $f_{2}({{ x1Aff }}) > f_{2}({{ x2Aff }})$
::::

::::{mcqAnswer}
:isRightAnswer: false
$f_{1}({{ x1Aff }}) > f_{1}({{ x2Aff }})$ {fr}`et`{en}`and` $f_{2}({{ x1Aff }}) < f_{2}({{ x2Aff }})$
::::

::::{mcqAnswer}
:isRightAnswer: false
$f_{1}({{ x1Aff }}) < f_{1}({{ x2Aff }})$ {fr}`et`{en}`and` $f_{2}({{ x1Aff }}) < f_{2}({{ x2Aff }})$
::::

::::{mcqAnswer}
:isRightAnswer: false
$f_{1}({{ x1Aff }}) > f_{1}({{ x2Aff }})$ {fr}`et`{en}`and` $f_{2}({{ x1Aff }}) > f_{2}({{ x2Aff }})$
::::

::::{mcqAnswer}
:isRightAnswer: false
{fr}`Aucune de ces réponses n'est correcte`{en}`None of these answers are correct`
::::

::::{detailedSolution}
$f_{1}$ {fr}`est strictement croissante et`{en}`is strictly increasing and` ${{ x1Aff }}<{{ x2Aff }}$, {fr}`donc`{en}`so` $f_{1}({{ x1Aff }})<f_{1}({{ x2Aff }})$ ({fr}`soit`{en}`i.e.` ${{ b1Aff }}^{ {{ x1Aff }} }<{{ b1Aff }}^{ {{ x2Aff }} }$, {fr}`c'est-à-dire`{en}`that is` ${{ f1x1Aff }}<{{ f1x2Aff }}$).\
\
$f_{2}$ {fr}`est strictement décroissante et`{en}`is strictly decreasing and` ${{ x1Aff }}<{{ x2Aff }}$, {fr}`donc`{en}`so` $f_{2}({{ x1Aff }})>f_{2}({{ x2Aff }})$ ({fr}`soit`{en}`i.e.` $\left({{ b2Aff }}\right)^{ {{ x1Aff }} }>\left({{ b2Aff }}\right)^{ {{ x2Aff }} }$, {fr}`c'est-à-dire`{en}`that is` ${{ f2x1Aff }}>{{ f2x2Aff }}$).
::::

::::{weightDistribution}
:logic: 25
:abstraction: 30
:reasoning: 35
:calculation: 10
::::
:::::

`````