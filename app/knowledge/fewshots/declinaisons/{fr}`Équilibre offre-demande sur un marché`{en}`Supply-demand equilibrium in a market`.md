`````{exercise}
:title: {fr}`Équilibre offre-demande sur un marché`{en}`Supply-demand equilibrium in a market`
:modules: 
:recommendedExecutionTime: 15
:level: Elementary
:chap: chap_lines_Systems_economicEquilibriumBreakeven_ESCP
:involvedConcepts: 
:originalSource: 
:visibility: All
:variations: 
:comment: Appliqué éco/gestion — prix et quantité d'équilibre comme intersection de la droite d'offre (croissante) et de la droite de demande (décroissante).
:id: 730a9473-74c0-11f1-a8a1-0ed8d3b012a9
:originalExerciseId: 0582ee6e-64e4-11f1-a8a1-0ed8d3b012a9

````{python}
import random as rd
from pyxiscience.Mes_fctions_generalistes_bis import pxs_config, pxsl_latex_coefficient as lc
config_standard = pxs_config()

# Offre croissante, demande décroissante, équilibre ENTIER dans le quadrant positif
for _ in range(300):
    a_offre = rd.randint(1, 5)
    b_offre = rd.randint(2, 10)
    a_demande = rd.randint(-5, -1)
    b_demande = rd.randint(max(15, b_offre + 10), 40)
    denom = a_offre - a_demande
    num = b_demande - b_offre
    if denom > 0 and num > 0 and num % denom == 0:
        repQ = num // denom
        repP = a_offre * repQ + b_offre
        if 2 <= repQ <= 12 and repP > 0:
            break

# Limites pour le graphique
q_max_graph = max(6.5, repQ * 1.3)
p_max_graph = max(32, b_demande + 3)

# Précalcul de l'affichage
slopeOffreAff = lc(a_offre)
interOffreAff = lc(b_offre, ones=True, sign=True)
slopeDemAff = lc(a_demande)
interDemAff = lc(b_demande, ones=True, sign=True)
slopeOffreSignAff = lc(a_offre, ones=True, sign=True)
slopeDemPlainAff = lc(a_demande, ones=True)
coefDiffAff = lc(a_offre - a_demande)
rhsAff = str(b_demande - b_offre)
aOffreAff = str(a_offre)
aDemandeAff = str(a_demande)
repQAff = str(repQ)
repPAff = str(repP)

# Libellés multilingues pour matplotlib
if pxs_lang == "fr":
    label_offre_prefix = "Offre : "
    label_demande_prefix = "Demande : "
    label_q_axis = r"$q$ (milliers)"
    label_p_axis = r"$p$ (euros)"
else:
    label_offre_prefix = "Supply: "
    label_demande_prefix = "Demand: "
    label_q_axis = r"$q$ (thousands)"
    label_p_axis = r"$p$ (euros)"

globals()
````

:::::{question}
:questionType: FGQ
:questionId: 0
:questionIndex: 0
:solution: [["ord","${{ a_offre }}$","${{ a_demande }}$"],["0","0"]]

::::{questionStatement}
{fr}`Sur le marché d'un bien de consommation, l'offre et la demande (prix`{en}`In the market for a consumer good, supply and demand (price` $p$ {fr}`en euros par unité, en fonction de la quantité`{en}`in euros per unit, as a function of quantity` $q$ {fr}`en milliers d'unités) sont`{en}`in thousands of units) are` $\ds \text{{fr}`Offre`{en}`Supply`} : p = {{slopeOffreAff}}q {{interOffreAff}}$ {fr}`et`{en}`and` $\ds \text{{fr}`Demande`{en}`Demand`} : p = {{slopeDemAff}}q {{interDemAff}}$. {fr}`Vérifier que la courbe d'offre est croissante et celle de demande décroissante, et interpréter économiquement.`{en}`Verify that the supply curve is increasing and the demand curve is decreasing, and interpret economically.`
- {fr}`Pente de l'offre :`{en}`Slope of supply:` {input}`||80` 
- {fr}`Pente de la demande :`{en}`Slope of demand:` {input}`||80`
::::

::::{questionHint}
{fr}`Le signe de la pente donne le sens de variation.`{en}`The sign of the slope gives the direction of variation.`
::::

::::{displayedSolution}
- {fr}`Pente offre`{en}`Supply slope` ${{ a_offre }}$ 
- {fr}`Pente demande`{en}`Demand slope` ${{ a_demande }}$
::::

::::{detailedSolution}
{fr}`La droite d'offre`{en}`The supply line` $p = {{slopeOffreAff}}q {{interOffreAff}}$ {fr}`a une pente`{en}`has a slope` ${{slopeOffreSignAff}} > 0$ : {fr}`elle est croissante. Économiquement, les producteurs offrent davantage quand le prix monte. La droite de demande`{en}`it is increasing. Economically, producers supply more when the price rises. The demand line` $p = {{slopeDemAff}}q {{interDemAff}}$ {fr}`a une pente`{en}`has a slope` ${{slopeDemPlainAff}} < 0$ : {fr}`elle est décroissante. Les consommateurs demandent moins quand le prix monte.`{en}`it is decreasing. Consumers demand less when the price rises.`
::::

::::{weightDistribution}
:logic: 18
:abstraction: 22
:reasoning: 35
:calculation: 25
::::
:::::

:::::{question}
:questionType: FGQ
:questionId: 1
:questionIndex: 1
:solution: [["ord","${{ repQAff }}$","${{ repPAff }}$"],["0","0"]]

::::{questionStatement}
{fr}`Déterminer la quantité d'équilibre`{en}`Determine the equilibrium quantity` $q^*$ {fr}`et le prix d'équilibre`{en}`and the equilibrium price` $p^*$ {fr}`en résolvant le système formé par les deux équations.`{en}`by solving the system formed by the two equations.`
- $q^*$ = {input}`||80` 
- $p^*$ = {input}`||80`
::::

::::{questionHint}
{fr}`À l'équilibre, offre = demande : égale les deux expressions de`{en}`At equilibrium, supply = demand: equate the two expressions of` $p$.
::::

::::{displayedSolution}
- $q^* = {{ repQAff }}$ 
- $p^* = {{ repPAff }}$
::::

::::{detailedSolution}
{fr}`On égale offre et demande :`{en}`We equate supply and demand:`

\begin{equation*}
{{slopeOffreAff}}q^* {{interOffreAff}} &= {{slopeDemAff}}q^* {{interDemAff}} \\
{{coefDiffAff}}q^* &= {{rhsAff}} \\
q^* &= {{repQAff}}.
\end{equation*}

{fr}`En reportant dans l'offre :`{en}`Substituting into the supply:`

\begin{equation*}
p^* &= {{aOffreAff}} \times {{repQAff}} {{interOffreAff}} \\
&= {{repPAff}}.
\end{equation*}

{fr}`Vérification par la demande :`{en}`Verification by demand:` ${{aDemandeAff}} \times {{repQAff}} {{interDemAff}} = {{repPAff}}$. {fr}`L'équilibre est`{en}`The equilibrium is` $q^* = {{repQAff}}$ {fr}`milliers d'unités au prix`{en}`thousands of units at price` $p^* = {{repPAff}}$ {fr}`€ par unité.`{en}`€ per unit.`
::::

::::{weightDistribution}
:logic: 15
:abstraction: 20
:reasoning: 30
:calculation: 35
::::
:::::

:::::{question}
:questionType: FGQ
:questionId: 2
:questionIndex: 2
:solution: [["ord","${{ repQAff }}$","${{ repPAff }}$"],["0","0"]]

::::{questionStatement}
{fr}`Représenter les deux droites sur un graphique clairement légendé et repérer le point d'équilibre.`{en}`Represent the two lines on a clearly labeled graph and identify the equilibrium point.`\
\
{fr}`Point d'équilibre`{en}`Equilibrium point` $E${fr}` `: 
- {fr}`abscisse`{en}`x-coordinate`{fr}` `: {input}`||80` 
- {fr}`ordonnée`{en}`y-coordinate`{fr}` `: {input}`||80`
::::

::::{questionHint}
{fr}`Trace les deux droites ; leur intersection est le point d'équilibre`{en}`Draw the two lines; their intersection is the equilibrium point` $E$.
::::

::::{displayedSolution}
{fr}`Point d'équilibre`{en}`Equilibrium point` $E${fr}` `: 
- {fr}`abscisse`{en}`x-coordinate`{fr}` `: ${{ repQAff }}$ 
- {fr}`ordonnée`{en}`y-coordinate`{fr}` `: ${{ repPAff }}$
::::

::::{detailedSolution}
{fr}`Les deux droites se coupent au point d'équilibre`{en}`The two lines intersect at the equilibrium point` $E({{repQAff}}\,;\,{{repPAff}})$ :

```{python}
import numpy as np
import matplotlib.pyplot as plt

# Libellés pour matplotlib : moteur mathtext, donc PAS de \displaystyle ni \; (non supportés).
def slopeTerm(a):
    if a == 1: return "q"
    if a == -1: return "-q"
    return f"{a}q"

def interTerm(b):
    if b == 0: return ""
    return f" + {b}" if b > 0 else f" - {abs(b)}"

q = np.linspace(0, q_max_graph, 200)
offre = a_offre * q + b_offre
demande = a_demande * q + b_demande

fig, ax = plt.subplots(figsize=(6, 6))
ax.plot(q, offre, color="blue", lw=2, label=f"{label_offre_prefix}$p = {slopeTerm(a_offre)}{interTerm(b_offre)}$")
ax.plot(q, demande, color="red", lw=2, label=f"{label_demande_prefix}$p = {slopeTerm(a_demande)}{interTerm(b_demande)}$")

ax.plot(repQ, repP, "ko", markersize=6)
ax.annotate(f"$E({repQ}\\,;\\,{repP})$", xy=(repQ, repP), xytext=(repQ + 0.15, repP + 1.2), fontsize=11)
ax.plot([repQ, repQ], [0, repP], ls="--", color="0.5", lw=1)
ax.plot([0, repQ], [repP, repP], ls="--", color="0.5", lw=1)

ax.annotate("", xy=(q_max_graph + 0.5, 0), xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="black", lw=1.2))
ax.annotate("", xy=(0, p_max_graph), xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="black", lw=1.2))
ax.text(q_max_graph + 0.6, -0.5, label_q_axis, ha="center", fontsize=11)
ax.text(-0.4, p_max_graph, label_p_axis, ha="center", fontsize=11)

q_step = max(1, int(q_max_graph / 6))
for x in range(q_step, int(q_max_graph) + 1, q_step):
    ax.plot([x, x], [-0.3, 0.3], color="black", lw=1)
    ax.text(x, -1.0, str(x), ha="center", fontsize=9)

p_step = max(5, int(p_max_graph / 6))
for y in range(p_step, int(p_max_graph) + 1, p_step):
    ax.plot([-0.1, 0.1], [y, y], color="black", lw=1)
    ax.text(-0.35, y, str(y), ha="right", va="center", fontsize=9)
ax.text(-0.35, 0, "0", ha="right", va="center", fontsize=9)

ax.legend(loc="upper right", fontsize=10)
ax.set_xlim(-0.5, q_max_graph + 1)
ax.set_ylim(-2, p_max_graph + 1)
ax.axis("off")
plt.tight_layout()
plt.show()
```

{fr}`L'offre (croissante) et la demande (décroissante) se croisent en`{en}`Supply (increasing) and demand (decreasing) intersect at` $E({{repQAff}}\,;\,{{repPAff}})$, {fr}`qui matérialise le prix où le marché s'équilibre.`{en}`which represents the price where the market reaches equilibrium.`
::::

::::{weightDistribution}
:logic: 20
:abstraction: 25
:reasoning: 35
:calculation: 20
::::
:::::

`````