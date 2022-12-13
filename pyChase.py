from fourni import simulateur, pathfinder
from outils import \
    creer_image, \
    creer_minotaure, creer_case_vide, creer_sortie, creer_mur, creer_personnage, \
    coordonnee_x, coordonnee_y, est_egal_a

# Constante à utiliser
NIVEAU_DIFFICULTE: int = 5  # Nombre de case que le minotaure avance en cas d'erreur

# Fonctions à développer

def jeu_en_cours(_joueur, _temps_restant) -> str:
    """
    Fonction testant si le jeu est encore en cours et retournant un string comme réponse sur l'état de la partie.
    :param _joueur: La liste des joueurs du niveau en cours
    :param _temps_restant : Le temps restant de la partie
    :return: un string "mort" si le joueur est mort ou "fini" si le joueur s'est echappé. Retourne "" si la partie 
             est en cours
    """
    
    if _temps_restant <= 0:
        print("fini")
        return "fini"
    for jouer in _joueur:
        if jouer.mort:
            return "mort"
        if jouer.est_sorti():
            return "fini"
    return ""


def charger_niveau(_carte: list, _joueur: list, _minotaures: list, _sorties: list, _murs: list, _path: str):
    """
    Fonction permettant de charger depuis un fichier.txt et de remplir les différentes listes permettant le
    fonctionnement du jeu (joueur, minotaures, murs, sorties)
    :param _carte: liste de liste comportant toutes les entités (joueur, minotaures, murs, sorties). C'est la grille du jeu.
    :param _joueur: liste contenant le joueur
    :param _minotaures: liste des minotaures
    :param _sorties: liste des sorties
    :param _murs: liste des murs
    :param _path: chemin du fichier.txt
    """
    with open(_path, 'r') as f: # Ouverture du fichier en lecture
        lines = f.read().splitlines()
        _carte = [line.strip() for line in lines]

    f.close() # Fermeture du fichier
    for i in range(len(_carte)):
        _carte[i] = list(_carte[i])
        for j in (range(len(_carte[i]))):
            if _carte[i][j] == "#": # Mur
                _murs.append(creer_mur(j, i))
                _carte[i][j] = "mur"
            elif _carte[i][j] == "$": # Minotaure
                _minotaures.append(creer_minotaure(j, i))
                _carte[i][j] = "minotaure" 
            elif _carte[i][j] == ".": # Sortie
                _sorties.append(creer_sortie(j, i))
                _carte[i][j] = "sortie"
            elif _carte[i][j] == "@":  # Joueur
                _joueur.append(creer_personnage(j, i))
                _carte[i][j] = "joueur"
            else: # Vide
                _carte[i][j] = "vide"
    return _carte

def avancer_minotaure(_minotaures: list, _joueur: list, _murs: list, _carte: list, _can, _liste_image: list):
    """
        Fonction permettant de faire avancer le(s) minotaure(s) grâce à l'algorithme de pathfinding. Suivant le niveau
        de difficulté, le minotaure va avancer d'un certain nombre de cases vers le joueur. Si le joueur est trop
        proche, celui-ci est éliminé.
        :param _minotaures: La liste de minotaure
        :param _joueur: La liste contenant le joueur
        :param _murs: La liste contenant les murs
        :param _carte : La liste de liste formant la grille du jeu
        :param _can: Canvas (ignorez son fonctionnement), utile uniquement pour créer_image()
        :param _liste_image : Liste contenant les références sur les images
    """
    print("Avancer minotaure")
    for minotaure in _minotaures:
        chemin = pathfinder.search(_murs, _carte, cost=1, start=(minotaure.x, minotaure.y), end=(_joueur[0].x, _joueur[0].y))
        for step in range(NIVEAU_DIFFICULTE+1):
            for i in range(len(chemin)):
                for j in range(len(chemin[i])):
                    if step == chemin[i][j]:
                        creer_image(_can, minotaure.x, minotaure.y, _liste_image[4])
                        minotaure.x = j
                        minotaure.y = i
                        creer_image(_can, minotaure.x, minotaure.y, _liste_image[2])
                    if _joueur[0].x == minotaure.x and _joueur[0].y == minotaure.y:
                        _joueur[0].mort = True
                        creer_image(_can, _joueur[0].x, _joueur[0].y, _liste_image[4])
                        creer_image(_can, _joueur[0].x, _joueur[0].y, _liste_image[3])


