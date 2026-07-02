`````{exercise}
:originalExerciseId: a6a3c85d-689a-11f1-a8a1-0ed8d3b012a9
:title: {fr}`Lecture graphique du sens de variation et des extremums`{en}`Graphical reading of monotonicity and extrema`
:modules: fund_of_math_I_ESCP
:recommendedExecutionTime: 10
:level: Elementary
:chap: chap_extremaCurveSketching_monotonicityRelativeExtrema_ESCP
:involvedConcepts: 
:originalSource: 
:visibility: All
:variations: 
:comment: Échauffement (thème pur) : lecture sur une courbe des intervalles de croissance/décroissance, du minimum et du maximum, et comparaison de deux images par la monotonie. Aucune dérivée.
:id: e2835bb5-74b2-11f1-a8a1-0ed8d3b012a9

````{python}
import random as rd
# ──────────────────────────────────────────────────────────────────────────
# MÉTHODE CONSTRUCTIVE — partir de la réponse (les extremums et la structure)
# ──────────────────────────────────────────────────────────────────────────
# On veut une fonction continue sur [xMin, xMax] avec :
#   - un minimum global en (x2, y2)
#   - un maximum global en (x3, y3)
#   - décroissante sur [xMin, x2], croissante sur [x2, x3], décroissante sur [x3, xMax]
#
# On tire d'abord les extremums (la réponse), puis on place les points de départ
# et d'arrivée de manière cohérente (y1 et y4 entre le min et le max).

xMin = rd.randint(-6, -3)
xMax = rd.randint(4, 7)

# Abscisses des extremums : x2 < x3
x2 = rd.randint(xMin + 2, xMin + 4)
x3 = rd.randint(x2 + 2, xMax - 2) if xMax - 2 >= x2 + 2 else x2 + 2

# Valeurs des extremums (la réponse)
y2 = rd.randint(-3, -1)  # minimum
y3 = rd.randint(3, 5)    # maximum

minVal = y2
maxVal = y3

# Points de départ et d'arrivée : ordonnées entre min et max
y1 = rd.randint(2, 4)  # au-dessus du min, en dessous du max
y4 = rd.randint(0, 2)  # idem

# Points remarquables pour le tracé
x1 = xMin
x4 = xMax

# Question 3 : comparaison par monotonie sur l'intervalle de croissance [x2, x3]
# On tire xComp1 < xComp2 dans cet intervalle -> f(xComp1) < f(xComp2)
xComp1 = rd.randint(x2 + 1, x3 - 2) if x3 - x2 > 2 else x2 + 1
xComp2 = x3
# ──────────────────────────────────────────────────────────────────────────
# MÉTHODE CONSTRUCTIVE — partir de la réponse (la comparaison par monotonie)
# ──────────────────────────────────────────────────────────────────────────
# La réponse attendue est : f(xComp1) < f(xComp2) car f est croissante sur [x2, x3]
# et xComp1 < xComp2 appartiennent à cet intervalle.
#
# Les variables xMin, xMax, x2, x3, y2, y3, minVal, maxVal, xComp1, xComp2
# sont déjà définies dans le bloc précédent. On les réutilise pour construire
# l'énoncé de cette question.

# === Ajouts conversion FGQ ===
minValSolAff = str(minVal)
x2SolAff = str(x2)
maxValSolAff = str(maxVal)
x3SolAff = str(x3)
globals()
````
:::::{question}
:questionType: MCQ

::::{questionStatement}
{fr}`La figure ci-dessous représente la courbe d'une fonction`{en}`The figure below represents the curve of a function` $f$ {fr}`définie sur`{en}`defined on` $[{{ xMin }}\,;\,{{ xMax }}]$. {fr}`Lire les intervalles sur lesquels`{en}`Read the intervals on which` $f$ {fr}`est croissante, puis ceux sur lesquels`{en}`is increasing, then those on which` $f$ {fr}`est décroissante.`{en}`is decreasing.`

