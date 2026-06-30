#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 04 2025

@author: Delphine 
"""


from __future__ import division
import sys
from copy import deepcopy

import src.scripts.Mes_fctions.Mes_fctions_deterministes
from src.scripts.Mes_fctions.Mes_fctions_deterministes import * 

import src.scripts.Mes_fctions.Mes_fctions_generalistes
from src.scripts.Mes_fctions.Mes_fctions_generalistes import * 

import src.scripts.Mes_fctions.Mes_fctions_probabilistes
from src.scripts.Mes_fctions.Mes_fctions_probabilistes import * 

import src.scripts.Mes_fctions.Mes_fctions_d_ecriture_Latex
from src.scripts.Mes_fctions.Mes_fctions_d_ecriture_Latex import * 

import src.scripts.Mes_fctions.Mes_fctions_d_alg_lineaire_bis
from src.scripts.Mes_fctions.Mes_fctions_d_alg_lineaire_bis import * 

from src.scripts.pxs_runtime import myst
from sympy import *
import sympy.stats as stats
import functools as fct
import math as m
import random as rd
import numpy as np

####################### FONCTIONS COPIES A RETIRER DES QUE LE PROBLEME DE DOUBLE APPEL EST REGLE

def pxsl_pow(x, n=1, opt=0, displaystyle=True):
    """
    Fonction permettant d'écrire le nombre x entouré de parenthèses 
    lorsqu'il est négatif ou irrationnel avec deux termes (par ex : 1+sqrt(2) ou 3sqrt(2))
    Ne fonctionne pas pour des valeurs numériques non simplifiées (par ex : 1+3 ou 3*3/2)

    Version
    -------
    13/02/25
    
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

    :pxs_trigger: écriture LaTeX d'une puissance, base potentiellement négative, base fractionnaire Rational, expression composée (Add/Mul), parenthèses conditionnelles autour d'une base, affichage x^n dans un calcul, exposant entier appliqué à un coefficient
    :pxs_returns: |
        str LaTeX rendu via myst() (pour injection \\py{...}).
        Ajoute automatiquement \\left(...\\right) autour de x si x est négatif, Rational non entier, Add ou Mul.
        Sans parenthèses si x est Symbol ou positif. Si n==1, l'exposant n'est pas affiché.
    :pxs_example: |
        a = -3
        expr = pxsl_pow(a, 2)          # -> \\left(-3\\right)^{2}
        expr2 = pxsl_pow(Rational(1,2), 3)  # -> \\left(\\frac{1}{2}\\right)^{3}
        # Injection : myst(r\"\"\"On a \\py{expr}\"\"\", globals(), locals())
    :pxs_antipattern: écrire à la main f"({latex(x)})^{n}" if x < 0 else f"{latex(x)}^{n}" — manque les cas Rational, Add, Mul, Symbol et n==1.
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
            
#################################################################################

def pxs_nvirgzero(x):
   """
   Fr : Fonction qui supprime .0 si le nombre a une valeur entière en le convertissant en int.
   En : Function that removes .0 if the number has an integer value by converting it to int.

   Version 2
   ---------
   13/03/25
   
   Vérification
   ------------
   Auteur : Ronan
   Vérificateurs : Delphine

   Paramètres
   ----------
   x : nombre

   Retour
   ------
   int ou float :
      si le nombre a une valeur entière avec une précision de E-10, il est transformé en int, sinon il n'est pas modifié.

   Fonction utilisée par
   ---------------------
   pxsl_res_num, pxs_simul_law, pxsl_sum_vector

   :pxs_trigger: suppression du .0 terminal, conversion float→int si valeur entière, nettoyage d'affichage numérique avant LaTeX, éviter "3.0" au lieu de "3", tolérance numérique aux erreurs de flottant
   :pxs_returns: |
        int si abs(x - int(x)) < 1e-10 (tolérance), sinon float inchangé.
        Utilisé principalement juste avant latex(...) pour éviter ".0" parasites.
   :pxs_example: |
        a = pxs_nvirgzero(3.0)                 # -> 3 (int)
        b = pxs_nvirgzero(2.00000000000004)    # -> 2 (int, tolérance)
        c = pxs_nvirgzero(0.235)               # -> 0.235 (float, inchangé)
        # Usage typique : myst(r"\\py{latex(pxs_nvirgzero(round(v, 4)))}", ...)
   :pxs_antipattern: `int(x) if x == int(x) else x` — échoue silencieusement sur 2.00000000000004 qui devrait être traité comme 2.
   """   
   
   if m.isclose(x, int(x), abs_tol=1e-10)==True:
      x=int(x)
   return x

# # #############################################################################################################
# # ####                                            Début des essais                                      #######
# # #############################################################################################################

# a=0.23546
# pxs_nvirgzero(a) 
# retourne 0.23546
# b=3.0
# pxs_nvirgzero(b) 
# retourne 3
# c=2.00000000000004
# pxs_nvirgzero(c) 
# retourne 2

# # #############################################################################################################
# # ####                                            Fin des essais                                       ########
# # #############################################################################################################

