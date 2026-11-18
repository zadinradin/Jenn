"""Réglages généraux du jeu : dimensions, couleurs, difficultés."""

WIDTH, HEIGHT = 400, 700
FPS = 60

# --- COULEURS ---
FOND = (15, 23, 42)
BLEU_FONCE = (14, 85, 125)
NEON_BLEU = (56, 189, 248)
NEON_ROSE = (244, 114, 182)
BLANC = (255, 255, 255)
JAUNE = (250, 204, 21)
VERT = (74, 222, 128)
GRIS = (51, 65, 85)

# --- DIFFICULTÉS ---
# nom : (multiplicateur de vitesse des objets, multiplicateur du délai d'apparition)
# Un délai plus petit = plus d'objets qui tombent.
DIFFICULTES = {
    "facile": (0.8, 1.2),
    "normal": (1.0, 1.0),
    "difficile": (1.35, 0.8),
}
