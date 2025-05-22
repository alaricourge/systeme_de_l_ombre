import numpy as np
import random

class case:
    letters=['a','b','c','d','e','f','g','h']
    letter_to_index = {letter: idx+1 for idx, letter in enumerate(letters)}
    index_to_letter = {idx+1: letter for idx, letter in enumerate(letters)}


    def __init__(self, x, y):
        if y is None:
            # Un seul argument, peut-être une string genre 'e4'
            if isinstance(x, str):
                x = x.strip().lower()
                if len(x) == 2 and x[0] in self.letters and x[1].isdigit():
                    self.x = self.letter_to_index[x[0]]
                    self.y = int(x[1])
                else:
                    raise ValueError(f"Format invalide pour une case : '{x}'")
            else:
                raise TypeError("Argument invalide pour la case")
        else:
            # Deux arguments, vérifier les types
            if isinstance(x, str):
                x = x.lower()
                if x in self.letter_to_index:
                    self.x = self.letter_to_index[x]
                else:
                    raise ValueError(f"Lettre invalide : '{x}'")
            elif isinstance(x, int):
                if 1 <= x <= 8:
                    self.x = x
                else:
                    raise ValueError("x doit être entre 1 et 8")
            else:
                raise TypeError("x doit être une lettre ou un entier")

            if isinstance(y, int) and 1 <= y <= 8:
                self.y = y
            else:
                raise ValueError("y doit être un entier entre 1 et 8")

    def suivant (self):
        """
        Renvoie les coordonnées des cases accessibles par le cavalier
        """
        # Définition des mouvements possibles du cavalier
        moves = [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)]
        # Liste pour stocker les mouvements valides
        valid_moves = []
        # Parcours de tous les mouvements possibles
        for move in moves:
            new_x = self.x + move[0]
            new_y = self.y + move[1]
            # Vérification si le mouvement est valide
            if 1 <= new_x <= 8 and 1 <= new_y <= 8:
                valid_moves.append(case(new_x, new_y))
        return valid_moves

    def __str__(self):
        return f"({self.letters[self.x-1]},{self.y})"
    def __repr__(self):
        return f"({self.letters[self.x-1]},{self.y})"
    def __eq__(self, other):
        if other is str:
            split = other.split(",")
            print(split)
            return self.x == int(split[0]) and self.y == int(split[1])
        if isinstance(other, case):
            return self.x == other.x and self.y == other.y
        return False
    def __hash__(self):
        return hash((self.x, self.y))

class board:
    letters=['a','b','c','d','e','f','g','h']
    numbers=[1,2,3,4,5,6,7,8]
    cases = []
    for i in numbers:
        for j in numbers:
            cases.append(case(i,j))
    def suivant(self, x, y):
        """
        Renvoie les coordonnées des cases accessibles par le cavalier
        """
        # Définition des mouvements possibles du cavalier
        moves = [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)]
        # Liste pour stocker les mouvements valides
        valid_moves = []
        # Parcours de tous les mouvements possibles
        for move in moves:
            new_x = x + move[0]
            new_y = y + move[1]
            # Vérification si le mouvement est valide
            if 1 <= new_x <= 8 and 1 <= new_y <= 8:
                valid_moves.append((new_x, new_y))
        return valid_moves
    
    def __str__(self):
        string=""

        for i,cas in enumerate(self.cases):
            if i%8==0:
                string+="\n"
            string+=str(cas)


        return string
    def __getitem__(cls, item):
        if isinstance(item, int):
            return cls.cases[item]
        
    
def jeu_next():
    """
    jeu trouve l'un des prochaines postions du cavalier
    """
    boarde = board()
    # print(boarde)
    randomCase=random.randint(0,63)
    print("randomCase",boarde[randomCase])
    #print(case.suivant(boarde[18]))
    a_enlever = case.suivant(boarde[randomCase])
    #print("a_enlever",a_enlever)
    resultat = [t for t in boarde.cases if t not in a_enlever]
    #print("resultat",resultat)

    nautre=random.randint(len(a_enlever),8)
    autres=random.choices(resultat, k=nautre)
    ngood=9-nautre
    good=random.choices(a_enlever, k=ngood)

    total=autres+good
    random.shuffle(total)
    print("to find",total)
    find=[]
    while len(find) < len(good):
        ans = input("Entrez votre coup (ex: 3,4) ou 'q' pour quitter: ")
        if ans == 'q':
            break
        try:
            x_str, y_str = ans.split(',')
            x, y = int(x_str), int(y_str)
            tentative = case(x, y)
            if tentative in good:
                print("Coup valide")
                find.append(tentative)
            else:
                print("Coup invalide")
        except Exception:
            print("Format invalide. Entrez sous forme x,y (ex: 3,4)")


from collections import deque

def iterative_bfs(start_case):
    visited = {}
    queue = deque()
    queue.append((start_case, 0))
    
    while queue:
        current_case, depth = queue.popleft()
        if current_case not in visited:
            visited[current_case] = depth
            for move in current_case.suivant():
                if move not in visited:
                    queue.append((move, depth + 1))
    
    return visited

import matplotlib.pyplot as plt
import matplotlib.patches as patches
def visualize_knight_moves(visited_dict):
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # Trouver la profondeur maximale pour normaliser les couleurs
    max_depth = max(visited_dict.values()) if visited_dict else 1
    
    for x in range(1, 9):
        for y in range(1, 9):
            current_case = case(x, y)
            base_color = 'white' if (x + y) % 2 == 0 else 'lightgray'
            
            # Vérifier si la case a été visitée
            if current_case in visited_dict:
                depth = visited_dict[current_case]
                
                # Calculer la couleur en dégradé vert -> rouge
                # ratio va de 0 (vert pur) à 1 (rouge pur)
                ratio = depth / max_depth
                red = ratio
                green = 1 - ratio
                blue = 0.2  # Un peu de bleu pour adoucir
                
                color = (red, green, blue)
            else:
                color = base_color
            
            # Dessiner la case
            rect = patches.Rectangle((x-0.5, y-0.5), 1, 1, 
                                   linewidth=1, edgecolor='black',
                                   facecolor=color)
            ax.add_patch(rect)
            
            # Ajouter le texte (profondeur)
            if current_case in visited_dict:
                text_color = 'white' if depth > max_depth/2 else 'black'
                plt.text(x, y, str(depth), 
                        ha='center', va='center', 
                        fontsize=10, color=text_color)
    
    # Configuration de l'affichage
    ax.set_xlim(0.5, 8.5)
    ax.set_ylim(0.5, 8.5)
    ax.set_xticks(range(1, 9))
    ax.set_yticks(range(1, 9))
    ax.set_xticklabels(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'])
    ax.set_yticklabels(range(1, 9))
    ax.set_title("Parcours du cavalier (vert = proche, rouge = loin)")
    plt.gca().invert_yaxis()
    plt.grid(True)
    plt.show()


# Initialisation
b = board()
start_case = b[0]  # Case a1

# Calcul du parcours
visited = {}
result = iterative_bfs(start_case)

# Visualisation
visualize_knight_moves(result)