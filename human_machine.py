import chess
import chess.engine
import chess.pgn

def traitement_coup(coup):
    """
    Traite le coup donné par l'utilisateur.
    """
    # si 4 caractères to lower
    # si 3 caractères capitalize
    # si 2 caractères to lower
    if len(coup) == 4:
        coup = coup.lower()
    elif len(coup) == 3:
        coup = coup.capitalize()
    elif len(coup) == 2:
        coup = coup.lower()
    return coup


enginefile = "/Users/alaricdebastard/Documents/autre/systeme_de_l_ombre/stockfish-macos-m1-apple-silicon" # engine file name
board = chess.Board()
engine = chess.engine.SimpleEngine.popen_uci(enginefile, setpgrp=True)
while True:
    print(board)
    move = input("Enter your move (or 'q' to quit): ")
    if move == 'ia':
        # Initialize the chess engine
        evaluation = engine.analyse(board, chess.engine.Limit(depth=20))
        result=evaluation["pv"][0]
        print(f"AI move: {result}")
        #board.push(result.move)
        move = input("Enter your move (or 'q' to quit): ")
    if move == 'q':
        break
    if move ==  '':
        board.push_san(str(result))
    if move == 'fen':
        # afficher le fen
        print(" ")
        print(board.fen())
        print("")
        move = input("Enter your move (or 'q' to quit): ")
    if len(move) > 10:
        # try board.fen
        try:
            board.set_fen(move)
            continue
        except ValueError:
            print("Invalid FEN string. Please try again.")
            continue
    if move == 'back':
        # revenir en arrière
        board.pop()
        continue
    # traitement pour ne pas alterner maj minuscule
    move = traitement_coup(move)
    try:
        board.push_san(move)
    except ValueError:
        print("Invalid move. Please try again.")
    print("")

# Close the engine
engine.quit()


