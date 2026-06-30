# Importation des modules nécessaires

import re           # Module pour les expressions régulières
from sympy import symbols, oo, latex, Interval  # Importation des classes SymPy
from sympy import *
import random as rd
import math as m
from sympy.series.sequences import RecursiveSeq
from src.scripts.Mes_fctions.Mes_fctions_d_alg_lineaire_bis import pxsl_pow
import re  
from src.scripts.pxs_runtime import get_pxs_lang, myst

class pxs_Interval(Interval):
    """
    Classe personnalisée héritant de Interval de SymPy
    Permet un affichage formaté des intervalles avec :
    - Séparateurs de milliers pour les grands nombres
    - Notation française pour l'infini et les intervalles

    :pxs_trigger: |
    intervalle mathématique, domaine de définition, domaine d'étude,
    ensemble solution, ensemble image, image d'un intervalle par une fonction,
    tableau de variations intervalle, tableau de signes, borne,
    ]a;b[, [a;b], ]-\infty, +\infty[, intervalle ouvert fermé semi-ouvert,
    notation française intervalle, TVI intervalle de continuité,
    f\left(\left]...\\right]\\right), domaine de continuité, domaine de dérivabilité,
    intervalle de convexité, intervalle de monotonie,
    croissante sur I, décroissante sur I, continue sur I
    :pxs_returns: |
        Instance de classe héritant de sympy.Interval. À utiliser comme
        un Interval SymPy classique mais avec la méthode .print() pour
        obtenir l'affichage LaTeX francisé.
    :pxs_example: |
        I = pxs_Interval(-oo, 5, True, False)  # ]-∞ ; 5]
        # Dans MyST : $D = \\py{I.print()}$
    :pxs_antipattern: Utiliser sympy.Interval(...) puis latex() qui produit la notation anglo-saxonne (a, b].
    """
    @classmethod
    def from_Interval(cls, interval):
        """
        Convertit un Interval standard en pxs_Interval.

        :pxs_trigger: conversion Interval SymPy vers pxs_Interval, upcast intervalle, résultat solveset/domain
        :pxs_returns: |
            Une instance pxs_Interval reprenant les mêmes bornes et
            ouvertures que l'Interval SymPy fourni.
        :pxs_example: |
            I_sympy = Interval(0, 1, True, False)
            I_pxs = pxs_Interval.from_Interval(I_sympy)
            # Dans MyST : $\\py{I_pxs.print()}$
        :pxs_antipattern: Recréer manuellement pxs_Interval(I.start, I.end, I.left_open, I.right_open).
        """
        if not isinstance(interval, Interval):
            raise TypeError("L'objet fourni n'est pas un Interval")
        return cls(interval.start, interval.end,
                   left_open=interval.left_open,
                   right_open=interval.right_open)


    def print(self):
        """
        Méthode pour générer une représentation LaTeX formatée de l'intervalle
        
        Returns:
            str: Chaîne LaTeX formatée selon les conventions françaises

        :pxs_trigger: intervalle français, notation ]a,b[, borne infinie, affichage LaTeX intervalle, séparateur milliers intervalle
        :pxs_returns: |
            Chaîne LaTeX (objet myst) représentant l'intervalle avec délimiteurs
            français (]a,b[) ou anglais ((a,b)) selon pxs_lang, séparateurs de
            milliers pour les grands entiers, et \\infty pour les bornes infinies.
            À injecter dans MyST via \\py{...}.
        :pxs_example: |
            I = pxs_Interval(-oo, 1000, True, False)
            intervalle_latex = I.print()
            # Dans MyST : $x \\in \\py{intervalle_latex}$
            # Rendu FR : $x \\in \\left]-\\infty;1\\ 000\\right]$
        :pxs_antipattern: Concaténer manuellement f"]{a};{b}[" ou utiliser latex(Interval(...)) qui donne la notation anglo-saxonne (a, b).
        """
        
        # Formatage de la borne gauche si elle n'est pas -∞
        if self.left != -oo:
            # Exemple: 1000 devient "1\ 000"
            if isinstance(self.left, (int, Integer)):
                left_formate = f"{int(self.left):,}".replace(",", r"\ ")
            else:
                left_formate = latex(self.left)
        else:
            left_formate = myst(r""" -\infty """)
            
        
        # Formatage de la borne gauche si elle n'est pas -∞
        if self.right != oo:
            # Exemple: 1000 devient "1\ 000"
            if isinstance(self.right, (int, Integer)):
                right_formate = f"{int(self.right):,}".replace(",", r"\ ")
            else:
                right_formate = latex(self.right)
        else:
            right_formate = myst(r""" \inftys """)
        # Application des conventions françaises si la langue est française
        # Note: pxs_lang doit être définie ailleurs dans le programme
        pxs_lang = get_pxs_lang()
        if pxs_lang == "fr":  
            l_delim = r'\left[' if not self.left_open else r'\left]'
            r_delim = r'\right]' if not self.right_open else r'\right['
        if pxs_lang == "en":  
            l_delim = r'\left[' if not self.left_open else r'\left('
            r_delim = r'\right]' if not self.right_open else r'\right)'
        
            # Conversion des crochets selon la notation française
            # En français: ]a,b[ au lieu de (a,b) pour les intervalles ouverts
        if pxs_lang == "fr":
            Inter_latex = myst(r""" \py{l_delim}\py{left_formate};\py{right_formate}\py{r_delim} """, globals(), locals()) 
        else:
            Inter_latex = myst(r""" \py{l_delim}\py{left_formate},\py{right_formate}\py{r_delim} """, globals(), locals()) 
        
        # Retour de la chaîne LaTeX formatée
        return Inter_latex
    

# Tests
# \begin{python}
# # Code Python : Ecrivez ci-dessous votre code Python
# import sympy 
# import random as rd
# from sympy import *

# from pyxiscience.Mes_fctions_d_alg_generale import *
# from pyxiscience.Classes_Extensions import *

# \end{python}


# ## Test de la classe interval de Sympy versus l'extension de PyxiScience



# \begin{python}
# I1 = Interval(1, oo, True, True)
# I2 = Interval(1, oo, False, True)
# I3 = Interval(1, oo, False, False)
# I4 = Interval(1, oo, False, False)

# Id1 = Interval(1, 2, True, True)
# Id2 = Interval(1, 2, False, True)
# Id3 = Interval(1, 2, True, False)
# Id4 = Interval(1, 2, False, False)



# I1_latex = latex(I1)
# I2_latex = latex(I2)
# I3_latex = latex(I3)
# I4_latex = latex(I4)





# Inter_1 = pxs_Interval(1, oo, True, True)
# Inter_2 = pxs_Interval(1, oo, False, True)
# Inter_3 = pxs_Interval(1, oo, False, False)
# Inter_4 = pxs_Interval(1, oo, False, False)

# Interd_1 = pxs_Interval(1, 2, True, True)
# Interd_2 = pxs_Interval(1, 2, False, True)
# Interd_3 = pxs_Interval(1, 2, True, False)
# Interd_4 = pxs_Interval(1, 2, False, False)


# \end{python}

# $I = \py{I1}$

# C'est normal car on appelle l'objet python directement...




# ## Avec interval de Sympy


# \begin{equation*}
# &I_1 = \py{I1_latex}&
# &I_2 = \py{I2_latex}&
# &I_3 = \py{I3_latex}&
# &I_4 = \py{I4_latex}&\\

# &Id_1 = \py{Interd_1.print()}&
# &Id_2 = \py{Interd_2.print()}&
# &Id_3 = \py{Interd_3.print()}&
# &Id_4 = \py{Interd_4.print()}&
# \end{equation*}



# ## Avec pxs_interval
# \begin{equation*}
# &I_1 = \py{Inter_1.print()}&
# &I_2 = \py{Inter_2.print()}&
# &I_3 = \py{Inter_3.print()}&
# &I_4 = \py{Inter_4.print()}&\\

# &Id_1 = \py{Interd_1.print()}&
# &Id_2 = \py{Interd_2.print()}&
# &Id_3 = \py{Interd_3.print()}&
# &Id_4 = \py{Interd_4.print()}&
# \end{equation*}






#from sympy import *

class ReverseString:
    """
    Classe utilitaire pour inverser l'ordre de tri des chaînes de caractères.
    Utilisée pour trier les variables dans l'ordre inverse alphabétique.

    :pxs_trigger: tri inverse alphabétique, ordre descendant variables, clé de tri personnalisée polynôme
    :pxs_returns: |
        Wrapper autour d'une chaîne dont __lt__ est inversé, à utiliser comme
        key dans sorted() pour trier de z vers a au lieu de a vers z.
    :pxs_example: |
        vars_sorted = sorted(["y", "x", "z"], key=ReverseString)
        # → ["z", "y", "x"]
    :pxs_antipattern: Utiliser sorted(..., reverse=True) qui inverse TOUT le tri y compris la clé principale (puissance).
    """
    def __init__(self, string):
        """
        Initialise le wrapper autour de la chaîne à inverser.

        :pxs_trigger: instanciation interne classe ReverseString
        :pxs_returns: |
            Instance ReverseString encapsulant la chaîne fournie.
        :pxs_example: |
            wrap = ReverseString("x")
            # Utilisé typiquement via sorted(..., key=ReverseString)
        :pxs_antipattern: Appeler ReverseString directement dans du code pédagogique — c'est un utilitaire interne de tri.
        """
        self.string = string
    
    def __lt__(self, other):
        """
        Comparaison inversée pour le tri descendant.

        :pxs_trigger: comparaison tri inverse interne
        :pxs_returns: |
            bool : True si self.string > other.string (comparaison inversée).
        :pxs_example: |
            ReverseString("a") < ReverseString("b")  # False (car 'a' < 'b' devient inversé)
        :pxs_antipattern: Appeler __lt__ directement au lieu de laisser Python l'utiliser via sorted().
        """
        return self.string > other.string  # Inversion de la comparaison
    
    def __eq__(self, other):
        """
        Égalité standard entre chaînes.

        :pxs_trigger: égalité interne ReverseString
        :pxs_returns: |
            bool : True si les deux chaînes encapsulées sont identiques.
        :pxs_example: |
            ReverseString("x") == ReverseString("x")  # True
        :pxs_antipattern: Appeler __eq__ directement au lieu d'utiliser ==.
        """
        return self.string == other.string

