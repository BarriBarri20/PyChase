from fourni.minotaure import Minotaure
from fourni.case_vide import CaseVide
from fourni.sortie import Sortie
from fourni.mur import Mur
from fourni.personnage import Personnage

DISTANCE_ENTRE_CASE = 32
X_PREMIERE_CASE = 20

def creer_image(_can, _x: int, _y: int, _image: object):
    """
    Fonction qui permet de créer/remplacer une image dans le canvas. Pour l'utiliser il faut préciser :
    :param _can: un canvas (faites abstraction de ce que c'est et marquez : can
    :param _x: une coordonnée dans l'axe des abscisses ( coordonnée x)
    :param _y: une coordonnée dans l'axe des ordonnées ( coordonnée y)
    :param _image: une image tirée de la liste d'image (voir énoncé pour quelle image choisir via quel index)
    :return:
    """
    _can.create_image(_x* DISTANCE_ENTRE_CASE + X_PREMIERE_CASE, _y* DISTANCE_ENTRE_CASE + X_PREMIERE_CASE, image=_image)


def creer_mur(_x: int, _y: int) -> Mur:
    """
    Fonction permettant de créer un mur.
    :param _x: coordonnée en x du mur à créer
    :param _y:coordonnée en y du mur à créer
    :return: la variable mur
    """
    return Mur(_x, _y)


def creer_minotaure(_x: int, _y: int) -> Minotaure:
    """
    Fonction permettant de créer un minotaure.
    :param _x: coordonnée en x du minotaure à créer
    :param _y:coordonnée en y du minotaure à créer
    :return: la variable minotaure
    """
    return Minotaure(_x, _y)


def creer_sortie(_x: int, _y: int)-> Sortie:
    """
    Fonction permettant de créer une Sortie.
    :param _x: coordonnée en x de la Sortie à créer
    :param _y:coordonnée en y de la Sortie à créer
    :return: la variable Sortie
    """
    return Sortie(_x, _y)


def creer_personnage(_x: int, _y: int) -> Personnage:
    """
    Fonction permettant de créer un personnage.
    :param _x: coordonnée en x du personnage à créer
    :param _y:coordonnée en y du personnage à créer
    :return: la variable personnage
    """
    return Personnage(_x, _y)


def creer_case_vide(_x: int, _y: int) -> CaseVide:
    """
    Fonction permettant de créer une case vide.
    :param _x: coordonnée en x de la case vide à créer
    :param _y:coordonnée en y de la case vide à créer
    :return: la variable case vide
    """
    return CaseVide(_x, _y)


def coordonnee_x(_variable: object) -> int:
    """
    Fonction permettant de retourner la coordonnée en x de la variable.
    :param _variable: la variable (Personnage,Minotaure, CaseVide, Sortie, Mur)
    :return: la coordonnée en x de la variable
    """
    return _variable.get_x()


def coordonnee_y(_variable: object) -> int:
    """
    Fonction permettant de retourner la coordonnée en y de la variable.
    :param _variable: la variable (Personnage,Minotaure, CaseVide, Sortie, Mur)
    :return: la coordonnée en y de la variable
    """
    return _variable.get_y()


def est_egal_a(_variable1: object, _variable2: object) -> bool:
    """
    Fonction permettant de tester l'égalité entre 2 variables (Personnage, Minotaure, CaseVide, Sortie, Mur)
    :param _variable1: variable (Personnage, Minotaure, CaseVide, Sortie, Mur)
    :param _variable2: variable (Personnage, Minotaure, CaseVide, Sortie, Mur)
    :return: Booléen (True si les deux variables sont identiques, False sinon)
    """
    return _variable1 == _variable2