def pxsl_res_num(x, dec=4, pourc=False, text=False, egal=True, dot = True):
    """
    Fr : Formate un nombre pour l'affichage avec LaTeX, avec gestion d'approximation.
    En : Formats a number for display with LaTeX, with approximation handling.

    Version 2
    ---------
    13/03/25
   
    Vérification
    ------------
    Auteur : Ronan
    Vérificateurs : Delphine

    Arguments:
        x (float/str): Nombre à formater
        dec (int): Nombre de décimales pour l'arrondi (défaut: 4)
        pourc (bool): Si True, affiche également le résultat en pourcentage (défaut: False)
        text (bool): Si True, utilise un format texte plus descriptif (défaut: False)
        egal (bool): Si False, affichera simplement le nombre sans = ou approx devant
    
    Returns:
        str: Formule LaTeX formatée
    
    Fonction utilisée par
    ---------------------
    Aucune fonction pyxiscience

    :pxs_trigger: affichage résultat final d'un calcul probabiliste ou numérique, choix automatique entre "=" et "\\approx" selon exactitude de l'arrondi, conversion en pourcentage avec texte bilingue FR/EN, "soit environ X %"
    :pxs_returns: |
        str LaTeX. Si egal=True : préfixé par " = " (exact) ou " \\approx " (arrondi).
        Si pourc=True : ajoute la version en pourcentage. Si text=True : texte descriptif bilingue "\\fr{environ}\\en{approximately}".
    :pxs_example: |
        p = 7/30
        resultat = pxsl_res_num(p, dec=4, pourc=True)
        # -> " \\approx 0.2333 \\%" en fait " \\approx 23.33 \\%"
        # myst(r"La probabilité vaut \\py{resultat}", globals(), locals())
    :pxs_antipattern: f" = {round(x, 4)}" ou f" \\approx {round(x*100, 2)}\\%" — ne distingue pas exact/approché et ne gère ni le bilinguisme ni le point final.
    """
    # Conversion et arrondi du nombre
    valeur_precise = round(float(x), 10)       # Conversion en float et arrondi à 10 décimales pour précision interne
    valeur_arrondie = round(valeur_precise, dec)   # Arrondi au nombre de décimales demandé
    
    # Vérification si l'arrondi modifie la valeur (pour décider d'utiliser ≈ ou =)
    valeur_precise_int = int(valeur_precise * (10**10))     # Conversion en entier pour comparaison précise
    valeur_arrondie_int = int(valeur_arrondie * (10**10))   # Conversion de la valeur arrondie
    
    # Définition du symbole et format selon que la valeur est exacte ou approximative
    est_exact = (valeur_precise_int == valeur_arrondie_int)
    symbole = "" if egal == False else (" = " if est_exact else " \\approx ")
    
    # Construction de la formule LaTeX selon les paramètres
    if text:
        # Version texte descriptive
        prefixe = "" if est_exact else " \\fr{ environ }\\en{ approximately } "
        
        if pourc:
            # Format pourcentage avec texte explicatif
            texte_pourcentage = ", \\fr{ soit " + ("" if est_exact else "environ ") + "}\\en{that is " + ("" if est_exact else "approximately ") + "} "
            if dot:
                resultat = myst(r"""{0}$\py{{latex(pxs_nvirgzero(round(valeur_precise,dec)))}}${1}$\py{{latex(pxs_nvirgzero(round(100*valeur_precise,dec-2)))}}$ $\%$.""".format(
                prefixe, texte_pourcentage), globals(), locals())
            else:
                resultat = myst(r"""{0}$\py{{latex(pxs_nvirgzero(round(valeur_precise,dec)))}}${1}$\py{{latex(pxs_nvirgzero(round(100*valeur_precise,dec-2)))}}$ $\%$""".format(
                prefixe, texte_pourcentage), globals(), locals())
        else:
            # Format décimal simple
            if dot:
                resultat = myst(r"""{0}$\py{{latex(pxs_nvirgzero(round(valeur_precise,dec)))}}$.""".format(prefixe), globals(), locals())
            else:
                resultat = myst(r"""{0}$\py{{latex(pxs_nvirgzero(round(valeur_precise,dec)))}}$""".format(prefixe), globals(), locals())
    else:
        # Version concise avec symbole mathématique
        if pourc:
            # Format pourcentage
            resultat = myst(r"""{0}\py{{latex(pxs_nvirgzero(round(100*valeur_precise,dec-2)))}} \%""".format(symbole), globals(), locals())
        else:
            # Format décimal simple
            resultat = myst(r"""{0}\py{{latex(pxs_nvirgzero(round(valeur_precise,dec)))}}""".format(symbole), globals(), locals())
    
    return resultat

# # #############################################################################################################
# # ####                                            Début des essais                                      #######
# # #############################################################################################################

# a=0.2354
# b=pxsl_res_num(a,dec=4,pourc=False,text=False) 
# retourne "=0.2354"
# c=pxsl_res_num(a,dec=4,pourc=True,text=False) 
# retourne "=23.45%"
# d=pxsl_res_num(a,dec=4,pourc=False,text=True) 
# retourne "0.2354." centré
# e=pxsl_res_num(a,dec=4,pourc=True,text=True) 
# retourne "est 0.2354, soit 23.54%"
# f=0.2354278
# g=pxsl_res_num(f,dec=4,pourc=False,text=False) 
# retourne "\approx 0.2354"
# h=pxsl_res_num(f,dec=4,pourc=True,text=False) 
# retourne "\approx 23.54%"
# i=pxsl_res_num(f,dec=4,pourc=False,text=True) 
# retourne "est environ 0.2354"
# j=pxsl_res_num(f,dec=4,pourc=True,text=True) 
# retourne "est environ 0.2354, soit environ 23.54%"

# # #############################################################################################################
# # ####                                            Fin des essais                                       ########
# # #############################################################################################################

