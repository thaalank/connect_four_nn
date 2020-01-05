from connect4 import Connect4
from heuristics_final import heuristic5
from alpha_beta_class import AlphaBeta





def manage_human_input(game):
    try:

        column = int(input('It is your turn, choose a valid column \n'))
        if column not in game.available_moves():
            raise Exception
        return column


    except Exception as e:
        print(e)
        manage_human_input(game)


mmObj = AlphaBeta(4, heuristic5, 'B')
game = Connect4()

done = game.turn == 'B_WINS' or game.turn == 'R_WINS' or game.turn == 'TIE'


while not done:
    game.new_print_board()
    if game.turn == 'B':
        score, move = mmObj.find_move(game)
        print(score, move)
        game.drop_chip(move)
    else:
        human_move = manage_human_input(game)
        game.drop_chip(human_move)

    done = game.turn == 'B_WINS' or game.turn == 'R_WINS' or game.turn == 'TIE'


game.new_print_board()
print(game.turn)