def definir_mouvement(_direction: str, _can, _joueur: list, _murs: list, _minotaures: list, _sorties: list, _carte: list, _liste_image: list):
    """
    Fonction permettant de définir la case de destination selon la direction choisie.
    :param _direction: Direction dans laquelle le joueur se déplace (droite, gauche, haut, bas)
    :param _can: Canvas (ignorez son fonctionnement), utile uniquement pour créer_image()
    :param _joueur: Liste des joueurs
    :param _murs: Liste des murs
    :param _minotaures: Liste des minotaures
    :param _sorties: Liste des sorties
    :param _carte: La liste de liste formant la grille du jeu
    :param _liste_image: Liste contenant les références sur les images
    :return:
    """
    for jouer in _joueur:
        if _direction == "droite":
            coordonnee_destination = creer_case_vide(coordonnee_x(jouer)+1, coordonnee_y(jouer))
            try :
                effectuer_mouvement(coordonnee_destination, _minotaures, _murs, _joueur, _sorties, _carte, _can, _liste_image, coordonnee_x(coordonnee_destination), coordonnee_y(coordonnee_destination))
            except:
                print("Erreur")
            print("Droite")

        elif _direction == "gauche":
            coordonnee_destination = creer_case_vide(coordonnee_x(jouer)-1, coordonnee_y(jouer))
            try:
                effectuer_mouvement(coordonnee_destination, _minotaures, _murs, _joueur, _sorties, _carte, _can, _liste_image, coordonnee_x(coordonnee_destination), coordonnee_y(coordonnee_destination))
            except:
                print('Erreur')
            print("Gauche")
        elif _direction == "haut":
            coordonnee_destination = creer_case_vide(coordonnee_x(jouer), coordonnee_y(jouer) - 1)
            try:
                effectuer_mouvement(coordonnee_destination, _minotaures, _murs, _joueur, _sorties, _carte, _can, _liste_image, coordonnee_x(coordonnee_destination), coordonnee_y(coordonnee_destination))
            except:
                print('Erreur')
            print("Haut")
        elif _direction == "bas":
            coordonnee_destination = creer_case_vide(coordonnee_x(jouer), coordonnee_y(jouer) + 1)
            try:
                effectuer_mouvement(coordonnee_destination, _minotaures, _murs, _joueur, _sorties, _carte, _can, _liste_image, coordonnee_x(coordonnee_destination), coordonnee_y(coordonnee_destination))
            except:
                print('Erreur')
            print("Bas")

def effectuer_mouvement(_coordonnee_destination, _minotaures: list, _murs: list, _joueur: list, _sorties: list, _carte: list, _can,
                        _liste_image: list, _deplace_joueur_x: int, _deplace_joueur_y: int):
    """
    Fonction permettant d'effectuer le déplacement ou de ne pas l'effectuer si celui-ci n'est pas possible.
    Voir énoncé "Quelques règles".
    ----------Cette methode est appelée par mouvement.--------------
    :param _coordonnee_destination: variable CaseVide ayant possiblement des coordonnées identiques à une autre variable
    (murs, minotaure, casevide)
    :param _minotaures: liste des minotaures
    :param _murs: liste des murs
    :param _joueur: liste des joueurs
    :param _sorties: Liste des sorties
    :param _carte: La liste de liste formant la grille du jeu
    :param _can: Canvas (ignorez son fonctionnement), utile uniquement pour créer_image()
    :param _liste_image: Liste contenant les références sur les images
    :param _deplace_joueur_x: coordonnée en x à laquelle le joueur va être après le mouvement
    :param _deplace_joueur_y: coordonnée en y à laquelle le joueur va être après le mouvement
    """
    for jouer in _joueur:
        for mur in _murs:
            if _deplace_joueur_x == coordonnee_x(mur) and _deplace_joueur_y == coordonnee_y(mur):
                avancer_minotaure(_minotaures, _joueur, _murs, _carte, _can, _liste_image)
                return
        for minotaure in _minotaures:
            if _deplace_joueur_x == coordonnee_x(minotaure) and _deplace_joueur_y == coordonnee_y(minotaure):
                jouer.mort = True
                return
                
        for sortie in _sorties:
            if _deplace_joueur_x == coordonnee_x(sortie) and _deplace_joueur_y == coordonnee_y(sortie):
                creer_image(_can, jouer.x, jouer.y, _liste_image[4])
                jouer.x = _deplace_joueur_x
                jouer.y = _deplace_joueur_y
                creer_image(_can, jouer.x, jouer.y, _liste_image[4])
                jouer.fini = True
                jouer.gagne = True
                return
        
        creer_image(_can, jouer.x, jouer.y, _liste_image[4])
        jouer.x = _deplace_joueur_x
        jouer.y = _deplace_joueur_y
        creer_image(_can, jouer.x, jouer.y, _liste_image[3])