class pxs_Poly(Poly):
    """
    Extension de la classe Poly de SymPy avec une méthode d'affichage personnalisée.
    Permet d'afficher les polynômes avec un formatage LaTeX personnalisé et une factorisation optionnelle.

    :pxs_trigger: polynôme pédagogique, trinôme second degré, affichage LaTeX polynôme, discriminant racines factorisation
    :pxs_returns: |
        Classe héritant de sympy.Poly, avec méthodes pxsl_print, pxsl_discriminant,
        pxsl_solution, pxs_factor et pxs_generate pour usage pédagogique en MyST.
    :pxs_example: |
        p = pxs_Poly(x**2 + 3*x - 4, x)
        # Dans MyST : $P(x) = \\py{p.pxsl_print()}$
    :pxs_antipattern: Utiliser sympy.Poly puis latex() et écrire à la main le calcul du discriminant ou des racines.
    """

    @classmethod
    def pxs_generate(cls, x = Symbol("x"), lim_coeff = 9, nb_root = None):
        """
        Génère un polynôme du second degré avec des coefficients aléatoires non nuls,
        en contrôlant optionnellement le nombre de racines réelles.
    
        Args:
            x: Variable symbolique du polynôme (par défaut Symbol("x"))
            lim_coeff: Valeur maximale absolue des coefficients (par défaut 9)
            nb_root: Nombre de racines réelles souhaité (0, 1, 2 ou None pour aléatoire)
        
        Returns:
            Un objet pxs_Poly représentant le polynôme ax² + bx + c généré

        :pxs_trigger: générer trinôme aléatoire, exercice second degré avec n racines, discriminant positif/négatif/nul contrôlé
        :pxs_returns: |
            Un objet pxs_Poly de la forme ax² + bx + c avec a, b, c entiers
            non nuls, et discriminant contrôlé selon nb_root (0, 1, 2 ou aléatoire).
        :pxs_example: |
            p = pxs_Poly.pxs_generate(nb_root=2)
            # Trinôme à 2 racines réelles distinctes, coeffs dans [-9,9]\\{0}
            # Dans MyST : $P(x) = \\py{p.pxsl_print()}$
        :pxs_antipattern: Tirer a, b, c au hasard avec random.randint puis vérifier le signe du discriminant dans une boucle while.
        """
        # Génération aléatoire des signes pour chaque coefficient
        sign_coeff = [rd.choice([-1,1]), rd.choice([-1,1]), rd.choice([-1,1])]

        # Génération des coefficients a, b, c (tous non nuls)
        # Valeurs entre 1 et lim_coeff, multipliées par leur signe
        a = sign_coeff[0] * rd.randint(1, lim_coeff)
        b = sign_coeff[1] * rd.randint(1, lim_coeff)
        c = sign_coeff[2] * rd.randint(1, lim_coeff)

        # Création du polynôme initial
        p = Poly(a * x**2 + b * x + c, x)
        
        # Si aucune contrainte sur le nombre de racines, retourner le polynôme tel quel
        if nb_root is None:
            return p

        # CAS 1 : On veut 0 racine réelle (Δ < 0)
        # Condition : b² < 4ac, donc a et c doivent être de même signe
        if nb_root == 0 and p.discriminant() >= 0:
            # Forcer a et c à avoir le même signe (on utilise sign[0] pour les deux)
        	c = sign_coeff[0] * rd.randint(1,9)
            # Choisir b tel que b < 2√(ac) pour garantir Δ < 0
        	b = sign_coeff[1] * rd.randint(1, int(2 * m.sqrt(a * c)-1))

        # CAS 2 : On veut 1 racine double (Δ = 0)
        # Condition : b² = 4ac, donc b = ±2√(ac)
        if nb_root == 1 and p.discriminant() != 0:
            # Pour faciliter, on choisit a et c comme des carrés parfaits
            a = sign_coeff[0] * rd.randint(1, int(m.sqrt(lim_coeff)))**2
            c = sign_coeff[0] * rd.randint(1, int(m.sqrt(lim_coeff)))**2
            
            # Vérifier qu'on ne dépasse pas la limite des coefficients
            if a >= lim_coeff and c >= lim_coeff:
                # Si les deux sont trop grands, prendre des valeurs égales plus petites
                a = sign_coeff[0] * rd.randint(1, lim_coeff)
                c = a

            # Calculer b pour avoir exactement Δ = 0
            b = rd.choice([-1,1]) * int(2 * m.sqrt(a * c))

        # CAS 3 : On veut 2 racines distinctes (Δ > 0)
        # Condition : b² > 4ac, donc c < b²/(4a)
        if nb_root == 2 and p.discriminant() <= 0 :
            # Choisir c dans l'intervalle qui garantit Δ > 0
            # c doit être inférieur à b²/(4a) - 1 pour avoir une marge
            c = sign_coeff[2] * rd.randint(-lim_coeff, min(int(b**2 / (4 * a)) - 1, lim_coeff)) 
            
            # S'assurer que c n'est pas nul (tous les coefficients doivent être non nuls)
            while c == 0:
                c = sign_coeff[0] * rd.randint(-lim_coeff, int(b**2 / (4 * a)) - 1) 

        # Retourner le polynôme avec les coefficients ajustés
        return cls(a * x**2 + b * x + c, x)
    
    def pxsl_print(self, variable=None, ascending=False, displaystyle=True, factor=False):
        """
        Affiche le polynôme avec un formatage LaTeX personnalisé.
        
        Paramètres:
        - variable: Variable principale pour l'organisation/factorisation (None = auto-détection)
        - ascending: Si True, trie par puissances croissantes, sinon décroissantes
        - displaystyle: Si True, utilise le style d'affichage LaTeX étendu
        - factor: Si True, factorise le polynôme par rapport à la variable spécifiée
        
        Retourne:
        - String: Expression LaTeX formatée

        :pxs_trigger: afficher polynôme pédagogique, ordre puissances croissantes/décroissantes, factoriser par variable, polynôme deux variables
        :pxs_returns: |
            Chaîne LaTeX (str) représentant le polynôme avec termes triés selon
            'variable' et 'ascending', coefficients 1/-1 simplifiés, et
            optionnellement factorisé par 'variable' si factor=True.
        :pxs_example: |
            p = pxs_Poly(3*x*y - x**2 + y**2 + x + 2)
            # Dans MyST : $P = \\py{p.pxsl_print(variable=x)}$
            # Avec factor=True : $P = \\py{p.pxsl_print(variable=x, factor=True)}$
        :pxs_antipattern: Utiliser latex(poly.as_expr()) qui trie mal les termes multi-variables et n'offre pas la factorisation par variable.
        """
        
        def is_numeric_key(key):
            """
            Vérifie si une clé est numérique (pour filtrer les constantes).
            Utilisée pour séparer les variables des constantes numériques.
            """
            try:
                float(key)
                return True
            except (ValueError, TypeError):
                return False

        # Convertir le polynôme en expression SymPy
        expr = self.as_expr()

        # Auto-détection de la variable si non spécifiée
        if variable is None:
            variables = sorted(expr.free_symbols, key=str)
            if not variables: 
                return latex(expr)  # Retourne directement si pas de variables
        else:
            variables = variable 
    
        # MODE FACTORISATION : traitement spécial quand factor=True
        if factor and variable is not None:
            # Utilise la fonction collect() de SymPy pour factoriser par la variable
            factored_expr = collect(expr, variable)
            
            # Dictionnaire pour organiser les termes par puissance de la variable
            terms_by_power = {}
            constant_terms = []  # Termes qui ne contiennent pas la variable
            
            # Analyser chaque terme de l'expression factorisée
            for term in Add.make_args(factored_expr):
                if term.has(variable):
                    # Trouver la puissance de la variable dans ce terme
                    power = 0
                    coeff = term
                    
                    # Recherche de la puissance (de 10 à 1 pour prendre la plus haute)
                    for p in range(10, 0, -1):
                        c = term.coeff(variable, p)  # Coefficient de variable^p
                        if c != 0:
                            power = p
                            coeff = c
                            break
                    
                    # Stocker le coefficient pour cette puissance
                    if power > 0:
                        terms_by_power[power] = coeff
                else:
                    # Terme constant (ne contient pas la variable)
                    constant_terms.append(term)
            
            # Construction de l'affichage avec la variable APRÈS le coefficient
            result_terms = []
            
            # Traiter les termes par puissance décroissante
            for power in sorted(terms_by_power.keys(), reverse=True):
                coeff = terms_by_power[power]
                
                if power == 1:
                    # Cas spécial : puissance 1 (pas d'exposant affiché)
                    if coeff == 1:
                        result_terms.append(f"{latex(variable)}")
                    elif coeff == -1:
                        result_terms.append(f"-{latex(variable)}")
                    else:
                        coeff_str = latex(coeff)
                        # Ajouter des parenthèses si le coefficient est complexe
                        if len(str(coeff).split()) > 1 or '+' in coeff_str or '-' in coeff_str[1:]:
                            result_terms.append(f"({coeff_str}){latex(variable)}")
                        else:
                            result_terms.append(f"{coeff_str}{latex(variable)}")
                else:
                    # Puissances supérieures à 1
                    if coeff == 1:
                        result_terms.append(f"{latex(variable)}^{{{power}}}")
                    elif coeff == -1:
                        result_terms.append(f"-{latex(variable)}^{{{power}}}")
                    else:
                        coeff_str = latex(coeff)
                        # Ajouter des parenthèses si le coefficient est complexe
                        if len(str(coeff).split()) > 1 or '+' in coeff_str or '-' in coeff_str[1:]:
                            result_terms.append(f"({coeff_str}){latex(variable)}^{{{power}}}")
                        else:
                            result_terms.append(f"{coeff_str}{latex(variable)}^{{{power}}}")
            
            # Ajouter les termes constants à la fin
            for term in constant_terms:
                result_terms.append(latex(term))
            
            # Assemblage final avec gestion des signes
            if not result_terms:
                return "0"
            
            result = result_terms[0]
            for term in result_terms[1:]:
                if term.startswith('-'):
                    result += term  # Pas de '+' avant un terme négatif
                else:
                    result += f"+{term}"
            
            return result
    
        # MODE NORMAL : affichage standard sans factorisation
        terms = []
        
        # Analyser chaque terme de l'expression pour extraire puissances et coefficients
        for term in Add.make_args(expr):
            power = 0  # Puissance de la variable principale (0 pour les constantes)
            rest = 1   # Coefficient/reste du terme
            
            # Traitement quand aucune variable n'est spécifiée (auto-détection)
            if variable is None:
                powers = 0  # Somme de toutes les puissances du terme (pour le tri)
                entire_power_dict = term.as_powers_dict()
                
                # Filtrer les clés numériques (constantes)
                keys_to_remove = []
                for key in entire_power_dict.keys():
                    try:
                        float(key)
                        keys_to_remove.append(key)
                    except (ValueError, TypeError):
                        pass  # La clé n'est pas numérique, on la garde
                
                # Créer un dictionnaire sans les constantes numériques
                power_dict = {k: v for k, v in entire_power_dict.items() if not is_numeric_key(k)}
                
                try:
                    # Choisir la variable "principale" (la plus grande alphabétiquement)
                    variable = max(power_dict.keys())
                    power = power_dict[variable]
                    rest = term / (variable ** power) if variable else term
                except (ValueError, TypeError):
                    # Pas de variable trouvée, c'est un terme constant
                    variable = None
                    rest = term
                
                # Calculer la somme totale des puissances pour le tri
                powers = sum(power_dict.values())
                terms.append((powers, power, variable, False, rest))
                variable = None  # Reset pour le prochain terme
                
            else:
                # Variable spécifiée : analyser chaque facteur du terme
                for factor in Mul.make_args(term):
                    if factor.has(variable):
                        # Ce facteur contient la variable
                        power_dict = factor.as_powers_dict()
                        power = power_dict[variable]
                        # Diviser par la variable à la puissance pour isoler le coefficient
                        rest *= factor / (variable ** power)
                    else:
                        # Ce facteur ne contient pas la variable, c'est part du coefficient
                        rest *= factor
                
                # Déterminer si le terme contient d'autres variables (pour le tri)
                if variable is not None:
                    has_other_var = False
                    if len(expr.free_symbols) > 1:
                        # Vérifie si le coefficient contient d'autres variables
                        has_other_var = len(rest.free_symbols) > 0
            
                    terms.append((power, power, variable, has_other_var, rest))
    
        # TRI DES TERMES selon les paramètres spécifiés
        if variable is None:
            # Tri global par somme des puissances, puis par puissance individuelle, puis par nom de variable
            if ascending:
                terms.sort(key=lambda x: (x[0], x[1], ReverseString(str(x[2]))))
            else:
                terms.sort(key=lambda x: (x[0], x[1], ReverseString(str(x[2]))), reverse=True)
        else:
            # Tri par puissance de la variable spécifiée
            if ascending:
                # Ordre croissant des puissances, termes avec autres variables après
                terms.sort(key=lambda x: (x[1], x[3]))
            else:
                # Ordre décroissant des puissances, termes avec autres variables après
                terms.sort(key=lambda x: (x[1], x[3]), reverse=True)
    
        # CONSTRUCTION DE L'EXPRESSION LATEX FINALE
        result = ""
    
        for i, (powers, power, variable, has_other_var, coeff) in enumerate(terms):
            # Analyse du coefficient pour la gestion des signes
            is_negative = latex(coeff).startswith('-')

            # Vérification si le coefficient est +1 ou -1 (pour simplifier l'affichage)
            try:
                is_One = coeff == 1
            except TypeError:
                is_One = False
            try:
                is_minus_One = coeff == -1
            except TypeError:
                is_minus_One = False
        
            # CONSTRUCTION DU TERME selon sa puissance
            if power == 0:
                # Terme constant (pas de variable)
                term = f"{latex(coeff)}"
            elif power == 1:
                # Puissance 1 (variable sans exposant)
                if is_One:
                    term = f"{latex(variable)}"
                elif is_minus_One:
                    term = f"-{latex(variable)}"
                else:
                    if displaystyle:
                        term = f"\\displaystyle {latex(coeff)}{latex(variable)}"
                    else:
                        term = f"{latex(coeff)}{latex(variable)}"
            else:
                # Puissances supérieures à 1
                if is_One:
                    term = f"{latex(variable)}^{power}"
                elif is_minus_One:
                    term = f"-{latex(variable)}^{power}"
                else:
                    if displaystyle:
                        term = f"\\displaystyle {latex(coeff)}{latex(variable)}^{power}"
                    else:
                        term = f"{latex(coeff)}{latex(variable)}^{power}"
        
            # GESTION DES SIGNES pour l'assemblage final
            if i == 0 or is_negative:
                # Premier terme ou terme négatif : pas de '+' devant
                result += term
            else:
                # Terme positif : ajouter un '+'
                result += f" +{term}"
    
        # Retourner l'expression LaTeX complète
        return result
    
    def pxsl_discriminant(self, mult = "\\times", formula = True):
        """
        Calcule et affiche le discriminant d'une équation du second degré au format LaTeX.
    
        Args:
            mult: Symbole de multiplication à utiliser (par défaut \times en LaTeX)
    
        Returns:
            Un objet myst contenant l'affichage LaTeX du calcul du discriminant

        :pxs_trigger: calcul discriminant, Delta = b²-4ac, étapes substitution trinôme, exercice second degré
        :pxs_returns: |
            Objet myst contenant le calcul multi-lignes du discriminant au
            format LaTeX aligné (utilisable dans un environnement equation*+split),
            avec ou sans la formule littérale Δ = b²-4ac en première ligne.
        :pxs_example: |
            p = pxs_Poly(x**2 - 5*x + 6, x)
            calc = p.pxsl_discriminant()
            # Dans MyST :
            # \\begin{equation*}\\begin{split}
            # \\py{calc}
            # \\end{split}\\end{equation*}
        :pxs_antipattern: Écrire à la main "\\Delta = b^2-4ac = {b**2} - 4*{a}*{c} = ..." avec f-strings et risquer les signes négatifs mal parenthésés.
        """
        # Récupération de tous les coefficients de l'équation (a, b, c)
        coeffs = self.all_coeffs()

        # Génération de l'affichage LaTeX du calcul du discriminant
        # avec les étapes de substitution et de calcul
        if formula:
            return myst(r""" 
        \Delta &= b^2-4ac\\
        &= \py{pxsl_pow(coeffs[1],2)} - 4 \py{mult}\py{pxsl_pow(coeffs[0],1)} \py{mult}\py{pxsl_pow(coeffs[2],1)}\\
        &=\py{latex(self.discriminant())}"""
        ,globals(), locals())
        else:
            return myst(r""" 
        \Delta &= \py{pxsl_pow(coeffs[1],2)} - 4 \py{mult}\py{pxsl_pow(coeffs[0],1)} \py{mult}\py{pxsl_pow(coeffs[2],1)}\\
        &=\py{latex(self.discriminant())}"""
        ,globals(), locals())

    def pxsl_solution(self, mult = "\\times", formula = True):
        """
        Affiche la ou les solutions d'une équation du second degré au format LaTeX.

        Args:
            mult: Symbole de multiplication à utiliser (par défaut \times en LaTeX)

        Returns:
            Un tuple de 4 éléments (x1_complet, x2_complet, x1_final, x2_final) où :
            - x1_complet, x2_complet : calculs détaillés étape par étape
            - x1_final, x2_final : formes finales simplifiées
            Retourne (None, None, None, None) si pas de solution réelle

        :pxs_trigger: résoudre équation second degré, racines trinôme, x1 x2, formule (-b±√Δ)/2a, solution double
        :pxs_returns: |
            Tuple (x_1_complet, x_2_complet, x_1_final, x_2_final) d'objets myst :
            les deux premiers contiennent le calcul détaillé étape par étape,
            les deux derniers la forme simplifiée finale. Si Δ=0, les deux
            solutions sont égales. Si Δ<0, retourne (None, None, None, None).
        :pxs_example: |
            p = pxs_Poly.pxs_generate(nb_root=2)
            expr_x1, expr_x2, x1, x2 = p.pxsl_solution()
            # Dans MyST :
            # $x_1 = \\py{expr_x1}$, $x_2 = \\py{expr_x2}$
            # Finalement : $x_1 = \\py{x1}$ et $x_2 = \\py{x2}$
        :pxs_antipattern: Calculer sqrt(disc) puis composer une f-string "-b - sqrt(D) / 2a" à la main, en oubliant la simplification des fractions ou la réduction de √Δ.
        """
        # Récupération de tous les coefficients de l'équation (a, b, c)
        coeffs = self.all_coeffs()

        # Vérifier si le discriminant peut être simplifié (contient des facteurs carrés)
        factors = factorint(self.discriminant())
        is_reducible = False
        for prime, power in factors.items():
            if power >= 2:
                is_reducible = True
    
        # Préparer l'affichage des coefficients avec parenthèses si négatifs
        if self.discriminant() >= 0:
            coeff_fin = [pxsl_pow(coeff, 1) for coeff in coeffs]
        
        # CAS 1 : Discriminant strictement positif (2 solutions distinctes)
        if self.discriminant() > 0:
            # Calcul détaillé de x1 = (-b - √Δ) / 2a
            if formula:
                x_1 = myst(r""" \displaystyle{\frac{-b-\sqrt{\Delta}}{2a}}=\displaystyle{\frac{-\py{coeff_fin[1]}-\sqrt{\py{self.discriminant()}}}{2\py{mult}\py{coeff_fin[0]}}}=\displaystyle{\frac{\py{-coeffs[1]}-\py{latex(sqrt(self.discriminant()))}}{\py{2*coeffs[0]}}}""",globals(), locals())
            else:
                x_1 = myst(r""" \displaystyle{\frac{-\py{coeff_fin[1]}-\sqrt{\py{self.discriminant()}}}{2\py{mult}\py{coeff_fin[0]}}}=\displaystyle{\frac{\py{-coeffs[1]}-\py{latex(sqrt(self.discriminant()))}}{\py{2*coeffs[0]}}}""",globals(), locals())
        
            # Calcul détaillé de x2 = (-b + √Δ) / 2a
            if formula:
                x_2 = myst(r""" \displaystyle{\frac{-b+\sqrt{\Delta}}{2a}}=\displaystyle{\frac{-\py{coeff_fin[1]}+\sqrt{\py{self.discriminant()}}}{2\py{mult}\py{coeff_fin[0]}}}=\displaystyle{\frac{\py{-coeffs[1]}+\py{latex(sqrt(self.discriminant()))}}{\py{2*coeffs[0]}}}""",globals(), locals())
            else:
                x_2 = myst(r""" \displaystyle{\frac{-\py{coeff_fin[1]}+\sqrt{\py{self.discriminant()}}}{2\py{mult}\py{coeff_fin[0]}}}=\displaystyle{\frac{\py{-coeffs[1]}+\py{latex(sqrt(self.discriminant()))}}{\py{2*coeffs[0]}}}""",globals(), locals())
        
            # Si √Δ est un entier (carré parfait), calculer directement les fractions
            if isinstance(sqrt(self.discriminant()),Integer) or isinstance(sqrt(self.discriminant()),Rational):
                x_1 += myst(r""" =\displaystyle{\frac{\py{latex(-coeffs[1]-sqrt(self.discriminant()))}}{\py{2*coeffs[0]}}}""",globals(), locals())
                x_1final = myst(r"""\displaystyle{\py{latex(Rational(-coeffs[1]-sqrt(self.discriminant()),2*coeffs[0]))}} """,globals(), locals())
                x_2 += myst(r""" =\displaystyle{\frac{\py{latex(-coeffs[1]+sqrt(self.discriminant()))}}{\py{2*coeffs[0]}}}""",globals(), locals())
                x_2final = myst(r"""\displaystyle{\py{latex(Rational(-coeffs[1]+sqrt(self.discriminant()),2*coeffs[0]))}} """,globals(), locals())
                return x_1 + myst(r"""= """) + x_1final, x_2 + myst(r""" = """) + x_2final, x_1final, x_2final
        
            # Si √Δ n'est pas un entier, essayer de simplifier l'expression
            else:
                # Si a > 0 et qu'on peut simplifier (PGCD ou racine réductible)
                if coeffs[0] > 0 and (gcd(-coeffs[1],2*coeffs[0]) != 1 or is_reducible):
                    # Séparer la partie rationnelle et la partie irrationnelle
                    x_1final = myst(r"""\displaystyle{\py{latex(Rational(-coeffs[1],2*coeffs[0]))}-\py{latex(sqrt(self.discriminant())/(2*coeffs[0]))}}""", globals(), locals())
                    x_2final = myst(r"""\displaystyle{\py{latex(Rational(-coeffs[1],2*coeffs[0]))}+\py{latex(sqrt(self.discriminant())/(2*coeffs[0]))}}""", globals(), locals())
                    return x_1 + myst(r"""=""") + x_1final, x_2 + myst(r"""=""") + x_2final, x_1final, x_2final
            
                # Si a < 0, ajuster les signes pour un affichage plus propre
                elif coeffs[0] < 0 :
                    x_1final = myst(r"""\displaystyle{\py{latex(Rational(-coeffs[1],2*coeffs[0]))}+\py{latex(sqrt(self.discriminant())/(-2*coeffs[0]))}}""", globals(), locals())
                    x_2final = myst(r"""\displaystyle{\py{latex(Rational(-coeffs[1],2*coeffs[0]))}-\py{latex(sqrt(self.discriminant())/(-2*coeffs[0]))}}""", globals(), locals())
                    return x_1 + myst(r"""= """) + x_1final, x_2 + myst(r"""= """) + x_2final, x_1final, x_2final
            
                # Cas par défaut : garder la forme fractionnaire complète
                else:
                    x_1final = myst(r"""\displaystyle{\frac{\py{-coeffs[1]}-\py{latex(sqrt(self.discriminant()))}}{\py{2*coeffs[0]}}}""",globals(), locals())
                    x_2final = myst(r"""\displaystyle{\frac{\py{-coeffs[1]}+\py{latex(sqrt(self.discriminant()))}}{\py{2*coeffs[0]}}}""",globals(), locals())
                    return x_1, x_2, x_1final, x_2final
    
        # CAS 2 : Discriminant nul (1 solution double)
        if self.discriminant() == 0:
            # Calcul détaillé de x0 = -b / 2a
            x_0 = myst(r""" \displaystyle{\frac{-b}{2a}}=\displaystyle{\frac{-\py{coeff_fin[1]}}{2\py{mult}\py{coeff_fin[0]}}}=\displaystyle{\frac{\py{-coeffs[1]}}{\py{2*coeffs[0]}}}""",globals(), locals())
        
            # Si on peut simplifier la fraction (PGCD > 1 ou a < 0)
            if coeffs[0] > 0 and gcd(-coeffs[1],2*coeffs[0]) != 1:
                x_0final = myst(r"""\displaystyle{\py{latex(Rational(-coeffs[1],2*coeffs[0]))}}""", globals(), locals())
                return x_0 + myst(r"""= """) + x_0final, x_0 + myst(r"""= """) + x_0final, x_0final, x_0final
            elif coeffs[0] < 0 :
                x_0final = myst(r"""\displaystyle{\py{latex(Rational(-coeffs[1],2*coeffs[0]))}}""", globals(), locals())
                return x_0 + myst(r"""= """) + x_0final, x_0 + myst(r"""= """) + x_0final, x_0final, x_0final
        
            # Cas par défaut : garder la forme fractionnaire
            else:
                x_0final = myst(r"""\displaystyle{\frac{\py{-coeffs[1]}}{\py{2*coeffs[0]}}}""",globals(), locals())
                return x_0, x_0, x_0final, x_0final
    
        # CAS 3 : Discriminant négatif (pas de solution réelle)
        if self.discriminant() < 0:
            return None, None, None, None

    def pxs_factor(self, variable = None, display = "\displaystyle"):
        """
        Factorise un polynôme en utilisant sympy.Poly.
        Prend un objet Poly en argument.

        :pxs_trigger: factoriser polynôme par variable dominante, mise en facteur x^n, x²(1 + 1/x + 1/x²), factorisation forcée par plus haut degré
        :pxs_returns: |
            Tuple (myst_expr, factor, term) :
            - myst_expr : chaîne LaTeX "x^n (1 + a/x + ... )" prête à injecter en MyST
            - factor : expression sympy du facteur sorti (variable ** degré)
            - term : expression sympy du contenu entre parenthèses
        :pxs_example: |
            p = pxs_Poly(3*x**2 + 2*x + 1, x)
            expr, fact, term = p.pxs_factor(variable=x)
            # Dans MyST : $P = \\py{expr}$  →  $x^2(3 + 2/x + 1/x^2)$
        :pxs_antipattern: Utiliser sympy.factor() qui cherche une factorisation complète sur Q, ou construire la mise en facteur de x^n à la main avec des f-strings.
        """
    
        # Récupérer la variable (premier générateur)
        if variable is None and len(self.gens) != 1:
            raise ValueError("Il faut spécifier une variable pour factoriser un polynôme à plusieurs variables")
        if variable is None:
            variable = self.gens[0]  # si variable n'est précisé c'est qu'il n'y en a qu'une, on la récupère

        p = pxs_Poly(self, variable)
    
    # Récupérer tous les coefficients (SymPy gère automatiquement l'ordre)
        coeffs = p.all_coeffs()  # Coefficients dans l'ordre décroissant des puissances
        degree_poly = p.degree()
    
        if degree_poly == 0:
            return str(coeffs[0])

        # renvoyer le même terme si y en a qu'un
    
    # Construire la factorisation
        factorized_form = myst(r"""""")
        term = 0
    
    # Parcourir tous les coefficients depuis la plus haute puissance
        for i, coeff in enumerate(coeffs):
            if coeff == 0:
                continue
            current_power = degree_poly - i
        
        # Coefficient relatif au terme principal
            power_diff = degree_poly - current_power
            
        # Gestion du signe
            try:
                if coeff > 0 and i != 0:
                    sign_coeff = "+"
                else:
                    sign_coeff = ""
            except:
                coeff_str = str(coeff)
                if i != 0 and not coeff_str.startswith('-'):
                    sign_coeff = "+"
                else:
                    sign_coeff = ""
            
        # Formatage selon la différence de puissance
            if i == 0:
                term +=coeff
                factorized_form += myst(r"""\py{latex(coeff)}""", globals(), locals())
                continue
            if power_diff == 1:
                term += coeff/variable
            # Division par variable
                if coeff == 1:
                    factorized_form += myst(r"""\py{sign_coeff}\py{display}\py{latex(1/variable)}""", globals(), locals())
                elif coeff == -1:
                    factorized_form += myst(r"""-\py{display}\py{latex(1/variable)}""", globals(), locals())
                else:
                    factorized_form += myst(r"""\py{sign_coeff} \py{display}\py{latex(coeff/variable)}""", globals(), locals())
            else:
                term += coeff/(variable**power_diff)
            # Division par variable^power_diff
                if coeff == 1:
                    factorized_form += myst(r"""\py{sign_coeff}\py{display}\py{latex(1/variable**power_diff)}""", globals(), locals())
                elif coeff == -1:
                    factorized_form += myst(r"""-\py{display}\py{latex(1/variable**power_diff)}""", globals(), locals())
                else:
                    factorized_form += myst(r"""\py{sign_coeff}\py{display}\py{latex(coeff/variable**power_diff)}""", globals(), locals())
    
        # Construire le facteur principal
        factor = variable**degree_poly
        factor_latex = myst(r"""\py{pxsl_pow(variable, degree_poly)}""", globals(), locals())
    
        return myst(r"""\py{factor_latex}\left(\py{factorized_form}\right) """, globals(), locals()), factor, term
    
