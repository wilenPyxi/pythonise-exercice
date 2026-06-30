`````{exercise}
:title: Évaluation d'une fonction exponentielle et monotonie
:modules: 
:recommendedExecutionTime: 7
:level: Elementary
:chap: 
:involvedConcepts: 
:originalSource: 
:visibility: All
:variations: 
:comment: Échauffement (thème pur) : évaluation de x↦3^x en des entiers (dont les exposants négatifs), passage par (0,1), et monotonie déduite de la base.

````{python}
import random as rd

# Construction déterministe : base entière > 1 (donc f croissante), valeurs exactes.
b = rd.choice([2, 3, 4, 5])

f1 = b
f2 = b**2
f3 = b**3

fm1Aff = r'\dfrac{1}{' + str(b) + '}'
fm2Aff = r'\dfrac{1}{' + str(b**2) + '}'
monotonie = 'croissante' if b > 1 else 'décroissante'

globals()
````

Soit $f(x)={{ b }}^{x}$. Calculer $f(0)$, $f(1)$, $f(2)$, $f(3)$, puis $f(-1)$ et $f(-2)$.

:::::{question}
:questionType: STQ
:questionId: 0
:questionIndex: 0

::::{questionStatement}
Soit $f(x)={{ b }}^{x}$. Calculer $f(0)$, $f(1)$, $f(2)$, $f(3)$, puis $f(-1)$ et $f(-2)$.
::::

::::{questionHint}
Rappel : $b^{x}=1$ lorsque $x=0$ pour toute base $b>0$, et $b^{-n}=\dfrac{1}{b^{n}}$.
::::

::::{detailedSolution}
Pour les exposants positifs ou nuls : $f(0)=1$, $f(1)={{ f1 }}$, $f(2)={{ f2 }}$, $f(3)={{ f3 }}$.

En particulier $f(0)=1$ : le graphe d'une fonction exponentielle passe toujours par le point $(0,1)$.

Pour les exposants négatifs : $f(-1)={{ fm1Aff }}$ et $f(-2)={{ fm2Aff }}$.
::::

::::{weightDistribution}
:logic: 10
:abstraction: 15
:reasoning: 25
:calculation: 50
::::
:::::

:::::{question}
:questionType: STQ
:questionId: 1
:questionIndex: 1

::::{questionStatement}
En déduire si $f$ est croissante ou décroissante, et justifier à partir de la base.
::::

::::{questionHint}
Si $b>1$, la fonction $x\mapsto b^{x}$ est strictement croissante.
::::

::::{detailedSolution}
La base est $b={{ b }}>1$, donc $f$ est strictement {{ monotonie }} sur $\mathbb{R}$. On le vérifie sur les valeurs : ${{ fm2Aff }}<{{ fm1Aff }}<1<{{ f1 }}<{{ f2 }}<{{ f3 }}$, soit $f(-2)<f(-1)<f(0)<f(1)<f(2)<f(3)$.
::::

::::{weightDistribution}
:logic: 25
:abstraction: 35
:reasoning: 30
:calculation: 10
::::
:::::

`````
