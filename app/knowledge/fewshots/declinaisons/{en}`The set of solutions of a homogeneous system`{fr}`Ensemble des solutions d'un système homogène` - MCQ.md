`````{exercise}
:id: e2c3b203-6fb1-11f1-a8a1-0ed8d3b012a9
:originalExerciseId: e5717816-752a-4abf-9afc-55df5774e4e0
:title: {en}`The set of solutions of a homogeneous system`{fr}`Ensemble des solutions d'un système homogène` - MCQ
:modules: 
:recommendedExecutionTime: 30
:level: Elementary
:chap: section_2_4_linalg_Trush
:involvedConcepts: 
:originalSource: 7.1 Ronan
:visibility: All
:variations: 
:comment: 

````{python}
# Code Python : Ecrivez ci-dessous votre code Python
from __future__ import division
from pyxiscience.Mes_fctions_d_alg_lineaire_bis import *
from sympy import *
import random as rd 




systems = []

 
n = rd.randint(2,3)
p = rd.randint(n+1,n+2)

nb_pivots = rd.randint(2, min(n, p))
pivots = tuple(rd.sample([i for i in range(1, min(n, p) + 1)], nb_pivots))
A, B = pxs_repeat_generate_sys(n = n, p = p, M = tuple(pivots), N = Matrix([rd.randint(1, 5) for _ in range(n-1)] + [0]), backup = zeros(3, 3))
if A == zeros(3, 3):
    A = Matrix([[1, -5, -1, 0], [-2, 10, 1, -4], [0, 0, -1, -4]])
    B = Matrix([[0, -3, -3]]).T
    
A, B = pxs_break_all_colinear_rows(A, B, max_iter=5)
systems.append((A, B))

B=0*B
Blat=pxsl_matrix(B)
Alat=pxsl_matrix(A)

augmentmat=pxsl_double_matrix(A,B,opt='ext')

sys = pxsl_system_lin(A, B)

soluce=pxs_gauss_jordan(A.copy(), B.copy(), method = "mat", view = "ext")
 
Ared=pxsl_double_matrix(soluce["A"],soluce["B"],opt='ext')


````

:::::{question}
:questionType: MCQ
:questionId: 1
:questionIndex: 1

::::{questionStatement}
{en}`Which of the following best describes the solution set of the equation`{fr}`Laquelle des propositions suivantes décrit le mieux l'ensemble des solutions de l'équation` $Ax=0$ {en}`where`{fr}`où`
\begin{equation*}
A={{Alat}}?
\end{equation*}
::::

::::{questionHint}

::::

::::{mcqAnswer}
:isRightAnswer: true
{en}`An infinite set of vectors forming a subspace through the origin (the system has infinitely many solutions)`{fr}`Un ensemble infini de vecteurs formant un sous-espace vectoriel passant par l'origine (le système a une infinité de solutions)`
::::

::::{mcqAnswer}
:isRightAnswer: false
{en}`Only the trivial solution $x=0$`{fr}`Uniquement la solution triviale $x=0$`
::::

::::{mcqAnswer}
:isRightAnswer: false
{en}`The empty set (the system has no solution)`{fr}`L'ensemble vide (le système n'a aucune solution)`
::::

::::{mcqAnswer}
:isRightAnswer: false
{en}`A single nonzero vector`{fr}`Un unique vecteur non nul`
::::

::::{mcqAnswer}
:isRightAnswer: false
{fr}`Aucune de ces réponses n'est correcte` {en}`None of these answers are correct`
::::

::::{detailedSolution}
{en}`The equation `{fr}`L'équation ` $Ax=0$ {en}`may be written with an augmented matrix as `{fr}`peut s'écrire sous la forme de matrice augmentée comme `
\begin{equation*}
{{augmentmat}}
\end{equation*}
{en}`The Row Reduction Echelon Form of this matrix is`{fr}`La forme échelonnée réduite de cette matrice est `
\begin{equation*}
{{Ared}}
\end{equation*}

:::{dropdown} {en}`See more details`{fr}`Voir plus de détails`
{en}`We may apply the Row Reduction Algorithm to reduce the augmented matrix: `{fr}`Nous pouvons appliquer l'algorithme de Gauss pour réduire la matrice augmentée :`
{{soluce["resol"]}}
:::

{en}`which is equivalent to the system `{fr}`ce qui est équivalent au système`
\begin{equation*}
{{soluce["sys"]}}.
\end{equation*}

{en}`The set of solutions of the equation `{fr}`L'ensemble des solution de l'équation ` $Ax=0$ {en}` is then `{fr}` est donc `
\begin{equation*}
\boxed{
{{soluce["span"]}}.

}
\end{equation*}
::::

::::{weightDistribution}
:reasoning: 25
:logic: 25
:abstraction: 25
:calculation: 25
::::
:::::
`````