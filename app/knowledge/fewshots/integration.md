`````{exercise}
:title: {fr}`Étude d'une fonction avec logarithme : limites, variations et intégration par parties`{en}`Study of a function involving a logarithm: limits, variations and integration by parts`
:modules: annale_bac
:recommendedExecutionTime: 30
:level: Intermediate
:chap:
:involvedConcepts: TYPE_BAC,Integration_by_Parts, Limits, Comparative_Growth
:originalSource: Exercice 4 du baccalauréat Amérique du Nord 21 mai 2026 (sujet 2)
:visibility: All
:variations:
:comment: Exercice d'analyse (fonction x(ln x)^2, deux IPP, théorème de la bijection) - non randomisé. Énoncé et solution officiels ; solution validée par Chabane.
:id: 4e6e2f22-5f5a-11f1-a8a1-0ed8d3b012a9

````{python}
import math
import random as rd
from sympy import symbols, exp, ln, sqrt, latex, Rational, nsolve
from pyxiscience.Mes_fctions_generalistes_bis import pxs_config, pxsl_res_num

config_standard = pxs_config()
x = symbols('x', positive=True, real=True)

# Fonction et identités officielles : f(x) = x (ln x)^2.
# L'exposant 2 est VERROUILLÉ (l'identité f = 4 (g(sqrt x))^2 de la Q2a, l'expression de f',
# le tableau de variation et les deux IPP avec la limite 1/4 ne valent que pour le carré).
# Seul paramètre randomisable proprement : le second membre de l'équation f(x) = seuil.
f = x * (ln(x)) ** 2
xCrit = exp(-2)
fMax = 4 * exp(-2)                      # = e^{-2} * (-2)^2, maximum local sur ]0 ; 1] (~0,541)

# Second membre entier de l'équation f(x) = seuil : seuil > 4/e^2 (~0,541),
# donc aucune solution sur ]0 ; 1] et une unique solution sur [1 ; +inf[. (Officiel : seuil = 2.)
seuil = rd.randint(1, 6)
alphaApprox = float(nsolve(f - seuil, 3))
alphaInf = math.floor(alphaApprox * 10) / 10
alphaSup = round(alphaInf + 0.1, 1)
limInt = Rational(1, 4)

fMaxAff = latex(fMax, **config_standard)
fMaxDecAff = pxsl_res_num(fMax, dec=2, egal=False)
seuilAff = str(seuil)
alphaApproxAff = pxsl_res_num(alphaApprox, dec=2, egal=False)
alphaInfAff = pxsl_res_num(alphaInf, dec=1, egal=False)
alphaSupAff = pxsl_res_num(alphaSup, dec=1, egal=False)
limIntAff = latex(limInt, **config_standard)

globals()
````

On considère la fonction $f$ définie sur l'intervalle $]0\,;\,+\infty[$ par
\begin{equation*}
f(x) = x(\ln x)^2.
\end{equation*}
On admet que la fonction $f$ est dérivable sur l'intervalle $]0\,;\,+\infty[$. On note $f'$ sa fonction dérivée.

:::::{question}
:questionType: STQ
:questionId: 0
:questionIndex: 0

::::{questionStatement}
Déterminer la limite de la fonction $f$ en $+\infty$.
::::

::::{questionHint}
Écrire $f(x) = x \times (\ln x)^2$ et utiliser la limite de $\ln x$ en $+\infty$, puis un produit de limites.
::::

::::{detailedSolution}
Pour tout réel $x > 0$, on a $f(x) = x \times (\ln x)^2$.

Comme $\ds \lim_{x \to +\infty} \ln x = +\infty$ et $\ds \lim_{x \to +\infty} x = +\infty$, on obtient par produit :
\begin{equation*}
\boxed{\lim_{x \to +\infty} f(x) = +\infty.}
\end{equation*}
::::

::::{weightDistribution}
:reasoning: 30
:logic: 20
:abstraction: 15
:calculation: 35
::::
:::::

Pour tout réel $x > 0$, on pose $g(x) = x \ln x$.