```{python}
import matplotlib.pyplot as plt
import numpy as np

def bez(p0, p1, p2, p3, t):
    return (1-t)**3*p0 + 3*(1-t)**2*t*p1 + 3*(1-t)*t**2*p2 + t**3*p3

t = np.linspace(0, 1, 60)
fig, ax = plt.subplots(figsize=(6, 4.5))
segments = [((x1, y1), (x1+1, (y1+y2)/2), (x2-1, y2+0.5), (x2, y2)),
            ((x2, y2), ((x2+x3)/2, (y2+y3)/2), (x3-1, y3-0.5), (x3, y3)),
            ((x3, y3), (x3+1, (y3+y4)/2), (x4-1, y4+0.5), (x4, y4))]
for P0, C1, C2, P1 in segments:
    ax.plot(bez(P0[0], C1[0], C2[0], P1[0], t), bez(P0[1], C1[1], C2[1], P1[1], t),
            color="#1f77b4", linewidth=2)
pts = [(x1, y1, "right", "bottom"), (x2, y2, "left", "top"),
       (x3, y3, "left", "bottom"), (x4, y4, "left", "top")]
for px, py, ha, va in pts:
    ax.plot(px, py, "o", color="red", markersize=5)
    ax.annotate(f"$({px}\\,;\\,{py})$", (px, py), textcoords="offset points",
                xytext=(6 if ha == "left" else -6, 6 if va == "bottom" else -10),
                ha=ha, fontsize=9)
ax.axhline(0, color="k", linewidth=0.8)
ax.axvline(0, color="k", linewidth=0.8)
ax.set_xticks(range(xMin, xMax+1))
ax.set_yticks(range(y2, y3+1))
ax.set_xlabel("$x$")
ax.set_ylabel("$y$")
ax.grid(True, alpha=0.3)
plt.show()
```
::::

::::{questionHint}
{fr}`Lire les intervalles de croissance (courbe montante) et de décroissance (courbe descendante) directement sur la courbe.`{en}`Read the intervals of increase (rising curve) and decrease (falling curve) directly from the curve.`
::::

::::{mcqAnswer}
:isRightAnswer: true
{fr}`Croissante sur`{en}`Increasing on` $[{{ x2 }}\,;\,{{ x3 }}]$ {fr}`; décroissante sur`{en}`; decreasing on` $[{{ xMin }}\,;\,{{ x2 }}]$ {fr}`et`{en}`and` $[{{ x3 }}\,;\,{{ xMax }}]$
::::

::::{mcqAnswer}
:isRightAnswer: false
{fr}`Décroissante sur`{en}`Decreasing on` $[{{ x2 }}\,;\,{{ x3 }}]$ {fr}`; croissante sur`{en}`; increasing on` $[{{ xMin }}\,;\,{{ x2 }}]$ {fr}`et`{en}`and` $[{{ x3 }}\,;\,{{ xMax }}]$
::::

::::{mcqAnswer}
:isRightAnswer: false
{fr}`Croissante sur tout`{en}`Increasing on the whole` $[{{ xMin }}\,;\,{{ xMax }}]$
::::

::::{mcqAnswer}
:isRightAnswer: false
{fr}`Aucune de ces réponses n'est correcte`{en}`None of these answers are correct`
::::

::::{detailedSolution}
{fr}`La courbe descend de`{en}`The curve falls from` $x={{ xMin }}$ {fr}`à`{en}`to` $x={{ x2 }}$ : $f$ {fr}`est décroissante sur`{en}`is decreasing on` $[{{ xMin }}\,;\,{{ x2 }}]$. {fr}`Elle monte de`{en}`It rises from` $x={{ x2 }}$ {fr}`à`{en}`to` $x={{ x3 }}$ : $f$ {fr}`est croissante sur`{en}`is increasing on` $[{{ x2 }}\,;\,{{ x3 }}]$. {fr}`Elle redescend de`{en}`It falls again from` $x={{ x3 }}$ {fr}`à`{en}`to` $x={{ xMax }}$ : $f$ {fr}`est décroissante sur`{en}`is decreasing on` $[{{ x3 }}\,;\,{{ xMax }}]$.
::::

::::{weightDistribution}
:logic: 15
:abstraction: 25
:reasoning: 35
:calculation: 25
::::
:::::

:::::{question}
:questionType: FGQ
:solution: [["ord","${{ minValSolAff }}$","${{ x2SolAff }}$","${{ maxValSolAff }}$","${{ x3SolAff }}$"],["0","0","0","0"]]

