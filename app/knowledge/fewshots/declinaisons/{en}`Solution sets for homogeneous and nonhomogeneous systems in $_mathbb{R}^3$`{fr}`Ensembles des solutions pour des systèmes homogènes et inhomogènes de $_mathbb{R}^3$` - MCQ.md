`````{exercise}
:id: 27512f8b-6fb2-11f1-a8a1-0ed8d3b012a9
:originalExerciseId: 9cad7853-dc83-4e8f-b06c-dcfc516b66fb
:title: {en}`Solution sets for homogeneous and nonhomogeneous systems in $\mathbb{R}^3$`{fr}`Ensembles des solutions pour des systèmes homogènes et inhomogènes de $\mathbb{R}^3$` - MCQ
:modules: Linear_Algebra_Pyx, Linear_Algebra_Trush
:recommendedExecutionTime: 30
:level: Elementary
:chap: section_2_4_linalg_Trush
:involvedConcepts: 
:originalSource: 7.4 Ronan
:visibility: All
:variations: 
:comment: 

```{python}

# Code Python : Ecrivez ci-dessous votre code Python
from __future__ import division
from pyxiscience.Mes_fctions_d_alg_lineaire_bis import *
from sympy import *
import random as rd 




#### Question 1

 
n = 3
p = 3

lam=rd.randint(-9,9)
nu=rd.randint(-9,9)
bnn=rd.randint(-9,9)
while lam==0 or nu==0 or bnn==0:
    lam=rd.randint(-9,9)
    nu=rd.randint(-9,9)
    bnn=rd.randint(-9,9)

A= randmatrixrect(n,p,-9,9)
B= randmatrixrect(n,1,-9,9)

A[0,0]=1
A[0,1]=lam
A[0,2]=nu

for i in range(1,n):
    for j in range(0,p):
        A[i,j]=0
        B[i]=0
 
B[0]=0
x='x'
vect_x=Matrix([Symbol(x+'_1')])
for i in range(p-1):
    vect_x=vect_x.row_join(Matrix([Symbol(x+'_'+str(i+2))]))
expr=myst(r""" """,globals(),locals())

if A[0, :].is_zero_matrix:
    expr += "0"
# Gère l'affichage du premier terme non nul sans le '+' devant
if A[0, 0] != 0:
    expr+=pxsl_ax(A[0,0],vect_x[0], frac = frac)
    sign="+"
else:
    sign=""
for j in range(1,p):
    if A[0,j]!=0:
        expr+=pxsl_ax(A[0,j],vect_x[j],sign, frac = frac)
        sign="+"

rhs = myst(r"""{{ B[0].p }}/{{ B[0].q }}""", globals(), locals()) if (isinstance(B[i], Rational) and B[0].q != 1 and not frac) else latex(B[0])

expr+=myst(r""" ={{ rhs }}""",globals(),locals())

sys=expr

 
Alat=pxsl_matrix(A)
Blat=pxsl_matrix(B)
augmentmat1=pxsl_double_matrix(A,B,opt='ext')

 
 
 
soluce1=pxs_gauss_jordan(A.copy(), B.copy(), method = "mat", view = "ext")
 
Ared1=pxsl_double_matrix(soluce1["A"],soluce1["B"],opt='ext')
 


#### Question 2

B[0]=bnn

x='x'
vect_x=Matrix([Symbol(x+'_1')])
for i in range(p-1):
    vect_x=vect_x.row_join(Matrix([Symbol(x+'_'+str(i+2))]))
expr=myst(r""" """,globals(),locals())

if A[0, :].is_zero_matrix:
    expr += "0"
# Gère l'affichage du premier terme non nul sans le '+' devant
if A[0, 0] != 0:
    expr+=pxsl_ax(A[0,0],vect_x[0], frac = frac)
    sign="+"
else:
    sign=""
for j in range(1,p):
    if A[0,j]!=0:
        expr+=pxsl_ax(A[0,j],vect_x[j],sign, frac = frac)
        sign="+"

rhs = myst(r"""{{ B[0].p }}/{{ B[0].q }}""", globals(), locals()) if (isinstance(B[i], Rational) and B[0].q != 1 and not frac) else latex(B[0])

expr+=myst(r""" ={{ rhs }}""",globals(),locals())

sys2=expr

 
Alat=pxsl_matrix(A)
Blat=pxsl_matrix(B)
augmentmat2=pxsl_double_matrix(A,B,opt='ext')

 
 
 
soluce2=pxs_gauss_jordan(A.copy(), B.copy(), method = "mat", view = "ext")
 
Ared2=pxsl_double_matrix(soluce2["A"],soluce2["B"],opt='ext')
 


```


 


:::::{question}
:questionType: MCQ
:questionId: 1
:questionIndex: 1

::::{questionStatement}
{en}`Which of the following best describes the solution set of the equation`{fr}`Laquelle des propositions suivantes décrit le mieux l'ensemble des solutions de l'équation`

\begin{equation}\label{hom}
{{ sys }}.
\end{equation}
::::

::::{questionHint}

::::

::::{mcqAnswer}
:isRightAnswer: true
{en}`A plane through the origin`{fr}`Un plan passant par l'origine`
::::

::::{mcqAnswer}
:isRightAnswer: false
{en}`A line through the origin`{fr}`Une droite passant par l'origine`
::::

::::{mcqAnswer}
:isRightAnswer: false
{en}`The whole space $\mathbb{R}^3$`{fr}`L'espace $\mathbb{R}^3$ tout entier`
::::

::::{mcqAnswer}
:isRightAnswer: false
{en}`Only the origin $\{0\}$`{fr}`Uniquement l'origine $\{0\}$`
::::

