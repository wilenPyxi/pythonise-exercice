`````{exercise}
:title: {fr}`Symétries d'une courbe de demande et restriction économique`{en}`Symmetries of a demand curve and economic restriction`
:modules: 
:recommendedExecutionTime: 18
:level: Elementary
:chap: chap_realFunctions_Graphs_graphSymmetries_ESCP
:involvedConcepts: 
:originalSource: 
:visibility: All
:variations: 
:comment: Appliqué (économie & gestion) : quatre tests de symétrie sur une courbe de demande implicite (cercle), puis restriction au premier quadrant et identification de la seule symétrie pertinente (y=x), en reconnaissance uniquement.
:id: 64470bcd-74b4-11f1-a8a1-0ed8d3b012a9
:originalExerciseId: e6ac5c47-6409-11f1-a8a1-0ed8d3b012a9

````{python}
import random as rd
from pyxiscience.Mes_fctions_generalistes_bis import pxs_config

config_standard = pxs_config()

rayon = rd.randint(3, 10)
rayon_carre = rayon**2

if pxs_lang == "fr":
    unite_demande = rd.choice(["centaines d'unités", "milliers d'unités", "dizaines d'unités"])
    unite_prix = rd.choice(["dizaines d'euros", "centaines d'euros", "euros"])
    type_produit = rd.choice(["produit de luxe", "produit technologique", "bien de consommation", "service premium"])
else:
    unite_demande = rd.choice(["hundreds of units", "thousands of units", "tens of units"])
    unite_prix = rd.choice(["tens of dollars", "hundreds of dollars", "dollars"])
    type_produit = rd.choice(["luxury product", "technological product", "consumer good", "premium service"])

# Rendus
rayonCarre = rayon_carre
uniteDemande = unite_demande
unitePrix = unite_prix
typeProduit = type_produit

globals()
````

:::::{question}
:questionType: MCQ
:questionId: 0
:questionIndex: 0

::::{questionStatement}
{fr}`Un directeur commercial étudie la courbe de demande d'un`{en}`A sales director studies the demand curve of a` {{ typeProduit }} {fr}`: la demande`{en}`: the demand` $D>0$ {fr}`(en`{en}`(in` {{ uniteDemande }}) {fr}`et le prix`{en}`and the price` $p>0$ {fr}`(en`{en}`(in` {{ unitePrix }}) {fr}`vérifient`{en}`satisfy` $p^2+D^2={{ rayonCarre }}$. {fr}`Appliquer les quatre tests algébriques de symétrie (par rapport à l'axe`{en}`Apply the four algebraic symmetry tests (with respect to the axis` $Op$, {fr}`à l'axe`{en}`to the axis` $OD$, {fr}`à l'origine, à la droite`{en}`to the origin, to the line` $D=p$) {fr}`à la courbe complète et conclure pour chacun.`{en}`to the complete curve and conclude for each.`
::::

::::{questionHint}
{fr}`Substituer dans l'équation : les carrés rendent`{en}`Substitute in the equation: the squares make` $p^2$ {fr}`et`{en}`and` $D^2$ {fr}`inchangés par changement de signe ; échanger`{en}`unchanged by sign change; exchanging` $p$ {fr}`et`{en}`and` $D$ {fr}`ne change pas une somme.`{en}`does not change a sum.`
::::

::::{mcqAnswer}
:isRightAnswer: true
{fr}`Les quatre :`{en}`All four:` $Op$, $OD$, {fr}`l'origine et la droite`{en}`the origin, and the line` $D=p$
::::

::::{mcqAnswer}
:isRightAnswer: false
{fr}`Seulement les axes`{en}`Only the axes` $Op$ {fr}`et`{en}`and` $OD$
::::

::::{mcqAnswer}
:isRightAnswer: false
{fr}`Seulement la droite`{en}`Only the line` $D=p$
::::

::::{mcqAnswer}
:isRightAnswer: false
{fr}`Seulement l'origine`{en}`Only the origin`
::::

::::{mcqAnswer}
:isRightAnswer: false
{fr}`Aucune de ces réponses n'est correcte`{en}`None of these answers are correct`
::::

::::{detailedSolution}
{fr}`La courbe complète`{en}`The complete curve` $p^2+D^2={{ rayonCarre }}$ {fr}`est un cercle de centre`{en}`is a circle with center` $O$ {fr}`et de rayon`{en}`and radius` ${{ rayon }}$.

\begin{equation*}
p^2 + D^2 = {{ rayonCarre }}.
\end{equation*}

