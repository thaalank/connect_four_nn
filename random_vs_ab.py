from alpha_beta_class import AlphaBeta
from heuristics_final import heuristic5
from connect4 import Connect4
from random import randint


def random_drop(game: Connect4):
    valid_moves = game.available_moves()
    random_index = randint(0, len(valid_moves) - 1)
    random_column = valid_moves[random_index]
    return random_column


ab_obj = AlphaBeta(4, heuristic5, 'R')
game = Connect4()

final_states = ('B_WINS', 'R_WINS', 'TIE')

while game.turn not in final_states:
    game.new_print_board()
    if game.turn == 'R':
        score, move = ab_obj.find_move(game)
        game.drop_chip(move)
    elif game.turn == 'B':
        random_column = random_drop(game)
        game.drop_chip(random_column)

game.new_print_board()
print(game.turn)