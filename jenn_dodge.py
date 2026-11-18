import os
import math
import random
import array
import pygame

WIDTH, HEIGHT = 400, 700
FPS = 60

# --- SAUVEGARDE LOCALE ---
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


# --- INITIALISATION PYGAME ---
pygame.init()

try:
    pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
    SON_ACTIF = True
except Exception:
    SON_ACTIF = False

try:
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)
except Exception:
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("JENN DODGE")
clock = pygame.time.Clock()

# --- COULEURS ---
FOND = (15, 23, 42)
BLEU_FONCE = (14, 85, 125)
NEON_BLEU = (56, 189, 248)
NEON_ROSE = (244, 114, 182)
BLANC = (255, 255, 255)
JAUNE = (250, 204, 21)
VERT = (74, 222, 128)
GRIS = (51, 65, 85)

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


# --- SONS ---
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


# --- DESSIN DES VIES ---
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


# --- OBJETS DU JEU ---
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


# --- PARTIE ---
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

        if difficulte == "facile":
            self.mult_vitesse = 0.8
            self.mult_spawn = 1.2
        elif difficulte == "difficile":
            self.mult_vitesse = 1.35
            self.mult_spawn = 0.8
        else:
            self.mult_vitesse = 1.0
            self.mult_spawn = 1.0

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


# --- BOUTONS ET MENUS ---
def dessiner_bouton(rect, label, couleur, font=font_big):
    pygame.draw.rect(screen, couleur, rect, border_radius=12)
    pygame.draw.rect(screen, BLANC, rect, 2, border_radius=12)
    texte(label, font, BLANC, centre=rect.center)


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


def dessiner_voile():
    surface = pygame.Surface((WIDTH, HEIGHT))
    surface.set_alpha(205)
    surface.fill(FOND)
    screen.blit(surface, (0, 0))


# --- BOUCLE PRINCIPALE ---
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
            dessiner_accueil(
                bouton_jouer,
                bouton_musique,
                musique_active,
            )

        elif ecran == "difficulte":
            dessiner_choix_difficulte(boutons_difficulte)

        else:
            dessiner_jeu(partie, pause_rect)

            if partie.etat == "pause":
                dessiner_voile()
                texte("PAUSE", font_titre, BLANC,
                      centre=(WIDTH // 2, 235))

                dessiner_bouton(bouton_reprendre, "REPRENDRE", NEON_BLEU,
                                font_small)
                dessiner_bouton(bouton_recommencer, "RECOMMENCER", (40, 110, 170),
                                font_small)
                dessiner_bouton(bouton_menu_pause, "MENU", (170, 60, 90),
                                font_small)

                etiquette = "MUSIQUE : ON" if musique_active else "MUSIQUE : OFF"
                dessiner_bouton(bouton_musique_pause, etiquette, GRIS,
                                font_small)

            elif partie.etat == "fin":
                dessiner_voile()
                texte("PARTIE TERMINÉE", font_big, NEON_ROSE,
                      centre=(WIDTH // 2, 300))
                texte(f"Score : {partie.score}", font_small, BLANC,
                      centre=(WIDTH // 2, 345))
                texte(f"Record : {partie.meilleur}", font_small, JAUNE,
                      centre=(WIDTH // 2, 375))

                dessiner_bouton(bouton_rejouer, "REJOUER", NEON_BLEU,
                                font_small)
                dessiner_bouton(bouton_menu_fin, "MENU", (170, 60, 90),
                                font_small)

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
    