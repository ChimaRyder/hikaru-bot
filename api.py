import chess.pgn

from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import to_categorical
import numpy as np
from chess import pgn, Board
from flask_cors import CORS
from io import StringIO

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"])

model = load_model("hikarubot_24_2.keras")

# turn the board into a matrix
def board_to_matrix(board : Board):
    matrix = np.zeros((8, 8, 15))
    piece_map = board.piece_map()

    for square, piece in piece_map.items():
        row, col = divmod(square, 8)
        piece_type = piece.piece_type - 1
        piece_color = 0 if piece.color else 6
        matrix[row, col, piece_type + piece_color] = 1 if piece.color else 2

    legal_moves = board.legal_moves
    pseudo_moves = board.pseudo_legal_moves

    for move in legal_moves:
        to_square = move.to_square
        row_to, col_to = divmod(to_square, 8)
        matrix[row_to, col_to, 12] = 1

        if board.piece_at(move.to_square):
            matrix[row_to, col_to, 13] = 1

    for move in pseudo_moves:
        to_square = move.to_square
        row_to, col_to = divmod(to_square, 8)
        matrix[row_to, col_to, 14] = 1

    return matrix

# inputs for possible moves
def input_for_nn(games):
    X = []
    y = []
    for game in games:
        print(f'game {games.index(game) + 1} / {len(games)}')
        board = game.board()
        for move in game.mainline_moves():
            X.append(board_to_matrix(board))
            y.append(move.uci())
            board.push(move)
    return X, y

# convert moves
def encode_moves(moves):
    print("encoding...")
    move_to_int = {move: idx for idx, move in enumerate(set(moves))}
    return [move_to_int[move] for move in moves], move_to_int

@app.route('/bestmove', methods=['POST'])
def best_move():
    data = request.get_json()

    notation = data['pgn']
    print(notation)

    pgn = StringIO(notation)
    pgn = chess.pgn.read_game(pgn)

    # X, y = input_for_nn(pgn)
    # y, move_to_int = encode_moves(y)
    move_to_int = np.load('move_to_int.npy', allow_pickle=True).item()

    int_to_move = dict(zip(move_to_int.values(), move_to_int.keys()))

    print(pgn.board())
    board_matrix = board_to_matrix(pgn.board()).reshape(1, 8, 8, 15)
    prediction = model.predict(board_matrix)

    legal_moves = list(pgn.board().legal_moves)
    legal_moves_uci = [move.uci() for move in legal_moves]

    sorted_ind = np.argsort(prediction[0])[::-1]
    for idx in sorted_ind:
        move = int_to_move[idx]
        if move in legal_moves_uci:
            print(f"found move: {move}")
            return jsonify({'move': move})

    return jsonify({'result': "resigned"})

if __name__ == "__main__":
    app.run(debug=True)
