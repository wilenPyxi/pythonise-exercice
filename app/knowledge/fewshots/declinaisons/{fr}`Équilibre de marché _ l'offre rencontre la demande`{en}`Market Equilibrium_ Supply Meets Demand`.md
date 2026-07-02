`````{exercise}
:title: {fr}`Équilibre de marché : l'offre rencontre la demande`{en}`Market Equilibrium: Supply Meets Demand`
:modules: 
:recommendedExecutionTime: 10
:level: Elementary
:chap: chap_lines_Systems_economicEquilibriumBreakeven_ESCP
:involvedConcepts: 
:originalSource: Session 4 — Erwan Lamy, ESCP Business School
:visibility: All
:variations: 
:comment: Appliqué (micro-économie) : sens de variation de l'offre et de la demande, point d'équilibre par résolution de S(q) = D(q), vérification.
:id: 0924e9e6-74c0-11f1-a8a1-0ed8d3b012a9
:originalExerciseId: 0177637c-64e3-11f1-a8a1-0ed8d3b012a9

````{python}
import random as rd
from pyxiscience.Mes_fctions_generalistes_bis import pxs_config, pxsl_latex_coefficient as lc, pxsl_format_number
# --- Helpers PyxiScience (definis inline, autonomes : aucun import externe) ---

config_standard = pxs_config()

# S croissante (penteS>0), D decroissante (penteD<0), ordD>ordS,
# equilibre q* entier positif
for _ in range(300):
    penteS = rd.randint(1, 5)
    ordS = rd.randint(2, 10)
    penteD = rd.randint(-5, -1)
    ordD = rd.randint(15, 30)
    if ordD > ordS and (ordD - ordS) % (penteS - penteD) == 0:
        qStar = (ordD - ordS) // (penteS - penteD)
        if qStar > 0:
            break

pStar = penteS * qStar + ordS
pStarVerif = penteD * qStar + ordD     # = pStar
pots = qStar * 100

# Affichage
penteSCoefAff = lc(penteS); ordSConstAff = lc(ordS, ones=True, sign=True)
penteDCoefAff = lc(penteD); ordDConstAff = lc(ordD, ones=True, sign=True)
penteSAff = str(penteS); penteDAff = str(penteD)
penteDiffAff = lc(penteS - penteD); rhsEq = ordD - ordS

globals()
````

{fr}`Sur le marché du miel bio (prix `{en}`On the organic honey market (price `$p${fr}` en €/pot, quantité `{en}` in €/jar, quantity `$q${fr}` en centaines de pots par semaine), l'offre et la demande sont `{en}` in hundreds of jars per week), supply and demand are `$S(q) = {{penteSCoefAff}}q {{ordSConstAff}}${fr}` et `{en}` and `$D(q) = {{penteDCoefAff}}q {{ordDConstAff}}$.

:::::{question}
:questionType: FGQ
:questionId: 0
:questionIndex: 0
:solution: [["ord","${{ penteS }}$","${{ ordS }}$","${{ penteD }}$","${{ ordD }}$"],["0","0","0","0"]]

::::{questionStatement}
{fr}`Vérifier que `{en}`Check that `$S${fr}` est croissante et `{en}` is increasing and `$D${fr}` décroissante, et donner leurs coefficients directeurs et ordonnées à l'origine.`{en}` decreasing, and give their slopes and y-intercepts.`
- $S$ {fr}`: coefficient directeur`{en}`: slope` {input}`||80` {fr}`, ordonnée à l'origine`{en}`, y-intercept` {input}`||80` 
- $D$ {fr}`: coefficient directeur`{en}`: slope` {input}`||80` {fr}`, ordonnée à l'origine`{en}`, y-intercept` {input}`||80`
::::

::::{questionHint}
{fr}`Le signe du coefficient directeur donne le sens de variation.`{en}`The sign of the slope gives the direction of variation.`
::::

::::{displayedSolution}
- $S$ {fr}`: pente`{en}`: slope` ${{ penteS }}$ {fr}`, ordonnée`{en}`, intercept` ${{ ordS }}$ 
- $D$ {fr}`: pente`{en}`: slope` ${{ penteD }}$ {fr}`, ordonnée`{en}`, intercept` ${{ ordD }}$
::::

::::{detailedSolution}
{fr}`Pour `{en}`For `$S(q) = {{penteSCoefAff}}q {{ordSConstAff}}${fr}` : coefficient directeur `{en}`: slope `${{penteS}} > 0${fr}`, donc `{en}`, so `$S${fr}` est croissante (les producteurs offrent davantage quand le prix monte) ; ordonnée à l'origine `{en}` is increasing (producers supply more as the price rises); y-intercept `${{ordS}}${fr}` (prix d'offre minimal).`{en}` (minimum supply price).`