def chargement_score(_scores_file_path: str, _dict_scores: dict):
    """
    Fonction chargeant les scores depuis un fichier.txt et les stockent dans un dictionnaire
    :param _scores_file_path: le chemin d'accès du fichier
    :param _dict_scores:  le dictionnaire pour le stockage
    :return:
    """
    with open(_scores_file_path, "r") as fichier:
        lignes = fichier.readlines()
    for i in range(len(lignes)):
        scores = lignes[i].strip().split(";")[1:][:-1]
        print(scores[:-1])
        list_scores = [float(j) for j in scores] # On récupère les scores
        _dict_scores[int(lignes[i].replace("\n", "").split(";")[0])] = list_scores


def maj_score(_niveau_en_cours: int, _dict_scores: dict) -> str:
    """
    Fonction mettant à jour l'affichage des scores en stockant dans un str l'affichage visible
    sur la droite du jeu.
    ("Niveau x
      1) 7699
      2) ... ").
    :param _niveau_en_cours: le numéro du niveau en cours
    :param _dict_scores: le dictionnaire pour stockant les scores
    :return str: Le str contenant l'affichage pour les scores ("\n" pour passer à la ligne)
    """
    str_score = f"Niveau {_niveau_en_cours}\n"
    if _niveau_en_cours in _dict_scores:
        for i in range(len(_dict_scores[_niveau_en_cours])):
            str_score += f"{i + 1}) {_dict_scores[_niveau_en_cours][i]}\n"
    return str_score
    

def calcule_score(_temps_initial: float, _temps_restant: float) -> float:
    """
    calcule le score du joueur : temps initial - temps restant
    -------- Appelé par enregistre_score ----------
    :param _temps_restant:
    :param _temps_initial: debut du jeu
    :return: le score du joueur
    """
    return round(_temps_initial - _temps_restant, 2)


def enregistre_score(_temps_niveau: float, _temps_initial: float, _dict_scores: dict, _niveau_en_cours: int):
    """
    Fonction enregistrant un nouveau score réalisé par le joueur.
    :param _temps_niveau: le temps qu'il reste à la fin du niveau
    :param _temps_initial: le temps initial du niveau
    :param _dict_scores: Le dictionnaire stockant les scores
    :param _niveau_en_cours: Le numéro du niveau en cours
    """
    score = calcule_score(_temps_initial, _temps_niveau)
    if _niveau_en_cours not in _dict_scores.keys():
        _dict_scores[_niveau_en_cours] = [score]
    else:
        _dict_scores[_niveau_en_cours].append(score)

def update_score_file(_scores_file_path: str, _dict_scores: dict):
    """
    Fonction sauvegardant tous les scores dans le fichier.txt. Celle-ci est appelée à la fermeture de l'application.
    :param _scores_file_path: le chemin d'accès du fichier de stockage des scores
    :param _dict_scores: Le dictionnaire stockant les scores
    """
    with open(_scores_file_path, "w") as fichier:
        for i in _dict_scores.keys():
            print(i)


if __name__ == '__main__':
    simulateur.simulate()