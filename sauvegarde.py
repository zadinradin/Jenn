"""Sauvegarde locale du meilleur score."""

import os


def dossier_donnees():
    dossier_android = os.environ.get("ANDROID_PRIVATE")
    if dossier_android and os.path.isdir(dossier_android):
        return dossier_android

    try:
        return os.path.dirname(os.path.abspath(__file__))
    except Exception:
        return os.getcwd()


SCORE_FILE = os.path.join(dossier_donnees(), "meilleur_score.txt")


def lire_meilleur_score():
    try:
        with open(SCORE_FILE, "r") as fichier:
            return int(fichier.read())
    except Exception:
        return 0


def sauver_meilleur_score(score):
    try:
        with open(SCORE_FILE, "w") as fichier:
            fichier.write(str(score))
    except Exception:
        pass
