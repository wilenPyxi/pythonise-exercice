"""Mes_fctions_generalistes_bis - Gestion de certaines fonctions de formatage Latex.
    Pour voir les tests unitaires s'afficher dans l'éditeur
    ----------------------------------------------------------------------
    >>> \\begin{python}
    >>>  # Code Python : Ecrivez ci-dessous votre code Python
    >>> from src.scripts.tests.test_Mes_fctions_generalistes_bis import print_tests_Mes_fctions_generalistes_bis
    >>> print_tests_Mes_fctions_generalistes_bis()
    >>> \\end{python}

"""



from sympy import *
from fractions import Fraction
from sympy import latex as sympy_latex
from src.scripts.pxs_runtime import get_pxs_lang, myst
import random as rd

# Les fonctions à tester

def pxs_config(mul_symbol: str = "") -> dict:
    """
    Build a configuration dictionary for LaTeX rendering, depending on the
    current pyxisciences language settings.

    The language is retrieved using `get_pxs_lang()` and affects some formatting
    options, such as the decimal separator.

    Parameters
    ----------
    mul_symbol : str, optional
        Multiplication symbol to be used in LaTeX output (default is "").

    Returns
    -------
    dict
        A dictionary containing LaTeX configuration options, including:
        - ln_notation : bool
        - mul_symbol : str
        - order : str
        - decimal_separator : str
        - inv_trig_style : str

    Examples
    --------
    >>> pxs_config()
    {'ln_notation': True, 'mul_symbol': '', 'order': 'lex', ...}

    :pxs_trigger: configuration LaTeX standard sympy, virgule/point décimal selon FR/EN via get_pxs_lang(), kwargs à passer à latex(**config), ln_notation, inv_trig_style, choix du mul_symbol, mise en forme homogène dans un exercice PyxiScience
    :pxs_returns: |
        dictionnaire de kwargs ``{ln_notation, mul_symbol, order, decimal_separator, inv_trig_style}``
        à déballer avec ``**`` dans ``sympy.latex(expr, **config)`` pour obtenir un rendu LaTeX
        conforme à la langue courante de l'exercice.
    :pxs_example: |
        config_standard = pxs_config()
        txt = myst(r"\py{latex(expr, **config_standard)}")
    :pxs_antipattern: Fixer ``decimal_separator="comma"`` en dur sans tenir compte de la langue, ou appeler ``sympy.latex(expr)`` sans kwargs.
    """
    pxs_lang = get_pxs_lang()
    if pxs_lang == 'fr':
        return {
            "ln_notation": True,
            "mul_symbol": mul_symbol,
            "order": "lex",
            "decimal_separator": "comma",
            "inv_trig_style": "full",
        }
    else:
        return {
            "ln_notation": True,
            "mul_symbol": mul_symbol,
            "order": "lex",
            "decimal_separator": "dot",
            "inv_trig_style": "full",
        }
    

def pxsl_mult(val, mult=myst(r"""\cdot""")):
    """
    Return a multiplication symbol or a blank space depending on the coefficient
    value.

    This function is used to avoid displaying an explicit multiplication symbol
    when the coefficient is 0, 1, or -1, following standard mathematical
    conventions.

    Parameters
    ----------
    val : Any
        Coefficient value to be tested (typically a numeric or SymPy object).
    mult : Any, optional
        LaTeX representation (or compatible object) of the multiplication symbol.
        Default is ``myst(r"\\cdot")``.

    Returns
    -------
    Any
        The multiplication symbol if `val` is not equal to 0, 1, or -1;
        otherwise, a blank space.

    Examples
    --------
    >>> pxsl_mult(3)
    \\cdot

    >>> pxsl_mult(1)
     

    :pxs_trigger: décider d'afficher ou non un symbole de multiplication devant un coefficient, éviter "1·x" ou "-1·x", omettre · quand coef ∈ {-1, 0, 1}, chaînage propre de coefficients dans un polynôme, affichage mathématique standard
    :pxs_returns: |
        chaîne MyST : soit le symbole ``\cdot`` (ou le ``mult`` passé en paramètre)
        si ``val`` n'est pas dans ``{-1, 0, 1}``, soit un espace vide sinon.
    :pxs_example: |
        myst(r"\py{pxsl_mult(a)}\py{latex(x)}")  # n'affiche pas · si a == 1
    :pxs_antipattern: Insérer un ``\cdot`` en dur devant la variable sans tester les cas ±1 et 0.
    """
    if val != 1 and val != -1 and val != 0:
        return mult
    else:
        return myst(r""" """)
    

def pxsl_sign(expr: str):
    ''' {py:function} Returns the sign of an expression in LaTeX format.
    
    This function takes an expression and returns its sign in LaTeX format:
    '+' if the expression is positive, '-' if it is negative,
    and '' (empty string) if it is zero.
    
    :param sympy.Expr: The expression whose sign we want to determine.
    :return: The sign of the expression in LaTeX format.
    :rtype: str
    
    Examples
    --------
    >>> pxsl_sign(5)
    '+'

    >>> pxsl_sign(-3)
    '-'

    >>> pxsl_sign(0)
    ''

    :pxs_trigger: récupérer uniquement le signe "+"/"-"/"" d'une valeur pour l'afficher en LaTeX, préfixer un terme dans un polynôme, chaînage de termes, extraction de signe avant affichage de |valeur|
    :pxs_returns: |
        chaîne MyST "+" si ``expr > 0``, "-" si ``expr < 0``, "" si ``expr == 0``.
    :pxs_example: |
        myst(r"\py{pxsl_sign(coef)}\py{latex(abs(coef))}x")
    :pxs_antipattern: Tester ``if expr > 0: "+"`` à la main dans chaque exercice.
    '''
    if expr > 0:
        return myst(r"""+""", globals(), locals())
    elif expr < 0:
        return myst(r"""-""", globals(), locals())
    else:
        return myst(r"""""" , globals(), locals())


def formater_nombre(nombre):
    """
    Formate un nombre en ajoutant des espaces pour les milliers et gère l'infini.
    
    Cette fonction prend un nombre et le formate pour l'affichage LaTeX en ajoutant
    des espaces pour séparer les milliers. Elle gère également les cas spéciaux
    de l'infini positif et négatif.
    
    Parameters
    ----------
    nombre : int, float, or sympy.core.numbers.Infinity
        Le nombre à formater. Peut être un entier, un flottant, ou l'infini.
    
    Returns
    -------
    str
        Le nombre formaté avec des espaces pour les milliers ou la représentation
        LaTeX de l'infini.
    
    Examples
    --------
    >>> formater_nombre(1234)
    '1\\ 234'

    >>> formater_nombre(1000000)
    '1\\ 000\\ 000'

    >>> formater_nombre(oo)
    '\\infty'

    >>> formater_nombre(-oo)
    '-\\infty'

    :pxs_trigger: afficher un entier en LaTeX avec séparateur de milliers "1\ 000\ 000", gérer oo / -oo, version historique FR uniquement, éviter "1000000" brut ; préférer ``pxsl_format_number`` pour un exercice bilingue
    :pxs_returns: |
        chaîne MyST : nombre avec séparateurs ``\ `` entre milliers, ou ``\infty`` / ``-\infty``
        pour l'infini. Attention : bug historique qui renvoie ``\inftys`` au lieu de ``\infty``
        pour +oo, corrigé dans ``pxsl_format_number``.
    :pxs_example: |
        txt = myst(r"\py{formater_nombre(1500000)}")  # → "1\ 500\ 000"
    :pxs_antipattern: Écrire ``str(n).replace(',', ' ')`` à la main dans chaque exercice, ou oublier le cas ``oo``.
    """
    if isinstance(nombre, Integer):
        nombre = int(nombre)
    if nombre != oo and nombre != -oo:
        #return f"{nombre:,}".replace(",", r"\ ")
        return myst(f"{nombre:,}".replace(",", r"\ "), globals(), locals())
    elif nombre == oo:
        go = myst(r"""\inftys""")
        return f"{go}"
    else:
        go = myst(r"""-\infty""")
        return f"{go}"
    
def pxsl_formater_nombre(nombre):
    """
    Formate un nombre en ajoutant des espaces pour les milliers et gère l'infini.
    
    Cette fonction prend un nombre et le formate pour l'affichage LaTeX en ajoutant
    des espaces pour séparer les milliers. Elle gère également les cas spéciaux
    de l'infini positif et négatif.
    
    Parameters
    ----------
    nombre : int, float, or sympy.core.numbers.Infinity
        Le nombre à formater. Peut être un entier, un flottant, ou l'infini.
    
    Returns
    -------
    str
        Le nombre formaté avec des espaces pour les milliers ou la représentation
        LaTeX de l'infini.
    
    Examples
    --------
    >>> pxsl_formater_nombre(1234)
    '1\\ 234'

    >>> pxsl_formater_nombre(1000000)
    '1\\ 000\\ 000'

    >>> pxsl_formater_nombre(oo)
    '\\infty'

    >>> pxsl_formater_nombre(-oo)
    '-\\infty'

    :pxs_trigger: idem formater_nombre, variante préfixée pxsl_, séparateur de milliers en espace LaTeX \ et gestion de oo/-oo ; version FR historique à éviter dans les exercices bilingues (préférer pxsl_format_number)
    :pxs_returns: |
        chaîne MyST, séparateur ``\ `` entre milliers, ou ``\infty`` / ``-\infty``.
        Hérite du bug ``\inftys`` pour +oo.
    :pxs_example: |
        myst(r"\py{pxsl_formater_nombre(1234)}")
    :pxs_antipattern: Réinventer le formatage des milliers avec f-string au lieu d'appeler cette fonction.
    """
    if isinstance(nombre, Integer):
        nombre = int(nombre)
    if nombre != oo and nombre != -oo:
        #return f"{nombre:,}".replace(",", r"\ ")
        return myst(f"{nombre:,}".replace(",", r"\ "), globals(), locals())
    elif nombre == oo:
        go = myst(r"""\inftys""")
        return f"{go}"
    else:
        go = myst(r"""-\infty""")
        return f"{go}"

def pxsl_format_number(number):
    """
    \en{Formats a number by adding spaces for thousands and handles infinity.}
    \fr{Formate un nombre en ajoutant des espaces pour les milliers et gère l'infini.}
    
    \en{This function takes a number and formats it for LaTeX display by adding
    spaces to separate thousands. It also handles the special cases
    of positive and negative infinity.}
    \fr{Cette fonction prend un nombre et le formate pour l'affichage LaTeX en ajoutant
    des espaces pour séparer les milliers. Elle gère également les cas spéciaux
    de l'infini positif et négatif.}
    
    Parameters
    ----------
    number : int, float, or sympy.core.numbers.Infinity
        \en{The number to format. Can be an integer, a float, or infinity.}
        \fr{Le nombre à formater. Peut être un entier, un flottant, ou l'infini.}
    
    Returns
    -------
    str
        \en{The number formatted with spaces for thousands or its LaTeX representation of infinity.}
        \fr{Le nombre formaté avec des espaces pour les milliers ou la représentation LaTeX de l'infini.}
    
    Examples
    --------
    >>> pxsl_format_number(1234)
    '1\\ 234'

    >>> pxsl_format_number(1000000)
    '1\\ 000\\ 000'

    >>> pxsl_format_number(oo)
    '\\infty'

    >>> pxsl_format_number(-oo)
    '-\\infty'

    :pxs_trigger: formatage bilingue FR/EN d'un nombre avec séparateur de milliers, version à préférer dans tout nouvel exercice PyxiScience (QCM/QCL/QAT), renvoie correctement \infty (pas \inftys), gestion de oo et -oo
    :pxs_returns: |
        chaîne MyST bilingue : séparateurs ``\ `` entre milliers, ``\infty`` ou ``-\infty``
        pour l'infini. Version corrigée et bilingue de ``pxsl_formater_nombre``.
    :pxs_example: |
        myst(r"\py{pxsl_format_number(10000)}")  # → "10\ 000"
    :pxs_antipattern: Choisir ``formater_nombre`` ou ``pxsl_formater_nombre`` (FR-only, bug \inftys) dans un exercice bilingue.
    """
    if isinstance(number, Integer):
        number = int(number)
    if number != oo and number != -oo:
        #return f"{number:,}".replace(",", r"\ ")
        return myst(f"{number:,}".replace(",", r"\ "), globals(), locals())
    elif number == oo:
        go = myst(r"""\infty""")
        return f"{go}"
    else:
        go = myst(r"""-\infty""")
        return f"{go}"

def latex_avec_formatage(expr, sign = False, display = True):
    """
    Wrapper LaTeX qui applique le formatage des nombres.
    
    Cette fonction prend une expression et la convertit en format LaTeX en appliquant
    un formatage spécial pour les grands nombres (>= 1000). Elle gère les entiers,
    flottants, fractions rationnelles et expressions SymPy.
    
    Parameters
    ----------
    expr : int, float, sympy.Rational, or sympy.Expr
        L'expression à convertir en LaTeX avec formatage.
    
    Returns
    -------
    str
        La représentation LaTeX de l'expression avec formatage appliqué.
    
    Examples
    --------
    >>> latex_avec_formatage(1500)
    '1\\ 500'

    >>> latex_avec_formatage(Rational(2000, 3))
    '\\frac{2\\ 000}{3}'

    >>> latex_avec_formatage(Rational(1, 2))
    '\\frac{1}{2}'

    :pxs_trigger: affichage LaTeX d'un grand nombre ou d'une fraction avec séparateurs de milliers + signe préfixé optionnel + \displaystyle, auto-simplification des fractions via gcd, fallback sympy_latex ; version historique FR — préférer ``pxsl_latex_with_formatting`` en bilingue
    :pxs_returns: |
        chaîne LaTeX : ``\displaystyle\frac{num}{den}`` pour les Rational non entiers,
        nombre formaté avec ``\ `` pour les entiers ≥ 1000, préfixe "+" ou "-" si ``sign=True``.
    :pxs_example: |
        txt = myst(r"\py{latex_avec_formatage(Rational(2000,3), sign=True)}")
    :pxs_antipattern: Appeler ``latex(expr)`` directement et laisser "2000/3" sans espaces de milliers, ou dupliquer la logique de simplification gcd.
    """
    if display:
        disp = '\displaystyle '
    else:
        disp = ' '
    if expr == oo or expr == -oo:
        return formater_nombre(expr)
    if isinstance(expr, (int, Integer, float, Float)) and abs(expr) >= 1000:
        if sign is False:
            return formater_nombre(expr)
        else:
            return myst(r""" - \;\py{formater_nombre(abs(expr))} """, globals(), locals()) if expr < 0 else myst(r""" + \;\py{formater_nombre(abs(expr))} """, globals(), locals())
    elif isinstance(expr, Rational):
        if expr.q == 1:
            num = expr.p
            if abs(num) >= 1000:
                if sign is False:
                    return formater_nombre(num)
                else:
                    return myst(r""" - \py{formater_nombre(abs(num))} """, globals(), locals()) if num < 0 else myst(r""" + \py{formater_nombre(abs(num))} """, globals(), locals())
            else:
                if sign is False:
                    return str(num)
                else:
                    return myst(r""" - \py{str(num)} """, globals(), locals()) if num < 0 else myst(r""" + \py{str(num)} """, globals(), locals())
        else:
            num = expr.p
            den = expr.q
            # Pour les fractions, simplifier d'abord puis formater
            if abs(num) >= 1000 and abs(den) >= 1000:
                from math import gcd
                pgcd = gcd(abs(num), abs(den))
                if pgcd > 1:
                    num_simp = num // pgcd
                    den_simp = den // pgcd
                    if abs(num_simp) < 1000 and abs(den_simp) < 1000:
                        if sign is False:
                            return myst(r"""\py{disp}\frac{\py{num_simp}}{\py{den_simp}}""", globals(), locals()) if num_simp > 0 else myst(r"""-\py{disp}\frac{\py{abs(num_simp)}}{\py{den_simp}}""", globals(), locals())
                        else:
                            return myst(r"""+ \py{disp}\frac{\py{num_simp}}{\py{den_simp}}""", globals(), locals()) if num_simp > 0 else myst(r"""- \py{disp}\frac{\py{abs(num_simp)}}{\py{den_simp}}""", globals(), locals())
            
            # Sinon, formater avec espaces pour les grands nombres
            if abs(num) >= 1000:
                num_formatted = formater_nombre(abs(num))
            else:
                num_formatted = str(abs(num))
                
            if abs(den) >= 1000:
                den_formatted = formater_nombre(den)
            else:
                den_formatted = str(den)
                
            if sign is False:
                return myst(r"""\py{disp}\frac{\py{num_formatted}}{\py{den_formatted}}""", globals(), locals()) if num > 0 else myst(r"""-\py{disp}\frac{\py{num_formatted}}{\py{den_formatted}}""", globals(), locals())
            else:
                return myst(r"""+\; \py{disp}\frac{\py{num_formatted}}{\py{den_formatted}}""", globals(), locals()) if num > 0 else myst(r"""- \;\py{disp}\frac{\py{num_formatted}}{\py{den_formatted}}""", globals(), locals())
    else:
        try:
            from sympy import latex as sympy_latex
            if sign is False:
                return sympy_latex(expr)
            else:
                if str(expr.startswith('-')):
                    return myst(r""" \py{disp}sympy_latex(expr)""", globals(), locals())
                else:
                    return myst(r"""+ \py{disp}\py{sympy_latex(expr)}""", globals(), locals())
        except:
            try:
                if expr < 0:
                    return myst(r""" -\; \py{disp} \py{sympy_latex(abs(expr))}""", globals(), locals())
                else:
                    return myst(r"""+ \;\py{disp} \py{sympy_latex(expr)}""", globals(), locals())
            except:
                return str(expr)

