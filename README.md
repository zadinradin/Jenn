## Structure du projet

```
Jenn/
├── jenn_dodge.py   # point d'entrée et boucle principale
├── config.py       # dimensions, couleurs, difficultés
├── partie.py       # logique du jeu : score, vies, niveaux, collisions
├── entites.py      # vaisseau, objets qui tombent, particules
├── ui.py           # fenêtre, menus, boutons, affichage
├── audio.py        # sons et musique (générés par le code)
└── sauvegarde.py   # meilleur score
```

## Où modifier quoi ?

| Je veux... | Fichier |
|---|---|
| Changer la difficulté ou les couleurs | `config.py` |
| Ajouter un type d'objet ou de bonus | `entites.py` et `partie.py` |
| Modifier les menus ou l'affichage | `ui.py` |
| Changer les sons | `audio.py` |# 🚀 Jenn Dodge

Un jeu d'arcade en Python (Pygame). Pilote ton vaisseau, attrape les objets **Py** jaunes et évite les **bugs** !

## Gameplay

- 🟡 **Py** : +10 points, et des combos pour multiplier le score
- 🟥 **Bug** : fait perdre une vie (3 vies au total)
- 🔵 **Bouclier** : protège des bugs pendant quelques secondes
- 3 niveaux de difficulté : facile, normal, difficile
- Le meilleur score est sauvegardé automatiquement

## Installation

```
pip install pygame
python jenn_dodge.py
```

## Commandes

- Clic ou glisser : déplacer le vaisseau
- Échap ou bouton ⏸ : pause

## Contribuer

Les contributions sont les bienvenues ! Ouvre une **issue** pour signaler un bug
ou proposer une idée, ou une **pull request** pour proposer une modification.

Idées d'amélioration : nouveaux objets, boss, vrais sons et musiques,
classement en ligne, version Android.

## Licence

MIT