def pxsl_scalar_product(a, b, prod="times",displaystyle=True):
    """
    Fr : Fonction permettant d'écrire le calcul du produit scalaire entre les deux vecteurs a et b. 
    En : Function to calculate the dot product between two vectors a and b.

    Version 1
    ---------
    02/03/25
    
    Vérification
    ------------
    Auteur : Ronan
    Vérificateurs : Delphine
    
    Paramètres
    ----------
    a : liste
        Premier vecteur du produit
    b : liste
        Deuxième vecteur du produit 
    prod : str
        times : le symbole produit est \times
        dot : le symbole produit est \cdot
        
    Retour
    ------
    str
        retourne l'expression en latex
    
    Fonction utilisée par
    ---------------------
    Aucune fonction pyxiscience

    :pxs_trigger: produit scalaire de deux vecteurs, somme de produits terme à terme a1×b1+a2×b2+..., calcul détaillé en LaTeX avec \\times ou \\cdot, développement de <u,v> pour exercice de géométrie ou probabilités
    :pxs_returns: |
        str LaTeX de la forme "a1 \\times b1 + a2 \\times b2 + ... + an \\times bn".
        Chaque terme passe par pxsl_pow donc parenthèses auto sur nombres négatifs/Rational.
        Retourne un message d'erreur LaTeX si listes vides ou tailles différentes.
    :pxs_example: |
        u = [Rational(1,2), 2]
        v = [3, 4]
        calcul = pxsl_scalar_product(u, v, prod="times")
        # -> "\\frac{1}{2}\\times 3 + 2\\times 4"
        # myst(r"\\langle u,v\\rangle = \\py{calcul}", globals(), locals())
    :pxs_antipattern: " + ".join(f"{ai}\\times {bi}" for ai, bi in zip(a, b)) — casse sur négatifs (signe perdu) et fractions (pas de displaystyle).
    """
    # Vérification si une des listes est vide
    if len(a) == 0 or len(b) == 0:
        return myst(r""" \textrm{Attention liste vide}""")
    
    # Vérification si les listes sont de tailles différentes
    if len(a) != len(b):
        return myst(r"""\textrm{Attention les deux listes ne sont pas de la même taille}""")
    
    # Détermination de la taille des vecteurs
    taille_vecteur = len(a)
    dernier_index = taille_vecteur - 1
    
    # Initialisation de la chaîne résultat
    resultat = myst(r""" """)
    
    # Détermination du symbole de produit à utiliser
    symbole_produit = r"""\times""" if prod == "times" else r"""\cdot"""
    
    # Construction de l'expression du produit scalaire terme à terme
    for i in range(dernier_index):
        # Ajout de chaque terme sauf le dernier, suivi du symbole +
        resultat = resultat + pxsl_pow(a[i],displaystyle=displaystyle) + myst(symbole_produit) + pxsl_pow(b[i],displaystyle=displaystyle) + myst(r"""+ """)
    
    # Ajout du dernier terme (sans symbole + à la fin)
    resultat = resultat + pxsl_pow(a[dernier_index],displaystyle=displaystyle) + myst(f" {symbole_produit}") + pxsl_pow(b[dernier_index],displaystyle=displaystyle)
    
    return resultat

# # #############################################################################################################
# # ####                                            Début des essais                                      #######
# # #############################################################################################################

# pxsl_scalar_product([1, 2], [3, 4], prod="times")
# renvoie la forme latex de 1x3+2x4
# pxsl_scalar_product([5, 6, 7], [8, 9, 10], prod="dot")
# renvoie la forme latex de 5.8+6.9+7.10
# pxsl_scalar_product([Rational(1,2), 2], [3, 4])
# renvoie la forme latex de 1/2x3+2x4 avec displaystyle actif
# pxsl_scalar_product([Rational(1,2), 2], [3, 4],displaystyle=False)
# renvoie la forme latex de 1/2x3+2x4 avec displaystyle inactif
# pxsl_scalar_product([], [])
# renvoie un message indiquant qu'une des listes est vide
# pxsl_scalar_product([5], [10])
# renvoie la forme latex de 5x10
# pxsl_scalar_product([5,2], [10])
# renvoie un message indiquant que les listes ne sont pas de la même taille

# # #############################################################################################################
# # ####                                            Fin des essais                                       ########
# # #############################################################################################################

def pxsl_moment(X, n=1, prod="times",displaystyle=True):
    """
    Fr : Fonction permettant d'écrire le calcul du moment d'ordre n de la variable aléatoire finie X.
    En : Function to calculate the nth order moment of the finite random variable X.

    Version 1
    ---------
    02/03/25
    
    Vérification
    ------------
    Auteur : Ronan
    Vérificateurs : Delphine
    
    Paramètres
    ----------
    X : variable aléatoire finie
    
    n : int
        Ordre du moment
    
    prod : str
        times : le symbole produit est \times
        dot : le symbole produit est \cdot
    
    Retour
    ------
    str
        retourne l'expression en latex

    Fonction utilisée par
    ---------------------
    Aucune fonction pyxiscience

    :pxs_trigger: calcul détaillé espérance E(X) ou E(X^n) d'une variable aléatoire finie sympy, moment d'ordre n, écriture développée Σ x_i^n × P(X=x_i), exercice "calculer E(X)" ou "calculer la variance" avec étape détaillée
    :pxs_returns: |
        str LaTeX de la forme "x1^n \\times p1 + x2^n \\times p2 + ... + xk^n \\times pk".
        Valeurs triées par clé croissante. pxsl_pow gère les parenthèses autour de valeurs négatives et des Rational.
    :pxs_example: |
        X = stats.FiniteRV('X', {-1: Rational(1,4), 0: Rational(1,2), 1: Rational(1,4)})
        calcul_esp = pxsl_moment(X, n=1)      # pour E(X)
        calcul_var = pxsl_moment(X, n=2)      # pour E(X^2)
        # myst(r"E(X) = \\py{calcul_esp}", globals(), locals())
    :pxs_antipattern: boucler manuellement `density(X).dict.items()` et concaténer `f"{k}^{n} * {v} + "` — rate le tri, les parenthèses sur négatifs et le displaystyle des fractions.
    """
    # Récupération et tri des éléments de la variable aléatoire
    loi_proba = stats.density(X).dict
    loi_proba_triee = dict(sorted(loi_proba.items()))
    valeurs = list(loi_proba_triee.keys())
    probabilites = list(loi_proba_triee.values())
    
    # Vérification si la distribution est vide
    if len(valeurs) == 0:
        return myst(r""" Attention distribution vide""")
    
    # Détermination du symbole de produit à utiliser
    symbole_produit = r"""\times""" if prod == "times" else r"""\cdot"""
    
    # Initialisation du résultat
    resultat = myst(r""" """)
    
    # Construction de l'expression du moment terme à terme
    dernier_index = len(valeurs) - 1
    
    # Ajout de tous les termes sauf le dernier
    for i in range(dernier_index):
        resultat = resultat + pxsl_pow(valeurs[i], n,displaystyle=displaystyle) + myst(symbole_produit) + pxsl_pow(probabilites[i],displaystyle=displaystyle) + myst(r"""+ """)
    
    # Ajout du dernier terme (sans symbole + à la fin)
    resultat = resultat + pxsl_pow(valeurs[dernier_index], n,displaystyle=displaystyle) + myst(f" {symbole_produit}") + pxsl_pow(probabilites[dernier_index],displaystyle=displaystyle)
    
    return resultat