def pxsl_latex_avec_formatage(expr, sign = False, display = True):
    """
    Wrapper LaTeX qui applique le formatage des nombres.
    
    Cette fonction prend une expression et la convertit en format LaTeX en appliquant
    un formatage spécial pour les grands nombres (>= 1000). Elle gère les entiers,
    flottants, fractions rationnelles et expressions SymPy.
    
    Parameters
    ----------
    expr : int, float, sympy.Rational, or sympy.Expr
        L'expression à convertir en LaTeX avec formatage.
    
    Returns
    -------
    str
        La représentation LaTeX de l'expression avec formatage appliqué.
    
    Examples
    --------
    >>> pxsl_latex_avec_formatage(1500)
    '1\\ 500'

    >>> pxsl_latex_avec_formatage(Rational(2000, 3))
    '\\frac{2\\ 000}{3}'

    >>> pxsl_latex_avec_formatage(Rational(1, 2))
    '\\frac{1}{2}'

    :pxs_trigger: idem latex_avec_formatage, variante préfixée pxsl_, formatage LaTeX d'un nombre ou d'une fraction avec milliers ; version FR historique, ne pas confondre avec ``pxsl_latex_with_formatting`` qui est bilingue
    :pxs_returns: |
        chaîne LaTeX identique à ``latex_avec_formatage`` : fraction en \displaystyle,
        nombre avec séparateurs, signe optionnel préfixé.
    :pxs_example: |
        pxsl_latex_avec_formatage(Rational(1, 2))
    :pxs_antipattern: Dupliquer cette logique dans chaque exercice au lieu d'importer la fonction.
    """
    if display:
        disp = '\displaystyle '
    else:
        disp = ' '
    if expr == oo or expr == -oo:
        return pxsl_formater_nombre(expr)
    if isinstance(expr, (int, Integer, float, Float)) and abs(expr) >= 1000:
        if sign is False:
            return pxsl_formater_nombre(expr)
        else:
            return myst(r""" - \;\py{pxsl_formater_nombre(abs(expr))} """, globals(), locals()) if expr < 0 else myst(r""" + \;\py{pxsl_formater_nombre(abs(expr))} """, globals(), locals())
    elif isinstance(expr, Rational):
        if expr.q == 1:
            num = expr.p
            if abs(num) >= 1000:
                if sign is False:
                    return pxsl_formater_nombre(num)
                else:
                    return myst(r""" - \py{pxsl_formater_nombre(abs(num))} """, globals(), locals()) if num < 0 else myst(r""" + \py{pxsl_formater_nombre(abs(num))} """, globals(), locals())
            else:
                if sign is False:
                    return str(num)
                else:
                    return myst(r""" - \py{str(num)} """, globals(), locals()) if num < 0 else myst(r""" + \py{str(num)} """, globals(), locals())
        else:
            num = expr.p
            den = expr.q
            # Pour les fractions, simplifier d'abord puis formater
            if abs(num) >= 1000 and abs(den) >= 1000:
                from math import gcd
                pgcd = gcd(abs(num), abs(den))
                if pgcd > 1:
                    num_simp = num // pgcd
                    den_simp = den // pgcd
                    if abs(num_simp) < 1000 and abs(den_simp) < 1000:
                        if sign is False:
                            return myst(r"""\py{disp}\frac{\py{num_simp}}{\py{den_simp}}""", globals(), locals()) if num_simp > 0 else myst(r"""-\py{disp}\frac{\py{abs(num_simp)}}{\py{den_simp}}""", globals(), locals())
                        else:
                            return myst(r"""+ \py{disp}\frac{\py{num_simp}}{\py{den_simp}}""", globals(), locals()) if num_simp > 0 else myst(r"""- \py{disp}\frac{\py{abs(num_simp)}}{\py{den_simp}}""", globals(), locals())
            
            # Sinon, formater avec espaces pour les grands nombres
            if abs(num) >= 1000:
                num_formatted = pxsl_formater_nombre(abs(num))
            else:
                num_formatted = str(abs(num))
                
            if abs(den) >= 1000:
                den_formatted = pxsl_formater_nombre(den)
            else:
                den_formatted = str(den)
                
            if sign is False:
                return myst(r"""\py{disp}\frac{\py{num_formatted}}{\py{den_formatted}}""", globals(), locals()) if num > 0 else myst(r"""-\py{disp}\frac{\py{num_formatted}}{\py{den_formatted}}""", globals(), locals())
            else:
                return myst(r"""+\; \py{disp}\frac{\py{num_formatted}}{\py{den_formatted}}""", globals(), locals()) if num > 0 else myst(r"""- \;\py{disp}\frac{\py{num_formatted}}{\py{den_formatted}}""", globals(), locals())
    else:
        try:
            from sympy import latex as sympy_latex
            if sign is False:
                return sympy_latex(expr)
            else:
                if str(expr.startswith('-')):
                    return myst(r""" \py{disp}sympy_latex(expr)""", globals(), locals())
                else:
                    return myst(r"""+ \py{disp}\py{sympy_latex(expr)}""", globals(), locals())
        except:
            try:
                if expr < 0:
                    return myst(r""" -\; \py{disp} \py{sympy_latex(abs(expr))}""", globals(), locals())
                else:
                    return myst(r"""+ \;\py{disp} \py{sympy_latex(expr)}""", globals(), locals())
            except:
                return str(expr)

def pxsl_latex_with_formatting(expr, sign=False, display=True):
    """
    \en{LaTeX wrapper that applies number formatting.}
    \fr{Wrapper LaTeX qui applique le formatage des nombres.}
    
    \en{This function converts an expression to LaTeX and applies special formatting
    for large numbers (>= 1000). It handles integers, floats, rational fractions,
    and general SymPy expressions.}
    \fr{Cette fonction convertit une expression en LaTeX et applique un formatage
    spécial pour les grands nombres (>= 1000). Elle gère les entiers, flottants,
    fractions rationnelles et expressions SymPy.}
    
    Parameters
    ----------
    expr : int, float, sympy.Rational, or sympy.Expr
        \en{Expression to convert to LaTeX with formatting.}
        \fr{Expression à convertir en LaTeX avec formatage.}
    sign : bool, optional
        \en{If True, explicitly prefixes a sign ('+' or '-'). Default: False.}
        \fr{Si True, préfixe explicitement un signe ('+' ou '-'). Par défaut : False.}
    display : bool, optional
        \en{If True, uses `\displaystyle` for the LaTeX output. Default: True.}
        \fr{Si True, utilise `\displaystyle` pour la sortie LaTeX. Par défaut : True.}
    
    Returns
    -------
    str
        \en{The LaTeX string with number formatting applied.}
        \fr{La chaîne LaTeX avec formatage appliqué.}
    
    Examples
    --------
    >>> pxsl_latex_with_formatting(1500)
    '1\\ 500'
    >>> pxsl_latex_with_formatting(Rational(2000, 3))
    '\\frac{2\\ 000}{3}'
    >>> pxsl_latex_with_formatting(Rational(1, 2))
    '\\frac{1}{2}'

    :pxs_trigger: affichage LaTeX bilingue (FR/EN) d'un nombre, d'une fraction ou d'une expression symbolique avec formatage des milliers, intégration automatique de pxs_config() (virgule/point selon langue) ; version à préférer dans tous les nouveaux exercices PyxiScience
    :pxs_returns: |
        chaîne LaTeX bilingue : grands entiers avec ``\ ``, Rational en ``\displaystyle\frac``,
        expressions sympy rendues via ``sympy_latex(expr, **pxs_config())``, signe ``+``/``-``
        préfixé si ``sign=True``.
    :pxs_example: |
        myst(r"x = \py{pxsl_latex_with_formatting(Rational(-5,2), sign=True)}")
    :pxs_antipattern: Utiliser ``latex_avec_formatage`` (FR-only) dans un exercice exporté en EN, ou oublier d'intégrer la virgule décimale selon la langue.
    """
    config_standard = pxs_config()

    if display:
        disp = '\displaystyle '
    else:
        disp = ' '
    
    if expr == oo or expr == -oo:
        return pxsl_format_number(expr)
    
    if isinstance(expr, (int, Integer, float, Float)) and abs(expr) >= 1000:
        if sign == False:
            return pxsl_format_number(expr)
        else:
            return myst(r""" - \;\py{pxsl_format_number(abs(expr))} """, globals(), locals()) if expr < 0 else myst(r""" + \;\py{pxsl_format_number(abs(expr))} """, globals(), locals())
    
    elif isinstance(expr, Rational):
        if expr.q == 1:
            num = expr.p
            if abs(num) >= 1000:
                if sign == False:
                    return pxsl_format_number(num)
                else:
                    return myst(r""" - \py{pxsl_format_number(abs(num))} """, globals(), locals()) if num < 0 else myst(r""" + \py{pxsl_format_number(abs(num))} """, globals(), locals())
            else:
                if sign == False:
                    return str(num)
                else:
                    return myst(r""" - \py{str(abs(num))} """, globals(), locals()) if num < 0 else myst(r""" + \py{str(num)} """, globals(), locals())
        else:
            num = expr.p
            den = expr.q
            # For fractions, simplify first and then format
            if abs(num) >= 1000 and abs(den) >= 1000:
                from math import gcd
                gcd_val = gcd(abs(num), abs(den))
                if gcd_val > 1:
                    num_simplified = num // gcd_val
                    den_simplified = den // gcd_val
                    if abs(num_simplified) < 1000 and abs(den_simplified) < 1000:
                        if sign == False:
                            return myst(r"""\py{disp}\frac{\py{num_simplified}}{\py{den_simplified}}""", globals(), locals()) if num_simplified > 0 else myst(r"""-\py{disp}\frac{\py{abs(num_simplified)}}{\py{den_simplified}}""", globals(), locals())
                        else:
                            return myst(r"""+ \py{disp}\frac{\py{num_simplified}}{\py{den_simplified}}""", globals(), locals()) if num_simplified > 0 else myst(r"""- \py{disp}\frac{\py{abs(num_simplified)}}{\py{den_simplified}}""", globals(), locals())
            
            # Otherwise, format with spaces for large numbers
            if abs(num) >= 1000:
                num_formatted = pxsl_format_number(abs(num))
            else:
                num_formatted = str(abs(num))
                
            if abs(den) >= 1000:
                den_formatted = pxsl_format_number(den)
            else:
                den_formatted = str(den)
                
            if sign == False:
                return myst(r"""\py{disp}\frac{\py{num_formatted}}{\py{den_formatted}}""", globals(), locals()) if num > 0 else myst(r"""-\py{disp}\frac{\py{num_formatted}}{\py{den_formatted}}""", globals(), locals())
            else:
                return myst(r"""+\; \py{disp}\frac{\py{num_formatted}}{\py{den_formatted}}""", globals(), locals()) if num > 0 else myst(r"""- \;\py{disp}\frac{\py{num_formatted}}{\py{den_formatted}}""", globals(), locals())
    
    else:
        try:
            from sympy import latex as sympy_latex
            if sign == False:
                return sympy_latex(expr)
            else:
                if str(expr.startswith('-')) or expr.could_extract_minus_sign():
                    return myst(r""" \py{disp}sympy_latex(expr, **config_standard)""", globals(), locals())
                else:
                    return myst(r"""+ \py{disp}\py{sympy_latex(expr, **config_standard)}""", globals(), locals())
        except:
            try:
                if expr < 0:
                    return myst(r""" -\; \py{disp} \py{sympy_latex(abs(expr), **config_standard)}""", globals(), locals())
                else:
                    return myst(r"""+ \;\py{disp} \py{sympy_latex(expr, **config_standard)}""", globals(), locals())
            except:
                return myst(r"""\py{sympy_latex(expr, **config_standard)}""", globals(), locals())


def latex_coefficient(coeff, variable = None, sign = False, zeros = True, ones = False, display = True):
    """
    Formats a coefficient for LaTeX display.
    
    This function formats a coefficient for display in a LaTeX polynomial expression.
    It handles special cases where the coefficient is 1 or -1 and provides options for
    displaying signs, omitting zeros, or showing numerical ones.
    
    Parameters
    ----------
    coeff : int, float, or sympy.Expr
        The coefficient to format.
    sign : None or '+'
        If '+', a '+' sign is displayed before the expression when it is positive.
    variable : str or Symbol, optional
        Expression or variable attached to the coefficient (can be omitted if zeros=False).
    zeros : bool, default True
        If False, the coefficient and its variable are not written when the coefficient is zero.
    ones : bool, default False
        If False, -1 is written as '-' and 1 as an empty string.
        If True, both -1 and 1 are kept as numeric values.
    display : bool, optional
        Whether to produce display-mode LaTeX (used in the examples below).
    
    Returns
    -------
    str
        The coefficient formatted for LaTeX. Returns an empty string for coeff=1,
        '-' for coeff=-1, and the formatted representation otherwise.
    
    Examples
    --------
    >>> pxsl_latex_coefficient(1)
    ''
    >>> pxsl_latex_coefficient(-1, ones = True)
    '-1'
    >>> pxsl_latex_coefficient(-1)
    '-'
    >>> pxsl_latex_coefficient(5)
    '5'
    >>> pxsl_latex_coefficient(5, sign = True)
    '+5'
    >>> pxsl_latex_coefficient(1500)
    '1\\ 500'
    >>> pxsl_latex_coefficient(0, variable = Symbol('L_1'), zeros = True)
    '0L_1'
    >>> pxsl_latex_coefficient(0, variable = Symbol('L_1'), zeros = False)
    ''
    >>> pxsl_latex_coefficient(Rational(-5, 2), sign = '+', display = False)
    '-\\frac{5}{2}'
    >>> pxsl_latex_coefficient(Rational(-5, 2), sign='+')
    '-\\displaystyle \\frac{5}{2}'

    :pxs_trigger: affichage d'un coefficient dans un polynôme avec cas spéciaux 1→"", -1→"-", 0→"" si zeros=False, variable attachée après le coefficient (5x, -y, ...), préfixe "+" pour chaînage, délègue à pxsl_latex_with_formatting pour les autres cas
    :pxs_returns: |
        chaîne LaTeX du coefficient : vide pour ``1``, ``"-"`` pour ``-1``, nombre formaté sinon ;
        avec ``"\;"`` entre signe et valeur si ``sign=True`` ; concatène la variable si fournie.
    :pxs_example: |
        myst(r"\py{latex_coefficient(5, Symbol('x'))} \py{latex_coefficient(-1, Symbol('y'), sign=True)}")
    :pxs_antipattern: Écrire ``f"{coef}x"`` à la main sans gérer les cas ±1 et 0, ou afficher "1x" au lieu de "x".
    """
    config_standard = pxs_config()
    if zeros == False and coeff == 0:
        return myst(r""" """)
    elif variable is not None:
        return myst(
            r"""\py{pxsl_latex_coefficient(coeff, sign=sign, zeros=zeros, ones=ones, display=display)}\py{latex(variable, **config_standard)}""",
            globals(), locals()
        )
    if coeff == 1:
        if sign:
            return myst(r""" +\; """) if ones == False else myst(r"""+ \;\py{latex(coeff, **config_standard)} """, globals(), locals())
        else:
            return myst(r""" """) if ones == False else myst(r"""\py{latex(coeff, **config_standard)} """, globals(), locals())
    elif coeff == -1:
        if sign:
            return myst(r""" -\; """) if ones == False else myst(r"""- \;\py{latex(abs(coeff), **config_standard)} """, globals(), locals())
        else:
            return myst(r""" - """) if ones == False else myst(r"""\py{latex(coeff, **config_standard)} """, globals(), locals())
    else:
        return pxsl_latex_with_formatting(coeff, sign=sign, display=display)


def pxsl_latex_coefficient(coeff, variable=None, sign=False, zeros=True, ones=False, display=True):
    """
    Formats a coefficient for LaTeX display.
    
    This function formats a coefficient for display in a LaTeX polynomial expression.
    It handles special cases where the coefficient is 1 or -1 and provides options for
    displaying signs, omitting zeros, or showing numerical ones.
    
    Parameters
    ----------
    coeff : int, float, or sympy.Expr
        The coefficient to format.
    sign : None or '+'
        If '+', a '+' sign is displayed before the expression when it is positive.
    variable : str or Symbol, optional
        Expression or variable attached to the coefficient (can be omitted if zeros=False).
    zeros : bool, default True
        If False, the coefficient and its variable are not written when the coefficient is zero.
    ones : bool, default False
        If False, -1 is written as '-' and 1 as an empty string.
        If True, both -1 and 1 are kept as numeric values.
    display : bool, optional
        Whether to produce display-mode LaTeX (used in the examples below).
    
    Returns
    -------
    str
        The coefficient formatted for LaTeX. Returns an empty string for coeff=1,
        '-' for coeff=-1, and the formatted representation otherwise.
    
    Examples
    --------
    >>> pxsl_latex_coefficient(1)
    ''
    >>> pxsl_latex_coefficient(-1, ones = True)
    '-1'
    >>> pxsl_latex_coefficient(-1)
    '-'
    >>> pxsl_latex_coefficient(5)
    '5'
    >>> pxsl_latex_coefficient(5, sign = True)
    '+5'
    >>> pxsl_latex_coefficient(1500)
    '1\\ 500'
    >>> pxsl_latex_coefficient(0, variable = Symbol('L_1'), zeros = True)
    '0L_1'
    >>> pxsl_latex_coefficient(0, variable = Symbol('L_1'), zeros = False)
    ''
    >>> pxsl_latex_coefficient(Rational(-5, 2), sign = '+', display = False)
    '-\\frac{5}{2}'
    >>> pxsl_latex_coefficient(Rational(-5, 2), sign='+')
    '-\\displaystyle \\frac{5}{2}'

    :pxs_trigger: version préfixée pxsl_ de latex_coefficient, gestion coefficient + variable dans un polynôme/somme avec cas ±1 et 0, affichage d'un terme a_i·x^i ; version à préférer dans les nouveaux scripts PyxiScience
    :pxs_returns: |
        identique à ``latex_coefficient`` : chaîne LaTeX du coefficient (vide pour 1, "-" pour -1)
        avec variable optionnelle attachée et préfixe de signe optionnel.
    :pxs_example: |
        pxsl_latex_coefficient(-5, Symbol('x'), sign=True)  # "- \;5 x"
    :pxs_antipattern: Gérer manuellement les cas particuliers ±1 et 0 à chaque ligne de polynôme.
    """
    config_standard = pxs_config()
    if zeros == False and coeff == 0:
        return myst(r""" """)
    elif variable is not None:
        return myst(
            r"""\py{pxsl_latex_coefficient(coeff, sign=sign, zeros=zeros, ones=ones, display=display)}\py{latex(variable, **config_standard)}""",
            globals(), locals()
        )
    if coeff == 1:
        if sign:
            return myst(r""" +\; """) if ones == False else myst(r"""+ \;\py{latex(coeff, **config_standard)} """, globals(), locals())
        else:
            return myst(r""" """) if ones == False else myst(r"""\py{latex(coeff, **config_standard)} """, globals(), locals())
    elif coeff == -1:
        if sign:
            return myst(r""" -\; """) if ones == False else myst(r"""- \;\py{latex(abs(coeff), **config_standard)} """, globals(), locals())
        else:
            return myst(r""" - """) if ones == False else myst(r"""\py{latex(coeff, **config_standard)} """, globals(), locals())
    else:
        return pxsl_latex_with_formatting(coeff, sign=sign, display=display)


