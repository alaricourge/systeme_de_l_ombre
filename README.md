# Chess Analyzer

## Description

Chess Analyzer est un outil permettant d’analyser automatiquement la dernière partie d’échecs jouée par un utilisateur en ligne. Il utilise Selenium pour récupérer la partie, puis Stockfish pour l’analyser en fournissant les meilleurs coups et l’avantage des joueurs au fil de la partie. Enfin, il affiche une courbe d’évaluation de la partie pour visualiser son déroulement.

## Fonctionnalités

- **Récupération automatique** : Obtient la dernière partie jouée à partir du nom d’utilisateur.
- **Analyse avec Stockfish** : Détermine les meilleurs coups possibles à chaque tour et l’évaluation de la position.
- **Visualisation des résultats** : Affiche une courbe d’évaluation de la partie.

## Prérequis

Avant de commencer, assure-toi d’avoir installé :

- **Python** (>= 3.8)
- **Selenium**
- **Stockfish**
- **Matplotlib** (pour la courbe d’évaluation)

Installation des dépendances :
```bash
pip install selenium matplotlib
```

Assure-toi également d’avoir Stockfish installé et accessible dans ton système.

## Installation

1. Clone ce dépôt :
```bash
git clone https://github.com/alaricourge/systeme_de_l_ombre.git
cd chess-analyzer
```
BIENTOT
2. Installe les dépendances :
```bash
pip install -r requirements.txt
```

3. Télécharge et installe **Stockfish** si ce n’est pas déjà fait.