# # #############################################################################################################
# # ####                                            Début des essais                                      #######
# # #############################################################################################################

# Calcul du moment d'ordre 1 d'une loi de Bernouilli
# X = stats.FiniteRV('X', {0: 0.3, 1: 0.7})
# pxsl_moment(X, n=1, prod="times")
# renvoie l'expression latex de 0 x 0.3 + 1 x 0.7

# Calcul du moment d'ordre 2 pour un dé à 6 faces displaystyle actif
# Y = stats.FiniteRV('Y', {1: Rational(1,6), 2: Rational(1,6), 3: Rational(1,6), 4: Rational(1,6), 5: Rational(1,6), 6: Rational(1,6)})
# pxsl_moment(Y, n=2, prod="dot")
# renvoie l'expression latex de 1^2.1/6+2^2.1/6+3^2.1/6+4^2.1/6+5^2.1/6+6^2.1/6 les fractions étant écrite en displaystyle

# Calcul du moment d'ordre 2 pour un dé à 6 faces, displaystyle inactif
# Z = stats.FiniteRV('Z', {1: Rational(1,6), 2: Rational(1,6), 3: Rational(1,6), 4: Rational(1,6), 5: Rational(1,6), 6: Rational(1,6)})
# pxsl_moment(Z, n=2, prod="dot",displaystyle=False)
# même résultat que pour Y mais sans le format displaystyle

# Loi simple - moment d'ordre 3
# W = stats.FiniteRV('W', {-1: 0.25, 0: 0.5, 1: 0.25})
# pxsl_moment(W, n=3, prod="times")
# renvoie l'expression latex de (-1)^3 x 0.25+0^3 x 0.5 + 1^3 x 0.25

# # #############################################################################################################
# # ####                                            Fin des essais                                       ########
# # #############################################################################################################

def pxsl_law(textx, textprob, X, frac="", nzero=True):
    """
    Fr : Fonction permettant d'écrire le tableau de loi d'une variable aléatoire X finie.
    En : Function to write the probability distribution table of a finite random variable X.

    Version 1
    ---------
    02/03/25
    
    Vérification
    ------------
    Auteur : Ronan
    Vérificateurs : Delphine
    
    Paramètres
    ----------
    textx : str
        Entrée de la première ligne du tableau de loi (valeurs possibles)
        Peut contenir du LaTeX directement (sans échappement)
    
    textprob : str
        Entrée de la deuxième ligne du tableau de loi (probabilités)
        Peut contenir du LaTeX directement (sans échappement)
    
    X : variable aléatoire finie
        Variable aléatoire dont on veut afficher la loi
    
    frac : str, optional
        "/" : les fractions sont représentées avec / (notation simple)
        "" : les fractions sont représentées avec la commande \frac{}{} (défaut)
    
    nzero : boolean, optional
        True : les probabilités nulles ne sont pas représentées (défaut)
        False : les probabilités nulles sont représentées
    
    Retour
    ------
    str
        Retourne un tableau LaTeX contenant la loi de probabilité

    Fonction utilisée par
    ---------------------
    Aucune fonction pyxiscience

    :pxs_trigger: tableau de loi d'une variable aléatoire discrète finie, ligne x_i + ligne P(X=x_i), représenter la distribution d'une VA dans un énoncé ou une correction, table à 2 lignes valeurs/probabilités avec entêtes LaTeX personnalisées
    :pxs_returns: |
        str LaTeX d'un \\begin{array}{...} à 2 lignes (valeurs, probabilités) avec séparateurs verticaux.
        Les fractions sont rendues en \\displaystyle par défaut. Les probabilités nulles sont masquées si nzero=True.
    :pxs_example: |
        X = stats.FiniteRV('X', {1: Rational(1,6), 2: Rational(1,6), 3: Rational(1,6),
                                 4: Rational(1,6), 5: Rational(1,6), 6: Rational(1,6)})
        tableau = pxsl_law("x_i", "P(X=x_i)", X)
        # myst(r"La loi de X est donnée par : \\py{tableau}", globals(), locals())
    :pxs_antipattern: construire à la main `\\begin{array}{|c|c|c|}` avec une boucle sur `density(X).dict.items()` et `latex(v)` — duplique la logique de tri, de gestion des zéros et du displaystyle.
    """
    # Récupération et tri des éléments de la variable aléatoire
    loi_proba = stats.density(X).dict
    loi_proba_triee = dict(sorted(loi_proba.items()))
    
    # Filtrage des probabilités nulles si demandé
    if nzero:
        loi_proba_triee = {k: v for k, v in loi_proba_triee.items() if v != 0}
    
    # Extraction des valeurs et probabilités
    valeurs = list(loi_proba_triee.keys())
    probabilites = list(loi_proba_triee.values())
    nb_valeurs = len(valeurs)
    
    # Configuration du tableau LaTeX
    largeur_colonnes = 'ccc|' * (nb_valeurs + 1)
    ligne_vide = '&' * (nb_valeurs * 3 + 2)
    
    # Début du tableau
    resultat = myst(r""" \begin{array}{|\py{largeur_colonnes}} \hline """, globals(), locals())
    
    # Construction de la première ligne (valeurs possibles) - Les en-têtes sont passés tels quels
    resultat = resultat + myst(r""" \py{ligne_vide} \\""", globals(), locals())
    resultat = resultat + myst(r""" & \py{textx} & """, globals(), locals())
    
    for i in range(nb_valeurs):
        if frac == "/":
            # Affichage simple sans utiliser \frac
            resultat = resultat + myst(r"""& & \py{valeurs[i]} & """, globals(), locals())
        else:
            # Affichage avec \displaystyle pour les fractions
            resultat = resultat + myst(r"""& & \displaystyle \py{latex(valeurs[i])} & """, globals(), locals())
    
    resultat = resultat + myst(r"""\\ """)
    resultat = resultat + myst(r""" \py{ligne_vide} \\""", globals(), locals())
    resultat = resultat + myst(r"""\hline """)
    
    # Construction de la deuxième ligne (probabilités)
    resultat = resultat + myst(r""" \py{ligne_vide} \\""", globals(), locals())
    resultat = resultat + myst(r""" & \py{textprob} & """, globals(), locals())
    
    for i in range(nb_valeurs):
        if frac == "/":
            # Affichage simple des probabilités
            resultat = resultat + myst(r"""& & \py{probabilites[i]} &""", globals(), locals())
        else:
            # Affichage des probabilités avec \displaystyle pour les fractions
            resultat = resultat + myst(r"""& & \displaystyle \py{latex(probabilites[i])} &""", globals(), locals())
    
    resultat = resultat + myst(r"""\\ """)
    resultat = resultat + myst(r""" \py{ligne_vide} \\""", globals(), locals())
    
    # Fin du tableau
    resultat = resultat + myst(r"""\hline """)
    resultat = resultat + myst(r"""\end{array}""")
    
    return resultat

