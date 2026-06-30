#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 19:11:52 2022

@author: jlebovits
"""
from __future__ import division
import sys
from copy import deepcopy
from src.scripts.pxs_runtime import myst, get_pxs_lang
from sympy.printing.latex import LatexPrinter


# import src.scripts.Mes_fctions.Mes_fctions_deterministes
# from src.scripts.Mes_fctions.Mes_fctions_deterministes import *

# import src.scripts.Mes_fctions.Mes_fctions_generalistes
# from src.scripts.Mes_fctions.Mes_fctions_generalistes import *

# import src.scripts.Mes_fctions.Mes_fctions_probabilistes
# from src.scripts.Mes_fctions.Mes_fctions_probabilistes import *

# import src.scripts.Mes_fctions.Mes_fctions_d_ecriture_Latex
# from src.scripts.Mes_fctions.Mes_fctions_d_ecriture_Latex import *

# import src.scripts.Mes_fctions.Mes_fctions_d_alg_generale
# from src.scripts.Mes_fctions.Mes_fctions_d_alg_generale import *


from sympy import *
import functools as fct
import math as m
import random as rd
import numpy as np
from src.scripts.Mes_fctions.Mes_fctions_d_alg_lineaire import randmatrixdiagonale, zeros
from src.scripts.Mes_fctions.Mes_fctions_probabilistes_bis import pxsl_res_num
from sympy.stats import P, E, variance, Die, Normal, DiscreteUniform, Bernoulli, sample, Binomial, density,  Normal, sample_iter, given



def pxsl_pow(x, n=1, opt=0, displaystyle=True):
    """
    Fr : Fonction permettant d'écrire le nombre x entouré de parenthèses
    lorsqu'il est négatif ou irrationnel avec deux termes (par ex : 1+sqrt(2) ou 3sqrt(2))
    Ne fonctionne pas pour des valeurs numériques non simplifiées (par ex : 1+3 ou 3*3/2)
    En : Function that writes the number x surrounded by parentheses
    when it is negative or irrational with two terms (e.g.: 1+sqrt(2) or 3sqrt(2))
    Does not work for unsimplified numerical values (e.g.: 1+3 ou 3*3/2)

    Version 5
    ---------
    13/02/25

    Vérification
    ------
    Auteur : Delphine
    Vérificateurs : ??

    Paramètres
    ----------
    x : nombre ou expression
        La base à élever à la puissance n
    n : int, optional
        L'exposant (défaut: 1)
    opt : int, optional
        Option de formatage (défaut: 0)
        0: formatage standard
        1: simplifie l'affichage pour x=1, x=0 ou n=1
        2: simplifie davantage et renvoie une chaîne vide pour x=0
    displaystyle : bool, optional
        Si True, utilise \displaystyle pour les fractions (défaut: False)

    Retour
    ------
    str
        retourne l'expression en latex

    Fonction utilisée par
    ---------------------
    pxsl_sum_matrix, pxsl_prod_scalar_matrix, pxsl_prod_matrix, pxsl_pow_matrix
:pxs_trigger: |
    afficher coefficient avec parenthèses, parenthéser terme négatif,
    puissance sécurisée coeff^n, affichage pédagogique produit,
    substitution valeur numérique dans formule, dérivée formelle affichage,
    premier calcul d'une dérivée ligne par ligne, IBP ligne par ligne,
    pxsl_pow(coeff, n), a^2 avec a négatif, (-3)^2 éviter -3^2,
    coefficient dans équation différentielle y' + ay = ..., affichage trinôme,
    étapes de développement polynôme, substitution x=a dans f(x)
:pxs_returns: |
    Chaîne LaTeX (str) affichant `coeff^puissance` avec parenthèses
    automatiques autour de `coeff` si celui-ci est négatif, rationnel,
    ou une expression composée (Add). Si puissance=1, retourne juste le
    coefficient (avec parenthèses si nécessaire). Indispensable pour
    tout affichage pédagogique où on substitue des valeurs numériques
    dans une formule littérale.
:pxs_example: |
    # Question : b^2 - 4ac avec a=-3, b=5
    # À la main : f"{b}^2 - 4 \\times {a}" donne "5^2 - 4 \\times -3" ← FAUX
    latex_b2 = pxsl_pow(b, 2)   # "5^2"
    latex_a  = pxsl_pow(a, 1)   # "(-3)"
    # myst(r"\Delta = \py{latex_b2} - 4 \times \py{latex_a} \times ...")
