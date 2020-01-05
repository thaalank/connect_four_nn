from connect4 import Connect4
from copy import deepcopy

from heuristics_final import heuristic5
import math




'''
Input: Connect4 game instance
Returns: the score of the given board, along with the boards last move that caused it to be in 
the state we are evalutating
'''
def score_board(game):
    tie = 'TIE'
    loss = 'B_WINS'
    win = 'R_WINS'

    if game.turn == tie:
        return 0
    elif game.turn == loss:
        return -math.inf
    elif game.turn == win:
        return math.inf
    else:
        # print('need to actually score the board')
        return heuristic5(game, 'R')



def alpha_beta(depth, alpha, beta, maximizing_player, game):
    '''
    returns value and move to take for the alpha_beta pruning AI to take
    '''

    # print('making call to alpha beta')
    # print(depth)
    done = game.turn == 'B_WINS' or game.turn == 'R_WINS' or game.turn == 'TIE'

    if depth == 0 or done:
        # return the heuristic value of the the Leaf
        # TODO: ensure that the move here is correct
        # move = None
        # print('AT DEPTH 0')
        return score_board(game), None





    # print('about to make recursive call ')

    if maximizing_player:
        value = -math.inf
        best_move = 0


        #get the list of available moves
        valid_moves = game.available_moves()

        for move_to_take in valid_moves:
            child_game = Connect4(deepcopy(game.board), deepcopy(game.turn), deepcopy(game.last_move))

            #make copy of the game instance
            child_game.drop_chip(move_to_take)
            score = alpha_beta(depth-1, alpha, beta, False, child_game)[0]

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
            child_game = Connect4(deepcopy(game.board), deepcopy(game.turn), deepcopy(game.last_move))

            # make copy of the game instance

            child_game.drop_chip(move_to_take)

            score = alpha_beta(depth - 1, alpha, beta, True, child_game)[0]

            if score < value:
                best_move = move_to_take
                value = score

            beta = min(beta, value)

            if alpha >= beta:
                # print('BREAKING')
                break
        return value, best_move



    # findMove helper function, utilizing alpha-beta pruning within the  minimax algorithm
def online_alpha_beta( game, depth, player, alpha, beta):

    '''
    done = game.turn == 'B_WINS' or game.turn == 'R_WINS' or game.turn == 'TIE'

    if depth == 0 or done:
    '''
    done = game.turn == 'B_WINS' or game.turn == 'R_WINS' or game.turn == 'TIE'

    if done:
        return -math.inf if player else math.inf, -1
    elif depth == 0:
        return score_board(game), -1

    if player:
        bestScore = -math.inf
        shouldReplace = lambda x: x > bestScore
    else:
        bestScore = math.inf
        shouldReplace = lambda x: x < bestScore

    bestMove = -1

    #TODO: here, what does board.children() do?
    # children = board.children()
    for move in game.available_moves():
        # make new move
        child_game = Connect4(deepcopy(game.board), deepcopy(game.turn), deepcopy(game.last_move))
        child_game.drop_chip(move)


        # move, childboard = child
        temp = online_alpha_beta(child_game, depth-1, not player, alpha, beta)[0]
        if shouldReplace(temp):
            bestScore = temp
            bestMove = move
        if player:
            alpha = max(alpha, temp)
        else:
            beta = min(beta, temp)
        if alpha >= beta:
            break

    return bestScore, bestMove


def findMove(board):
    # score, move = self.alphaBeta(board, self.depthLimit, self.isPlayerOne, -math.inf, math.inf)

    # score, move = online_alpha_beta(board, 5, True, -math.inf, math.inf)
    score, move = alpha_beta(5, -math.inf, math.inf, True, board)
    return score, move






def return_move_for_ABPruning(depth):
    print(3)


'''
Modifies the 'turn' of the game using our Minimax algorithm implemented with Alpha-Beta Pruning
'''
def manage_AB_input(game):


    # if it is the first turn of the game, just go in column 0

    # def alpha_beta(depth, alpha, beta, maximizing_player, game):
    optimal_value, optimal_move = findMove(game)
    game.drop_chip(optimal_move)
    print('optimal value is: ' + str(optimal_value) + 'optimal move is: ' + str(optimal_move))



def manage_human_input(game):

    move_to_take = input('it is your turn, enter a valid column\n')
    valid_moves = game.available_moves()

    if move_to_take not in valid_moves:
        game.drop_chip(int(move_to_take))
        game.new_print_board()
    else:
        print('invalid move, enter a column that is not currently full')
        manage_human_input(game)

def run_pve():

    game = Connect4()

    done = game.turn == 'B_WINS' or game.turn == 'R_WINS' or game.turn == 'TIE'


    human = 'B'
    AI_turn = 'R'

    while not done:


        if game.turn == human:
            game.new_print_board()
            manage_human_input(game)
        else:
            manage_AB_input(game)

        done = game.turn == 'B_WINS' or game.turn == 'R_WINS' or game.turn == 'TIE'


    print(game.turn)
    game.new_print_board()


def test_ensures_block_move():
    game = Connect4()

    game.turn = 'B'

    game.drop_chip(5)

    manage_AB_input(game)

    game.drop_chip(5)

    manage_AB_input(game)

    game.drop_chip(5)

    game.new_print_board()
    game.new_print_board()
    game.new_print_board()
    game.new_print_board()
    game.new_print_board()




    manage_AB_input(game)


    game.new_print_board()


def test_print_board():
    game = Connect4()
    game.new_print_board()
    game.drop_chip(4)
    game.new_print_board()

if __name__ == '__main__':

    # test_print_board()
    run_pve()



    # test_ensures_block_move()