def to_rational_or_symbol(value):
    """
    Convertit un nombre en Rational SymPy ou garde un symbole SymPy.
    
    Cette fonction prend une valeur et la convertit en objet Rational de SymPy
    si c'est un nombre, ou la garde telle quelle si c'est déjà un symbole SymPy.
    Pour les flottants, elle utilise Fraction pour une conversion précise.
    
    Parameters
    ----------
    value : int, float, sympy.Symbol, or sympy.Rational
        La valeur à convertir.
    
    Returns
    -------
    sympy.Rational or sympy.Symbol or any
        La valeur convertie en Rational si c'est un nombre, ou la valeur
        originale si c'est un symbole ou autre type.
    
    Examples
    --------
    >>> from sympy import Symbol
    >>> x = Symbol('x')
    >>> to_rational_or_symbol(5)
    Rational(5, 1)

    >>> to_rational_or_symbol(0.5)
    Rational(1, 2)
    
    >>> to_rational_or_symbol(0.5)
    Rational(1, 2)

    >>> to_rational_or_symbol(x)
    Symbol('x')

    :pxs_trigger: normaliser une entrée utilisateur (int, float, Rational, Symbol) en Rational sympy exact pour manipulation algébrique, conversion précise des floats via Fraction.from_float(...).limit_denominator(), conservation des symboles ; version historique FR — préférer ``pxsl_to_rational_or_symbol``
    :pxs_returns: |
        objet sympy : ``Rational`` si ``value`` est numérique, la ``value`` originale si c'est un
        ``Symbol``, sinon identité. Les floats passent par ``Fraction`` pour éviter l'imprécision binaire.
    :pxs_example: |
        a = to_rational_or_symbol(0.5)  # → Rational(1, 2), pas 0.5 binaire
    :pxs_antipattern: Appeler ``Rational(0.5)`` directement, ce qui produit une approximation binaire grossière du float.
    """
    if isinstance(value, Symbol):
        return value
    elif isinstance(value, (int, Rational)):
        return Rational(value)
    elif isinstance(value, float):
        frac = Fraction.from_float(value).limit_denominator()
        return Rational(frac.numerator, frac.denominator)
    else:
        return value

def pxsl_to_rational_or_symbol(value):
    r"""
    \en{Converts a number to a SymPy Rational or keeps a SymPy symbol as is.}
    \fr{Convertit un nombre en Rational SymPy ou garde un symbole SymPy tel quel.}
    
    \en{This function takes a value and converts it into a SymPy `Rational`
    object if it is numeric, or keeps it unchanged if it is already a SymPy `Symbol`.
    For floats, it uses Python's `Fraction` class to ensure a precise rational conversion.}
    \fr{Cette fonction prend une valeur et la convertit en objet `Rational` de SymPy
    si c’est un nombre, ou la garde telle quelle si c’est déjà un symbole SymPy.
    Pour les flottants, elle utilise la classe `Fraction` de Python pour une conversion rationnelle précise.}
    
    Parameters
    ----------
    value : int, float, sympy.Symbol, or sympy.Rational
        \en{The value to convert.}
        \fr{La valeur à convertir.}
    
    Returns
    -------
    sympy.Rational or sympy.Symbol or any
        \en{The value converted to `Rational` if numeric, or the original value
        if it is a symbol or another type.}
        \fr{La valeur convertie en `Rational` si c’est un nombre, ou la valeur
        originale si c’est un symbole ou un autre type.}
    
    Examples
    --------
    >>> from sympy import Symbol
    >>> x = Symbol('x')
    >>> pxsl_to_rational_or_symbol(5)
    Rational(5, 1)

    >>> pxsl_to_rational_or_symbol(0.5)
    Rational(1, 2)

    >>> pxsl_to_rational_or_symbol(x)
    Symbol('x')

    :pxs_trigger: idem to_rational_or_symbol, variante préfixée pxsl_ à utiliser dans les nouveaux scripts, conversion exacte des floats en Rational via Fraction, garder les Symbol intacts, bilingue par convention de nommage
    :pxs_returns: |
        ``sympy.Rational`` exact si ``value`` est numérique, ou la ``value`` inchangée si elle
        est déjà un Symbol ou un autre type non numérique.
    :pxs_example: |
        pxsl_to_rational_or_symbol(x)  # → x si x est un Symbol
        pxsl_to_rational_or_symbol(0.25)  # → Rational(1, 4)
    :pxs_antipattern: Utiliser ``sympify(0.1)`` pour obtenir une fraction exacte (ne le fait pas), ou ``Rational(0.1)`` directement.
    """
    if isinstance(value, Symbol):
        return value
    elif isinstance(value, (int, Rational)):
        return Rational(value)
    elif isinstance(value, float):
        frac = Fraction.from_float(value).limit_denominator()
        return Rational(frac.numerator, frac.denominator)
    else:
        return value

