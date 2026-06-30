#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 19:11:52 2022

@author: jlebovits
"""

from __future__ import division
import sys
import random
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

import src.scripts.Mes_fctions.Mes_fctions_generalistes_bis
from src.scripts.Mes_fctions.Mes_fctions_generalistes_bis import * 

import src.scripts.Mes_fctions.Mes_fctions_utilitaires
from src.scripts.Mes_fctions.Mes_fctions_utilitaires import _pxs_add_letter 

from sympy import *
from src.scripts.pxs_runtime import get_pxs_lang, myst



def pxsl_par(expr, minus = False, add = False):
    """
    Wraps a LaTeX expression in parentheses if it starts with a minus sign or if it is an Add.

    Parameters
    ----------
    expr : sympy expression or numeric
        The expression to be displayed.
    minus : bool
        If True, wrap when the expression extracts a minus sign.
    add : bool
        If True, wrap when the expression is a sympy ``Add``.

    Returns
    -------
    myst : LaTeX-formatted object (via the myst function)
        The LaTeX string, wrapped in parentheses if negative or Add.

    :pxs_trigger: affichage d'une expression dans une formule, parenthèses conditionnelles autour d'un terme, éviter ambiguïté de signe, protéger un coefficient négatif ou une somme dans un produit LaTeX
    :pxs_returns: |
        chaîne MyST/LaTeX prête à être injectée dans une équation : soit
        ``\\left(<latex>\\right)`` si l'expression est négative ou un ``Add``,
        soit simplement ``<latex>`` sinon.
    :pxs_example: |
        from sympy import Symbol
        x = Symbol('x')
        expr = -x + 1
        txt = pxsl_par(expr, add=True, minus=True)
        # injection : a \\cdot {txt}  →  a \\cdot \\left(-x + 1\\right)
    :pxs_antipattern: Concaténer manuellement r"\\left(" + latex(expr) + r"\\right)" sans vérifier si les parenthèses sont vraiment nécessaires.
    """
    config_standard = pxs_config()
    # Vérifie si l'expression, convertie en chaîne, commence par un signe '-'
    # Cela permet d'identifier les expressions négatives (par exemple -x, -3, -sin(x)...)
    if minus and add:
        if str(expr).startswith('-') or expr.could_extract_minus_sign() or isinstance(expr, Add):
        # Si l'expression est négative, on ajoute des parenthèses autour de son affichage LaTeX
        # Exemple : -x  →  \left(-x\right)
        # myst() est ici utilisée pour insérer la version LaTeX dynamique de l'expression
            return myst(
                r"""\left(\py{latex(expr, **config_standard)}\right) """,
                globals(), locals()
                )
    elif minus:
        if str(expr).startswith('-') or expr.could_extract_minus_sign():
        # Si l'expression est négative, on ajoute des parenthèses autour de son affichage LaTeX
        # Exemple : -x  →  \left(-x\right)
        # myst() est ici utilisée pour insérer la version LaTeX dynamique de l'expression
            return myst(
                r"""\left(\py{latex(expr, **config_standard)}\right) """,
                globals(), locals()
                )
    elif add:
        if isinstance(expr, Add):
        # Si l'expression est négative, on ajoute des parenthèses autour de son affichage LaTeX
        # Exemple : -x  →  \left(-x\right)
        # myst() est ici utilisée pour insérer la version LaTeX dynamique de l'expression
            return myst(
                r"""\left(\py{latex(expr, **config_standard)}\right) """,
                globals(), locals()
            )
        # Si l'expression n’est pas négative, on la renvoie simplement en LaTeX sans parenthèses
    return myst(
            r"""\py{latex(expr, **config_standard)} """,
            globals(), locals()
        )



        
def _pxsl_choose_udv(sol, u, du, v, dv, var = Symbol('x')):
    """
    Generates bilingual LaTeX text (English/French) explaining the choice of
    functions u and v' in an integration by parts setup.

    Parameters
    ----------
    u : sympy expression
        Function chosen as u(x).
    du : sympy expression
        Derivative of u(x).
    v : sympy expression
        Function chosen as v(x).
    dv : sympy expression
        Derivative of v(x), i.e., v'(x).

    Returns
    -------
    str
        A LaTeX-formatted bilingual text describing u, v', and their derivatives.

    :pxs_trigger: intégration par parties, annonce du choix de u et v', phrase "on choisit u et v' tels que", mise en place initiale d'une IBP quand l'utilisateur donne (u, dv)
    :pxs_returns: |
        chaîne MyST bilingue (FR/EN) contenant deux blocs ``\\begin{equation*}`` :
        l'un pour u(x) et v'(x), l'autre pour u'(x) et v(x). Également stockée
        dans ``sol["choice"]`` pour réutilisation ultérieure.
    :pxs_example: |
        from sympy import Symbol, exp, diff, integrate
        x = Symbol('x')
        u, dv = x, exp(x)
        du, v = diff(u, x), integrate(dv, x)
        txt = _pxsl_choose_udv(sol, u, du, v, dv, x)
        # injection dans le corrigé : {txt}
    :pxs_antipattern: Rédiger à la main les deux blocs ``\\begin{equation*}`` en FR+EN pour annoncer u, u', v, v' à chaque nouvel exercice.
    """
    config_standard = pxs_config()
    text = "" 

    # Introduction : phrase bilingue annonçant le choix de u et v'
    text = myst(r"""
        \en{with}\fr{On choisit $u$ et $v'$ tels que :}
        """, globals(), locals())

    # Bloc d'équations affichant les expressions de u(x) et v'(x)
    text += myst(r"""
                      \en{\begin{equation*}
                      &u = \py{latex(u, **config_standard)}&
                      &\textrm{and}&
                      &v' = \py{latex(dv, **config_standard)}&
                      \end{equation*}}
                      \fr{\begin{equation*}
                      &u(\py{var}) = \py{latex(u, **config_standard)}&
                      &\textrm{et}&
                      &v'(\py{var}) = \py{latex(dv, **config_standard)}.&
                      \end{equation*}}
                      """, globals(), locals())

    # Transition bilingue vers les dérivées et primitives correspondantes
    text += myst(r""" 
        \en{gives}\fr{On en déduit donc}
        """)

    # Bloc d'équations affichant u'(x) et v(x)
    text += myst(r"""
                      \en{\begin{equation*}
                      &u' = \py{latex(du, **config_standard)}&
                      &\textrm{and}&
                      &v = \py{latex(v, **config_standard)}.&
                      \end{equation*}}
                      \fr{\begin{equation*}
                      &u'(\py{var}) = \py{latex(du, **config_standard)}&
                      &\textrm{et}&
                      &v(\py{var}) = \py{latex(v, **config_standard)}.&
                      \end{equation*}} 
                      """, globals(), locals())

    # Retourne le texte LaTeX complet (mélange de phrases et équations)
    sol["choice"] = text
    return text

def _pxsl_choose_vdu(sol, u, du, v, dv, var = Symbol('x')):
    """
    Generates bilingual LaTeX text (English/French) explaining the choice of
    functions u' and v in an integration by parts setup.

    Parameters
    ----------
    u : sympy expression
        Function corresponding to u(x).
    du : sympy expression
        Derivative of u(x), i.e., u'(x).
    v : sympy expression
        Function chosen as v(x).
    dv : sympy expression
        Derivative of v(x), i.e., v'(x).

    Returns
    -------
    str
        A LaTeX-formatted bilingual text describing u', v, and their corresponding
        functions and derivatives.

    :pxs_trigger: intégration par parties avec choix inversé, annonce "on choisit u' et v tels que", IBP partant d'une dérivée et d'une primitive déjà connues
    :pxs_returns: |
        chaîne MyST bilingue (FR/EN) avec deux blocs ``\\begin{equation*}`` :
        u'(x) et v(x), puis u(x) et v'(x). Également stockée dans ``sol["choice"]``.
    :pxs_example: |
        from sympy import Symbol, sin, cos, diff, integrate
        x = Symbol('x')
        du, v = cos(x), x
        u, dv = integrate(du, x), diff(v, x)
        txt = _pxsl_choose_vdu(sol, u, du, v, dv, x)
    :pxs_antipattern: Copier-coller _pxsl_choose_udv et inverser à la main l'ordre des lignes pour obtenir l'annonce "u' et v".
    """
    config_standard = pxs_config()
    text = ""

    # Introduction : phrase bilingue annonçant le choix de u' et v
    text = myst(r"""
        \en{with}\fr{On choisit $u'$ et $v$ tels que :}
        """, globals(), locals())

    # Bloc d'équations affichant u'(x) et v(x)
    text += myst(r"""
                      \en{\begin{equation*}
                      &u' = \py{latex(du, **config_standard)}&
                      &\textrm{and}&
                      &v = \py{latex(v, **config_standard)}&
                      \end{equation*}}
                      \fr{\begin{equation*}
                      &u'(\py{var}) = \py{latex(du, **config_standard)}&
                      &\textrm{et}&
                      &v(\py{var}) = \py{latex(v, **config_standard)}.&
                      \end{equation*}}
                      """, globals(), locals())

    # Transition bilingue vers les primitives et dérivées correspondantes
    text += myst(r""" 
        \en{gives}\fr{On en déduit donc}
        """)

    # Bloc d’équations affichant u(x) et v'(x)
    text += myst(r"""
                      \en{\begin{equation*}
                      &u = \py{latex(u, **config_standard)}&
                      &\textrm{and}&
                      &v' = \py{latex(dv, **config_standard)}.&
                      \end{equation*} }
                      \fr{\begin{equation*}
                      &u(\py{var}) = \py{latex(u, **config_standard)}&
                      &\textrm{et}&
                      &v'(\py{var}) = \py{latex(dv, **config_standard)}.&
                      \end{equation*} }
                      """, globals(), locals())

    # Retourne le texte LaTeX complet (phrases bilingues et équations)
    sol["choice"] = text
    return text


def _pxsl_sentence1(sol, u, du, v, dv, type_int, var = Symbol('x'), bl = None, br = None, intf = None):
    """
    Generates the bilingual LaTeX formula showing the integration by parts
    resolution in the case of an *indefinite integral* (primitive).

    Depending on the type of pair chosen ("udv" or "vdu"),
    the function builds the appropriate LaTeX equation for:
        ∫ u·v' dx  =  u·v − ∫ u'·v dx
    or
        ∫ u'·v dx  =  u·v − ∫ u·v' dx

    Parameters
    ----------
    u : sympy expression
        Function u(x).
    du : sympy expression
        Derivative of u(x).
    v : sympy expression
        Function v(x).
    dv : sympy expression
        Derivative of v(x), i.e., v'(x).
    type_int : str
        Type of integration by parts ("udv" or "vdu").

    Returns
    -------
    str
        A LaTeX-formatted bilingual text representing the integration by parts formula.

    :pxs_trigger: première ligne de l'IBP, écriture de l'égalité ∫u·v' = [uv] − ∫u'·v, ouverture du begin{equation*} du calcul
    :pxs_returns: |
        chaîne LaTeX commençant un ``\\begin{equation*}`` avec le label ``eq``
        et la première égalité de l'IBP ; parenthèses sur u, v, u', v' déjà
        gérées via ``pxsl_par``. Également stockée dans ``sol["sentence1"]``.
    :pxs_example: |
        bl, br, intf = _pxs_bounds(a=None, b=None)
        txt = _pxsl_sentence1(sol, u, du, v, dv, "udv", x, bl, br, intf)
    :pxs_antipattern: Écrire à la main "\\int u \\cdot v' dx &= uv - \\int u' \\cdot v dx" sans passer par pxsl_par pour les signes et les Add.
    """

    # Cas où l'utilisateur a fourni (u, dv)
    # Construction de la formule : ∫u·v' dx = u·v − ∫u'·v dx
    if type_int == "udv":
        text = myst(r"""
              \begin{equation*}
                \label{eq}
                \py{intf} \py{pxsl_par(u, add = True)}\cdot \py{pxsl_par(dv, add = True, minus = True)} \ d\py{var}
                &= \py{bl}\py{pxsl_par(u, add = True)}\cdot \py{pxsl_par(v, add = True, minus = True)}\py{br} - \py{intf} \py{pxsl_par(du, add = True)} \cdot \py{pxsl_par(v, add = True, minus = True)} \ d\py{var}\\
                    """, globals(), locals())

    # Cas où l'utilisateur a fourni (du, v)
    # Construction de la formule : ∫u'·v dx = u·v − ∫u·v' dx
    if type_int == "vdu":
        text = myst(r"""
          \begin{equation*}
            \label{eq}
            \py{intf} \py{pxsl_par(du, add = True)}\cdot \py{pxsl_par(v, add = True, minus = True)} \ d\py{var}
            &=\py{bl} \py{pxsl_par(u, add = True)}\cdot \py{pxsl_par(v, add = True, minus = True)} \py{br}- \py{intf} \py{pxsl_par(u, add = true)} \cdot \py{pxsl_par(dv, add = True, minus = True)} \ d\py{var}\\
                """, globals(), locals())

    # Retourne le texte LaTeX de la résolution par parties
    sol["sentence1"] = text
    return text




def _pxsl_sentence2(sol, uv, expr, nb_IBP, a = None, b = None, var = Symbol('x')):
    """
    Builds LaTeX fragments for the integration by parts process when handling
    sign changes and coefficients, with or without integration bounds.

    Parameters
    ----------
    uv : sympy expression
        The product term u·v from integration by parts.
    expr : sympy expression
        The remaining integral expression after applying integration by parts.
    nb_IBP : int
        The number of successive integrations by parts already applied (used to adjust display).
    a, b : numeric or symbolic, optional
        Lower and upper bounds of integration. If None, the integral is indefinite.

    Returns
    -------
    tuple
        text : LaTeX string representing intermediate and simplified steps
        of the integration by parts process, with correct sign and coefficient handling.

    :pxs_trigger: deuxième ligne de l'IBP, simplification du terme [uv] et factorisation de l'intégrale résiduelle, gestion du coefficient et du signe devant la seconde intégrale
    :pxs_returns: |
        tuple ``(text, expr, sol)`` :
        - ``text`` : chaîne LaTeX de la ligne "= [uv] ± coef·∫..."
        - ``expr`` : expression résiduelle factorisée (coef déjà extrait)
        - ``sol`` : dictionnaire enrichi avec ``sol["uv"]``, ``sol["coeff"]``, ``sol["sentence2"]``.
    :pxs_example: |
        txt, expr_res, sol = _pxsl_sentence2(sol, u*v, v*du, nb_IBP=1,
                                             a=None, b=None, var=x)
    :pxs_antipattern: Appeler latex(uv) puis latex(expr) séparément et recoller manuellement le signe sans pxs_separate_factors/pxsl_par.
    """
    config_standard = pxs_config()
    # Si les bornes a et b ne sont pas données → intégrale indéfinie
    bl, br, intf = _pxs_bounds(a, b)

    # Extraction du coefficient numérique de expr (partie indépendante de x)
    # puis gestion du signe et de la valeur absolue
    expr = factor(-simplify(-expr))
    if a is None and b is None:
        text = myst(r""" 
             &= \py{bl}\py{latex(uv, **config_standard)}\py{br} 
             """, globals(), locals())
        sol["uv"] = uv
    else:
        text = myst(r""" 
             &= \py{latex(uv.subs(var,b), **config_standard)} - \py{pxsl_par(uv.subs(var,a), minus = True, add = True)} 
             """, globals(), locals())
        sol["uv"] = uv.subs(var,b) - uv.subs(var,a)
    text += myst(r""" \py{pxsl_latex_coefficient(-pxs_separate_factors(expr, var)[0], sign = True)}\py{intf} \py{pxsl_par(pxs_separate_factors(expr, var)[1], add = True, minus = True)}  \ d\py{var}
            """, globals(), locals())

    sol["coeff"] = pxs_separate_factors(expr, var)[0]
    if nb_IBP == 2 and a is not None and b is not None:
        if uv.subs(var,a).could_extract_minus_sign():
                text += myst(r""" 
        \\&=\py{latex(uv.subs(var,b) - uv.subs(var,a), **config_standard)} \py{pxsl_latex_coefficient(pxs_separate_factors(expr, var)[0], sign = True)}\py{intf} \py{pxsl_par(pxs_separate_factors(expr, var)[1], add = True, minus = True)}  \ d\py{var}
              """, globals(), locals())
        sol["sentence2"] = text
        return text, pxs_separate_factors(expr, var)[1], sol
    sol["sentence2"] = text
    return text, expr, sol


def _pxsl_explain(sol, u, du, v, dv, type_int, nb_IBP, a = None, b = None, var = Symbol('x'), bl = None, br = None, intf = None):  
    """
    Builds a bilingual LaTeX explanation for the integration by parts process,
    using either the primitive form or the definite integral form.

    The function combines:
    - the core integration by parts equation (via _pxsl_resolution_prim or _pxsl_resolution_int)
    - the corresponding minus/plus term adjustments (via _pxsl_minus)
    depending on the integration type ("udv" or "vdu") and the presence of bounds.

    Parameters
    ----------
    u : sympy expression
        Function u(x).
    du : sympy expression
        Derivative of u(x).
    v : sympy expression
        Function v(x).
    dv : sympy expression
        Derivative of v(x), i.e., v'(x).
    type_int : str
        Integration by parts type: "udv" for (u, dv) or "vdu" for (du, v).
    nb_IBP : int
        Number of integration by parts steps performed (for formatting purposes).
    a, b : numeric or symbolic, optional
        Integration bounds. If None, the integral is indefinite.

    Returns
    -------
    tuple
        text : LaTeX string representing the detailed explanation
        and simplified version of the integration by parts process.

    :pxs_trigger: rédaction des deux premières lignes d'une IBP (formule + simplification), orchestration interne de sentence1 + sentence2, prise en compte du type (udv/vdu) et des bornes
    :pxs_returns: |
        tuple ``(text, expr, sol)`` :
        - ``text`` : chaîne LaTeX concaténée (sentence1 suivi de sentence2)
        - ``expr`` : intégrale résiduelle simplifiée
        - ``sol`` : dictionnaire enrichi par les deux sous-fonctions.
    :pxs_example: |
        bl, br, intf = _pxs_bounds(a, b)
        txt, expr_res, sol = _pxsl_explain(sol, u, du, v, dv,
                                           "udv", nb_IBP=1,
                                           a=a, b=b, var=x,
                                           bl=bl, br=br, intf=intf)
    :pxs_antipattern: Appeler _pxsl_sentence1 puis _pxsl_sentence2 à la main dans chaque exercice en gérant soi-même le swap udv/vdu.
    """

    # Étape 1 : construire la résolution pour une primitive
    text = _pxsl_sentence1(sol, u, du, v, dv, type_int, var, bl, br, intf)

    # Étape 2 : ajouter les termes avec le bon signe selon le type d’intégration
    if type_int == "udv":
        txt, expr, sol = _pxsl_sentence2(sol, u*v, v*du, nb_IBP, a = a, b = b, var = var)
        text += txt
    else:
        txt, expr, sol = _pxsl_sentence2(sol, u*v, u*dv, nb_IBP, a = a, b = b, var = var)
        text += txt
    
    # Retourne le texte complet et sa version simplifiée
    return text, expr, sol



def _pxsl_conclude(sol, uv, expr, origin_int, var = Symbol('x')):
    """
    Generates the final bilingual LaTeX step that concludes the integration by parts
    process, displaying the complete evaluated primitive with constant C.

    Parameters
    ----------
    uv : sympy expression
        The product term u·v obtained during integration by parts.
    expr : sympy expression
        The remaining part of the expression (integral to be evaluated or simplified).
    origin_int : sympy expression
        The original integral expression (used for final verification and display).

    Returns
    -------
    str
        A LaTeX-formatted bilingual text showing the final result of the integration,
        including the constant of integration.

    :pxs_trigger: conclusion d'une IBP sur une primitive (pas de bornes), ligne finale "= primitive + C", fermeture du begin{equation*}, ajout de la mention "C constante réelle"
    :pxs_returns: |
        chaîne LaTeX terminant le calcul : ligne "= [uv] ± coef·primitive + C",
        puis ligne "= résultat sympy + C" et fermeture ``\\end{equation*}``.
        Également stockée dans ``sol["conclude"]``.
    :pxs_example: |
        txt = _pxsl_conclude(sol, u*v, v*du, u*dv, var=x)
        # Fermeture propre du corrigé IBP indéfini.
    :pxs_antipattern: Terminer à la main avec "+ C" et ``integrate(origin_int, var)`` sans gérer le signe du coefficient ni la phrase bilingue "where C is a real constant".
    """
    config_standard = pxs_config()
    expr = factor(-simplify(-expr))
    # Extraction du coefficient numérique de l’expression (partie indépendante de x)
    # Gestion du signe et des cas particuliers (valeurs 1 ou -1 ignorées)
    
    if pxs_separate_factors(expr, var)[0] < 0 and pxs_separate_factors(expr, var)[0] != -1:
        coeff = myst(r"""\py{latex(-pxs_separate_factors(expr, var)[0], **config_standard)} """, globals(), locals())
        dot = myst(r"""\cdot """)
    elif pxs_separate_factors(expr, var)[0] > 0 and pxs_separate_factors(expr, var)[0] != 1:
       coeff = myst(r"""\py{latex(pxs_separate_factors(expr, var)[0], **config_standard)} """, globals(), locals()) 
       dot = myst(r"""\cdot """)
    else:
        coeff = myst(r""" """, globals(), locals())
        
    # Si l’expression commence par un signe négatif
    if str(expr).startswith('-'):
        # Cas où le signe devient "plus" après simplification

        
        text = myst(r""" \\&=
\py{latex(uv, **config_standard)} + \py{coeff}\py{dot} \py{pxsl_par(integrate(pxs_separate_factors(expr, var)[1], x), add = True, minus = True)} + C 
              
              """, globals(), locals())
    else:
        # Cas standard : on garde le signe négatif devant le terme intégré
        text = myst(r""" \\&=
\py{latex(uv, **config_standard)} - \py{coeff}\py{dot}\py{pxsl_par(integrate(pxs_separate_factors(expr, var)[1], var), add = True, minus = True)} + C 
                
                """, globals(), locals())

    # Ajout de la ligne finale donnant la primitive complète de l’intégrale d’origine
    text += myst(r"""\\
              & = \py{latex(integrate(origin_int, var), **config_standard)} + C, \textrm{ \en{with}\fr{où} }C\textrm{ \en{a real constant}\fr{est une constante réelle}}.
              \end{equation*}
              """, globals(), locals())

    # Retourne le texte LaTeX complet de conclusion
    sol["conclude"] = text
    return text


def _pxsl_conclude_int(sol, uv, expr, origin_int, a, b, var = Symbol('x')):
    """
    Generates the final bilingual LaTeX step concluding the integration by parts
    process for a *definite integral* between bounds a and b.

    This function evaluates and formats the expression:
        [u·v]_a^b ± coefficient × [∫f(x)dx]_a^b
    and shows the fully evaluated result of the original definite integral.

    Parameters
    ----------
    uv : sympy expression
        The product term u·v obtained during integration by parts.
    expr : sympy expression
        The remaining part of the expression (integral to be evaluated or simplified).
    origin_int : sympy expression
        The original integral expression (used for final comparison and display).
    a, b : numeric or symbolic
        Lower and upper bounds of the definite integral.

    Returns
    -------
    str
        A LaTeX-formatted bilingual text showing the final step of the definite
        integration by parts, with all evaluations and signs displayed correctly.

    :pxs_trigger: conclusion d'une IBP sur une intégrale définie, évaluation ``[uv]_a^b`` et ``[primitive]_a^b``, ligne finale donnant la valeur numérique/symbolique de ∫_a^b
    :pxs_returns: |
        chaîne LaTeX terminant le ``\\begin{equation*}`` avec les évaluations
        aux bornes, le développement du terme ``u(a)v(a)`` (Add géré terme à
        terme), puis l'égalité avec ``integrate(origin_int, (var, a, b))``.
        Également stockée dans ``sol["conclude"]``.
    :pxs_example: |
        txt = _pxsl_conclude_int(sol, u*v, v*du, u*dv, a=0, b=1, var=x)
    :pxs_antipattern: Écrire à la main ``f(b) - f(a)`` en oubliant de gérer séparément les Add négatifs de ``u(a)v(a)`` et les signes de coef.
    """
    config_standard = pxs_config()
    bl, br, intf = _pxs_bounds(a, b)
    expr = factor(-simplify(-expr))
    # Définit les crochets et notations bilingues pour les bornes d’intégration

    # Extraction du coefficient numérique et gestion du signe
    # On ajoute aussi les symboles nécessaires selon la présence d’un coefficient
    if pxs_separate_factors(expr, var)[0] < 0 and pxs_separate_factors(expr, var)[0] != -1:
        coeff = myst(r"""\py{latex(-pxs_separate_factors(expr, var)[0], **config_standard)} """, globals(), locals())
        dot = myst(r"""\cdot """)
        l_par = myst(r"""\left( """)
        r_par = myst(r"""\right) """)
    elif pxs_separate_factors(expr, var)[0] > 0 and pxs_separate_factors(expr, var)[0] != 1:
       coeff = myst(r"""\py{latex(pxs_separate_factors(expr, var)[0], **config_standard)} """, globals(), locals()) 
       dot = myst(r"""\cdot """)
       l_par = myst(r"""\left( """)
       r_par = myst(r"""\right) """)
    else:
        coeff = myst(r""" """, globals(), locals())
        dot = myst(r""" """)
        l_par = myst(r""" """)
        r_par = myst(r""" """)
    text = ""
    # Si l’expression commence par un signe négatif
    if expr.could_extract_minus_sign():
        # Cas où le signe devient "plus" après simplification

        if isinstance(uv.subs(var,a), Add):
            text += myst(r"""
        \\&=\py{latex(uv.subs(var,b), **config_standard)}""", globals(), locals())
            for term in uv.subs(var,a).as_ordered_terms():
                if term.could_extract_minus_sign():
                    text += myst(r""" + \py{latex(-term, **config_standard)}""", globals(), locals())
                else:
                    text += myst(r""" - \py{latex(abs(term), **config_standard)}""", globals(), locals())
            text += myst(r""" + \py{coeff} \py{dot}\py{bl}\py{pxsl_par(integrate(pxs_separate_factors(expr, var)[1], var), minus = True)}\py{br}
              """, globals(), locals())
            text += myst(r""" + \py{coeff} \py{dot}\py{l_par}\py{latex(integrate(pxs_separate_factors(expr, var)[1], var).subs(var,b), **config_standard)} - \py{pxsl_par(integrate(pxs_separate_factors(expr, var)[1], var).subs(var,a), add = True, minus = True)}\py{r_par}
              """, globals(), locals())
        elif uv.subs(var,a).could_extract_minus_sign():
            text += myst(r"""
        \\&=\py{latex(uv.subs(var,b), **config_standard)} + \py{latex(-uv.subs(var,a), **config_standard)} + \py{coeff} \py{dot}\py{bl}\py{pxsl_par(integrate(pxs_separate_factors(expr, var)[1], var), minus = True)}\py{br}
              """, globals(), locals())
            text += myst(r"""
        \\&=\py{latex(uv.subs(var,b), **config_standard)} + \py{latex(-uv.subs(var,a), **config_standard)} + \py{coeff} \py{dot}\py{l_par}\py{pxsl_par(integrate(pxs_separate_factors(expr, var)[1], var).subs(var,b), minus = True, add = True)} - \py{pxsl_par(integrate(pxs_separate_factors(expr, var)[1], var).subs(var,a), minus = True, add = True)}\py{r_par}
              """, globals(), locals())
        else:
            text += myst(r"""
        \\&=\py{latex(uv.subs(var,b) - uv.subs(var,a), **config_standard)} + \py{coeff} \py{dot}\py{bl}\py{pxsl_par(integrate(pxs_separate_factors(expr, var)[1], var), minus = True)}\py{br}
              """, globals(), locals())
            text += myst(r"""
        \\&=\py{latex(uv.subs(var,b) - uv.subs(var,a), **config_standard)} + \py{coeff} \py{dot}\py{l_par}\py{pxsl_par(integrate(pxs_separate_factors(expr, var)[1], var).subs(var,b))} - \py{pxsl_par(integrate(pxs_separate_factors(expr, var)[1], var).subs(var,a), add = True, minus = True)}\py{r_par}
              """, globals(), locals())
    else:
        # Cas standard : le signe reste négatif devant la deuxième intégrale
        text = myst(r""" \\&=
\py{latex(uv.subs(var,b), **config_standard)} - \py{pxsl_par(uv.subs(var,a), add = True, minus = True)} - \py{coeff}\py{dot}\py{bl}\py{pxsl_par(integrate(pxs_separate_factors(expr, var)[1], var), minus = True)}\py{br}""", globals(), locals())
        if isinstance(uv.subs(var,a), Add):
            text += myst(r"""
        \\&=\py{latex(uv.subs(var,b), **config_standard)}""", globals(), locals())
            for term in uv.subs(var,a).as_ordered_terms():
                if term.could_extract_minus_sign():
                    text += myst(r""" + \py{latex(-term, **config_standard)}""", globals(), locals())
                else:
                    text += myst(r""" - \py{latex(term, **config_standard)}""", globals(), locals())
            text += myst(r""" - \py{coeff} \py{dot}\left(\py{latex(integrate(pxs_separate_factors(expr, var)[1], var).subs(var,b), **config_standard)} - \py{pxsl_par(integrate(pxs_separate_factors(expr, var)[1], var).subs(var,a), minus = True, add = True)}\right)
              """, globals(), locals())
        elif uv.subs(var,a).could_extract_minus_sign():
            text += myst(r"""
        \\&=\py{latex(uv.subs(var,b), **config_standard)} + \py{latex(-uv.subs(var,a), **config_standard)} - \py{coeff} \py{dot}\left(\py{latex(integrate(pxs_separate_factors(expr, var)[1], var).subs(var,b), **config_standard)} - \py{pxsl_par(integrate(pxs_separate_factors(expr, var)[1], var).subs(var,a), add = True, minus = True)}\right)
              """, globals(), locals())
        else:
            text += myst(r"""
        \\&=\py{latex(uv.subs(var,b), **config_standard)} - \py{latex(uv.subs(var,a), **config_standard)} - \py{coeff} \py{dot}\left(\py{latex(integrate(pxs_separate_factors(expr, var)[1], var).subs(var,b), **config_standard)} - \py{pxsl_par(integrate(pxs_separate_factors(expr, var)[1], var).subs(var,a), add = True, minus = True)}\right)
              """, globals(), locals())

    # Ligne finale : égalité avec l’intégrale définie complète d’origine
    text += myst(r"""\\
              & =\py{latex(integrate(origin_int, (var, a, b)), **config_standard)}.
              \end{equation*}
              """, globals(), locals())

    # Retourne le texte LaTeX complet de conclusion (forme avec bornes)
    sol["conclude"] = text
    return text




def _pxs_bounds(a, b):
    """
    Builds the LaTeX fragments needed to render either an indefinite integral
    or a definite integral with bounds ``a`` and ``b``.

    Parameters
    ----------
    a, b : numeric or symbolic, optional
        Lower and upper bounds of integration. If both are ``None`` the
        integral is treated as indefinite.

    Returns
    -------
    tuple
        ``(bl, br, intf)`` where ``bl`` is the left bracket (or empty),
        ``br`` is the right bracket / evaluation bar, and ``intf`` is the
        integral symbol with or without bounds.

    :pxs_trigger: génération conjointe des crochets d'évaluation et du symbole intégrale, bascule FR (\\left[...\\right]_a^b) / EN (\\bigg|_a^b), distinction primitive vs intégrale définie
    :pxs_returns: |
        tuple ``(bl, br, intf)`` :
        - ``bl`` : crochet gauche ``\\left[`` en FR, vide en EN, vide si primitive
        - ``br`` : crochet droit ``\\right]_a^b`` en FR, ``\\bigg|_a^b`` en EN, vide si primitive
        - ``intf`` : ``\\int`` ou ``\\int_a^b`` selon la présence des bornes.
    :pxs_example: |
        bl, br, intf = _pxs_bounds(0, 1)
        # utilisables directement dans \\py{intf} ... \\py{bl} uv \\py{br}
    :pxs_antipattern: Tester à la main ``if a is None`` dans chaque fonction et recréer les chaînes ``\\left[`` / ``\\bigg|`` à chaque endroit.
    """
    config_standard = pxs_config()
    if a is None and b is None:
        bl = myst(r""" """)
        br = myst(r""" """)
        intf = myst(r""" \int """)
    else:
        bl = myst(r"""\en{}\fr{\left[} """, globals(), locals())
        br = myst(r"""\en{\bigg|_{\py{latex(a, **config_standard)}}^{\py{latex(b, **config_standard)}}}\fr{\right]_{\py{latex(a, **config_standard)}}^{\py{latex(b, **config_standard)}}} """, globals(), locals())
        intf = myst(r""" \int_{\py{latex(a, **config_standard)}}^{\py{latex(b, **config_standard)}} """, globals(), locals())
    return bl, br, intf

    

def _pxs_explain_IBP(sol, var = Symbol('x'), f1 = None, f2 = None, type_int = None, nb_IBP = 1, a = None, b = None):
    """
    Builds a complete bilingual LaTeX correction text for the Integration by Parts (IBP) process,
    handling both single and double applications, and supporting definite or indefinite integrals.

    Depending on the number of integrations by parts (`nb_IBP`) and the type (`type_int`),
    this function calls all the appropriate sub-functions:
        - _pxs_resolve_pairs     → identifies (u, du, v, dv)
        - _pxsl_choose_udv/vdu   → generates the introduction LaTeX text
        - _pxsl_explain          → generates the main formula
        - _pxsl_conclude/_int    → final step (primitive or definite)
        - recursively calls itself if nb_IBP = 2

    Parameters
    ----------
    x : sympy Symbol
        The integration variable.
    f1, f2 : sympy expressions
        The two parts of the integrand provided by the user.
    type_int : str
        Integration by parts type: "udv" for (u, dv) or "vdu" for (du, v).
    nb_IBP : int, optional
        Number of integration by parts steps (1 or 2). Default is 1.
    a, b : numeric or symbolic, optional
        Lower and upper bounds of integration (if given, produces a definite integral).

    Returns
    -------
    str
        A LaTeX-formatted bilingual text that fully explains the integration by parts
        procedure, with all symbolic steps, coefficients, and final results.

    :pxs_trigger: orchestration complète d'un corrigé IBP interne, IBP simple ou double, intégrale définie ou indéfinie, enchaînement choose → explain → conclude
    :pxs_returns: |
        tuple ``(text, u, du, v, dv, expr, sol)`` :
        - ``text`` : corrigé LaTeX complet (intro + formule + simplification + conclusion éventuelle)
        - ``u, du, v, dv`` : les quatre fonctions de l'IBP, prêtes pour une 2e IBP
        - ``expr`` : intégrale résiduelle à traiter ensuite
        - ``sol`` : dictionnaire enrichi à chaque étape.
    :pxs_example: |
        text, u, du, v, dv, expr, sol = _pxs_explain_IBP(
            sol, var=x, f1=x, f2=exp(x), type_int="udv", nb_IBP=1)
    :pxs_antipattern: Réécrire dans chaque exercice l'enchaînement choose_udv → sentence1 → sentence2 → conclude au lieu d'appeler la fonction passerelle.
    """
    config_standard = pxs_config()
    text = ""
    
    # --- Définition des éléments de mise en forme selon la présence de bornes ---
    bl, br, intf = _pxs_bounds(a, b)

    # === Première intégration par parties ===
    
    # Retrouver u, du, v et dv en fonction des informations de départ
    if type_int == "udv":
        u, du, v, dv = f1, diff(f1, var), integrate(f2, var), f2
    if type_int == "vdu":
        u, du, v, dv  = integrate(f2, var), f2, f1, diff(f1, var)
    
    # Introduction selon le type choisi (u,dv) ou (du,v)
    if type_int == "udv":
        text += _pxsl_choose_udv(sol, u, du, v, dv, var)
    else:
        text += _pxsl_choose_vdu(sol, u, du, v, dv, var)

    # Phrase bilingue avant l’application de la formule
    text += myst(r"""
    \en{So integration by parts gives us:}\fr{En appliquant la formule, on obtient : }""")

    # Construction de la formule selon la présence ou non de bornes
    txt, expr, sol = _pxsl_explain(sol, u, du, v, dv, type_int, nb_IBP, var = var, a = a, b = b, bl = bl, br = br, intf = intf)
    text += txt
    

    # === Conclusion si une seule intégration par parties ===
    if nb_IBP == 1 and a is None and b is None:
        if type_int == "udv":
            text += _pxsl_conclude(sol, u*v, v*du, u*dv, var = var)
        if type_int == "vdu":
            text += _pxsl_conclude(sol, u*v, u*dv, v*du, var = var)
    elif nb_IBP == 1:
        if type_int == "udv":
            text += _pxsl_conclude_int(sol, u*v, v*du, u*dv, a, b, var = var)
        if type_int == "vdu":
            text += _pxsl_conclude_int(sol, u*v, u*dv, v*du, a, b, var = var)

    # === Cas où une deuxième intégration par parties est demandée (primitive) ===
    if nb_IBP == 2 :
        text += myst(r"""
    \end{equation*}
    """)

    # Retourne le texte LaTeX complet expliquant les étapes de l’IBP
    return text, u, du, v, dv, expr, sol


def pxs_explain_IBP(var = Symbol('x'), f1 = None, f2 = None, type_int = "udv", a = None, b = None, nb_IBP = 1, intro = True, conclude = True, link = "https://app.pyxiscience.com/teacher/dashboard/module/7e0b271d-92f9-11f0-a777-0e37881c19a9/chapter/258e5825-9de5-11f0-a5a8-0e37881c19a9#quotient-fini#IBP2"):
    """
    Creates a complete bilingual LaTeX explanation for computing an integral
    using the Integration by Parts (IBP) method.

    This is the main public-facing function that introduces the IBP concept,
    calls the internal recursive explanation generator `_pxs_explain_IBP`, and
    concludes by showing the final boxed result of the integral (definite or
    indefinite).

    Parameters
    ----------
    var : sympy Symbol
        The integration variable.
    f1, f2 : sympy expressions
        The two parts of the integrand (used as u and dv or du and v).
    type_int : str, optional
        Type of integration by parts ("udv" or "vdu"). Default is "udv".
    a, b : numeric or symbolic, optional
        Lower and upper bounds of the integral. If None, it’s treated as an
        indefinite integral.
    nb_IBP : int, optional
        Number of integrations by parts to perform (1 or 2). Default is 1.

    Returns
    -------
    str
        A bilingual LaTeX-formatted text containing the full reasoning,
        step-by-step explanation, and final boxed conclusion of the IBP process.

    :pxs_trigger: calcul d'une intégrale par intégration par parties, corrigé automatique d'un ∫ f(x)g(x)dx ou ∫_a^b f(x)g(x)dx, énoncé "calculer cette intégrale en utilisant une IBP", primitive de x·e^x, ln(x), x·cos(x), etc.
    :pxs_returns: |
        dictionnaire ``sol`` prêt à être injecté dans un corrigé MyST :
        - ``sol["text"]`` : corrigé LaTeX bilingue complet (intro + déroulé + conclusion encadrée)
        - ``sol["int"]`` : valeur sympy de l'intégrale (définie ou indéfinie)
        - ``sol["u"]``, ``sol["du"]``, ``sol["v"]``, ``sol["dv"]`` : fonctions choisies
        - ``sol["choice"]``, ``sol["sentence1"]``, ``sol["sentence2"]``, ``sol["conclude"]`` : fragments réutilisables
        - ``sol["a"]``, ``sol["b"]``, ``sol["var"]``, ``sol["expr"]`` : contexte de l'exercice.
    :pxs_example: |
        from sympy import Symbol, exp, ln
        x = Symbol('x')
        sol = pxs_explain_IBP(var=x, f1=ln(x), f2=1, type_int="udv")
        # dans le .md :   {sol["text"]}
        # ou juste la valeur :   \\(\\py{{latex(sol["int"])}}\\)
    :pxs_antipattern: Rédiger à la main un corrigé IBP avec ``\\begin{equation*}``, ``\\int``, ``[uv]_a^b``, la conclusion encadrée et la phrase bilingue "C constante réelle".
    """
    config_standard = pxs_config()
    sol = {}
    # Introduction bilingue avec lien interactif vers le chapitre concerné
    if intro:
        text = myst(r"""
```{fr}
On calcule cette intégrale en réalisant une [{color:blue}`intégration par parties`]({{link}}) :
```
```{en}
Using [{color:blue}`integration by parts`]({link}) :
```
""", globals(), locals())
    else:
        text = myst(r""" """)
        
    sol["intro"] = text
    # Appel de la fonction principale interne qui rédige les étapes détaillées
    txt, u, du, v, dv, expr, sol = _pxs_explain_IBP(sol, var, f1, f2, type_int, nb_IBP, a, b)
    text += txt
    sol["u"], sol["du"], sol["v"], sol["dv"] = u, du, v, dv
    sol["a"], sol["b"], sol["var"] = a, b, var


    # === Cas (u, dv) sans bornes ===
    if conclude and type_int == "udv" and a is None and b is None and nb_IBP == 1:
        text += myst(r"""
                  \en{Thus,}\fr{On a donc montré :}
                    \begin{equation*}
                    \fbox{$\displaystyle{\int \py{latex(u*dv, **config_standard)} \;d\py{var} = \py{latex(integrate(u*dv, var), **config_standard)}} + C$, \en{with}\fr{où} $C$ \en{a real constant}\fr{est une constante réelle}.}
                    \end{equation*}""", globals(), locals())
    elif type_int == "udv" and a is None and b is None and nb_IBP == 1:
        sol["int"] = integrate(u*dv, var)

    # === Cas (u, dv) avec bornes ===
    elif conclude and type_int == "udv" and nb_IBP == 1:
        text += myst(r"""
                  \en{Thus,}\fr{On a donc montré :}
                    \begin{equation*}
                    \fbox{$\displaystyle{\int_{\py{latex(a, **config_standard)}}^{\py{latex(b, **config_standard)}} \py{latex(u*dv, **config_standard)} \;d\py{var} = \py{latex(integrate(u*dv, (var, a, b)), **config_standard)}}$}
                    \end{equation*}""", globals(), locals())
        sol["int"] = integrate(u*dv, (var, a, b))
    elif type_int == "udv" and nb_IBP == 1:
        sol["int"] = integrate(u*dv, (var, a, b))

    # === Cas (du, v) sans bornes ===
    if conclude and type_int == "vdu" and a is None and b is None and nb_IBP == 1:
        text += myst(r"""
                  \en{Thus,}\fr{On a donc montré :}
                    \begin{equation*}
                    \fbox{$\displaystyle{\int \py{latex(v*du, **config_standard)} \;d\py{var} = \py{latex(integrate(v*du, var), **config_standard)}} + C$, \en{with}\fr{où} $C$ \en{a real constant}\fr{est une constante réelle}.}
                    \end{equation*}""", globals(), locals())
        sol["int"] = integrate(v*du, var)
    elif type_int == "vdu" and a is None and b is None and nb_IBP == 1:
        sol["int"] = integrate(v*du, var)

    # === Cas (du, v) avec bornes ===
    elif conclude and type_int == "vdu" and nb_IBP == 1:
        text += myst(r"""
                  \en{Thus,}\fr{On a donc montré :}
                    \begin{equation*}
                    \fbox{$\displaystyle{\int_{\py{latex(a, **config_standard)}}^{\py{latex(b, **config_standard)}} \py{latex(v*du, **config_standard)}\;d\py{var} = \py{latex(integrate(v*du, (var, a, b)), **config_standard)}}$}
                    \end{equation*}""", globals(), locals())
        sol["int"] = integrate(v*du, (var, a, b))
    elif type_int == "vdu" and nb_IBP == 1:
        sol["int"] = integrate(v*du, (var, a, b))

    sol["text"] = text
    sol["expr"] = expr
    # Retourne le texte complet, incluant l’introduction, le déroulé et la conclusion
    return sol

def pxsl_final_sentence(sol, a, b, var, mult, *args):
    """
    Recombine the intermediate ``sol`` dictionaries from successive integrations
    by parts into a single bilingual LaTeX conclusion, showing how the two
    partial results collapse into the final value of the original integral.

    Parameters
    ----------
    sol : dict
        Master solution dictionary (the final LaTeX is stored in
        ``sol["final_sentence"]``).
    a, b : numeric or symbolic, optional
        Integration bounds. If both are ``None`` a ``+C`` is appended.
    var : sympy Symbol
        Integration variable.
    mult : str
        Multiplication symbol used between coefficient and remaining integral.
    *args : dict
        Successive per-step dictionaries produced by ``pxs_explain_IBP``
        (each contains ``"uv"``, ``"coeff"``, ``"int"``, ``"u"``, ``"dv"``).

    Returns
    -------
    str
        A LaTeX string (also stored in ``sol["final_sentence"]``) wrapping up
        the full multi-IBP computation in a single ``\\begin{equation*}``.

    :pxs_trigger: conclusion d'une double (ou multiple) intégration par parties, recollage des résultats partiels, égalité finale "∫ f(x)g(x)dx = ... + C", synthèse de deux IBP successives
    :pxs_returns: |
        chaîne LaTeX contenue dans un ``\\begin{equation*}`` qui part de
        l'intégrale originale ``∫ u·dv`` et enchaîne les égalités jusqu'à la
        valeur finale (avec ``+ C`` si intégrale indéfinie). Également stockée
        dans ``sol["final_sentence"]``.
    :pxs_example: |
        sol1 = pxs_explain_IBP(var=x, f1=x**2, f2=exp(x),
                               type_int="udv", conclude=False, nb_IBP=2)
        sol2 = pxs_explain_IBP(var=x, f1=sol1["expr"], f2=1,
                               type_int="udv", intro=False, conclude=False)
        pxsl_final_sentence(sol, a=None, b=None, var=x,
                            mult=r"\\cdot", sol1, sol2)
        # injection :  {sol["final_sentence"]}
    :pxs_antipattern: Concaténer à la main ``sol1["uv"] + sol2["int"]`` dans une f-string LaTeX sans gérer les signes, le ``+C`` et la réduction finale via ``integrate``.
    """
    config_standard = pxs_config()
    bl, br, intf = _pxs_bounds(a, b)
    
    final_sol = myst(r"""
            \begin{equation*}
\py{intf}\py{latex(args[0]["u"]*args[0]["dv"],**config_standard)}\,d\py{var} 
            """, globals(), locals())
    for i in range(len(args) - 1):
        if args[i]["coeff"] == -1 and (args[i+1]["int"].could_extract_minus_sign() or latex(args[i+1]["int"], **config_standard).startswith('-')):
            final_sol += myst(r"""
                &= \py{latex(args[i]["uv"], **config_standard)}\py{latex(args[i+1]["int"], **config_standard)}
                """, globals(), locals())
            if a is None and b is None:
                final_sol += myst(r""" +C """, globals(), locals())
            if Add(args[i]["uv"], args[i+1]["int"], evaluate = False) != args[i]["uv"] + args[i+1]["int"]:
                final_sol += myst(r"""
                \\ &= \py{latex(integrate(args[0]["u"]*args[0]["dv"], (var, a, b)), **config_standard)}
                """, globals(), locals())
                if a is None and b is None:
                    final_sol += myst(r""" +C """, globals(), locals())
        elif args[i]["coeff"] == -1:
            final_sol += myst(r"""
                &=\py{latex(args[i]["uv"], **config_standard)}+\py{latex(args[i+1]["int"], **config_standard)}
                """, globals(), locals())
            if a is None and b is None:
                final_sol += myst(r""" + C """, globals(), locals())
            if Add(args[i]["uv"], args[i+1]["int"], evaluate = False) != args[i]["uv"] + args[i+1]["int"]:
                final_sol += myst(r"""
                        \\&= \py{latex(integrate(args[0]["u"]*args[0]["dv"], (var, a, b)), **config_standard)}
                        """, globals(), locals())
                if a is None and b is None:
                    final_sol += myst(r""" + C """, globals(), locals())
        else :
            mult2 = mult if args[i]["coeff"] != 1 else myst(r""" """)
            final_sol += myst(r"""
        &= \py{latex(args[i]["uv"], **config_standard)}\py{pxsl_latex_coefficient(-args[i]["coeff"], sign = True)}\py{mult2}\py{pxsl_par(args[i+1]["int"], add = True, minus = True)}
                              """, globals(), locals())
            if a is None and b is None:
                final_sol += myst(r""" + C """, globals(), locals())
            final_sol += myst(r"""
\\&= \py{latex(integrate(args[0]["u"]*args[0]["dv"], (var, a, b)), **config_standard)}
            """, globals(), locals())
            if a is None and b is None:
                final_sol += myst(r""" + C, \textrm{ \en{with}\fr{où} }C\textrm{ \en{a real constant}\fr{est une constante réelle}}. """, globals(), locals())
    final_sol += myst(r""" \end{equation*}""")
    sol["final_sentence"] = final_sol
    return final_sol

def pxsl_partial_decomp(
    num: list = [],
    den: list = [],
    var=Symbol('x'),
    mul_symbol=myst(r""" \cdot"""),
    method = "simple"
) -> dict:
    """
    Construct the symbolic structure of a partial fraction decomposition.

    The function analyzes the denominator factors, generates the appropriate
    elementary fractions (including powers for repeated factors), assigns
    symbolic coefficients (A, B, C, ...), and builds the associated identity
    equation.

    Parameters
    ----------
    num : list, optional
        List representing the numerator (kept for consistency, not expanded here).
    den : list, optional
        List of denominator factors (SymPy expressions).
    var : Symbol, optional
        Main symbolic variable (default is ``Symbol('x')``).
    mul_symbol : Any, optional
        Multiplication symbol used in LaTeX rendering.
    method : str, optional
        Decomposition method: "simple" or "advanced" (default is "simple"). 
        If "simple", one letter by term, if "advanced", linear terms for irreducible quadratics.

    Returns
    -------
    dict
        A dictionary containing:
        - num : list
        - den : list
        - letters : list of str
        - elem_list : list of denominator elements
        - var : Symbol
        - expr : symbolic sum of elementary fractions
        - identity : simplified identity after clearing denominators

    Examples
    --------
    Basic usage (distinct linear factors)
    >>> from sympy import Symbol
    >>> x = Symbol('x')
    >>> sol = pxsl_partial_decomp(den=[x, x - 1])
    >>> sol["letters"]
    ['A', 'B']
    >>> sol["expr"]
    A/x + B/(x - 1)

    Repeated factor (powers are generated automatically)
    >>> sol = pxsl_partial_decomp(den=[x, (x - 1)**2])
    >>> sol["letters"]
    ['A', 'B', 'C']
    >>> sol["expr"]
    A/x + B/(x - 1) + C/(x - 1)**2

    Mix of repeated and distinct factors
    >>> sol = pxsl_partial_decomp(den=[(x + 2)**3, (2*x - 1)])
    >>> sol["letters"]
    ['A', 'B', 'C', 'D']
    >>> sol["expr"]
    A/(x + 2) + B/(x + 2)**2 + C/(x + 2)**3 + D/(2*x - 1)

    Advanced mode (irreducible quadratic gets a linear numerator)
    >>> sol = pxsl_partial_decomp(den=[x**2 + 1], method="advanced")
    >>> sol["letters"]
    ['A', 'B']
    >>> sol["expr"]
    (A*x + B)/(x**2 + 1)

    Advanced mode with a mix (quadratic + repeated linear factor)
    >>> sol = pxsl_partial_decomp(den=[x**2 + 1, (x - 3)**2], method="advanced")
    >>> sol["letters"]
    ['A', 'B', 'C', 'D']
    >>> sol["expr"]
    (A*x + B)/(x**2 + 1) + C/(x - 3) + D/(x - 3)**2

    Identity after clearing denominators (useful to solve for coefficients)
    >>> sol = pxsl_partial_decomp(den=[x, x - 1])
    >>> sol["identity"]
    A*(x - 1) + B*x

    :pxs_trigger: décomposition en éléments simples, fraction rationnelle P(x)/Q(x), pôles simples et multiples, poser les coefficients A, B, C, trinôme irréductible au dénominateur (méthode "advanced"), identité polynomiale après multiplication
    :pxs_returns: |
        dictionnaire ``sol`` contenant :
        - ``letters`` : liste des coefficients symboliques générés ["A","B",...]
        - ``expr`` : somme symbolique ``A/den1 + B/den2 + ...`` (avec
          numérateur linéaire ``A*x+B`` pour les quadratiques irréductibles
          si ``method="advanced"``)
        - ``identity`` : polynôme obtenu en multipliant ``expr`` par le
          produit des dénominateurs (utile pour résoudre A, B, C)
        - ``num``, ``den``, ``var`` : ré-exposés pour les étapes suivantes.
    :pxs_example: |
        from sympy import Symbol
        x = Symbol('x')
        sol = pxsl_partial_decomp(den=[x, (x - 1)**2], method="simple")
        # sol["expr"]     → A/x + B/(x-1) + C/(x-1)**2
        # sol["identity"] → A*(x-1)**2 + B*x*(x-1) + C*x
    :pxs_antipattern: Créer à la main ``Symbol('A')/d1 + Symbol('B')/d2 + ...`` et boucler soi-même sur les puissances et les trinômes irréductibles à chaque exercice.
    """
    
    sol = {
        "num": num,
        "den": den,
        "letters": [],
        "expr": 0,
        "var": var,
    }
    for elem in sol["den"]:
        try:
            poly = Poly(elem, sol["var"])
        except:
            pass
        if isinstance(poly, Poly) and poly.degree() >= 2 and not pxs_is_factorable(poly) and method != "simple":
            _pxs_add_letter(sol)
            _pxs_add_letter(sol)
            sol["expr"] += (Symbol(sol["letters"][-2])*sol["var"] + Symbol(sol["letters"][-1])) / poly
        elif isinstance(elem, Pow) and elem.args[1] >= 2:
            for n in range(1, elem.exp + 1):
                _pxs_add_letter(sol)
                sol["expr"] += Symbol(sol["letters"][-1]) / elem.base**n
        else:
            _pxs_add_letter(sol)
            sol["expr"] += Symbol(sol["letters"][-1]) / elem

    sol["identity"] = simplify(sol["expr"] * Mul(*sol["den"]))

    return sol


def pxsl_decomp_sol(sol: dict, x_0, mul_symbol: str = "", par: bool = False) -> None:
    """
    Generate and store the LaTeX representation of the decomposition identity
    evaluated at a specific value of the variable.

    The result is stored directly in the solution dictionary under a dynamically
    generated key.

    Parameters
    ----------
    sol : dict
        Dictionary produced by ``pxsl_partial_decomp``.
    x_0 : int or float
        Value substituted for the main variable.
    mul_symbol : str, optional
        Multiplication symbol used in LaTeX output.
    par : bool, optional
        If True, negative values of `x_0` are enclosed in parentheses.

    Returns
    -------
    None
        The dictionary is modified in place by adding a LaTeX string.

    Examples
    --------
    >>> pxsl_decomp_sol(sol, 2)
    >>> "expr_2" in sol
    True

    :pxs_trigger: évaluation de l'identité de décomposition en éléments simples en un point x_0, méthode des valeurs particulières pour trouver A, B, C, substitution x = pôle ou x = 0/1 dans l'identité polynomiale
    :pxs_returns: |
        ``None``. Effet de bord : ajoute à ``sol`` une clé ``"expr" + str(x_0)``
        contenant la chaîne LaTeX de ``sol["identity"]`` avec la variable
        remplacée par ``x_0`` (entourée de parenthèses si ``x_0 < 0`` et
        ``par=True``), prête pour un ``\\py{...}`` dans le corrigé MyST.
    :pxs_example: |
        sol = pxsl_partial_decomp(den=[x, x - 1])
        pxsl_decomp_sol(sol, 0)
        pxsl_decomp_sol(sol, 1)
        # dans le .md : {sol["expr0"]}  et  {sol["expr1"]}
    :pxs_antipattern: Faire ``latex(sol["identity"].subs(var, x_0))`` à la main en oubliant de gérer les parenthèses pour les valeurs négatives et de stocker sous la bonne clé "expr<x_0>".
    """
    var_str = (
        myst(r"""\py{str(x_0)}""", globals(), locals())
        if x_0 >= 0 or par is False
        else myst(r"""\left(\py{str(x_0)}\right)""", globals(), locals())
    )

    sol["expr" + str(x_0)] = latex(
        sol["identity"],
        symbol_names={sol["var"]: var_str},
        mul_symbol=mul_symbol,
    )