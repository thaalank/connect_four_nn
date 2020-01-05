from connect4 import Connect4
from copy import deepcopy
threeinarowconditions = [

    ['R', 'R', 'R', None],
    ['R', 'R', None, 'R'],
    ['R', None, 'R', 'R'],
    [None, 'R', 'R', 'R'],

    ['B', 'B', 'B', None],
    ['B', 'B', None, 'B'],
    ['B', None, 'B', 'B'],
    [None, 'B', 'B', 'B']

]
twoinarowconditions = [

    ['R', 'R', None, None],
    ['R', None, 'R', None],
    ['R', None, None, 'R'],
    [None, 'R', 'R', None],
    [None, 'R', None, 'R'],
    [None, None, 'R', 'R'],
#     blues
    ['B', 'B', None, None],
    ['B', None, 'B', None],
    ['B', None, None, 'B'],
    [None, 'B', 'B', None],
    [None, 'B', None, 'B'],
    [None, None, 'B', 'B'],
]

'''
Scores the entire board
'''
def score_entire_board(game, player):

    red_twos_that_can_win = 0
    blue_twos_that_can_win = 0
    blue_threes_that_can_win = 0
    red_threes_that_can_win = 0

    for row in range(game.rows):
        for col in range(game.columns):

            if game.get_chip(row, col) is None:
                continue
            elif game.get_chip(row, col) == 'B':
                # print('adding to blues score')
                blue_twos_that_can_win += count_2s_that_can_win(game, (row, col))
                blue_threes_that_can_win += count_3s_that_can_win(game, (row, col))
            else:
                # print('adding to reds score')
                red_twos_that_can_win += count_2s_that_can_win(game, (row, col))
                red_threes_that_can_win += count_3s_that_can_win(game, (row, col))


    if player == 'R':
        return 10 * (red_threes_that_can_win - blue_threes_that_can_win) + 1 * (red_twos_that_can_win - blue_twos_that_can_win)
    else:
        return 10*(blue_threes_that_can_win - red_threes_that_can_win) + 1*(blue_twos_that_can_win - red_twos_that_can_win)


def count_3s_that_can_win(game, lastMove):
    row = lastMove[0]
    column = lastMove[1]
    # game.print_board()
    chip = game.get_chip(row, column)
    # print(chip)

    up_to_7_horiz = game.get_up_to_7_horizontal(lastMove[0], lastMove[1])
    up_to_7_vert = game.get_up_to_7_vertical(row, column)
    up_to_7_forward_slash = game.win_diagonal_forward_slash(row, column)
    up_to_7_backward_slash = game.win_diagonal_backward_slash(row, column)
    # print(up_to_7_backward_slash)

    all_possible_ways = [up_to_7_horiz, up_to_7_vert, up_to_7_forward_slash, up_to_7_backward_slash]
    total_num_conversions = 0
    for way in all_possible_ways:

        possible_conversions_this_way = 0
        for index, chip in enumerate(way):
            try:
                arr = [way[index], way[index + 1], way[index + 2], way[index + 3]]
                if arr in threeinarowconditions:
                    # print('the last move taken can convert into a win')
                    # print(arr)
                    possible_conversions_this_way += 1
            except:
                continue
        total_num_conversions += possible_conversions_this_way
    # print(total_num_conversions)

    return total_num_conversions

def count_2s_that_can_win(game, lastMove):
    row = lastMove[0]
    column = lastMove[1]
    # game.print_board()
    chip = game.get_chip(row, column)
    # print(chip)



    up_to_7_horiz = game.get_up_to_7_horizontal(lastMove[0], lastMove[1])
    up_to_7_vert = game.get_up_to_7_vertical(row, column)
    up_to_7_forward_slash = game.win_diagonal_forward_slash(row, column)
    up_to_7_backward_slash = game.win_diagonal_backward_slash(row, column)
    # print(up_to_7_backward_slash)

    all_possible_ways = [up_to_7_horiz, up_to_7_vert, up_to_7_forward_slash, up_to_7_backward_slash]
    total_num_conversions = 0
    for way in all_possible_ways:

        possible_conversions_this_way = 0
        for index, chip in enumerate(way):
            try:
                arr = [way[index], way[index+1], way[index+2], way[index+3]]
                if arr in twoinarowconditions:

                    # print('the last move taken can convert into a win')
                    # print(arr)
                    possible_conversions_this_way += 1
            except:
                continue
        total_num_conversions += possible_conversions_this_way
    # print(total_num_conversions)

    return total_num_conversions