""" X = Symbol('X')
y = Symbol('y')
x = Symbol('x')
poly = pxs_Poly(3*x**4*y**2+Rational(2,3)*x**2*y+3, x)
poly2 = pxs_Poly(3*x**4*y**2+Rational(2,3)*x**2*y+3)

p1 = pxs_Poly.pxs_generate(nb_root = 2)
p2 = pxs_Poly.pxs_generate(nb_root = 1)
p3 = pxs_Poly.pxs_generate(nb_root = 0)

expr1 = pxs_Poly(1 + x + x**2)
expr2 = pxs_Poly(3*x**2 - 5*x + 7 - 2*x**3)
expr3 = pxs_Poly(3*x*y - x**2 + y**2 + x + 2)
expr4 = pxs_Poly(x/2 - x**2/3 + 5)
expr5 = pxs_Poly(3*X*y + 2*X**2 + y**2 + X + 2)
expr6 = pxs_Poly(3*x**4*y**2+Rational(2,3)*x**2 +x**2*y+3,x)

poly = pxs_Poly.pxs_generate(nb_root = 2)
[expr_x1, expr_x2, x1, x2] = poly.pxsl_solution()
poly = pxs_Poly.pxs_generate(nb_root = 1)
[expr_x0, expr_x0, x0, x0] = poly.pxsl_solution()

\end{python}

Méthode pxs_generate(cls, x = Symbol("x"), lim_coeff = 9, nb_root = None)

$\py{latex(pxs_Poly.pxs_generate().as_expr())}$

$\py{latex(pxs_Poly.pxs_generate(y).as_expr())}$

Modifier la limite des coefficients : $\py{latex(pxs_Poly.pxs_generate(lim_coeff = 2).as_expr())}$

2 racines : $\py{latex(p1.as_expr())}$ $\longrightarrow$ $\Delta = \py{p1.discriminant()}$

1 racine : $\py{latex(p2.as_expr())}$ $\longrightarrow$ $\Delta = \py{p2.discriminant()}$

0 racine : $\py{latex(p3.as_expr())}$ $\longrightarrow$ $\Delta = \py{p3.discriminant()}$

________________________________________________

Méthode pxsl_print(self, variable=None, ascending=False, displaystyle=True, factor = False)

expr1: $\py{expr1.pxsl_print()}$

expr1 en ordre croissant: $\py{expr1.pxsl_print(ascending = True)}$

expr2: $\py{expr2.pxsl_print()}$

expr3: $\py{expr3.pxsl_print()}$

Par rapport à x : $\py{expr3.pxsl_print(variable = x)}$

Par rapport à y : $\py{expr3.pxsl_print(variable = y)}$

expr4: $\py{expr4.pxsl_print()}$

expr4, sans displaystyle: $\py{expr4.pxsl_print(displaystyle = False)}$

expr5: $\py{expr5.pxsl_print()}$

Par rapport à X : $\py{expr5.pxsl_print(variable = X)}$

expr6, Forme développée : $\py{expr6.pxsl_print(factor=False, variable=x)}$

expr6, Forme factorisée en x : $\py{expr6.pxsl_print(factor=True, variable=x)}$
_________________________________________________________

Méthode pxsl_discriminant(self, mult = "\\times")

expr1: 
\begin{equation*}
\begin{split}
\py{expr1.pxsl_discriminant()}
\end{split}
\end{equation*}

expr4: 
\begin{equation*}
\begin{split}
\py{expr4.pxsl_discriminant()}
\end{split}
\end{equation*}

en modifiant le signe multiplié :
\begin{equation*}
\begin{split}
\py{expr4.pxsl_discriminant("\cdot")}
\end{split}
\end{equation*}
_____________________________________________________________

Méthode pxsl_solution(self, mult = "\\times")

2 racines :

\begin{equation*}
x_1 = \py{expr_x1}
\end{equation*}
et
\begin{equation*}
x_2 = \py{expr_x2}.
\end{equation*}

\begin{equation*}
x_1 =\py{x1}\textrm{ et }x_2 = \py{x2}.
\end{equation*}

1 racine : 

\begin{equation*}
x_0 = \py{expr_x0}
\end{equation*}

\begin{equation*}
x_0 =\py{x0}.
\end{equation*}
____________________________________________________________

Méthode pxs_factor(self, variable = None, display = "\displaystyle")

expr1 : $\py{expr1.pxs_factor()[0]}$

factor : $\py{latex(expr1.pxs_factor(variable = x)[1])}$

term : $\py{latex(expr1.pxs_factor(variable = x)[2])}$

expr3: $\py{expr3.pxsl_print()}$

expr3 par rapport à $x$: $\py{expr3.pxs_factor(variable = x)[0]}$

factor : $\py{latex(expr3.pxs_factor(variable = x)[1])}$

term : $\py{latex(expr3.pxs_factor(variable = x)[2])}$

expr3 par rapport à $y$: $\py{expr3.pxs_factor(variable = y)[0]}$

factor : $\py{latex(expr3.pxs_factor(variable = y)[1])}$

term : $\py{latex(expr3.pxs_factor(variable = y)[2])}$
 """