# # #############################################################################################################
# # ####                                            Début des essais                                      #######
# # #############################################################################################################

# Affichage entête simple
# X = stats.FiniteRV('X', {0: 0.3, 1: 0.7})
# pxsl_law("x", "P(X=x)", X)
# renvoie un tableau 2 lignes, 3 colonnes
#    |   x  | 0 | 1 |
#    |P(X=x)|0.3|0.7|

# Affichage entête mathématique
# X2 = stats.FiniteRV('X2', {1: Rational(1,6), 2: Rational(1,6), 3: Rational(1,6), 4: Rational(1,6), 5: Rational(1,6), 6: Rational(1,6)})
# pxsl_law("y", "P(Y=y)", X2)
# renvoie un tableau 2 lignes, 7 colonnes (fractions écrites en displaystyle)
#    |   y  | 1 | 2 | 3 | 4 | 5 | 6 |
#    |P(Y=y)|1/6|1/6|1/6|1/6|1/6|1/6|

# Choix d'affichage des zéros
# Z = stats.FiniteRV('Z', {1: 0.2, 2: 0, 3: 0.5, 4: 0, 5: 0.3})
# Sans les zéros
# pxsl_law("z", "P(Z=z)", Z)
# renvoie un tableau 2 lignes, 4 colonnes
#    |   z  | 1 | 3 | 5 | 
#    |P(Z=z)|0.2|0.5|0.3|
# Avec les zéros
# pxsl_law("z", "P(Z=z)", Z, nzero=False)
# renvoie un tableau 2 lignes, 6 colonnes
#    |   z  | 1 | 2 | 3 | 4 | 5 | 
#    |P(Z=z)|0.2| 0 |0.5| 0 |0.3|

# Variable avec valeur fractionnaire 
# W = stats.FiniteRV('W', {Rational(1, 3): 0.25, Rational(2, 3): 0.25, 1: 0.5})
# pxsl_law("z", "P(Z=z)", W)
# renvoie un tableau 2 lignes, 4 colonnes, les fractions sont en displaystyle
#    |   z  |1/3 |2/3 | 1 |
#    |P(Z=z)|0.25|0.25|0.5|

# Affichage entête personnalisée
# stats.FiniteRV('Z', {1: 0.4, 2: 0.6})
# pxsl_law(r"\text{Valeur} ~ z", r"\text{Probabilité} ~ P(Z=z)", Z)
# renvoie un tableau 2 lignes, 3 colonnes
#    |     Valeur z     | 1 | 2 |
#    |Probabilité P(Z=z)|0.4|0.6|
# stats.FiniteRV('W', {10: 0.25, 20: 0.25, 30: 0.5})
# pxsl_law("w", "P_W(w)", W)
# renvoie un tableau 2 lignes, 4 colonnes (le P_W(w) est interprêté en latex)
#    |  w   | 10 | 20 | 30 |
#    |P_W(w)|0.25|0.25|0.5 |

# # #############################################################################################################
# # ####                                            Fin des essais                                       ########
# # #############################################################################################################