::::{questionStatement}
{fr}`Lire le minimum et le maximum de`{en}`Read the minimum and maximum of` $f$ {fr}`sur`{en}`on` $[{{ xMin }}\,;\,{{ xMax }}]$, {fr}`et préciser les abscisses où ils sont atteints.`{en}`and specify the abscissas where they are attained.`

{fr}`minimum`{en}`minimum` $=$ {input}`||60` {fr}`atteint en`{en}`attained at` $x =$ {input}`||60` {fr}`; maximum`{en}`; maximum` $=$ {input}`||60` {fr}`atteint en`{en}`attained at` $x =$ {input}`||60`
::::

::::{questionHint}
{fr}`Repérer le point le plus bas et le point le plus haut de la courbe.`{en}`Identify the lowest point and the highest point of the curve.`
::::

::::{displayedSolution}
{fr}`minimum`{en}`minimum` $= {{ minVal }}$ {fr}`atteint en`{en}`attained at` $x = {{ x2 }}$ ; {fr}`maximum`{en}`maximum` $= {{ maxVal }}$ {fr}`atteint en`{en}`attained at` $x = {{ x3 }}$
::::

::::{detailedSolution}
{fr}`Le point le plus bas est`{en}`The lowest point is` $({{ x2 }}\,;\,{{ minVal }})$ : {fr}`le minimum de`{en}`the minimum of` $f$ {fr}`sur`{en}`on` $[{{ xMin }}\,;\,{{ xMax }}]$ {fr}`est`{en}`is` ${{ minVal }}$, {fr}`atteint en`{en}`attained at` $x={{ x2 }}$. {fr}`Le point le plus haut est`{en}`The highest point is` $({{ x3 }}\,;\,{{ maxVal }})$ : {fr}`le maximum est`{en}`the maximum is` ${{ maxVal }}$, {fr}`atteint en`{en}`attained at` $x={{ x3 }}$.
::::

::::{weightDistribution}
:logic: 15
:abstraction: 25
:reasoning: 35
:calculation: 25
::::
:::::

:::::{question}
:questionType: MCQ

::::{questionStatement}
{fr}`Justifier, à partir du sens de variation, que`{en}`Justify, from the monotonicity, that` $f({{ xComp1 }}) < f({{ xComp2 }})$.
::::

::::{questionHint}
{fr}`Observer que`{en}`Observe that` ${{ xComp1 }}$ {fr}`et`{en}`and` ${{ xComp2 }}$ {fr}`appartiennent au même intervalle de croissance.`{en}`belong to the same interval of increase.`
::::

::::{mcqAnswer}
:isRightAnswer: true
{fr}`$f$ est croissante sur`{en}`$f$ is increasing on` $[{{ x2 }}\,;\,{{ x3 }}]$ {fr}`qui contient`{en}`which contains` ${{ xComp1 }}$ {fr}`et`{en}`and` ${{ xComp2 }}$, {fr}`et`{en}`and` ${{ xComp1 }}<{{ xComp2 }}$
::::

::::{mcqAnswer}
:isRightAnswer: false
{fr}`$f$ est décroissante sur cet intervalle`{en}`$f$ is decreasing on this interval`
::::

::::{mcqAnswer}
:isRightAnswer: false
{fr}`$f$ est constante sur cet intervalle`{en}`$f$ is constant on this interval`
::::

::::{mcqAnswer}
:isRightAnswer: false
{fr}`Aucune de ces réponses n'est correcte`{en}`None of these answers are correct`
::::

::::{detailedSolution}
{fr}`On a`{en}`We have` ${{ xComp1 }}<{{ xComp2 }}$, {fr}`et`{en}`and` $f$ {fr}`est croissante sur`{en}`is increasing on` $[{{ x2 }}\,;\,{{ x3 }}]$, {fr}`intervalle qui contient`{en}`an interval that contains` ${{ xComp1 }}$ {fr}`et`{en}`and` ${{ xComp2 }}$. {fr}`Par définition de la croissance,`{en}`By definition of increasing function,` ${{ xComp1 }}<{{ xComp2 }}$ {fr}`entraîne`{en}`implies` $f({{ xComp1 }})<f({{ xComp2 }})$.
::::

::::{weightDistribution}
:logic: 25
:abstraction: 30
:reasoning: 35
:calculation: 10
::::
:::::
`````