class pxs_SeqFormula(SeqFormula):
    """
    Sous-classe de SeqFormula offrant une méthode de sommation des coefficients.
    La méthode pxsl_summation produit une expression (myst) représentant
    la somme des coefficients de la suite entre deux indices, soit en valeur
    numérique, soit en notation symbolique.

    :pxs_trigger: suite numérique, suite avec somme, SeqFormula pédagogique, somme développée termes successifs
    :pxs_returns: |
        Classe héritant de sympy.SeqFormula, offrant en plus la méthode
        pxsl_summation pour afficher la somme u_min + u_{min+1} + ... + u_{max-1}
        en LaTeX (valeurs numériques ou notation symbolique u_i).
    :pxs_example: |
        u = pxs_SeqFormula(n**2, (n, 0, oo))
        # Dans MyST : $S = \\py{u.pxsl_summation(0, 5)}$
    :pxs_antipattern: Utiliser sympy.SeqFormula puis écrire la somme à la main sans simplification des signes.
    """
    def pxsl_summation(self, min=0, max=9, symbolic=None):
        """
        Génère l'expression de la somme des coefficients u_min + u_{min+1} + ... + u_{max-1}.

        Paramètres:
        - min (int) : indice de départ de la sommation (inclu).
        - max (int) : indice de fin de la sommation (exclu).
        - symbolic (str ou None) : nom du symbole à utiliser pour la notation symbolique;
          si None, on utilise self.coeff(i) pour extraire les valeurs numériques.

        Retourne:
        - expr : un objet myst contenant la somme formatée.

        :pxs_trigger: somme développée suite, u_0 + u_1 + ... + u_n, écriture symbolique ou numérique d'une somme partielle
        :pxs_returns: |
            Objet myst (LaTeX) de la somme développée : soit les valeurs
            numériques des termes avec gestion correcte des signes (+/-),
            soit la notation symbolique "symbolic_0 + symbolic_1 + ...".
        :pxs_example: |
            u = pxs_SeqFormula(2*n + 1, (n, 0, oo))
            somme = u.pxsl_summation(0, 4)  # "1 +3 +5 +7"
            somme_sym = u.pxsl_summation(0, 4, symbolic="u")  # "u_0 + u_1 + u_2 + u_3"
            # Dans MyST : $\\py{somme}$
        :pxs_antipattern: Boucler manuellement en f-string sans gérer le signe (produit "1 + -3" au lieu de "1 - 3").
        """
        if symbolic is None:
            # Cas numérique : on ajoute la valeur de chaque coefficient
            expr = myst(r"""\py{self.coeff(min)} """, globals(), locals())
            for i in range(min + 1, max):
                coeff_i = self.coeff(i)  # on récupère le coefficient numérique
                if coeff_i >= 0:
                    # Ajoute '+ coeff_i' si coefficient positif
                    expr += myst(r""" +\py{coeff_i} """, globals(), locals())
                else:
                    # Ajoute '- |coeff_i|' si coefficient négatif
                    expr += myst(r""" -\py{abs(coeff_i)} """, globals(), locals())
            return expr  # retourne l'expression complète
        else:
            # Cas symbolique : on génère u_min = symbolic_0 puis + symbolic_i
            expr = myst(r"""\py{symbolic}_0 """, globals(), locals())
            for i in range(min + 1, max):
                # On concatène '+ symbolic_i' pour chaque terme suivant
                expr += myst(r"""+\py{symbolic}_\py{i} """, globals(), locals())
            return expr  # retourne la somme symbolique