:pxs_antipattern: |
    ✗ f"{coeff}^{n}" en f-string — casse les signes négatifs ((-3)^2 devient "-3^2"),
      oublie les parenthèses autour des fractions (1/2)^2, et ne gère pas le cas n=1.
    ✓ Utiliser pxsl_pow(coeff, n)
    :pxs_antipattern: Écrire f"({x})^{{{n}}}" à la main qui ne gère pas les cas x=1, x=0, n=1, ni les sous-cas Rational/Add/Mul/Symbol.
    """

    # Préparation de l'expression LaTeX selon le mode displaystyle
    if displaystyle:
        latex_x = r"\displaystyle " + latex(x)
    else:
        latex_x = latex(x)

    # Cas où x est une expression (Add ou Mul) ou nombre négatif:
    if isinstance(x, Add) or isinstance(x, Mul) :
        if n == 1 :
            return myst(r"""\left(\py{latex_x}\right)""", globals(), locals())
        else:
            return myst(r"""\left(\py{latex_x}\right)^{\py{n}}""", globals(), locals())
    # Cas où x est un Rational
    elif isinstance(x,Rational) and x.q!=1:
        if n == 1 : # Pas de parenthèses quand n=1
            if x < 0: # si la fraction est négative il faut des parenthèses
                return myst(r"""\left(\py{latex_x}\right)""", globals(), locals())
            else:
                return myst(r"""\py{latex_x}""", globals(), locals())
        else: # Parenthèses quand n différent de 1
            return myst(r"""\left(\py{latex_x}\right)^{\py{n}}""", globals(), locals())
    # Cas où x est un Symbol:
    elif isinstance(x,Symbol):
        if n == 1:
            return myst(r"""\py{latex_x}""", globals(), locals())
        else:
            return myst(r"""\py{latex_x}^{\py{n}}""", globals(), locals())
    # Cas où x est strictement négatif
    elif x<0:
        if n == 1:
            return myst(r"""\left(\py{latex_x}\right)""", globals(), locals())
        else:
            return myst(r"""\left(\py{latex_x}\right)^{\py{n}}""", globals(), locals())
    # Cas où x est un nombre positif ou nul
    else:
        # Option 0: formatage standard
        if opt == 0:
            if n == 1:
                return myst(r"""\py{latex_x}""", globals(), locals())
            else:
                return myst(r"""\py{latex_x}^{\py{n}}""", globals(), locals())

        # Option 1: simplifie pour x=0, x=1 ou n=1
        elif opt == 1:
            if x == 1 or x == 0 or n == 1:
                return myst(r"""\py{latex_x}""", globals(), locals())
            else:
                return myst(r"""\py{latex_x}^{\py{n}}""", globals(), locals())

        # Option 2: simplifie davantage, chaîne vide pour x=0
        else:  # opt == 2 ou autres valeurs
            if x == 0:
                return myst(r""" """, globals(), locals())
            elif x == 1 or n == 1:
                return myst(r"""\py{latex_x}""", globals(), locals())
            else:
                return myst(r"""\py{latex_x}^{\py{n}}""", globals(), locals())


################ EXEMPLES ##################
# pxsl_pow(3,2) retourne l'écriture latex de 3^{2}
# pxsl_pow(-3,2) retourne l'écriture latex de \left(-3\right)^{2}
# pxsl_pow(-3+sqrt(2),3) retourne l'écriture latex de \left(-3+\sqrt{2}\right)^{3}
# pxsl_pow(-3*sqrt(2),3) retourne l'écriture latex de \left(-3\sqrt{2}\right)^{3}
# pxsl_pow(3,Symbol('n')) retourne l'écriture latex de 3^{n}
# pxsl_pow(1,'n') retourne l'écriture latex de 1^n
# pxsl_pow(0,Symbol('n')) retourne l'écriture latex de 0^n
#
# x=Symbol('x')
# y=Symbol('y')
# pxsl_pow(x+y,Symbol('n')) retourne l'écriture latex de \left(x+y\right)^{n}
#
# x=Symbol('x')
# y=Symbol('y')
# pxsl_pow(x*y,Symbol('n')) retourne l'écriture latex de \left(x y\right)^{n}


def pxsl_matrix(A, sepG="(", sepD=")", display=False, res_num=False):
    """
    Return a LaTeX representation of a matrix with right-aligned entries.

    This function converts a matrix into a nicely formatted LaTeX matrix.
    By default, entries are displayed as raw values. Optional display modes
    allow symbolic LaTeX rendering or numerical result formatting.

    Parameters
    ----------
    A : Matrix
        The matrix to be displayed.
    sepG : str, optional
        Left delimiter of the matrix (default "(").
        In English mode, it is automatically replaced by "[".
    sepD : str, optional
        Right delimiter of the matrix (default ")").
        In English mode, it is automatically replaced by "]".
    display : bool, optional
        If True, matrix entries are rendered in LaTeX format.
    res_num : bool, optional
        If True (and `display=True`), entries are displayed as numerical results.

    Returns
    -------
    str
        A LaTeX string representing the formatted matrix.

    Examples
    --------
    Basic usage with raw values:

    >>> from sympy import Matrix
    >>> A = Matrix([[1, 2], [3, 4]])
    >>> pxsl_matrix(A)
    '\\\\left(\\begin{array}{rr}1 & 2\\\\[0.3em]3 & 4\\end{array}\\\\right)'

    Using custom delimiters:

    >>> pxsl_matrix(A, sepG='[', sepD=']')
    '\\\\left[\\begin{array}{rr}1 & 2\\\\[0.3em]3 & 4\\end{array}\\\\right]'

    Displaying symbolic expressions in LaTeX:

    >>> from sympy import symbols
    >>> x = symbols('x')
    >>> B = Matrix([[x, x**2], [1/x, 2]])
    >>> pxsl_matrix(B, display=True)
    '\\\\left(\\begin{array}{rr}x & x^{2}\\\\[0.3em]\\frac{1}{x} & 2\\end{array}\\\\right)'

    Displaying numerical results (after evaluation):

    >>> from sympy import Rational
    >>> C = Matrix([[Rational(1, 2), Rational(3, 4)], [1, 2]])
    >>> pxsl_matrix(C, display=True, res_num=True)
    '\\\\left(\\begin{array}{rr}0.5 & 0.75\\\\[0.3em]1 & 2\\end{array}\\\\right)'

    :pxs_trigger: afficher matrice LaTeX, délimiteurs personnalisés, déterminant |…|, matrice entre parenthèses ou crochets, alignement colonnes
    :pxs_returns: |
        Objet myst contenant la représentation LaTeX d'une matrice en
        environnement array avec entrées alignées à droite et délimiteurs
        configurables (par défaut ( ) en français, [ ] en anglais).
        Mode display=True : entrées rendues via latex(). Mode res_num=True :
        entrées formatées comme résultats numériques via pxsl_res_num.
    :pxs_example: |
        A = Matrix([[1, 2, 3], [4, 5, 6]])
        # Dans MyST : $A = \\py{pxsl_matrix(A)}$
        # Pour un déterminant : $\\py{pxsl_matrix(A, sepG='|', sepD='|')}$
    :pxs_antipattern: Écrire f"\\\\begin{{pmatrix}}{a}&{b}\\\\\\\\{c}&{d}\\\\end{{pmatrix}}" à la main sans gérer la dimension variable ni la langue.
    """
    [n,p]=A.shape
    pxs_lang = get_pxs_lang()
    if pxs_lang == "en" and sepG=='(':
        sepG='['
    if pxs_lang == "en" and sepD==')':
        sepD=']'
    expr=myst(r"""\left\py{sepG}\begin{array}{\py{'r'*p}}""",globals(),locals())
    for i in range(n):
        if display:
            if res_num:
                expr+=myst(r"""\py{pxsl_res_num(A[i,0], egal = False)}""",globals(),locals())
            else:
                expr+=myst(r"""\py{latex(A[i,0])}""",globals(),locals())
        else:
            expr+=myst(r""" \py{A[i,0]}""",globals(),locals())
        for j in range(p-1):
            if display:
                if res_num:
                    expr+=myst(r""" &\py{pxsl_res_num(A[i,1+j], egal = False)}""",globals(),locals())
                else:
                    expr+=myst(r""" &\py{latex(A[i,1+j])}""",globals(),locals())
            else:
                expr+=myst(r""" &\py{A[i,1+j]}""",globals(),locals())
        expr+=myst(r"""\\[0.3em]""")
    expr+=myst(r"""\end{array}\right\py{sepD}""",globals(),locals())
    return expr


################ EXEMPLES ##################
# pxsl_matrix(Matrix([[1,2,3],[2,-3,4]])) retourne
# l'expression latex : \left(\begin{array}{rrr}1&2&3\2&-3&4\\end{array}\right)
# soit la matrice (entourée de parenthèses) :
#                       1  2 3
#                       2 -3 4
# pxsl_matrix(Matrix([[1,2,3],[2,-3,4]]),'|','|') retourne
# l'expression latex : \left|\begin{array}{rrr}1&2&3\2&-3&4\\end{array}\right|
# soit le déterminant (matrice entourée de |)  :
#                       1  2 3
#                       2 -3 4
# on peut aussi utiliser une forme de séparateur d'un côté et un autre de l'autre côté


def pxsl_sum_matrix(A,B,s="+",sepG='(',sepD=')'):
  """
    Fonction permettant d'afficher le détail de la somme (ou la différence) de deux matrices

    Version
    -------
    13/02/25

    Vérification
    ------------
    Auteur : Ronan - Delphine
    Vérificateurs :

    Paramètres
    ----------
    A : Matrix
        Première matrice de la somme
    B : Matrix
        Deuxième matrice de la somme
    s : str
        "+" par défaut pour réaliser une somme
        "-" pour réaliser une différence
    sepG : str
           délimiteur gauche de la matrice
    sepD : str
           délimiteur droit de la matrice

    Retour
    ------
    str
        retourne l'expression en latex

    Fonction utilisée par
    ---------------------
    aucune fonction pyxiscience

    :pxs_trigger: détailler somme de matrices, a_ij + b_ij terme à terme, différence matricielle A - B, affichage pédagogique A+B non calculé
    :pxs_returns: |
        Objet myst affichant la matrice dont chaque coefficient est
        "a_ij + b_ij" (ou "a_ij - b_ij" si s="-") sans calcul effectué,
        avec parenthèses automatiques autour des b_ij négatifs via pxsl_pow.
    :pxs_example: |
        A = Matrix([[-1, 0], [2, 3]])
        B = Matrix([[2, -3], [1, -3]])
        # Dans MyST : $A + B = \\py{pxsl_sum_matrix(A, B)}$
        # Résultat : matrice des expressions "-1+2", "0+(-3)", "2+1", "3+(-3)"
    :pxs_antipattern: Calculer A + B avec sympy puis afficher le résultat final — perd le détail pédagogique "a_ij + b_ij" montrant l'opération.
  """
  [n,p]=A.shape
  pxs_lang = get_pxs_lang()
  if pxs_lang == "en" and sepG=='(':
    sepG='['
  if pxs_lang == "en" and sepD==')':
    sepD=']'
  expr=myst(r"""\left\py{sepG}\begin{array}{\py{'c'*p}}""",globals(),locals())
  for i in range(n):
    expr+=myst(r""" \py{A[i,0]}\py{s}""",globals(),locals())+pxsl_pow(B[i,0])
    for j in range(p-1):
      expr+=myst(r""" &\py{A[i,1+j]}\py{s}""",globals(),locals())+pxsl_pow(B[i,1+j])
    expr+=myst(r"""\\""")
  expr+=myst(r"""\end{array}\right\py{sepD}""",globals(),locals())
  return expr

################ EXEMPLES ##################
# pxsl_sum_matrix(Matrix([[-1,0,3],[2,3,4]]),Matrix([[2,3,5],[2,-3,4]])) retourne
# l'expression latex : \left(\begin{array}{ccc} -1+2&0+3&3+5\2+2&3+\left(-3\right)&4+4\\end{array}\right)
# soit la matrice :
#                       -1+2   0+3    3+5
#                        2+2  3+(-3)  4+4
# la commande pxsl_sum_matrix(Matrix([[-1,0,3],[2,3,4]]),Matrix([[2,3,5],[2,-3,4]]),"+") renvoie la même chose
# pxsl_sum_matrix(Matrix([[-1,0,3],[2,3,4]]),Matrix([[2,3,5],[2,-3,4]]),"-") retourne
# l'expression latex : \left(\begin{array}{-1-2&0-3&3-5\2-2&3-\left(-3\right)&4-4\\end{array}\right)
# soit la matrice :
#                       -1-2   0-3    3-5
#                        2-2  3-(-3)  4-4

def pxsl_prod_scalar_matrix(lamb,A,mult="times",sepG='(',sepD=')'):
  """
    Fonction permettant d'afficher le détail du produit entre un scalaire et une matrice

    Version
    -------
    13/02/25

    Vérification
    ------------
    Auteur : Ronan - Delphine
    Vérificateurs :

    Paramètres
    ----------
    lamb : float
           coefficient multiplicateur
    A : Matrix
        Matrice
    mult : str
           "times" par défaut, peut-être remplacé par "cdot" pour modifier le symbole multiplicatif
    sepG : str
           délimiteur gauche de la matrice
    sepD : str
           délimiteur droit de la matrice

    Retour
    ------
    str
        retourne l'expression en latex

    Fonction utilisée par
    ---------------------
    aucune fonction pyxiscience

    :pxs_trigger: détailler produit scalaire par matrice, λ·A terme à terme, afficher 2×A sans calcul, lambda x a_ij pédagogique
    :pxs_returns: |
        Objet myst affichant la matrice dont chaque coefficient est
        "λ × a_ij" (ou "λ · a_ij" si mult="cdot") sans calcul effectué,
        avec parenthèses automatiques autour des a_ij négatifs via pxsl_pow.
    :pxs_example: |
        A = Matrix([[1, 2, -3], [2, 3, 4]])
        # Dans MyST : $2A = \\py{pxsl_prod_scalar_matrix(2, A)}$
        # Avec symbole ·  : $\\py{pxsl_prod_scalar_matrix(2, A, "cdot")}$
    :pxs_antipattern: Calculer 2*A avec sympy puis afficher — perd le détail "2×1, 2×(-3)" montrant le produit avant simplification.
  """
  [n,p]=A.shape
  pxs_lang = get_pxs_lang()
  if pxs_lang == "en" and sepG=='(':
    sepG='['
  if pxs_lang == "en" and sepD==')':
    sepD=']'
  expr=myst(r"""\left\py{sepG}\begin{array}{\py{'c'*p}}""",globals(),locals())
  for i in range(n):
    expr+=myst(r"""\py{lamb}\\py{mult}""",globals(),locals())+pxsl_pow(A[i,0])
    for j in range(p-1):
      expr+=myst(r"""&""")+myst(r"""\py{lamb}\\py{mult}""",globals(),locals())+pxsl_pow(A[i,1+j])
    expr+=myst(r"""\\""")
  expr+=myst(r"""\end{array}\right\py{sepD}""",globals(),locals())
  return expr

################ EXEMPLES ##################
# pxsl_prod_scalar_matrix(2,Matrix([[1,2,-3],[2,3,4]])) retourne
# l'expression latex : \left(\begin{array}{ccc} 2\times1&2\times2&2\times\left(-3\right)\2\times2&2\times3&2\times4\\end{array}\right)
# donc la matrice :
#                       2 x 1   2 x 2    2 x (-3)
#                       2 x 2   2 x 3     2 x 4
# la commande pxsl_prod_scalar_matrix(2,Matrix([[1,2,-3],[2,3,4]]),"times") renvoie la même chose
# pxsl_prod_scalar_matrix(-2,Matrix([[1,2,-3],[2,3,4]])) retourne
# l'expression latex : \left(\begin{array}{ccc} -2\times1&-2\times2&-2\times\left(-3\right)\-2\times2&-2\times3&-2\times4\\end{array}\right)
# soit la matrice :
#                       -2 x 1   -2 x 2    -2 x (-3)
#                       -2 x 2   -2 x 3     -2 x 4
# pxsl_prod_scalar_matrix(2,Matrix([[1,2,-3],[2,3,4]]),"cdot") retourne
# l'expression latex : \left(\begin{array}{ccc} 2\cdot1&2\cdot2&2\cdot\left(-3\right)\2\cdot2&2\cdot3&2\cdot4\\end{array}\right)
# soit la matrice :
#                       -2.1   -2.2    -2.(-3)
#                       -2.2   -2.3     -2.4   avec le . correspondant à la commande latex cdot
# pxsl_prod_scalar_matrix('a',Matrix([[1,2,-3],[2,3,4]])) retourne
# l'expression latex : \left(\begin{array}{ccc} a\times1&a\times2&a\times\left(-3\right)\a\times2&a\times3&a\times4\\end{array}\right)
# soit la matrice :
#                       a x 1   a x 2    a x (-3)
#                       a x 2   a x 3     a x 4
# pxsl_prod_scalar_matrix(Symbol('a'),Matrix([[1,2,-3],[2,3,4]])) renvoie la même chose

def pxsl_prod_matrix(A,B,mult="times",sepG='(',sepD=')'):
  """
    Fonction permettant d'afficher le détail du produit entre deux matrices

    Version
    -------
    13/02/25

    Vérification
    ------------
    Auteur : Ronan - Delphine
    Vérificateurs :

    Paramètres
    ----------
    A : Matrix
        Première matrice du produit
    B : Matrix
        Deuxième matrice du produit
    mult : str
          "times" par défaut, peut-être remplacé par "cdot" pour modifier le symbole multiplicatif
    sepG : str
           délimiteur gauche de la matrice
    sepD : str
           délimiteur droit de la matrice

    Retour
    ------
    str
        retourne l'expression en latex

    Fonction utilisée par
    ---------------------
    aucune fonction pyxiscience

    :pxs_trigger: détailler produit matriciel A×B, somme a_ik × b_kj, formule produit matrices non calculée, pédagogique composante (AB)_ij
    :pxs_returns: |
        Objet myst affichant la matrice produit A·B où chaque coefficient
        (AB)_ij est présenté sous forme développée "a_i0·b_0j + a_i1·b_1j + …"
        sans calcul effectué, avec parenthèses automatiques via pxsl_pow.
    :pxs_example: |
        A = Matrix([[-1, -2, 3], [2, 0, 4]])
        B = Matrix([[2, 3], [2, -3], [2, 3]])
        # Dans MyST : $AB = \\py{pxsl_prod_matrix(A, B)}$
    :pxs_antipattern: Calculer A*B avec sympy puis afficher — perd l'explicitation pédagogique des sommes de produits de la formule matricielle.
  """
  [nA,pA]=A.shape
  [nB,pB]=B.shape
  pxs_lang = get_pxs_lang()
  if pxs_lang == "en" and sepG=='(':
    sepG='['
  if pxs_lang == "en" and sepD==')':
    sepD=']'
  expr=myst(r"""\left\py{sepG}\begin{array}{\py{'c'*pB}}""",globals(),locals())
  for i in range(nA):
    expr+=myst(r"""\py{A[i,0]}\\py{mult}""",globals(),locals())+pxsl_pow(B[0,0])
    for k in range(pA-1):
      expr+=myst(r"""+""")+pxsl_pow(A[i,1+k])+myst(r"""\\py{mult}""",globals(),locals())+pxsl_pow(B[1+k,0])
    for j in range(pB-1):
      expr+=myst(r"""&""")+myst(r"""\py{A[i,0]}\\py{mult}""",globals(),locals())+pxsl_pow(B[0,1+j])
      for k in range(pA-1):
          expr+=myst(r"""+""")+pxsl_pow(A[i,1+k])+myst(r"""\\py{mult}""",globals(),locals())+pxsl_pow(B[1+k,1+j])
    expr+=myst(r"""\\""")
  expr+=myst(r"""\end{array}\right\py{sepD}""",globals(),locals())
  return expr

################ EXEMPLES ##################
# pxsl_prod_matrix(Matrix([[-1,-2,3],[2,0,4]]),Matrix([[2,3,5],[2,-3,4],[2,3,4]])) retourne
# l'expression latex : \left(\begin{array}{ccc} -1\times2+\left(-2\right)\times2+3\times2&-1\times3+\left(-2\right)\times\left(-3\right)+3\times3&-1\times5+\left(-2\right)\times4+3\times4\2\times2+0\times2+4\times2&2\times3+0\times\left(-3\right)+4\times3&2\times5+0\times4+4\times4\\end{array}\right)
# donc la matrice :
#                       -1x2+(-2)x2+3x2   -1x3+(-2)x(-3)+3x3    -1x5+(-2)x4+3x4
#                          2x2+0x2+4x2       2x3+0x(-3)+4x3        2x5+0x4+4x4
# la commande pxsl_prod_matrix(Matrix([[-1,-2,3],[2,0,4]]),Matrix([[2,3,5],[2,-3,4],[2,3,4]]),"times") renvoie la même chose
# pxsl_prod_matrix(Matrix([[-1,-2,3],[2,0,4]]),Matrix([[2,3,5],[2,-3,4],[2,3,4]]),"cdot") retourne la matrice :
#                       -1.2+(-2).2+3.2   -1.3+(-2).(-3)+3.3    -1.5+(-2).4+3.4
#                          2.2+0.2+4.2       2.3+0.(-3)+4.3        2.5+0.4+4.4    avec le . correspondant à la commande latex cdot


def pxs_system_simpl(n=3,N="",opt="sys",max_coef=2,limit_sum=15):
  """
    Fonction permettant de créer les matrices A et B d'un système linéaire en s'assurant de la simplicité de la solution
    Par défaut, la matrice est de taille 3x3 et B un vecteur aléatoire, de composant entre 1 et 3, de dimension 3
    La fonction est également utilisable pour générer A dans le cadre de l'inversion de matrice

    Version
    -------
    25/03/25

    Vérification
    ------------
    Auteur : Delphine
    Vérificateurs :

    Paramètres
    ----------
      n : int
          Dimension de la matrice A
      N : Matrix
          Deuxième matrice du produit, solution du système
      opt : char
            "sys" : c'est un système, on renvoie A et B pour Ax=B
            sinon : on renvoie seulement A
      max_coef : int
                 on tire les opérations à réaliser sur les coefficients entre 1 et max_coef
      limit_sum : int
                  si les coefficients de A et B dépassent la valeur de limit_sum la simulation est relancée

    Retour
    ------
      A,B
        retourne les deux matrices du système AX=B

    Fonction utilisée par
    ---------------------
    pxs_commute_matrix

    :pxs_trigger: générer système linéaire à solution simple, exercice AX=B aléatoire avec solution entière, matrice inversible à coefficients bornés
    :pxs_returns: |
        Si opt="sys" : tuple (A, B) de Matrix sympy tels que AX=B admet la
        solution N (vecteur fourni ou aléatoire à composantes dans [-3,3]).
        Sinon : Matrix A seule (typiquement pour une inversion).
        Les coefficients de A et B sont bornés en valeur absolue par limit_sum.
    :pxs_example: |
        A, B = pxs_system_simpl(n=3)
        # Dans MyST : $\\py{pxsl_system_lin(A, B)}$
        # de solution entière simple
    :pxs_antipattern: Tirer les coefficients de A et B au hasard sans garantir une solution simple — produit des solutions irrationnelles ou énormes.
  """
  # La matrice est N est copiée pour ne pas modifier la matrice originale
  if N=="":
    N=Matrix([rd.randint(-3,3) for i in range(n)])
  A,B=eye(n),N.copy()
  # La variable compte permet de compter le nombre d'éléments >15 en valeur absolue dans la matrice A
  # Si un élément est supérieur à 15 en valeur absolue, on recommence. La variable compte est initialisée à 1 par défaut
  compte=1
  while compte!=0:
    A,B=eye(n),N.copy()
  # Tant que le nombre de 0 dans la matrice A est supérieur à la dimension -1, on continue
  # on autorise donc pas de 0 pour une matrice 2x2, on autorise un 0 pour une matrice 3x3 etc...
    while sum(1 for element in A if element == 0)>=n-1:
  # on tire aléatoirement les deux lignes impliquées dans la relation
      index=rd.sample([i for i in range(n)],2)
  # on tire les coefficients multiplicateurs
      lamb=[rd.choice([-1,1])*rd.randint(1,max_coef),rd.choice([-1,1])*rd.randint(1,max_coef)]
  # On aura par exemple L1=2*L1+3*L2
      A[index[0],:]=lamb[0]*A[index[0],:]+lamb[1]*A[index[1],:]
      B[index[0],:]=lamb[0]*B[index[0],:]+lamb[1]*B[index[1],:]
    compte=sum(1 for element in A if abs(element) >= limit_sum)+sum(1 for element in B if abs(element) >= limit_sum)
  if opt=="sys":
    return A,B
  else:
    return A



################ EXEMPLES ##################
# pxs_system_simpl() retournera par exemple les matrices :
#              2  -4  -2                 -4
#          A=  2  -5  -2              B= -6
#              2  -4  -4                  0
# pour la solution
#              0
#          x=  2
#             -2



def pxsl_ax(a,x=Symbol('x'),sign=" ",frac=True):
  """
    Fonction permettant d'afficher l'expression ax en fonction des valeurs de a

    Version
    -------
    23/09/25

    Vérification
    ------------
    Auteur : Delphine
    Vérificateurs :

    Paramètres
    ----------
    a : numerique
    x : Symbol ('x' par défaut)
        si x=Symbol("val"), la valeur a est affichée dans tous les cas
    sign : str
           "" ou "+", "" par défaut, le symbole "+" indique qu'il faut écrire le signe '+'
           devant l'expression.
    frac : boolean
           True : fraction écrite en mode math
           False : fraction écrite a/b en ligne

    Retour
    ------
    str
        retourne l'expression en latex

    Fonction utilisée par
    ---------------------
    pxsl_system_lin, pxsl_lines_op

    :pxs_trigger: afficher terme ax avec gestion signes automatique, coefficient fraction dans équation, a=1 ou a=-1 simplifié, a=0 chaîne vide, terme d'un système linéaire
    :pxs_returns: |
        Objet myst représentant "ax" en LaTeX avec :
        - chaîne vide si a=0
        - "x" ou "-x" si a=±1 (coefficient implicite)
        - "a/b x" en ligne si frac=False et a rationnel
        - "\\frac{p}{q}x" si frac=True
        - préfixe '+' configurable via sign pour l'enchaînement des termes.
    :pxs_example: |
        pxsl_ax(2, Symbol('x'))                # → "+2x"
        pxsl_ax(Rational(1,3), Symbol('x_1'))  # → "+\\frac{1}{3}x_1"
        pxsl_ax(0, Symbol('x'))                # → "" (chaîne vide)
        pxsl_ax(-1, Symbol('L_1'))             # → "-L_1"
    :pxs_antipattern: Utiliser f"{a}{x}" qui produit "1x", "-1x", "0x" au lieu de "x", "-x", "" et ne gère pas le signe + devant un terme positif.
  """

  # on règle le cas a nul en premier
  if a==0:
    return myst(r""" """)
  # on considère ensuite le cas a entier (qui est aussi considéré comme un Rational donc
  # il ne faut pas inverser les if)
  if isinstance(a,Integer):
    if a==1:
      return myst(r""" \py{sign} 1""",globals(),locals()) if x is None else myst(r""" \py{sign} \py{x}""",globals(),locals())
    elif a==-1:
      return myst(r"""  - 1""",globals(),locals()) if x is None else myst(r"""  - \py{x}""",globals(),locals())
    elif a<0:
      return myst(r""" \py{a}""",globals(),locals()) if x is None else myst(r""" \py{a}\py{x}""",globals(),locals())
    else :
      return myst(r"""\py{sign} \py{a}""",globals(),locals()) if x is None else myst(r"""\py{sign} \py{a}\py{x}""",globals(),locals())
  # on considère ensuite le cas a Rational
  if isinstance(a,Rational) and frac == True:
    if a<0:
      return myst(r""" -\frac{\py{abs(a.p)}}{\py{a.q}}""",globals(),locals()) if x is None else myst(r""" -\frac{\py{abs(a.p)}}{\py{a.q}}\py{x}""",globals(),locals())
    else:
      return myst(r""" \py{sign}\frac{\py{a.p}}{\py{a.q}}""",globals(),locals()) if x is None else myst(r""" \py{sign}\frac{\py{a.p}}{\py{a.q}}\py{x}""",globals(),locals())
  if isinstance(a,Rational) and frac == False:
    if a.p==-1:
      return myst(r""" - 1/\py{a.q}""",globals(),locals()) if x is None else myst(r""" - \py{x}/\py{a.q}""",globals(),locals())
    elif a.p==1:
      return myst(r""" \py{sign}1/\py{a.q}""",globals(),locals()) if x is None else myst(r""" \py{sign}\py{x}/\py{a.q}""",globals(),locals())
    elif a<0:
      return myst(r""" -\py{abs(a.p)}/\py{a.q}""",globals(),locals()) if x is None else myst(r""" -\py{abs(a.p)}\py{x}/\py{a.q}""",globals(),locals())
    else:
      return myst(r""" \py{sign}\py{a.p}/\py{a.q}""",globals(),locals()) if x is None else myst(r""" \py{sign}\py{a.p}\py{x}/\py{a.q}""",globals(),locals())
  # on ferme avec le traitement pour tout nombre car certains calculs envoient un int
  # non reconnu dans les conditionnels précédants

  if a==1:
    return myst(r""" \py{sign} 1""",globals(),locals()) if x is None else myst(r""" \py{sign} \py{x}""",globals(),locals())
  elif a==-1:
    return myst(r"""  - 1""",globals(),locals()) if x is None else myst(r"""  - \py{x}""",globals(),locals())
  try:
      if a<0:
          return myst(r""" \py{a}""",globals(),locals()) if x is None else myst(r""" \py{a}\py{x}""",globals(),locals())
      else:
          return myst(r"""\py{sign} \py{a}""",globals(),locals()) if x is None else myst(r"""\py{sign} \py{a}\py{x}""",globals(),locals())
  except :
    return myst(r"""\py{sign} \py{latex(a)}""",globals(),locals()) if x is None else myst(r"""\py{sign} \py{latex(a)}\py{x}""",globals(),locals())


################ EXEMPLES ##################
# pxsl_ax(2) retourne
# l'expression latex : 2x
#
# pxsl_ax(2,Symbol('y')) retourne
# l'expression latex : 2y
#
# pxsl_ax(2,Symbol('L_{'+str(1)+'}')) retourne
# l'expression latex : 2L_{1}
#
# pxsl_ax(1,Symbol('L_{'+str(1)+'}')) retourne
# l'expression latex : L_{1}
#
# pxsl_ax(0,Symbol('L_{'+str(1)+'}')) retourne ""

def pxsl_double_matrix(A,B,listeMat=[],opt='sep'):
  """
    Fonction permettant d'afficher un système linéaire Ax=B

    Version
    -------
    13/02/25

    Vérification
    ------------
    Auteur : Delphine
    Vérificateurs :

    Paramètres
    ----------
    A : Matrix
    B : Matrix
    listeMat : liste
               permet d'envisager l'ajout de matrices supplémentaires
    opt : str ('sep' par défaut)
          permet de préciser la présentation des matrices
          'sep' : les deux matrices sont présentées côte à côte entourées de parenthèses
          'ext' : les deux matrices sont présentées en matrice étendue séparée par

    Retour
    ------
    str
        retourne l'expression en latex

    Fonction utilisée par
    ---------------------
    pxsl_resol_system

    :pxs_trigger: afficher deux matrices côte à côte, matrice étendue A|B, matrice augmentée pour inversion ou système linéaire
    :pxs_returns: |
        Objet myst affichant deux matrices en environnement array :
        - opt="sep" : (A) (B) côte à côte, chacune entre parenthèses
        - opt="ext" : matrice augmentée (A|B) avec séparation pointillée
          (utilisée pour les étapes de Gauss).
    :pxs_example: |
        A = Matrix([[1, 2], [3, 4]])
        B = Matrix([[1], [0]])
        # Matrices séparées : $\\py{pxsl_double_matrix(A, B)}$
        # Matrice augmentée : $\\py{pxsl_double_matrix(A, B, opt="ext")}$
    :pxs_antipattern: Concaténer deux appels pxsl_matrix sans environnement array — l'alignement vertical et la matrice étendue (A|B) ne marcheront pas.
  """
  if opt=="sep":
    expr=myst(r"""\begin{array}{cc}""")
    expr+=pxsl_matrix(A)+pxsl_matrix(B)+myst(r"""\end{array}""")
    return expr
  else:
    expr=myst(r"""\begin{array}{c:c}""")
    expr+=pxsl_matrix(A,'(','.')+myst(r"""&""",globals(),locals())+pxsl_matrix(B,".",')')+myst(r"""\end{array}""")
    return expr

################ EXEMPLES ##################
# pxsl_double_matrix(Matrix([[1,2,3],[2,-3,4]]),Matrix([[1,2,3],[2,-3,4]])) retourne
# l'expression latex : \begin{array}{ccc}\left(\begin{array}{rrr}1&2&3\2&-3&4\\end{array}\right)&&\left(\begin{array}{rrr}1&2&3\2&-3&4\\end{array}\right)\end{array}
# c'est-à-dire deux matrices entourées de parenthèses et placées l'une à côté de l'autre
# pxsl_double_matrix(Matrix([[1,2,3],[2,-3,4]]),Matrix([[1,2,3],[2,-3,4]]),opt="sep") retourne la même chose
# ATTENTION : ne pas oublier opt= car il y a un autre paramêtre au milieu (la liste)
#
# pxsl_double_matrix(Matrix([[1,2,3],[2,-3,4]]),Matrix([[1,2,3],[2,-3,4]]),opt="ext") retourne
# l'expression latex : \begin{array}{c:c}\left(\begin{array}{rrr}1&2&3\2&-3&4\\end{array}\right.&\left.\begin{array}{rrr}1&2&3\2&-3&4\\end{array}\right)\end{array}
# c'est-à-dire deux matrices réécrite en matrice étendue séparées par des pointillés
#
# EXTENSION A VENIR : écrire une opération entre les deux matrices, possibilités d'écrire plus de 2 matrices

def pxsl_system_lin(A, B, x = 'x', frac = True):
    """
    Construct a LaTeX representation of a linear system.

    The function formats a linear system of equations defined by a coefficient
    matrix `A` and a right-hand side vector `B` into a LaTeX `array` environment.
    Each equation is written as a linear combination of symbolic variables
    followed by its corresponding constant term.

    Parameters
    ----------
    A : Matrix
        Coefficient matrix of the linear system.
    B : Matrix
        Right-hand side vector of the system.
    x : str, optional
        Base name of the unknown variables (default is `"x"`), producing
        variables of the form `x_1, x_2, ..., x_n`.
    frac : bool, optional
        If True, coefficients are displayed as fractions when appropriate.
        If False, coefficients are displayed in a simplified inline form.

    Returns
    -------
    Any
        A symbolic object representing the LaTeX code of the linear system
        formatted as an `array`.

    Examples
    --------
    >>> pxsl_system_lin(A, B)
    '\\\\left\\{ \\\\begin{array}{rcl} ... \\\\end{array}\\\\right.'

    :pxs_trigger: afficher système linéaire accolade, a1x1 + a2x2 = b, forme équationnelle de AX=B, variables x_1 x_2 x_3 personnalisables
    :pxs_returns: |
        Objet myst représentant le système linéaire AX=B avec accolade gauche,
        en environnement array{rcl}, une équation par ligne de la forme
        "a1 x_1 + a2 x_2 = b". Gère les coefficients nuls (terme omis),
        ±1 (signe simple), et l'affichage en fraction ou en ligne.
    :pxs_example: |
        A = Matrix([[2, 3], [1, 4]])
        B = Matrix([1, 1])
        # Dans MyST : $\\py{pxsl_system_lin(A, B)}$
        # → { 2x_1 + 3x_2 = 1 ; x_1 + 4x_2 = 1 }
    :pxs_antipattern: Composer manuellement des f-strings "2x_1+3x_2=1" sans gérer les coefficients nuls, les ±1 ni les variables personnalisées.
    """
    [n,p]=A.shape

  # Permet de créer le vecteur des x_i en fonction de la dimension de A
    vect_x=Matrix([Symbol(x+'_1')])
    for i in range(p-1):
        vect_x=vect_x.row_join(Matrix([Symbol(x+'_'+str(i+2))]))
    expr=myst(r"""\left\lbrace \begin{array}{rcl} """)
    for i in range(n):
        if A[i, :].is_zero_matrix:
            expr += "0"
  # Gère l'affichage du premier terme non nul sans le '+' devant
        if A[i, 0] != 0:
            expr+=pxsl_ax(A[i,0],vect_x[0], frac = frac)
            sign="+"
        else:
            sign=""
        for j in range(1,p):
            if A[i,j]!=0:
                expr+=pxsl_ax(A[i,j],vect_x[j],sign, frac = frac)
                sign="+"

        rhs = myst(r"""\py{B[i].p}/\py{B[i].q}""", globals(), locals()) if (isinstance(B[i], Rational) and B[i].q != 1 and not frac) else latex(B[i])

        expr+=myst(r""" &=&\py{rhs}""",globals(),locals())+myst(r"""\\[0.3em]""")
    expr+=myst(r"""\end{array}\right.""")
    return expr

################ EXEMPLES ##################
# pxsl_system_lin(Matrix([[2,3],[1,4]]),Matrix([1,1])) renvoie
# l'expression latex \left{ \begin{array}{rcr} 2x_1+ 3x_2&=&1\\ x_1+ 4x_2&=&1\\end{array}\right.
#
# pxsl_system_lin(Matrix([[2,3,0],[1,4,-1],[-2,3,5]]),Matrix([1,1,0])) renvoie
# l'expression latex \left{ \begin{array}{rcr} 2x_1+ 3x_2&=&1\\ x_1+ 4x_2-x_3&=&1\\-2x_1+ 3x_2+ 5x_3&=&0\\end{array}\right.



def pxsl_lines_op(n, listOp, opt="sys", frac = True):
    """
    Construct a LaTeX array describing elementary row (line) operations.

    The function generates a symbolic LaTeX representation of a sequence of
    elementary row operations applied to a system or a matrix. Each operation
    is displayed line by line using an `array` environment, with arrows and
    linear combinations formatted according to the current language settings
    (French or English).

    Parameters
    ----------
    n : int
        Number of rows of the system or matrix.
    listOp : list
        List of elementary row operations. Each element of the list is expected
        to be a tuple of the form `(a, i, b, j)` representing an operation applied
        to row `i` using row `j`:
        - if `a == 0`, rows `i` and `j` are swapped;
        - otherwise, the operation corresponds to
          `row_i ← a * row_i + b * row_j`.
        Row indices are assumed to be 1-based.
    opt : str, optional
        Output option (currently kept for interface consistency; default is
        `"sys"`).
    frac : bool, optional
        If True, coefficients are displayed as fractions when appropriate.
        If False, coefficients are displayed in a simplified inline form.

    Returns
    -------
    Any
        A symbolic object representing the LaTeX code of an `array` environment
        describing the row operations.

    Examples
    --------
    >>> pxsl_lines_op(
    ...     n=3,
    ...     listOp=[(1, 1, -2, 2), (0, 2, 1, 3)]
    ... )
    '\\\\begin{array}{ccc} ... \\\\end{array}'

    :pxs_trigger: afficher opérations élémentaires sur les lignes, L1 ← 2L1 + 3L2, permutation L_i ↔ L_j, étapes pivot de Gauss, pédagogique
    :pxs_returns: |
        Objet myst affichant les opérations élémentaires en LaTeX, une par
        ligne en environnement array{ccc} :
        - "L_i ← a·L_i + b·L_j" pour les combinaisons linéaires
        - "L_i ↔ b·L_j" pour les permutations (a=0)
        Utilise L_i (français) ou R_i (anglais) selon pxs_lang.
    :pxs_example: |
        # Affiche L_1 ← L_1 - 2·L_2 puis L_2 ↔ L_3
        ops = [(1, 1, -2, 2), (0, 2, 1, 3)]
        # Dans MyST : $\\py{pxsl_lines_op(3, ops)}$
    :pxs_antipattern: Écrire f"L_{i} \\\\leftarrow {a}L_{i} + {b}L_{j}" sans gérer a=0 (swap), a=±1, b=±1, ni la langue (L/R).
    """

    espace = ""
    expr = myst(r""" \begin{array}{ccc}""")
    pxs_lang = get_pxs_lang()
    for j in range(n):
        for i in range(len(listOp)):
            if j==listOp[i][1]-1:
                a,b=listOp[i][0],listOp[i][2]
                ind1,ind2=listOp[i][1],listOp[i][3]
                var1 = Symbol('L_{'+str(ind1)+'}') if pxs_lang == "fr" else Symbol('R_{'+str(ind1)+'}')
                var2 = Symbol('L_{'+str(ind2)+'}') if pxs_lang == "fr" else Symbol('R_{'+str(ind2)+'}')
                if a==0:
                    expr+=myst(r""" \fr{L}\en{R}_{\py{ind1}}& \leftrightarrow &""",globals(),locals())+pxsl_ax(a,var1,"",frac = frac)+pxsl_ax(b,var2,"")+myst(r"""\py{espace}""",globals(),locals())
                else:
                    expr+=myst(r""" \fr{L}\en{R}_{\py{ind1}}& \leftarrow &""",globals(),locals())+pxsl_ax(a,var1,"",frac = frac)+pxsl_ax(b,var2,"+",frac = frac)+myst(r"""\py{espace}""",globals(),locals())
            if i==len(listOp)-1:
                expr+=myst(r""" \\[0.3em]""")
    expr+=myst(r"""\end{array}""")
    return expr

################ EXEMPLES ##################
# pxsl_lines_op(2,[2,1,3,2]) retourne
# l'expression latex : \begin{array}{c}L_{1} \leftarrow 2L_{1}+ 3L_{2}\\\end{array}\
#
# pxsl_lines_op(2,[0,1,3,2]) retourne
# l'expression latex : \begin{array}{c}L_{1} \leftarrow 3L_{2}\\\end{array}\
#
# pxsl_lines_op(2,[0,1,-1,2]) retourne
# l'expression latex : \begin{array}{c}L_{1} \leftarrow -3L_{2}\\\end{array}\
#

def pxsl_resol_system(listA,listB=[],listOp=[],x='x',method="sys",view="sep", detail = "on"):
  """
    Fonction qui permet d'écrire chaque étape de la résolution d'un problème impliquant des manipulations de lignes

    Version
    -------
    23/09/25

    Vérification
    ------------
    Auteur : Ronan - Delphine
    Vérificateurs :

    Paramètres
    ----------
    listA : list
            contient la liste des matrices A successives utilisées lors de la résolution
    listB : list
            contient la liste des vecteurs (système) ou matrice (inversion) B successives utilisées lors de la résolution
    listOp : liste de liste
             chaque liste de la liste contient 4 éléments [a, ind1,b,ind2] permettant de réaliser le calcul sur la ligne d'indice ind1 a*L_ind1+b*L_ind2
    x : s.Symbol ('x' par défaut)
        utilisé comme variable dans le cas de la résolution d'un système
    method : str ('sys' par défaut)
             "sys" : résolution d'un système
             "mat" : inversion d'une matrice
             "ech" : échelonnage d'une matrice
    view : str ("sep" par défaut)
           "sep" : les deux matrices sont représentées côte à côte
           "ext" : représente la matrice étendue A|B

    Retour
    ------
    str
        retourne l'expression en latex

    Fonction utilisée par
    ---------------------
    Aucune fonction pyxiscience

    :pxs_trigger: afficher étapes résolution système linéaire, pivot de Gauss pas à pas, inversion matrice avec opérations détaillées, échelonnage matrice historique complet
    :pxs_returns: |
        Objet myst affichant toute la résolution pas à pas en environnement
        array : chaque étape comprend les opérations sur les lignes
        (pxsl_lines_op) puis la matrice/système résultant, séparés par "\\\\".
        Modes method : "sys" (système), "mat" (inversion), "ech" (échelonnage).
    :pxs_example: |
        listA = [A0, A1, A2, A_final]
        listB = [B0, B1, B2, B_final]
        listOp = [[0,0,0,0], [1,2,-2,1], [1,3,1,2], [Rational(1,2),1,0,0]]
        # Dans MyST : $\\py{pxsl_resol_system(listA, listB, listOp)}$
    :pxs_antipattern: Construire la résolution à la main avec une boucle for et des concat LaTeX — perd l'alignement et la mise en page pédagogique automatiques.
  """
  listA, listB, listOp = pxs_regroupe_ligne(listA, listB, listOp)
  expr=""
  for i in range(len(listA)):
    if i==0:
      if method=="sys":
        expr=myst(r"""\begin{array}{cl} """)+myst(r"""&""")+ pxsl_system_lin(listA[i],listB[i],x)+myst(r"""\\ \\""")
      elif method=="ech":
        expr=myst(r"""\begin{array}{cc} """)+myst(r"""&""")+ pxsl_matrix(listA[i])+myst(r"""\\ \\""")
      else:
        expr=myst(r"""\begin{array}{cc} """)+myst(r"""&""")+ pxsl_double_matrix(listA[i],listB[i],opt=view)+myst(r""" \\ \\""")
    if i!=0:
      if detail == "on":
        if method=="sys":
          expr+=pxsl_lines_op(listA[0].shape[0],listOp[i])+myst(r""" & """)+pxsl_system_lin(listA[i],listB[i],x)+myst(r"""\\ \\""")
        elif method=="ech":
          expr+=pxsl_lines_op(listA[0].shape[0],listOp[i],opt="ech")+myst(r""" & """)+pxsl_matrix(listA[i])+myst(r"""\\ \\""")
        else:
          expr+=pxsl_lines_op(listA[0].shape[0],listOp[i])+myst(r""" & """)+pxsl_double_matrix(listA[i],listB[i],opt=view)+myst(r"""\\ \\""")
      else:
        if method=="sys":
          expr+=myst(r""" & """)+pxsl_system_lin(listA[i],listB[i],x)+myst(r"""\\ \\""")
        elif method=="ech":
          expr+=myst(r""" & """)+pxsl_matrix(listA[i])+myst(r"""\\ \\""")
        else:
          expr+=myst(r""" & """)+pxsl_double_matrix(listA[i],listB[i],opt=view)+myst(r"""\\ \\""")
  expr+=myst(r"""\end{array}""")
  return expr



################ EXEMPLES ##################
# Soit les variables de départ :
# listA=[Matrix([ [-4, 2], [ 1, -1]]), Matrix([ [-2, 1], [ 1, -1]]), Matrix([ [-2, 1], [ 0, -1]]), Matrix([ [-2, 0], [ 0, -1]]), Matrix([ [-1, 0], [ 0, -1]]), Matrix([ [1, 0], [0, -1]]), Matrix([ [1, 0], [0, 1]])]
# listB=[Matrix([ [-6], [ 0]]), Matrix([ [-3], [ 0]]), Matrix([ [-3], [-3]]), Matrix([ [-6], [-3]]), Matrix([ [-3], [-3]]), Matrix([ [ 3], [-3]]), Matrix([ [3], [3]])]
# listOp=[[0, 0, 0, 0], [Rational(1,2), 1, 0, 0], [2, 2, 1, 1], [1, 1, 1, 2], [Rational(1,2), 1, 0, 0], [-1, 1, 0, 0], [-1, 2, 0, 0]]
#
# pxsl_resol_system(listA,listB,listOp,method='sys') retourne l'expression latex pour représenter
# la résolution du système.
#

def pxs_reduce_pgcd(A, B, listA, listB, listOp):
    """
    Fonction permettant de diviser lignes des matrices A et B lorsque leur pgcd est différent de 1

    Version
    -------
    23/09/25 (modifié 14/10/25)

    Vérification
    ------------
    Auteur : Delphine
    Vérificateurs :
    Paramètres
    ----------
    A : Matrix
    B : Matrix
    listA : list
            liste de matrices, permet de retrouver les différentes transformations de la matrice A
    listB : list
            liste de matrices, permet de retrouver les différentes transformations de la matrice B
    listOp : list
             Chaque élément de la liste est une liste de 4 éléments :
             [facteur multiplicatif de la ligne i, indice de la ligne i, facteur multiplicatif de la ligne j, indice de la ligne j]
    Retour
    ------
    liste, liste, liste
        retourne les listes actualisées de l'opération de permutation
    Fonction utilisée par
    ---------------------
    pxs_steps_invert_matrix

    :pxs_trigger: simplifier ligne par PGCD, diviser ligne matrice pour réduire coefficients, intermédiaire Gauss simplification, interne pivot
    :pxs_returns: |
        Tuple (listA, listB, listOp) mis à jour : pour chaque ligne où le PGCD
        des coefficients (numérateurs A[i,:] et B[i,:]) est ≠ 1, une nouvelle
        étape est ajoutée aux trois listes (matrice divisée + opération [1/pgcd, i+1, 0, 0]).
        Modifie A et B en place. Appelée par pxs_steps_invert_matrix.
    :pxs_example: |
        # Appelée typiquement en interne après chaque élimination dans pxs_steps_invert_matrix
        # listA, listB, listOp = pxs_reduce_pgcd(A, B, listA, listB, listOp)
    :pxs_antipattern: Ne pas simplifier après chaque étape — produit des coefficients qui explosent (ex. 1024/512) au lieu de 2.
    """

    [n, p] = A.shape
    for i in range(n):
        # Extraction des numérateurs pour la ligne i de A
        A_row_nums = [elem.numerator if isinstance(elem, Rational) else elem for elem in A[i, :]]

        # Extraction des numérateurs pour la ligne i de B
        B_row_nums = [elem.numerator if isinstance(elem, Rational) else elem for elem in B[i, :]]

        # Calcul du PGCD pour les numérateurs
        if len(A_row_nums) > 0 and len(B_row_nums) > 0:
            # Utiliser sympy_gcd pour gérer les objets sympy
            pg_A = A_row_nums[0]
            for val in A_row_nums[1:]:
                pg_A = gcd(pg_A, val)

            pg_B = B_row_nums[0]
            for val in B_row_nums[1:]:
                pg_B = gcd(pg_B, val)

            pg = gcd(pg_A, pg_B)

            # Vérifier si pg est différent de 1
            if pg != 1 and pg != 0:
                # Division de la ligne par le PGCD
                A[i, :] = A[i, :] / pg
                B[i, :] = B[i, :] / pg

                # Mise à jour des listes
                listA.append(A.copy())
                listB.append(B.copy())

                for j in range(n):
                    if j == i:
                        # L'opération est L_{i+1} -> 1/pg * L_{i+1} d'où la liste [1/pg, i+1, 0, 0]
                        try:
                            listOp.append([Rational(1, pg), i+1, 0, 0])
                        except:
                            listOp.append([1/ pg, i+1, 0, 0])

    return listA, listB, listOp

################ EXEMPLES ##################
# Exemple pour une matrice avec PGCD = 2
# pxs_reduce_pgcd(Matrix([[2,4,6],[1,2,3]]),Matrix([2,3,4]),[Matrix([[2,4,6],[1,2,3]])],[Matrix([2,3,4])],[[0,0,0,0]]) retourne
# listA = [Matrix([ [2, 4, 6], [1, 2, 3]]), Matrix([ [1, 2, 3], [1, 2, 3]])]
# listB = [Matrix([ [2], [3], [4]]), Matrix([ [1], [3], [4]])]
# listOp = [[0, 0, 0, 0], [1/2, 1, 0, 0]]
#

def pxs_steps_invert_matrix(A,B,x='x',method="sys",view="sep", detail = "on"):
  """
    Fonction permettant de stocker toutes les étapes de la résolution d'un système ou l'inversion d'une matrice

    Version
    -------
    23/09/25

    Vérification
    ------------
    Auteur : Ronan - Delphine
    Vérificateurs :

    Paramètres
    ----------
    A : Matrix
    B : Matrix
    x : Symbol ('x' par défaut)
        liste de matrices, permet de retrouver les différentes transformations de la matrice A
    method : str
             "sys" : pour afficher la résolution d'un système
    listOp : list
             Chaque élément de la liste est une liste de 4 éléments :
             [facteur multiplicatif de la ligne i, indice de la ligne i, facteur multiplicatif de la ligne j, indice de la ligne j]

    Retour
    ------
    liste, liste, liste
        retourne les listes actualisées de l'opération de permutation

    Fonction utilisée par
    ---------------------
    Aucune fonction pyxiscience

    :pxs_trigger: résoudre système linéaire pas à pas, inverser matrice par Gauss-Jordan, échelonner matrice avec historique, AX=B résolution détaillée
    :pxs_returns: |
        Objet myst contenant la résolution complète pas à pas de AX=B par
        pivot de Gauss-Jordan, en mettant A et B sous forme échelonnée
        réduite. Modifie A et B en place. Appelle pxsl_print_operations
        pour le rendu LaTeX final.
    :pxs_example: |
        A = Matrix([[2,3,0],[1,4,-1],[-2,3,5]])
        B = Matrix([1, 1, 0])
        # Résolution système : $\\py{pxs_steps_invert_matrix(A, B)}$
        # Inversion : pxs_steps_invert_matrix(A, eye(3), method="mat")
    :pxs_antipattern: Utiliser A.inv() ou A.solve(B) qui donnent le résultat sans les étapes intermédiaires pédagogiques.
  """
  [n,p]=A.shape
  nmin=min(n,p)
  listA,listB=[A.copy()],[B.copy()]
  listOp=[[0,0,0,0]]
  # On vérifie le pgcd de chaque ligne pour simplifier
  listA,listB,listOp=pxs_reduce_pgcd(A,B,listA,listB,listOp)
  for k in range(nmin):
   # On cherche la ligne pivot
    r=-1
    for i in range(k,n):
      if r<0 and A[i,k]!=0:
        r=i
    if r>k:
   # On met la ligne pivot en haut si elle ne l'est pas
      A.row_swap(k, r)
      B.row_swap(k,r)
      listA.append(A.copy())
      listB.append(B.copy())
      for j in range(n):
        if j==r:
          listOp.append([0,r+1,1,1+k])
    if r>=k:
   # On élimine les lignes differentes de k
      for j in range(n):
        if A[j,k]!=0 and j!=k:
          pg=gcd(A[k,k],A[j,k])
          cpAjk=A[j,k]
          cpAkk=A[k,k]
          try:
              A[j,:]=abs(cpAkk)*A[j,:]/pg- abs(cpAjk)*A[k,:]/pg*np.sign( cpAjk* cpAkk)
          except:
              A[j,:]=cpAkk*A[j,:]/pg- cpAjk*A[k,:]/pg
          try:
              B[j,:]=abs(cpAkk)*B[j,:]/pg- abs(cpAjk)*B[k,:]/pg*np.sign( cpAjk* cpAkk)
          except:
              B[j,:]=cpAkk*B[j,:]/pg- cpAjk*B[k,:]/pg
          listA.append(A.copy())
          listB.append(B.copy())
          for l in range(n):
            if l==j:
              try:
                listOp.append([abs(cpAkk)/pg,j+1,-abs(cpAjk)/pg*np.sign( cpAjk* cpAkk),k+1])
              except:
                listOp.append([cpAkk/pg,j+1,-cpAjk/pg,k+1])
   # On vérifie le pgcd de chaque ligne pour simplifier
          listA,listB,listOp=pxs_reduce_pgcd(A,B,listA,listB,listOp)
   # On exprime les solutions sous la forme finale
  for i in range(nmin):
    if A[i,i]!=0 and A[i,i]!=1:
      for j in range(B.shape[1]):
        try:
          B[i,j]=Rational(B[i,j],A[i,i])
        except:
          B[i,j]=B[i,j]/A[i,i]
      cpAi=A[i,i]
      A[i,:]=A[i,:]/cpAi
      listA.append(A.copy())
      listB.append(B.copy())
   # Stockage de l'opération
      for j in range(nmin):
        if j==i and cpAi!=0:
          try:
            listOp.append([Rational(1,cpAi),i+1,0,0])
          except:
            listOp.append([1/cpAi,i+1,0,0])
        elif j==i and cpAi == -1:
          listOp.append([-1,i+1,0,0])
  expr = pxsl_print_operations([listA, listB], listOp, method, x, view, detail)
  return expr

################ EXEMPLES ##################
# pxs_steps_invert_matrix(Matrix([[2,3,0],[1,4,-1],[-2,3,5]]),Matrix([1,1,0])) renvoie
# l'expression latex qui permet de décrire toute la résolution du système.
#
# pxs_steps_invert_matrix(Matrix([[2,3,0],[1,4,-1],[-2,3,5]]),Matrix([[1,0,0],[0,1,0],[0,0,1]]),method="mat") renvoie
# l'expression latex qui permet de décrire l'inversion de la matrice avec les matrices mises côte à côte.
#
# pxs_steps_invert_matrix(Matrix([[2,3,0],[1,4,-1],[-2,3,5]]),Matrix([[1,0,0],[0,1,0],[0,0,1]]),method="mat",view="ext") renvoie
# l'expression latex qui permet de décrire l'inversion de la matrice avec la matrice étendue.

def pxs_LU_decomposition(A, view = "sep", detail = "on", name_matrix = " ", PLU = False):
    """
    Details the steps of LU factorization for a square matrix A.

    Version
    -------
    26/12/25

    Authors
    ------------
    Author: Raphaël
    Checked by:

    Arguments
    ----------
    A: Matrix, the matrix to factorize
    method: str, display option
    view: str, display option
    detail: str, "on" to get additional details
    name_matrix: str, name the matrix is referred as

    Returns
    ------
    text (str), L (Matrix), U (Matrix) (if PLU = False)
    text (str), P (Matrix), L (Matrix), U (Matrix) (if PLU = True)
        text: steps of the computation
        (P,) L, U: Matrixes such that (P)A = LU if they exist. None, None otherwise

    Function used by
    ---------------------
    No pyxiscience function

    Examples
    --------
    >>> A = Matrix([[1, 2, 1], [3, 10, 3], [-2, -8, 5]]) # LU factorization exists
    >>> resol, L, U = pxs_LU_decomposition(A.copy())

    >>> B = Matrix([[1, 2, 1], [3, 6, -1], [1, 1, 1]]) # LU factorization does not exist
    >>> resol, P, L, U = pxs_LU_decomposition(A4.copy(), name_matrix = "B", PLU = True) # L, U = None, None

    :pxs_trigger: décomposition LU matrice carrée, factorisation PLU avec permutation, triangulaire inférieure supérieure, pivots pédagogique
    :pxs_returns: |
        Si PLU=False : tuple (text, L, U) où text est l'objet myst des étapes
        LaTeX, L matrice triangulaire inf. à diagonale unité, U triangulaire
        sup. telle que A=LU (ou L,U=None si impossible sans permutation).
        Si PLU=True : tuple (text, P, L, U) avec P matrice de permutation
        telle que PA=LU (toujours possible pour A carrée).
    :pxs_example: |
        A = Matrix([[1, 2, 1], [3, 10, 3], [-2, -8, 5]])
        resol, L, U = pxs_LU_decomposition(A.copy())
        # Dans MyST : \\py{resol} puis $L = \\py{pxsl_matrix(L)}$, $U = \\py{pxsl_matrix(U)}$
    :pxs_antipattern: Utiliser A.LUdecomposition() qui donne uniquement le résultat final sans les étapes détaillées de réduction.
    """

    pxs_lang = get_pxs_lang()

    [n,p] = A.shape
    # Check if square
    if n != p:
        err = "La matrice fournie doit être carrée" if pxs_lang == "fr" else "Input matrix must be square"
        raise ValueError(err)

    B = Matrix(np.eye(n).astype(np.int64))
    listA, listB=[A.copy()], [B.copy()]
    if PLU:
        P = Matrix(np.eye(n).astype(np.int64))
        listP = [P.copy()]
    listOp = [[0,0,0,0]]
    k = 0
    ok = True
    while k < n - 1 and ok: # for each column except the last one and while it is possible
        if A[k, k] != 0:
            # Handle subdiagonal coefficients on the (k+1)-th column
            for j in range(k + 1, n):
                if A[j,k]!=0:
                    coeff = A[j, k] / A[k, k]
                    A[j, :] -= coeff * A[k, :]
                    B[j, k] = coeff
                    listA.append(A.copy())
                    listB.append(B.copy())
                    if PLU:
                        listP.append(P.copy())
                    listOp.append([1, j + 1, -coeff, k + 1])
            k += 1
        # below : cases where the k-th pivot is 0
        elif np.any(A[k+1:, k]): # else A[k:, k] == 0, all coeff under the pivot are 0, nothing to do
            if not PLU:
                # looking above for another line to use as a "pivot"
                r = k - 1
                while r >= 0 and not (A[r, k] != 0 and not np.any(A[r, :k])):
                    r -= 1
                if r == -1: # nothing found
                    ok = False
                else: # using r-th row to eliminate the subdiagonal coefficients on the (k+1)-th column
                    for j in range(k + 1, n):
                        if A[j,k]!=0:
                            coeff = A[j, k] / A[r, k]
                            A[j, :] -= coeff * A[r, :]
                            B[j, r] = coeff
                            listA.append(A.copy())
                            listB.append(B.copy())
                            listOp.append([1, j + 1, -coeff, r + 1])
                    k += 1
            else: # PLU case, looking for a non-zero coeff below in order to swap lines
                r = np.where(np.ravel(A[k + 1:, k]) != 0)[0][0] + k + 1 # row of first non-zero coeff. on column k
                A.row_swap(k, r)
                B[k, :k], B[r, :k] = B[r, :k], B[k, :k]
                P.row_swap(k, r)
                listA.append(A.copy())
                listB.append(B.copy())
                listP.append(P.copy())
                listOp.append([0, k + 1, 1, r + 1])
        else:
            k += 1

    list_mat = [listA, listB]
    if PLU: list_mat.append(listP)

    text = myst(r"""\begin{equation*}""", locals(), globals())
    text += pxsl_print_operations(list_mat, listOp, method = "mat", view = view, detail = detail)
    text += myst(r"""\end{equation*}""", locals(), globals())

    if PLU:
        return text, listP[-1], listB[-1], listA[-1] # text, P, L, U
    elif ok: # no permutation, and LU factorization exists
        return text, listB[-1], listA[-1]
    else: # no permutation, and LU factorization does not exist
        if pxs_lang == "fr":
            negative_conclusion = myst(r"""
