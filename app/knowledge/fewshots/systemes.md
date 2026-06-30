`````{exercise}
:title: Assortiment : solution unique mais non réalisable
:modules: 
:recommendedExecutionTime: 14
:level: Elementary
:chap: 
:involvedConcepts: 
:originalSource: 
:visibility: All
:variations: 
:comment: Appliqué (économie & gestion) : système 2×2 à solution unique mais non réalisable (quantité négative). Distinction « système soluble » vs « plan réalisable ».

````{python}
import random as rd
import numpy as np
import matplotlib.pyplot as plt
from sympy import Rational, latex
from pyxiscience.Mes_fctions_generalistes_bis import pxs_config, pxsl_latex_coefficient as lc

config_standard = pxs_config()

# solution entière, non réalisable (solR < 0) : (prix_A-prix_R) divise extra
for _ in range(2000):
    prix_A = rd.choice([10, 12, 14, 16, 18, 20])
    prix_R = rd.choice([4, 5, 6, 7, 8, 9, 10])
    quantite_totale = rd.choice([15, 20, 25, 30])
    if prix_A <= prix_R:
        continue
    extra = rd.randint(20, 80)
    if extra % (prix_A - prix_R) != 0:
        continue
    cout_total = quantite_totale * prix_A + extra
    solA = quantite_totale + extra // (prix_A - prix_R)
    solR = quantite_totale - solA
    if solR < 0 and solA > quantite_totale:
        break

# Rendus
prixA = prix_A
prixR = prix_R
quantiteTotale = quantite_totale
coutTotal = cout_total
prixRSignAff = lc(prix_R, sign=True)
prixRQtSignAff = lc(prix_R * quantite_totale, sign=True)
negPrixRSignAff = lc(-prix_R, sign=True)
prixMoins = prix_A - prix_R
coutMoins = cout_total - prix_R * quantite_totale
coutMoyenAff = latex(Rational(cout_total, quantite_totale))
rapportUnAff = latex(Rational(1, prix_A))
rapportDeuxAff = latex(Rational(1, prix_R))

# Figure (une seule fois) : droites D1 et D2 dans le plan (a, r)
amax = solA + 4
xs = np.linspace(-1, amax, 200)
r_d1 = quantite_totale - xs
r_d2 = (cout_total - prix_A * xs) / prix_R
fig, ax = plt.subplots(figsize=(6, 5.5))
ax.plot(xs, r_d1, color="tab:blue", linewidth=2, label="$D_1:a+r=%d$" % quantite_totale)
ax.plot(xs, r_d2, color="tab:red", linewidth=2, label="$D_2$ (coût total)")
ax.fill([0, quantite_totale, 0], [0, 0, quantite_totale], color="gray", alpha=0.15)
ax.text(quantite_totale * 0.18, quantite_totale * 0.18, "zone réalisable", color="gray", fontsize=9)
ax.plot([solA], [solR], "o", color="black", markersize=7)
ax.text(solA, solR, "  $(%d;%d)$" % (solA, solR), fontsize=10, va="top")
ax.axhline(y=0, color="k", linewidth=0.8)
ax.axvline(x=0, color="k", linewidth=0.8)
ax.set_xlabel("$a$ (kg Arabica)", fontsize=11)
ax.set_ylabel("$r$ (kg Robusta)", fontsize=11)
ax.set_title("Intersection hors du domaine réalisable", fontsize=11)
ax.grid(True, alpha=0.3)
ax.legend(fontsize=9, loc="upper right")
plt.tight_layout()
plt.show()

globals()
````

:::::{question}
:questionType: STQ
:questionId: 0
:questionIndex: 0

::::{questionStatement}
Un responsable logistique veut constituer un assortiment de deux cafés en grains : Arabica à ${}{{ prixA }}$ €/kg et Robusta à ${}{{ prixR }}$ €/kg. Il vise exactement ${}{{ quantiteTotale }}$ kg d'assortiment pour un coût total de ${}{{ coutTotal }}$ €. On note $a$ la quantité d'Arabica (kg) et $r$ celle de Robusta (kg). Modéliser la situation par un système de deux équations à deux inconnues.
::::

::::{questionHint}
Une équation pour la quantité totale, une équation pour le coût total.
::::

::::{detailedSolution}
Les contraintes de quantité totale et de coût total donnent :

\begin{equation*}
\begin{cases} 
a + r &= {{ quantiteTotale }} & (1) \\ 
{{ prixA }}a {{ prixRSignAff }}r &= {{ coutTotal }} & (2) 
\end{cases}
\end{equation*}
::::

::::{weightDistribution}
:logic: 20
:abstraction: 35
:reasoning: 30
:calculation: 15
::::
:::::

:::::{question}
:questionType: STQ
:questionId: 1
:questionIndex: 1

::::{questionStatement}
Résoudre le système, puis examiner le signe des quantités obtenues afin de déterminer si le plan d'assortiment est réalisable.
::::

::::{questionHint}
Les coefficients ne sont pas proportionnels (${}{{ rapportUnAff }}\neq {{ rapportDeuxAff }}$) : le système a une solution unique. Vérifier ensuite que $a\geq 0$ et $r\geq 0$.
::::

::::{detailedSolution}
Les rapports des coefficients diffèrent (${}{{ rapportUnAff }}\neq {{ rapportDeuxAff }}$) : droites sécantes, solution unique. De $(1)$ : $r={{ quantiteTotale }}-a$. On substitue dans $(2)$ :

\begin{equation*}
{{ prixA }}a + {{ prixR }}({{ quantiteTotale }} - a) &= {{ coutTotal }} \\
{{ prixA }}a {{ prixRQtSignAff }} {{ negPrixRSignAff }}a &= {{ coutTotal }} \\
{{ prixMoins }}a &= {{ coutMoins }} \\
a &= {{ solA }}.
\end{equation*}

\begin{equation*}
r &= {{ quantiteTotale }} - {{ solA }} \\
&= {{ solR }}.
\end{equation*}

La solution mathématique est $(a,r)=({{ solA }},{{ solR }})$. Comme $r={{ solR }}<0$, une quantité négative de Robusta n'a pas de sens : le système a bien une solution unique, mais le plan d'assortiment n'est pas réalisable.
::::

::::{weightDistribution}
:logic: 25
:abstraction: 30
:reasoning: 30
:calculation: 15
::::
:::::

:::::{question}
:questionType: STQ
:questionId: 2
:questionIndex: 2

::::{questionStatement}
Interpréter économiquement ce résultat : pourquoi ce plan d'assortiment est-il irréalisable ? La situation est représentée graphiquement en tête d'exercice.
::::

::::{questionHint}
Comparer le coût moyen visé au prix du café le plus cher.
::::

::::{detailedSolution}
Le coût moyen visé serait ${}{{ coutTotal }}/{{ quantiteTotale }}={{ coutMoyenAff }}$ €/kg. Or le café le plus cher (Arabica) ne coûte que ${}{{ prixA }}$ €/kg : aucun mélange de deux cafés à ${}{{ prixA }}$ et ${}{{ prixR }}$ €/kg ne peut atteindre une moyenne de ${}{{ coutMoyenAff }}$ €/kg. Le budget de ${}{{ coutTotal }}$ € est trop élevé pour ${}{{ quantiteTotale }}$ kg. Aucun plan réalisable ($a\geq 0$, $r\geq 0$) ne satisfait les deux contraintes : les droites se coupent en $({{ solA }},{{ solR }})$, hors du domaine de faisabilité (voir la figure en tête d'exercice).
::::

::::{weightDistribution}
:logic: 25
:abstraction: 35
:reasoning: 30
:calculation: 10
::::
:::::

`````