def resoudre_inequation_generale(a = 1, b = 0, c = 0, variable = "x", inegalite = ">=", domaine = "R", puissance = 1, signe_a = None, detail_signe_a = False):
    """
    Solves an inequality of the form ax^p + b ≥ c with detailed step-by-step reasoning in LaTeX.

    This function solves linear (p=1) or quadratic (p=2) inequalities and generates
    a complete LaTeX-formatted solution showing all intermediate steps. It handles
    symbolic coefficients, different domains (real, integer, natural numbers), and
    cases where the sign of coefficient 'a' needs to be analyzed separately.

    Parameters
    ----------
    a : int, float, or sympy expression, optional
        Coefficient of the variable term. Default is 1.
    b : int, float, or sympy expression, optional
        Constant term on the left side. Default is 0.
    c : int, float, or sympy expression, optional
        Constant term on the right side. Default is 0.
    variable : str, optional
        Name of the variable. Default is "x".
    inegalite : str, optional
        Inequality symbol: ">=", ">", "<=", or "<". Default is ">=".
    domaine : str, optional
        Solution domain: "R" (reals), "Z" (integers), or "N" (natural numbers).
        Default is "R".
    puissance : int, optional
        Exponent of the variable: 1 (linear) or 2 (quadratic). Default is 1.
    signe_a : str or None, optional
        Sign of coefficient 'a' when symbolic: ">" for positive, "<" for negative,
        or None to determine automatically. Default is None.
    detail_signe_a : bool, optional
        Whether to explicitly mention the sign of 'a' when dividing. Default is False.

    Returns
    -------
    tuple
        A tuple (solution_set, latex_reasoning) where:
        - solution_set : sympy set or dict
            The solution set. Returns a dict with cases if the sign of 'a'
            or the right-hand side is undetermined.
        - latex_reasoning : str
            Complete LaTeX-formatted step-by-step solution.

    Raises
    ------
    ValueError
        If inegalite is not in [">=", ">", "<=", "<"].
        If domaine is not in ["R", "Z", "N"].
        If puissance is not 1 or 2.
        If signe_a is not None, ">", or "<".

    Examples
    --------
    >>> # Simple linear inequality
    >>> sol, latex = resoudre_inequation_generale(2, 3, 7, variable="x", inegalite=">=")
    >>> print(sol)
    [2, oo)

    >>> # Quadratic inequality
    >>> sol, latex = resoudre_inequation_generale(1, 0, 4, puissance=2, inegalite="<=")
    >>> print(sol)
    [-2, 2]

    >>> # Integer domain
    >>> sol, latex = resoudre_inequation_generale(3, -1, 5, domaine="Z", inegalite=">")
    >>> print(sol)
    {3, 4, 5, ...}

    >>> # Symbolic coefficient with sign analysis
    >>> from sympy import Symbol
    >>> a = Symbol('a')
    >>> sol, latex = resoudre_inequation_generale(a, 0, 5, inegalite=">=")
    >>> # Returns dict with cases for a>0 and a<0

    :pxs_trigger: résoudre ET corriger pas-à-pas une inéquation ax^p + b ⋛ c (p ∈ {1, 2}), corrigé LaTeX complet en \begin{align*}, domaine R/Z/N, coefficients symboliques ou numériques, discussion automatique du signe de a quand indéterminé ; version historique FR — préférer ``pxsl_solve_general_inequality`` en bilingue
    :pxs_returns: |
        tuple ``(ensemble_solution, raisonnement_latex)`` :
        - ``ensemble_solution`` : ``sympy.Interval`` / ``Union`` / ``EmptySet`` / ``Intersection``,
          ou ``dict`` avec cas ``{"a>0": ..., "a<0": ...}`` / ``{"rhs>0": ..., "rhs<0": ...}``
          si le signe de ``a`` ou de ``c-b`` est indéterminé ;
        - ``raisonnement_latex`` : chaîne MyST avec un ``\begin{equation*}\begin{align*}``
          détaillant toutes les étapes jusqu'à l'ensemble solution.
    :pxs_example: |
        sol, corrige = resoudre_inequation_generale(2, 3, 7, variable="x", inegalite=">=")
        # dans le .md : Solutions : \py{latex(sol)}. Raisonnement : \py{corrige}
    :pxs_antipattern: Résoudre à la main avec ``sympy.solve`` puis rédiger séparément le raisonnement LaTeX étape par étape (duplication + risques d'incohérence).
    """


    # ======= FONCTIONS AUXILIAIRES =================

    def __ceil(x):
        return (x if x.is_integer else floor(x) + 1)

    def __simplifier_signes(chaine):
        return chaine.replace("+ + ", "+ ").replace("+ -", "-").replace("- + ", "- ").replace("- -", "+")

    def __test_a_frac(a):
        if isinstance(a, Rational) and a.q != 1:
            return True
        if isinstance(a, Mul):
            for fac in a.args:
                if isinstance(fac, Rational) or (isinstance(fac, Pow) and fac.args[1].is_integer and fac.args[1].is_negative):
                    return True
        return False


    def __solutions_inequation_generale(a=1, b=0, c=0, inegalite=">=", domaine="R", puissance=1, signe_a=None, signe_quotient = None):
        from src.scripts.Mes_fctions.Classes_Extensions import pxs_Interval

        a = sympify(a)
        b = sympify(b)
        c = sympify(c)
        dico_ensembles = {"R" : Reals, "N" : Naturals, "Z" : Integers}
        ensemble = dico_ensembles[domaine]
        quotient = (c - b) / a
        if a == 0:
            valeur = b - c
            dico_cas_existence = {"<=" : valeur.is_nonpositive, "<" : valeur.is_negative,
                                    ">=" : valeur.is_nonnegative, ">" : valeur.is_positive}
            cas_existence = dico_cas_existence[inegalite]
            sol = ensemble if cas_existence else EmptySet
        elif a.is_negative or signe_a == "<":
            dico_inverse = {"<=" : ">=", "<" : ">", ">=" : "<=", ">" : "<"}
            symb_inverse = dico_inverse[inegalite]
            return __solutions_inequation_generale(-a, -b, -c, inegalite = symb_inverse, domaine = domaine, puissance = puissance, signe_a = ">", signe_quotient = signe_quotient)
        elif a.is_nonnegative or signe_a == ">":

            if puissance == 1:
                if inegalite == ">=":
                    sol = pxs_Interval(quotient, oo)
                elif inegalite == ">":
                    sol = pxs_Interval.open(quotient, oo)
                elif inegalite == "<=":
                    sol = pxs_Interval(-oo, quotient)
                else:
                    sol = pxs_Interval.open(-oo, quotient)

            elif puissance == 2:
                if quotient.is_negative or signe_quotient == "<":
                    if inegalite in [">=", ">"]:
                        sol = ensemble
                    else:
                        sol = EmptySet
                elif quotient.is_nonnegative or signe_quotient == ">":
                    racine = simplify(sqrt(quotient))
                    if inegalite == ">=":
                        sol = pxs_Interval(-oo, -racine).union(pxs_Interval(racine, oo))
                    elif inegalite == ">":
                        sol = pxs_Interval.open(-oo, -racine).union(pxs_Interval.open(racine, oo))
                    elif inegalite == "<=":
                        sol = pxs_Interval(-racine, racine)
                    else:
                        sol = pxs_Interval.open(-racine, racine)
                else: # cas où le signe de quotient est indéterminé
                    sol_rhs_pos =  __solutions_inequation_generale(a, b, c, inegalite = inegalite, domaine = domaine, puissance = puissance, signe_a = signe_a, signe_quotient = ">")
                    sol_rhs_neg =  __solutions_inequation_generale(a, b, c, inegalite = inegalite, domaine = domaine, puissance = puissance, signe_a = signe_a, signe_quotient = "<")
                    return {"rhs>0" : sol_rhs_pos, "rhs<0" : sol_rhs_neg}


        else: # cas où le signe de a est indéterminé
            sol_pos = __solutions_inequation_generale(a, b, c, inegalite = inegalite, domaine = domaine, puissance = puissance, signe_a = ">", signe_quotient = signe_quotient)
            sol_neg = __solutions_inequation_generale(a, b, c, inegalite = inegalite, domaine = domaine, puissance = puissance, signe_a = "<", signe_quotient = signe_quotient)
            return {"a>0" : sol_pos, "a<0" : sol_neg}

        if domaine in ["Z", "N"]:
            try:
                sol = sol.intersect(Integers) if domaine == "Z" else sol.intersect(Naturals0)
            except:
                sol = Intersection(sol, Integers, evaluate = False) if domaine == "Z" else Intersection(sol, Naturals0, evaluate = False)

        return sol

    # ===================================================================

    if inegalite not in [">=", ">", "<=", "<"]:
        raise ValueError("Inégalité non valide")
    if domaine not in ["R", "Z", "N"]:
        raise ValueError("Domaine non valide")
    if puissance not in [1, 2]:
        raise ValueError("Puissance non valide (1 ou 2 seulement)")
    if signe_a not in [None, ">", "<"]:
        raise ValueError("Signe de a non valide. Utilisez None, '>' pour positif, ou '<' pour négatif.")

    # Convertir les paramètres
    a = to_rational_or_symbol(a)
    b = to_rational_or_symbol(b)
    c = to_rational_or_symbol(c)

    # Symbole associé à la variable
    var_symb = Symbol(variable)

    ensemble_solution = __solutions_inequation_generale(a, b, c, inegalite, domaine, puissance, signe_a)

    # Si le signe de a n'est pas déterminé, on distingue deux cas :
    if not (signe_a in [">", "<"] or sympify(a).is_nonpositive or sympify(a).is_nonnegative):
        latex_a = latex_avec_formatage(a)

        raisonnement_latex = myst(r"""On distingue deux cas :
1. Si \py{latex_a} > 0 :
""", locals(), globals())
        raisonnement_latex += resoudre_inequation_generale(a, b, c, variable = variable, inegalite = inegalite, domaine = domaine, puissance = puissance, signe_a = ">")[-1]
        raisonnement_latex += myst(r"""
2. Si \py{latex_a} < 0 :
""", locals(), globals())
        raisonnement_latex += resoudre_inequation_generale(a, b, c, variable = variable, inegalite = inegalite, domaine = domaine, puissance = puissance, signe_a = "<")[-1]

        raisonnement_latex = __simplifier_signes(raisonnement_latex)
        return ensemble_solution, raisonnement_latex # L'ensemble des solutions est indéterminé

    raisonnement_latex = myst(r"""\begin{equation*}\begin{align*}""", locals(), globals())

    # symbole d'inégalité initial (et son affichage latex)
    symb = inegalite
    dico_symboles_latex = {">=": myst(r"""\geq""", locals(), globals()), ">": myst(r""">""", locals(), globals()), "<=": myst(r"""\leq""", locals(), globals()), "<": myst(r"""<""", locals(), globals())}
    symb_inegalite = dico_symboles_latex[inegalite]

    # Construire l'inéquation d'origine
    # si a est une somme, on met des parenthèses autour
    coeff_str = latex_coefficient(a)
    coeff_str = myst(r"""\left(\py{coeff_str}\right)""", locals(), globals()) if a.is_Add else coeff_str
    latex_c = latex_avec_formatage(c)

    # Expression du côté gauche
    if sympify(b).is_zero:
        expression = sympy_latex(a * var_symb ** puissance)
        expr_gauche = myst(r"""\py{expression}""", locals(), globals())
    elif isinstance(b, (int, Rational)) and b >= 0:
        latex_b = latex_avec_formatage(b)
        if puissance == 1:
            expr_gauche = myst(r"""\py{coeff_str}\py{variable} + \py{latex_b}""", locals(), globals()) if coeff_str else myst(r"""\py{variable} + \py{latex_b}""", locals(), globals())
        else:
            expr_gauche = myst(r"""\py{coeff_str}\py{variable}^2 + \py{latex_b}""", locals(), globals()) if coeff_str else myst(r"""\py{variable}^2 + \py{latex_b}""", locals(), globals())
    elif isinstance(b, (int, Rational)) and b < 0:
        latex_abs_b = latex_avec_formatage(abs(b))
        if puissance == 1:
            expr_gauche = myst(r"""\py{coeff_str}\py{variable} - \py{latex_abs_b}""", locals(), globals()) if coeff_str else myst(r"""\py{variable} - \py{latex_abs_b}""", locals(), globals())
        else:
            expr_gauche = myst(r"""\py{coeff_str}\py{variable}^2 - \py{latex_abs_b}""", locals(), globals()) if coeff_str else myst(r"""\py{variable}^2 - \py{latex_abs_b}""", locals(), globals())
    else:
        latex_b = latex_avec_formatage(b)
        if puissance == 1:
            expr_gauche = myst(r"""\py{coeff_str}\py{variable} + \py{latex_b}""", locals(), globals()) if coeff_str else myst(r"""\py{variable} + \py{latex_b}""", locals(), globals())
        else:
            expr_gauche = myst(r"""\py{coeff_str}\py{variable}^2 + \py{latex_b}""", locals(), globals()) if coeff_str else myst(r"""\py{variable}^2 + \py{latex_b}""", locals(), globals())


    # CAS DÉGÉNÉRÉ: a = 0
    if a == 0:
        latex_b_simple = latex_avec_formatage(b)
        raisonnement_latex += myst(r"""\py{latex_b_simple} \py{symb_inegalite} \py{latex_c}""", locals(), globals())

        if ensemble_solution == EmptySet:
            raisonnement_latex += myst(r"""\text{ impossible.}""", locals(), globals())
        else:
            raisonnement_latex += myst(r"""&\text{ toujours vrai.}""", locals(), globals())

        raisonnement_latex += myst(r"""\\ \end{align*}\end{equation*}""", locals(), globals())

        raisonnement_latex = __simplifier_signes(raisonnement_latex)

        return ensemble_solution, raisonnement_latex


    # Première ligne: l'inéquation d'origine
    raisonnement_latex += myst(r"""
\py{expr_gauche} \py{symb_inegalite} \py{latex_c}""", locals(), globals())


    valeur_droite = c - b

    # Étape 1: Isoler le terme en x - construire c - b avec gestion des signes
    if not sympify(b).is_zero: # si b est nul il n'y a rien à faire à cette étape
        latex_b = latex_avec_formatage(b)
        latex_c = latex_avec_formatage(c)
        if c == 0:
            latex_droite_etape1 = latex_avec_formatage(-b)
        elif b.is_Add:
            latex_droite_etape1 = latex_c + " - " + myst(r"""\left(\py{latex_b}\right)""", locals(), globals())
        else:
            latex_droite_etape1 = __simplifier_signes(latex_c + " - " + latex_b)

        if puissance == 1:
            terme_variable = myst(r"""\py{coeff_str}\py{variable}""", locals(), globals()) if coeff_str else variable
        else:
            terme_variable = myst(r"""\py{coeff_str}\py{variable}^2""", locals(), globals()) if coeff_str else myst(r"""\py{variable}^2""", locals(), globals())

        raisonnement_latex += myst(r""" &\iff \py{terme_variable} \py{symb_inegalite}
\py{latex_droite_etape1} \\""", locals(), globals())

        # Etape de simplification de c-b
        latex_mb = latex_avec_formatage(-b)
        expr_equiv = __simplifier_signes(myst(r"""\py{latex_mb} + \py{latex_c}""", locals(), globals())) # si la réecriture est équivalente, on ne la détaille pas
        if latex_droite_etape1 != latex_avec_formatage(c - b) and latex_avec_formatage(c - b) != expr_equiv:
            latex_droite_etape1 = latex_avec_formatage(c - b)
            raisonnement_latex += myst(r""" &\iff \py{terme_variable} \py{symb_inegalite}
\py{latex_droite_etape1}\\""", locals(), globals())



    else: # si b=0
        latex_droite_etape1 = latex_avec_formatage(c)

    # Pour la fraction, utiliser la même logique de gestion des signes
    latex_fraction_num = latex_droite_etape1
    latex_a = latex_avec_formatage(a)

    # A partir de là on va diviser par a : le sens des inégalités peut changer
    if sympify(a).is_negative or signe_a == "<":
        symb = {"<=" : ">=", "<" : ">", ">=" : "<=", ">" : "<"}[inegalite]
        symb_inegalite = dico_symboles_latex[symb]


    # Étape 2: Solution selon le signe de a (avec option signe_a)

    # Désormais le membre de gauche vaudra juste variable ou variable^2 :
    if puissance == 1:
        terme_variable = myst(r"""\py{variable}""", locals(), globals())
    else:
        terme_variable = myst(r"""\py{variable}^2""", locals(), globals())

    if signe_a is None:
        signe_a = ">" if sympify(a).is_positive else "<"

    if detail_signe_a or a.free_symbols:
        car_a = myst(r""", \quad \text{car } \py{latex_a} \py{signe_a} 0""", locals(), globals())
    else:
        car_a = " "

    if a == 1:
        pass
    elif a == -1:
        symb_inverse = {">=": myst(r"""\leq""", locals(), globals()), ">": myst(r"""<""", locals(), globals()), "<=": myst(r"""\geq""", locals(), globals()), "<": myst(r""">""", locals(), globals())}[inegalite]
        latex_membre_droite = latex_avec_formatage(b - c)
        raisonnement_latex += myst(r"""&\iff \py{terme_variable} \py{symb_inegalite} \py{latex_membre_droite}\\""", locals(), globals())
    elif c - b == 0:
        raisonnement_latex += myst(r"""&\iff \py{terme_variable} \py{symb_inegalite} 0 \py{car_a}\\""", locals(), globals())

    elif __test_a_frac(a): # S'il est plus pertinent de multiplier par 1/a que de diviser par a
        fraction = Mul(c - b, 1 / a, evaluate = False)
        latex_fraction = latex_avec_formatage(fraction)
        raisonnement_latex += myst(r"""&\iff \py{terme_variable} \py{symb_inegalite} \py{latex_fraction} \py{car_a}\\""", locals(), globals())
        fraction1 = Mul(c - b, 1 / a)
        if fraction1 != fraction:
            latex_fraction = latex_avec_formatage(fraction1)
            raisonnement_latex += myst(r"""&\iff \py{terme_variable} \py{symb_inegalite} \py{latex_fraction} \\""", locals(), globals())
    else:
        latex_fraction = myst(r"""\frac{\py{latex_fraction_num}}{\py{latex_a}}""", locals(), globals())

        latex_rhs = latex_avec_formatage((c - b) / a)
        if gcd(c - b, a) != 1 or a.is_noninteger:
            raisonnement_latex += myst(r"""&\iff \py{terme_variable} \py{symb_inegalite} \py{latex_fraction} \py{car_a}\\""", locals(), globals())
            raisonnement_latex += myst(r"""&\iff \py{terme_variable} \py{symb_inegalite} \py{latex_rhs} \\""", locals(), globals())
        else:
            raisonnement_latex += myst(r"""&\iff \py{terme_variable} \py{symb_inegalite} \py{latex_fraction} \py{car_a} \\""", locals(), globals())


    # Gestion domaine entier pour puissance = 1
    valeur_critique = (c - b) / a
    if puissance == 1 and domaine in ["Z", "N"]:
        if symb in [">=", ">"]:
            if symb == ">":
                valeurs_entieres_limites = valeur_critique + 1 if valeur_critique.is_integer else __ceil(valeur_critique)
            else:
                valeurs_entieres_limites = valeur_critique if valeur_critique.is_integer else __ceil(valeur_critique)
        else:
            if symb == "<":
                valeurs_entieres_limites = valeur_critique - 1 if valeur_critique.is_integer else floor(valeur_critique)
            else:
                valeurs_entieres_limites = floor(valeur_critique)

        if domaine == "Z" or (symb in [">=", ">"] and (not valeurs_entieres_limites.is_negative)): # on inclut le cas n >= C Naturel

            # N'ajouter la phrase explicative que si on change vraiment l'inégalité pour les entiers
            if valeur_critique.is_noninteger or symb in ['<', '>'] or not (valeur_critique.is_nonpositive or valeur_critique.is_nonnegative):

                # Ne pas répéter la ligne qui est déjà dans le raisonnement principal
                latex_limite = latex_avec_formatage(valeurs_entieres_limites)
                if symb == ">":
                    resultat_final = myst(r"""\py{variable} \geq \py{latex_limite}""", locals(), globals())
                elif symb == "<":
                    resultat_final = myst(r"""\py{variable} \leq \py{latex_limite}""", locals(), globals())
                else:
                    symb_latex_final = dico_symboles_latex[symb]
                    resultat_final = myst(r"""\py{variable} \py{symb_latex_final} \py{latex_limite}""", locals(), globals())

                raisonnement_latex += myst(r"""&\iff \py{resultat_final} \quad \quad \text{car } \py{variable} \text{ doit appartenir à } \mathbb{\py{domaine}} \\""", locals(), globals())
        # autres cas où domaine = "N" et valeurs_entieres_limites a un signe déterminé :
        else:
            latex_limite = latex_avec_formatage(valeurs_entieres_limites)
            if valeurs_entieres_limites.is_positive and symb in ["<=", "<"]: # cas n <= C (C positif)
                resultat_final = myst(r"""0 \leq \py{variable} \leq \py{latex_limite}""", locals(), globals())
                raisonnement_latex += myst(r"""&\iff \py{resultat_final} \quad \quad \text{car } \py{variable} \text{ doit appartenir à } \mathbb{N} \\""", locals(), globals())

            elif valeurs_entieres_limites == 0 and symb in ["<=", "<"]:
                raisonnement_latex += myst(r"""&\iff \py{variable} = 0 \quad \quad \text{car } \py{variable} \text{ doit appartenir à } \mathbb{N} \\""", locals(), globals())
            elif valeurs_entieres_limites.is_negative and symb in [">=", ">"]: # cas n >= -C (C positif)

                raisonnement_latex += myst(r"""&\iff \py{variable} \text{ est un entier naturel quelconque} \\""", locals(), globals())

            elif valeurs_entieres_limites.is_negative and symb in ["<=", "<"]: # cas n <= -C (C positif)
                raisonnement_latex += myst(r"""\quad \quad \text{ impossible car } \py{variable}\in\N \\""", locals(), globals())

            else:
                raisonnement_latex += myst(r"""& \text{(le résultat dépend du signe de } \py{latex_limite}) \\""", locals(), globals())



    if puissance == 2:
        quotient = sympify(valeur_droite / a)
        latex_quotient = latex_avec_formatage(quotient)

        racine = simplify(sqrt(quotient))
        latex_racine = latex_avec_formatage(racine)
        # Remplacer brutalement et impoliment ces maudits "-b+c" par "c-b" :
        latex_mb = latex_avec_formatage(-b)
        expr_a_remplacer = __simplifier_signes(myst(r"""\py{latex_mb} + \py{latex_c}""", locals(), globals()))
        expr_nouvelle = __simplifier_signes(myst(r"""\py{latex_c} - \py{latex_b}""", locals(), globals()))
        latex_racine = latex_racine.replace(expr_a_remplacer, expr_nouvelle)

        # Étape 3: Résoudre x² symb quotient

        phrase_cas_entier_a_ajouter = False

        bool_q_neg = quotient.is_nonpositive or (signe_a == "<" and (c-b).is_positive) or (signe_a == ">" and (c-b).is_negative) # quotient négatif
        bool_q_pos = quotient.is_nonnegative or (signe_a == ">" and (c-b).is_positive) or (signe_a == "<" and (c-b).is_negative)

        if quotient.is_zero:
            if symb == ">=":
                raisonnement_latex += myst(r"""&\iff \py{variable} \text{ quelconque} """, locals(), globals())
                raisonnement_latex += myst(r"""\text{ (car on a toujours } \py{variable}^2 \geq 0) \\""", locals(), globals())
            elif symb == ">":
                if domaine == "N":
                    raisonnement_latex += myst(r"""&\iff \py{variable} \in \mathbb{N} \setminus \{0\} \\""", locals(), globals())
                else:
                     raisonnement_latex += myst(r"""&\iff \py{variable} \neq 0 \\""", locals(), globals())

            elif symb == "<=":
                if domaine == "N":
                    raisonnement_latex += myst(r"""&\iff \py{variable} = 0 \\""", locals(), globals())
                else:
                    raisonnement_latex += myst(r"""&\iff \py{variable} = 0 \\""", locals(), globals())
            else:  # symb == "<"
                raisonnement_latex += myst(r"""& \text{ impossible} \\""", locals(), globals())
                # raisonnement_latex += myst(r"""\text{ (car } \py{variable}^2 \geq 0 {et non} < 0)""", locals(), globals())

        elif bool_q_neg:
            if symb in [">=", ">"]:
                raisonnement_latex += myst(r"""&\iff \py{variable} \text{ quelconque } """, locals(), globals())
                raisonnement_latex += myst(r"""\text{ (car on a toujours } \py{variable}^2 \geq 0) \\""", locals(), globals())
            else:
                raisonnement_latex += myst(r"""& \text{ impossible car }  \py{variable}^2 \geq 0 > \py{latex_quotient} \\""", locals(), globals())


        elif bool_q_pos:  # quotient > 0
            racine0 = sqrt(quotient, evaluate = False)
            latex_racine0 = latex_avec_formatage(racine0)
            racine1 = sqrt(quotient)
            latex_racine1 = latex_avec_formatage(racine1)
            valeurs_critiques = [-racine, racine]

            if symb in [">=", ">"]:
                pg, pp = (r"\geq", r"\leq") if symb == ">=" else (">", "<")

                # Si nécessaire, on détaille le calcul de sqrt(quotient) :
                if racine1 != racine0:
                    raisonnement_latex += myst(r"""&\iff \py{variable} \py{pp} -\py{latex_racine0} \text{ ou } \py{variable} \py{pg} \py{latex_racine0} \\""", locals(), globals())
                if racine != racine1:
                    raisonnement_latex += myst(r"""&\iff \py{variable} \py{pp} -\py{latex_racine1} \text{ ou } \py{variable} \py{pg} \py{latex_racine1} \\""", locals(), globals())

                raisonnement_latex += myst(r"""&\iff \py{variable} \py{pp} -\py{latex_racine} \text{ ou } \py{variable} \py{pg} \py{latex_racine} \\""", locals(), globals())



            else:  # symb in ["<=", "<"]
                pp = r"\leq" if symb == "<=" else "<"

                # si nécessaire, on détaille le calcul de sqrt(racine1)
                if racine1 != racine0:
                    raisonnement_latex += myst(r"""&\iff -\py{latex_racine0} \py{pp} \py{variable} \py{pp} \py{latex_racine0} \\""", locals(), globals())
                if racine != racine1:
                    raisonnement_latex += myst(r"""&\iff -\py{latex_racine1} \py{pp} \py{variable} \py{pp} \py{latex_racine1} \\""", locals(), globals())


                raisonnement_latex += myst(r"""&\iff -\py{latex_racine} \py{pp} \py{variable} \py{pp} \py{latex_racine} \\""", locals(), globals())

        else: # le signe de quotient est indéterminé
            if (c-b).is_positive or (c-b).is_negative:
                sens_pos, sens_neg = (r"\geq", "<") if (c-b).is_positive else (r"\leq", ">")
                cas_pos = myst(r""" \text{ si } \py{latex_a} \py{sens_pos} 0""", locals(), globals())
                cas_neg = myst(r""" \text{ si } \py{latex_a} \py{sens_neg} 0""", locals(), globals())
            elif a.is_positive or a.is_negative or signe_a:
                sens_pos, sens_neg = (r"\geq", "<") if (a.is_positive or signe_a == ">") else (r"\leq", ">")
                cas_pos = myst(r""" \text{ si } \py{latex_fraction_num} \py{sens_pos} 0""", locals(), globals())
                cas_neg = myst(r""" \text{ si } \py{latex_fraction_num} \py{sens_neg} 0""", locals(), globals())
            else:
                cas_pos = myst(r""" \text{ si } \py{latex_quotient} > 0""", locals(), globals())
                cas_neg = myst(r""" \text{ si } \py{latex_quotient} < 0""", locals(), globals())

            if symb in [">=", ">"]:
                pg, pp = (r"\geq", r"\leq") if symb == ">=" else (">", "<")
                raisonnement_latex += myst(r"""&\iff \begin{cases} \py{variable} \py{pp} -\py{latex_racine} \text{ ou } \py{variable} \py{pg} \py{latex_racine}, & \py{cas_pos} \\
\py{variable} \text{ quelconque}, & \py{cas_neg}
\end{cases} \\""", locals(), globals())
            else:  # symb in ["<=", "<"]
                pp = r"\leq" if symb == "<=" else "<"
                raisonnement_latex += myst(r"""&\iff \begin{cases} -\py{latex_racine} \py{pp} \py{variable} \py{pp} \py{latex_racine}, & \py{cas_pos} \\
\text{ impossible}, & \py{cas_neg}
\end{cases} \\""", locals(), globals())


        # Si des détails doivent être donnés dans le cas entier :
        # (quel que soit le sens de l'inégalité)
        if not bool_q_neg: # à moins qu'on ne soit sûr que q <= 0
            if domaine in ["Z", "N"] and (not racine.is_integer or symb in ["<", ">"]):
                phrase_cas_entier_a_ajouter = True
                # cas particulier où 0 est la seule solution
                if (symb == "<=" and (racine - 1).is_negative) or (symb == "<" and (racine - 1).is_nonpositive):
                    raisonnement_latex += myst(r"""&\iff \py{variable}  = 0""", locals(), globals())
                # tous les autres cas :
                else:
                    # calcul des valeurs extrêmes :
                    if symb == "<=":
                        limite_pos = floor(racine)
                        limite_neg = __ceil(-racine) if domaine == "Z" else 0
                    elif symb == ">=":
                        limite_pos = __ceil(racine)
                        limite_neg = floor(-racine)
                    elif symb == "<":
                        if racine.is_integer:
                            limite_pos = racine - 1
                            limite_neg = - racine + 1 if domaine == "Z" else 0
                        else:
                            limite_pos = floor(racine)
                            limite_neg = __ceil(-racine) if domaine == "Z" else 0
                    else: #symb = ">"
                        limite_pos = racine + 1 if racine.is_integer else __ceil(racine)
                        limite_neg = - racine - 1 if racine.is_integer else floor(- racine)

                    # affichage de la dernière étape :
                    latex_limite_pos = latex_avec_formatage(limite_pos)
                    latex_limite_neg = latex_avec_formatage(limite_neg)
                    if symb in ["<=", "<"]:
                        raisonnement_latex += myst(r"""&\iff \py{latex_limite_neg} \leq \py{variable} \leq \py{latex_limite_pos}""", locals(), globals())
                    else: # >= ou >
                        if domaine == "Z":
                            raisonnement_latex += myst(r"""&\iff \py{variable} \leq \py{latex_limite_neg}   \text{ ou } \py{variable} \geq \py{latex_limite_pos}""", locals(), globals())
                        else:
                            raisonnement_latex += myst(r"""&\iff \py{variable} \geq \py{latex_limite_pos}""", locals(), globals())
                naturel_ou_pas = "naturel" if domaine == "N" else " "
                raisonnement_latex += myst(r"""& \text{car } \py{variable} \text{ est entier \py{naturel_ou_pas}}\\""", locals(), globals())
# ==============================================================================================================


    # Terminer le raisonnement LaTeX
    raisonnement_latex = raisonnement_latex[:-2] # on enlève le saut de ligne final
    raisonnement_latex += myst(r"""\,.
\end{align*}\end{equation*}""", locals(), globals())

    raisonnement_latex = __simplifier_signes(raisonnement_latex)

    return ensemble_solution, raisonnement_latex