On ne peut pas poursuivre la réduction sans permutation de lignes, la matrice $\py{name_matrix}$ ne possède donc pas de décomposition $LU$.""", locals(), globals())
        if pxs_lang == "en":
            negative_conclusion =  myst(r"""
A line permutation would be required at this stage, hence the matrix $\py{name_matrix}$ does not admit an $LU$ factorization.""", locals(), globals())
        text += negative_conclusion
        return text, None, None


def pxsl_print_operations(list_mat, listOp=[], method = "sys", x = "x", view="sep", detail = "on", frac = True):
    """
      Displays each step of the resolution for a problem involving line operations.
      This function is meant to replace pxsl_resol_system

      Version
      -------
      06/01/26

      Authors
      ------------
      Auteur : Ronan - Delphine - Raphaël
      Vérificateurs :

      Arguments
      ----------
      list_mat : list of lists
              each element is a list of successive matrices appearing in the resolution
      listOp : liste of lists
              each sublist contains 4 elements [a, ind1, b, ind2] describing the following operation:
               L(ind1) <- a * L_ind1 + b * L_ind2
      x : s.Symbol ('x' par défaut)
          determines the name of the variables in the system
      method : str ('sys' by default)
              "sys" : system form
              "mat" : matrix form
      view : str ("sep" by default)
            "sep" : matrices are displayed side-by-side
            "ext" : extended matrix A1|A2|...|An
      frac : bool, optional
        If True, coefficients are displayed as fractions when appropriate.
        If False, coefficients are displayed in a simplified inline form.

      Returns
      ------
      str
          Latex expression

      Function used by
      ---------------------
      pxs_steps_invert_matrix, pxs_LU_decomposition, pxs_compute_ech, pxs_compute_ech_reduite

      :pxs_trigger: afficher étapes résolution multi-matrices, remplace pxsl_resol_system, historique Gauss avec plusieurs matrices simultanées, LU échelonnage déterminant
      :pxs_returns: |
          Objet myst affichant toutes les étapes de résolution en LaTeX, avec
          une ligne par étape : opérations sur lignes + matrice(s)
          correspondante(s). Généralise pxsl_resol_system à un nombre
          arbitraire de matrices suivies en parallèle (ex. [A, B, P] pour
          LU+permutation). Modes method : "sys" ou "mat".
      :pxs_example: |
          # Appelée en interne par pxs_steps_invert_matrix, pxs_LU_decomposition,
          # pxs_compute_ech, pxs_compute_ech_reduite :
          # expr = pxsl_print_operations([listA, listB], listOp, method="mat")
      :pxs_antipattern: Utiliser l'ancien pxsl_resol_system qui ne gère que [listA, listB] au lieu d'un nombre arbitraire de listes de matrices.
    """

    def __pxsl_multiple_matrix(list_mat, view, display = frac):
        n = len(list_mat)
        cols = "c" * n if view == "sep" else ":".join("c" * n)
        seps = [["(", ")"] if view == "sep" else [".", "."] for _ in range(n)]
        seps[0][0], seps[-1][1] = "(", ")"
        expr = myst(r"""\begin{array}{\py{cols}}""", locals(), globals())
        expr += "&".join([pxsl_matrix(mat, sep[0], sep[1], display = display) for mat, sep in zip(list_mat, seps)])
        expr += myst(r"""\end{array}""", locals(), globals())
        return expr

    n = list_mat[0][0].shape[0]
    list_mat, listOp = pxs_regroupe_ligne(list_mat, listOp)

    if method == "sys":
        try:
            listA, listB = list_mat
        except:
            raise ValueError("list_mat must be of length 2 exactly when method is 'sys'")

    # First line
    if method=="sys":
        expr = myst(r"""\begin{array}{cl} """)+myst(r"""&""")+ pxsl_system_lin(listA[0],listB[0],x, frac = frac)+myst(r"""\\ \\""")
    else:
        expr = myst(r"""\begin{array}{cc} """)+myst(r"""&""")+ __pxsl_multiple_matrix([listX[0] for listX in list_mat], view = view) + myst(r""" \\ \\""")

    # other lines
    for i in range(1, len(list_mat[0])):
        printed_ops = pxsl_lines_op(n, listOp[i], frac = frac) if detail == "on" else " "
        if method=="sys":
            expr += myst(r"""\py{printed_ops} & """, locals(), globals()) + pxsl_system_lin(listA[i],listB[i],x, frac = frac)+myst(r"""\\ \\""")
        else:
            expr += myst(r"""\py{printed_ops} & """, locals(), globals()) + __pxsl_multiple_matrix([listX[i] for listX in list_mat], view = view) + myst(r"""\\ \\""")

    expr+=myst(r"""\end{array}""")
    return expr

##

def pxs_commute_matrix(n,opt=""):
  """
    Fonction permettant de créer les matrices A, B et C de dimension n avec A et B commutantes et A et C non commutantes

    Version
    -------
    13/02/25

    Vérification
    ------------
    Auteur : Ronan - Delphine
    Vérificateurs :

    Paramètres
    ----------
      n : int
          Dimension de la matrice A
      opt: str
           "commut" : Envoie deux matrices qui commutent
           "noncommut" : Envoie deux matrices qui ne commutent pas
           autre : renvoie les trois matrices

    Retour
    ------
      A,B
        retourne les deux matrices du système AX=B

    Fonction utilisée par
    ---------------------
    aucune fonction pyxiscience

    :pxs_trigger: générer matrices commutantes ou non, exercice AB=BA vs AB≠BA, matrices simultanément diagonalisables, P D P^-1, commutateur matriciel
    :pxs_returns: |
        Selon opt :
        - "commute" : tuple (A, B) de Matrix de dimension n×n qui commutent (AB=BA)
        - "noncommute" : tuple (A, C) qui ne commutent pas (AC≠CA)
        - autre : triplet (A, B, C) avec A·B=B·A et A·C≠C·A
        Coefficients entiers bornés en valeur absolue par 10n via construction
        P·D·P^-1 avec D diagonale aléatoire et P aléatoire inversible.
    :pxs_example: |
        A, B, C = pxs_commute_matrix(3)
        # Dans MyST : $A = \\py{pxsl_matrix(A)}$, $B = \\py{pxsl_matrix(B)}$
        # avec AB=BA mais AC≠CA pour un exercice de commutation.
    :pxs_antipattern: Tirer des coefficients aléatoirement et tester AB=BA — probabilité quasi-nulle d'obtenir la commutation sans construction P·D·P^-1.
  """
  Nmax=3
  A=ones(n)*10*n
  C=A.copy()
  while A*C==C*A or sum(1 for element in A if abs(element) >= 10*n)>=1 or sum(1 for element in C if abs(element) >= 10*n)>=1:
    # On construit les matrices diagonales de la décomposition P*A*Pinv
    P=pxs_system_simpl(n,eye(n),"mat")
    Pinv=P.inv()
    DiagA=randmatrixdiagonale(n,-Nmax,Nmax)
    DiagC=DiagA.copy()
    DiagC[0,n-1]=1
    C=P*DiagC*Pinv*P.det()
    C=C/fct.reduce(m.gcd,C[:,:])
    # on s'assure que A ne puisse pas commuter avec n'importe quelle matrice (ce qui arrive si les éléments de la diagonale sont tous égaux)
    # on s'assure également qu'on n'obtient pas la matrice nulle
    while DiagA==zeros(n) or DiagA[0,0]==DiagA[n-1,n-1]:
      DiagA=randmatrixdiagonale(n,-Nmax,Nmax)

    # on génère les matrices A et B commutantes
    A=P*DiagA*Pinv*P.det()
    A=A/fct.reduce(m.gcd,A[:,:])

  B=C.copy()*10*n
  while A*B!=B*A or sum(1 for element in B if abs(element) >= 10*n)>=1:
    DiagB=randmatrixdiagonale(n,-Nmax,Nmax)
    while DiagB==zeros(n):
      DiagB=randmatrixdiagonale(n,-Nmax,Nmax)
    if DiagA[0,0]==DiagB[0,0]:
      DiagB[0,0]=DiagB[0,0]+1
    B=P*DiagB*Pinv*P.det()
    B=B/fct.reduce(m.gcd,B[:,:])

  if opt=="commute":
    return A,B

  if opt=="noncommute":
    return A,C
  else:
    return A,B,C

################ EXEMPLES ##################
# pxs_commute_matrix(2) renvoie A, B et C de dimension 2x2 telles que A et B commutent et
# A et C ne commutent pas.
# Par exemple :
#           3   4          5   8           5  2
#     A =  -2  -3     B = -4  -7      C = -2  1
#
# pxs_commute_matrix(3) renvoie A, B et C de dimension 3x3 telles que A et B commutent et
# A et C ne commutent pas.
# Par exemple :
#          0   1   1         4  -5   -5          0  3   3
#     A =  4   3  -1    B = -8   1    5     C =  4  1  -3
#         -4  -1   3         8  -7  -11         -4  1   5
#
# pxs_commute_matrix(2,"commute") renvoie A, B dimension 2x2 telles que A et B commutent
# Par exemple :
#           3   4          5   8
#     A =  -2  -3     B = -4  -7
#
# pxs_commute_matrix(3,"noncommute") renvoie A et C de dimension 3x3 telles que A et C ne commutent pas.
# Par exemple :
#          0   1   1         0  3   3
#     A =  4   3  -1    C =  4  1  -3
#         -4  -1   3        -4  1   5

def pxsl_pow_matrix(A,k,opt=0,sepG='(',sepD=')'):
  """
  Fonction permettant d'écrire en latex une matrice dont tous les coefficients sont élevés à la même puissance
  Les puissances de 0 et 1 sont simplifiées, les valeurs sont centrées par défaut

  Version
  -------
  13/02/25

  Vérification
  ------------
  Auteur : Ronan - Delphine
  Vérificateurs :

  Paramètres
  ----------
  A : Matrix
  k : float ou Symbol
        valeur de la puissance
  sepG : str
           délimiteur gauche de la matrice
  sepD : str
           délimiteur droit de la matrice

  Retour
  ------
  str
      retourne l'expression en latex

  Fonction utilisée par
  ---------------------
  aucune fonction pyxiscience

  :pxs_trigger: matrice dont chaque coefficient est élevé à la même puissance, a_ij^k terme à terme, puissance symbolique matrice non matricielle
  :pxs_returns: |
      Objet myst affichant la matrice dont chaque coefficient a_ij est
      élevé à la puissance k (terme à terme, PAS la puissance matricielle
      A^k). Les cas a_ij=0,1 et k=1 sont simplifiés selon opt via pxsl_pow.
  :pxs_example: |
      A = Matrix([[2, 0, 1], [4, 8, -4]])
      # Dans MyST : $\\py{pxsl_pow_matrix(A, 2)}$
      # → matrice des 2², 0², 1², 4², 8², (-4)²
  :pxs_antipattern: Utiliser A**k qui calcule la puissance matricielle A·A·…·A au lieu du calcul terme à terme.
  """

  [n,q]=A.shape
  pxs_lang = get_pxs_lang()
  if pxs_lang == "en" and sepG=='(':
    sepG='['
  if pxs_lang == "en" and sepD==')':
    sepD=']'
  expr=myst(r"""\left\py{sepG}\begin{array}{\py{'c'*q}}""",globals(),locals())
  for i in range(n):
    expr=expr+pxsl_pow(A[i,0],k,opt)
    for j in range(q-1):
      expr=expr+myst(r""" &""")+pxsl_pow(A[i,1+j],k,opt)
    expr=expr+myst(r"""\\""")
  expr=expr+myst(r"""\end{array}\right\py{sepD}""",globals(),locals())
  return expr

################ EXEMPLES ##################
# pxsl_pow_matrix(Matrix([[2,0,1],[4,8,-4],[2,3,0]]),2)
# renvoie l'expression latex \left(\begin{array}{ccc}2^{2}&0^2&1^2\4^{2}&8^{2}&\left(-4\right)^{2}\2^{2}&3^{2}&0^2\\end{array}\right)
# c'est-à-dire
#
#           2^2  0^2   1^2
#           4^2  8^2  (-4)^2
#           2^2  3^2   0^2
# pxsl_pow_matrix(Matrix([[2,0,1],[4,8,-4],[2,3,0]]),2,1)
# renvoie l'expression latex \left(\begin{array}{ccc}2^{2}&0&1\4^{2}&8^{2}&\left(-4\right)^{2}\2^{2}&3^{2}&0\\end{array}\right)
# c'est-à-dire
#
#           2^2   0     1
#           4^2  8^2  (-4)^2
#           2^2  3^2    0


def pxs_regroupe_ligne(list_mat, listOp=[]):
    """
    Fonction permettant de regrouper les lignes qui peuvent être écrites en une seule étape

    Version
    -------
    21/03/25 -> 06/01/26 (Raphaël)

    Vérification
    ------------
    Auteur : Delphine
    Vérificateurs :

    Paramètres
    ----------
    listA : list
            liste des étapes pour la matrice/système de départ
    listB : list
            liste des étapes pour la matrice miroir (inversion) ou membre droit (système)
    listOp : liste
             liste des opérations sur lignes

    Retour
    ------
    listA, listB, listOp
        retourne les listes actualisées

    Fonction utilisée par
    ---------------------
    pxsl_resol_system, pxsl_print_operations

    :pxs_trigger: regrouper opérations indépendantes Gauss, compacter étapes résolution, fusionner opérations sur lignes disjointes, interne
    :pxs_returns: |
        Tuple (list_mat_bis, listOp_bis) où les opérations successives portant
        sur des lignes disjointes sont regroupées en une seule étape (liste
        d'opérations). Divise le nombre d'étapes affichées dans la résolution
        finale, rendant le LaTeX plus compact.
    :pxs_example: |
        # Appelée en interne par pxsl_resol_system et pxsl_print_operations :
        # list_mat, listOp = pxs_regroupe_ligne([listA, listB], listOp)
    :pxs_antipattern: Afficher chaque opération sur une ligne séparée, ce qui explose la longueur du LaTeX final pour les grandes matrices.
    """

    if len(listOp) <= 1:
        return list_mat, listOp

    n, nb_etape = len(list_mat[0]), 1

    listOp_bis = [listOp[0]]
    listOp_bis.append([listOp[1]])
    list_mat_bis = [[listX[0]] for listX in list_mat]

    for i in range(1, n-1):
        if listOp[i][0] != 0 and all(sous_liste[1] !=listOp[i+1][1] for sous_liste in listOp_bis[nb_etape]) and all(sous_liste[1] !=listOp[i+1][3] for sous_liste in listOp_bis[nb_etape]):
          listOp_bis[nb_etape].append(listOp[i+1])
        else:
          for j in range(len(list_mat)):
            list_mat_bis[j].append(list_mat[j][i])
          nb_etape += 1
          listOp_bis.append([listOp[i+1]])
        if i == n-2:
          for j in range(len(list_mat)):
            list_mat_bis[j].append(list_mat[j][i+1])

    if listOp_bis:
        return list_mat_bis, listOp_bis
    else:
        return list_mat, listOp


def pxs_compute_ech(A):
  """
    Fonction permettant de stocker toutes les étapes de la construction d'une matrice échelonnée

    Paramètres
    ----------
    A : Matrix

    Retour
    ------
    liste, liste, liste
        retourne les listes actualisées de l'opération de permutation

    Fonction utilisée par
    ---------------------
    Aucune fonction pyxiscience

    :pxs_trigger: échelonner matrice pas à pas, forme échelonnée par Gauss, REF row echelon form avec historique, zéros sous-diagonale
    :pxs_returns: |
        Objet myst affichant toutes les étapes de l'échelonnage de A en forme
        échelonnée (REF, PAS réduite) : recherche pivots, permutations des
        lignes si nécessaire, élimination sous la diagonale. Modifie A
        en place. Appelle pxsl_print_operations pour le rendu LaTeX.
    :pxs_example: |
        A = Matrix([[0, 1, 2], [2, 4, 6], [1, 1, 1]])
        # Dans MyST : \\py{pxs_compute_ech(A)}
        # Rend matrice triangulaire supérieure avec étapes intermédiaires.
    :pxs_antipattern: Utiliser A.echelon_form() qui donne directement la REF sans les étapes d'opérations pédagogiques.
  """
  [n,p]=A.shape
  nmin=min(n,p)
  listA=[A.copy()]
  listOp=[[0,0,0,0]]

  for k in range(nmin):
   # On cherche la ligne pivot
    r=-1
    for i in range(k,n):
      if r<0 and A[i,k]!=0:
        r=i
    if r>k:
   # On met la ligne pivot en haut si elle ne l'est pas
      A.row_swap(k, r)
      listA.append(A.copy())
      for j in range(n):
        if j==r:
          listOp.append([0,r+1,1,1+k])
    if r>=k:
   # On élimine les lignes après k
      for j in range(k,n):
        if A[j,k]!=0 and j!=k:
          pg=m.gcd(A[k,k],A[j,k])
          cpAjk=A[j,k]
          cpAkk=A[k,k]
          A[j,:]=abs(cpAkk)*A[j,:]/pg- abs(cpAjk)*A[k,:]/pg*np.sign( cpAjk* cpAkk)
          listA.append(A.copy())
          for l in range(n):
            if l==j:
              listOp.append([abs(cpAkk)/pg,j+1,-abs(cpAjk)/pg*np.sign( cpAjk* cpAkk),k+1])
  expr = pxsl_print_operations([listA], listOp = listOp, method = "mat")
  return expr




def pxs_compute_ech_reduite(A):
    """
    Fonction transformant une matrice en forme échelonnée réduite en stockant chaque étape.

    Paramètres
    ----------
    A : numpy.ndarray
        Matrice d'entrée

    Retour
    ------
    listA : liste des matrices à chaque étape
    listOp : liste des opérations sous forme [a, i, b, j] avec :
        - a : coefficient multiplicatif pour L_i
        - i : numéro de la ligne affectée (1-based index)
        - b : coefficient multiplicatif pour L_j
        - j : numéro de la ligne utilisée (1-based index)

    :pxs_trigger: forme échelonnée réduite RREF pas à pas, Gauss-Jordan matrice, pivots unités zéros au-dessus et en-dessous, échelon réduit
    :pxs_returns: |
        Objet myst affichant toutes les étapes pour amener A à sa forme
        échelonnée réduite (RREF) : permutations, normalisation des pivots
        à 1, élimination au-dessus ET au-dessous de chaque pivot. Modifie
        A en place. Appelle pxsl_print_operations pour le rendu LaTeX.
    :pxs_example: |
        A = Matrix([[1, 2, 3], [2, 5, 7], [0, 1, 1]])
        # Dans MyST : \\py{pxs_compute_ech_reduite(A)}
        # Rend matrice en RREF avec toutes les étapes.
    :pxs_antipattern: Utiliser A.rref() qui donne directement la RREF sans les étapes pédagogiques détaillées.
    """
    [n, p] = A.shape
    listA = [A.copy()]
    listOp = [[0,0,0,0]]

    for k in range(min(n, p)):
        # Trouver la ligne pivot
        r = -1
        for i in range(k, n):
            if A[i, k] != 0:
                r = i
                break

        if r == -1:
            continue  # Si toute la colonne est nulle, on passe à la suivante

        # Échanger L_k et L_r si nécessaire
        if r != k:
            A.row_swap(k, r)  # Échange des lignes
            listA.append(A.copy())
            listOp.append([0, k + 1, 1, r + 1])  # Format imposé

        # Normaliser le pivot (L_k = L_k / pivot pour avoir 1)
        pivot = A[k, k]
        if pivot != 1:
            A[k, :] /= pivot
            listA.append(A.copy())
            listOp.append([1 / pivot, k + 1, 0, 0])  # Division de la ligne par le pivot

        # Élimination en dessous et au-dessus
        for j in range(n):
            if j != k and A[j, k] != 0:
                facteur = A[j, k]
                A[j, :] -= facteur * A[k, :]
                listA.append(A.copy())
                listOp.append([1, j + 1, -facteur, k + 1])  # Format imposé
    expr = pxsl_print_operations([listA], listOp = listOp, method = "mat")
    return expr


def randmatrixrect(p,q,a,b):
    """Returns a rectangular matrix with p rows and q columns such that every coefficient is a realization of
of a discrete  random variable on range(a, b)
    :returns: LaTeX bmatrix as a string

    :pxs_trigger: générer matrice rectangulaire aléatoire, coefficients entiers uniformes, exercice matrice p x q quelconque
    :pxs_returns: |
        Matrix sympy de dimensions p×q dont chaque coefficient est tiré
        uniformément et indépendamment dans range(a, b) (intervalle semi-ouvert).
    :pxs_example: |
        M = randmatrixrect(3, 4, -5, 5)
        # Dans MyST : $M = \\py{pxsl_matrix(M)}$
    :pxs_antipattern: Utiliser np.random.randint puis convertir en Matrix sympy — perd le comportement reproductible avec sympy.stats.DiscreteUniform.
    """

    M= eye(p,q)
    for i in range(p):
        for j in range(q):
            #print('(i,j) =', i,j,'\n')
            #M[i,j] = next(sample(DiscreteUniform('h', range(a, b))))
            M[i,j] = sample(DiscreteUniform('h', range(a, b)))
       # M[i,j] = next(sample(DiscreteUniform('h', range(a, b)))) for i in range(p) for j in range(p)]

    return  M

def pxs_invertible_matrix(n):
    """
    Génère une matrice carrée inversible de dimension n à coefficients entiers.

    :pxs_trigger: générer matrice carrée inversible aléatoire, matrice n×n avec déterminant non nul, exercice avec matrice inversible
    :pxs_returns: |
        Matrix sympy de dimension n×n à coefficients entiers dans [-2, 2],
        garantie inversible (det≠0). Si 100 tirages consécutifs échouent,
        retourne la matrice identité eye(n).
    :pxs_example: |
        M = pxs_invertible_matrix(3)
        # Dans MyST : $M = \\py{pxsl_matrix(M)}$
        # Garantie : M.det() != 0
    :pxs_antipattern: Tirer coefficients au hasard sans vérifier det≠0 — risque d'obtenir une matrice non inversible dans un exercice qui exige l'inversibilité.
    """
    for _ in range(100):
        entries = [[random.randint(-2, 2) for _ in range(n)] for _ in range(n)]
        M = Matrix(entries)
        if M.det() != 0:
            return M
    return Matrix.eye(n)

def pxs_diag_matrix(p,a,b):
    """
    Returns a square diagonal matrix of size p such that every coefficient is a
    realization of a uniform discrete random variable, the range of which is range(a, b)

    :pxs_trigger: générer matrice diagonale aléatoire, diagonale de valeurs entières, exercice diagonalisation ou valeurs propres contrôlées
    :pxs_returns: |
        Matrix sympy diagonale de dimension p×p dont les coefficients
        diagonaux sont tirés uniformément dans range(a, b) (intervalle
        semi-ouvert), et zéros hors diagonale.
    :pxs_example: |
        D = pxs_diag_matrix(3, -5, 5)
        # Dans MyST : $D = \\py{pxsl_matrix(D)}$
        # Utile pour construire P·D·P^-1 avec valeurs propres contrôlées.
    :pxs_antipattern: Utiliser sympy.diag(randint, randint, randint) qui ne contrôle pas la bornitude exacte via DiscreteUniform.
    """
    D= eye(p)
    for i in range(p):
        for j in range(p):
            if j==i:
                D[i,j] = sample(DiscreteUniform('h', range(a, b)))
            else:
                    D[i,j] = 0
    return  D

def pxs_construct_RREF(n = 3, p = 3, M = (1, 2, 3), min = -9, max = 9):
    """
    Construct a matrix with a partial Row Reduced Echelon Form (RREF) structure
    based on a given pivot pattern.

    The function creates a matrix of shape `(n, p)` whose pivot positions are
    specified by the tuple `M`. Each element `m` of `M` indicates that the
    corresponding row has a pivot equal to 1 in column `m-1`.
    The remaining coefficients located to the right of the pivot and outside
    the pivot columns are filled with random integers between `min` and `max`.

    Parameters
    ----------
    n : int, optional
        Number of rows of the matrix (default is 3).
    p : int, optional
        Number of columns of the matrix (default is 3).
    M : tuple or Matrix, optional
        - If `M` is a tuple, it represents the pivot positions (1-based indexing).
        - If `M` is a SymPy Matrix, it is copied and used as the initial matrix.
    min : int, optional
        Minimum value for the random coefficients (default is -9).
    max : int, optional
        Maximum value for the random coefficients (default is 9).

    Returns
    -------
    Matrix
        A SymPy matrix of shape `(n, p)` that follows the structure imposed
        by `M`.

    Examples
    --------
    >>> pxs_construct_RREF(n=3, p=4, M=(1, 3))
    Matrix([
    [1, 0, 0, a],
    [0, 0, 1, b],
    [0, 0, 0, 0]
    ])

    >>> pxs_construct_RREF(n=2, p=3, M=(2,))
    Matrix([
    [0, 1, c],
    [0, 0, 0]
    ])

    :pxs_trigger: construire matrice RREF avec pivots aux positions choisies, exercice forme échelonnée réduite avec variables libres, pivots 1 sur colonnes imposées
    :pxs_returns: |
        Matrix sympy de forme (n, p) avec pivots égaux à 1 aux colonnes
        spécifiées dans M (1-based), zéros dans les colonnes de pivot hors
        ligne de pivot, et entiers aléatoires entre min et max dans les
        autres positions à droite des pivots.
    :pxs_example: |
        A = pxs_construct_RREF(n=3, p=4, M=(1, 3))
        # Matrice en RREF avec pivots en colonnes 1 et 3, x_2 et x_4 libres.
        # Dans MyST : $A = \\py{pxsl_matrix(A)}$
    :pxs_antipattern: Construire manuellement à la main — trop long et sujet à erreurs sur le placement des zéros dans les colonnes pivot.
    """

    if isinstance(M, Matrix):
        A = M. copy()
    elif isinstance(M, tuple):
        A = zeros(n, p)
    for i, m in enumerate(M):
        A[i, m-1] = 1
    for i in range(len(M)):
        for k in range(p):
            if k+1 > M[i] and k+1 not in M:
                A[i, k] = rd.randint(min, max)
    return A

def pxs_generate_sys(M = (1, 2, 3), n = 3, p = 3, N = "", opt = "sys", min = -9, max = 9):
    """
    Generate a linear system associated with a matrix in (partial) RREF form.

    The function first constructs a matrix with a Row Reduced Echelon Form–like
    structure using `pxs_construct_RREF`, based on the pivot pattern `M`.
    A right-hand side vector is generated (or copied) and a simplifying
    transformation matrix is then applied to produce either the full linear
    system or only the transformed coefficient matrix.

    Parameters
    ----------
    M : tuple or Matrix, optional
        - If `M` is a tuple, it specifies the pivot positions (1-based indexing)
          used to construct the RREF-like matrix.
        - If `M` is a SymPy Matrix, its shape defines the values of `n` and `p`.
    n : int, optional
        Number of rows of the system (default is 3).
    p : int, optional
        Number of columns of the coefficient matrix (default is 3).
    N : Matrix or str, optional
        Right-hand side vector of the system.
        If an empty string is provided, a random vector of length `n` with
        integer entries between `-3` and `3` is generated.
    opt : str, optional
        Output option:
        - `"sys"` returns both the transformed coefficient matrix and the
          transformed right-hand side vector.
        - Any other value returns only the transformed coefficient matrix.
    min : int, optional
        Minimum value for the random coefficients in the generated matrix
        (default is 9).
    max : int, optional
        Maximum value for the random coefficients in the generated matrix
        (default is 9).

    Returns
    -------
    Matrix or tuple of Matrix
        - If `opt == "sys"`, returns a tuple `(A, B)` where `A` is the transformed
          coefficient matrix and `B` is the transformed right-hand side vector.
        - Otherwise, returns only the transformed coefficient matrix.

    Examples
    --------
    >>> A, B = pxs_generate_sys(M=(1, 3), n=3, p=4)
    >>> A.shape
    (3, 4)

    >>> A = pxs_generate_sys(M=(2,), n=2, p=3, opt="mat")
    >>> A.shape
    (2, 3)

    :pxs_trigger: générer système linéaire avec pivots imposés, exercice Gauss-Jordan avec variables libres contrôlées, système à partir RREF brouillé
    :pxs_returns: |
        Si opt="sys" : tuple (A, B) où A est une matrice (n,p) obtenue en
        multipliant une matrice RREF par une transformation inversible
        (pxs_system_simpl) et B le second membre correspondant.
        Sinon : A seule. La solution du système est prédictible depuis M.
    :pxs_example: |
        A, B = pxs_generate_sys(M=(1, 3), n=3, p=4)
        # Système de 3 équations à 4 inconnues, x_2 et x_4 libres.
        # Dans MyST : $\\py{pxsl_system_lin(A, B)}$
    :pxs_antipattern: Tirer A et B au hasard puis rétro-ingénierer la solution — impossible de contrôler la structure des variables libres.
    """

    # La matrice est N est copiée pour ne pas modifier la matrice originale

    if isinstance(M, Matrix):
        n, p = M.shape
    if N=="":
        N = Matrix([rd.randint(-3,3) for i in range(n)])
    A, B = pxs_construct_RREF(n, p, M, min, max), N.copy()

    A1 = pxs_system_simpl(n = n, opt = "")

    if opt=="sys":
        return A1 * A, A1 * B
    else:
        return A1 * A

def pxs_repeat_generate_sys(M = (1, 2, 3), n = 3, p = 3, N = "", opt = "sys", min = -9, max = 9, backup = Matrix([[1, 1, 1], [1, 2, 3], [2, 3, 4]]), nb_iter = 10):
    """
    Essaie pxs_generate_sys jusqu'à obtenir un système sans colonne nulle.

    :pxs_trigger: générer système linéaire robuste sans colonne nulle, retry avec backup, exercice garantie coefficient de chaque variable présent
    :pxs_returns: |
        Même type de retour que pxs_generate_sys (tuple (A, B) ou A seule
        selon opt), mais en réessayant jusqu'à nb_iter fois pour éviter les
        matrices avec une colonne nulle (variable absente du système).
        Si échec après nb_iter essais, retourne le backup (matrice fixe)
        et un vecteur nul compatible.
    :pxs_example: |
        A, B = pxs_repeat_generate_sys(M=(1, 3), n=3, p=4, nb_iter=20)
        # Garantie : pas de colonne nulle dans A (toutes les variables apparaissent).
    :pxs_antipattern: Appeler pxs_generate_sys sans contrôle — risque d'obtenir un système où une variable n'apparaît nulle part (exercice cassé).
    """
    for _ in range(nb_iter):
        res = pxs_generate_sys(M, n, p, N, opt, min, max)
        A = res[0] if opt == "sys" else res
        if not pxs_zero_column(A):
            return res
    return (backup, zeros(backup.rows, 1)) if opt == "sys" else backup


def pxs_gauss_jordan(
    A,
    B=None,
    x: str = "x",
    method: str = "sys",
    view: str = "sep",
    detail: str = "on",
    strict: bool = False,
    frac: bool = True,
    vectors: str = "col",
    short: bool = True
):
    """
    Perform a Gauss–Jordan elimination and generate a formatted (LaTeX) output
    of all intermediate steps.

    The function applies the Gauss–Jordan algorithm to the linear system
    ``A * X = B`` (or to the reduction of ``A`` alone if ``B is None``).
    Each elementary row operation is recorded so that a detailed, step-by-step
    symbolic representation of the reduction process can be produced, typically
    for inclusion in a LaTeX document via the ``myst`` / ``pxsl_*`` utilities.

    Parameters
    ----------
    A : Matrix
        Coefficient matrix of the linear system (SymPy ``Matrix``).
    B : Matrix or None, optional
        Right-hand side vector or matrix. If ``None``, the function only reduces
        ``A`` (the right-hand side is taken as a zero matrix of compatible size).
    x : str, optional
        Base name of the unknown variables used in the symbolic display
        (e.g. ``"x"`` produces ``x_1, x_2, ...``). Default is ``"x"``.
    method : str, optional
        Display method passed to the printing routine (typically ``"sys"`` to
        format the output as a linear system). Default is ``"sys"``.
    view : str, optional
        Visualization mode for intermediate steps (for example, separate or
        combined views of matrices and operations). Default is ``"sep"``.
    detail : str, optional
        Level of detail in the output:
        - ``"on"`` displays all elementary operations,
        - other values may reduce verbosity (depending on
          ``pxsl_print_operations``).
        Default is ``"on"``.
    strict : bool, optional
        Pivot selection strategy:
        - if ``True``, applies a strict Gauss–Jordan strategy by choosing, below
          the current row, the pivot with the largest absolute value in the
          column (partial pivoting);
        - if ``False``, chooses the first non-zero coefficient below the current
          row (simplified strategy).
        Default is ``False``.
    frac : bool, optional
        Controls the rendering of rational coefficients:
        - if ``True``, coefficients are displayed as fractions when appropriate,
        - if ``False``, coefficients may be displayed in a simplified inline form.
        Default is ``True``.
    vectors : str, optional
        Orientation of solution vectors in the display:
        - ``"col"`` for column vectors,
        - any other value for row vectors.
        Default is ``"col"``.

    Returns
    -------
    Any
        A symbolic object representing the formatted output (typically a LaTeX
        string or structure produced via ``myst`` and ``pxsl_*`` utilities).

    Examples
    --------
    Basic example (solving a square linear system):

    >>> from sympy import Matrix
    >>> A = Matrix([[1, 2], [3, 4]])
    >>> B = Matrix([[5], [6]])
    >>> out = pxs_gauss_jordan(A, B)
    >>> isinstance(out, str) or out is not None
    True

    Changing the variable base name (``x="u"`` produces ``u_1, u_2, ...``):

    >>> A = Matrix([[1, 1], [0, 1]])
    >>> B = Matrix([[2], [3]])
    >>> out = pxs_gauss_jordan(A, B, x="u")
    >>> isinstance(out, str) or out is not None
    True

    Pivot strategy: simplified vs strict (partial pivoting):

    >>> A = Matrix([[0, 1], [2, 3]])
    >>> B = Matrix([[1], [1]])
    >>> out1 = pxs_gauss_jordan(A, B, strict=False)  # first non-zero pivot
    >>> out2 = pxs_gauss_jordan(A, B, strict=True)   # largest |value| pivot
    >>> (out1 is not None) and (out2 is not None)
    True

    Reducing verbosity (if supported by the display routine):

    >>> A = Matrix([[1, 2], [3, 4]])
    >>> B = Matrix([[5], [6]])
    >>> out = pxs_gauss_jordan(A, B, detail="off")
    >>> out is not None
    True

    Skipping the final solution display (only reduction steps):

    >>> A = Matrix([[1, 2], [3, 4]])
    >>> B = Matrix([[5], [6]])
    >>> out = pxs_gauss_jordan(A, B, solve=False)
    >>> out is not None
    True

    Reducing ``A`` alone (``B=None``):

    >>> A = Matrix([[1, 2, 3], [2, 4, 6]])
    >>> out = pxs_gauss_jordan(A)
    >>> out is not None
    True

    Solution set representation (vector orientation and span form):

    >>> A = Matrix([[1, 1, 0], [0, 0, 1]])
    >>> B = Matrix([[2], [3]])
    >>> out_col = pxs_gauss_jordan(A, B, vectors="col", span=True)
    >>> out_row = pxs_gauss_jordan(A, B, vectors="row", span=False)
    >>> (out_col is not None) and (out_row is not None)
    True

    :pxs_trigger: Gauss-Jordan complet avec solution paramétrique, résolution système sous-déterminé, ensemble solution vectoriel, Vect base noyau, AX=B paramétrée
    :pxs_returns: |
        Dictionnaire sol avec les clés :
        - "resol" (myst) : étapes détaillées de la réduction en LaTeX
        - "sys" (myst) : système final résolu ou incompatible
        - "param" (tuple myst) : écriture paramétrique (x_1,...) = (...)
        - "free_var" (myst) : liste des variables libres
        - "set" (myst) : ensemble solution sous forme {x0 + x_i·v_i + ... : x_i ∈ R}
        - "span" (myst) : représentation x0 + Vect(v_1, ..., v_k)
        - "A", "B" (Matrix) : matrices finales après réduction.
    :pxs_example: |
        A = Matrix([[1, 2, 3], [2, 4, 7]])
        B = Matrix([1, 3])
        sol = pxs_gauss_jordan(A, B)
        # Dans MyST : \\py{sol["resol"]} puis $\\mathcal{S} = \\py{sol["set"]}$
    :pxs_antipattern: Utiliser sympy.linsolve() qui donne la solution paramétrique en une seule expression sans détailler les étapes de Gauss-Jordan ni la décomposition en base + particulière.
    """

    def __check_incompatible(A, B):
        npA = np.array(A)
        npB = np.ravel(B)
        ind_zero_lines =  np.where([not npA[i].any() for i in range(len(npA))])[0]
        return npB[ind_zero_lines].any()

    #def __print_solved(A, B, col_pivots, free_indices, x = "x", frac = True):
        #n,p = A.shape
        #r = len(col_pivots)

        #vect_x = Matrix([Symbol(x + "_" + str(j + 1)) for j in range(p)])
        #expr = myst(r"""\left\{ \begin{array}{rcl} """) if r > 1 else myst(r"""\left. \begin{array}{rcl} """)
        #for i in range(r):
            #j = col_pivots[i] - 1
            #expr += myst(r"""\py{vect_x[j]} & =&  """, globals(), locals())
            #sign = " "
            #if B[i] == 0 and A[i, j+1:].is_zero_matrix:
                #expr += "0"
            #if B[i]:
                #rhs = myst(r"""\py{B[i].p}/\py{B[i].q}""", globals(), locals()) if (isinstance(B[i], Rational) and B[i].q != 1 and not frac) else latex(B[i])
                #expr += myst(r"""\py{rhs}""",globals(),locals())
                #sign = "+"

            #for k in range(j+1, p):
                #if A[i, k] != 0:
                    #expr += pxsl_ax(-A[i, k], vect_x[k], sign, frac = frac)
                    #sign = "+"
            #expr += myst(r"""\\[0.3em]""")



        # displaying the list of free variables
        #if free_indices:
            #expr += latex(tuple(vect_x[j-1] for j in free_indices)) if len(free_indices) > 1 else myst(r"""\py{vect_x[list(free_indices)[0] - 1]}""", globals(), locals())
            #set_r = myst(r"""\R^{\py{p-r}}""", globals(), locals()) if p - r > 1 else myst(r"""\R""")
            #expr += myst(r""" &\in &\py{set_r}\\""", globals(), locals())
        #expr += myst(r"""\end{array}\right.""")

        #return expr

    def __print_solved(A, B, col_pivots, free_indices, x = "x", frac = True):
        n,p = A.shape
        r = len(col_pivots)

        vect_x = Matrix([Symbol(x + "_" + str(j + 1)) for j in range(p)])
        expr = myst(r"""\left\{ \begin{array}{rcl} """)
        k = -1
        for i in range(p):
            if i+1 in free_indices:
                expr += myst(r"""\py{latex(vect_x[i])} &=&\py{latex(vect_x[i])}\\""", globals(), locals())
                continue
            k += 1
            j = i
            sign = " "

            expr += myst(r"""\py{latex(vect_x[i])} &=& """, globals(), locals())
            if B[k] == 0 and A[k, j+1:].is_zero_matrix:
                expr += myst(r"""0""", globals(), locals())
            if B[k]:
                rhs = myst(r"""\py{B[k].p}/\py{B[k].q},""", globals(), locals()) if (isinstance(B[k], Rational) and B[k].q != 1 and not frac) else latex(B[k])
                expr += myst(r"""\py{rhs}""",globals(),locals())
                sign = "+"

            for l in range(j+1, p):
                if A[k, l] != 0:
                    expr += myst(r"""\py{pxsl_ax(-A[k, l], vect_x[l], sign, frac = frac)}""", globals(), locals())
                    sign = "+"
            if i != p-1:
                expr += myst(r""" \\ """)

        # displaying the list of free variables
        #if free_indices:
            #for j in free_indices:
                #expr += myst(r"""\py{latex(vect_x[j-1])}""", globals(), locals())
        expr += myst(r"""\end{array}\right.""")


        return expr

    def __print_param(A, B, col_pivots, free_indices, x = "x", frac = True):
        n,p = A.shape
        r = len(col_pivots)

        vect_x = Matrix([Symbol(x + "_" + str(j + 1)) for j in range(p)])
        expr1 = myst(r"""\left( """)
        for i, v in enumerate(vect_x):
            if i != len(vect_x) -1:
                expr1 += myst(r"""\py{latex(v)},""", globals(), locals())
            else:
                expr1 += myst(r"""\py{latex(v)}""", globals(), locals())
        expr1 += myst(r""" \right) = ( """)
        k = -1
        for i in range(p):
            if i+1 in free_indices:
                if i != p-1:
                    expr1 += myst(r"""\py{latex(vect_x[i])},""", globals(), locals())
                else:
                    expr1 += myst(r"""\py{latex(vect_x[i])}""", globals(), locals())
                continue
            k += 1
            j = i
            sign = " "
            if B[k] == 0 and A[k, j+1:].is_zero_matrix:
                expr1 += myst(r"""0""", globals(), locals())
            if B[k]:
                rhs = myst(r"""\py{B[k].p}/\py{B[k].q},""", globals(), locals()) if (isinstance(B[k], Rational) and B[k].q != 1 and not frac) else latex(B[k])
                if k != p-1:
                    expr1 += myst(r"""\py{rhs}""",globals(),locals())
                else:
                    expr1 += myst(r"""\py{rhs}""",globals(),locals())
                sign = "+"

            for l in range(j+1, p):
                if A[k, l] != 0:
                    expr1 += myst(r"""\py{pxsl_ax(-A[k, l], vect_x[l], sign, frac = frac)}""", globals(), locals())
                    sign = "+"
            if i != p-1:
                expr1 += myst(r""" , """)

        # displaying the list of free variables
        #if free_indices:
            #for j in free_indices:
                #expr += myst(r"""\py{latex(vect_x[j-1])}""", globals(), locals())  -->
        expr1 += myst(r""") """)
        expr2 = myst(r""" """)
        if free_indices:
            expr2 = latex(tuple(vect_x[j-1] for j in free_indices)) if len(free_indices) > 1 else myst(r"""\py{vect_x[list(free_indices)[0] - 1]}""", globals(), locals())
            set_r = myst(r"""\R^{\py{p-r}}""", globals(), locals()) if p - r > 1 else myst(r"""\R""")
            expr2 += myst(r""" \in \py{set_r}""", globals(), locals())

        return expr1, expr2

    def __get_basis(A, B, col_pivots, free_indices, frac = True):
        n, p = A.shape
        canonical = eye(p)
        basis = []
        for j in free_indices:
            lesser_pivots = [p-1 for p in col_pivots if p < j]
            nb = len(lesser_pivots)
            u = canonical[j-1, :] - sum([A[i, j-1] * canonical[pivot, :] for i, pivot in enumerate(lesser_pivots)], start = zeros(1, p))
            basis.append(u)
        # particular solution:
        x0 = sum([B[i] * canonical[p - 1, :] for i, p in enumerate(col_pivots)], start = zeros(1, p))
        return basis, x0

    pxs_lang = get_pxs_lang()
    sol = {"sys": myst(r""" """), "param": myst(r""" """), "free_var": myst(r""" """)}


    [n, p] = A.shape

    no_rhs = B is None
    if no_rhs:
        B = zeros(n, 1)

    listA = [A.copy()]
    listB = [B.copy()]
    listOp = [[0,0,0,0]]
    r = -1

    col_pivots = []
    sol["resol"] = myst(r"""\begin{equation*}""", locals(), globals()) if solve else " "

    j = 0
    go_on = True
    while j < p and r < n - 1 and go_on:
        # looking for the line to swap with:
        if strict:
            k = max(range(r+1, A.rows), key = lambda i: Abs(A[i, j]))
        # if strict = False, take the row of the first non zero coefficient if any
        elif np.any(A[r+1:, j]):
            k = np.where(np.ravel(A[r + 1:, j]) != 0)[0][0] + r + 1
        else: # all coeffs under row r+1 are zero, nothing will be done anyway
            k = r + 1

        if A[k, j] != 0:
            r += 1
            if A[k, j] != 1:
                listOp.append([1 / A[k, j], k + 1, 0, 0])
                B[k, :] = B[k, :] / A[k, j]
                A[k, :] = A[k, :] / A[k, j]
                listA.append(A.copy())
                listB.append(B.copy())

            col_pivots.append(j + 1)

            if k != r:
                A.row_swap(k, r)
                B.row_swap(k, r)
                listA.append(A.copy())
                listB.append(B.copy())
                listOp.append([0, r + 1, 1, k + 1])
            for i in range(n):
                if i != r and A[i, j]:
                    listOp.append([1, i + 1, -A[i, j], r + 1])
                    B[i, :] = B[i, :] - A[i, j] * B[r, :]
                    A[i, :] = A[i, :] - A[i, j] * A[r, :]
                    listA.append(A.copy())
                    listB.append(B.copy())

        go_on = not (short and __check_incompatible(A, B))
        j += 1

    free_indices = set(range(1, p + 1)) - set(col_pivots) # will be useful for basis of solutions

    list_mat = [listA] if no_rhs else [listA, listB]
    sol["resol"] += pxsl_print_operations(list_mat, listOp = listOp, method = method, x = x, view = view, detail = detail, frac = frac)
    sol["resol"] += myst(r"""\end{equation*}
""")
        #if len(col_pivots) > 1:
            #sol["resol"] += myst(r"""
    #On obtient donc le système équivalent suivant :""") if pxs_lang == "fr" else myst(r"""Hence we get the following equivalent system:""")
        #else:
            #sol["resol"] += myst(r"""
    #Le système est donc équivalent à :""") if pxs_lang == "fr" else myst(r"""Hence the system is equivalent to:""") -->
#     sol["sys"] = myst(r"""
# \begin{equation*}""")

    consistent = not __check_incompatible(A, B)

    sol["sys"] = __print_solved(A, B, col_pivots, free_indices, x = x, frac = frac) if consistent else pxsl_system_lin(A, B, x = x, frac = frac)
    sol["param"], sol["free_var"] = __print_param(A, B, col_pivots, free_indices, x = x, frac = frac)
#     sol["sys"] += myst(r"""
# \end{equation*}""")
    sol["A"] = A
    sol["B"] = B
        #expr += myst(r"""\\ \\""")
        #expr += __print_solved(A, B, col_pivots, free_indices, x = x, frac = frac)
        #expr += myst(r"""\end{equation*}""", locals(), globals())

        # displaying the list of free variables
    vect_x_free = Matrix([Symbol(x + "_" + str(j)) for j in free_indices])
    basis, x0 = __get_basis(A, B, col_pivots, free_indices, frac = frac)
    if vectors == "col": basis, x0 = [v.T for v in basis], x0.T


        # displaying the solutions as linear combinations of the basis vectors:
    mat_delim = "[" if pxs_lang == "en" else "("
    if consistent:
        # sol["set"] = myst(r"""\begin{equation*}
        #   \begin{align*}
        #       \mathcal{S} &= \left\{""")
        sol["set"] = myst(r"""\left\{""")
        if not x0.is_zero_matrix or not free_indices:
            sol["set"] += latex(x0, mat_delim = mat_delim, fold_short_frac = not frac)
            if free_indices: sol["set"]+= " + "
        for l in range(len(basis)):
            vector_tex = latex(basis[l], mat_delim = mat_delim, fold_short_frac = not frac)
            sol["set"] += myst(r""" \py{vect_x_free[l]} . \py{vector_tex} \py{" + " if (l < len(basis) - 1) else " "}""", globals(), locals())
        if free_indices: sol["set"] += myst(r""" ~ : ~ """)
            # displaying the list of free variables
        if free_indices:
            sol["set"] += latex(tuple(vect_x_free)) if len(vect_x_free) > 1 else myst(r"""\py{vect_x_free[0]}""", globals(), locals())
            set_r = myst(r"""\R^{\py{p-r - 1}}""", globals(), locals()) if p - r -1 > 1 else myst(r"""\R""")
            sol["set"] += myst(r""" \in \py{set_r}""", globals(), locals())

        # sol["set"] += myst(r"""\right\}
        # \end{align*}
        # \end{equation*}""")
        sol["set"] += myst(r"""\right\}""")

        sol["span"] = myst(r""" """)
        if free_indices:
            vepan = "Vect" if pxs_lang == "fr" else "Span"
    #         sol["span"] = myst(r"""
    # \begin{equation*}
    # \begin{align*}""")
            if not x0.is_zero_matrix:
                sol["span"] += latex(x0, mat_delim = mat_delim, fold_short_frac = not frac) + " + "
            sol["span"] += myst(r"""\text{\py{vepan}}\left( """, globals(), locals())
                # for l in range(len(basis)):
                    # vector_tex = latex(basis[l], mat_delim = mat_delim, fold_short_frac = not frac)
                    # expr += myst(r"""\py{vector_tex} \py{" , " if (l < len(basis) - 1) else " "}""", globals(), locals())
            sol["span"] += " , ".join([latex(vector, mat_delim = mat_delim, fold_short_frac = not frac) for vector in basis])
            sol["span"] += myst(r"""\right)""")
    #         sol["span"] += myst(r"""
    # \end{align*}
    # \end{equation*}""")

    else:
        sol["set"], sol["span"] = myst(r"""\emptyset"""), myst(r"""\emptyset""")

    return sol

def pxs_colinear_rows(M, i, j):
    """
    Test whether two rows of a matrix are colinear.

    Two rows are said to be colinear if one is a scalar multiple of the other.
    The test is performed by computing the rank of the matrix formed by the
    two rows.

    By convention, if at least one of the two rows is a zero row, the function
    returns ``False`` (zero rows are ignored).

    Parameters
    ----------
    M : Matrix
        A SymPy matrix.
    i : int
        Index of the first row to test (0-based).
    j : int
        Index of the second row to test (0-based).

    Returns
    -------
    bool
        ``True`` if rows ``i`` and ``j`` are colinear, ``False`` otherwise.

    Examples
    --------
    Two proportional rows:

    >>> from sympy import Matrix
    >>> M = Matrix([[1, 2, 3],
    ...             [2, 4, 6],
    ...             [1, 0, 1]])
    >>> pxs_colinear_rows(M, 0, 1)
    True

    Rows that are not colinear:

    >>> pxs_colinear_rows(M, 0, 2)
    False

    A zero row is ignored:

    >>> M = Matrix([[1, 2, 3],
    ...             [0, 0, 0],
    ...             [2, 4, 6]])
    >>> pxs_colinear_rows(M, 0, 1)
    False

    Colinearity still detected with non-adjacent rows:

    >>> pxs_colinear_rows(M, 0, 2)
    True

    :pxs_trigger: tester colinéarité deux lignes matrice, lignes proportionnelles, rang 1 paire de lignes, vérifier redondance équations
    :pxs_returns: |
        bool : True si les lignes i et j sont non nulles et proportionnelles
        (rang de la matrice formée des deux lignes égal à 1), False sinon.
        Par convention, les lignes nulles sont ignorées (retourne False).
    :pxs_example: |
        M = Matrix([[1, 2, 3], [2, 4, 6], [1, 0, 1]])
        pxs_colinear_rows(M, 0, 1)  # True, car L_2 = 2·L_1
        pxs_colinear_rows(M, 0, 2)  # False
    :pxs_antipattern: Vérifier M.row(i) / M.row(j) == constant — échoue si une entrée est zéro ou si on teste avec des symboles.
    """
    if M.row(i).is_zero or M.row(j).is_zero:
        return False  # on ignore les lignes nulles ici
    return Matrix([M.row(i), M.row(j)]).rank() == 1

def pxs_break_colinearity(M, N, i, j, *, coef_range=(-3, 3)):
    """
    Break the colinearity between two rows of a linear system using
    an elementary row operation.

    If rows ``i`` and ``j`` of the matrix ``M`` are colinear, the function
    replaces row ``i`` by a linear combination

        row_i ← a * row_i + b * row_k

    where ``k`` is a row index different from ``i`` and ``j``, and
    ``a`` and ``b`` are nonzero integers chosen randomly in ``coef_range``.

    The same operation is applied consistently to the right-hand side
    vector ``N`` so that the linear system remains equivalent.

    If rows ``i`` and ``j`` are not colinear, or if no suitable third row
    is available, the matrices are returned unchanged.

    Parameters
    ----------
    M : Matrix
        Coefficient matrix of the linear system.
    N : Matrix
        Right-hand side column vector of the system.
    i : int
        Index of the first row (0-based).
    j : int
        Index of the second row (0-based).
    coef_range : tuple of int, optional
        Range ``(min, max)`` from which the integer coefficients ``a`` and
        ``b`` are drawn (default is ``(-3, 3)``). Zero is excluded.

    Returns
    -------
    Matrix
        The modified coefficient matrix.
    Matrix
        The modified right-hand side vector.

    Examples
    --------
    Breaking colinearity between two proportional rows:

    >>> from sympy import Matrix
    >>> M = Matrix([[1, 2, 3],
    ...             [2, 4, 6],
    ...             [1, 0, 1]])
    >>> N = Matrix([1, 2, 0])

    >>> M2, N2 = pxs_break_colinearity(M, N, 0, 1)

    The resulting system is equivalent, but rows 0 and 1 are no longer colinear:

    >>> from sympy import Matrix
    >>> Matrix([M2.row(0), M2.row(1)]).rank() == 1
    False

    If the rows are not colinear, nothing is changed:

    >>> M = Matrix([[1, 2],
    ...             [3, 4]])
    >>> N = Matrix([1, 1])
    >>> M2, N2 = pxs_break_colinearity(M, N, 0, 1)
    >>> M2 == M and N2 == N
    True

    If no suitable third row exists, the matrices are returned unchanged:

    >>> M = Matrix([[1, 2],
    ...             [2, 4]])
    >>> N = Matrix([1, 2])
    >>> M2, N2 = pxs_break_colinearity(M, N, 0, 1)
    >>> M2 == M and N2 == N
    True

    :pxs_trigger: casser colinéarité deux lignes système linéaire, rendre lignes indépendantes par opération élémentaire, préserver solution du système
    :pxs_returns: |
        Tuple (M_modifiée, N_modifiée) où la ligne i de M est remplacée par
        a·L_i + b·L_k avec k ≠ i,j et a,b entiers non nuls aléatoires
        dans coef_range. N est modifiée cohéremment pour préserver la
        solution. Si pas de colinéarité ou pas de ligne k valide, retourne
        (M, N) inchangées.
    :pxs_example: |
        M = Matrix([[1, 2, 3], [2, 4, 6], [1, 0, 1]])
        N = Matrix([1, 2, 0])
        M2, N2 = pxs_break_colinearity(M, N, 0, 1)
        # L_1 devient une combinaison avec L_3 ; la solution reste la même.
    :pxs_antipattern: Supprimer la ligne colinéaire — change le système et élimine une équation au lieu de la rendre indépendante.
    """
    M = M.copy()
    N = N.copy()
    n = M.rows

    if not pxs_colinear_rows(M, i, j):
        return M, N  # rien à faire

    # choisir une ligne k différente de i et j
    candidates = [k for k in range(n) if k not in (i, j) and not M.row(k).is_zero]
    if not candidates:
        return M, N  # pas de ligne exploitable

    k = rd.choice(candidates)

    # coefficients non nuls
    a = rd.choice([c for c in range(*coef_range) if c != 0])
    b = rd.choice([c for c in range(*coef_range) if c != 0])

    # opération élémentaire
    M.row_op(i, lambda v, col: a * v + b * M[k, col])
    N.row_op(i, lambda v, col: a * v + b * N[k])

    return M, N

def pxs_break_all_colinear_rows(A, B, max_iter=5):
    """
    Remove colinearity between all pairs of rows of a linear system.

    The function repeatedly scans the coefficient matrix ``A`` for pairs of
    colinear rows. Whenever such a pair is found, an elementary row operation
    is applied (via :func:`pxs_break_colinearity`) to break the colinearity
    while preserving the solution set of the system.

    The process is repeated until no colinear row pairs remain, or until the
    maximum number of iterations is reached.

    Parameters
    ----------
    A : Matrix
        Coefficient matrix of the linear system.
    B : Matrix
        Right-hand side column vector.
    max_iter : int, optional
        Maximum number of iterations allowed to remove colinearities
        (default is ``10``).

    Returns
    -------
    Matrix
        The modified coefficient matrix with reduced row colinearity.
    Matrix
        The modified right-hand side vector.

    Examples
    --------
    Removing colinearity between multiple rows:

    >>> from sympy import Matrix
    >>> A = Matrix([[1, 2, 3],
    ...             [2, 4, 6],
    ...             [3, 6, 9]])
    >>> B = Matrix([1, 2, 3])

    >>> A2, B2 = pxs_break_all_colinear_rows(A, B)

    After processing, no two nonzero rows are colinear:

    >>> any(
    ...     Matrix([A2.row(i), A2.row(j)]).rank() == 1
    ...     for i in range(A2.rows)
    ...     for j in range(i + 1, A2.rows)
    ...     if not A2.row(i).is_zero and not A2.row(j).is_zero
    ... )
    False

    If the matrix contains no colinear rows, it is returned unchanged:

    >>> A = Matrix([[1, 0],
    ...             [0, 1]])
    >>> B = Matrix([1, 1])
    >>> A2, B2 = pxs_break_all_colinear_rows(A, B)
    >>> A2 == A and B2 == B
    True

    :pxs_trigger: rendre toutes lignes indépendantes, supprimer toute colinéarité système linéaire, éviter système redondant, exercice avec lignes non proportionnelles
    :pxs_returns: |
        Tuple (A_modifiée, B_modifiée) où itérativement, toute paire de lignes
        colinéaires est brisée via pxs_break_colinearity jusqu'à ce qu'il
        n'y en ait plus ou que max_iter itérations aient été effectuées.
        Le système solution est préservé.
    :pxs_example: |
        A = Matrix([[1, 2, 3], [2, 4, 6], [3, 6, 9]])
        B = Matrix([1, 2, 3])
        A2, B2 = pxs_break_all_colinear_rows(A, B)
        # Plus aucune paire de lignes colinéaires, mais le système reste équivalent.
    :pxs_antipattern: Calculer A.rref() et s'arrêter — donne une forme réduite canonique, pas un système équivalent pédagogique avec lignes "dissemblables".
    """
    M = A.copy()
    N = B.copy()

    for _ in range(max_iter):
        changed = False
        for i in range(M.rows):
            for j in range(i + 1, M.rows):
                if pxs_colinear_rows(M, i, j):
                    M, N = pxs_break_colinearity(M, N, i, j)
                    changed = True
                    break
            if changed:
                break
        if not changed:
            return M, N

    return M, N

def pxs_zero_column(A):
    """
    Checks whether Matrix A has at least one zero column.

    Parameters
    ----------
    A : Matrix

    Returns
    -------
    bool : True if A has at least one zero column, False otherwise

    Examples
    --------
    >>> A = Matrix(
    ... [[1, 0, 2],
    ... [2, 0, -3],
    ... [1, 0, 1]])
    >>> pxs_zero_column(A)
    True

    >>> M = Matrix(
    ... [[1, 0, 2],
    ... [2, 1, -3],
    ... [1, 0, 1]])
    >>> pxs_zero_column(M)
    False

    :pxs_trigger: tester colonne nulle matrice, détecter variable absente système linéaire, colonne de zéros dans matrice
    :pxs_returns: |
        bool : True si la matrice A possède au moins une colonne entièrement
        nulle, False sinon. Utilisé pour filtrer les systèmes où une variable
        n'apparaît pas dans les équations (dégénérescence).
    :pxs_example: |
        A = Matrix([[1, 0, 2], [2, 0, -3], [1, 0, 1]])
        pxs_zero_column(A)  # True (colonne 2 entière nulle)
    :pxs_antipattern: Parcourir toutes les colonnes à la main avec une boucle for — utiliser .is_zero_matrix sur la tranche colonne est plus sûr.
    """
    return np.any([A[:, j].is_zero_matrix for j in range(A.cols)])

## CALCULS DE DÉTERMINANTS

def pxs_determinant(A, detail = "on", **kwargs):
    """
    Calcule pas à pas le déterminant d'une matrice par réduction à une forme triangulaire.

    :pxs_trigger: calcul déterminant par pivot de Gauss, étapes triangulaire supérieure, échanges de lignes factor signe, facteurs diagonaux déterminant
    :pxs_returns: |
        Dictionnaire avec les clés :
        - "oper" (myst) : affichage des opérations et matrices successives
        - "swaps" (int) : nombre d'échanges de lignes effectués
        - "exp" (str) : expression factorisée finale du déterminant (ex. "(-1)^2 · 2 · 3 · 5")
        - "val" (str) : valeur numérique simplifiée du déterminant
        - "all" (myst) : texte LaTeX complet avec explication des échanges.
    :pxs_example: |
        A = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 10]])
        det_info = pxs_determinant(A)
        # Dans MyST : \\py{det_info["all"]}
        # ou séparément : étapes = \\py{det_info["oper"]}, valeur = $\\py{det_info["val"]}$
    :pxs_antipattern: Utiliser A.det() qui donne la valeur sans détailler la méthode par pivot (échanges, facteurs, diagonale finale).
    """

    def __print_ops(listA, listOp, factors, **kwargs):
        n = listA[0].shape[0]
        [listA], listOp = pxs_regroupe_ligne([listA], listOp)
        swaps_txt = myst(r"""\text{swaps:}\quad """) if pxs_lang == "en" else myst(r"""échanges : """)
        factors_txt = myst(r"""\text{factors:}\quad """) if pxs_lang == "en" else myst(r"""facteurs : """)
        r = 0 # nb of swaps
        f = 0 # index of factor
        # First line
        expr = myst(r"""\begin{array}{ccc} """)+myst(r"""&""")+ pxsl_matrix(listA[0]) + myst(r""" \\ \\""")

        # other lines
        for i in range(1, len(listA)):
            printed_ops = pxsl_lines_op(n, listOp[i], frac = frac) if detail == "on" else " "
            expr += myst(r"""\py{printed_ops} & """, locals(), globals()) + pxsl_matrix(listA[i]) + myst(r"""&""")

            if not all([op[0] for op in listOp[i]]): # swap
                r += 1
                expr += myst(r"""\py{swaps_txt} \py{r}""", globals(), locals())
            if not all([op[2] for op in listOp[i]]): # scaling
                f += 1
                current_factors = latex(Mul(*factors[:f], evaluate = False), **kwargs)
                expr += myst(r"""\py{factors_txt} \py{current_factors}""", globals(), locals())
            expr += myst(r"""\\ \\""")
        expr+=myst(r"""\end{array}""")
        return expr

    def __writing(operations, expression, value, nb_swaps):
        text = myst(r"""\begin{equation*}
\py{operations}
\end{equation*}
""", globals(), locals())
        if expression:
            if nb_swaps:
                neg = " "
                nb_swaps_tex = myst(r"""$\py{latex(nb_swaps)}$""", globals(), locals())
            else:
                neg = "not" if pxs_lang == "en" else "n'"
                nb_swaps_tex = "aucun" if pxs_lang == "fr" else "any"
            if pxs_lang == "en":
                text += myst(r"""We have \py{neg} performed \py{nb_swaps_tex} row swap, hence:
\begin{equation*}
\begin{align*}
\det \py{pxsl_matrix(A)} &= \py{expression} \\
&= \py{value} \,.
\end{align*}
\end{equation*}
""", globals(), locals())
            else:
                text += myst(r"""Nous \py{neg}avons effectué \py{nb_swaps_tex} échange de lignes, donc :
\begin{equation*}
\begin{align*}
\det \py{pxsl_matrix(A)} &= \py{expression} \\
&= \py{value} \,.
\end{align*}
\end{equation*}
""", globals(), locals())
        else:
            if pxs_lang == "en":
                text += myst(r"""The last matrix above has a zero diagonal coefficient, hence:
\begin{equation*}
\det \py{pxsl_matrix(A)} = 0\,.
\end{equation*}""")
            else:
                text +=myst(r"""La dernière matrice obtenue ci-dessus possède un coefficient diagonal nul, hence:
\begin{equation*}
\det \py{pxsl_matrix(A)} = 0\,.
\end{equation*}""")

        return text


    pxs_lang = get_pxs_lang()

    n = A.rows
    listA=[A.copy()]
    listOp=[[0,0,0,0]]
    nb_swaps = 0
    factors = []
    for k in range(n - 1):
        if np.any(A[k:, k]):
            # swapping
            r = np.where(np.ravel(A[k:, k]) != 0)[0][0] + k
            if r != k:
                nb_swaps += 1
                A.row_swap(k, r)
                listA.append(A.copy())
                listOp.append([0, r + 1, 1, k + 1])
            # setting 1 as pivot
            if A[k, k] != 1:
                factors.append(A[k, k])
                listOp.append([1 / A[k, k], k + 1, 0, 0])
                A[k, :] /= A[k, k]
                listA.append(A.copy())
            # getting zeros under the pivot
            for j in range(k+1, n):
                if A[j, k] != 0:
                    listOp.append([1, j+1, -A[j, k], k + 1])
                    A[j, :] = A[j, :] - A[j, k] * A[k, :]
                    listA.append(A.copy())
        else: # zero pivot, computation is over
                operations = pxsl_print_operations([listA], listOp = listOp, method = "mat")
                all_details = __writing(operations, None, None, nb_swaps)
                return {"oper" : operations, "swaps" : nb_swaps, "exp" : "0",
                "val" : "0", "all" : all_details}
    np_diag = np.array(A)[range(n), range(n)]
    diag_coeffs = list(np_diag[np_diag != 1]) # non-ones diagonal coefficients of the last matrix
    if not diag_coeffs: diag_coeffs = [1]
    sign = [Pow(-1, nb_swaps, evaluate = False)] if nb_swaps else []
    all_det_factors = sign + factors + diag_coeffs

    # operations = pxsl_print_operations([listA], listOp = listOp, method = "mat")
    operations = __print_ops(listA, listOp, factors, **kwargs)
    expression = latex(Mul(*all_det_factors, evaluate = False), **kwargs)
    value = latex(Mul(*[(-1) ** nb_swaps] + factors + diag_coeffs), **kwargs)
    all_details = __writing(operations, expression, value, nb_swaps)

    result = {
    "oper" : operations,
    "swaps" : nb_swaps,
    "exp" : expression,
    "val" : value,
    "all" : all_details,
    }
    return result


def pxs_compute_determinant(A, smart = True, **kwargs):
    """
    Calcule le déterminant d'une matrice par développement récursif selon les cofacteurs.

    :pxs_trigger: calcul déterminant par cofacteurs développement Laplace, récurrence ligne ou colonne contenant des zéros, stratégie smart meilleure ligne/colonne
    :pxs_returns: |
        Objet myst contenant le calcul complet du déterminant par développement
        récursif selon lignes/colonnes en LaTeX (environnement align*), avec
        factorisation intermédiaire des coefficients communs. Si smart=True,
        choisit à chaque étape la ligne ou colonne contenant le plus de zéros.
    :pxs_example: |
        A = Matrix([[1, 0, 0, 2], [3, 4, 0, 5], [6, 7, 8, 0], [9, 1, 2, 3]])
        # Dans MyST : \\py{pxs_compute_determinant(A)}
        # Développement optimal par la 1ère ligne (3 zéros).
    :pxs_antipattern: Utiliser A.det() ou développer systématiquement selon la 1ère ligne sans exploiter les lignes/colonnes avec zéros — calcul inutilement lourd.
    """

    def __rec_compute_determinant(A, smart, expr, values, **kwargs):

        def __latex_without_ones(list_terms, **kwargs):
            list_no_ones = [x for x in list_terms if x != 1]
            if list_no_ones:
                return latex(Mul(*list_no_ones, evaluate = False), **kwargs) if list_no_ones != [-1] else myst(r""" - """)
            else:
                return " "

        def __get_coeffs(vector):
            flat = np.array(vector).ravel() # flatten to get a 1d-array
            ones_ind = np.where(flat == 1)[0] # indices of the ones, if any
            indices = np.where(flat)[0]
            if ones_ind: # if any
                return ones_ind[0], indices
            else:
                return indices[0], indices

        def __det2x2(A, **kwargs):
            a, b, c, d = A
            ad = Mul(a, d, evaluate = not (a * d))
            bc = Mul(b, c, evaluate = not (b * c))
            return myst(r"""\py{latex(ad, **kwargs)} - \py{latex(bc, **kwargs)}""", globals(), locals()).replace("- -", "+")

        pxs_lang = get_pxs_lang()
        n = A.rows

        if n == 2:
            try:
                mult = mul_symbol
            except:
                mult = myst(r""" """)
            lpar = myst(r"""\left(""") if len(values) != values.count(1) else myst(r""" """)
            rpar = myst(r"""\right)""") if len(values) != values.count(1) else myst(r""" """)
            expr += myst(r"""
    &= \py{__latex_without_ones(values, **kwargs)} \py{mult} \py{lpar} \py{__det2x2(A, **kwargs)} \py{rpar} & \\
        """, globals(), locals())
            values.append(A.det())
            final_value = Mul(*values)
            expr += myst(r"""
    &= \py{latex(final_value, **kwargs)} \,.
        """, globals(), locals())
            return expr

        if n <= 1:
            values.append(A[0, 0])
            final_value = Mul(*values)
            expr += myst(r"""\\
    &= \py{__latex_without_ones(values, **kwargs)} \\
    &= \py{latex(final_value, **kwargs)} \,.
    """, globals(), locals())
            return expr

        if A[:, 0].is_zero_matrix:
            expr += myst(r"""\\
    &= 0 \, .
        """)
            return expr

        operations = []
        sign = 1
        column_operations = False # replace row operations by column operations if needed
        if smart:
            nonzero_row = np.count_nonzero(A, axis = 1)
            nonzero_col = np.count_nonzero(A, axis = 0)
            row_min, col_min = min(nonzero_row), min(nonzero_col)
            if row_min < col_min: # The best is a row
                column_operations = True # in this case we perform column operations
                k = np.argmin(nonzero_row)
                j0, indices = __get_coeffs(A[k, :])

                coeff = A[k, j0]
                # scaling if need be
                if coeff != 1:
                    operations.append([1 / coeff, j0 + 1, 0, 0])
                    A[:, j0] /= coeff
                # getting zeros on the row
                for j in indices:
                    if j != j0:
                        operations.append([1, j + 1, -A[k, j], j0 + 1])
                        A[:, j] = A[:, j] - A[k, j] * A[:, j0]
                sign = (-1) ** (k + j0)

            else: # The best is a column
                k = np.argmin(nonzero_col)
                i0, indices = __get_coeffs(A[:, k])

                coeff = A[i0, k]
                # scaling if need be
                if coeff != 1:
                    operations.append([1 / coeff, i0 + 1, 0, 0])
                    A[i0, :] /= coeff
                # getting zeros on the row
                for i in indices:
                    if i != i0:
                        operations.append([1, i + 1, -A[i, k], i0 + 1])
                        A[i, :] = A[i, :] - A[i, k] * A[i0, :]
                sign = (-1) ** (i0 + k)
        else:
            # swapping
            if A[0, 0].is_zero:
                r = np.where(np.ravel(A[:, 0]) != 0)[0][0]
                sign = -1
                A.row_swap(0, r)
                operations.append([0, r + 1, 1, 1])
            coeff = A[0, 0]
            # scaling if need be
            if coeff != 1:
                operations.append([1 / coeff, 1, 0, 0])
                A[0, :] /= coeff
            # getting zeros under the pivot
            for j in range(1, n):
                if A[j, 0] != 0:
                    operations.append([1, j+1, -A[j, 0], 1])
                    A[j, :] = A[j, :] - A[j, 0] * A[0, :]


        minor = A.copy()
        if column_operations: # smart and column operations
            i, j = k, j0
        elif smart: # smart and row operations
            i, j = i0, k
        else: # unsmart
            i, j = 0, 0
        minor.row_del(i)
        minor.col_del(j)

        row_symb = "L" if pxs_lang == "fr" else "R"
        print_ops = pxsl_lines_op(n, operations).replace(row_symb, "C") if column_operations else pxsl_lines_op(n, operations)
        expr += myst(r"""
    &= \py{__latex_without_ones(values + [1 if smart else sign, coeff], **kwargs)} \det \py{pxsl_matrix(A)} & \py{print_ops} \\
    """, globals(), locals())
        values.append(sign * coeff)
        expr += myst(r"""
    &= \py{__latex_without_ones(values, **kwargs)} \det \py{pxsl_matrix(minor)} & \\
        """, globals(), locals())
        return __rec_compute_determinant(minor, smart, expr, values, **kwargs)

    begin = myst(r"""
\begin{equation*}
\begin{align*}
\det \py{pxsl_matrix(A)}
""")
    end = myst(r"""
\end{align*}
\end{equation*}
""")
    return begin + __rec_compute_determinant(A, smart, " ", [], **kwargs) + end


def pxs_expand_determinant(A, rc, k):
    """
    Développe un déterminant selon une ligne ou une colonne, formule de Laplace.

    :pxs_trigger: développer déterminant selon ligne ou colonne, formule de Laplace, cofacteurs signes (-1)^(i+j), écriture pédagogique somme des mineurs
    :pxs_returns: |
        Chaîne LaTeX de l'expression du déterminant développé selon la
        ligne/colonne k au format "Σ (-1)^(i+k)·a_ik·det(M_ik)".
        - rc="r" : développement selon la ligne k (1-based)
        - rc="c" : développement selon la colonne k (1-based)
        Les termes avec a_ik=0 sont omis.
    :pxs_example: |
        A = Matrix([[1, 0, 2], [3, 4, 5], [0, 6, 7]])
        # Développement selon la ligne 1 (contient un 0) :
        # Dans MyST : $\\det A = \\py{pxs_expand_determinant(A, "r", 1)}$
        # → "1·det(...) + 2·det(...)"
    :pxs_antipattern: Écrire la formule de Laplace à la main avec des f-strings — cauchemar pour gérer les signes (-1)^(i+j) et les coefficients ±1 implicites.
    """
    n = A.rows
    A = A.copy() if rc == "r" else A.T
    couples = []
    M = A.copy()
    M.row_del(k - 1)
    for j in range(n):
        if A[k - 1, j]:
            factor = (-1) ** (j + k - 1) * A[k - 1, j]
            minor = M.copy()
            minor.col_del(j)
            if rc == "c":
                minor = minor.T
            symb = Symbol(myst(r"""\det \py{pxsl_matrix(minor)}""", globals(), locals()))
            if factor != 1:
                couples.append((factor, symb))
            else:
                couples.append((symb,))
    addition = Add(*[Mul(*prod, evaluate = False) for prod in couples], evaluate = False)

    return LatexPrinter(dict(order = "none"))._print_Add(addition)