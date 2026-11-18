"""Affichage : fenêtre, textes, fond étoilé, boutons et écrans."""

import random

import pygame

from config import (
    WIDTH, HEIGHT, FPS,
    FOND, NEON_BLEU, NEON_ROSE, BLANC, JAUNE, GRIS,
)

# --- INITIALISATION DE LA FENÊTRE ---
pygame.init()

try:
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)
except Exception:
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("JENN DODGE")

font_titre = pygame.font.Font(None, 52)
font_big = pygame.font.Font(None, 40)
font_small = pygame.font.Font(None, 25)


def texte(message, font, couleur, centre=None, topleft=None):
    surface = font.render(message, True, couleur)
    rect = surface.get_rect()

    if centre is not None:
        rect.center = centre
    elif topleft is not None:
        rect.topleft = topleft

    screen.blit(surface, rect)


# --- FOND ÉTOILÉ ---
ETOILES = [
    (
        random.randint(0, WIDTH),
        random.randint(0, HEIGHT),
        random.choice((1, 1, 2)),
        random.uniform(20, 70),
    )
    for _ in range(50)
]


def dessiner_fond():
    screen.fill(FOND)
    temps = pygame.time.get_ticks() / 1000

    decalage = int(temps * 20) % 40
    for y in range(-40, HEIGHT + 40, 40):
        pygame.draw.line(
            screen,
            (30, 41, 59),
            (0, y + decalage),
            (WIDTH, y + decalage),
            1,
        )

    for x, y, taille, vitesse in ETOILES:
        position_y = int((y + temps * vitesse) % HEIGHT)
        pygame.draw.circle(
            screen,
            (120, 160, 190),
            (x, position_y),
            taille,
        )


# --- ÉLÉMENTS DE BASE ---
def dessiner_coeur(x, y, taille, couleur, plein=True):
    if plein:
        pygame.draw.circle(screen, couleur, (x - taille // 2, y), taille // 2 + 1)
        pygame.draw.circle(screen, couleur, (x + taille // 2, y), taille // 2 + 1)
        pygame.draw.polygon(
            screen,
            couleur,
            [
                (x - taille, y + 2),
                (x + taille, y + 2),
                (x, y + taille + 3),
            ],
        )
    else:
        points = [
            (x - taille, y + 1),
            (x - taille // 2, y - taille // 2),
            (x, y - 2),
            (x + taille // 2, y - taille // 2),
            (x + taille, y + 1),
            (x, y + taille + 3),
        ]
        pygame.draw.lines(screen, (100, 116, 139), True, points, 2)


def dessiner_bouton(rect, label, couleur, font=font_big):
    pygame.draw.rect(screen, couleur, rect, border_radius=12)
    pygame.draw.rect(screen, BLANC, rect, 2, border_radius=12)
    texte(label, font, BLANC, centre=rect.center)


def dessiner_voile():
    surface = pygame.Surface((WIDTH, HEIGHT))
    surface.set_alpha(205)
    surface.fill(FOND)
    screen.blit(surface, (0, 0))


# --- ÉCRANS ---
def dessiner_accueil(bouton_jouer, bouton_musique, musique_active):
    dessiner_fond()

    pygame.draw.circle(screen, (24, 55, 78), (WIDTH // 2, 220), 105, 2)
    pygame.draw.circle(screen, (24, 55, 78), (WIDTH // 2, 220), 78, 2)

    texte("JENN DODGE", font_titre, (14, 116, 160),
          centre=(WIDTH // 2 + 3, 195))
    texte("JENN DODGE", font_titre, NEON_BLEU,
          centre=(WIDTH // 2, 192))

    texte("ÉVITE LES BUGS !", font_small, NEON_ROSE,
          centre=(WIDTH // 2, 275))
    texte("Attrape les objets Py jaunes", font_small, BLANC,
          centre=(WIDTH // 2, 315))

    dessiner_bouton(bouton_jouer, "JOUER", NEON_BLEU)

    etiquette = "MUSIQUE : ON" if musique_active else "MUSIQUE : OFF"
    dessiner_bouton(bouton_musique, etiquette, GRIS, font_small)

    texte("Clique ou glisse pour bouger", font_small, BLANC,
          centre=(WIDTH // 2, HEIGHT - 75))


def dessiner_choix_difficulte(boutons):
    dessiner_fond()
    texte("DIFFICULTÉ", font_titre, NEON_BLEU,
          centre=(WIDTH // 2, 150))
    texte("Choisis ton défi", font_small, BLANC,
          centre=(WIDTH // 2, 190))

    dessiner_bouton(boutons["facile"], "FACILE", (40, 150, 90))
    dessiner_bouton(boutons["normal"], "NORMAL", (40, 110, 170))
    dessiner_bouton(boutons["difficile"], "DIFFICILE", (170, 60, 90))


def dessiner_jeu(partie, pause_rect):
    dessiner_fond()

    for objet in partie.objets:
        objet.dessiner()

    for particule in partie.particules:
        particule.dessiner()

    partie.joueur.dessiner(partie.shield_timer > 0)

    texte(f"SCORE {partie.score}", font_big, BLANC, topleft=(12, 12))
    texte(f"RECORD {partie.meilleur}", font_small, JAUNE, topleft=(14, 50))
    texte(f"NIV {partie.niveau}", font_small, NEON_BLEU, topleft=(14, 76))

    if partie.combo > 1:
        texte(f"COMBO x{partie.combo}", font_small, JAUNE,
              topleft=(14, 103))

    if partie.shield_timer > 0:
        secondes = (partie.shield_timer + FPS - 1) // FPS
        texte(f"BOUCLIER {secondes}s", font_small, NEON_BLEU,
              topleft=(14, 130))

    # Trois emplacements de vie : les vies perdues restent visibles en contour.
    for i in range(3):
        couleur = NEON_ROSE if i < partie.vies else (100, 116, 139)
        dessiner_coeur(WIDTH - 94 + i * 28, 29, 10, couleur,
                       plein=i < partie.vies)

    pygame.draw.rect(screen, GRIS, pause_rect, border_radius=8)
    cx, cy = pause_rect.center
    pygame.draw.rect(screen, BLANC, (cx - 7, cy - 8, 5, 16))
    pygame.draw.rect(screen, BLANC, (cx + 2, cy - 8, 5, 16))


def dessiner_pause(bouton_reprendre, bouton_recommencer, bouton_menu,
                   bouton_musique, musique_active):
    dessiner_voile()
    texte("PAUSE", font_titre, BLANC, centre=(WIDTH // 2, 235))

    dessiner_bouton(bouton_reprendre, "REPRENDRE", NEON_BLEU, font_small)
    dessiner_bouton(bouton_recommencer, "RECOMMENCER", (40, 110, 170),
                    font_small)
    dessiner_bouton(bouton_menu, "MENU", (170, 60, 90), font_small)

    etiquette = "MUSIQUE : ON" if musique_active else "MUSIQUE : OFF"
    dessiner_bouton(bouton_musique, etiquette, GRIS, font_small)


def dessiner_fin(partie, bouton_rejouer, bouton_menu):
    dessiner_voile()
    texte("PARTIE TERMINÉE", font_big, NEON_ROSE,
          centre=(WIDTH // 2, 300))
    texte(f"Score : {partie.score}", font_small, BLANC,
          centre=(WIDTH // 2, 345))
    texte(f"Record : {partie.meilleur}", font_small, JAUNE,
          centre=(WIDTH // 2, 375))

    dessiner_bouton(bouton_rejouer, "REJOUER", NEON_BLEU, font_small)
    dessiner_bouton(bouton_menu, "MENU", (170, 60, 90), font_small)