{fr}`**Test axe**`{en}`**Axis test**` $Op$ ($D \to -D$) : {fr}`on remplace`{en}`we replace` $D$ {fr}`par`{en}`by` $-D$ {fr}`dans l'équation :`{en}`in the equation:`

\begin{equation*}
p^2 + (-D)^2 = p^2 + D^2 = {{ rayonCarre }}.
\end{equation*}

{fr}`L'équation est inchangée : la courbe est symétrique par rapport à l'axe`{en}`The equation is unchanged: the curve is symmetric with respect to the axis` $Op$.

{fr}`**Test axe**`{en}`**Axis test**` $OD$ ($p \to -p$) : {fr}`on remplace`{en}`we replace` $p$ {fr}`par`{en}`by` $-p$ {fr}`dans l'équation :`{en}`in the equation:`

\begin{equation*}
(-p)^2 + D^2 = p^2 + D^2 = {{ rayonCarre }}.
\end{equation*}

{fr}`L'équation est inchangée : la courbe est symétrique par rapport à l'axe`{en}`The equation is unchanged: the curve is symmetric with respect to the axis` $OD$.

{fr}`**Test origine** (`{en}`**Origin test** (` $p \to -p$, $D \to -D$) : {fr}`on remplace`{en}`we replace` $p$ {fr}`par`{en}`by` $-p$ {fr}`et`{en}`and` $D$ {fr}`par`{en}`by` $-D$ :

\begin{equation*}
(-p)^2 + (-D)^2 = p^2 + D^2 = {{ rayonCarre }}.
\end{equation*}

{fr}`L'équation est inchangée : la courbe est symétrique par rapport à l'origine.`{en}`The equation is unchanged: the curve is symmetric with respect to the origin.`

{fr}`**Test droite**`{en}`**Line test**` $D=p$ {fr}`(échanger`{en}`(exchange` $p$ {fr}`et`{en}`and` $D$) : {fr}`on échange`{en}`we exchange` $p$ {fr}`et`{en}`and` $D$ {fr}`dans l'équation :`{en}`in the equation:`

\begin{equation*}
D^2 + p^2 = {{ rayonCarre }}.
\end{equation*}

{fr}`Cette équation est identique à l'équation initiale : la courbe est symétrique par rapport à la droite`{en}`This equation is identical to the initial equation: the curve is symmetric with respect to the line` $D=p$.

{fr}`**Conclusion** : la courbe complète possède les quatre symétries.`{en}`**Conclusion**: the complete curve has all four symmetries.`
::::

::::{weightDistribution}
:logic: 25
:abstraction: 35
:reasoning: 30
:calculation: 10
::::
:::::

:::::{question}
:questionType: MCQ
:questionId: 1
:questionIndex: 1

::::{questionStatement}
{fr}`Justifier pourquoi, dans le contexte économique (`{en}`Justify why, in the economic context (` $p>0$ {fr}`et`{en}`and` $D>0$), {fr}`la courbe de demande n'est définie que sur un quart de cercle. En déduire la seule symétrie pertinente pour ce modèle, et l'interpréter.`{en}`the demand curve is only defined on a quarter circle. Deduce the only relevant symmetry for this model, and interpret it.`
::::

::::{questionHint}
{fr}`Une symétrie n'est pertinente que si elle renvoie un point du premier quadrant dans le premier quadrant.`{en}`A symmetry is relevant only if it maps a point from the first quadrant to the first quadrant.`
::::

::::{mcqAnswer}
:isRightAnswer: true
{fr}`La droite`{en}`The line` $D=p$
::::

::::{mcqAnswer}
:isRightAnswer: false
{fr}`L'axe`{en}`The axis` $Op$
::::

::::{mcqAnswer}
:isRightAnswer: false
{fr}`L'axe`{en}`The axis` $OD$
::::

::::{mcqAnswer}
:isRightAnswer: false
{fr}`L'origine`{en}`The origin`
::::

::::{mcqAnswer}
:isRightAnswer: false
{fr}`Aucune de ces réponses n'est correcte`{en}`None of these answers are correct`
::::

::::{detailedSolution}
{fr}`**Restriction au premier quadrant** : dans le contexte économique, le prix`{en}`**Restriction to the first quadrant**: in the economic context, the price` $p$ {fr}`et la demande`{en}`and the demand` $D$ {fr}`sont des grandeurs strictement positives. On a donc`{en}`are strictly positive quantities. We therefore have` $p>0$ {fr}`et`{en}`and` $D>0$, {fr}`ce qui signifie que seuls les points du premier quadrant sont économiquement pertinents. La courbe de demande se réduit donc à un quart de cercle de rayon`{en}`which means that only points in the first quadrant are economically relevant. The demand curve is therefore reduced to a quarter circle of radius` ${{ rayon }}$ {fr}`situé dans le premier quadrant.`{en}`located in the first quadrant.`