def pxsl_solve_general_inequality(a=1, b=0, c=0, variable="x", inequality=">=", domain="R", power=1, sign_a=None, detail_sign_a=False):
    r"""
    \en{Solves an inequality of the form \(a x^p + b \,\square\, c\) with detailed step-by-step reasoning in LaTeX.}
    \fr{Résout une inéquation de la forme \(a x^p + b \,\square\, c\) avec un raisonnement détaillé pas à pas en LaTeX.}

    \en{This function solves linear (\(p=1\)) or quadratic (\(p=2\)) inequalities and generates
    a complete LaTeX-formatted solution showing all intermediate steps. It handles
    symbolic coefficients, different domains (reals, integers, natural numbers), and
    cases where the sign of the coefficient \(a\) must be analyzed.}
    \fr{Cette fonction résout des inéquations linéaires (\(p=1\)) ou quadratiques (\(p=2\)) et génère
    une solution complète au format LaTeX en détaillant toutes les étapes. Elle gère
    des coefficients symboliques, différents domaines (réels, entiers, naturels) et
    les cas où le signe du coefficient \(a\) doit être analysé.}

    Parameters
    ----------
    a : int, float, or sympy expression, optional
        \en{Coefficient of the variable term. Default: 1.}
        \fr{Coefficient du terme en variable. Par défaut : 1.}
    b : int, float, or sympy expression, optional
        \en{Constant term on the left-hand side. Default: 0.}
        \fr{Terme constant au membre de gauche. Par défaut : 0.}
    c : int, float, or sympy expression, optional
        \en{Constant term on the right-hand side. Default: 0.}
        \fr{Terme constant au membre de droite. Par défaut : 0.}
    variable : str, optional
        \en{Name of the variable. Default: "x".}
        \fr{Nom de la variable. Par défaut : "x".}
    inequality : str, optional
        \en{Inequality symbol: ">=", ">", "<=", "<". Default: ">=".}
        \fr{Symbole d'inégalité : ">=", ">", "<=", "<". Par défaut : ">=".}
    domain : str, optional
        \en{Solution domain: "R" (reals), "Z" (integers), "N" (natural numbers). Default: "R".}
        \fr{Domaine des solutions : "R" (réels), "Z" (entiers), "N" (naturels). Par défaut : "R".}
    power : int, optional
        \en{Exponent of the variable: 1 (linear) or 2 (quadratic). Default: 1.}
        \fr{Exposant de la variable : 1 (linéaire) ou 2 (quadratique). Par défaut : 1.}
    sign_a : str or None, optional
        \en{Sign of the coefficient \(a\) when symbolic: ">" for positive, "<" for negative,
        or None to determine automatically.}
        \fr{Signe du coefficient \(a\) quand il est symbolique : ">" pour positif, "<" pour négatif,
        ou None pour déterminer automatiquement.}
    detail_sign_a : bool, optional
        \en{Whether to explicitly mention the sign of \(a\) when dividing. Default: False.}
        \fr{Indique s'il faut expliciter le signe de \(a\) lors d'une division. Par défaut : False.}

    Returns
    -------
    tuple
        \en{A tuple \((\text{solution\_set}, \text{latex\_reasoning})\) where:}
        \fr{Un tuple \((\text{solution\_set}, \text{latex\_reasoning})\) où :}
        - solution_set : sympy set or dict
          \en{The solution set. Returns a dict with cases if the sign of \(a\) or the RHS is undetermined.}
          \fr{L'ensemble des solutions. Retourne un dictionnaire par cas si le signe de \(a\) ou le membre droit est indéterminé.}
        - latex_reasoning : str
          \en{Complete LaTeX-formatted step-by-step solution.}
          \fr{Solution détaillée pas à pas au format LaTeX.}

    Raises
    ------
    ValueError
        \en{If `inequality` not in [">=", ">", "<=", "<"].}
        \fr{Si `inequality` n'est pas dans [">=", ">", "<=", "<"].}
        \en{If `domain` not in ["R", "Z", "N"].}
        \fr{Si `domain` n'est pas dans ["R", "Z", "N"].}
        \en{If `power` not in [1, 2].}
        \fr{Si `power` n'est pas dans [1, 2].}
        \en{If `sign_a` not in {None, ">", "<"}.}
        \fr{Si `sign_a` n'est pas dans {None, ">", "<"}.}

    Examples
    --------
    >>> # Simple linear inequality
    >>> sol, latex = solve_general_inequality(2, 3, 7, variable="x", inequality=">=")
    >>> print(sol)
    [2, oo)

    >>> # Quadratic inequality
    >>> sol, latex = solve_general_inequality(1, 0, 4, power=2, inequality="<=")
    >>> print(sol)
    [-2, 2]

    >>> # Integer domain
    >>> sol, latex = solve_general_inequality(3, -1, 5, domain="Z", inequality=">")
    >>> print(sol)
    {3, 4, 5, ...}

    >>> # Symbolic coefficient with sign analysis
    >>> from sympy import Symbol
    >>> a = Symbol('a')
    >>> sol, latex = solve_general_inequality(a, 0, 5, inequality=">=")
    >>> # Returns dict with cases for a>0 and a<0

    :pxs_trigger: idem resoudre_inequation_generale, version bilingue FR/EN avec balises \en{}\fr{} dans le corrigé, gère aussi le cas égalité ``inequality="="`` (équations), paramètres en anglais (variable, inequality, domain, power, sign_a) ; version à préférer dans tous les nouveaux exercices PyxiScience
    :pxs_returns: |
        tuple ``(solution_set, latex_reasoning)`` bilingue : ``solution_set`` de type sympy
        (Interval, EmptySet, Intersection, ou ``dict`` par cas), ``latex_reasoning`` MyST bilingue
        avec ``\en{}`` / ``\fr{}`` et ``\begin{align*}`` détaillant chaque étape.
    :pxs_example: |
        from sympy import Symbol
        a = Symbol('a')
        sol, corrige = pxsl_solve_general_inequality(a, 0, 5, inequality=">=")
        # → sol = {"a>0": ..., "a<0": ...}, corrige = raisonnement bilingue cassé par cas
    :pxs_antipattern: Utiliser ``resoudre_inequation_generale`` (FR-only) dans un exercice destiné à NYU Paris, ou dupliquer la logique pour l'équation ``=`` au lieu de passer ``inequality="="``.
    """

    # ======= AUXILIARY FUNCTIONS =================

    def __ceil(x):
        return (x if x.is_integer else floor(x) + 1)

    def __simplify_signs(s):
        return s.replace("+ + ", "+ ").replace("+ -", "-").replace("- + ", "- ").replace("- -", "+")

    def __is_a_fraction_like(a_):
        if isinstance(a_, Rational) and a_.q != 1:
            return True
        if isinstance(a_, Mul):
            for fac in a_.args:
                if isinstance(fac, Rational) or (isinstance(fac, Pow) and fac.args[1].is_integer and fac.args[1].is_negative):
                    return True
        return False

    def __solutions_general_inequality(a=1, b=0, c=0, inequality=">=", domain="R", power=1, sign_a=None, sign_rhs=None):
        a = sympify(a)
        b = sympify(b)
        c = sympify(c)
        set_map = {"R": Reals, "N": Naturals, "Z": Integers}
        the_set = set_map[domain]
        quotient = (c - b) / a

        if a == 0:
            value = b - c
            existence_cases = {"<=": value.is_nonpositive, "<": value.is_negative,
                               ">=": value.is_nonnegative, ">": value.is_positive,
                               "=": value.is_nonzero}
            ok = existence_cases[inequality]
            sol = the_set if ok else EmptySet

        elif a.is_negative or sign_a == "<":
            inv = {"<=": ">=", "<": ">", ">=": "<=", ">": "<", "=" : "="}[inequality]
            return __solutions_general_inequality(-a, -b, -c, inequality=inv, domain=domain, power=power, sign_a=">", sign_rhs=sign_rhs)

        elif a.is_nonnegative or sign_a == ">":

            if power == 1:
                if inequality == ">=":
                    sol = pxs_Interval(quotient, oo)
                elif inequality == ">":
                    sol = pxs_Interval.open(quotient, oo)
                elif inequality == "<=":
                    sol = pxs_Interval(-oo, quotient)
                elif inequality == "<":
                    sol = pxs_Interval.open(-oo, quotient)
                else:
                    sol = sympify({quotient})

            elif power == 2:
                if quotient.is_negative or sign_rhs == "<":
                    if inequality in [">=", ">"]:
                        sol = the_set
                    else:
                        sol = EmptySet
                elif quotient.is_nonnegative or sign_rhs == ">":
                    root = simplify(sqrt(quotient))
                    if inequality == ">=":
                        sol = pxs_Interval(-oo, -root).union(pxs_Interval(root, oo))
                    elif inequality == ">":
                        sol = pxs_Interval.open(-oo, -root).union(pxs_Interval.open(root, oo))
                    elif inequality == "<=":
                        sol = pxs_Interval(-root, root)
                    elif inequality == "<":
                        sol = pxs_Interval.open(-root, root)
                    else:
                        sol = sympify({-root, root})
                else:  # sign of RHS undetermined
                    sol_rhs_pos = __solutions_general_inequality(a, b, c, inequality=inequality, domain=domain, power=power, sign_a=sign_a, sign_rhs=">")
                    sol_rhs_neg = __solutions_general_inequality(a, b, c, inequality=inequality, domain=domain, power=power, sign_a=sign_a, sign_rhs="<")
                    return {"rhs>0": sol_rhs_pos, "rhs<0": sol_rhs_neg}

        else:  # sign of a undetermined
            sol_pos = __solutions_general_inequality(a, b, c, inequality=inequality, domain=domain, power=power, sign_a=">", sign_rhs=sign_rhs)
            sol_neg = __solutions_general_inequality(a, b, c, inequality=inequality, domain=domain, power=power, sign_a="<", sign_rhs=sign_rhs)
            return {"a>0": sol_pos, "a<0": sol_neg}

        if domain in ["Z", "N"]:
            try:
                sol = sol.intersect(Integers) if domain == "Z" else sol.intersect(Naturals0)
            except:
                sol = Intersection(sol, Integers, evaluate=False) if domain == "Z" else Intersection(sol, Naturals0, evaluate=False)

        return sol

    # ===================================================================

    if inequality not in [">=", ">", "<=", "<", "="]:
        raise ValueError("Invalid inequality symbol")
    if domain not in ["R", "Z", "N"]:
        raise ValueError("Invalid domain")
    if power not in [1, 2]:
        raise ValueError("Invalid power (must be 1 or 2)")
    if sign_a not in [None, ">", "<"]:
        raise ValueError("Invalid sign_a. Use None, '>' for positive, or '<' for negative.")

    # Convert parameters
    a = pxsl_to_rational_or_symbol(a)
    b = pxsl_to_rational_or_symbol(b)
    c = pxsl_to_rational_or_symbol(c)

    # Variable symbol
    var_symb = Symbol(variable)

    solution_set = __solutions_general_inequality(a, b, c, inequality, domain, power, sign_a)

    # If the sign of a is not determined, split into cases
    if inequality != "=" and not (sign_a in [">", "<"] or sympify(a).is_nonpositive or sympify(a).is_nonnegative):
        latex_a = pxsl_latex_with_formatting(a)

        latex_reasoning = myst(r"""\en{We distinguish two cases:}\fr{On distingue deux cas :}
1. \en{If}\fr{Si} \py{latex_a} > 0:
""", locals(), globals())
        latex_reasoning += pxsl_solve_general_inequality(a, b, c, variable=variable, inequality=inequality, domain=domain, power=power, sign_a=">")[-1]
        latex_reasoning += myst(r"""
2. \en{If}\fr{Si} \py{latex_a} < 0:
""", locals(), globals())
        latex_reasoning += pxsl_solve_general_inequality(a, b, c, variable=variable, inequality=inequality, domain=domain, power=power, sign_a="<")[-1]

        latex_reasoning = __simplify_signs(latex_reasoning)
        return solution_set, latex_reasoning  # the solution set is case-dependent

    latex_reasoning = myst(r"""\begin{equation*}\begin{align*}""", locals(), globals())

    # Initial inequality symbol (and LaTeX display)
    symb = inequality
    symb_latex_map = {">=": myst(r"""\geq""", locals(), globals()), ">": myst(r""">""", locals(), globals()),
                      "<=": myst(r"""\leq""", locals(), globals()), "<": myst(r"""<""", locals(), globals()),
                      "=" : myst(r"""=""", locals(), globals())}
    latex_ineq_symbol = symb_latex_map[inequality]

    # Build the original inequality
    coeff_str = pxsl_latex_coefficient(a)
    coeff_str = myst(r"""\left(\py{coeff_str}\right)""", locals(), globals()) if a.is_Add else coeff_str
    latex_c = pxsl_latex_with_formatting(c)

    # Left-hand expression
    if sympify(b).is_zero:
        expression = sympy_latex(a * var_symb ** power)
        lhs_expr = myst(r"""\py{expression}""", locals(), globals())
    elif isinstance(b, (int, Rational)) and b >= 0:
        latex_b = pxsl_latex_with_formatting(b)
        if power == 1:
            lhs_expr = myst(r"""\py{coeff_str}\py{variable} + \py{latex_b}""", locals(), globals()) if coeff_str else myst(r"""\py{variable} + \py{latex_b}""", locals(), globals())
        else:
            lhs_expr = myst(r"""\py{coeff_str}\py{variable}^2 + \py{latex_b}""", locals(), globals()) if coeff_str else myst(r"""\py{variable}^2 + \py{latex_b}""", locals(), globals())
    elif isinstance(b, (int, Rational)) and b < 0:
        latex_abs_b = pxsl_latex_with_formatting(abs(b))
        if power == 1:
            lhs_expr = myst(r"""\py{coeff_str}\py{variable} - \py{latex_abs_b}""", locals(), globals()) if coeff_str else myst(r"""\py{variable} - \py{latex_abs_b}""", locals(), globals())
        else:
            lhs_expr = myst(r"""\py{coeff_str}\py{variable}^2 - \py{latex_abs_b}""", locals(), globals()) if coeff_str else myst(r"""\py{variable}^2 - \py{latex_abs_b}""", locals(), globals())
    else:
        latex_b = pxsl_latex_with_formatting(b)
        if power == 1:
            lhs_expr = myst(r"""\py{coeff_str}\py{variable} + \py{latex_b}""", locals(), globals()) if coeff_str else myst(r"""\py{variable} + \py{latex_b}""", locals(), globals())
        else:
            lhs_expr = myst(r"""\py{coeff_str}\py{variable}^2 + \py{latex_b}""", locals(), globals()) if coeff_str else myst(r"""\py{variable}^2 + \py{latex_b}""", locals(), globals())

    # Degenerate case: a = 0
    if a == 0:
        latex_b_simple = pxsl_latex_with_formatting(b)
        latex_reasoning += myst(r"""\py{latex_b_simple} \py{latex_ineq_symbol} \py{latex_c}""", locals(), globals())

        if solution_set == EmptySet:
            latex_reasoning += myst(r"""\text{ impossible.}""", locals(), globals())
        else:
            latex_reasoning += myst(r"""&\text{ \en{always true}\fr{toujours vrai}.}""", locals(), globals())

        latex_reasoning += myst(r"""\\ \end{align*}\end{equation*}""", locals(), globals())
        latex_reasoning = __simplify_signs(latex_reasoning)
        return solution_set, latex_reasoning

    # First line: original inequality
    latex_reasoning += myst(r"""
\py{lhs_expr} \py{latex_ineq_symbol} \py{latex_c}""", locals(), globals())

    rhs_value = c - b

    # Step 1: isolate the x-term — construct c - b with sign handling
    if not sympify(b).is_zero:
        latex_b = pxsl_latex_with_formatting(b)
        latex_c = pxsl_latex_with_formatting(c)
        if c == 0:
            latex_rhs_step1 = pxsl_latex_with_formatting(-b)
        elif b.is_Add:
            latex_rhs_step1 = latex_c + " - " + myst(r"""\left(\py{latex_b}\right)""", locals(), globals())
        else:
            latex_rhs_step1 = __simplify_signs(latex_c + " - " + latex_b)

        if power == 1:
            var_term = myst(r"""\py{coeff_str}\py{variable}""", locals(), globals()) if coeff_str else variable
        else:
            var_term = myst(r"""\py{coeff_str}\py{variable}^2""", locals(), globals()) if coeff_str else myst(r"""\py{variable}^2""", locals(), globals())

        latex_reasoning += myst(r""" &\iff \py{var_term} \py{latex_ineq_symbol}
\py{latex_rhs_step1} \\""", locals(), globals())

        # Simplify c-b
        latex_mb = pxsl_latex_with_formatting(-b)
        expr_equiv = __simplify_signs(myst(r"""\py{latex_mb} + \py{latex_c}""", locals(), globals()))
        if latex_rhs_step1 != pxsl_latex_with_formatting(c - b) and pxsl_latex_with_formatting(c - b) != expr_equiv:
            latex_rhs_step1 = pxsl_latex_with_formatting(c - b)
            latex_reasoning += myst(r""" &\iff \py{var_term} \py{latex_ineq_symbol}
\py{latex_rhs_step1}\\""", locals(), globals())
    else:
        latex_rhs_step1 = pxsl_latex_with_formatting(c)

    # Fraction handling and sign of a
    latex_fraction_num = latex_rhs_step1
    latex_a = pxsl_latex_with_formatting(a)

    # From here we divide by a: inequality direction may change
    if sympify(a).is_negative or sign_a == "<":
        symb = {"<=": ">=", "<": ">", ">=": "<=", ">": "<", "=" : "="}[inequality]
        latex_ineq_symbol = symb_latex_map[symb]

    # Step 2: solution depending on the sign of a (with option sign_a)

    # Left side becomes variable or variable^2:
    var_term_simple = myst(r"""\py{variable}""", locals(), globals()) if power == 1 else myst(r"""\py{variable}^2""", locals(), globals())

    if inequality != "=" and sign_a is None:
        sign_a = ">" if sympify(a).is_positive else "<"

    if inequality != "=" and (detail_sign_a or a.free_symbols):
        because_a = myst(r""", \quad \text{since } \py{latex_a} \py{sign_a} 0""", locals(), globals())
    else:
        because_a = " "

    if a == 1:
        pass
    elif a == -1:
        inv = {">=": myst(r"""\leq""", locals(), globals()), ">": myst(r"""<""", locals(), globals()),
               "<=": myst(r"""\geq""", locals(), globals()), "<": myst(r""">""", locals(), globals()),
               "=" : myst(r"""=""", locals(), globals())}[inequality]
        latex_rhs_only = pxsl_latex_with_formatting(b - c)
        latex_reasoning += myst(r"""&\iff \py{var_term_simple} \py{latex_ineq_symbol} \py{latex_rhs_only}\\""", locals(), globals())
    elif c - b == 0:
        latex_reasoning += myst(r"""&\iff \py{var_term_simple} \py{latex_ineq_symbol} 0 \py{because_a}\\""", locals(), globals())

    elif __is_a_fraction_like(a):  # multiplying by 1/a may be clearer than dividing by a
        fraction = Mul(c - b, 1 / a, evaluate=False)
        latex_fraction = pxsl_latex_with_formatting(fraction)
        latex_reasoning += myst(r"""&\iff \py{var_term_simple} \py{latex_ineq_symbol} \py{latex_fraction} \py{because_a}\\""", locals(), globals())
        fraction1 = Mul(c - b, 1 / a)
        if fraction1 != fraction:
            latex_fraction = pxsl_latex_with_formatting(fraction1)
            latex_reasoning += myst(r"""&\iff \py{var_term_simple} \py{latex_ineq_symbol} \py{latex_fraction} \\""", locals(), globals())
    else:
        latex_fraction = myst(r"""\frac{\py{latex_fraction_num}}{\py{latex_a}}""", locals(), globals())
        if gcd(c - b, a) != 1 or a.is_noninteger:
            latex_reasoning += myst(r"""&\iff \py{var_term_simple} \py{latex_ineq_symbol} \py{latex_fraction} \py{because_a}\\""", locals(), globals())
            latex_fraction = pxsl_latex_with_formatting((c - b) / a)
            latex_reasoning += myst(r"""&\iff \py{var_term_simple} \py{latex_ineq_symbol} \py{latex_fraction} \\""", locals(), globals())
        else:
            latex_reasoning += myst(r"""&\iff \py{var_term_simple} \py{latex_ineq_symbol} \py{latex_fraction} \py{because_a} \\""", locals(), globals())

    # Integer/Natural domain when power = 1
    critical_value = (c - b) / a
    if power == 1 and domain in ["Z", "N"]:
        if inequality == "=": # equation case
            if critical_value.is_noninteger or (domain == "N" and critical_value.is_negative): # on sait que la solution n'est pas dans le domaine
                latex_reasoning = latex_reasoning[:-2] # on enlève le saut de ligne final
                latex_reasoning += myst(r"""
            \end{align*}\end{equation*}""", locals(), globals())
                latex_reasoning += myst(r"""
Or $\py{variable}$ doit appartenir à l'ensemble $\mathbb{\py{domain}}\,$, donc l'équation ne possède aucune solution.""", locals(), globals())
                latex_reasoning = __simplify_signs(latex_reasoning)
                return solution_set, latex_reasoning

            elif (not critical_value.is_integer) or (domain == "N" and not critical_value.is_nonnegative):# solution might not be in domain
                positive_or_not = " positif" if domain == "N" else ""
                latex_reasoning = latex_reasoning[:-2]
                latex_reasoning += myst(r"""
            \end{align*}\end{equation*}""", locals(), globals())
                latex_reasoning += myst(r"""
Ainsi l'équation admet pour unique solution $\ds \py{latex_fraction}$ si $\ds \py{latex_fraction}$ est un entier\py{positive_or_not}, et n'admet aucune solution sinon.""", locals(), globals())
                latex_reasoning = __simplify_signs(latex_reasoning)
                return solution_set, latex_reasoning

        else: # inequation case
            if symb in [">=", ">"]:
                if symb == ">":
                    int_bounds = critical_value + 1 if critical_value.is_integer else __ceil(critical_value)
                else:
                    int_bounds = critical_value if critical_value.is_integer else __ceil(critical_value)
            else:
                if symb == "<":
                    int_bounds = critical_value - 1 if critical_value.is_integer else floor(critical_value)
                else:
                    int_bounds = floor(critical_value)

            if domain == "Z" or (symb in [">=", ">"] and (not int_bounds.is_negative)):
                if critical_value.is_noninteger or symb in ['<', '>'] or not (critical_value.is_nonpositive or critical_value.is_nonnegative):
                    latex_bound = pxsl_latex_with_formatting(int_bounds)
                    if symb == ">":
                        final_result = myst(r"""\py{variable} \geq \py{latex_bound}""", locals(), globals())
                    elif symb == "<":
                        final_result = myst(r"""\py{variable} \leq \py{latex_bound}""", locals(), globals())
                    else:
                        latex_final_symbol = symb_latex_map[symb]
                        final_result = myst(r"""\py{variable} \py{latex_final_symbol} \py{latex_bound}""", locals(), globals())

                    latex_reasoning += myst(r"""&\iff \py{final_result} \quad \quad \text{\en{since}\fr{car} } \py{variable} \text{ \en{must lie in}\fr{doit appartenir à} } \mathbb{\py{domain}} \\""", locals(), globals())
            else:
                latex_bound = pxsl_latex_with_formatting(int_bounds)
                if int_bounds.is_positive and symb in ["<=", "<"]:
                    final_result = myst(r"""0 \leq \py{variable} \leq \py{latex_bound}""", locals(), globals())
                    latex_reasoning += myst(r"""&\iff \py{final_result} \quad \quad \text{\en{since}\fr{car} } \py{variable} \text{ \en{must lie in}\fr{doit appartenir à} } \mathbb{N} \\""", locals(), globals())
                elif int_bounds == 0 and symb in ["<=", "<"]:
                    latex_reasoning += myst(r"""&\iff \py{variable} = 0 \quad \quad \text{\en{since}\fr{car} } \py{variable} \text{ \en{must lie in}\fr{doit appartenir à} } \mathbb{N} \\""", locals(), globals())
                elif int_bounds.is_negative and symb in [">=", ">"]:
                    latex_reasoning += myst(r"""&\iff \py{variable} \text{ \en{is any natural integer}\fr{est un entier naturel quelconque}} \\""", locals(), globals())
                elif int_bounds.is_negative and symb in ["<=", "<"]:
                    latex_reasoning += myst(r"""\quad \quad \text{ impossible \en{since}\fr{car} } \py{variable}\in\mathbb{N} \\""", locals(), globals())
                else:
                    latex_reasoning += myst(r"""& \text{(\en{the result depends on the sign of}\fr{le résultat dépend du signe de} } \py{latex_bound}) \\""", locals(), globals())

    # Quadratic case
    if power == 2:
        quotient = sympify(rhs_value / a)
        latex_quotient = pxsl_latex_with_formatting(quotient)

        root = simplify(sqrt(quotient))
        latex_root = pxsl_latex_with_formatting(root)

        # Replace "-b + c" by "c - b" inside latex_root when needed:
        latex_mb = pxsl_latex_with_formatting(-b)
        expr_to_replace = __simplify_signs(myst(r"""\py{latex_mb} + \py{latex_c}""", locals(), globals()))
        new_expr = __simplify_signs(myst(r"""\py{latex_c} - \py{latex_b}""", locals(), globals()))
        latex_root = latex_root.replace(expr_to_replace, new_expr)

        # Step 3: solve x^2 (symb) quotient
        phrase_integer_case = False

        q_neg = quotient.is_nonpositive or (sign_a == "<" and (c - b).is_positive) or (sign_a == ">" and (c - b).is_negative)
        q_pos = quotient.is_nonnegative or (sign_a == ">" and (c - b).is_positive) or (sign_a == "<" and (c - b).is_negative)

        if quotient.is_zero:
            if symb == ">=":
                latex_reasoning += myst(r"""&\iff \py{variable} \text{ \en{arbitraryø\fr{arbitraire}} """, locals(), globals())
                latex_reasoning += myst(r"""\text{ (\en{since we always have}\fr{car on a toujours} } \py{variable}^2 \ge 0) \\""", locals(), globals())
            elif symb == ">":
                if domain == "N":
                    latex_reasoning += myst(r"""&\iff \py{variable} \in \mathbb{N} \setminus \{0\} \\""", locals(), globals())
                else:
                    latex_reasoning += myst(r"""&\iff \py{variable} \neq 0 \\""", locals(), globals())
            elif symb in ["<=", "="]:
                latex_reasoning += myst(r"""&\iff \py{variable} = 0 \\""", locals(), globals())
            else:  # symb == "<"
                latex_reasoning += myst(r"""& \text{ impossible} \\""", locals(), globals())

        elif q_neg:
            if symb in [">=", ">"]:
                latex_reasoning += myst(r"""&\iff \py{variable} \text{ \en{arbitrary}\fr{arbitraire} } """, locals(), globals())
                latex_reasoning += myst(r"""\text{ (\en{since we always have}\fr{car on a toujours} } \py{variable}^2 \ge 0) \\""", locals(), globals())
            else:
                latex_reasoning += myst(r"""& \text{ impossible \en{since}\fr{car} } \py{variable}^2 \ge 0 > \py{latex_quotient} \\""", locals(), globals())

        elif q_pos:
            root0 = sqrt(quotient, evaluate=False)
            latex_root0 = pxsl_latex_with_formatting(root0)
            root1 = sqrt(quotient)
            latex_root1 = pxsl_latex_with_formatting(root1)

            if symb in [">=", ">", "="]:
                if symb == ">=":
                    ge, le = r"\geq", r"\leq"
                elif symb == ">":
                    ge, le = ">", "<"
                else: # symb = "="
                    ge, le = "=", "="

                if root1 != root0:
                    latex_reasoning += myst(r"""&\iff \py{variable} \py{le} -\py{latex_root0} \text{ or } \py{variable} \py{ge} \py{latex_root0} \\""", locals(), globals())
                if root != root1:
                    latex_reasoning += myst(r"""&\iff \py{variable} \py{le} -\py{latex_root1} \text{ or } \py{variable} \py{ge} \py{latex_root1} \\""", locals(), globals())
                latex_reasoning += myst(r"""&\iff \py{variable} \py{le} -\py{latex_root} \text{ or } \py{variable} \py{ge} \py{latex_root} \\""", locals(), globals())

            else:  # symb in ["<=", "<"]
                le = r"\leq" if symb == "<=" else "<"
                if root1 != root0:
                    latex_reasoning += myst(r"""&\iff -\py{latex_root0} \py{le} \py{variable} \py{le} \py{latex_root0} \\""", locals(), globals())
                if root != root1:
                    latex_reasoning += myst(r"""&\iff -\py{latex_root1} \py{le} \py{variable} \py{le} \py{latex_root1} \\""", locals(), globals())
                latex_reasoning += myst(r"""&\iff -\py{latex_root} \py{le} \py{variable} \py{le} \py{latex_root} \\""", locals(), globals())

        else:  # sign of quotient undetermined
            if (c - b).is_positive or (c - b).is_negative:
                ge0, lt0 = (r"\geq", "<") if (c - b).is_positive else (r"\leq", ">")
                case_pos = myst(r""" \text{ \en{if}\fr{si} } \py{latex_a} \py{ge0} 0""", locals(), globals())
                case_neg = myst(r""" \text{ \en{if}\fr{si} } \py{latex_a} \py{lt0} 0""", locals(), globals())
            elif a.is_positive or a.is_negative or sign_a:
                ge0, lt0 = (r"\geq", "<") if (a.is_positive or sign_a == ">") else (r"\leq", ">")
                case_pos = myst(r""" \text{ \en{if}\fr{si} } \py{latex_fraction_num} \py{ge0} 0""", locals(), globals())
                case_neg = myst(r""" \text{ \en{if}\fr{si} } \py{latex_fraction_num} \py{lt0} 0""", locals(), globals())
            else:
                case_pos = myst(r""" \text{ \en{if}\fr{si} } \py{latex_quotient} > 0""", locals(), globals())
                case_neg = myst(r""" \text{ \en{if}\fr{si} } \py{latex_quotient} < 0""", locals(), globals())

            if symb == "=":
                latex_reasoning += myst(r"""&\iff \begin{cases} \py{variable} = -\py{latex_root} \text{ \en{or}\fr{ou} } \py{variable} = \py{latex_root}, & \py{case_pos} \\
\text{ impossible}, & \py{case_neg}
\end{cases} \\""", locals(), globals())

            elif symb in [">=", ">"]:
                if symb == ">=":
                    ge, le = r"\geq", r"\leq"
                elif symb == ">":
                    ge, le = ">", "<"
                latex_reasoning += myst(r"""&\iff \begin{cases} \py{variable} \py{le} -\py{latex_root} \text{ \en{or}\fr{ou} } \py{variable} \py{ge} \py{latex_root}, & \py{case_pos} \\
\py{variable} \text{ \en{arbitrary}\fr{arbitraire}}, & \py{case_neg}
\end{cases} \\""", locals(), globals())

            else:  # "<=", "<"
                le = r"\leq" if symb == "<=" else "<"
                latex_reasoning += myst(r"""&\iff \begin{cases} -\py{latex_root} \py{le} \py{variable} \py{le} \py{latex_root}, & \py{case_pos} \\
\text{ impossible}, & \py{case_neg}
\end{cases} \\""", locals(), globals())

        # Integer-domain details (any inequality direction)
        if not q_neg:
            if domain in ["Z", "N"] and (not root.is_integer or symb in ["<", ">"] or domain == "N"):
                phrase_integer_case = True
                if (symb == "<=" and (root - 1).is_negative) or (symb == "<" and (root - 1).is_nonpositive):
                    latex_reasoning += myst(r"""&\iff \py{variable}  = 0""", locals(), globals())

                elif symb == "=":
                    if root.is_noninteger or (not root.free_symbols and not root.is_integer): # root is not an integer
                        final_sentence = myst(r"""
Or $\py{variable}$ doit être un entier, donc l'équation n'admet aucune solution.""", locals(), globals())
                    elif not root.is_integer: # don't know whether root is integer or not
                        if domain == "N":
                            final_sentence = myst(r"""
Or $\py{variable}$ doit être un entier positif, donc l'équation admet pour unique solution $\py{latex_root}$ si $\py{latex_root}$ est un entier, et n'admet aucune solution sinon.""", locals(), globals())
                        if domain == "Z":
                            final_sentence = myst(r"""
Or \py{variable} doit être un entier, donc l'équation admet deux solutions -\py{latex_root} et \py{latex_root} si \py{latex_root} est un entier, et n'admet aucune solution sinon.""", locals(), globals())
                    elif domain == "N": # on sait que racine est entier et domaine = N
                        latex_reasoning += myst(r"""&\iff \py{variable}  = \py{latex_root} \\""", locals(), globals())
                        final_sentence = myst(r"""
En effet, $\py{variable}$ doit être un entier positif.""", locals(), globals())

                    latex_reasoning = latex_reasoning[:-2] # on enlève le saut de ligne final
                    latex_reasoning += myst(r"""\,.
                    \end{align*}\end{equation*}""", locals(), globals())
                    latex_reasoning += final_sentence

                    latex_reasoning = __simplify_signs(latex_reasoning)

                    return solution_set, latex_reasoning

                else:
                    if symb == "<=":
                        lim_pos = floor(root)
                        lim_neg = __ceil(-root) if domain == "Z" else 0
                    elif symb == ">=":
                        lim_pos = __ceil(root)
                        lim_neg = floor(-root)
                    elif symb == "<":
                        if root.is_integer:
                            lim_pos = root - 1
                            lim_neg = -root + 1 if domain == "Z" else 0
                        else:
                            lim_pos = floor(root)
                            lim_neg = __ceil(-root) if domain == "Z" else 0
                    else:  # ">"
                        lim_pos = root + 1 if root.is_integer else __ceil(root)
                        lim_neg = -root - 1 if root.is_integer else floor(-root)

                    latex_lim_pos = pxsl_latex_with_formatting(lim_pos)
                    latex_lim_neg = pxsl_latex_with_formatting(lim_neg)
                    if symb in ["<=", "<"]:
                        latex_reasoning += myst(r"""&\iff \py{latex_lim_neg} \leq \py{variable} \leq \py{latex_lim_pos}""", locals(), globals())
                    else:
                        if domain == "Z":
                            latex_reasoning += myst(r"""&\iff \py{variable} \leq \py{latex_lim_neg}   \text{ \en{or}\fr{ou} } \py{variable} \geq \py{latex_lim_pos}""", locals(), globals())
                        else:
                            latex_reasoning += myst(r"""&\iff \py{variable} \geq \py{latex_lim_pos}""", locals(), globals())
                nat_flag = myst(r"""\en{natural}\fr{naturel}""", locals(), globals()) if domain == "N" else " "
                latex_reasoning += myst(r"""& \text{\fr{since}\en{car} } \py{variable} \text{ \en{is an integer}\fr{est un entier} \py{nat_flag}}\\""", locals(), globals())

    # Finish LaTeX reasoning
    latex_reasoning = latex_reasoning[:-2]  # remove last line break
    latex_reasoning += myst(r"""\,.
\end{align*}\end{equation*}""", locals(), globals())

    latex_reasoning = __simplify_signs(latex_reasoning)

    return solution_set, latex_reasoning



