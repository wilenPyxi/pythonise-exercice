`````{exercise}
:title: {fr}`Inéquation linéaire en une étape et notation intervalle`{en}`One-step linear inequality and interval notation`
:modules: 
:recommendedExecutionTime: 5
:level: Elementary
:chap: 
:involvedConcepts: Interval_Notation, Solving_inequalities
:originalSource: 
:visibility: All
:variations: 
:comment: Échauffement : résolution d'une inéquation en une étape (règle d'addition), écriture de l'ensemble solution en notation intervalle et statut de la borne.
:originalExerciseId: cdbe79e9-633f-11f1-a8a1-0ed8d3b012a9
:id: 6fef6add-6e40-11f1-a8a1-0ed8d3b012a9

````{python}
import random as rd
from sympy import oo
from pyxiscience.Mes_fctions_generalistes_bis import pxs_config, pxsl_latex_coefficient as lc
from pyxiscience.Classes_Extensions import pxs_Interval

config_standard = pxs_config()

# Tirage des paramètres
a = rd.choice([i for i in range(-10, 11) if i != 0])
b = rd.randint(-20, 20)
signe = rd.choice(['\\leq', '\\geq', '<', '>'])

# Solution de x + a (signe) b  ->  x (signe) b - a
sol = b - a
stricte = signe in ['<', '>']

if signe == '\\leq':
    intervalAff = pxs_Interval(-oo, sol, True, False).print()
    valVraie, valFausse = sol, sol + 1
elif signe == '\\geq':
    intervalAff = pxs_Interval(sol, oo, False, True).print()
    valVraie, valFausse = sol, sol - 1
elif signe == '<':
    intervalAff = pxs_Interval(-oo, sol, True, True).print()
    valVraie, valFausse = sol - 1, sol
else:  # '>'
    intervalAff = pxs_Interval(sol, oo, True, True).print()
    valVraie, valFausse = sol + 1, sol


if pxs_lang == "fr":
    borneStatutAff = "exclue" if stricte else "incluse"
    inegaliteTypeAff = "stricte" if stricte else "large"
    crochetAff = "ouvert" if stricte else "fermé"
else:
    borneStatutAff = "excluded" if stricte else "included"
    inegaliteTypeAff = "strict" if stricte else "non-strict"
    crochetAff = "open" if stricte else "closed"

infiniAff = "-\\infty" if signe in ['\\leq', '<'] else "+\\infty"

# Rendus
aSignAff = lc(a, ones=True, sign=True)
negASignAff = lc(-a, ones=True, sign=True)
verifVraieGauche = valVraie + a
verifFausseGauche = valFausse + a
solLineAff = f"x {aSignAff} {negASignAff} {signe} {b} {negASignAff} \\implies x {signe} {sol}"

globals()


# ═══════════════ Ajouts conversion QCM (distracteurs) ═══════════════
from sympy import oo as _oo
_sol2 = b + a   # erreur arithmétique : b + a au lieu de b - a
if signe == '\\leq':
    distInt1 = pxs_Interval(-_oo, sol, True, True).print()
    distInt2 = pxs_Interval(sol, _oo, False, True).print()
    distInt3 = pxs_Interval(-_oo, _sol2, True, False).print()
elif signe == '\\geq':
    distInt1 = pxs_Interval(sol, _oo, True, True).print()
    distInt2 = pxs_Interval(-_oo, sol, True, False).print()
    distInt3 = pxs_Interval(_sol2, _oo, False, True).print()
elif signe == '<':
    distInt1 = pxs_Interval(-_oo, sol, True, False).print()
    distInt2 = pxs_Interval(sol, _oo, True, True).print()
    distInt3 = pxs_Interval(-_oo, _sol2, True, True).print()
else:
    distInt1 = pxs_Interval(sol, _oo, False, True).print()
    distInt2 = pxs_Interval(-_oo, sol, True, True).print()
    distInt3 = pxs_Interval(_sol2, _oo, True, True).print()
````

:::::{question}
:questionType: MCQ
:questionId: 0
:questionIndex: 0

::::{questionStatement}
{fr}`Résoudre l'inéquation`{en}`Solve the inequality` $x{{ aSignAff }} {{ signe }} {{ b }}$, {fr}`écrire l'ensemble solution en notation intervalle et préciser si la borne obtenue est incluse ou exclue.`{en}`write the solution set in interval notation and specify whether the obtained bound is included or excluded.`
::::

::::{questionHint}
{fr}`Soustraire`{en}`Subtract` ${{ a }}$ {fr}`des deux membres : ajouter ou soustraire un même réel conserve le sens de l'inégalité (règle d'addition).`{en}`from both sides: adding or subtracting the same real number preserves the direction of the inequality (addition rule).`
::::

::::{mcqAnswer}
:isRightAnswer: true
$S = {{ intervalAff }}$
::::

::::{mcqAnswer}
:isRightAnswer: false
$S = {{ distInt1 }}$
::::

::::{mcqAnswer}
:isRightAnswer: false
$S = {{ distInt2 }}$
::::

::::{mcqAnswer}
:isRightAnswer: false
$S = {{ distInt3 }}$
::::

::::{mcqAnswer}
:isRightAnswer: false
{fr}`Aucune de ces réponses n'est correcte`{en}`None of these answers are correct`
::::

::::{detailedSolution}
{fr}`Additionner ou soustraire ne change pas le sens de l'inégalité.`{en}`Adding or subtracting does not change the direction of the inequality.`

\begin{equation*}
{{ solLineAff }}.
\end{equation*}

{fr}`L'ensemble des solutions est`{en}`The solution set is`

\begin{equation*}
S = {{ intervalAff }}.
\end{equation*}

{fr}`La borne`{en}`The bound` ${{ sol }}$ {fr}`est`{en}`is` {{ borneStatutAff }} ({fr}`inégalité`{en}`inequality` {{ inegaliteTypeAff }} ${{ signe }}$), {fr}`d'où le crochet`{en}`hence the bracket is` {{ crochetAff }}. {fr}`Le symbole`{en}`The symbol` ${{ infiniAff }}$ {fr}`n'est pas un réel donc la parenthèse ouverte est obligatoire.`{en}`is not a real number so the open parenthesis is mandatory.`
::::

::::{weightDistribution}
:logic: 15
:abstraction: 20
:reasoning: 30
:calculation: 35
::::
:::::

`````
