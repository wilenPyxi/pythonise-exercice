`````{exercise}
:title: {fr}`Seuil de rentabilité d'une boutique`{en}`Break-Even Point of a Store`
:modules: 
:recommendedExecutionTime: 15
:level: Elementary
:chap: chap_lines_Systems_economicEquilibriumBreakeven_ESCP
:involvedConcepts: 
:originalSource: Session 4 — Erwan Lamy, ESCP Business School
:visibility: All
:variations: 
:comment: Appliqué (gestion) : revenu total, coût total, profit, seuil de rentabilité, marge sur coût variable.
:id: 33724a3b-74c0-11f1-a8a1-0ed8d3b012a9
:originalExerciseId: 10e7b53f-64e3-11f1-a8a1-0ed8d3b012a9

````{python}
import random as rd
from pyxiscience.Mes_fctions_generalistes_bis import pxs_config, pxsl_latex_coefficient as lc, pxsl_format_number
# --- Helpers PyxiScience (definis inline, autonomes : aucun import externe) ---

config_standard = pxs_config()

# p > c (marge positive) ; y_FC multiple de 50 divisible par la marge (seuil entier)
for _ in range(300):
    p = rd.randint(20, 50)
    c = rd.randint(5, 15)
    if p <= c:
        continue
    marge = p - c
    yFc = rd.randint(6, 16) * 50
    if yFc % marge == 0:
        break

qStar = yFc // marge
qTest = qStar + rd.randint(5, 20)
profitQtest = marge * qTest - yFc

# Affichage
yFcAff = pxsl_format_number(yFc)
profitQtestAff = pxsl_format_number(profitQtest)

globals()
````

{fr}`Une boutique vend des écharpes faites main au prix unitaire `{en}`A shop sells handmade scarves at the unit price `$p = {{p}}${fr}` €. Le coût variable unitaire est `{en}` €. The unit variable cost is `$c = {{c}}${fr}` € et le coût fixe mensuel `{en}` € and the monthly fixed cost `$y_{FC} = {{yFcAff}}$ €.

:::::{question}
:questionType: FGQ
:questionId: 0
:questionIndex: 0
:solution: [["ord","${{ p }}$","${{ c }}$","${{ yFcAff }}$"],["0","0","0"]]

::::{questionStatement}
{fr}`Écrire le revenu total `{en}`Write the total revenue `$y_{TR}(q)${fr}` et le coût total `{en}` and the total cost `$y_{TC}(q)$.
- $y_{TR}(q) =$ {input}`||80` $q$ 
- $y_{TC}(q) =$ {input}`||80` $q +$ {input}`||80`
::::

::::{questionHint}
$y_{TR} = p\,q${fr}` et `{en}` and `$y_{TC} = c\,q + y_{FC}$.
::::

::::{displayedSolution}
$y_{TR}(q) = {{ p }}q$ — $y_{TC}(q) = {{ c }}q + {{ yFcAff }}$
::::

::::{detailedSolution}
{fr}`On applique les définitions :`{en}`We apply the definitions:`

\begin{equation*}
y_{TR}(q) = {{p}}\,q, \qquad y_{TC}(q) = {{c}}\,q + {{yFcAff}}.
\end{equation*}
::::

::::{weightDistribution}
:logic: 10
:abstraction: 25
:reasoning: 30
:calculation: 35
::::
:::::

:::::{question}
:questionType: FGQ
:questionId: 1
:questionIndex: 1
:solution: [["ord","${{ marge }}$","${{ yFcAff }}$"],["0","0"]]

::::{questionStatement}
{fr}`Calculer le profit `{en}`Compute the profit `$\Pi(q) = y_{TR}(q) - y_{TC}(q)${fr}` et simplifier.`{en}` and simplify.`\
\
$\Pi(q) =$ {input}`||80` $q -$ {input}`||80`
::::

::::{questionHint}
{fr}`Soustraire le coût total du revenu total, puis regrouper les termes en `{en}`Subtract the total cost from the total revenue, then group the terms in `$q$.
::::

::::{displayedSolution}
$\Pi(q) = {{ marge }}q - {{ yFcAff }}$
::::

::::{detailedSolution}
{fr}`On développe :`{en}`We expand:`

\begin{equation*}
\Pi(q) = {{p}}\,q - ({{c}}\,q + {{yFcAff}}) = {{marge}}\,q - {{yFcAff}}.
\end{equation*}

{fr}`Le profit est affine, de coefficient directeur `{en}`The profit is affine, with slope `${{marge}}${fr}` : c'est la marge sur coût variable `{en}`: it is the contribution margin `$p - c = {{p}} - {{c}} = {{marge}}${fr}` € par écharpe.`{en}` € per scarf.`
::::

::::{weightDistribution}
:logic: 15
:abstraction: 25
:reasoning: 25
:calculation: 35
::::
:::::

:::::{question}
:questionType: FGQ
:questionId: 2
:questionIndex: 2
:solution: [["ord","${{ qStar }}$"],["0"]]

::::{questionStatement}
{fr}`Déterminer la quantité de seuil de rentabilité `{en}`Determine the break-even quantity `$q^{*}${fr}` en résolvant `{en}` by solving `$y_{TR}(q) = y_{TC}(q)$.\
\
$q^*$ = {input}`||80`
::::

::::{questionHint}
{fr}`Au seuil de rentabilité, le profit est nul : `{en}`At the break-even point, the profit is zero: `$\Pi(q) = 0$.
::::

::::{displayedSolution}
$q^* = {{ qStar }}$
::::

::::{detailedSolution}
{fr}`On résout `{en}`We solve `$\Pi(q) = 0$ :

\begin{equation*}
{{marge}}\,q - {{yFcAff}} = 0 \implies {{marge}}\,q = {{yFcAff}} \implies q^{*} = {{qStar}}.
\end{equation*}

{fr}`La boutique doit vendre au moins `{en}`The shop must sell at least `${{qStar}}${fr}` écharpes par mois pour couvrir ses coûts.`{en}` scarves per month to cover its costs.`
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
:questionId: 3
:questionIndex: 3
:solution: [["ord","${{ profitQtestAff }}$"],["0"]]

::::{questionStatement}
{fr}`Calculer le profit pour `{en}`Compute the profit for `$q = {{qTest}}${fr}` écharpes vendues. La boutique est-elle rentable à ce niveau ?`{en}` scarves sold. Is the shop profitable at this level?`\
\
$\Pi({{ qTest }})$ = {input}`||80`
::::

::::{questionHint}
{fr}`Évaluer `{en}`Evaluate `$\Pi({{qTest}})${fr}` et comparer `{en}` and compare `${{qTest}}${fr}` au seuil `{en}` with the break-even `$q^{*}$.
::::

::::{displayedSolution}
$\Pi({{ qTest }}) = {{ profitQtestAff }}$
::::

::::{detailedSolution}
{fr}`On évalue le profit en `{en}`We evaluate the profit at `$q = {{qTest}}$ :

\begin{equation*}
\Pi({{qTest}}) = {{marge}} \times {{qTest}} - {{yFcAff}} = {{profitQtestAff}}.
\end{equation*}

{fr}`soit`{en}`i.e.` ${{ profitQtestAff }}$ {fr}`€.`{en}`€.`

{fr}`Comme `{en}`Since `${{qTest}} > q^{*} = {{qStar}}${fr}`, la boutique est rentable et dégage un profit mensuel de `{en}`, the shop is profitable and earns a monthly profit of `${{profitQtestAff}}$ €.
::::

::::{weightDistribution}
:logic: 15
:abstraction: 20
:reasoning: 30
:calculation: 35
::::
:::::

`````