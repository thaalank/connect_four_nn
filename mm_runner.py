from minimax_class import Minimax
from connect4 import Connect4
from new_heuristics import heuristic1




def human_vs_ai():
    stop_conditions = ['B_WINS', 'R_WINS', 'TIE']
    game = Connect4()
    mm_player = Minimax(4, heuristic1, 'R')

    while game.turn not in stop_conditions:
        game.new_print_board()

        if game.turn == 'R':
            move, score = mm_player.find_move(game)
            game.drop_chip(move)
            # game.new_print_board()

        else:
            human_move = input('Drop a chip into a valid column \n')
            game.drop_chip(int(human_move))
            # game.new_print_board()


    game.new_print_board()
    print(game.turn)

def ai_vs_ai():
    stop_conditions = ['B_WINS', 'R_WINS', 'TIE']
    game = Connect4()
    mm_player_red = Minimax(3, heuristic1, 'R')
    mm_player_blue = Minimax(3, heuristic1, 'B')

    while game.turn != "B_WINS" and game.turn != "R_WINS" and game.turn != "TIE":
        print(game.turn)
        game.new_print_board()

        if game.turn == 'R':
            score, move = mm_player_red.find_move(game)
            game.drop_chip(move)
            # game.new_print_board()

        else:
            score, move = mm_player_blue.find_move(game)
            game.drop_chip(move)
            # game.new_print_board()

    game.new_print_board()
    print(game.turn)


if __name__ == '__main__':
    ai_vs_ai()