{fr}`**Analyse des symétries** :`{en}`**Analysis of symmetries**:`

- {fr}`**Symétrie par rapport à l'axe**`{en}`**Symmetry with respect to the axis**` $Op$ ($D \to -D$) : {fr}`cette transformation envoie un point`{en}`this transformation maps a point` $(p_0, D_0)$ {fr}`avec`{en}`with` $p_0>0$ {fr}`et`{en}`and` $D_0>0$ {fr}`sur le point`{en}`to the point` $(p_0, -D_0)$ {fr}`avec`{en}`with` $-D_0<0$. {fr}`Ce point sort du premier quadrant : cette symétrie n'est pas pertinente dans le contexte économique.`{en}`This point leaves the first quadrant: this symmetry is not relevant in the economic context.`

- {fr}`**Symétrie par rapport à l'axe**`{en}`**Symmetry with respect to the axis**` $OD$ ($p \to -p$) : {fr}`cette transformation envoie un point`{en}`this transformation maps a point` $(p_0, D_0)$ {fr}`avec`{en}`with` $p_0>0$ {fr}`et`{en}`and` $D_0>0$ {fr}`sur le point`{en}`to the point` $(-p_0, D_0)$ {fr}`avec`{en}`with` $-p_0<0$. {fr}`Ce point sort du premier quadrant : cette symétrie n'est pas pertinente dans le contexte économique.`{en}`This point leaves the first quadrant: this symmetry is not relevant in the economic context.`

- {fr}`**Symétrie par rapport à l'origine** (`{en}`**Symmetry with respect to the origin** (` $p \to -p$, $D \to -D$) : {fr}`cette transformation envoie un point`{en}`this transformation maps a point` $(p_0, D_0)$ {fr}`avec`{en}`with` $p_0>0$ {fr}`et`{en}`and` $D_0>0$ {fr}`sur le point`{en}`to the point` $(-p_0, -D_0)$ {fr}`avec`{en}`with` $-p_0<0$ {fr}`et`{en}`and` $-D_0<0$. {fr}`Ce point sort du premier quadrant : cette symétrie n'est pas pertinente dans le contexte économique.`{en}`This point leaves the first quadrant: this symmetry is not relevant in the economic context.`

- {fr}`**Symétrie par rapport à la droite**`{en}`**Symmetry with respect to the line**` $D=p$ {fr}`(échanger`{en}`(exchange` $p$ {fr}`et`{en}`and` $D$) : {fr}`cette transformation envoie un point`{en}`this transformation maps a point` $(p_0, D_0)$ {fr}`avec`{en}`with` $p_0>0$ {fr}`et`{en}`and` $D_0>0$ {fr}`sur le point`{en}`to the point` $(D_0, p_0)$ {fr}`avec`{en}`with` $D_0>0$ {fr}`et`{en}`and` $p_0>0$. {fr}`Ce point reste dans le premier quadrant : c'est la seule symétrie pertinente dans le contexte économique.`{en}`This point remains in the first quadrant: this is the only relevant symmetry in the economic context.`

{fr}`**Interprétation** : la symétrie par rapport à la droite`{en}`**Interpretation**: the symmetry with respect to the line` $D=p$ {fr}`signifie que si à un prix`{en}`means that if at a price` $p_0$ {fr}`correspond une demande`{en}`corresponds a demand` $D_0$ {fr}`(le point`{en}`(the point` $(p_0, D_0)$ {fr}`est sur la courbe), alors le point`{en}`is on the curve), then the point` $(D_0, p_0)$ {fr}`est également sur la courbe. Autrement dit, si la demande vaut`{en}`is also on the curve. In other words, if the demand equals` $D_0$ {fr}`unités au prix`{en}`units at price` $p_0$, {fr}`alors elle vaudra`{en}`then it will equal` $p_0$ {fr}`unités au prix`{en}`units at price` $D_0$. {fr}`Le modèle est donc réversible vis-à-vis de l'échange entre prix et demande : la relation entre`{en}`The model is therefore reversible with respect to the exchange between price and demand: the relationship between` $p$ {fr}`et`{en}`and` $D$ {fr}`est symétrique.`{en}`is symmetric.`
::::

::::{weightDistribution}
:logic: 30
:abstraction: 35
:reasoning: 30
:calculation: 5
::::
:::::

`````