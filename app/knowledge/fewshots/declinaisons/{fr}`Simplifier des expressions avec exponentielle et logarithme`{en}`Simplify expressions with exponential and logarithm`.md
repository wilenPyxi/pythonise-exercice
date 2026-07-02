`````{exercise}
:title: {fr}`Simplifier des expressions avec exponentielle et logarithme`{en}`Simplify expressions with exponential and logarithm`
:modules: 
:recommendedExecutionTime: 10
:level: Elementary
:chap: chap_expLogFunctions_logarithmicFunctions_ESCP
:involvedConcepts: 
:originalSource: 
:visibility: All
:variations: 
:comment: Échauffement (thème pur) : simplification via les relations réciproques e^(ln y)=y, ln(e^x)=x, b^(log_b y)=y, log_b(b^x)=x, y compris en composition. Aucune loi algébrique du logarithme.
:originalExerciseId: 2f1a6101-6599-11f1-a8a1-0ed8d3b012a9
:id: 07721958-74bf-11f1-a8a1-0ed8d3b012a9

````{python}
import random as rd

# Q1 : e^(ln y1)=y1, ln(e^x1)=x1, b1^(log_b1 y2)=y2
y1 = rd.randint(2, 20)
x1 = rd.randint(2, 15)
b1 = rd.choice([2, 3, 4, 5, 6, 7, 8, 9])
y2 = rd.randint(2, 20)
r1, r2, r3 = y1, x1, y2

# Q2 : log_b2(b2^x2)=x2 (x2 != 0, 1 pour éviter ^1), e^(ln(e^x3))=e^x3
b2 = rd.choice([2, 3, 4, 5, 6, 7, 8, 9])
x2 = rd.choice(list(range(-10, 0)) + list(range(2, 11)))
x3 = rd.randint(2, 10)
r4 = x2
r5Aff = "e^{%d}" % x3

globals()
````

:::::{question}
:questionType: FGQ
:solution: [["ord","{{ r1 }}","{{ r2 }}","{{ r3 }}"],["0","0","0"]]

::::{questionStatement}
{fr}`Simplifier`{en}`Simplify` $e^{\ln {{ y1 }}}$, $\ln(e^{ {{ x1 }} })$ {fr}`et`{en}`and` ${{ b1 }}^{\log_{ {{ b1 }} }({{ y2 }})}$.

$e^{\ln {{ y1 }}} =$ {input}`||70`

$\ln(e^{ {{ x1 }} }) =$ {input}`||70`

${{ b1 }}^{\log_{ {{ b1 }} }({{ y2 }})} =$ {input}`||70`
::::

::::{questionHint}
$e^{\ln y}=y$, $\ln(e^{x})=x$, $b^{\log_{b} y}=y$.
::::

::::{displayedSolution}
$e^{\ln {{ y1 }}} = {{ r1 }}$

$\ln(e^{ {{ x1 }} }) = {{ r2 }}$

${{ b1 }}^{\log_{ {{ b1 }} }({{ y2 }})} = {{ r3 }}$
::::

::::{detailedSolution}
{fr}`Par les relations réciproques :`{en}`By the reciprocal relations:` $e^{\ln {{ y1 }}}={{ r1 }}$, $\quad \ln(e^{ {{ x1 }} })={{ r2 }}$, $\quad {{ b1 }}^{\log_{ {{ b1 }} }({{ y2 }})}={{ r3 }}$.

{fr}`(respectivement`{en}`(respectively` $e^{\ln y}=y$ {fr}`avec`{en}`with` $y={{ y1 }}$ ; $\ln(e^{x})=x$ {fr}`avec`{en}`with` $x={{ x1 }}$ ; $b^{\log_{b} y}=y$ {fr}`avec`{en}`with` $b={{ b1 }}$, $y={{ y2 }}$.)
::::

::::{weightDistribution}
:logic: 20
:abstraction: 30
:reasoning: 30
:calculation: 20
::::
:::::

:::::{question}
:questionType: FGQ
:solution: [["ord","{{ r4 }}","${{ r5Aff }}$"],["0","0"]]

::::{questionStatement}
{fr}`Simplifier`{en}`Simplify` $\log_{ {{ b2 }} }({{ b2 }}^{ {{ x2 }} })$ {fr}`et`{en}`and` $e^{\ln(e^{ {{ x3 }} })}$.

$\log_{ {{ b2 }} }({{ b2 }}^{ {{ x2 }} }) =$ {input}`||70`

$e^{\ln(e^{ {{ x3 }} })} =$ {input}`||90`
::::

::::{questionHint}
{fr}`Pour la seconde, simplifier de l'intérieur vers l'extérieur : d'abord`{en}`For the second, simplify from the inside out: first` $\ln(e^{ {{ x3 }} })$.
::::

::::{displayedSolution}
$\log_{ {{ b2 }} }({{ b2 }}^{ {{ x2 }} }) = {{ r4 }}$

$e^{\ln(e^{ {{ x3 }} })} = {{ r5Aff }}$
::::

::::{detailedSolution}
{fr}`Par`{en}`By` $\log_{b}(b^{x})=x$ :

\begin{equation*}
\log_{ {{ b2 }} }({{ b2 }}^{ {{ x2 }} }) = {{ r4 }}.
\end{equation*}

{fr}`Pour la seconde,`{en}`For the second,` $\ln(e^{ {{ x3 }} })={{ x3 }}$, {fr}`puis`{en}`then` $e^{\ln(e^{ {{ x3 }} })}=e^{ {{ x3 }} }$ {fr}`(relation`{en}`(relation` $e^{\ln y}=y$ {fr}`avec`{en}`with` $y=e^{ {{ x3 }} }>0$) :

\begin{equation*}
e^{\ln(e^{ {{ x3 }} })} = {{ r5Aff }}.
\end{equation*}
::::

::::{weightDistribution}
:logic: 20
:abstraction: 35
:reasoning: 30
:calculation: 15
::::
:::::

`````