import chess
import chess.engine
import asyncio
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re
from tqdm import tqdm

enginefile = "stockfish-windows-x86-64-avx2.exe" # engine file name

def ass_to_move(ass):
    a=str(ass)

    # suprime les nombres suivie d'un point et les doubles espaces
    b=re.sub(r"\d+\.", "", a)
    b=re.sub(r"  ", " ", b)

    c=b.split(" ")
    return c[1:]
# convert uci to san

def uci_to_san(uci):
    return chess.Move.from_uci(uci).uci()


def analysing_fish(coups):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    # Initialisation du moteur
    engine = chess.engine.SimpleEngine.popen_uci(enginefile, setpgrp=True)
    gamedata = []
    board = chess.Board()
    for i, move in tqdm(enumerate(coups)):
        board.push_san(move)
        evaluation = engine.analyse(board, chess.engine.Limit(depth=20))
        #{'string': 'NNUE evaluation using nn-37f18f62d772.nnue (6MiB, (22528, 128, 15, 32, 1))', 'depth': 20, 'seldepth': 23, 'multipv': 1, 'score': PovScore(Cp(-25), BLACK), 'nodes': 314556, 'nps': 970851, 'hashfull': 116, 'tbhits': 0, 'time': 0.324, 'pv': [Move.from_uci('d7d5'), Move.from_uci('d2d4'), Move.from_uci('g8f6'), Move.from_uci('c2c4'), Move.from_uci('e7e6'), Move.from_uci('c4d5'), Move.from_uci('e6d5'), Move.from_uci('b1c3'), Move.from_uci('f8b4'), Move.from_uci('c1g5'), Move.from_uci('c7c5'), Move.from_uci('e2e3'), Move.from_uci('h7h6'), Move.from_uci('g5h4'), Move.from_uci('g7g5'), Move.from_uci('h4g3'), Move.from_uci('c5c4')]}

        score = evaluation["score"].relative.score(mate_score=10000) if evaluation["score"].relative.is_mate() else evaluation["score"].relative.score()
        if 'pv' in evaluation:
            reply=evaluation["pv"][0:5]
        else:
            reply='a1h8'
        if i%2==0:
            score=-score
        gamedata.append({
            "move_number": i + 1,
            "move": move,
            "1reply":reply[0],
            "evaluation": score / 100 if score is not None else None,
            "reply":reply,
            "board": board.fen()
        })

    engine.quit()

    df = pd.DataFrame(gamedata)

    # TRANSFORMER LES COUPS EN SAN
    board = chess.Board()
    san_coup = []
    for i in df.move.to_list():
        san_coup.append(board.parse_san(i))
        board.push_san(i)
    df['move'] = san_coup

    # MEILLEUR COUP 
    ajoute=df['1reply'].tolist()
    # ajouter a2a4 pour le premier coup
    ajoute.insert(0, chess.Move.from_uci('e2e4'))
    df['1reply']=ajoute[:-1]
    # rename 1reply to best_reply
    df.rename(columns={'1reply':'best_move'}, inplace=True)
    # ACCURACY of the game
    df['accurate']=df['move']==df['best_move']
    df['str_reply'] = df['reply'].apply(lambda x: [str(i) for i in x])
    return df
