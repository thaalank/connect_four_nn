from connect4 import Connect4
from copy import deepcopy
import math

class AlphaBeta:
    maxdepth = 0
    heuristic_function = None
    player_chip = None

    def __init__(self, maxdepth, heuristic_function, player_chip):
        self.maxdepth = maxdepth
        self.heuristic_function = heuristic_function
        self.player_chip = player_chip
        self.win_string = self.player_chip + '_WINS'
        self.lose_string = 'B_WINS' if self.player_chip == 'R' else 'R_WINS'

    def find_move(self, board):
        score, move = self.alpha_beta(self.maxdepth, -math.inf, math.inf, True, board)
        # print(score, move)
        return score, move

    def score_board(self, game):
        tie = 'TIE'
        loss = self.lose_string
        win = self.win_string

        if game.turn == tie:
            return 0
        elif game.turn == loss:
            return -math.inf
        elif game.turn == win:
            return math.inf
        else:
            # print('need to actually score the board')
            return self.heuristic_function(game, self.player_chip)

    def alpha_beta(self, depth, alpha, beta, maximizing_player, game):
        '''
        returns value and move to take for the alpha_beta pruning AI to take
        '''

        done = game.turn == 'B_WINS' or game.turn == 'R_WINS' or game.turn == 'TIE'

        if depth == 0 or done:
            return self.score_board(game), None

        if maximizing_player:
            value = -math.inf
            best_move = 0

            # get the list of available moves
            valid_moves = game.available_moves()

            for move_to_take in valid_moves:
                child_game = Connect4(deepcopy(game.board), deepcopy(game.turn), deepcopy(game.last_move), deepcopy(game.total_moves))

                # make copy of the game instance
                child_game.drop_chip(move_to_take)
                score = self.alpha_beta(depth - 1, alpha, beta, False, child_game)[0]

                if score > value:
                    best_move = move_to_take
                    value = score

                alpha = max(alpha, value)
                if alpha >= beta:
                    # cut B OFF
                    # print("BREAKING")
                    break
            return value, best_move

        else:
            value = math.inf
            best_move = 0

            valid_moves = game.available_moves()
            for move_to_take in valid_moves:

                # make copy of the current game state
                child_game = Connect4(deepcopy(game.board), deepcopy(game.turn), deepcopy(game.last_move), deepcopy(game.total_moves))

                # make copy of the game instance

                child_game.drop_chip(move_to_take)

                score = self.alpha_beta(depth - 1, alpha, beta, True, child_game)[0]

                if score < value:
                    best_move = move_to_take
                    value = score

                beta = min(beta, value)

                if alpha >= beta:
                    # print('BREAKING')
                    break
            return value, best_move