def score_board(game):
    # game.print_board()
    # print(game.last_move)

    # print('current turn is: ' + game.turn)
    if game.turn == 'B':

        # print('finding number of twos that ' + game.turn + ' can make')
        # print(game.turn)
        twos = score_entire_board(game, 'B')
        # print('found this many potential 2 in a rows for red this game: ' + str(twos))
        if twos != 0:
            game.new_print_board()
        return twos
    else:
        # print('')
        return score_entire_board(game, 'R')

def minimax(game, depth, maximizingPlayer):
    # print('calling minimax')


    # if the node is a terminal node (depth is at zero or the state of the game is gameover
    if depth == 0 or game.turn == 'B_WINS' or game.turn == 'R_WINS':
        # print('calling score board')
#         return the heruristic value of board

        if game.turn == 'R_WINS':

            # return the last chip to be played!!
            return None, 999999999999

        elif game.turn == 'B_WINS':
            return None, -999999999999

        else:

            board_score = score_board(game)

            # print(board_score)
            # print('score of this board is: ' + str(board_score))
            return None, board_score

    if maximizingPlayer:
        # print('maximizing')
        value = -999999999999
        best_move = 0
        for valid_move in game.available_moves():
            # print(valid_move)
            child_game = Connect4(deepcopy(game.board), deepcopy(game.turn))



            last_move = child_game.drop_chip(valid_move)
            # print('printing child game turn ')
            # print(child_game.turn)
            # print(child_game.turn)
            # print(child_game.turn)
            # print(child_game.turn)
            # print(child_game.turn)
            # print(child_game.turn)
            # print(child_game.turn)
            value_this_move = minimax(child_game, depth-1, not maximizingPlayer)[1]

            if value_this_move == -1:
                # print("HELLO THERE LOOK AT ME!!!!")
                # print("GAME IS CURRENTLY AT THIS STATE AND WE ARE MAXIMIZING THIS PLAYER")
                game.new_print_board()
            if value_this_move > value:
                value = value_this_move
                best_move = valid_move

            # value = max(value, minimax(child_game, depth-1, False))
        return best_move, value

    else:
        value = 999999999999
        best_move = 0
        for valid_move in game.available_moves():
            # print(valid_move)
            child_game = Connect4(deepcopy(game.board), deepcopy(game.turn))


            last_move = child_game.drop_chip(valid_move)
            # print('printing turn from the minimizing player!!')
            # print(child_game.turn)
            value_this_move = minimax(child_game, depth-1, not maximizingPlayer)[1]


            # print('comparing: ' + str(value_this_move) + ' to: ' + str(value))
            if value_this_move < value:
                # print('found a new minimum value')
                # print(value, best_move)
                value = value_this_move
                best_move = valid_move
        return best_move, value

def manage_input(c):

    x = input("it is " + c.turn + "'s turn enter a column\n")
    try:
        if (int(x) in range(c.columns)) and (not c.is_column_full(int(x))):

            c.drop_chip(int(x))
            c.new_print_board()
        else:
            print("invalid input")
            return False
        return True
    except:
        return False


def manage_minimax_input(game):
    '''
        if the AI moves first, just go in the middle
    '''
    if game.board == game.new_board():
        # print("AI IS GOING FIRST")
        game.drop_chip(0)
        game.new_print_board()
    else:

        best_move, value = minimax(game, 4, True)
        # print('best move is : ' + str((best_move, value)))
        game.drop_chip(best_move)
        game.new_print_board()

    # best_move = minimax(game, 2, True, None)
    # print(best_move)

def runPVE():
    x = input("would you like to play a game against our minimax ai? yes or no\n")
    if x == 'yes':
        print("playing game")

        c = Connect4()
        c.new_print_board()

        # human is always blue
        human = "B"

        while c.turn != "B_WINS" and c.turn != "R_WINS" and c.turn != "TIE":

            if c.turn == human:
                # if it is the humans turn: manage the humans input
                # TODO: bug here
                if not manage_input(c): continue

            else:
                #         manage the ai's input
                manage_minimax_input(c)

        print("GAME IS OVER")
        print(c.turn)


if __name__ == "__main__":
    runPVE()
    # c1 = Connect4()
    # c1.turn = 'B'
    # c1.drop_chip(6)
    # c1.drop_chip(5)
    # c1.drop_chip(5)
    # c1.drop_chip(4)
    # c1.drop_chip(4)
    # c1.drop_chip(3)
    # c1.drop_chip(4)
    # c1.drop_chip(3)
    # c1.drop_chip(3)
    # c1.drop_chip(0)
    # c1.drop_chip(0)
    # c1.drop_chip(0)
    # c1.drop_chip(2)
    #
    #
    # print(c1.turn)
    # c1.print_board()
    # #
    # #
    # print(minimax(c1, 3, True))







