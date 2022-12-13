import os

import time
from PIL import ImageTk as itk
from tkinter import Tk, Canvas, Label, Menu, PhotoImage, Toplevel, Button, LEFT, ALL, StringVar, Entry, messagebox
import threading
import pyChase

LEVEL_FOLDER_PATH: str = os.path.abspath("./niveaux")
SCORE_FILE_PATH: str = os.path.abspath("./scores/scores.txt")
temps_niveau = 59


class Jeu:
    def __init__(self):
        self.nb_coups: int = 0
        self.started: bool = False
        self.score_start: bool = False
        self.niveau_en_cours: int = None
        self.temps_initial: float = temps_niveau
        self.fenetre = None
        self.gauche_presse = False
        self.droite_presse = False
        self.haut_presse = False
        self.bas_presse = False

        self.nb_file: int = 1

        self.joueur: list = []
        self.minotaurs: list = []
        self.cibles: list = []
        self.murs: list = []
        self.carte: list = []

        self.liste_image: list = []

        self.dict_scores: dict = {}
        self.can: Canvas = None
        self.score_label: Label = None

    def refresh(self):
        self.joueur: list = []
        self.minotaurs: list = []
        self.cibles: list = []
        self.murs: list = []
        self.carte: list = []

        self.nb_coups: int = 0
        self.started: bool = False
        self.score_start: bool = False
        self.niveau_en_cours: int = None
        self.temps_initial: float = temps_niveau


def quitter(fenetre: Tk):
    """
    fonction qui ferme l'application
    :param fenetre:
    :return:
    """
    fenetre.quit()
    fenetre.destroy()


def affichage_jeu(jeu: Jeu):
    """
    fonction qui utilise le fichier texte du nom nivo1.txt, pour creer la liste ch du niveau 1
    :param jeu: configuration du jeu
    :return:
    """
    if not jeu.started:
        for j in jeu.murs:
            pyChase.creer_image(jeu.can, j.get_x(), j.get_y(), jeu.liste_image[0])
    for j in jeu.joueur:
        pyChase.creer_image(jeu.can, j.get_x(), j.get_y(), jeu.liste_image[3])
    for j in jeu.cibles:
        pyChase.creer_image(jeu.can, j.get_x(), j.get_y(), jeu.liste_image[1])
    for j in jeu.minotaurs:
        pyChase.creer_image(jeu.can, j.get_x(), j.get_y(), jeu.liste_image[2])
        for c in jeu.cibles:
            if j == c:
                pyChase.creer_image(jeu.can, j.get_x(), j.get_y(), jeu.liste_image[3])



def charger_niveau(jeu: Jeu, path: str):
    """
    charge la configuration du jeu pour un niveau
    :param jeu: configuration du jeu
    :param path: fichier avec la configuration du niveau
    :return:
    """
    jeu.can.delete(ALL)
    jeu.refresh()

    jeu.carte = pyChase.charger_niveau(jeu.carte, jeu.joueur, jeu.minotaurs, jeu.cibles, jeu.murs, path)
    affichage_jeu(jeu)
    jeu.can.bind_all("<Right>", lambda event: droite(jeu))
    jeu.can.bind_all("<KeyRelease-Right>", lambda event: on_release_right(jeu))
    jeu.can.bind_all("<Left>", lambda event: gauche(jeu))
    jeu.can.bind_all("<KeyRelease-Left>", lambda event: on_release_left(jeu))
    jeu.can.bind_all("<Up>", lambda event: haut(jeu))
    jeu.can.bind_all("<KeyRelease-Up>", lambda event: on_release_up(jeu))
    jeu.can.bind_all("<Down>", lambda event: bas(jeu))
    jeu.can.bind_all("<KeyRelease-Down>", lambda event: on_release_down(jeu))
    jeu.can.pack()
    tmp_str: str = path.split("level")[1]
    jeu.niveau_en_cours = int(tmp_str.replace(".txt", ""))
    jeu.started = True
    jeu.stop = False
    jeu.temps_initial = temps_niveau

    if not jeu.t.is_alive():
        jeu.t.start()
    else:
        jeu.temps_niveau = temps_niveau

    refresh_score(jeu)


