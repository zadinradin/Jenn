"""JENN DODGE : point d'entrée et boucle principale.

Lance le jeu avec :  python jenn_dodge.py
"""

import pygame

from config import WIDTH, FPS
from sauvegarde import lire_meilleur_score
from audio import musique
from partie import Partie
from ui import (
    dessiner_accueil,
    dessiner_choix_difficulte,
    dessiner_jeu,
    dessiner_pause,
    dessiner_fin,
)

clock = pygame.time.Clock()


def main():
    bouton_jouer = pygame.Rect(WIDTH // 2 - 100, 390, 200, 60)
    bouton_musique = pygame.Rect(WIDTH // 2 - 90, 475, 180, 45)

    boutons_difficulte = {
        "facile": pygame.Rect(WIDTH // 2 - 110, 240, 220, 58),
        "normal": pygame.Rect(WIDTH // 2 - 110, 325, 220, 58),
        "difficile": pygame.Rect(WIDTH // 2 - 110, 410, 220, 58),
    }

    pause_rect = pygame.Rect(WIDTH - 50, 60, 35, 35)
    bouton_reprendre = pygame.Rect(WIDTH // 2 - 105, 310, 210, 52)
    bouton_recommencer = pygame.Rect(WIDTH // 2 - 105, 380, 210, 52)
    bouton_menu_pause = pygame.Rect(WIDTH // 2 - 105, 450, 210, 52)
    bouton_musique_pause = pygame.Rect(WIDTH // 2 - 95, 520, 190, 42)

    bouton_rejouer = pygame.Rect(WIDTH // 2 - 105, 420, 210, 52)
    bouton_menu_fin = pygame.Rect(WIDTH // 2 - 105, 490, 210, 52)

    ecran = "accueil"
    difficulte = "normal"
    partie = Partie(lire_meilleur_score(), difficulte)
    musique_active = False

    def basculer_musique():
        nonlocal musique_active

        if musique is None:
            musique_active = False
            return

        musique_active = not musique_active
        if musique_active:
            musique.play(-1)
        else:
            musique.stop()

    while True:
        tap = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if musique:
                    musique.stop()
                pygame.quit()
                return

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if ecran == "jeu" and partie.etat == "jeu":
                    partie.etat = "pause"
                elif ecran == "jeu" and partie.etat == "pause":
                    partie.etat = "jeu"

            if event.type == pygame.MOUSEBUTTONDOWN:
                tap = event.pos

        # --- LOGIQUE ---
        if ecran == "accueil":
            if tap and bouton_jouer.collidepoint(tap):
                ecran = "difficulte"
            elif tap and bouton_musique.collidepoint(tap):
                basculer_musique()

        elif ecran == "difficulte":
            if tap:
                for nom, rect in boutons_difficulte.items():
                    if rect.collidepoint(tap):
                        difficulte = nom
                        partie = Partie(lire_meilleur_score(), difficulte)
                        ecran = "jeu"
                        break

        elif ecran == "jeu" and partie.etat == "jeu":
            if tap:
                if pause_rect.collidepoint(tap):
                    partie.etat = "pause"
                else:
                    partie.target_x = tap[0]

            # Tant que la souris est maintenue, le joueur suit sa position.
            boutons_souris = pygame.mouse.get_pressed()
            if boutons_souris[0]:
                position_souris = pygame.mouse.get_pos()
                partie.target_x = position_souris[0]

            partie.update()

        elif ecran == "jeu" and partie.etat == "pause":
            if tap:
                if bouton_reprendre.collidepoint(tap):
                    partie.etat = "jeu"
                elif bouton_recommencer.collidepoint(tap):
                    partie = Partie(lire_meilleur_score(), difficulte)
                elif bouton_menu_pause.collidepoint(tap):
                    ecran = "accueil"
                elif bouton_musique_pause.collidepoint(tap):
                    basculer_musique()

        elif ecran == "jeu" and partie.etat == "fin":
            if tap and bouton_rejouer.collidepoint(tap):
                partie = Partie(lire_meilleur_score(), difficulte)
            elif tap and bouton_menu_fin.collidepoint(tap):
                ecran = "accueil"

        # --- DESSIN ---
        if ecran == "accueil":
            dessiner_accueil(bouton_jouer, bouton_musique, musique_active)

        elif ecran == "difficulte":
            dessiner_choix_difficulte(boutons_difficulte)

        else:
            dessiner_jeu(partie, pause_rect)

            if partie.etat == "pause":
                dessiner_pause(
                    bouton_reprendre,
                    bouton_recommencer,
                    bouton_menu_pause,
                    bouton_musique_pause,
                    musique_active,
                )
            elif partie.etat == "fin":
                dessiner_fin(partie, bouton_rejouer, bouton_menu_fin)

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