class pxs_Set:
    """
    Wrapper pédagogique pour l'affichage LaTeX d'ensembles SymPy (Interval, Union,
    Intersection, Complement, Range, ensembles usuels N, N*, Z, R) avec notation
    française et délimiteurs \\llbracket \\rrbracket pour les intervalles entiers.

    :pxs_trigger: ensemble mathématique LaTeX, union intersection complément, N*, Reals, Integers, intervalle d'entiers ⟦a,b⟧, notation française ensembles
    :pxs_returns: |
        Wrapper autour d'un ensemble SymPy (Set) avec une méthode .print()
        produisant une chaîne LaTeX respectant les conventions pédagogiques
        françaises (N*, ]a;b[, ⟦a;b⟧, A ∪ B, A ∩ B, A \\ B).
    :pxs_example: |
        S = pxs_Set(Union(Interval(-oo, 0), Interval(1, 5, False, True)))
        # Dans MyST : $D = \\py{S.print()}$
    :pxs_antipattern: Utiliser directement latex(ensemble) qui donne la notation anglo-saxonne et ne gère pas N*, ⟦a,b⟧, ni les conventions françaises.
    """
    def __init__(self, st):
        """
        Initialise le wrapper autour d'un ensemble SymPy.

        :pxs_trigger: instanciation wrapper pxs_Set autour d'un Set sympy
        :pxs_returns: |
            Instance pxs_Set encapsulant l'ensemble SymPy fourni, prête à
            être affichée via .print().
        :pxs_example: |
            S = pxs_Set(Interval(0, 1))
            latex_str = S.print()
        :pxs_antipattern: Passer une expression qui n'est pas un Set SymPy — la méthode print() suppose la présence d'attributs args cohérents.
        """
        self.s = st

    def print(self):
        """
        Produit la représentation LaTeX de l'ensemble selon les conventions
        pédagogiques françaises PyxiScience.

        :pxs_trigger: afficher ensemble en LaTeX, notation française ensembles, union intersection, ⟦a,b⟧, N*, Reals, domaine de définition composé
        :pxs_returns: |
            Chaîne LaTeX (str) représentant l'ensemble : Reals pour ]-∞,+∞[,
            N, N*, Z pour les ensembles usuels, ⟦a,b⟧ pour les intervalles
            entiers (Range), et A ∪ B / A ∩ B / A \\ B avec parenthésage
            automatique des sous-ensembles composés.
        :pxs_example: |
            D = pxs_Set(Complement(Reals, FiniteSet(0))).print()
            # Dans MyST : $D_f = \\py{D}$
        :pxs_antipattern: Composer manuellement la représentation d'une union/intersection sans gérer le parenthésage des sous-ensembles composés (A ∪ (B ∩ C)).
        """

        def __pxs_parentheses(st):
            #Déterminer si st est composé de plusieurs ensembles
            pxs_st = pxs_Set(st)
            compose = st.args # tuple des composantes de st, et False si aucune
            for x in st.args:
                if not isinstance(x, Set):
                    compose = False

            if compose:
                return fr"\big({pxs_st.print()}\big)"
            return pxs_st.print()

        if isinstance(self.s, Interval) and self.s.left == -oo and self.s.right == oo:
            return latex(Reals)
        elif isinstance(self.s, Interval):
            pxs_st = pxs_Interval.from_Interval(self.s)
            return pxs_st.print()
        if isinstance(self.s, Complement):
            return r" \setminus ".join(map(__pxs_parentheses, self.s.args))
        if isinstance(self.s, (Union, Intersection)):
            op = r" \cap " if isinstance(self.s, Intersection) else r" \cup "
            return fr"{op}".join(map(__pxs_parentheses, self.s.args))
        if isinstance(self.s, Range) and self.s.args[2] == 1:
            if self.s.args[0] == -oo and self.s.args[1] == oo:
                return latex(Integers)
            elif self.s.args[0] == 0 and self.s.args[1] == oo:
                return latex(Naturals)
            elif self.s.args[0] == 1 and self.s.args[1] == oo:
                return r"\N^*"
            else:
                return pxs_Interval(self.s.args[0], self.s.args[1] - 1).print().replace(r"\left[", r"\llbracket").replace(r"\left]", r"\rrbracket").replace(r"\right[", r"\llbracket").replace(r"\right]", r"\rrbracket")
        if self.s == Naturals:
            return r"\N^*"
        if self.s == Naturals0:
            return latex(Naturals)
        else:
            return latex(self.s)
            
            
 # =========================================================================
 # CLASSE pxs_Plotable POUR LA REPRÉSENTATION GRAPHIQUE D'EXPRESSIONS SYMPY
 # =========================================================================

""" PISTES D'AMÉLIORATION :
- Gestion des singularités : retirer les singularités de la liste des abscisses, voire éventuellement plafonner les valeurs extrêmes de la fonction. P. ex :
if max(ordo) > seuil:  # (seuil = 100 par défaut ?)
    # ...limiter l'axe des ordonnées à +seuil
if min(ordo) < - seuil:
    # ... limiter l'axe des ordonnées à - seuil.

- vérifier mais je crois que plot_vars n'est pas utile (sauf peut-être pour les vérifs)
dans plot_surface_partial et contour_partial. Peut sans doute être enlevée des variables de sortie de la fonction auxiliaire associée.

- ajouter une colorbar (peut-être en option) sur les contour.
"""

import matplotlib.pyplot as plt
import sympy as sp
import numpy as np


# # finalement inutile si l'on est obligés d'utiliser numpy pour les tracés 3d...
# def pxs_meshgrid(x, y):
#     """Pour remplacer le meshgrid de Numpy"""
#     n, p = len(x), len(y)
#     X = [x for _ in range(p)]
#     Y = [[yi] * n for yi in y]
#     return X, Y