def popup_aide():
    """
    fonction qui creer une fenetre popup
    :return:
    """
    popup = Toplevel()
    popup.title("Instructions")
    bouton = Button(popup, text="Fermer", command=popup.withdraw)
    bouton.pack()


def load_levels_menu(jeu: Jeu, filemenu: Menu):
    """
    charge les niveaux
    :param jeu: configuration du jeu
    :param filemenu: menu pour charger les niveaux
    :return:
    """
    files: list = [f for f in os.listdir(LEVEL_FOLDER_PATH) if f.endswith(".txt")]
    for i in range(1, len(files) + 1):
        tag: str = "Niveau %s" % i
        path: str = os.path.join(LEVEL_FOLDER_PATH, "level%d.txt" % i)
        filemenu.add_command(label=tag, command=lambda x=path: charger_niveau(jeu, x))


def init_menu(jeu: Jeu, fenetre: Tk):
    menu: Menu = Menu(fenetre)
    fenetre.config(menu=menu)
    filemenu: Menu = Menu(menu)
    menu.add_cascade(label="Choix du niveau", menu=filemenu)
    load_levels_menu(jeu, filemenu)
    menu.add_command(label="Exit", command=lambda: update_score_file(jeu, fenetre))


def check_status(jeu: Jeu):
    if pyChase.jeu_en_cours(jeu.joueur, jeu.temps_niveau) == "fini" and jeu.started:
        jeu.stop = True
        affichage_jeu(jeu)
        save_score(jeu)
        jeu.can.bind_all("<Right>")
        jeu.can.bind_all("<Left>")
        jeu.can.bind_all("<Up>")
        jeu.can.bind_all("<Down>")
        jeu.started = False
    elif pyChase.jeu_en_cours(jeu.joueur, jeu.temps_niveau) == "mort" and jeu.started:
        jeu.stop = True
        affichage_jeu(jeu)
        jeu.can.bind_all("<Right>")
        jeu.can.bind_all("<Left>")
        jeu.can.bind_all("<Up>")
        jeu.can.bind_all("<Down>")
        jeu.started = False
    else:
        affichage_jeu(jeu)


def on_release_right(jeu):
    jeu.droite_presse = False


def on_release_left(jeu):
    jeu.gauche_presse = False


def on_release_up(jeu):
    jeu.haut_presse = False


def on_release_down(jeu):
    jeu.bas_presse = False


def mouvement(jeu: Jeu, direction: str):
    if jeu.started:
        pyChase.definir_mouvement(direction, jeu.can, jeu.joueur, jeu.murs, jeu.minotaurs, jeu.cibles, jeu.carte, jeu.liste_image)
    jeu.nb_coups += 1
    check_status(jeu)


def droite(jeu: Jeu):
    if not jeu.droite_presse:
        mouvement(jeu, "droite")
    jeu.droite_presse = True


def gauche(jeu: Jeu):
    if not jeu.gauche_presse:
        mouvement(jeu, "gauche")
    jeu.gauche_presse = True


def haut(jeu: Jeu):
    if not jeu.haut_presse:
        mouvement(jeu, "haut")
    jeu.haut_presse = True


def bas(jeu: Jeu):
    if not jeu.bas_presse:
        mouvement(jeu, "bas")
    jeu.bas_presse = True


def load_scores(jeu: Jeu):
    pyChase.chargement_score(SCORE_FILE_PATH, jeu.dict_scores)


def refresh_score(jeu: Jeu):
    score_affichage = pyChase.maj_score(jeu.niveau_en_cours, jeu.dict_scores)
    jeu.score_label.config(text=score_affichage)


def save_score(jeu: Jeu):
    pyChase.enregistre_score(jeu.temps_niveau, jeu.temps_initial, jeu.dict_scores, jeu.niveau_en_cours)
    refresh_score(jeu)


