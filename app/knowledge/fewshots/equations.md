`````{exercise}
:title: Tester si une valeur est solution
:modules: 
:recommendedExecutionTime: 6
:level: Elementary
:chap: chap_equations_Inequalities_linearEquations_ESCP
:involvedConcepts: 
:originalSource: 
:visibility: All
:variations: 
:comment: Échauffement. Tester une valeur par substitution dans les deux membres, puis résoudre l'équation linéaire et donner l'ensemble solution.

````{python}
import random as rd
from pyxiscience.Mes_fctions_generalistes_bis import pxs_config, pxsl_latex_coefficient as lc

config_standard = pxs_config()

# Contraintes : a != 0, b != 0, solution entière non nulle (a | (c - b), c != b).
for _ in range(300):
    a = rd.choice([i for i in range(-10, 11) if i not in (0, 1, -1)])
    b = rd.choice([i for i in range(-15, 16) if i != 0])
    c = rd.randint(-15, 15)
    if c == b or (c - b) % a != 0:
        continue
    xSol = (c - b) // a
    if xSol == 0:
        continue
    delta = rd.choice([i for i in range(-3, 4) if i != 0])
    xTest1 = xSol
    xTest2 = xSol + delta
    break

bPrime = b - c
verifTest1 = a * xTest1 + b      # == c (xTest1 est solution)
verifTest2 = a * xTest2 + b      # != c (xTest2 n'est pas solution)
prodTest1 = a * xTest1
prodTest2 = a * xTest2

coefAAff = lc(a)
coefANumAff = lc(a, ones=True)
cstBAff = lc(b, ones=True, sign=True)
cstBPrimeAff = lc(bPrime, ones=True, sign=True)
prodTest1Aff = lc(prodTest1, ones=True)
prodTest2Aff = lc(prodTest2, ones=True)
xTest1ParenAff = str(xTest1) if xTest1 >= 0 else "(%d)" % xTest1
xTest2ParenAff = str(xTest2) if xTest2 >= 0 else "(%d)" % xTest2
repSolAff = str(xSol)
repSolParenAff = str(xSol) if xSol >= 0 else "(%d)" % xSol

globals()
````

:::::{question}
:questionType: STQ
:questionId: 0
:questionIndex: 0

::::{questionStatement}
On considère l'équation ${}{{coefAAff}}x {{cstBAff}} = {{c}}$. La valeur $x = {{xTest1}}$ est-elle solution ? Et la valeur $x = {{xTest2}}$ ? Justifier dans chaque cas en substituant la valeur dans les deux membres.
::::

::::{questionHint}
Pour tester une valeur, substitue-la dans les deux membres et vérifie si l'égalité est vraie.
::::

::::{detailedSolution}
Test de $x = {{xTest1}}$ :

\begin{equation*}
{{coefANumAff}} \times {{xTest1ParenAff}} {{cstBAff}} &= {{prodTest1Aff}} {{cstBAff}} \\
&= {{verifTest1}}.
\end{equation*}

Le membre de droite vaut ${}{{c}}$. Comme ${}{{verifTest1}} = {{c}}$, l'égalité est vraie : $x = {{xTest1}}$ est solution.

Test de $x = {{xTest2}}$ :

\begin{equation*}
{{coefANumAff}} \times {{xTest2ParenAff}} {{cstBAff}} &= {{prodTest2Aff}} {{cstBAff}} \\
&= {{verifTest2}}.
\end{equation*}

Le membre de droite vaut ${}{{c}}$. Comme ${}{{verifTest2}} \neq {{c}}$, l'égalité est fausse : $x = {{xTest2}}$ n'est pas solution.
::::

::::{weightDistribution}
:logic: 15
:abstraction: 15
:reasoning: 25
:calculation: 45
::::
:::::

:::::{question}
:questionType: STQ
:questionId: 1
:questionIndex: 1

::::{questionStatement}
Donner l'ensemble solution de l'équation ${}{{coefAAff}}x {{cstBAff}} = {{c}}$.
::::

::::{questionHint}
Mets l'équation sous la forme $ax + b = 0$, puis applique $x = -b/a$.
::::

::::{detailedSolution}
En soustrayant ${}{{c}}$ des deux membres, l'équation s'écrit ${}{{coefAAff}}x {{cstBPrimeAff}} = 0$, avec $a = {{a}} \neq 0$ et $b = {{bPrime}}$. Par le théorème d'unicité :

\begin{equation*}
x &= -\dfrac{b}{a} \\
&= -\dfrac{ {{bPrime}} }{ {{a}} } \\
&= {{repSolAff}}.
\end{equation*}

Vérification : ${}{{coefANumAff}} \times {{repSolParenAff}} {{cstBAff}} = {{c}}$. L'ensemble solution est $\{ {{repSolAff}} \}$.
::::

::::{weightDistribution}
:logic: 12
:abstraction: 18
:reasoning: 25
:calculation: 45
::::
:::::

`````