:::::{question}
:questionType: STQ
:questionId: 1
:questionIndex: 1

::::{questionStatement}
Démontrer que, pour tout réel $x > 0$, on a $f(x) = 4\bigl(g(\sqrt{x})\bigr)^2$.
::::

::::{questionHint}
Utiliser que $\ln\sqrt{x} = \dfrac{1}{2}\ln x$, puis développer ${}4\bigl(g(\sqrt{x})\bigr)^2$.
::::

::::{detailedSolution}
Soit $x \in\, ]0\,;\,+\infty[$. En utilisant $\ln\sqrt{x} = \dfrac{1}{2}\ln x$ :
\begin{equation*}
4\bigl(g(\sqrt{x})\bigr)^2 &= 4\bigl(\sqrt{x}\,\ln(\sqrt{x})\bigr)^2 \\
&= 4\left(\sqrt{x} \times \tfrac{1}{2}\ln x\right)^2 \\
&= 4 \times x \times \tfrac{1}{4}(\ln x)^2 \\
&= x(\ln x)^2 \\
&= f(x).
\end{equation*}
On a donc bien, pour tout réel $x > 0$ :
\begin{equation*}
\boxed{f(x) = 4\bigl(g(\sqrt{x})\bigr)^2.}
\end{equation*}
::::

::::{weightDistribution}
:reasoning: 20
:logic: 20
:abstraction: 15
:calculation: 45
::::
:::::

:::::{question}
:questionType: STQ
:questionId: 2
:questionIndex: 2

::::{questionStatement}
En déduire $\ds \lim_{x\to 0}f(x)$.
::::

::::{questionHint}
Par croissances comparées, $\ds\lim_{X\to 0}X\ln X=0$. Composer avec $X=\sqrt{x}$.
::::

::::{detailedSolution}
On sait que $\ds\lim_{x\to 0}\sqrt{x}=0$ et, par croissances comparées, $\ds\lim_{X\to 0}X\ln X=0$.

Par composition, $\ds\lim_{x\to 0}g(\sqrt{x})=\lim_{x\to 0}\sqrt{x}\,\ln(\sqrt{x})=0$.

D'après la question précédente, $f(x)=4\bigl(g(\sqrt{x})\bigr)^2$, donc par produit :
\begin{equation*}
\boxed{\lim_{x\to 0}f(x)=0.}
\end{equation*}
::::

::::{weightDistribution}
:reasoning: 35
:logic: 25
:abstraction: 25
:calculation: 15
::::
:::::

Dans cette question, on étudie les variations de la fonction $f$ sur l'intervalle $]0\,;\,+\infty[$.

:::::{question}
:questionType: STQ
:questionId: 3
:questionIndex: 3

::::{questionStatement}
Démontrer que, sur l'intervalle $]0\,;\,+\infty[$, $f'(x)=(\ln x)(2+\ln x)$.
::::

::::{questionHint}
$f$ est un produit : poser $u(x)=x$ et $v(x)=(\ln x)^2$, puis appliquer $f'=u'v+uv'$.
::::

::::{detailedSolution}
La fonction $f$ est de la forme $uv$ avec, pour tout $x\in\,]0\,;\,+\infty[$, $u(x)=x$ et $v(x)=(\ln x)^2$, d'où $u'(x)=1$ et $v'(x)=2\times\dfrac{1}{x}\times\ln x=\dfrac{2\ln x}{x}$.

Comme $f'=u'v+uv'$, on obtient pour tout $x\in\,]0\,;\,+\infty[$ :
\begin{equation*}
f'(x)&=1\times(\ln x)^2+x\times\dfrac{2\ln x}{x}\\
&=(\ln x)^2+2\ln x\\
&=(\ln x)(\ln x+2).
\end{equation*}
Donc, sur l'intervalle $]0\,;\,+\infty[$ :
\begin{equation*}
\boxed{f'(x)=(\ln x)(2+\ln x).}
\end{equation*}
::::

::::{weightDistribution}
:reasoning: 20
:logic: 15
:abstraction: 10
:calculation: 55
::::
:::::

:::::{question}
:questionType: STQ
:questionId: 4
:questionIndex: 4

::::{questionStatement}
En déduire les variations de la fonction $f$ sur l'intervalle $]0\,;\,+\infty[$.
::::

::::{questionHint}
Étudier séparément le signe de $\ln x$ et celui de ${}2+\ln x$, puis en déduire le signe du produit $f'(x)$.
::::

::::{detailedSolution}
On étudie le signe de $f'(x)=(\ln x)(2+\ln x)$.

$\bullet$ ${}2+\ln x>0\iff \ln x>-2\iff x>\mathrm{e}^{-2}$ ;

$\bullet$ $\ln x>0\iff x>1$.

On en déduit le signe de $f'$ sur $]0\,;\,+\infty[$ :

$\bullet$ sur $]0\,;\,\mathrm{e}^{-2}]$ : $\ln x<0$ et ${}2+\ln x<0$, donc $f'(x)>0$ ;