## ==================== Tests resoudre_inequation_generale() =================

def run_tests_resoudre_inequation_generale():
    """
    Lance la batterie de 35 tests de régression de ``resoudre_inequation_generale``.

    Affiche pour chaque cas le raisonnement LaTeX et l'ensemble solution, à des fins
    de debug uniquement. Ne retourne rien et n'a pas vocation à être appelée depuis
    un exercice PyxiScience.

    :pxs_trigger: lancer manuellement la batterie de tests de régression (35 cas : linéaire/quadratique, R/Z/N, coefficients numériques/symboliques, dégénéré, totalement indéterminé) après une modification de ``resoudre_inequation_generale``, debug d'un corrigé cassé, vérification avant commit — PAS un helper d'affichage
    :pxs_returns: |
        ``None``. Effet de bord : ``print()`` de chaque cas avec son raisonnement LaTeX
        et son ensemble solution séparés par des barres de 80 ``=``.
    :pxs_example: |
        from src.scripts.Mes_fctions.Mes_fctions_generalistes_bis import run_tests_resoudre_inequation_generale
        run_tests_resoudre_inequation_generale()
    :pxs_antipattern: Appeler cette fonction dans un bloc ``myst(...)`` d'exercice — c'est un outil de debug, pas un helper d'affichage. Utiliser ``resoudre_inequation_generale`` directement dans un exercice.
    """
    from sympy import Symbol, sqrt, Rational, oo, latex

    # Définition des variables symboliques
    x = Symbol('x')
    a_sym = Symbol('a', positive=True)
    b_sym = Symbol('b', real=True)
    k = Symbol('k', real=True)

    print("="*80)
    print("TESTS DE LA FONCTION resoudre_inequation_generale")
    print("="*80 + "\n")

    # ============================================================================
    # TESTS LINÉAIRES (puissance=1) - CAS NUMÉRIQUES
    # ============================================================================

    print("Test 1a: 2x + 3 ≥ 10 (linéaire, a>0, >=, domaine R)")
    result = resoudre_inequation_generale(2, 3, 10, variable="x", inegalite=">=", domaine="R", puissance=1)
    print("RAISONNEMENT DÉTAILLÉ:")
    print(result[1])
    print(f"\nSolutions : ${latex(result[0])}$")
    print("\n" + "="*80 + "\n")

    print("Test 1b: 2x + 3 ≤ 10 (linéaire, a>0, <=, domaine R)")
    result = resoudre_inequation_generale(2, 3, 10, variable="x", inegalite="<=", domaine="R", puissance=1)
    print("RAISONNEMENT DÉTAILLÉ:")
    print(result[1])
    print(f"\nSolutions : ${latex(result[0])}$")
    print("\n" + "="*80 + "\n")

    print("Test 1c: 2x + 3 > 10 (linéaire, a>0, >, domaine R)")
    result = resoudre_inequation_generale(2, 3, 10, variable="x", inegalite=">", domaine="R", puissance=1)
    print("RAISONNEMENT DÉTAILLÉ:")
    print(result[1])
    print(f"\nSolutions : ${latex(result[0])}$")
    print("\n" + "="*80 + "\n")

    print("Test 1d: 2x + 3 < 10 (linéaire, a>0, <, domaine R)")
    result = resoudre_inequation_generale(2, 3, 10, variable="x", inegalite="<", domaine="R", puissance=1)
    print("RAISONNEMENT DÉTAILLÉ:")
    print(result[1])
    print(f"\nSolutions : ${latex(result[0])}$")
    print("\n" + "="*80 + "\n")

    print("Test 2a: -3x + 5 ≥ 2 (linéaire, a<0, >=, domaine R)")
    result = resoudre_inequation_generale(-3, 5, 2, variable="x", inegalite=">=", domaine="R", puissance=1)
    print("RAISONNEMENT DÉTAILLÉ:")
    print(result[1])
    print(f"\nSolutions : ${latex(result[0])}$")
    print("\n" + "="*80 + "\n")

    print("Test 2b: -3x + 5 ≤ 2 (linéaire, a<0, <=, domaine R)")
    result = resoudre_inequation_generale(-3, 5, 2, variable="x", inegalite="<=", domaine="R", puissance=1)
    print("RAISONNEMENT DÉTAILLÉ:")
    print(result[1])
    print(f"\nSolutions : ${latex(result[0])}$")
    print("\n" + "="*80 + "\n")

    print("Test 3a: 4x - 7 ≥ 5 (linéaire, b<0, domaine Z)")
    result = resoudre_inequation_generale(4, -7, 5, variable="x", inegalite=">=", domaine="Z", puissance=1)
    print("RAISONNEMENT DÉTAILLÉ:")
    print(result[1])
    print(f"\nSolutions : ${latex(result[0])}$")
    print("\n" + "="*80 + "\n")

    print("Test 3b: 4x - 7 ≥ 5 (linéaire, b<0, domaine N)")
    result = resoudre_inequation_generale(4, -7, 5, variable="x", inegalite=">=", domaine="N", puissance=1)
    print("RAISONNEMENT DÉTAILLÉ:")
    print(result[1])
    print(f"\nSolutions : ${latex(result[0])}$")
    print("\n" + "="*80 + "\n")

    print("Test 4: 5x + 12 < -3 (linéaire, c<0, domaine Z)")
    result = resoudre_inequation_generale(5, 12, -3, variable="x", inegalite="<", domaine="Z", puissance=1)
    print("RAISONNEMENT DÉTAILLÉ:")
    print(result[1])
    print(f"\nSolutions : ${latex(result[0])}$")
    print("\n" + "="*80 + "\n")

    print("Test 5: -2x - 8 > -4 (linéaire, a<0, b<0, c<0, domaine R)")
    result = resoudre_inequation_generale(-2, -8, -4, variable="x", inegalite=">", domaine="R", puissance=1)
    print("RAISONNEMENT DÉTAILLÉ:")
    print(result[1])
    print(f"\nSolutions : ${latex(result[0])}$")
    print("\n" + "="*80 + "\n")

    # ============================================================================
    # TESTS LINÉAIRES - CAS AVEC FRACTIONS
    # ============================================================================

    print("Test 6: (1/2)x + 3 ≥ 7 (linéaire, coefficients rationnels)")
    result = resoudre_inequation_generale(Rational(1, 2), 3, 7, variable="x", inegalite=">=", domaine="R", puissance=1)
    print("RAISONNEMENT DÉTAILLÉ:")
    print(result[1])
    print(f"\nSolutions : ${latex(result[0])}$")
    print("\n" + "="*80 + "\n")

    print("Test 7: (-3/4)x + 2 < 5 (linéaire, a rationnel négatif)")
    result = resoudre_inequation_generale(Rational(-3, 4), 2, 5, variable="x", inegalite="<", domaine="R", puissance=1)
    print("RAISONNEMENT DÉTAILLÉ:")
    print(result[1])
    print(f"\nSolutions : ${latex(result[0])}$")
    print("\n" + "="*80 + "\n")

    print("Test 7b: autre cas a fractionnaire : (1/sqrt(2))x + 2 < 5 (linéaire, a rationnel négatif)")
    result = resoudre_inequation_generale(1 / sqrt(2), 2, 5, variable="x", inegalite="<", domaine="R", puissance=1)
    print("RAISONNEMENT DÉTAILLÉ:")
    print(result[1])
    print(f"\nSolutions : ${latex(result[0])}$")
    print("\n" + "="*80 + "\n")

    # ============================================================================
    # TESTS LINÉAIRES - CAS AVEC RACINES ET EXPRESSIONS
    # ============================================================================

    print("Test 8: x + √2 ≥ 5 (linéaire, b irrationnel)")
    result = resoudre_inequation_generale(1, sqrt(2), 5, variable="x", inegalite=">=", domaine="R", puissance=1)
    print("RAISONNEMENT DÉTAILLÉ:")
    print(result[1])
    print(f"\nSolutions : ${latex(result[0])}$")
    print("\n" + "="*80 + "\n")

    print("Test 9: 2x + (1 - √3) ≤ 4 (linéaire, b expression avec racine)")
    result = resoudre_inequation_generale(2, 1 - sqrt(3), 4, variable="x", inegalite="<=", domaine="R", puissance=1)
    print("RAISONNEMENT DÉTAILLÉ:")
    print(result[1])
    print(f"\nSolutions : ${latex(result[0])}$")
    print("\n" + "="*80 + "\n")

    print("Test 10: √5·x + 2 > √7 + 1 (linéaire, a et c irrationnels)")
    result = resoudre_inequation_generale(sqrt(5), 2, sqrt(7) + 1, variable="x", inegalite=">", domaine="R", puissance=1)
    print("RAISONNEMENT DÉTAILLÉ:")
    print(result[1])
    print(f"\nSolutions : ${latex(result[0])}$")
    print("\n" + "="*80 + "\n")

    print("Test 10bis: 2x - 3 + 2√3 > 1 (linéaire, a et c irrationnels, doit se simplifier)")
    result = resoudre_inequation_generale(2, -3 + 2 * sqrt(3), 1, variable="x", inegalite=">", domaine="R", puissance=1)
    print("RAISONNEMENT DÉTAILLÉ:")
    print(result[1])
    print(f"\nSolutions : ${latex(result[0])}$")
    print("\n" + "="*80 + "\n")

    # ============================================================================
    # TESTS LINÉAIRES - CAS SYMBOLIQUES
    # ============================================================================

    print("Test 11: ax + 3 ≥ 10 (linéaire symbolique, a>0 par hypothèse)")
    result = resoudre_inequation_generale(a_sym, 3, 10, variable="x", inegalite=">=", domaine="R", puissance=1)
    print("RAISONNEMENT DÉTAILLÉ:")
    print(result[1])
    print(f"\nSolutions : ${latex(result[0])}$")
    print("\n" + "="*80 + "\n")

    print("Test 12: 2x + b ≤ 5 (linéaire symbolique, b réel)")
    result = resoudre_inequation_generale(2, b_sym, 5, variable="x", inegalite="<=", domaine="R", puissance=1)
    print("RAISONNEMENT DÉTAILLÉ:")
    print(result[1])
    print(f"\nSolutions : ${latex(result[0])}$")
    print("\n" + "="*80 + "\n")

    print("Test 13: ax + b > k (linéaire entièrement symbolique)")
    result = resoudre_inequation_generale(a_sym, b_sym, k, variable="x", inegalite=">", domaine="R", puissance=1)
    print("RAISONNEMENT DÉTAILLÉ:")
    print(result[1])
    print(f"\nSolutions : ${latex(result[0])}$")
    print("\n" + "="*80 + "\n")

    # ============================================================================
    # TESTS QUADRATIQUES (puissance=2) - CAS NUMÉRIQUES
    # ============================================================================

    print("Test 14a: x² + 0 ≥ 9 (quadratique, a>0, b=0, >=)")
    result = resoudre_inequation_generale(1, 0, 9, variable="x", inegalite=">=", domaine="R", puissance=2)
    print("RAISONNEMENT DÉTAILLÉ:")
    print(result[1])
    print(f"\nSolutions : ${latex(result[0])}$")
    print("\n" + "="*80 + "\n")

    print("Test 14b: x² + 0 ≤ 9 (quadratique, a>0, b=0, <=)")
    result = resoudre_inequation_generale(1, 0, 9, variable="x", inegalite="<=", domaine="R", puissance=2)
    print("RAISONNEMENT DÉTAILLÉ:")
    print(result[1])
    print(f"\nSolutions : ${latex(result[0])}$")
    print("\n" + "="*80 + "\n")

    print("Test 15: 2x² + 5 > 15 (quadratique, a>0, b>0, >)")
    result = resoudre_inequation_generale(2, 5, 15, variable="x", inegalite=">", domaine="R", puissance=2)
    print("RAISONNEMENT DÉTAILLÉ:")
    print(result[1])
    print(f"\nSolutions : ${latex(result[0])}$")
    print("\n" + "="*80 + "\n")

    print("Test 16a: 3x² - 7 < 20 (quadratique, a>0, b<0, <)")
    result = resoudre_inequation_generale(3, -7, 20, variable="x", inegalite="<", domaine="R", puissance=2)
    print("RAISONNEMENT DÉTAILLÉ:")
    print(result[1])
    print(f"\nSolutions : ${latex(result[0])}$")
    print("\n" + "="*80 + "\n")

    print("Test 16b: 3x² - 7 < 20 (quadratique, a>0, b<0, < et détail signe a)")
    result = resoudre_inequation_generale(3, -7, 20, variable="x", inegalite="<", domaine="R", puissance=2, detail_signe_a = True)
    print("RAISONNEMENT DÉTAILLÉ:")
    print(result[1])
    print(f"\nSolutions : ${latex(result[0])}$")
    print("\n" + "="*80 + "\n")

    print("Test 17: -x² + 10 ≥ 6 (quadratique, a<0, >=)")
    result = resoudre_inequation_generale(-1, 10, 6, variable="x", inegalite=">=", domaine="R", puissance=2)
    print("RAISONNEMENT DÉTAILLÉ:")
    print(result[1])
    print(f"\nSolutions : ${latex(result[0])}$")
    print("\n" + "="*80 + "\n")

    print("Test 18: -2x² + 8 ≤ 0 (quadratique, a<0, c=0, <=)")
    result = resoudre_inequation_generale(-2, 8, 0, variable="x", inegalite="<=", domaine="R", puissance=2)
    print("RAISONNEMENT DÉTAILLÉ:")
    print(result[1])
    print(f"\nSolutions : ${latex(result[0])}$")
    print("\n" + "="*80 + "\n")

    print("Test 19: x² + 3 ≥ 7 (quadratique, domaine Z)")
    result = resoudre_inequation_generale(1, 3, 7, variable="x", inegalite=">=", domaine="Z", puissance=2)
    print("RAISONNEMENT DÉTAILLÉ:")
    print(result[1])
    print(f"\nSolutions : ${latex(result[0])}$")
    print("\n" + "="*80 + "\n")

    print("Test 20: x² - 5 < 4 (quadratique, domaine N)")
    result = resoudre_inequation_generale(1, -5, 4, variable="x", inegalite="<", domaine="N", puissance=2)
    print("RAISONNEMENT DÉTAILLÉ:")
    print(result[1])
    print(f"\nSolutions : ${latex(result[0])}$")
    print("\n" + "="*80 + "\n")

    # ============================================================================
    # TESTS QUADRATIQUES - CAS SANS SOLUTION OU SOLUTION VIDE
    # ============================================================================

    print("Test 21: x² + 5 < 2 (quadratique, pas de solution réelle)")
    result = resoudre_inequation_generale(1, 5, 2, variable="x", inegalite="<", domaine="R", puissance=2)
    print("RAISONNEMENT DÉTAILLÉ:")
    print(result[1])
    print(f"\nSolutions : ${latex(result[0])}$")
    print("\n" + "="*80 + "\n")

    print("Test 22: -x² - 3 > 0 (quadratique, a<0, pas de solution)")
    result = resoudre_inequation_generale(-1, -3, 0, variable="x", inegalite=">", domaine="R", puissance=2)
    print("RAISONNEMENT DÉTAILLÉ:")
    print(result[1])
    print(f"\nSolutions : ${latex(result[0])}$")
    print("\n" + "="*80 + "\n")

    # ============================================================================
    # TESTS QUADRATIQUES - CAS AVEC FRACTIONS ET RACINES
    # ============================================================================

    print("Test 23: (1/2)x² + 1 ≥ 3 (quadratique, a rationnel)")
    result = resoudre_inequation_generale(Rational(1, 2), 1, 3, variable="x", inegalite=">=", domaine="R", puissance=2)
    print("RAISONNEMENT DÉTAILLÉ:")
    print(result[1])
    print(f"\nSolutions : ${latex(result[0])}$")
    print("\n" + "="*80 + "\n")

    print("Test 24: x² + √2 ≤ 5 (quadratique, b irrationnel)")
    result = resoudre_inequation_generale(1, sqrt(2), 5, variable="x", inegalite="<=", domaine="R", puissance=2)
    print("RAISONNEMENT DÉTAILLÉ:")
    print(result[1])
    print(f"\nSolutions : ${latex(result[0])}$")
    print("\n" + "="*80 + "\n")

    print("Test 25: 2x² + (√3 - 1) > √5 (quadratique, expressions irrationnelles)")
    result = resoudre_inequation_generale(2, sqrt(3) - 1, sqrt(5), variable="x", inegalite=">", domaine="R", puissance=2)
    print("RAISONNEMENT DÉTAILLÉ:")
    print(result[1])
    print(f"\nSolutions : ${latex(result[0])}$")
    print("\n" + "="*80 + "\n")

    # ============================================================================
    # TESTS QUADRATIQUES - CAS SYMBOLIQUES
    # ============================================================================

    print("Test 26: ax² + 2 ≥ 10 (quadratique symbolique, a>0)")
    result = resoudre_inequation_generale(a_sym, 2, 10, variable="x", inegalite=">=", domaine="R", puissance=2)
    print("RAISONNEMENT DÉTAILLÉ:")
    print(result[1])
    print(f"\nSolutions : ${latex(result[0])}$")
    print("\n" + "="*80 + "\n")

    print("Test 27: x² + b ≤ k (quadratique symbolique)")
    result = resoudre_inequation_generale(1, b_sym, k, variable="x", inegalite="<=", domaine="R", puissance=2)
    print("RAISONNEMENT DÉTAILLÉ:")
    print(result[1])
    print(f"\nSolutions : ${latex(result[0])}$")
    print("\n" + "="*80 + "\n")

    # ============================================================================
    # TESTS DE CAS LIMITES
    # ============================================================================

    print("Test 28: 0x + 5 ≥ 3 (linéaire dégénéré, a=0, toujours vrai)")
    result = resoudre_inequation_generale(0, 5, 3, variable="x", inegalite=">=", domaine="R", puissance=1)
    print("RAISONNEMENT DÉTAILLÉ:")
    print(result[1])
    print(f"\nSolutions : ${latex(result[0])}$")
    print("\n" + "="*80 + "\n")

    print("Test 29: 0x + 2 > 5 (linéaire dégénéré, a=0, jamais vrai)")
    result = resoudre_inequation_generale(0, 2, 5, variable="x", inegalite=">", domaine="R", puissance=1)
    print("RAISONNEMENT DÉTAILLÉ:")
    print(result[1])
    print(f"\nSolutions : ${latex(result[0])}$")
    print("\n" + "="*80 + "\n")

    print("Test 30: x² + 0 ≥ 0 (quadratique, toujours vrai)")
    result = resoudre_inequation_generale(1, 0, 0, variable="x", inegalite=">=", domaine="R", puissance=2)
    print("RAISONNEMENT DÉTAILLÉ:")
    print(result[1])
    print(f"\nSolutions : ${latex(result[0])}$")
    print("\n" + "="*80 + "\n")

    print("Test 31a: -3x + 7 ≤ 1 (linéaire, a<0, domaine N avec solution)")
    result = resoudre_inequation_generale(-3, 7, 1, variable="x", inegalite="<=", domaine="N", puissance=2)
    print("RAISONNEMENT DÉTAILLÉ:")
    print(result[1])
    print(f"\nSolutions : ${latex(result[0])}$")
    print("\n" + "="*80 + "\n")

    print("Test 31b: -3x + 7 ≤ 1 (linéaire, a<0, domaine N avec solution + détail signe a)")
    result = resoudre_inequation_generale(-3, 7, 1, variable="x", inegalite="<=", domaine="N", puissance=2, detail_signe_a = True)
    print("RAISONNEMENT DÉTAILLÉ:")
    print(result[1])
    print(f"\nSolutions : ${latex(result[0])}$")
    print("\n" + "="*80 + "\n")

    print("Test 32: (1/3)x² - 2 > 1 (quadratique rationnel, domaine Z)")
    result = resoudre_inequation_generale(Rational(1, 3), -2, 1, variable="x", inegalite=">", domaine="Z", puissance=2)
    print("RAISONNEMENT DÉTAILLÉ:")
    print(result[1])
    print(f"\nSolutions : ${latex(result[0])}$")
    print("\n" + "="*80 + "\n")


    print("Test 33: Cx² + sqrt(2) + 1 > sqrt(3)")
    C = Symbol("C")
    result = resoudre_inequation_generale(C, sqrt(2) + 1, sqrt(3), variable="n", inegalite=">", domaine="R", puissance=2)
    print("RAISONNEMENT DÉTAILLÉ:")
    print(result[1])
    print(f"\nSolutions : ${latex(result[0])}$")
    print("\n" + "="*80 + "\n")

    print("Test 34: Cx² + sqrt(2) + 1 > sqrt(3) dans Z")
    C = Symbol("C")
    result = resoudre_inequation_generale(C, sqrt(2) + 1, sqrt(3), variable="n", inegalite=">", domaine="Z", puissance=2)
    print("RAISONNEMENT DÉTAILLÉ:")
    print(result[1])
    print(f"\nSolutions : ${latex(result[0])}$")
    print("\n" + "="*80 + "\n")

    print("Test 35: totalement indéterminé:")
    a, b, c = symbols("a,b,c")
    result = resoudre_inequation_generale(a, b, c, variable="n", inegalite=">", domaine="R", puissance=2)
    print("RAISONNEMENT DÉTAILLÉ:")
    print(result[1])
    print(f"\nSolutions : ${latex(result[0])}$")
    print("\n" + "="*80 + "\n")

    print("="*80)
    print("FIN DES TESTS")
    print("="*80)