def pxs_simul_law(n, type_proba="dec", prec=0.01, nzero=True):
    """
    Fr : Fonction permettant de simuler une loi de probabilité discrète de taille n.
    En : Function to simulate a discrete probability distribution of size n.

    Version 1
    ---------
    02/03/25
    
    Vérification
    ------------
    Auteur : Ronan
    Vérificateurs : Delphine
    
    Paramètres:
    -----------
    n : int
        Nombre de valeurs possibles de la loi
    
    type_proba : str
        Format des probabilités générées
        - "dec" : nombres décimaux (entre 0 et 1)
        - "perc" : pourcentages (entre 0 et 100)
        - "frac" : fractions
    
    prec : float ou int
        - Si type=="dec" ou "perc" : les probabilités seront des multiples de prec
        - Si type=="frac" : prec est un entier, les probabilités seront des multiples de 1/prec
    
    nzero : bool
        - True : les probabilités seront non nulles si possible
        - False : les probabilités peuvent être nulles
    
    Retour:
    -------
    list
        Liste des probabilités (la somme vaut 1 ou 100 selon le type)

    Fonction utilisée par
    ---------------------
    Aucune fonction pyxiscience

    :pxs_trigger: génération aléatoire des probabilités d'un énoncé probabiliste, simulation d'une loi discrète dont la somme vaut exactement 1 (ou 100%), création de données pour exercices variabilisés, choix décimal/pourcentage/fraction avec précision contrôlée
    :pxs_returns: |
        list de longueur n. Somme exacte = 1 (dec), 100 (perc) ou 1 (frac).
        En mode "frac" : liste de sympy.Rational avec dénominateur prec. Ordre aléatoire (shuffle final).
        Avec nzero=True : toutes les entrées sont > 0 si faisable.
    :pxs_example: |
        probas = pxs_simul_law(4, type_proba="frac", prec=12)
        # ex: [Rational(1,2), Rational(1,3), Rational(1,12), Rational(1,12)]
        X = pxs_finiterv('X', [5, 10, 15, 20], probas)
        tableau = pxsl_law("x_i", "P(X=x_i)", X)
    :pxs_antipattern: `probas = [random.random() for _ in range(n)]; probas = [p/sum(probas) for p in probas]` — pas de précision contrôlée, ne garantit pas la somme exacte après arrondi, pas de support Rational.
    """
    
    resultat = []
    
    # Cas des pourcentages (entre 0 et 100)
    if type_proba == "perc":
        total_restant = 100
        compteur = 1
        probas_temp = []
        precision_log = m.floor(m.log10(prec))
        valeur = rd.randint(0, int(round(total_restant/(2*prec)))) * prec
        if precision_log < 0:
            valeur = round(valeur, -precision_log)
        probas_temp.append(pxs_nvirgzero(valeur))
        
        while compteur < (n-1):
            total_restant = 100 - sum(probas_temp)
            valeur = rd.randint(0, int(round(total_restant/(2*prec)))) * prec
            if precision_log < 0:
                valeur = round(valeur, -precision_log)
            probas_temp.append(pxs_nvirgzero(valeur))
            compteur += 1
            
        valeur = 100 - sum(probas_temp)
        if precision_log < 0:
            valeur = round(valeur, -precision_log)
        probas_temp.append(pxs_nvirgzero(valeur))
        
        # Si on veut des valeurs non nulles et que c'est possible
        if nzero == True and prec*(n-1) < 100:
            produit = 1
            taille = len(probas_temp)
            for i in range(taille):
                produit *= probas_temp[i]
                
            while produit == 0:  # S'il y a au moins un zéro
                total_restant = 100
                compteur = 1
                probas_temp = []
                precision_log = m.floor(m.log10(prec))
                valeur = rd.randint(0, int(round(total_restant/(2*prec)))) * prec
                if precision_log < 0:
                    valeur = round(valeur, -precision_log)
                probas_temp.append(pxs_nvirgzero(valeur))
                
                while compteur < (n-1):
                    total_restant = 100 - sum(probas_temp)
                    valeur = rd.randint(0, int(round(total_restant/(2*prec)))) * prec
                    if precision_log < 0:
                        valeur = round(valeur, -precision_log)
                    probas_temp.append(pxs_nvirgzero(valeur))
                    compteur += 1
                    
                valeur = 100 - sum(probas_temp)
                if precision_log < 0:
                    valeur = round(valeur, -precision_log)
                probas_temp.append(pxs_nvirgzero(valeur))
                
                # Recalculer le produit
                produit = 1
                for i in range(taille):
                    produit *= probas_temp[i]
        
        resultat = probas_temp

    # Cas des décimaux (entre 0 et 1)
    elif type_proba == "dec":
        total_restant = 1
        compteur = 1
        probas_temp = []
        precision_log = m.floor(m.log10(prec))
        valeur = rd.randint(0, int(round(total_restant/(2*prec)))) * prec
        if precision_log < 0:
            valeur = round(valeur, -precision_log)
        probas_temp.append(pxs_nvirgzero(valeur))
        
        while compteur < (n-1):
            total_restant = 1 - sum(probas_temp)
            valeur = rd.randint(0, int(round(total_restant/(2*prec)))) * prec
            if precision_log < 0:
                valeur = round(valeur, -precision_log)
            probas_temp.append(pxs_nvirgzero(valeur))
            compteur += 1
            
        valeur = 1 - sum(probas_temp)
        if precision_log < 0:
            valeur = round(valeur, -precision_log)
        probas_temp.append(pxs_nvirgzero(valeur))
        
        # Si on veut des valeurs non nulles et que c'est possible
        if nzero == True and prec*(n-1) < 1:
            produit = 1
            taille = len(probas_temp)
            for i in range(taille):
                produit *= probas_temp[i]
                
            while produit == 0:  # S'il y a au moins un zéro
                total_restant = 1
                compteur = 1
                probas_temp = []
                precision_log = m.floor(m.log10(prec))
                valeur = rd.randint(0, int(round(total_restant/(2*prec)))) * prec
                if precision_log < 0:
                    valeur = round(valeur, -precision_log)
                probas_temp.append(pxs_nvirgzero(valeur))
                
                while compteur < (n-1):
                    total_restant = 1 - sum(probas_temp)
                    valeur = rd.randint(0, int(round(total_restant/(2*prec)))) * prec
                    if precision_log < 0:
                        valeur = round(valeur, -precision_log)
                    probas_temp.append(pxs_nvirgzero(valeur))
                    compteur += 1
                    
                valeur = 1 - sum(probas_temp)
                if precision_log < 0:
                    valeur = round(valeur, -precision_log)
                probas_temp.append(pxs_nvirgzero(valeur))
                
                # Recalculer le produit
                produit = 1
                for i in range(len(probas_temp)):
                    produit *= probas_temp[i]
        
        resultat = probas_temp

    # Cas des fractions
    elif type_proba == "frac":
        total_restant = prec
        compteur = 1
        probas_temp = []
        probas_temp.append(Rational(rd.randint(0, int(round(total_restant/2))), prec))
        
        while compteur < (n-1):
            total_restant = int(prec - sum(probas_temp)*prec)
            probas_temp.append(Rational(rd.randint(0, int(round(total_restant/2))), prec))
            compteur += 1
            
        probas_temp.append(Rational(prec - sum(probas_temp*prec), prec))
        
        # Si on veut des valeurs non nulles et que c'est possible
        if nzero == True and n <= prec:
            produit = 1
            taille = len(probas_temp)
            for i in range(taille):
                produit *= probas_temp[i]
                
            while produit == 0:  # S'il y a au moins un zéro
                total_restant = prec
                compteur = 1
                probas_temp = []
                probas_temp.append(Rational(rd.randint(0, int(round(total_restant/2))), prec))
                
                while compteur < (n-1):
                    total_restant = int(prec - sum(probas_temp)*prec)
                    probas_temp.append(Rational(rd.randint(0, int(round(total_restant/2))), prec))
                    compteur += 1
                    
                probas_temp.append(Rational(prec - sum(probas_temp*prec), prec))
                
                # Recalculer le produit
                produit = 1
                for i in range(len(probas_temp)):
                    produit *= probas_temp[i]
        
        resultat = probas_temp

    # Mélange des probabilités pour avoir un ordre aléatoire
    rd.shuffle(resultat)
    return resultat

