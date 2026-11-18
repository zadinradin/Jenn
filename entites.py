"""Les objets du jeu : le joueur, les objets qui tombent et les particules."""

import math
import random

import pygame

from config import (
    WIDTH, HEIGHT,
    FOND, BLEU_FONCE, NEON_BLEU, NEON_ROSE, BLANC, JAUNE,
)
from ui import screen, texte, font_small


class Joueur:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT - 100
        self.taille = 30
        self.vitesse = 7

    def deplacer(self, cible_x):
        cible_x = max(self.taille, min(WIDTH - self.taille, cible_x))

        if abs(self.x - cible_x) > self.vitesse:
            if self.x < cible_x:
                self.x += self.vitesse
            else:
                self.x -= self.vitesse
        else:
            self.x = cible_x

    def dessiner(self, bouclier_actif=False):
        temps = pygame.time.get_ticks()
        flottement = math.sin(temps / 140) * 3
        y = int(self.y + flottement)
        x = int(self.x)

        # Petite flamme animée sous le vaisseau
        longueur_flamme = 8 + int((temps // 100) % 5)
        pygame.draw.polygon(
            screen,
            NEON_ROSE,
            [
                (x - 8, y + 20),
                (x + 8, y + 20),
                (x, y + 20 + longueur_flamme),
            ],
        )
        pygame.draw.polygon(
            screen,
            JAUNE,
            [
                (x - 4, y + 20),
                (x + 4, y + 20),
                (x, y + 17 + longueur_flamme),
            ],
        )

        points = [
            (x, y - self.taille),
            (x - self.taille, y + self.taille),
            (x + self.taille, y + self.taille),
        ]

        pygame.draw.polygon(screen, BLEU_FONCE, points, 8)
        pygame.draw.polygon(screen, NEON_BLEU, points)
        pygame.draw.polygon(screen, BLANC, points, 2)
        pygame.draw.circle(screen, BLANC, (x, y + 8), 4)

        if bouclier_actif:
            pygame.draw.circle(screen, NEON_BLEU, (x, y), 43, 2)
            pygame.draw.circle(screen, (40, 120, 170), (x, y), 48, 1)


class Objet:
    def __init__(self, type_objet, multiplicateur_vitesse=1.0):
        self.x = random.randint(22, WIDTH - 22)
        self.y = -25
        self.type = type_objet
        self.vitesse = random.uniform(3, 6) * multiplicateur_vitesse

        if type_objet == "bug":
            self.couleur = NEON_ROSE
            self.rayon = 18
        elif type_objet == "shield":
            self.couleur = NEON_BLEU
            self.rayon = 16
        else:
            self.couleur = JAUNE
            self.rayon = 14

    def update(self):
        self.y += self.vitesse

    def dessiner(self):
        x = int(self.x)
        y = int(self.y)

        if self.type == "bug":
            rect = pygame.Rect(
                x - self.rayon,
                y - self.rayon,
                self.rayon * 2,
                self.rayon * 2,
            )
            pygame.draw.rect(screen, self.couleur, rect, border_radius=5)
            pygame.draw.rect(screen, BLANC, rect, 2, border_radius=5)
            pygame.draw.line(screen, BLANC, (x - 8, y - 8), (x + 8, y + 8), 2)
            pygame.draw.line(screen, BLANC, (x + 8, y - 8), (x - 8, y + 8), 2)

        elif self.type == "shield":
            pygame.draw.circle(screen, BLEU_FONCE, (x, y), self.rayon + 4)
            pygame.draw.circle(screen, NEON_BLEU, (x, y), self.rayon)
            pygame.draw.circle(screen, BLANC, (x, y), self.rayon - 5, 2)
            texte("+", font_small, BLANC, centre=(x, y))

        else:
            pygame.draw.circle(screen, (160, 120, 20), (x, y), self.rayon + 3)
            pygame.draw.circle(screen, self.couleur, (x, y), self.rayon)
            texte("Py", font_small, FOND, centre=(x, y))


class Particule:
    def __init__(self, x, y, couleur):
        self.x = x
        self.y = y
        self.vx = random.uniform(-5, 5)
        self.vy = random.uniform(-7, -1)
        self.couleur = couleur
        self.vie = 30

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.2
        self.vie -= 1

    def dessiner(self):
        if self.vie > 0:
            pygame.draw.circle(
                screen,
                self.couleur,
                (int(self.x), int(self.y)),
                3,
            )
