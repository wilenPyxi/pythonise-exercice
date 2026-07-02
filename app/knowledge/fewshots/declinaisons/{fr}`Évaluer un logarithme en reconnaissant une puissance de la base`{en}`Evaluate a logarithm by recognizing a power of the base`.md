`````{exercise}
:title: {fr}`Évaluer un logarithme en reconnaissant une puissance de la base`{en}`Evaluate a logarithm by recognizing a power of the base`
:modules: 
:recommendedExecutionTime: 10
:level: Elementary
:chap: chap_expLogFunctions_logarithmicFunctions_ESCP
:involvedConcepts: 
:originalSource: 
:visibility: All
:variations: 
:comment: Échauffement (thème pur) : évaluation de log_b(x) en reconnaissant x comme une puissance de b, via log_b(b^k)=k. Aucune loi algébrique du logarithme.
:originalExerciseId: 1331c2a5-6599-11f1-a8a1-0ed8d3b012a9
:id: fee348e8-74be-11f1-a8a1-0ed8d3b012a9

````{python}
import random as rd

# Construction déterministe : on part des exposants (réponses) puis on bâtit les arguments.
base1 = rd.choice([2, 3, 5, 7, 10])
exp1 = rd.randint(2, 5)
arg1 = base1 ** exp1
base2 = rd.choice([b for b in [2, 3, 5, 7, 10] if b != base1])
exp2 = rd.randint(2, 4)
arg2 = base2 ** exp2
base3 = rd.choice([b for b in [2, 3, 5, 7] if b not in [base1, base2]])
exp3 = rd.randint(2, 5)
arg3 = base3 ** exp3
l1, l2, l3 = exp1, exp2, exp3

base4 = rd.choice([2, 3, 5, 7, 10])
base5 = rd.choice([b for b in [2, 3, 4, 5, 6, 7, 10] if b != base4])
l4, l5 = 1, 0

globals()
````

:::::{question}
:questionType: FGQ
:questionId: 0
:questionIndex: 0
:solution: [["ord","{{ l1 }}","{{ l2 }}","{{ l3 }}"],["0","0","0"]]

::::{questionStatement}
{fr}`Évaluer`{en}`Evaluate` $\log_{ {{ base1 }} }({{ arg1 }})$, $\log_{ {{ base2 }} }({{ arg2 }})$ {fr}`et`{en}`and` $\log_{ {{ base3 }} }({{ arg3 }})$ {fr}`en reconnaissant chaque argument comme une puissance de la base.`{en}`by recognizing each argument as a power of the base.`

$\log_{ {{ base1 }} }({{ arg1 }}) =$ {input}`||70`

$\log_{ {{ base2 }} }({{ arg2 }}) =$ {input}`||70`

$\log_{ {{ base3 }} }({{ arg3 }}) =$ {input}`||70`
::::

::::{questionHint}
${{ arg1 }}={{ base1 }}^{ {{ exp1 }} }$, ${{ arg2 }}={{ base2 }}^{ {{ exp2 }} }$, ${{ arg3 }}={{ base3 }}^{ {{ exp3 }} }$ ; {fr}`utiliser`{en}`use` $\log_{b}(b^{k})=k$.
::::

::::{displayedSolution}
$\log_{ {{ base1 }} }({{ arg1 }}) = {{ l1 }}$

$\log_{ {{ base2 }} }({{ arg2 }}) = {{ l2 }}$

$\log_{ {{ base3 }} }({{ arg3 }}) = {{ l3 }}$
::::

::::{detailedSolution}
{fr}`Par la relation réciproque`{en}`By the reciprocal relation` $\log_{b}(b^{k})=k$ :

\begin{equation*}
\log_{ {{ base1 }} }({{ arg1 }}) &= \log_{ {{ base1 }} }({{ base1 }}^{ {{ exp1 }} }) \\
&= {{ l1 }}, \\
\log_{ {{ base2 }} }({{ arg2 }}) &= \log_{ {{ base2 }} }({{ base2 }}^{ {{ exp2 }} }) \\
&= {{ l2 }}, \\
\log_{ {{ base3 }} }({{ arg3 }}) &= \log_{ {{ base3 }} }({{ base3 }}^{ {{ exp3 }} }) \\
&= {{ l3 }}.
\end{equation*}
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
:solution: [["ord","{{ l4 }}","{{ l5 }}"],["0","0"]]

::::{questionStatement}
{fr}`Évaluer`{en}`Evaluate` $\log_{ {{ base4 }} }({{ base4 }})$ {fr}`et`{en}`and` $\log_{ {{ base5 }} }(1)$, {fr}`et justifier à partir des cas`{en}`and justify from the cases` $b^1=b$ {fr}`et`{en}`and` $b^0=1$.

$\log_{ {{ base4 }} }({{ base4 }}) =$ {input}`||70`

$\log_{ {{ base5 }} }(1) =$ {input}`||70`
::::

::::{questionHint}
${{ base4 }}={{ base4 }}^1$ {fr}`et`{en}`and` $1={{ base5 }}^0$.
::::

::::{displayedSolution}
$\log_{ {{ base4 }} }({{ base4 }}) = {{ l4 }}$

$\log_{ {{ base5 }} }(1) = {{ l5 }}$
::::

::::{detailedSolution}
{fr}`On a`{en}`We have` ${{ base4 }}={{ base4 }}^1$ {fr}`et`{en}`and` $1={{ base5 }}^0$, {fr}`donc :`{en}`so:`

\begin{equation*}
\log_{ {{ base4 }} }({{ base4 }}) &= \log_{ {{ base4 }} }({{ base4 }}^1) \\
&= {{ l4 }}, \\
\log_{ {{ base5 }} }(1) &= \log_{ {{ base5 }} }({{ base5 }}^0) \\
&= {{ l5 }}.
\end{equation*}

{fr}`En particulier`{en}`In particular` $\log_{b}(1)=0$ {fr}`pour toute base : le graphe d'un logarithme passe toujours par`{en}`for any base: the graph of a logarithm always passes through` $(1,0)$.
::::

::::{weightDistribution}
:logic: 20
:abstraction: 30
:reasoning: 30
:calculation: 20
::::
:::::

`````