$\bullet$ sur $[\mathrm{e}^{-2}\,;\,1]$ : $\ln x<0$ et ${}2+\ln x>0$, donc $f'(x)<0$ ;

$\bullet$ sur $[1\,;\,+\infty[$ : $\ln x>0$ et ${}2+\ln x>0$, donc $f'(x)>0$.

Par conséquent, $f$ est strictement croissante sur $]0\,;\,\mathrm{e}^{-2}]$, strictement décroissante sur $[\mathrm{e}^{-2}\,;\,1]$, puis strictement croissante sur $[1\,;\,+\infty[$.
::::

::::{weightDistribution}
:reasoning: 25
:logic: 35
:abstraction: 15
:calculation: 25
::::
:::::

:::::{question}
:questionType: STQ
:questionId: 5
:questionIndex: 5

::::{questionStatement}
Donner la valeur exacte du maximum de la fonction $f$ sur l'intervalle $]0\,;\,1]$.
::::

::::{questionHint}
Sur $]0\,;\,1]$, $f$ croît jusqu'en $\mathrm{e}^{-2}$ puis décroît : le maximum est $f(\mathrm{e}^{-2})$. Calculer cette valeur.
::::

::::{detailedSolution}
Sur l'intervalle $]0\,;\,1]$, la fonction $f$ est croissante sur $]0\,;\,\mathrm{e}^{-2}]$ puis décroissante sur $[\mathrm{e}^{-2}\,;\,1]$ : son maximum est donc atteint en $x=\mathrm{e}^{-2}$.
\begin{equation*}
f(\mathrm{e}^{-2})&=\mathrm{e}^{-2}\bigl(\ln(\mathrm{e}^{-2})\bigr)^2\\
&=\mathrm{e}^{-2}\times(-2)^2\\
&={{fMaxAff}}.
\end{equation*}
Le maximum de $f$ sur $]0\,;\,1]$ vaut donc :
\begin{equation*}
\boxed{ {{fMaxAff}} \approx {{fMaxDecAff}}. }
\end{equation*}
::::

::::{weightDistribution}
:reasoning: 25
:logic: 20
:abstraction: 15
:calculation: 40
::::
:::::

On considère l'équation $f(x)={{seuilAff}}$.

:::::{question}
:questionType: STQ
:questionId: 6
:questionIndex: 6

::::{questionStatement}
Justifier que, sur l'intervalle $]0\,;\,+\infty[$, cette équation admet une unique solution. On note $\alpha$ cette solution.
::::

