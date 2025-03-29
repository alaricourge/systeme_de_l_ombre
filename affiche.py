import chess
import chess.pgn
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import cairosvg
from PIL import Image
from io import BytesIO
from chess import Move
# CODE 
from recherche_chess import find_party
from analyse_party import *

action='test'
name_white,name_black = "white","black"
if action =="test": 
    df=pd.read_csv('game_data.csv')
    df['move'] = df['move'].apply(lambda x: chess.Move.from_uci(x))
    df['best_move'] = df['best_move'].apply(lambda x: chess.Move.from_uci(x))
else:
    name="grandmother"
    ## Récupération des coups
    coups,name_white,name_black = find_party(name)
    ## ANALYSE
    print('analyse')
    df = analysing_fish(coups)
#transformation en liste
moves= df.move.to_list()
best_moves = df.best_move.to_list()

# transformation de chiffre en position dans une matrice
def number_to_position(n):
    x = n // 8
    y = n % 8
    return 7-x,y 

# accuracy de la partie 
print('accuracy: ',df.accurate.mean())
# accuracy par joueur
print('accuracy white '+name_white+' : ',df[df.move_number%2==0].accurate.mean())
print('accuracy black '+name_black+' : ',df[df.move_number%2==1].accurate.mean())

# Récupération de la liste des coups
board = chess.Board()
current_move = -1  # Indice du coup

# AFFICHAGE DE LA COURBE DE LA PARTIE
plt.figure(figsize=(8,4))
plt.plot(df["evaluation"], color='black')
plt.yscale("symlog", linthresh=10)
plt.fill_between(df.index, df["evaluation"], np.max(df["evaluation"]), color='#0000', alpha=1)
plt.yticks([np.min(df["evaluation"]), np.max(df["evaluation"])], [ name_white, name_black], fontsize=12,fontweight="bold")  
plt.title("Évaluation de la position")
plt.xlabel("Coup")
plt.ylabel("Évaluation")
plt.grid(True)





fig, ax = plt.subplots(figsize=(5, 5))

def update_board():
    global current_move
    board.reset()
    for i in range(current_move + 1):
        board.push(moves[i])
    
    # Générer l'échiquier
    board_svg = chess.svg.board(board=board, size=350)
    img = cairosvg.svg2png(bytestring=board_svg)
    img = Image.open(BytesIO(img))
    
    ax.clear()
    ax.imshow(img)
    ax.set_xticks([])
    ax.set_yticks([])
    rate_coup=""
    if current_move > 0:
        if current_move%2==0:
            rate_coup=eval_rise(df.evaluation[current_move]-df.evaluation[current_move-1])
        else:
            rate_coup=eval_rise(-df.evaluation[current_move]+df.evaluation[current_move-1])
        real_title_text = str(current_move)+" : "+rate_coup+"\n"+str(df.str_reply[current_move-1])
    title_text = "Chess" if current_move <= 0 else real_title_text
    ax.set_title(title_text, fontsize=14, fontweight='bold')

    # Dessiner une flèche
    start, end = best_moves[current_move].from_square, best_moves[current_move].to_square
    start = number_to_position(start)
    end = number_to_position(end)
    start_x, start_y = 32+40*start[1],32+40*start[0]
    end_x, end_y = 32+40*end[1],32+40*end[0]
    ax.annotate("", xy=(end_x, end_y), xytext=(start_x, start_y),
                arrowprops=dict(arrowstyle="->", lw=5, color="red"))

    plt.draw()

# Boutons de navigation
def next_move(event):
    global current_move
    if current_move < len(moves) - 1:
        current_move += 1
        update_board()

def prev_move(event):
    global current_move
    if current_move >= 0:
        current_move -= 1
        update_board()



ax_prev = plt.axes([0.1, 0.01, 0.15, 0.075])
ax_next = plt.axes([0.75, 0.01, 0.15, 0.075])
btn_prev = Button(ax_prev, '⬅ Précédent')
btn_next = Button(ax_next, 'Suivant ➡')

btn_prev.on_clicked(prev_move)
btn_next.on_clicked(next_move)

update_board()
plt.show()