def update_score_file(jeu: Jeu, fenetre: Tk):
    pyChase.update_score_file(SCORE_FILE_PATH, jeu.dict_scores)
    quitter(fenetre)


def countdown(jeu: Jeu):
    timeformat = 0
    while jeu.temps_niveau > -99999999:
        if jeu.started != False:
            mins, secs = divmod(jeu.temps_niveau, 60)
            timeformat = '{:.0f}:{:.2f}'.format(mins, secs)
            jeu.my_string_var.set(timeformat)
            time.sleep(0.01)
            jeu.temps_niveau -= 0.015
            if jeu.temps_niveau < 10:
                jeu.time_label.config(fg="Red")
            else:
                jeu.time_label.config(fg="Black")
            if jeu.temps_niveau < 0:
                jeu.my_string_var.set("Fin du temps !")
                jeu.started = False
        else:
            if jeu.my_string_var != timeformat:
                time.sleep(0.5)


def simulate():
    title: str = "Projet 63-11"

    fenetre: Tk = Tk()
    fenetre.title(title)

    # Référence sur les images (obligatoire avec tkinter)
    jpeg_mur = "./images/mur.jpg"
    img_mur: PhotoImage = itk.PhotoImage(file=jpeg_mur)
    jpeg_cible = "./images/dock.jpg"
    img_cible: PhotoImage = itk.PhotoImage(file=jpeg_cible)
    jpeg_mino = "./images/mino.jpg"
    img_mino: PhotoImage = itk.PhotoImage(file=jpeg_mino)
    img_boite_correcte: PhotoImage = PhotoImage(file=os.path.abspath("./images/box_docked.gif"))
    jpeg_joueur = "./images/worker.jpg"
    img_joueur: PhotoImage = itk.PhotoImage(file=jpeg_joueur)
    img_joueur_cible: PhotoImage = PhotoImage(file=os.path.abspath("./images/worker_dock.gif"))
    jpeg_sol = "./images/floor.jpg"
    img_sol: PhotoImage = itk.PhotoImage(file=jpeg_sol)

    jeu: Jeu = Jeu()

    jeu.liste_image.append(img_mur)
    jeu.liste_image.append(img_cible)
    jeu.liste_image.append(img_mino)
    jeu.liste_image.append(img_joueur)
    jeu.liste_image.append(img_sol)

    can: Canvas = Canvas(fenetre, height=760, width=1200, bg="#2d7119")
    can.pack(side=LEFT)
    jeu.can = can
    jeu.fenetre = fenetre
    my_string_var = StringVar(value="")
    time_label: Label = Label(fenetre, anchor="nw", font="Cooper", justify="left", bg="#d8c09e", fg="black",
                              textvariable=my_string_var, height=3, width=17)

    time_label.config(font=("Impact", 30))  # fonte change this to change the font
    time_label.pack()
    score_label: Label = Label(fenetre, anchor="nw", font="Cooper", justify="left", bg="#d8c09e", fg="black",
                               text=load_scores(jeu), height=13, width=38)

    score_label.pack()
    jeu.score_label = score_label
    jeu.time_label = time_label
    jeu.my_string_var = my_string_var
    jeu.temps_niveau = temps_niveau
    jeu.stop = True
    jeu.t = threading.Thread(target=countdown, args=(jeu,), daemon=True)

    init_menu(jeu, fenetre)

    _help: str = """_______________________________________
    
    Règles du jeu
    
    Déplacez le personnage à l'aide des flèches 
    du clavier afin d'arriver jusqu'à la sortie. 
    Le minotaur n'avance que grâce à vos erreurs !'"""

    t: Label = Label(fenetre, anchor="s", font="Cooper", bg="#d8c09e", fg="black", pady="20",
                     text=_help,
                     height=18, width=38)
    t.pack(side=LEFT)
    fenetre.resizable(height=0, width=0)
    fenetre.protocol("WM_DELETE_WINDOW", lambda: update_score_file(jeu, fenetre))
    fenetre.mainloop()