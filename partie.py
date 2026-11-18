"""La logique d'une partie : score, vies, niveaux, collisions."""

import math
import random

import pygame

from config import (
    WIDTH, HEIGHT, DIFFICULTES,
    NEON_BLEU, NEON_ROSE, JAUNE,
)
from audio import jouer, son_python, son_bug
from entites import Joueur, Objet, Particule
from sauvegarde import sauver_meilleur_score


class Partie:
    def __init__(self, meilleur, difficulte="normal"):
        self.joueur = Joueur()
        self.objets = []
        self.particules = []
        self.score = 0
        self.vies = 3
        self.niveau = 1
        self.target_x = WIDTH // 2
        self.spawn_timer = 0
        self.meilleur = meilleur
        self.etat = "jeu"
        self.fin_temps = 0

        self.shield_timer = 0
        self.combo = 0
        self.combo_timer = 0
        self.difficulte = difficulte

        reglages = DIFFICULTES.get(difficulte, DIFFICULTES["normal"])
        self.mult_vitesse, self.mult_spawn = reglages

    def update(self):
        self.joueur.deplacer(self.target_x)

        if self.shield_timer > 0:
            self.shield_timer -= 1

        if self.combo_timer > 0:
            self.combo_timer -= 1
            if self.combo_timer == 0:
                self.combo = 0

        self.spawn_timer += 1
        delai_spawn = max(
            8,
            int((30 - self.niveau * 2) * self.mult_spawn),
        )

        if self.spawn_timer > delai_spawn:
            self.spawn_timer = 0

            if self.score > 30 and random.random() < 0.12:
                self.objets.append(
                    Objet("shield", self.mult_vitesse)
                )
            else:
                type_objet = "python" if random.random() > 0.4 else "bug"
                self.objets.append(
                    Objet(type_objet, self.mult_vitesse)
                )

        for objet in self.objets[:]:
            objet.update()

            distance = math.hypot(
                objet.x - self.joueur.x,
                objet.y - self.joueur.y,
            )

            if distance < self.joueur.taille + objet.rayon:
                if objet.type == "python":
                    self.score += 10 + self.combo * 2
                    self.combo += 1
                    self.combo_timer = 90
                    jouer(son_python)

                    for _ in range(10):
                        self.particules.append(
                            Particule(objet.x, objet.y, JAUNE)
                        )

                elif objet.type == "bug":
                    if self.shield_timer > 0:
                        self.score += 5
                        jouer(son_python)
                    else:
                        self.vies -= 1
                        jouer(son_bug)

                    self.combo = 0
                    self.combo_timer = 0

                    for _ in range(15):
                        self.particules.append(
                            Particule(objet.x, objet.y, NEON_ROSE)
                        )

                elif objet.type == "shield":
                    self.shield_timer = 240
                    self.score += 20
                    jouer(son_python)

                    for _ in range(20):
                        self.particules.append(
                            Particule(objet.x, objet.y, NEON_BLEU)
                        )

                self.objets.remove(objet)

            elif objet.y > HEIGHT + 30:
                self.objets.remove(objet)

        for particule in self.particules[:]:
            particule.update()
            if particule.vie <= 0:
                self.particules.remove(particule)

        self.niveau = 1 + self.score // 100

        if self.vies <= 0 and self.etat != "fin":
            if self.score > self.meilleur:
                self.meilleur = self.score
                sauver_meilleur_score(self.score)

            self.etat = "fin"
            self.fin_temps = pygame.time.get_ticks()