{fr}`Pour `{en}`For `$D(q) = {{penteDCoefAff}}q {{ordDConstAff}}${fr}` : coefficient directeur `{en}`: slope `${{penteD}} < 0${fr}`, donc `{en}`, so `$D${fr}` est décroissante (les consommateurs demandent moins quand le prix monte) ; ordonnée à l'origine `{en}` is decreasing (consumers demand less as the price rises); y-intercept `${{ordD}}$.
::::

::::{weightDistribution}
:logic: 15
:abstraction: 25
:reasoning: 30
:calculation: 30
::::
:::::

:::::{question}
:questionType: FGQ
:questionId: 1
:questionIndex: 1
:solution: [["ord","${{ qStar }}$"],["0"]]

::::{questionStatement}
{fr}`Déterminer la quantité d'équilibre `{en}`Determine the equilibrium quantity `$q^{*}${fr}` en résolvant `{en}` by solving `$S(q) = D(q)$.\
\
$q^*$ = {input}`||80`
::::

::::{questionHint}
{fr}`À l'équilibre, le prix d'offre égale le prix de demande : `{en}`At equilibrium, the supply price equals the demand price: `${{penteSCoefAff}}q {{ordSConstAff}} = {{penteDCoefAff}}q {{ordDConstAff}}$.
::::

::::{displayedSolution}
$q^* = {{ qStar }}$
::::

::::{detailedSolution}
{fr}`On résout `{en}`We solve `$S(q) = D(q)$ :

\begin{equation*}
{{penteSCoefAff}}q {{ordSConstAff}} &= {{penteDCoefAff}}q {{ordDConstAff}} \\
{{penteDiffAff}}q &= {{rhsEq}} \\
q^{*} &= {{qStar}}.
\end{equation*}

{fr}`La quantité d'équilibre est `{en}`The equilibrium quantity is `$q^{*} = {{qStar}}${fr}` (soit `{en}` (i.e. `${{pots}}${fr}` pots par semaine).`{en}` jars per week).`
::::

::::{weightDistribution}
:logic: 15
:abstraction: 25
:reasoning: 30
:calculation: 30
::::
:::::

:::::{question}
:questionType: FGQ
:questionId: 2
:questionIndex: 2
:solution: [["ord","${{ pStar }}$"],["0"]]

::::{questionStatement}
{fr}`En déduire le prix d'équilibre `{en}`Deduce the equilibrium price `$p^{*} = S(q^{*})$.\
\
$p^*$ = {input}`||80`
::::

::::{questionHint}
{fr}`Remplacer `{en}`Replace `$q${fr}` par `{en}` by `$q^{*}${fr}` dans la fonction d'offre.`{en}` in the supply function.`
::::

::::{displayedSolution}
$p^* = {{ pStar }}$
::::

::::{detailedSolution}
{fr}`On utilise la fonction d'offre :`{en}`We use the supply function:`

\begin{equation*}
p^{*} = S({{qStar}}) = {{penteSAff}} \times {{qStar}} {{ordSConstAff}} = {{pStar}}.
\end{equation*}

{fr}`soit`{en}`i.e.` ${{ pStar }}$ {fr}`€/pot.`{en}`€/jar.`
::::

::::{weightDistribution}
:logic: 10
:abstraction: 20
:reasoning: 25
:calculation: 45
::::
:::::

:::::{question}
:questionType: FGQ
:questionId: 3
:questionIndex: 3
:solution: [["ord","${{ pStar }}$"],["0"]]

::::{questionStatement}
{fr}`Vérifier la réponse à l'aide de `{en}`Check the answer using `$D(q^{*})$.\
\
$D(q^*)$ = {input}`||80`
::::

::::{questionHint}
{fr}`À l'équilibre, l'offre et la demande doivent donner le même prix.`{en}`At equilibrium, supply and demand must give the same price.`
::::

::::{displayedSolution}
$D(q^*) = {{ pStar }}$
::::

::::{detailedSolution}
{fr}`On calcule la demande en `{en}`We compute demand at `$q^{*} = {{qStar}}$ :

\begin{equation*}
D({{qStar}}) = {{penteDAff}} \times {{qStar}} {{ordDConstAff}} = {{pStar}}.
\end{equation*}

{fr}`soit`{en}`i.e.` ${{ pStar }}$ {fr}`€/pot.`{en}`€/jar.`

{fr}`On a `{en}`We have `$S({{qStar}}) = D({{qStar}}) = {{pStar}}${fr}` : le point d'équilibre est bien `{en}`: the equilibrium point is indeed `$(q^{*},\, p^{*}) = ({{qStar}},\, {{pStar}})$.
::::

::::{weightDistribution}
:logic: 15
:abstraction: 20
:reasoning: 30
:calculation: 35
::::
:::::

`````