def pxsl_latex(expr, reverse = False):
    """
    Convertit une expression symbolique en représentation LaTeX.
    
    Args:
        expr: Expression symbolique (probablement SymPy) à convertir
        reverse (bool): Si True, inverse l'ordre des termes dans l'expression
    
    Returns:
        str: Représentation LaTeX de l'expression
    
    Examples:
        >>> from sympy import symbols
        >>> x, y = symbols('x y')
        
        # Conversion standard
        >>> expr = x**2 + 3*x - 5
        >>> pxsl_latex(expr)
        'x^{2} + 3 x - 5'
        
        # Conversion avec ordre inversé
        >>> pxsl_latex(expr, reverse=True)
        '- 5 + 3 x + x^{2}'
        
        # Expression avec termes négatifs
        >>> expr2 = -2*x**2 + x - 7
        >>> pxsl_latex(expr2, reverse=True)
        '- 7 + x - 2 x^{2}'
        
        # Expression plus complexe
        >>> expr3 = x**3 - 2*x**2 + 3*x - 4
        >>> pxsl_latex(expr3, reverse=True)
        '- 4 + 3 x - 2 x^{2} + x^{3}'
    
    Note:
        La fonction utilise myst() pour l'interpolation des variables,
        ce qui suggère une intégration avec MyST (Markedly Structured Text).

    :pxs_trigger: afficher une expression sympy en LaTeX avec option d'ordre inversé (degrés croissants au lieu de décroissants), polynôme "-5 + 3x + x^2" au lieu de "x^2 + 3x - 5", énoncé qui lit les termes du plus bas au plus haut degré, chaînage terme à terme avec + / -
    :pxs_returns: |
        chaîne LaTeX. Si ``reverse=False``, équivalent à ``sympy.latex(expr)``. Si ``reverse=True``,
        itère sur ``expr.as_ordered_terms()[::-1]`` et insère manuellement ``+`` entre termes
        positifs consécutifs.
    :pxs_example: |
        pxsl_latex(x**2 + 3*x - 5, reverse=True)  # → "- 5 + 3 x + x^{2}"
    :pxs_antipattern: Reconstruire la chaîne LaTeX à la main en concaténant les termes d'un polynôme dans l'ordre inverse avec des str.split.
    """
    # Si l'option reverse est activée, traiter les termes dans l'ordre inverse
    if reverse == True:
        # Initialiser la chaîne LaTeX vide
        expr_latex = ""
        
        # Obtenir les termes de l'expression dans l'ordre inverse
        # as_ordered_terms() retourne une liste des termes, [::-1] inverse la liste
        terms = expr.as_ordered_terms()[::-1]
        
        # Parcourir chaque terme avec son index
        for i, term in enumerate(terms):
            # Convertir le terme en chaîne de caractères
            term_str = str(term)
            
            # Pour tous les termes sauf le premier, ajouter un signe +
            # seulement si le terme ne commence pas déjà par un signe négatif
            if i != 0 and not term_str.startswith('-'):
                sign = myst(r"""+""")
            else:
                # Pas de signe pour le premier terme ou les termes négatifs
                sign = ""
            
            # Construire l'expression LaTeX en ajoutant le signe et le terme converti
            # myst() semble être une fonction de template qui interpole les variables
            expr_latex += myst(r"""\py{sign}\py{latex(term)} """, globals(), locals())
        
        # Retourner l'expression LaTeX complète
        return expr_latex
    
    # Cas par défaut : retourner simplement la conversion LaTeX standard
    return latex(expr)

