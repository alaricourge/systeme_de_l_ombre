import chess
import chess.pgn
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import cairosvg
from PIL import Image
from io import BytesIO
from chess import Move
from recherche_chess import find_party
from analyse_party import analysing_fish

moves=[Move.from_uci('e2e4'), Move.from_uci('e7e6'), Move.from_uci('g1f3'), Move.from_uci('b7b6'), Move.from_uci('f1c4'), Move.from_uci('c8b7'), Move.from_uci('e4e5'), Move.from_uci('b8c6'), Move.from_uci('b1c3'), Move.from_uci('g8h6'), Move.from_uci('d2d4'), Move.from_uci('h6f5'), Move.from_uci('d4d5'), Move.from_uci('c6b4'), Move.from_uci('d5e6'), Move.from_uci('f7e6'), Move.from_uci('e1g1'), Move.from_uci('d8e7'), Move.from_uci('c3b5'), Move.from_uci('e8c8'), Move.from_uci('b5a7'), Move.from_uci('c8b8'), Move.from_uci('a7b5'), Move.from_uci('h7h6'), Move.from_uci('a2a3'), Move.from_uci('b4c6'), Move.from_uci('d1e2'), Move.from_uci('g7g5'), Move.from_uci('c1e3'), Move.from_uci('f5e3'), Move.from_uci('e2e3'), Move.from_uci('f8g7'), Move.from_uci('a1d1'), Move.from_uci('g5g4'), Move.from_uci('f3d4'), Move.from_uci('c6d4'), Move.from_uci('e3d4'), Move.from_uci('h6h5'), Move.from_uci('d1d3'), Move.from_uci('d8g8'), Move.from_uci('c4b3'), Move.from_uci('h5h4'), Move.from_uci('d4g4'), Move.from_uci('b7g2'), Move.from_uci('g4c4'), Move.from_uci('g7e5'), Move.from_uci('h2h3'), Move.from_uci('g2d5'), Move.from_uci('c4g4'), Move.from_uci('g8g4'), Move.from_uci('h3g4'), Move.from_uci('h4h3'), Move.from_uci('f2f4'), Move.from_uci('h3h2'), Move.from_uci('g1f2'), Move.from_uci('e5f4'), Move.from_uci('b3d5'), Move.from_uci('e7h4'), Move.from_uci('f2f3'), Move.from_uci('h4g3'), Move.from_uci('f3e4'), Move.from_uci('h2h1q'), Move.from_uci('f1h1'), Move.from_uci('e6d5'), Move.from_uci('d3d5'), Move.from_uci('g3g2'), Move.from_uci('e4f4'), Move.from_uci('h8h1'), Move.from_uci('d5d7'), Move.from_uci('h1f1'), Move.from_uci('f4g5'), Move.from_uci('g2c2'), Move.from_uci('d7d8'), Move.from_uci('b8b7'), Move.from_uci('a3a4'), Move.from_uci('c2c5'), Move.from_uci('g5h4'), Move.from_uci('f1h1'), Move.from_uci('h4g3'), Move.from_uci('c5e3'), Move.from_uci('g3g2'), Move.from_uci('h1g1'), Move.from_uci('g2h2'), Move.from_uci('e3f2'), Move.from_uci('h2h3'), Move.from_uci('g1g3'), Move.from_uci('h3h4'), Move.from_uci('f2g2'), Move.from_uci('d8g8'), Move.from_uci('g2h3'), Move.from_uci('h4g5'), Move.from_uci('g3g4'), Move.from_uci('g5f6'), Move.from_uci('g4g8')]
best_moves =[Move.from_uci('e2e4'), Move.from_uci('c7c5'), Move.from_uci('d2d4'), Move.from_uci('d7d5'), Move.from_uci('d2d4'), Move.from_uci('c8b7'), Move.from_uci('d2d3'), Move.from_uci('d7d5'), Move.from_uci('d2d4'), Move.from_uci('d7d6'), Move.from_uci('d2d4'), Move.from_uci('h6f5'), Move.from_uci('d4d5'), Move.from_uci('c6e7'), Move.from_uci('a2a3'), Move.from_uci('d7e6'), Move.from_uci('e1g1'), Move.from_uci('f8e7'), Move.from_uci('a2a3'), Move.from_uci('e7c5'), Move.from_uci('c2c3'), Move.from_uci('c8b8'), Move.from_uci('c2c3'), Move.from_uci('e7c5'), Move.from_uci('c2c3'), Move.from_uci('b4c6'), Move.from_uci('c2c3'), Move.from_uci('g7g5'), Move.from_uci('c2c3'), Move.from_uci('g5g4'), Move.from_uci('e2e3'), Move.from_uci('g5g4'), Move.from_uci('a3a4'), Move.from_uci('g5g4'), Move.from_uci('f3d4'), Move.from_uci('c6e5'), Move.from_uci('d1d4'), Move.from_uci('h6h5'), Move.from_uci('d1d3'), Move.from_uci('h8f8'), Move.from_uci('f1e1'), Move.from_uci('g4g3'), Move.from_uci('d3c3'), Move.from_uci('g7e5'), Move.from_uci('g4a4'), Move.from_uci('g7e5'), Move.from_uci('f2f4'), Move.from_uci('g2f3'), Move.from_uci('c4g4'), Move.from_uci('g8g4'), Move.from_uci('h3g4'), Move.from_uci('e7g5'), Move.from_uci('b3d5'), Move.from_uci('h3h2'), Move.from_uci('g1f2'), Move.from_uci('e7h4'), Move.from_uci('b3d5'), Move.from_uci('e6d5'), Move.from_uci('f2e2'), Move.from_uci('e6d5'), Move.from_uci('f3e2'), Move.from_uci('e6d5'), Move.from_uci('f1h1'), Move.from_uci('e6d5'), Move.from_uci('e4d5'), Move.from_uci('g3e3'), Move.from_uci('e4f4'), Move.from_uci('g2h1'), Move.from_uci('b5c3'), Move.from_uci('g2f1'), Move.from_uci('f4g5'), Move.from_uci('g2c6'), Move.from_uci('d7d8'), Move.from_uci('b8b7'), Move.from_uci('a3a4'), Move.from_uci('c2h7'), Move.from_uci('g5g6'), Move.from_uci('f1h1'), Move.from_uci('h4g3'), Move.from_uci('c5e3'), Move.from_uci('g3g2'), Move.from_uci('h1g1'), Move.from_uci('g2h2'), Move.from_uci('e3g3'), Move.from_uci('h2h3'), Move.from_uci('g1h1'), Move.from_uci('h3h4'), Move.from_uci('g3d3'), Move.from_uci('d8d4'), Move.from_uci('g2h3'), Move.from_uci('h4g5'), Move.from_uci('h3g4'), Move.from_uci('g5f6'), Move.from_uci('h3f3')]
name="loup_rouge"
## Récupération des coups
coups = find_party(name)
print('analyse')
df = analysing_fish(coups)
moves= df.move.to_list()
best_moves = df.best_move.to_list()


def number_to_position(n):
    x = n // 8
    y = n % 8
    return 7-x,y 


print('accuracy: ',df.accurate.mean())
# Récupération de la liste des coups
board = chess.Board()
current_move = -1  # Indice du coup


plt.figure(figsize=(8,4))
plt.plot(df["evaluation"])
plt.yscale("symlog", linthresh=10)
plt.title("Évaluation de la position")
plt.xlabel("Coup")
plt.ylabel("Évaluation")
plt.grid(True)
plt.show()





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


    title_text = "Chess" if current_move <= 0 else df.str_reply[current_move-1]
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
