"""Sons et musique, générés par le code (aucun fichier audio nécessaire)."""

import array
import math
import random

import pygame

pygame.init()  # sans effet si pygame est déjà initialisé

try:
    pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
    SON_ACTIF = True
except Exception:
    SON_ACTIF = False


def creer_son(frequence, duree_ms, volume=0.3, bruit=False):
    if not SON_ACTIF:
        return None

    try:
        infos = pygame.mixer.get_init()
        if not infos:
            return None

        frequence_echantillonnage, format_audio, canaux = infos
        if format_audio != -16 or canaux != 2:
            return None

        nombre = int(frequence_echantillonnage * duree_ms / 1000)
        buffer_audio = array.array("h")

        for i in range(nombre):
            if bruit:
                valeur = random.uniform(-1, 1)
            else:
                valeur = math.sin(
                    2 * math.pi * frequence * i / frequence_echantillonnage
                )

            echantillon = int(valeur * volume * 32767)
            buffer_audio.append(echantillon)
            buffer_audio.append(echantillon)

        return pygame.mixer.Sound(buffer=buffer_audio.tobytes())
    except Exception:
        return None


def creer_musique_ambiante():
    """Crée une boucle sonore douce sans fichier externe."""
    if not SON_ACTIF:
        return None

    try:
        infos = pygame.mixer.get_init()
        if not infos:
            return None

        frequence_echantillonnage, format_audio, canaux = infos
        if format_audio != -16 or canaux != 2:
            return None

        duree_secondes = 4
        nombre = frequence_echantillonnage * duree_secondes
        buffer_audio = array.array("h")

        for i in range(nombre):
            temps = i / frequence_echantillonnage
            valeur = (
                0.42 * math.sin(2 * math.pi * 110 * temps)
                + 0.25 * math.sin(2 * math.pi * 165 * temps)
                + 0.15 * math.sin(2 * math.pi * 220 * temps)
            )
            echantillon = int(valeur * 1800)
            buffer_audio.append(echantillon)
            buffer_audio.append(echantillon)

        son = pygame.mixer.Sound(buffer=buffer_audio.tobytes())
        son.set_volume(0.18)
        return son
    except Exception:
        return None


son_python = creer_son(800, 100, 0.35)
son_bug = creer_son(150, 250, 0.4, bruit=True)
musique = creer_musique_ambiante()


def jouer(son):
    if son:
        try:
            son.play()
        except Exception:
            pass
