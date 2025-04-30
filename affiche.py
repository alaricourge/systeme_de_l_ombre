import chess
import chess.pgn
from chess import Move
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import os

#import cairosvg
from PIL import Image
from io import BytesIO
# CODE 
from recherche_chess import find_party
from analyse_party import *

current_move = -1  # Indice du coup

def number_to_position(n):
    x = n // 8
    y = n % 8
    return 7-x,y 

def courbe_partie(df,name_white,name_black):
    plt.figure(figsize=(8,4))
    plt.plot(df["evaluation"], color='black')
    plt.yscale("symlog", linthresh=10)
    plt.fill_between(df.index, df["evaluation"], np.max(df["evaluation"]), color='#0000', alpha=1)
    plt.yticks([np.min(df["evaluation"]), np.max(df["evaluation"])], [ name_white, name_black], fontsize=12,fontweight="bold")  
    plt.title("Évaluation de la position")
    plt.xlabel("Coup")
    plt.ylabel("Évaluation")
    plt.grid(True)

def draw_board(ax, board):

    piece_dir = "pieces/" 
    colors = ["#F0D9B5", "#B58863"]
    square_size = 1

    for i in range(8):
        for j in range(8):
            color = colors[(i + j) % 2]
            rect = plt.Rectangle((j, 7 - i), square_size, square_size, facecolor=color)
            ax.add_patch(rect)

            square = chess.square(j, i)
            piece = board.piece_at(square)
            if piece:
                img_path = os.path.join(piece_dir, f"{piece.color and 'w' or 'b'}{piece.symbol().lower()}.png")
                image = Image.open(img_path).convert("RGBA")
                # if piece king zoom =0.015
                if img_path == "pieces/wk.png":
                    zoom = 0.015
                elif img_path == "pieces/bk.png":
                    zoom = 0.015
                else:
                    zoom = 0.03
                imagebox = OffsetImage(image, zoom=zoom)
                ab = AnnotationBbox(imagebox, (j + 0.5, 7 - i + 0.5), frameon=False)
                ax.add_artist(ab)
                

def update_board():
    global current_move
    board.reset()
    for i in range(current_move + 1):
        board.push(moves[i])

    ax.clear()
    draw_board(ax, board)
    ax.set_xlim(0, 8)
    ax.set_ylim(0, 8)
    ax.set_xticks([])
    ax.set_yticks([])

    # Évaluer le coup
    rate_coup = ""
    if current_move > 0:
        delta = df.evaluation[current_move] - df.evaluation[current_move - 1]
        rate_coup = eval_rise(delta if current_move % 2 == 0 else -delta)
        real_title_text = mat_en(df.reply[current_move]) + str(current_move) + " : " + rate_coup + "\n" + str(df.str_reply[current_move - 1])
    title_text = "Chess" if current_move <= 0 else real_title_text
    ax.set_title(title_text, fontsize=14, fontweight='bold')

    # Dessiner une flèche
    start, end = best_moves[current_move].from_square, best_moves[current_move].to_square
    start_pos = (chess.square_file(start), 7 - chess.square_rank(start))
    end_pos = (chess.square_file(end), 7 - chess.square_rank(end))

    ax.annotate("", xy=(end_pos[0]+0.5, end_pos[1]+0.5), xytext=(start_pos[0]+0.5, start_pos[1]+0.5),
                arrowprops=dict(arrowstyle="->", lw=2, color="red"))

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

if __name__ == "__main__":
    action='test'
    name_white,name_black = "white","black"
    ## DEFLAUT 
    if action =="test": 
        df=pd.read_csv('game_data.csv')
        df['move'] = df['move'].apply(lambda x: chess.Move.from_uci(x))
        df['best_move'] = df['best_move'].apply(lambda x: chess.Move.from_uci(x))
    # REAL
    else:
        ### PUT YOUR NAME HERE ###
        # frouty6
        name="hugues"
        ## Récupération des coups
        coups,name_white,name_black = find_party(name,2)
        ## ANALYSE
        print('analyse')
        df = analysing_fish(coups)
    #transformation en liste
    moves= df.move.to_list()
    best_moves = df.best_move.to_list()

    # transformation de chiffre en position dans une matrice

    # accuracy de la partie 
    print('accuracy: ',df.accurate.mean())
    # accuracy par joueur
    print('accuracy white '+name_white+' : ',df[df.move_number%2==0].accurate.mean())
    print('accuracy black '+name_black+' : ',df[df.move_number%2==1].accurate.mean())

    # Récupération de la liste des coups
    board = chess.Board()
    current_move = -1  # Indice du coup

    # AFFICHAGE DE LA COURBE DE LA PARTIE
    courbe_partie(df,name_white,name_black)
    fig, ax = plt.subplots(figsize=(5, 5))

    ax_prev = plt.axes([0.1, 0.01, 0.15, 0.075])
    ax_next = plt.axes([0.75, 0.01, 0.15, 0.075])
    btn_prev = Button(ax_prev, '⬅ Précédent')
    btn_next = Button(ax_next, 'Suivant ➡')

    btn_prev.on_clicked(prev_move)
    btn_next.on_clicked(next_move)

    update_board()
    plt.show()
