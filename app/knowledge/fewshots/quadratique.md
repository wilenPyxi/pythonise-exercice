`````{exercise}
:title: Racine double et produit nul
:modules: 
:recommendedExecutionTime: 6
:level: Elementary
:chap: chap_equations_Inequalities_radicalQuadraticEquations_ESCP
:involvedConcepts: 
:originalSource: 
:visibility: All
:variations: 
:comment: Échauffement. Cas Delta nul (racine double) et règle du produit nul.

````{python}
import random as rd
from sympy import symbols, latex, Rational
from pyxiscience.Mes_fctions_generalistes_bis import pxs_config

config_standard = pxs_config()
x = symbols('x')

# Carré parfait (m x - n)^2 = m^2 x^2 - 2 m n x + n^2 : discriminant nul.
m = rd.randint(2, 4)
n = rd.randint(1, 6)
a = m * m
b = -2 * m * n
c = n * n

bSquared = b * b
fourAC = 4 * a * c
negB = -b
twoA = 2 * a
doubleRoot = Rational(n, m)

eqAff = latex(a * x ** 2 + b * x + c, **config_standard)
factoredAff = latex((m * x - n) ** 2, **config_standard)
aAff = str(a)
bAff = str(b)
cAff = str(c)
bSquaredAff = str(bSquared)
fourACAff = str(fourAC)
negBAff = str(negB)
twoAAff = str(twoA)
doubleRootAff = latex(doubleRoot, **config_standard)

# Question 2 : produit nul x(alpha x - gamma) = 0, racines 0 et r = gamma/alpha.
alpha = rd.randint(2, 4)
r = rd.randint(2, 6)
gamma = alpha * r
alphaAff = str(alpha)
gammaAff = str(gamma)
rAff = str(r)

globals()
````

:::::{question}
:questionType: STQ
:questionId: 0
:questionIndex: 0

::::{questionStatement}
{fr}`Résoudre l'équation `{en}`Solve the equation `$\ds {{eqAff}} = 0${fr}`.`{en}`.`
::::

::::{questionHint}
{fr}`Calculer le discriminant : s'il est nul, il y a une racine double $\ds x_0 = \dfrac{-b}{2a}$.`{en}`Compute the discriminant: if it is zero, there is a double root $\ds x_0 = \dfrac{-b}{2a}$.`
::::

::::{detailedSolution}
{fr}`Avec `{en}`With `$\ds a = {{aAff}}${fr}`, `{en}`, `$\ds b = {{bAff}}${fr}`, `{en}`, `$\ds c = {{cAff}}${fr}`, le discriminant vaut :`{en}`, the discriminant is:`

\begin{equation*}
\ds \Delta &= ({{bAff}})^2 - 4 \times {{aAff}} \times {{cAff}} \\
&= {{bSquaredAff}} - {{fourACAff}} \\
&= 0.
\end{equation*}

{fr}`Comme $\ds \Delta = 0$, il existe une unique solution réelle (racine double) :`{en}`Since $\ds \Delta = 0$, there is a single real solution (double root):`

\begin{equation*}
\ds x_0 &= \frac{-b}{2a} \\
&= \frac{ {{negBAff}} }{ {{twoAAff}} } \\
&= {{doubleRootAff}}.
\end{equation*}

{fr}`On retrouve la forme factorisée `{en}`This matches the factored form `$\ds {{factoredAff}} = 0${fr}`, qui s'annule en `{en}`, which vanishes at `$\ds x = {{doubleRootAff}}${fr}`. L'ensemble solution est `{en}`. The solution set is `$\ds \left\{ {{doubleRootAff}} \right\}${fr}`.`{en}`.`
::::

::::{weightDistribution}
:logic: 15
:abstraction: 20
:reasoning: 25
:calculation: 40
::::
:::::

:::::{question}
:questionType: STQ
:questionId: 1
:questionIndex: 1

::::{questionStatement}
{fr}`Résoudre l'équation `{en}`Solve the equation `$\ds x({{alphaAff}}x - {{gammaAff}}) = 0${fr}`.`{en}`.`
::::

::::{questionHint}
{fr}`Le membre gauche est un produit : appliquer la règle du produit nul.`{en}`The left-hand side is a product: apply the zero-product rule.`
::::

::::{detailedSolution}
{fr}`Par la règle du produit nul, un produit est nul si et seulement si l'un de ses facteurs est nul :`{en}`By the zero-product rule, a product is zero if and only if one of its factors is zero:`

\begin{equation*}
\ds x({{alphaAff}}x - {{gammaAff}}) = 0 \quad\Longleftrightarrow\quad x = 0 \quad\text{ou}\quad x = {{rAff}}.
\end{equation*}

{fr}`Le second facteur donne `{en}`The second factor gives `$\ds {{alphaAff}}x - {{gammaAff}} = 0${fr}`, soit `{en}`, i.e. `$\ds x = {{rAff}}${fr}`. L'ensemble solution est `{en}`. The solution set is `$\ds \{0\,;\,{{rAff}}\}${fr}`.`{en}`.`
::::

::::{weightDistribution}
:logic: 18
:abstraction: 18
:reasoning: 24
:calculation: 40
::::
:::::

`````
