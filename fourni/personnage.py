from .actor import Actor


class Personnage(Actor):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.tag = "perso"
        self.mort = False
        self.fini = False

    def __eq__(self, other: object) -> bool:
        return (self.x == other.x) and (self.y == other.y)

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def est_mort(self)-> bool:
        """
        Fonction permettant de donner l'état du joueur (mort ou vivant)
        :return: un booléen disant si le joueur est mort ou non
        """
        return self.mort

    def est_attraper(self):
        """
        Fonction permettant de changer l'état du joueur de vivant à mort.
        """
        self.mort = True

    def a_fini(self):
        """
        Fonction permettant de changer l'état du joueur de "en jeu" à "sorti".
        """
        self.fini = True

    def est_sorti(self)-> bool:
        """
        Fonction permettant de donner l'état du joueur (en jeu ou sorti)
        :return: un booléen disant si le joueur est sorti ou non
        """
        return self.fini