# # #############################################################################################################
# # ####                                            Début des essais                                      #######
# # #############################################################################################################

# 1. Test avec type "dec" (décimal, valeur par défaut)
# Test avec paramètres par défaut
# pxs_simul_law(n=5)
# renvoie par exemple la liste [0.2,0.04,0.47,0.23,0.06]

# Test avec une précision différente
# pxs_simul_law(n=4, prec=0.05)
# renvoie par exemple la liste [0.4,0.3,0.25,0.05]

# Test avec sans_zero=False
# pxs_simul_law(n=6, nzero=False)
# renvoie par exemple la liste [0.45,0.19,0.09,0.17,0.1,0]

# Test avec un grand nombre de valeurs
# pxs_simul_law(n=10, prec=0.001)
# renvoie par exemple la liste [0.012,0.191,0.134,0.187,0.05,0.046,0.078,0.043,0.024,0.235]

# 2. Test avec type "perc" (pourcentage)
# pxs_simul_law(n=4, type_proba="perc", prec=0.5)
# renvoie par exemple la liste [1.5,43.5,47,8]

# 3. Test avec type "frac" (fraction)
# pxs_simul_law(n=4, type_proba="frac", prec=12)
# renvoie par exemple la liste [1/2,1/3,1/12,1/12]

# # #############################################################################################################
# # ####                                            Fin des essais                                       ########
# # #############################################################################################################

def pxs_fct_finiterv(f, X):
    """
    Fr : Transforme une variable aléatoire finie X via une fonction f.
    Cette fonction crée une nouvelle variable aléatoire Y = f(X) en appliquant
    la fonction f à chaque valeur possible de X et en adaptant les probabilités.
    En : Transforms a finite random variable X using a function f.
    This function creates a new random variable Y = f(X) by applying 
    the function f to each possible value of X and adapting the probabilities accordingly.
    
    Version 1
    ---------
    02/03/25
    
    Vérification
    ------------
    Auteur : Ronan
    Vérificateurs : Delphine

    Paramètres
    ----------
    f : function
        Fonction à appliquer à la variable aléatoire X
    X : RandomSymbol
        Variable aléatoire finie source
    
    Retour
    ------
    RandomSymbol
        Variable aléatoire finie Y = f(X)

    Fonction utilisée par
    ---------------------
    Aucune fonction pyxiscience

    :pxs_trigger: création de Y=f(X) à partir d'une VA finie X (Y=X², Y=|X|, Y=floor(X), Y=1_{X>a}), calcul de la loi de image d'une VA, agrégation automatique des probabilités quand f n'est pas injective
    :pxs_returns: |
        stats.FiniteRV nommé "Y" : nouvelle variable aléatoire finie sympy avec pour support {f(x): sum_{k:f(k)=f(x)} P(X=k)}.
        Prêt à être passé à pxsl_law, pxsl_moment, stats.E(), stats.variance()...
    :pxs_example: |
        X = stats.FiniteRV('X', {-2: 0.25, -1: 0.25, 1: 0.25, 2: 0.25})
        Y = pxs_fct_finiterv(lambda x: x**2, X)   # Y=X², support {1: 0.5, 4: 0.5}
        tableau_Y = pxsl_law("y_i", "P(Y=y_i)", Y)
        # myst(r"Loi de Y=X^2 : \\py{tableau_Y}", globals(), locals())
    :pxs_antipattern: `{f(k): v for k, v in density(X).dict.items()}` — écrase les probabilités quand f non injective (ex : f(-1)=f(1)=1) au lieu de les sommer.
    """
    
    # Initialisation du nouveau dictionnaire de probabilités
    dico = {}
    
    # Pour chaque valeur possible de X et sa probabilité associée
    for key, value in density(X).dict.items():
        # Appliquer f à la valeur
        newkey = f(key)
        
        # Si la valeur transformée existe déjà, on ajoute la probabilité
        # (cas où plusieurs valeurs de X donnent la même valeur après transformation)
        if newkey in dico:
            dico[newkey] = dico[newkey] + value
        else:
            dico[newkey] = value
    
    # Création du nom de la nouvelle variable aléatoire
    Name = "Y"
    
    # Création de la nouvelle variable aléatoire
    Y = stats.FiniteRV(Name, dico)
    
    return Y

# # #############################################################################################################
# # ####                                            Début des essais                                      #######
# # #############################################################################################################

# Définir une pièce biaisée (70% face, 30% pile)
# piece_biaisee = stats.FiniteRV('piece_biaisee', {0: 0.3, 1: 0.7})

# Définir une variable discrète représentant le nombre d'enfants dans une famille
# nb_enfants = stats.FiniteRV('nb_enfants', {0: 0.1, 1: 0.3, 2: 0.4, 3: 0.15, 4: 0.05})

# Cas 1: Fonction définie directement (lambda x: x**2)
# pxs_fct_finiterv(lambda x: x**2, X2)
# renvoie stats.FiniteRV('Y',{1: Rational(1,6), 4: Rational(1,6), 9: Rational(1,6), 16: Rational(1,6), 25: Rational(1,6), 36: Rational(1,6)})

# Cas 2: Fonctions mathématiques standard
# pxs_fct_finiterv(exp, X2)
# renvoie stats.FiniteRV('Y',{e: Rational(1,6), e^2: Rational(1,6), e^3: Rational(1,6), e^4: Rational(1,6), e^5: Rational(1,6), e^6: Rational(1,6)})
# pxs_fct_finiterv(sqrt, X2)
# renvoie stats.FiniteRV('Y',{1: Rational(1,6), sqrt(2): Rational(1,6), sqrt(3): Rational(1,6), 2: Rational(1,6), sqrt(5): Rational(1,6), sqrt(6): Rational(1,6)})

# Cas 3: Fonctions de partie entière
# notes = stats.FiniteRV('notes', {8.5: 0.05, 8.7: 0.1, 11.3: 0.15, 11.6: 0.2,14.9: 0.15, 15.5: 0.2, 17.8: 0.15})
# pxs_fct_finiterv(floor, notes)
# renvoie stats.FiniteRV('Y',{8: 0.15, 11: 0.35, 14: 0.15, 15: 0.2, 17: 0.15})
# pxs_fct_finiterv(ceiling, notes)
# renvoie stats.FiniteRV('Y',{9: 0.15, 12: 0.35, 15: 0.15, 16: 0.2, 18: 0.15})

