from connect4 import Connect4
from copy import deepcopy
from new_heuristics import heuristic1


class Minimax:
    maxdepth = 0
    heuristic_function = None
    player_chip = None

    def __init__(self, maxdepth, heuristic_function, chip_color):
        self.maxdepth = maxdepth
        self.heuristic_function = heuristic_function
        self.player_chip = chip_color
        self.win_string = self.player_chip + '_WINS'
        self.lose_string = 'B_WINS' if self.player_chip == 'R' else 'R_WINS'

    def find_move(self, game):
        return self.minimax(game, self.maxdepth, True)

    def minimax(self, game, depth, maximizingPlayer):
        # print('calling minimax')

        # if the node is a terminal node (depth is at zero or the state of the game is gameover
        if depth == 0 or game.turn == 'B_WINS' or game.turn == 'R_WINS':

            if game.turn == self.win_string:
                return 999999999999, None

            elif game.turn == self.lose_string:
                return -999999999999, None

            else:

                board_score = self.heuristic_function(game, self.player_chip)

                return board_score, None
        if maximizingPlayer:
            value = -999999999999
            best_move = 0
            for valid_move in game.available_moves():
                child_game = Connect4(deepcopy(game.board), deepcopy(game.turn), deepcopy(game.last_move), deepcopy(game.total_moves))

                last_move = child_game.drop_chip(valid_move)
                value_this_move = self.minimax(child_game, depth - 1, not maximizingPlayer)[0]

                if value_this_move > value:
                    value = value_this_move
                    best_move = valid_move

            return value, best_move

        else:
            value = 999999999999
            best_move = 0
            for valid_move in game.available_moves():
                # print(valid_move)
                child_game = Connect4(deepcopy(game.board), deepcopy(game.turn), deepcopy(game.last_move), deepcopy(game.total_moves))

                last_move = child_game.drop_chip(valid_move)
                value_this_move = self.minimax(child_game, depth - 1, not maximizingPlayer)[0]

                if value_this_move < value:
                    value = value_this_move
                    best_move = valid_move
            return value, best_move



# if __name__ == '__main__':
#
#     c1 = Connect4()
#     mm_player = Minimax(3, heuristic1)
#
#
#     c1.drop_chip(3)
#     c1.new_print_board()
#
#     move, score = mm_player.find_move(c1)
#     print(move, score)