::::{questionHint}
Distinguer $]0\,;\,1]$ (comparer le maximum à ${}{{seuilAff}}$) et $[1\,;\,+\infty[$ (appliquer le théorème de la bijection).
::::

::::{detailedSolution}
$\bullet$ Sur l'intervalle $]0\,;\,1]$, le maximum de $f$ vaut ${}{{fMaxAff}} \approx {{fMaxDecAff}} < {{seuilAff}}$ : l'équation $f(x)={{seuilAff}}$ n'y admet donc aucune solution.

$\bullet$ Sur l'intervalle $[1\,;\,+\infty[$, la fonction $f$ est continue (car dérivable) et strictement croissante. De plus $f(1)=0<{{seuilAff}}$ et $\ds\lim_{x\to+\infty}f(x)=+\infty>{{seuilAff}}$.

D'après le théorème de la bijection (corollaire du théorème des valeurs intermédiaires), l'équation $f(x)={{seuilAff}}$ admet une unique solution sur $[1\,;\,+\infty[$.

En réunissant les deux intervalles, l'équation $f(x)={{seuilAff}}$ admet une unique solution $\alpha$ sur $]0\,;\,+\infty[$.
::::

::::{weightDistribution}
:reasoning: 35
:logic: 30
:abstraction: 20
:calculation: 15
::::
:::::

:::::{question}
:questionType: STQ
:questionId: 7
:questionIndex: 7

::::{questionStatement}
Donner un encadrement de $\alpha$ d'amplitude ${}0{,}1$.
::::

::::{questionHint}
Utiliser la calculatrice (ou un tableau de valeurs) pour localiser $\alpha$ entre deux décimaux distants de ${}0{,}1$.
::::

::::{detailedSolution}
À l'aide de la calculatrice, $\alpha\approx{{alphaApproxAff}}$. On en déduit l'encadrement d'amplitude ${}0{,}1$ :
\begin{equation*}
\boxed{ {{alphaInfAff}} \leqslant \alpha \leqslant {{alphaSupAff}}. }
\end{equation*}
::::

::::{weightDistribution}
:reasoning: 15
:logic: 15
:abstraction: 10
:calculation: 60
::::
:::::

Soit $a$ un nombre réel appartenant à l'intervalle $]0\,;\,1]$.

:::::{question}
:questionType: STQ
:questionId: 8
:questionIndex: 8

::::{questionStatement}
Donner une interprétation géométrique de $\ds\int_a^1 f(x)\,\mathrm{d}x$.
::::

::::{questionHint}
Déterminer le signe de $f$ sur $[a\,;\,1]$, puis relier l'intégrale à une aire.
::::

::::{detailedSolution}
Sur l'intervalle $[a\,;\,1]$, la fonction $f$ est positive. L'intégrale $\ds\int_a^1 f(x)\,\mathrm{d}x$ représente donc l'aire, exprimée en unités d'aire, du domaine délimité par la courbe représentative de $f$, l'axe des abscisses et les droites d'équations $x=a$ et $x=1$.
::::

::::{weightDistribution}
:reasoning: 30
:logic: 20
:abstraction: 40
:calculation: 10
::::
:::::

:::::{question}
:questionType: STQ
:questionId: 9
:questionIndex: 9

::::{questionStatement}
À l'aide d'une intégration par parties, justifier que :
\begin{equation*}
\int_a^1 f(x)\,\mathrm{d}x=-\dfrac{a^2}{2}(\ln a)^2-\int_a^1 x\ln x\,\mathrm{d}x.
\end{equation*}
::::

::::{questionHint}
Poser $u'(x)=x$ et $v(x)=(\ln x)^2$, d'où $u(x)=\dfrac{x^2}{2}$ et $v'(x)=\dfrac{2\ln x}{x}$.
::::

::::{detailedSolution}
On pose $u'(x)=x$ et $v(x)=(\ln x)^2$, d'où $u(x)=\dfrac{x^2}{2}$ et $v'(x)=\dfrac{2\ln x}{x}$. Ces fonctions sont continûment dérivables sur $[a\,;\,1]$, donc par intégration par parties :
\begin{equation*}
\int_a^1 f(x)\,\mathrm{d}x&=\left[\dfrac{x^2}{2}(\ln x)^2\right]_a^1-\int_a^1 \dfrac{x^2}{2}\times\dfrac{2\ln x}{x}\,\mathrm{d}x\\
&=\left(\dfrac{1}{2}(\ln 1)^2-\dfrac{a^2}{2}(\ln a)^2\right)-\int_a^1 x\ln x\,\mathrm{d}x\\
&=-\dfrac{a^2}{2}(\ln a)^2-\int_a^1 x\ln x\,\mathrm{d}x,
\end{equation*}
ce qui est le résultat demandé.
::::

::::{weightDistribution}
:reasoning: 25
:logic: 20
:abstraction: 15
:calculation: 40
::::
:::::

:::::{question}
:questionType: STQ
:questionId: 10
:questionIndex: 10

::::{questionStatement}
En utilisant à nouveau une intégration par parties, démontrer que :
\begin{equation*}
\int_a^1 f(x)\,\mathrm{d}x=-\dfrac{a^2}{2}(\ln a)^2+\dfrac{a^2}{2}\ln a+\dfrac{1}{4}-\dfrac{a^2}{4}.
\end{equation*}
::::

::::{questionHint}
Calculer $\ds\int_a^1 x\ln x\,\mathrm{d}x$ par IPP avec $u'(x)=x$ et $v(x)=\ln x$, puis reporter dans la question précédente.
::::

::::{detailedSolution}
On calcule d'abord $\ds\int_a^1 x\ln x\,\mathrm{d}x$ par intégration par parties, avec $u'(x)=x$ et $v(x)=\ln x$, d'où $u(x)=\dfrac{x^2}{2}$ et $v'(x)=\dfrac{1}{x}$ :
\begin{equation*}
\int_a^1 x\ln x\,\mathrm{d}x&=\left[\dfrac{x^2}{2}\ln x\right]_a^1-\int_a^1 \dfrac{x^2}{2}\times\dfrac{1}{x}\,\mathrm{d}x\\
&=-\dfrac{a^2}{2}\ln a-\int_a^1 \dfrac{x}{2}\,\mathrm{d}x\\
&=-\dfrac{a^2}{2}\ln a-\left[\dfrac{x^2}{4}\right]_a^1\\
&=-\dfrac{a^2}{2}\ln a-\dfrac{1}{4}+\dfrac{a^2}{4}.
\end{equation*}
En reportant dans le résultat de la question précédente :
\begin{equation*}
\int_a^1 f(x)\,\mathrm{d}x&=-\dfrac{a^2}{2}(\ln a)^2-\left(-\dfrac{a^2}{2}\ln a-\dfrac{1}{4}+\dfrac{a^2}{4}\right)\\
&=-\dfrac{a^2}{2}(\ln a)^2+\dfrac{a^2}{2}\ln a+\dfrac{1}{4}-\dfrac{a^2}{4},
\end{equation*}
ce qui est le résultat demandé.
::::

::::{weightDistribution}
:reasoning: 20
:logic: 20
:abstraction: 10
:calculation: 50
::::
:::::

:::::{question}
:questionType: STQ
:questionId: 11
:questionIndex: 11

::::{questionStatement}
Déterminer la limite de $\ds\int_a^1 f(x)\,\mathrm{d}x$ quand $a$ tend vers ${}0$.
::::

::::{questionHint}
Faire apparaître $a\ln a$ : $a^2(\ln a)^2=(a\ln a)^2$. Par croissances comparées, $\ds\lim_{a\to 0}a\ln a=0$.
::::

::::{detailedSolution}
On part de l'expression obtenue à la question précédente. Par croissances comparées, $\ds\lim_{a\to 0}a\ln a=0$, donc :

$\bullet$ $\ds\lim_{a\to 0}\dfrac{a^2}{2}(\ln a)^2=\lim_{a\to 0}\dfrac{1}{2}(a\ln a)^2=0$ ;

$\bullet$ $\ds\lim_{a\to 0}\dfrac{a^2}{2}\ln a=\lim_{a\to 0}\dfrac{a}{2}\times a\ln a=0$ ;

$\bullet$ $\ds\lim_{a\to 0}\left(\dfrac{1}{4}-\dfrac{a^2}{4}\right)=\dfrac{1}{4}$.

Par somme :
\begin{equation*}
\boxed{\lim_{a\to 0}\int_a^1 f(x)\,\mathrm{d}x={{limIntAff}}.}
\end{equation*}
::::

::::{weightDistribution}
:reasoning: 30
:logic: 25
:abstraction: 20
:calculation: 25
::::
:::::

`````