# Cas 4: Fonctions indicatrices
# nb_enfants = stats.FiniteRV('nb_enfants', {0: 0.1, 1: 0.3, 2: 0.4, 3: 0.15, 4: 0.05})
# Indicatrice (x > 2)
# pxs_fct_finiterv(lambda x: 1 if x > 2 else 0, nb_enfants)
# renvoie stats.FiniteRV('Y',{0: 0.8, 1: 0.2})
# Indicatrice (x est pair)
# pxs_fct_finiterv(lambda x: 1 if x % 2 == 0 else 0, nb_enfants)
# renvoie stats.FiniteRV('Y',{0: 0.45, 1: 0.55})

# # #############################################################################################################
# # ####                                            Fin des essais                                       ########
# # #############################################################################################################

def pxsl_sum_vector(x):
   """
    Fr : Fonction permettant d'écrire la somme des éléments du vecteur x
    En: Function to calculate the sum of elements in vector x

    Version
    -------
    02/03/25
    
    Vérification
    ------
    Auteur : Ronan
    Vérificateurs : Delphine

    Paramètres
    ----------
    x : liste

    Retour
    ------
    str
        retourne la somme de la liste de x

    Fonction utilisée par
    ---------------------
    Aucune fonction pyxiscience

    :pxs_trigger: affichage LaTeX d'une somme d'entiers/décimaux signés, écriture "a - b + c" avec gestion automatique des signes + et -, détail du calcul d'une somme algébrique d'une liste, linéarisation d'un résultat (ex : total d'une série)
    :pxs_returns: |
        str LaTeX. Premier terme : "-v" si négatif, "v" sinon (pas de "+" initial).
        Termes suivants : " -|v|" si négatif, " +v" si positif. Passe par pxs_nvirgzero pour nettoyer les .0.
    :pxs_example: |
        valeurs = [2, -1, 3, -4]
        somme_latex = pxsl_sum_vector(valeurs)        # -> "2 -1 +3 -4"
        # myst(r"S = \\py{somme_latex} = \\py{sum(valeurs)}", globals(), locals())
    :pxs_antipattern: `" + ".join(str(v) for v in liste)` qui produit "2 + -1 + 3 + -4" (double opérateur laid) au lieu de "2 - 1 + 3 - 4".
   """
   s=len(x)
   if x[0]<0:
      d=myst(r""" -\py{latex(pxs_nvirgzero(abs(x[0])))}""",globals(),locals())
   else:
      d=myst(r"""\py{latex(pxs_nvirgzero(x[0]))}""",globals(),locals())
   for i in range(1,s):
      if x[i]<0:
         d=d+myst(r""" -\py{latex(pxs_nvirgzero(abs(x[i])))}""",globals(),locals())
      else:
         d=d+myst(r""" +\py{latex(pxs_nvirgzero(x[i]))}""",globals(),locals())
   return d

# # #############################################################################################################
# # ####                                            Début des essais                                      #######
# # #############################################################################################################

# a=[2,-1]
# pxsl_sum_vector(a) 
# retourne l'écriture latex de la somme des éléments de a : 2 - 1
# b=[-2,-1,3]
# pxsl_sum_vector(b) 
# retourne l'écriture latex de la somme des éléments de b : - 2 - 1 + 3

# # #############################################################################################################
# # ####                                            Fin des essais                                       ########
# # #############################################################################################################

def pxs_finiterv(x,val,prob):
   """
    Fr : Fonction permettant de créer la variables aléatoire x dont les valeurs sont val et les probabilités associées sont prob.
    En: Function to create the random variable x whose values are val and the associated probabilities are prob.
    
    Version
    -------
    02/03/25
    
    Vérification
    ------------
    Auteur : Ronan
    Vérificateurs : Delphine

    Paramètres
    ----------
    x : liste

    Retour
    ------
    variable aléatoire

    Fonction utilisée par
    ---------------------
    Aucune fonction pyxiscience

    :pxs_trigger: création d'une VA finie sympy à partir de deux listes parallèles valeurs/probabilités, raccourci de stats.FiniteRV quand on a déjà val et prob séparés (souvent issus de pxs_simul_law), instanciation rapide d'une loi discrète
    :pxs_returns: |
        stats.FiniteRV (RandomSymbol sympy) nommé x, de support dict(zip(val, prob)).
        Prêt à passer à pxsl_law, pxsl_moment, pxs_fct_finiterv, stats.E(), stats.variance()...
    :pxs_example: |
        val = [5, 10, 15]
        prob = [Rational(1,4), Rational(1,2), Rational(1,4)]
        X = pxs_finiterv('X', val, prob)
        tableau = pxsl_law("x_i", "P(X=x_i)", X)
        # myst(r"La loi de X : \\py{tableau}", globals(), locals())
    :pxs_antipattern: `stats.FiniteRV('X', {val[i]: prob[i] for i in range(len(val))})` — verbose, duplique la logique à chaque exercice.
    """
    
   siz=len(val)
   dic={}
   for j in range(siz):
      dic[val[j]]=prob[j]
   return stats.FiniteRV(x,dic)

# # #############################################################################################################
# # ####                                            Début des essais                                      #######
# # #############################################################################################################

# x='X'
# val = [5,10,15]
# prob= [1/4,1/2,1/4] 
# pxsl_law("x", "P(X=x)",pxs_finiterv(x,val,prob) )
# retourne la variable aléatoire X dont la loi est dict={5 : 0.25 , 10 : 0.5, 15 : 0.25}
# prob= [Rational(1,4),Rational(1,2),Rational(1,4)] 
# pxsl_law("x", "P(X=x)",pxs_finiterv(x,val,prob) )
# retourne la variable aléatoire X dont la loi est dict={5 : 1/4 , 10 : 1/2, 15 : 1/4}

# # #############################################################################################################
# # ####                                            Fin des essais                                       ########
# # #############################################################################################################