::::{mcqAnswer}
:isRightAnswer: false
{fr}`Aucune de ces réponses n'est correcte` {en}`None of these answers are correct`
::::

::::{detailedSolution}

{en}`The equation`{fr}`L'équation` ${{ sys }}$ {en}`may be written with an augmented matrix as`{fr}`peut s'écrire sous la forme de matrice augmentée comme`
\begin{equation*}
{{ Ared1 }},
\end{equation*}
 

{en}`which is equivalent to the system`{fr}`ce qui est équivalent au système`
\begin{equation*}
{{ soluce1["sys"] }}.
\end{equation*}

{en}`The set of solutions of the equation`{fr}`L'ensemble des solution de l'équation` ${{ sys }}$ {en}`is then`{fr}`est donc`
\begin{equation*}
\boxed{ 
{{ soluce1["span"] }}.
}
\end{equation*}
{en}`Geometrically, the solution set forms a plane in`{fr}`Géométriquement, l'ensemble des solutions forme un plan de` $\mathbb{R}^3.$
::::

::::{weightDistribution}
:
::::
:::::



:::::{question}
:questionType: MCQ
:questionId: 2
:questionIndex: 2

::::{questionStatement}
{en}`Which of the following best describes the solution set of the equation`{fr}`Laquelle des propositions suivantes décrit le mieux l'ensemble des solutions de l'équation`
\begin{equation}\label{inhom}
{{ sys2 }}.
\end{equation}
::::

::::{questionHint}

::::

::::{mcqAnswer}
:isRightAnswer: true
{en}`A plane that does not pass through the origin`{fr}`Un plan ne passant pas par l'origine`
::::

::::{mcqAnswer}
:isRightAnswer: false
{en}`A plane through the origin`{fr}`Un plan passant par l'origine`
::::

::::{mcqAnswer}
:isRightAnswer: false
{en}`A single point`{fr}`Un unique point`
::::

::::{mcqAnswer}
:isRightAnswer: false
{en}`The empty set (the equation has no solution)`{fr}`L'ensemble vide (l'équation n'a aucune solution)`
::::

::::{mcqAnswer}
:isRightAnswer: false
{fr}`Aucune de ces réponses n'est correcte` {en}`None of these answers are correct`
::::

::::{detailedSolution}

{en}`The equation`{fr}`L'équation` ${{ sys2 }}$ {en}`may be written with an augmented matrix as`{fr}`peut s'écrire sous la forme de matrice augmentée comme`
\begin{equation*}
{{ Ared2 }},
\end{equation*}
 

{en}`which is equivalent to the system`{fr}`ce qui est équivalent au système`
\begin{equation*}
{{ soluce2["sys"] }}.
\end{equation*}

{en}`The set of solutions of the equation`{fr}`L'ensemble des solution de l'équation` ${{ sys2 }}$ {en}`is then`{fr}`est donc`
\begin{equation*}
\boxed{ 
{{ soluce2["span"] }}.
}
\end{equation*}
{en}`Geometrically, the solution set forms a plane in`{fr}`Géométriquement, l'ensemble des solutions forme un plan de` $\mathbb{R}^3.$
::::

::::{weightDistribution}
:
::::
:::::



:::::{question}
:questionType: MCQ
:questionId: 3
:questionIndex: 3

::::{questionStatement}
{en}`How do the two solution sets compare geometrically?`{fr}`Comment peut-on comparer géométriquement les deux ensembles de solutions ?`
::::

::::{questionHint}

::::

::::{mcqAnswer}
:isRightAnswer: true
{en}`They are parallel planes: the nonhomogeneous one is a translate of the homogeneous one`{fr}`Ce sont des plans parallèles : celui du système inhomogène est un translaté de celui du système homogène`
::::

::::{mcqAnswer}
:isRightAnswer: false
{en}`They are the same plane`{fr}`Ce sont le même plan`
::::

::::{mcqAnswer}
:isRightAnswer: false
{en}`They are two perpendicular planes`{fr}`Ce sont deux plans perpendiculaires`
::::

::::{mcqAnswer}
:isRightAnswer: false
{en}`They intersect along a line`{fr}`Ils se coupent selon une droite`
::::

::::{mcqAnswer}
:isRightAnswer: false
{fr}`Aucune de ces réponses n'est correcte` {en}`None of these answers are correct`
::::

::::{detailedSolution}

{en}`Geometrically, the solution set of the nonhomogeneous equation` [](#inhom) {en}`is a translation by the vector` ${{ Blat }}$ {en}`of the solution set of the homogeneous equation` [](#hom).


```{python}

# Code Python : Ecrivez ci-dessous votre code Python


import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Création de la figure et de l'axe 3D
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Définition des limites pour x et y
x = np.linspace(-4, 4, 10)
y = np.linspace(-4, 4, 10)
X, Y = np.meshgrid(x, y)

# Équation du premier plan : z = a*x + b*y + c
a, b, c = -1/nu, -lam/nu, 0
Z1 = a*X + b*Y + c

# Équation du deuxième plan parallèle : z = a*x + b*y + d (d ≠ c)
d = -bnn/nu
Z2 = a*X + b*Y + d

# Tracé des deux plans
ax.plot_surface(X, Y, Z1, alpha=0.5, color='blue', label='Plane (1)')
ax.plot_surface(X, Y, Z2, alpha=0.5, color='red', label='Plane (2)')

# Ajout des labels et titre
ax.set_xlabel('$x_1$')
ax.set_ylabel('$x_2$')
ax.set_zlabel('$x_3$')
ax.set_title('The two planes')

# Affichage de la légende
ax.legend()

plt.show()

```
::::

::::{weightDistribution}
:
::::
:::::
`````