class pxs_Plotable:
    """
    Cette classe permet de représenter graphiquement des fonctions ou suites mathématiques d'une ou plusieurs variables définies par des expressions SymPy (fraphes 2D, 3D, fonctions partielles, suites).
    
    Voir la documentation de chaque fonction, et la fonction tests_visuels_pxs_Plotable() du fichier de test correspondant
    pour un aperçu graphique général.

    :pxs_trigger: représentation graphique expression SymPy, tracé fonction matplotlib pédagogique, courbe surface contour nuage suite
    :pxs_returns: |
        Classe wrappant une expression SymPy et offrant les méthodes plot,
        plot_partial, plot_surface, plot_surface_partial, contour,
        contour_partial, plot_corde, scatter pour tous les besoins graphiques
        pédagogiques (2D, 3D, suites, fonctions partielles).
    :pxs_example: |
        pex = pxs_Plotable("cos(x)")
        pex.plot(interv=pxs_Interval(0, 2*pi))
        # La figure matplotlib courante est modifiée par effet de bord.
    :pxs_antipattern: Combiner sympy.lambdify + np.linspace + plt.plot à la main, avec titre LaTeX et gestion des bornes infinies réécrits à chaque exercice.
    """

    def __init__(self, expr):
        """
        Initialise un objet pxs_Plotable pour le tracé de fonctions SymPy.

        Cette classe permet de représenter graphiquement des fonctions ou suites mathématiques d'une ou plusieurs variables définies par des expressions SymPy (fraphes 2D, 3D, fonctions partielles, suites).

        Paramètres
        ----------
        expr : str, sympy.Expr
            L'expression mathématique à tracer. Peut être une chaîne de caractères
            (qui sera convertie automatiquement) ou une expression SymPy.

        Exemples
        --------
        >>> from sympy.abc import x, y
        >>> pex1 = pxs_Plotable("cos(x)")
        >>> pex2 = pxs_Plotable(x**2 + y**2)
        >>> pex3 = pxs_Plotable(5)  # fonction constante

        :pxs_trigger: créer objet traçable depuis expression sympy ou chaîne, conversion automatique sympify
        :pxs_returns: |
            Instance pxs_Plotable avec attributs .expr (expression SymPy) et
            .vars (set des variables libres), prête pour l'appel à plot,
            plot_surface, contour, scatter, etc.
        :pxs_example: |
            pex = pxs_Plotable("x**2 + y**2")
            pex.plot_surface()
        :pxs_antipattern: Stocker l'expression sous forme de chaîne et la reconvertir à chaque tracé.
        """

        expr = sp.sympify(expr) # si p. ex expr est une chaîne en entrée
        self.expr = expr
        self.vars = expr.free_symbols

    def plot(self, interv = pxs_Interval(-5, 5), pas = None, ymin = None, ymax = None, title = True, fast = False, **kwargs):

        """
        Trace la courbe représentative d'une fonction d'une variable.

        Cette méthode trace le graphe d'une fonction à une variable ou d'une constante.
        Elle gère automatiquement les bornes infinies et les intervalles ouverts.

        Paramètres
        ----------
        interv : pxs_Interval, optionnel
            L'intervalle de tracé. Par défaut [-5, 5].
        pas : float, optionnel
            Le pas d'échantillonnage. Par défaut (b-a)/1000.
        title : bool, optionnel
            Afficher ou non le titre avec l'expression LaTeX. Par défaut True.
        fast : bool, optionnel
            Mode de tracé rapide utilisant plt directement. Par défaut False.
        **kwargs
            Arguments supplémentaires passés à matplotlib.pyplot.plot.

        Lève
        ----
        ValueError
            Si l'expression contient plus d'une variable libre.

        Exemples
        --------
        >>> from sympy.abc import x
        >>> pex = pxs_Plotable("cos(x)")
        >>> pex.plot()  # Trace cos(x) sur [-5, 5]
        >>> pex.plot(interv=pxs_Interval(0, 2*pi), color="red")
        >>>
        >>> # Intervalle ouvert
        >>> pex_log = pxs_Plotable("log(x)")
        >>> pex_log.plot(interv=pxs_Interval.open(0, 5))

        :pxs_trigger: tracer courbe fonction une variable, graphe f(x) sur intervalle, représentation graphique exercice
        :pxs_returns: |
            None (effet de bord). Dessine la courbe sur l'axe matplotlib
            courant (plt.gca() ou plt.plot si fast=True), avec titre LaTeX
            automatique "Courbe représentative de la fonction x ↦ f(x)".
        :pxs_example: |
            pex = pxs_Plotable("x**2 - 1")
            pex.plot(interv=pxs_Interval(-3, 3), color="blue")
            # Sauvegarde via plt.savefig(...)
        :pxs_antipattern: Utiliser np.linspace + sp.lambdify + plt.plot et composer manuellement le titre LaTeX à chaque exercice.
        """

        a, b = interv.left, interv.right

        # /!\ GADGET DE CLAUDE : Gestion des bornes infinies, est-il bien utile de le garder ?
        if a == -sp.oo:
            a = -100  # Grande valeur négative par défaut
        elif a == sp.oo:
            a = 100   # Grande valeur positive par défaut

        if b == sp.oo:
            b = 100   # Grande valeur positive par défaut
        elif b == -sp.oo:
            b = -100  # Grande valeur négative par défaut


        # pas par défaut : 1000 subdivisions
        if pas is None:
            pas = (b - a) / 1000

        nb_vars = len(self.vars)
        # Fonction constante
        if nb_vars == 0:
            x = sp.Symbol("x")
            var = x # pour le titre
            absc = [a, b]
            c = self.expr.evalf()
            ordo = [c, c]
        # Fonction d'exactement deux variables
        elif nb_vars == 1:
            var = list(self.vars)[0]
            fonction = sp.lambdify(var, self.expr, "math")
            absc = [a + k * pas for k in range(int( (b-a) / pas) + 1)]

            # Cas d'un intervalle ouvert : retrait des bornes
            if interv.left_open:
                absc.pop(0)
            if interv.right_open:
                absc.pop()

            ordo = [fonction(xk) for xk in absc]

        # Cas d'une fonction de plus de deux variables : erreur
        elif nb_vars == 2:
            raise ValueError("Trop de variables dans l'expression. Utiliser plot_partial ou plot_surface")
        else:
            raise ValueError("Trop de variables dans l'expression. Utiliser plot_partial ou plot_surface_partial")

        if fast: # Pour une seule figure, sans avoir à définir des subplots et des axes
            # plt.clf()
            plt.plot(absc, ordo, **kwargs)
            if title:
                plt.title(fr"Courbe représentative de la fonction ${var} \mapsto {sp.latex(self.expr)}$ sur l'intervalle ${sp.latex(interv)}$")
            # plt.show()
        else:
            ax = plt.gca()
            ax.plot(absc, ordo, **kwargs)
            if title:
                ax.set_title(fr"Courbe représentative de la fonction ${var} \mapsto {sp.latex(self.expr)}$ sur l'intervalle ${sp.latex(interv)}$")

            # Si l'utilisateur spécifie des valeurs limites en ordonnées
            if ymin is not None:
                ax.set_ylim(bottom = ymin)
            if ymax is not None:
                ax.set_ylim(top = ymax)

    def plot_partial(self, plot_var = None, fixes = None, **kwargs):

        """
        Trace la courbe d'une fonction partielle en fixant certaines variables.

        Cette méthode permet de tracer une fonction de plusieurs variables en fixant
        toutes les variables sauf une. La figure obtenue est une courbe dans le plan.

        Paramètres
        ----------
        plot_var : sympy.Symbol, optionnel
            La variable selon laquelle tracer. Par défaut, la première variable
            de l'expression.
        fixes : dict, optionnel
            Dictionnaire {variable: valeur} fixant les autres variables.
            Par défaut, toutes les autres variables sont fixées à 0.
        **kwargs
            Arguments supplémentaires passés à la méthode plot().

        Lève
        ----
        ValueError
            Si l'expression est constante, si plot_var n'appartient pas aux variables
            de l'expression, si certaines variables ne sont pas fixées, ou si une
            valeur fixée correspond à une singularité.

        Exemples
        --------
        >>> from sympy.abc import x, y, t
        >>> pex = pxs_Plotable(2*x**2 + 3*y/t)
        >>> # Trace selon x avec y=1, t=1
        >>> pex.plot_partial(x, {y: 1, t: 1})
        >>> # Trace selon t avec x=1, y=1, évite t=0 (singularité)
        >>> pex.plot_partial(t, {x: 1, y: 1}, interv=pxs_Interval.open(0, 5))

        :pxs_trigger: fonction partielle, fixer variables, tracer f(x,y,t) selon x avec y et t fixés, coupe 1D d'une fonction multivariable
        :pxs_returns: |
            None (effet de bord matplotlib). Substitue les variables de fixes
            par leurs valeurs, puis trace la courbe de la fonction partielle
            résultante selon plot_var via pxs_Plotable.plot.
        :pxs_example: |
            pex = pxs_Plotable(2*x**2 + 3*y/t)
            pex.plot_partial(x, {y: 1, t: 1})
            # Trace x ↦ 2x² + 3
        :pxs_antipattern: Faire self.expr.subs({y:1, t:1}) à la main puis reconstruire un pxs_Plotable et appeler plot sans vérifier les singularités ni l'appartenance des variables.
        """

        if fixes is None:
            const_vars = self.vars.copy()
            # Vérification avant suppression
            try:
                const_vars.remove(plot_var)
            except:
                raise ValueError(f"La variable {plot_var} ne fait pas partie des variables de l'expression")
            fixes = {v : 0 for v in const_vars} # par défaut toutes les var fixées valent 0

        if len(self.vars) == 0:
            raise ValueError("L'expression est constante")
        elif plot_var is not None and plot_var not in self.vars:
            raise ValueError(f"La variable {plot_var} ne fait pas partie des variables de l'expression")

        if not self.vars.issubset( set(fixes.keys()).union({plot_var}) ):
            raise ValueError("Certaines variables de l'expression n'ont pas été fixées")

        for k, v in fixes.items():
            if v in sp.singularities(self.expr, k):
                raise ValueError(f"La valeur {v} est une singularité de l'expression par rapport à la variable {k}")


        # Définition des valeurs par défaut de plot_var et fixes (impossible d'appeler self
        # dans les arguments par défaut)
        if plot_var is None:
            plot_var = list(self.vars)[0]

        if fixes is None:
            const_vars = self.vars.copy()
            # Vérification avant suppression
            try:
                const_vars.remove(plot_var)
            except:
                raise ValueError(f"La variable {plot_var} ne fait pas partie des variables de l'expression")
            fixes = {v : 0 for v in const_vars} # par défaut toutes les var fixées valent 0

        fonction_partielle = pxs_Plotable(self.expr.subs(fixes))
        fonction_partielle.plot(**kwargs)

    def __aux_2var(self, interv1, interv2, nb_points):
        """
        Fonction auxiliaire privée utilisée dans les fonctions plot_surface et contour pour discrétiser une fonction de deux variables.

        :pxs_trigger: interne — discrétisation fonction 2 variables pour plot_surface et contour
        :pxs_returns: |
            Tuple (X, Y, Z) de np.ndarray : grille meshgrid des abscisses et
            ordonnées, plus l'évaluation vectorisée de l'expression sur cette grille.
        :pxs_example: |
            # Appelé uniquement en interne par plot_surface et contour
            # X, Y, Z = self.__aux_2var(interv1, interv2, 30)
        :pxs_antipattern: Appeler cette méthode privée directement depuis un exercice au lieu d'utiliser plot_surface ou contour.
        """

        if len(self.vars) != 2:
            raise ValueError("La fonction à tracer doit être une fonction d'exactement deux variables")
        # Convertir les bornes en float "normaux"
        a1, b1 = float(interv1.left), float(interv1.right)
        a2, b2 = float(interv2.left), float(interv2.right)

        x = np.linspace(a1, b1, nb_points)
        y = np.linspace(a2, b2, nb_points)
        # Cas d'un intervalle ouvert
        if interv1.left_open:
            x.pop(0)
        if interv1.right_open:
            x.pop()
        if interv2.left_open:
            y.pop(0)
        if interv2.right_open:
            y.pop()

        X, Y = np.meshgrid(x, y)
        liste_vars = list(self.vars)
        f = sp.lambdify(liste_vars, self.expr, "numpy")
        Z = f(X, Y)

        return X, Y, Z

    def __aux_verif_partial_2var(self, plot_vars, fixes):
        """
        Vérifications à effectuer avant l'utilisation des méthodes de tracé de fonctions partielles à plus de deux variables.

        :pxs_trigger: interne — validation arguments plot_surface_partial et contour_partial
        :pxs_returns: |
            Le dictionnaire fixes complété avec les valeurs par défaut (0)
            pour toutes les variables non explicitement fixées et non présentes
            dans plot_vars. Lève ValueError en cas d'incohérence.
        :pxs_example: |
            # Appelé uniquement en interne par plot_surface_partial et contour_partial
            # fixes = self.__aux_verif_partial_2var([x, y], {z: 1})
        :pxs_antipattern: Dupliquer cette logique de validation dans plot_surface_partial et contour_partial au lieu de centraliser.
        """

        if plot_vars is None:
            lis_vars = list(self.vars)
            plot_vars = lis_vars[:2]

        if len(plot_vars) != 2:
            raise ValueError("plot_vars doit contenir exactement 2 variables")

        if fixes is None:
            const_vars = self.vars.copy()
            # Vérifications avant suppression
            for var in plot_vars:
                try:
                    const_vars.remove(var)
                except:
                    raise ValueError(f"La variable {var} ne fait pas partie des variables de l'expression")

            fixes = {v : 0 for v in const_vars} # par défaut toutes les var fixées valent 0

        for var in plot_vars:
            if var not in self.vars:
                raise ValueError(f"La variable {var} ne fait pas partie des variables de l'expression")

        if fixes is not None:
            for k, v in fixes.items():
                if v in sp.singularities(self.expr, k):
                    raise ValueError(f"La valeur {v} est une singularité de l'expression par rapport à la variable {k}")

        if not self.vars.issubset( set(fixes.keys()).union(set(plot_vars)) ):
            raise ValueError("Certaines variables de l'expression n'ont pas été fixées")

        return fixes


    def plot_surface(self, interv1 = pxs_Interval(-5, 5), interv2 = pxs_Interval(-5, 5), nb_points = 30, cmap = "viridis", title = True, **kwargs):
        """
        Trace la surface représentative d'une fonction de deux variables.

        Cette méthode génère un tracé 3D de la surface définie par une fonction
        à exactement deux variables.

        Paramètres
        ----------
        interv1 : pxs_Interval, optionnel
            Intervalle pour la première variable. Par défaut [-5, 5].
        interv2 : pxs_Interval, optionnel
            Intervalle pour la deuxième variable. Par défaut [-5, 5].
        nb_points : int, optionnel
            Nombre de points par axe pour la grille. Par défaut 30.
        cmap : str, optionnel
            Colormap matplotlib pour la surface. Par défaut "viridis".
        title : bool, optionnel
            Afficher ou non le titre avec l'expression LaTeX. Par défaut True.
        **kwargs
            Arguments supplémentaires passés à matplotlib.Axes3D.plot_surface.

        Lève
        ----
        ValueError
            Si l'expression ne contient pas exactement deux variables libres.

        Exemples
        --------
        >>> from sympy.abc import x, y
        >>> surf1 = pxs_Plotable(x**2 + y**2)  # Paraboloïde
        >>> fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
        >>> surf1.plot_surface(cmap="plasma")
        >>>
        >>> surf2 = pxs_Plotable("sin(x)*cos(y)")  # Surface trigonométrique
        >>> surf2.plot_surface(nb_points=50, cmap="coolwarm")

        :pxs_trigger: surface 3D fonction deux variables, paraboloïde selle de cheval, tracé tridimensionnel matplotlib, z=f(x,y)
        :pxs_returns: |
            None (effet de bord). Dessine la surface 3D sur l'axe 3D courant
            (nécessite subplot_kw={"projection": "3d"}), avec titre LaTeX
            automatique et colormap configurable.
        :pxs_example: |
            surf = pxs_Plotable(x**2 + y**2)
            fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
            surf.plot_surface(cmap="plasma")
        :pxs_antipattern: Construire meshgrid + lambdify + Axes3D.plot_surface à la main pour chaque exercice, sans titre LaTeX normalisé.
        """

        # l'utilisation de numpy semble obligatoire ici :
        # (et si on s'en sert autant le faire partout où ça simplifie les choses non ?)

        # --- ci-dessous : tentative infructueuse de ne pas utiliser numpy... ---

        # a1, b1 = interv1.left.evalf(), interv1.right.evalf() # evalf() pour convetir en float "normaux"
        # h1 = (b1 - a1) / (nb_points - 1)
        # a2, b2 = interv2.left.evalf(), interv2.right.evalf() # idem
        # h2 = (b2 - a2) / (nb_points - 1)
        # x = [a1 + k * h1 for k in range(nb_points)]
        # y = [a2 + k * h2 for k in range(nb_points)]
        # X, Y = pxs_meshgrid(x, y)
        # liste_vars = list(self.vars)
        # f = sp.lambdify(liste_vars, self.expr, "math")
        # Z = [[f(xi, yj).evalf() for xi in x] for yj in y]

        X, Y, Z = self.__aux_2var(interv1, interv2, nb_points)
        liste_vars = list(self.vars)
        ax = plt.gca()
        ax.plot_surface(X, Y, Z, cmap = cmap, **kwargs)

        if title:
            var1, var2 = liste_vars[0], liste_vars[1]
            ax.set_title(fr"Surface représentative de la fonction $({var1}, {var2}) \mapsto {sp.latex(self.expr)}$")



    def plot_surface_partial(self, plot_vars = None, fixes = None, **kwargs):
        """
        Trace la surface d'une fonction partielle en fixant certaines variables.

        Cette méthode permet de tracer une fonction de plus de deux variables en fixant
        toutes les variables sauf deux, générant ainsi une surface 3D. Elle effectue
        automatiquement les vérifications de cohérence.

        Paramètres
        ----------
        plot_vars : list of sympy.Symbol, optionnel
            Liste de deux variables pour les axes de la surface. Par défaut,
            les deux premières variables de l'expression.
        fixes : dict, optionnel
            Dictionnaire {variable: valeur} fixant les autres variables.
            Par défaut, toutes les autres variables sont fixées à 0.
        **kwargs
            Arguments supplémentaires passés à la méthode plot_surface().

        Lève
        ----
        ValueError
            Si plot_vars ne contient pas exactement 2 variables, si les variables
            de plot_vars n'appartiennent pas à l'expression, si certaines variables
            ne sont pas fixées, ou si une valeur fixée correspond à une singularité.

        Exemples
        --------
        >>> from sympy.abc import x, y, z, t
        >>> pex = pxs_Plotable(x**2 + y**2 + z + t)
        >>> fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
        >>> # Surface x-y avec z=1, t=0
        >>> pex.plot_surface_partial([x, y], {z: 1, t: 0})
        >>> # Surface x-z avec y=0, t=1
        >>> pex.plot_surface_partial([x, z], {y: 0, t: 1}, cmap="plasma")

        :pxs_trigger: surface 3D fonction partielle plus de 2 variables, coupe 2D en 3D, fixer certaines variables pour tracer surface, section surface
        :pxs_returns: |
            None (effet de bord). Fixe les variables de fixes, puis trace la
            surface 3D de la fonction partielle sur les deux variables restantes
            (plot_vars) via pxs_Plotable.plot_surface.
        :pxs_example: |
            pex = pxs_Plotable(x**2 + y**2 + z + t)
            fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
            pex.plot_surface_partial([x, y], {z: 1, t: 0})
        :pxs_antipattern: Faire self.expr.subs puis reconstruire un pxs_Plotable et appeler plot_surface sans valider que plot_vars contient exactement 2 variables ni repérer les singularités.
        """

        fixes = self.__aux_verif_partial_2var(plot_vars, fixes)

        fonction_partielle = pxs_Plotable(self.expr.subs(fixes))
        fonction_partielle.plot_surface(**kwargs)

    def contour(self, interv1 = pxs_Interval(-5, 5), interv2 = pxs_Interval(-5, 5), nb_points = 30, levels = 10, title = True, **kwargs):
        """
        Trace les lignes de niveau d'une fonction de deux variables.

        Cette méthode génère un tracé 2D des courbes de niveau d'une fonction
        à exactement deux variables.

        Paramètres
        ----------
        interv1 : pxs_Interval, optionnel
            Intervalle pour la première variable. Par défaut [-5, 5].
        interv2 : pxs_Interval, optionnel
            Intervalle pour la deuxième variable. Par défaut [-5, 5].
        nb_points : int, optionnel
            Nombre de points par axe pour la grille. Par défaut 30.
        levels : int ou array-like, optionnel
            Nombre de niveaux ou valeurs spécifiques pour les lignes de niveau.
            Par défaut 10.
        cmap : str, optionnel
            Colormap matplotlib pour les lignes de niveau. Par défaut "viridis".
        title : bool, optionnel
            Afficher ou non le titre avec l'expression LaTeX. Par défaut True.
        **kwargs
            Arguments supplémentaires passés à matplotlib.pyplot.contour ou contourf.

        Lève
        ----
        ValueError
            Si l'expression ne contient pas exactement deux variables libres.

        Exemples
        --------
        >>> from sympy.abc import x, y
        >>> import matplotlib.pyplot as plt
        >>>
        >>> # Lignes de niveau d'un paraboloïde
        >>> parab = pxs_Plotable(x**2 + y**2)
        >>> parab.contour(levels=15)
        >>> plt.show()
        >>>
        >>> # Lignes de niveau avec couleurs personnalisées
        >>> gaussian = pxs_Plotable(sp.exp(-(x**2 + y**2)/2))
        >>> gaussian.contour(cmap="hot", levels=20)
        >>>
        >>> # Niveaux spécifiques pour une fonction trigonométrique
        >>> trig = pxs_Plotable(sp.sin(x)*sp.cos(y))
        >>> levels_custom = [-0.8, -0.4, 0, 0.4, 0.8]
        >>> trig.contour(levels=levels_custom, colors="black", linewidths=2)
        >>> plt.clabel(cs, inline=True, fontsize=10)  # Ajouter des labels
        >>>
        >>> # Selle de cheval avec intervalle personnalisé
        >>> selle = pxs_Plotable(x**2 - y**2)
        >>> selle.contour(interv1=pxs_Interval(-3, 3),
        ...                    interv2=pxs_Interval(-3, 3),
        ...                    levels=25, cmap="RdBu_r")

        :pxs_trigger: lignes de niveau, courbes de niveau, isolignes, carte topographique, contour 2D fonction deux variables, f(x,y)=c
        :pxs_returns: |
            None (effet de bord). Dessine les courbes de niveau sur l'axe
            matplotlib courant, avec titre LaTeX, labels des axes, et ratio
            d'aspect "equal" pour une représentation fidèle.
        :pxs_example: |
            parab = pxs_Plotable(x**2 + y**2)
            parab.contour(levels=15)
            plt.show()
        :pxs_antipattern: Construire meshgrid + lambdify + plt.contour à la main sans normaliser le titre ni verrouiller l'aspect ratio.
        """

        X, Y, Z = self.__aux_2var(interv1, interv2, nb_points)
        liste_vars = list(self.vars)
        # Tracé des lignes de niveau
        ax = plt.gca()
        cs = ax.contour(X, Y, Z, levels=levels, **kwargs)

        # Ajout du titre
        if title:
            var1, var2 = liste_vars[0], liste_vars[1]
            ax.set_title(fr"Lignes de niveau de $({var1}, {var2}) \mapsto {sp.latex(self.expr)}$")


        # Labels des axes
        ax.set_xlabel(f"${liste_vars[0]}$")
        ax.set_ylabel(f"${liste_vars[1]}$")

        # Assurer un ratio d'aspect égal pour une représentation fidèle
        ax.set_aspect('equal', adjustable='box')


    def contour_partial(self, plot_vars = None, fixes = None, **kwargs):
        """
        Trace les lignes de niveau d'une fonction partielle en fixant certaines variables.

        Cette méthode permet de tracer les lignes de niveau d'une fonction de plus de deux
        variables en fixant toutes les variables sauf deux, générant ainsi un tracé 2D de
        lignes de niveau. Elle effectue automatiquement les vérifications de cohérence.

        Paramètres
        ----------
        plot_vars : lise de sympy.Symbol, optionnel
            Liste de deux variables pour les axes du tracé de contour. Par défaut,
            les deux premières variables de l'expression.
        fixes : dict, optionnel
            Dictionnaire {variable: valeur} fixant les autres variables.
            Par défaut, toutes les autres variables sont fixées à 0.
        **kwargs
            Arguments supplémentaires passés à la méthode contour().

        Retourne
        --------
        matplotlib.contour.QuadContourSet
            L'objet contour retourné par matplotlib, utile pour ajouter des labels
            ou personnaliser l'affichage.

        Lève
        ----
        ValueError
            Si plot_vars ne contient pas exactement 2 variables, si les variables
            de plot_vars n'appartiennent pas à l'expression, si certaines variables
            ne sont pas fixées, ou si une valeur fixée correspond à une singularité.

        Exemples
        --------
        >>> from sympy.abc import x, y, z, t
        >>> import matplotlib.pyplot as plt
        >>>
        >>> # Fonction de 4 variables
        >>> pex = pxs_Plotable(x**2 + y**2 + z*t)
        >>>
        >>> # Lignes de niveau dans le plan x-y avec z=1, t=2
        >>> pex.contour_partial([x, y], {z: 1, t: 2}, levels=15)
        >>>
        >>> # Lignes de niveau dans le plan x-z avec y=0, t=1
        >>> pex.contour_partial([x, z], {y: 0, t: 1}, cmap="plasma")
        >>>
        >>> # Niveaux personnalisés pour une fonction trigonométrique
        >>> trig_3d = pxs_Plotable(sp.sin(x)*sp.cos(y) + z)
        >>> levels_custom = [0, 0.5, 1.0, 1.5, 2.0]
        >>> trig_3d.contour_partial([x, y], {z: 1}, levels=levels_custom,
        ...                              colors="black", linewidths=2)

        :pxs_trigger: lignes de niveau fonction partielle plus de 2 variables, contour 2D avec variables fixées, section isolignes
        :pxs_returns: |
            None (effet de bord). Fixe les variables de fixes, puis trace les
            courbes de niveau de la fonction partielle sur les deux variables
            restantes (plot_vars) via pxs_Plotable.contour.
        :pxs_example: |
            pex = pxs_Plotable(x**2 + y**2 + z*t)
            pex.contour_partial([x, y], {z: 1, t: 2}, levels=15)
        :pxs_antipattern: Faire expr.subs puis contour à la main sans vérifier la cohérence de plot_vars ni détecter les singularités.
        """

        fixes = self.__aux_verif_partial_2var(plot_vars, fixes)

        fonction_partielle = pxs_Plotable(self.expr.subs(fixes))
        fonction_partielle.contour(**kwargs)



    def plot_corde(self, absc_corde, fast = False, color = "black", linestyle = "dashed", marker = ".", **kwargs):
        """
        Trace la corde reliant deux points d'une courbe.

        Cette méthode trace un segment de droite reliant deux points de la courbe
        représentative de la fonction.

        Paramètres
        ----------
        absc_corde : tuple ou list
            Tuple ou liste de deux abscisses (a, b) définissant les extrémités
            de la corde.
        fast : bool, optionnel
            Mode de tracé rapide utilisant plt directement. Par défaut False.
        color : str, optionnel
            Couleur de la corde. Par défaut "black".
        linestyle : str, optionnel
            Style de ligne. Par défaut "dashed".
        marker : str, optionnel
            Marqueur aux extrémités. Par défaut ".".
        **kwargs
            Arguments supplémentaires passés à matplotlib.pyplot.plot.

        Lève
        ----
        ValueError
            Si l'expression ne contient pas exactement une variable libre.

        Exemples
        --------
        >>> from sympy.abc import x
        >>> pex = pxs_Plotable("x**3 - 2*x")
        >>> pex.plot(color="blue")
        >>> # Corde entre x=-1 et x=2
        >>> pex.plot_corde((-1, 2), color="red", linewidth=2)
        >>> # Plusieurs cordes
        >>> pex.plot_corde((0, 1), color="green", marker="o")

        :pxs_trigger: corde courbe, taux d'accroissement visuel, sécante, segment reliant (a,f(a)) et (b,f(b)), illustration dérivée
        :pxs_returns: |
            None (effet de bord). Trace un segment en pointillés noirs reliant
            les points (a, f(a)) et (b, f(b)) sur l'axe matplotlib courant.
            Typiquement superposé à un appel pxs_Plotable.plot préalable.
        :pxs_example: |
            pex = pxs_Plotable("x**3 - 2*x")
            pex.plot(color="blue")
            pex.plot_corde((-1, 2), color="red", linewidth=2)
        :pxs_antipattern: Calculer f(a) et f(b) via sympy.subs puis plt.plot([a,b],[fa,fb]) à la main à chaque exercice.
        """

        # Vérification du nombre de variables
        if len(self.vars) != 1:
            raise ValueError("La fonction plot_corde ne peut être utilisée que pour des fonctions d'une seule variable")

        # ci-dessous on suppose que c'est OK
        a, b = absc_corde
        var = list(self.vars)[0]
        fa, fb = self.expr.subs(var, a), self.expr.subs(var, b)
        if fast:
            plt.plot([a, b], [fa, fb], color = color, linestyle = linestyle,  marker = marker, **kwargs)
        else:
            ax = plt.gca()
            ax.plot([a, b], [fa, fb], color = color, linestyle = linestyle, marker = marker, **kwargs)

    def scatter(self, n_terms=20, start_index=0, fast=False, **kwargs):
        """
        Trace les termes d'une suite numérique sous forme de nuage de points.

        Cette méthode évalue l'expression pour des valeurs entières consécutives
        de la variable et affiche les résultats sous forme de nuage de points.

        Paramètres
        ----------
        n_terms : int, optionnel
            Nombre de termes de la suite à tracer. Doit être un entier positif.
            Par défaut 20.
        start_index : int, optionnel
            Indice de départ de la suite. Peut être négatif, nul ou positif
            selon la définition de la suite. Par défaut 0.
        fast : bool, optionnel
            Mode de tracé rapide utilisant plt directement sans axes personnalisés.
            Si False, ajoute automatiquement les labels et le titre. Par défaut False.
        **kwargs
            Arguments supplémentaires passés à matplotlib.pyplot.scatter.
            Exemples : color, s (taille), alpha, marker, etc.

        Lève
        ----
        ValueError
            Si l'expression ne contient pas exactement une variable libre.
            Message : "La fonction scatter ne peut être utilisée que
            pour des suites (fonction d'une seule variable)".

        Exemples
        --------
        >>> from sympy.abc import n
        >>> import matplotlib.pyplot as plt
        >>>
        >>> # Suite arithmétique : u_n = 2n + 1
        >>> suite1 = pxs_Plotable(2*n + 1)
        >>> suite1.scatter(n_terms=15, color="blue", s=50)
        >>> plt.show()
        >>>
        >>> # Suite géométrique : u_n = (1/2)^n
        >>> suite2 = pxs_Plotable("(1/2)**n")
        >>> suite2.scatter(n_terms=20, start_index=1, color="red", s=40)
        >>>
        >>> # Suite alternée : u_n = (-1)^n / n
        >>> suite4 = pxs_Plotable((-1)**n / n)
        >>> suite4.scatter(n_terms=20, start_index=1, color="purple", alpha=0.7)
        >>>
        >>> # Mode fast pour tracé rapide sans labels
        >>> suite1.scatter(fast=True, n_terms=10, color="cyan", s=80)

        :pxs_trigger: suite numérique, nuage de points, termes u_n graphique, représentation points isolés indice/valeur, suite arithmétique géométrique alternée
        :pxs_returns: |
            None (effet de bord). Évalue l'expression pour les indices entiers
            de start_index à start_index+n_terms-1, puis trace un scatter avec
            labels et titre LaTeX de la forme "(u_n)_{n ≥ start_index}".
        :pxs_example: |
            suite = pxs_Plotable(2*n + 1)
            suite.scatter(n_terms=15, color="blue", s=50)
        :pxs_antipattern: Faire une boucle for + sympy.subs + plt.scatter à la main sans labels normalisés ni titre LaTeX pédagogique.
        """
        if len(self.vars) != 1:
            raise ValueError("La fonction plot_scatter_sequence ne peut être utilisée que pour des suites (fonction d'une seule variable)")

        var = list(self.vars)[0]
        indices = list(range(start_index, start_index + n_terms))
        values = [float(self.expr.subs(var, n)) for n in indices]

        if fast:
            plt.scatter(indices, values, **kwargs)
        else:
            ax = plt.gca()
            ax.scatter(indices, values, **kwargs)
            ax.set_xlabel(f"${var}$ (indice)")
            ax.set_ylabel(f"${sp.latex(self.expr)}$")
            ax.set_title(fr"Termes de la suite de $\left({sp.latex(self.expr)}\right)_{{ {var} \geq {start_index} }}$")