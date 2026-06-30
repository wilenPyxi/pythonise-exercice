`````{exercise}
:title: Seuil de rentabilité d'une entreprise
:modules: 
:recommendedExecutionTime: 18
:level: Advanced
:chap: 
:involvedConcepts: 
:originalSource: 
:visibility: All
:variations: 
:comment: Appliqué (économie & gestion) : profit comme différence recette − coût, seuil de rentabilité, interprétation des signes et lecture graphique.

````{python}
import random as rd
import math
import matplotlib.pyplot as plt
from sympy import symbols, latex, Rational
from pyxiscience.Mes_fctions_generalistes_bis import pxs_config, pxsl_latex_coefficient as lc
from pyxiscience.Mes_fctions_probabilistes_bis import pxsl_res_num

config_standard = pxs_config()
q = symbols('q')

# Tirage avec contraintes
for _ in range(2000):
    prix_unitaire = rd.choice(range(40, 105, 5))
    cout_variable = rd.choice(range(10, 55, 5))
    if prix_unitaire <= cout_variable:
        continue
    cout_fixe = rd.choice(range(500, 3100, 100))
    coef_profit = prix_unitaire - cout_variable
    q_seuil = Rational(cout_fixe, coef_profit)
    q_test_1 = rd.choice([10, 15, 20, 25, 30, 35, 40])
    q_test_2 = rd.choice([50, 55, 60, 65, 70, 75, 80])
    if q_test_1 < q_seuil < q_test_2:
        break

profit_expr = coef_profit * q - cout_fixe
q_seuil_entier = math.ceil(cout_fixe / coef_profit)
qSeuilExactAff = latex(q_seuil)
qSeuilDecimalAff = pxsl_res_num(q_seuil, dec=2, egal=False)

# Marges et profits aux points de test
marge_un = coef_profit * q_test_1
marge_deux = coef_profit * q_test_2
profit_un = marge_un - cout_fixe
profit_deux = marge_deux - cout_fixe

# Chaînes d'affichage
piMidUn = f"{prix_unitaire}q - ({cout_fixe} + {cout_variable}q)"
piMidDeux = f"{prix_unitaire}q - {cout_fixe} - {cout_variable}q"
piFinalAff = f"{coef_profit}q {lc(-cout_fixe, ones=True, sign=True)}"
line1Un = f"{coef_profit}\\times {q_test_1} - {cout_fixe}"
line2Un = f"{marge_un} - {cout_fixe}"
line1Deux = f"{coef_profit}\\times {q_test_2} - {cout_fixe}"
line2Deux = f"{marge_deux} - {cout_fixe}"

# Variables injectées (sans underscore)
prixUnit = prix_unitaire
coutVar = cout_variable
coutFixe = cout_fixe
coefProfit = coef_profit
qTestUn = q_test_1
qTestDeux = q_test_2
qSeuilEntier = q_seuil_entier
profitUn = profit_un
profitDeux = profit_deux

# Figure (construite une seule fois dans le bloc unique)
q_seuil_f = float(q_seuil)
fig, ax = plt.subplots(figsize=(6, 5))
q_vals = [0, 100]
R_vals = [prix_unitaire * v for v in q_vals]
C_vals = [cout_fixe + cout_variable * v for v in q_vals]
ax.plot(q_vals, R_vals, 'b-', linewidth=2, label=f'$R(q)={prix_unitaire}q$')
ax.plot(q_vals, C_vals, 'r-', linewidth=2, label=f'$C(q)={cout_fixe}+{cout_variable}q$')
y_seuil = prix_unitaire * q_seuil_f
ax.plot([q_seuil_f, q_seuil_f], [0, y_seuil], 'k--', linewidth=1)
ax.plot([0, q_seuil_f], [y_seuil, y_seuil], 'k--', linewidth=1)
ax.plot(q_seuil_f, y_seuil, 'ko', markersize=6)
ax.text(q_seuil_f, y_seuil + 200, '$q_0$', ha='center')
ax.set_xlabel('$q$ (unités)', fontsize=11)
ax.set_ylabel('Euros', fontsize=11)
ax.set_xlim(-5, 105)
ax.set_ylim(-200, max(R_vals[-1], C_vals[-1]) + 500)
ax.grid(True, alpha=0.3)
ax.legend(fontsize=10)
ax.axhline(y=0, color='k', linewidth=0.8)
ax.axvline(x=0, color='k', linewidth=0.8)
plt.tight_layout()
plt.show()

globals()
````

:::::{question}
:questionType: STQ
:questionId: 0
:questionIndex: 0

::::{questionStatement}
Une entreprise produit et vend $q\geq 0$ unités d'un bien. La recette est $R(q)={{ prixUnit }}q$ euros et le coût total est $C(q)={{ coutFixe }} + {{ coutVar }}q$ euros. Écrire la fonction profit $\Pi(q)=R(q)-C(q)$ et simplifier.
::::

::::{questionHint}
$\Pi(q)=R(q)-C(q)$ : penser à distribuer le signe moins sur les deux termes de $C(q)$.
::::

::::{detailedSolution}
Règle utilisée : différence de deux fonctions, puis regroupement des termes.

\begin{equation*}
\Pi(q) &= {{ piMidUn }} \\
&= {{ piMidDeux }} \\
&= {{ piFinalAff }}.
\end{equation*}
::::

::::{weightDistribution}
:logic: 15
:abstraction: 20
:reasoning: 30
:calculation: 35
::::
:::::

:::::{question}
:questionType: STQ
:questionId: 1
:questionIndex: 1

::::{questionStatement}
Déterminer le seuil de rentabilité $q_0$, c'est-à-dire la valeur de $q$ pour laquelle $\Pi(q)=0$.
::::

::::{questionHint}
Résoudre l'équation du premier degré ${}{{ piFinalAff }}=0$.
::::

::::{detailedSolution}
On résout $\Pi(q_0)=0$.

\begin{equation*}
{{ coefProfit }}q_0 - {{ coutFixe }} &= 0 \\
q_0 &= \frac{ {{ coutFixe }} }{ {{ coefProfit }} } \\
&= {{ qSeuilExactAff }} \approx {{ qSeuilDecimalAff }}.
\end{equation*}

L'entreprise atteint le seuil de rentabilité à partir de ${}{{ qSeuilEntier }}$ unités vendues (arrondi au nombre entier supérieur).
::::

::::{weightDistribution}
:logic: 20
:abstraction: 25
:reasoning: 30
:calculation: 25
::::
:::::

:::::{question}
:questionType: STQ
:questionId: 2
:questionIndex: 2

::::{questionStatement}
Calculer $\Pi({{ qTestUn }})$ et $\Pi({{ qTestDeux }})$, puis interpréter.
::::

::::{questionHint}
Substituer chaque valeur dans $\Pi(q)={{ piFinalAff }}$ et comparer avec le seuil $q_0$.
::::

::::{detailedSolution}
On évalue la fonction profit.

\begin{equation*}
\Pi({{ qTestUn }}) &= {{ line1Un }} \\
&= {{ line2Un }} \\
&= {{ profitUn }}.
\end{equation*}

\begin{equation*}
\Pi({{ qTestDeux }}) &= {{ line1Deux }} \\
&= {{ line2Deux }} \\
&= {{ profitDeux }}.
\end{equation*}

Pour $q={{ qTestUn }}<q_0$, l'entreprise est en perte (${}{{ profitUn }}$ euros) ; pour $q={{ qTestDeux }}>q_0$, elle réalise un bénéfice de ${}{{ profitDeux }}$ euros.
::::

::::{weightDistribution}
:logic: 15
:abstraction: 20
:reasoning: 30
:calculation: 35
::::
:::::

:::::{question}
:questionType: STQ
:questionId: 3
:questionIndex: 3

::::{questionStatement}
Sur la figure ci-dessus, identifier graphiquement le seuil de rentabilité comme l'intersection des courbes de $R$ et $C$.
::::

::::{questionHint}
Le seuil de rentabilité est le point où recette = coût, c'est-à-dire l'intersection des deux droites.
::::

::::{detailedSolution}
Au seuil de rentabilité, les courbes de la recette $R$ et du coût total $C$ se croisent : à gauche de $q_0$ le coût dépasse la recette (perte), à droite la recette dépasse le coût (bénéfice).

Sur le graphique, on observe que les deux droites se coupent en $q_0 \approx {{ qSeuilDecimalAff }}$, ce qui correspond au calcul algébrique effectué à la question précédente. Pour $q<q_0$, la droite rouge (coût) est au-dessus de la droite bleue (recette), indiquant une perte. Pour $q>q_0$, la situation s'inverse et l'entreprise réalise un profit.
::::

::::{weightDistribution}
:logic: 25
:abstraction: 30
:reasoning: 35
:calculation: 10
::::
:::::

`````