def pxs_is_reductible_sqrt(x):
    """
    fr : détermine si un nombre ou une expression est reductible en racine carrée
    en : determines if a number or an expression is reducible for square root

    Args:
        x : nombre ou expression symbolique
    
    Returns:
        bool: True si x est simplifiable dans une racine carrée
    
    Examples:
        >>> pxs_is_reductible_sqrt(16) 
        'True'
        >>> pxs_is_reductible_sqrt(24)
        'True'
        >>> pxs_is_reductible_sqrt(13)
        'False'
        >>> pxs_is_reductible_sqrt(13/24)
        'True'

        >>> x = Symbol('x')
        >>> pxs_is_reductible_sqrt(4*x)
        'True'
        >>> pxs_is_reductible_sqrt(x/4)
        'True'
        >>> y = Symbol('y')
        >>> pxs_is_reductible_sqrt(x/(4*y))
        'True'
        >>> pxs_is_reductible_sqrt(3*x/(2*y))
        'False'

    :pxs_trigger: tester si sqrt(x) peut être simplifié, détection d'un facteur premier de multiplicité ≥ 2 dans la factorisation du numérateur ou dénominateur de x, préparer une étape "√24 = 2√6" dans un corrigé, décider d'ajouter l'étape de simplification des racines
    :pxs_returns: |
        ``bool`` : ``True`` si ``x`` (int, Integer, Rational ou Mul d'entiers/symboles) possède un
        facteur premier d'exposant ≥ 2 dans ``p`` ou ``q``, ``False`` sinon.
    :pxs_example: |
        if pxs_is_reductible_sqrt(24):
            # ajouter l'étape √24 = 2√6 dans le corrigé
            ...
    :pxs_antipattern: Appeler ``simplify(sqrt(x)) != sqrt(x)`` qui peut échouer ou boucler sur des Mul symboliques, ou tester ``str(sqrt(x))``.
    """

    def _is_factor(x, is_reducible):
        factors = factorint(x)
        for prime, power in factors.items():
            if power >= 2:
                is_reducible = True
        return is_reducible

    def _is_reducible_int(x, is_reducible):
        if isinstance(x, (int, Integer)):
            is_reducible = _is_factor(x, is_reducible)
        return is_reducible

    def _is_reducible_rational(x, is_reducible):
        try:
            x_ratio = Rational(x)
            is_reducible = _is_factor(x_ratio.p, is_reducible)
            is_reducible = _is_factor(x_ratio.q, is_reducible)
        except:
            pass
        return is_reducible
        
    is_reducible = False
    is_reducible = _is_reducible_int(x, is_reducible)
    is_reducible = _is_reducible_rational(x, is_reducible)
    
    if isinstance(x, Mul):
        for arg in x.args:
            is_reducible = _is_reducible_int(arg, is_reducible)
            is_reducible = _is_reducible_rational(arg, is_reducible)
    return is_reducible

def pxsl_Rational(num, den, orientation="v", display=True):
    """
    Builds a SymPy expression representing the rational fraction `num/den`,
    simplifying only the numeric parts while keeping the symbolic or irrational
    factors in place.

    Parameters
    ----------
    num : sympy.Expr, int, float
        The numerator of the fraction. Can be numeric or symbolic
        (e.g., `3*pi`, `2*x`, etc.).
    den : sympy.Expr, int, float
        The denominator of the fraction. Must not be zero.
    orientation : str, optional
        Display orientation: `'v'` for vertical (LaTeX-style fraction),
        or any other value for horizontal rendering. Default is `'v'`.
    display : bool, optional
        If `True`, returns a formatted LaTeX string via `myst()` for
        visual display. If `False`, returns a raw LaTeX string.
        Default is `True`.

    Returns
    -------
    sympy.Expr or str
        A SymPy expression representing the simplified fraction, or a LaTeX
        string depending on the `orientation` and `display` parameters.

    Raises
    ------
    ZeroDivisionError
        If `den` equals zero.

    Examples
    --------
    >>> pxsl_Rational(3*pi, 6)
    \displaystyle{\frac{\pi}{2}}

    >>> x = Symbol('x')
    >>> pxsl_Rational(4*x, 8)
    \displaystyle{\frac{x}{2}}

    >>> pxsl_Rational(3*pi, 6, orientation='h')
    \pi / 2

    :pxs_trigger: construire une fraction LaTeX ``num/den`` en simplifiant uniquement les parties numériques et en gardant les symboles/irrationnels (π, x, √3) intacts, affichage vertical \frac par défaut ou horizontal "a / b", gestion du cas dénominateur ±1, simplification par gcd en interne
    :pxs_returns: |
        chaîne MyST/LaTeX : ``\displaystyle{\frac{...}{...}}`` par défaut (``orientation="v"``,
        ``display=True``), variante horizontale ``a / b`` si ``orientation!="v"``, ou juste le
        numérateur si le dénominateur se simplifie à ±1. Lève ``ZeroDivisionError`` si ``den == 0``.
    :pxs_example: |
        myst(r"x = \py{pxsl_Rational(3*pi, 6)}")  # → \displaystyle{\frac{\pi}{2}}
    :pxs_antipattern: Passer ``Rational(3*pi, 6)`` ou ``3*pi / 6`` à ``latex()`` directement — sympy peut écraser le π ou produire une forme non simplifiée.
    """

    # Convert inputs into SymPy expressions
    num = sympify(num)
    den = sympify(den)

    # Denominator must not be zero
    if den == 0:
        raise ZeroDivisionError("Denominator is zero.")

    # Separate the numeric coefficient from the symbolic/irrational remainder
    # Example: 3*pi → (3, pi), 6 → (6, 1)
    ncoef, nrest = num.as_coeff_Mul()
    dcoef, drest = den.as_coeff_Mul()

    # Extract internal numerator/denominator for rational arithmetic
    # Example: Rational(3,2) → (3, 2)
    a, b = ncoef.as_numer_denom()
    c, d = dcoef.as_numer_denom()

    # Preliminary GCD reduction between a and c to avoid large integers
    g1 = gcd(a, c)
    if g1 != 0:
        a //= g1
        c //= g1

    # Compute the numeric coefficient (a*d)/(b*c)
    num_int = a * d
    den_int = b * c

    # Normalize sign: denominator must always be positive
    if den_int < 0:
        den_int = -den_int
        num_int = -num_int

    # Final GCD reduction for the numeric ratio
    g2 = gcd(num_int, den_int)
    if g2 != 0:
        num_int //= g2
        den_int //= g2

    # Build the final SymPy expression, keeping symbolic structure intact
    expr = (Integer(num_int) * nrest) / (Integer(den_int) * drest)

    # Display handling according to user parameters
    if orientation == 'v' and display:
        # Special case: denominator equals ±1
        if Integer(den_int) * drest == 1:
            return myst(r""" \displaystyle{\py{latex(Integer(num_int) * nrest)}} """, locals(), globals())
        elif Integer(den_int) * drest == -1:
            return myst(r""" \displaystyle{\py{latex(-Integer(num_int) * nrest)}} """, locals(), globals())
        # General case
        return myst(r"""\displaystyle{\py{latex(expr)}}""", locals(), globals())

    elif orientation == 'v':
        # Non-displayed version (raw LaTeX)
        return myst(r"""\py{latex(expr)}""", locals(), globals())

    else:
        # Horizontal display mode
        if Integer(den_int) * drest == 1:
            return myst(r"""\py{latex(Integer(num_int) * nrest)}""", locals(), globals())
        elif Integer(den_int) * drest == -1:
            return myst(r"""\py{latex(-Integer(num_int) * nrest)}""", locals(), globals())
        else:
            return myst(r"""\py{latex(Integer(num_int) * nrest)} / \py{latex(Integer(den_int) * drest)}""", locals(), globals())
        
def pxs_separate_factors(expr, var):
    """
    Split an expression into (factor independent of ``var``, factor containing ``var``).

    For a ``Mul``, delegates to ``expr.as_independent(var)``. For an ``Add``, attempts
    factorization first and retries ; returns ``(1, expr)`` if no clean split is found.

    :pxs_trigger: séparer un produit en (coefficient indépendant de var, partie contenant var), isoler le coefficient numérique/symbolique extérieur à la variable d'intégration, utilisé en IBP pour extraire le facteur devant u(x) ou v'(x), décomposition Mul vs Add
    :pxs_returns: |
        tuple ``(coeff, reste)`` : ``coeff`` indépendant de ``var``, ``reste`` contenant ``var``.
        Retourne ``(1, expr)`` si ``expr`` est un ``Add`` non factorisable ou d'un autre type.
    :pxs_example: |
        from sympy import Symbol, exp
        x = Symbol('x')
        coef, rest = pxs_separate_factors(3*x*exp(x), x)  # → (3, x*exp(x))
    :pxs_antipattern: Deviner manuellement le coefficient extérieur avec des regex sur la chaîne LaTeX, ou appeler ``expr.args[0]`` en supposant que c'est toujours le coefficient.
    """
    if isinstance(expr, Mul):
        return expr.as_independent(var)[0], expr.as_independent(var)[1]
    if isinstance(expr, Add):
        expr = factor(expr)
        if isinstance(expr, Add):
            return 1, expr
        else:
            return pxs_separate_factors(expr, var)
    return 1, expr

def pxs_ln(arg):
    """
    Reduce the natural logarithm ln(arg) when the argument is a perfect power.

    The function rewrites ln(m**k) as k*ln(m) whenever possible.
    If the argument cannot be reduced, the expression ln(arg) is returned unchanged.

    Parameters
    ----------
    arg : sympy expression or int
        Argument of the natural logarithm.

    Returns
    -------
    sympy expression
        A reduced logarithmic expression of the form k*ln(m) if applicable,
        otherwise ln(arg).

    Examples
    --------
    >>> pxs_ln(9)
    2*ln(3)

    >>> pxs_ln(12)
    ln(12)

    >>> pxs_ln(1)
    ln(1)

    >>> pxs_ln(72)
    2*ln(6)

    :pxs_trigger: simplifier ln(m**k) en k·ln(m) pour un entier positif dont la factorisation admet un exposant commun ≥ 2, factorisation de l'argument d'un logarithme, exercice "écrire ln(9) sous la forme k·ln(m)", propriétés des log
    :pxs_returns: |
        expression sympy : ``k*ln(m)`` si ``arg = m**k`` avec ``k = min(exponents) ≥ 2`` dans sa
        factorisation première, sinon ``ln(arg)`` inchangé. Retourne ``ln(arg)`` pour les
        non-entiers, les négatifs, et le cas ``arg == 1``.
    :pxs_example: |
        pxs_ln(9)   # → 2*ln(3)
        pxs_ln(12)  # → ln(12)  (pas de facteur commun ≥ 2)
    :pxs_antipattern: Utiliser ``logcombine`` ou ``expand_log`` qui ne cherchent pas à factoriser l'argument entier du log.
    """

    # Convert input to a SymPy object
    arg = sympify(arg)

    # Domain and type checks
    if not arg.is_Integer or arg <= 0:
        return ln(arg)

    # Special case: ln(1)
    if arg == 1:
        return ln(1)

    # Prime factorization of the argument
    factors = factorint(arg)

    # Safety check: empty factorization (e.g. arg == 1)
    if not factors:
        return ln(arg)

    # Extract the maximal common exponent
    k = min(factors.values())
    if k <= 1:
        return ln(arg)

    # Reconstruct the base m such that arg = m**k
    m = Integer(1)
    for p, e in factors.items():
        m *= p**(e // k)

    return k * ln(m)

def pxs_is_factorable(expr) -> bool:
    """
    Determine whether a SymPy expression is factorable.

    An expression is considered factorable if its factorized form
    is not equivalent to its expanded form.

    Parameters
    ----------
    expr : sympy expression or str
        The expression to test.

    Returns
    -------
    bool
        True if the expression is factorable, False otherwise.

    Examples
    --------
    >>> pxsl_is_factorable("x^2 - 1")
    True

    >>> pxsl_is_factorable("x^2 + 1")
    False

    >>> pxsl_is_factorable("2*x*(x+1)")
    False

    :pxs_trigger: tester si un polynôme est factorisable (x²-1 factorisable, x²+1 non), choisir entre méthode "simple" et "advanced" pour la décomposition en éléments simples, décider d'afficher une étape de factorisation dans un corrigé, branchement logique avant appel à factor()
    :pxs_returns: |
        ``bool`` : ``True`` si ``factor(expr)`` diffère structurellement de ``expand(expr)``
        (test via ``simplify(expanded - factored) != 0``), ``False`` sinon. Accepte ``Poly``,
        expression sympy ou ``str``.
    :pxs_example: |
        if pxs_is_factorable(x**2 - 1):
            # afficher (x-1)(x+1) dans le corrigé
            ...
    :pxs_antipattern: Comparer ``str(factor(e)) == str(expand(e))`` qui dépend de l'ordre d'affichage des termes.
    """
    if isinstance(expr, Poly):
        expr = expr.as_expr()
    expr = sympify(expr)

    expanded = expand(expr)
    factored = factor(expr)

    # If factor() does not change the structure, it's not factorable
    return not simplify(expanded - factored) == 0

def pxsl_quotient(num: "sympy.Expr", den: "sympy.Expr", sign: bool = True) -> str:
    """
    Formats a quotient in LaTeX using myst, with special handling depending
    on whether the numerator is equal to 1.

    Parameters
    ----------
    num : sympy.Expr
        The numerator of the quotient.
    den : sympy.Expr
        The denominator of the quotient.
    sign : bool, optional
        If True, the sign of the expression is explicitly handled.
        Default is True.

    Returns
    -------
    str
        A LaTeX-formatted string generated via `myst`, representing
        either the simplified quotient `num/den` or the product
        `num * 1/den` depending on the value of `num.q`.

    Examples
    --------
    Case 1 — numerator behaves like 1 (num.q == 1)
    The function returns a single `lc(num/den, sign=sign)` block.

    >>> # Example setup (illustrative)
    >>> # num = 1, den = x + 1
    >>> pxsl_quotient(num, den)
    '\\n        \\\\py{lc(num/den, sign = sign)}\\n        '

    >>> # Same case, but without forcing sign handling
    >>> pxsl_quotient(num, den, sign=False)
    '\\n        \\\\py{lc(num/den, sign = sign)}\\n        '

    Case 2 — general numerator (num.q != 1)
    The function returns `lc(num, sign=sign)` multiplied by `1/den`.

    >>> # Example setup (illustrative)
    >>> # num = 3*x, den = x + 1
    >>> pxsl_quotient(num, den)
    '\\n        \\\\py{lc(num, sign = sign)}\\\\py{mult_A}\\\\frac{1}{\\\\py{latex(den)}}\\n        '

    >>> # Same case, but without forcing sign handling
    >>> pxsl_quotient(num, den, sign=False)
    '\\n        \\\\py{lc(num, sign = sign)}\\\\py{mult_A}\\\\frac{1}{\\\\py{latex(den)}}\\n        '

    :pxs_trigger: afficher un quotient num/den en LaTeX avec choix automatique entre ``\frac{num}{den}`` (si num.q == 1, i.e. num entier) et ``num · \frac{1}{den}`` (si num est une Rational non entière), formatage de coefficients complexes dans un corrigé de dérivation / intégration ; attention : dépend de ``lc`` et ``mult_A`` disponibles dans le scope appelant
    :pxs_returns: |
        chaîne MyST/LaTeX : soit ``\py{lc(num/den, sign=sign)}``, soit
        ``\py{lc(num, sign=sign)}\py{mult_A}\frac{1}{\py{latex(den)}}`` selon la nature de
        ``num.q``. Nécessite ``lc`` et ``mult_A`` définis en globals/locals à l'appel.
    :pxs_example: |
        # dans un exercice où `lc = pxsl_latex_coefficient` et `mult_A = myst(r"\cdot")`
        myst(r"f'(x) = \py{pxsl_quotient(Rational(3), x + 1)}")
    :pxs_antipattern: Écrire ``\frac{num}{den}`` en dur sans différencier le cas où num contient déjà une fraction (produit une fraction complexe illisible).
    """

    if num.q == 1:
        return myst(r"""
        \py{lc(num/den, sign = sign)}
        """, globals(), locals())
    else:
        return myst(r"""
        \py{lc(num, sign = sign)}\py{mult_A}\frac{1}{\py{latex(den)}}
        """, globals(), locals())

def pxs_randint(mini, maxi, exclude = []):
    """
    Returns a random integer between mini and maxi avoiding the element(s) in exclude.
    Exclude can be an integer or a collection of integers.

    :pxs_trigger: tirer un entier aléatoire dans [mini, maxi] en excluant une ou plusieurs valeurs, génération de paramètres d'exercice (coefficients, exposants, indices) sans collision, éviter 0 / 1 / une valeur déjà utilisée ailleurs, randomisation reproductible d'un énoncé
    :pxs_returns: |
        ``int`` : entier tiré uniformément dans ``{mini, ..., maxi} \ exclude``.
        ``exclude`` accepte un ``int`` seul ou n'importe quel itérable d'entiers.
    :pxs_example: |
        a = pxs_randint(-5, 5, exclude=0)      # coefficient non nul
        b = pxs_randint(1, 10, exclude=[a, a+1])  # évite a et a+1
    :pxs_antipattern: Boucler ``while x in exclude: x = randint(...)`` à la main dans chaque exercice, ou tirer dans la liste complète et re-tirer en cas de collision.
    """
    
    if isinstance(exclude, int):
        exclude = exclude,
    st = set(range(mini, maxi + 1)) - set(exclude)
    return rd.choice(list(st))