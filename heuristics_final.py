from connect4 import Connect4
from minimax_class import Minimax
from random import randint
from alpha_beta_class import AlphaBeta
import time
import matplotlib.pyplot as plt

'''
Returns the number of 3 in a rows that can be converted into a win![
'''
def count_3s_that_can_win(game, lastMove):

    three_in_a_row_conditions = [

        ['R', 'R', 'R', None],
        ['R', 'R', None, 'R'],
        ['R', None, 'R', 'R'],
        [None, 'R', 'R', 'R'],

        ['B', 'B', 'B', None],
        ['B', 'B', None, 'B'],
        ['B', None, 'B', 'B'],
        [None, 'B', 'B', 'B']

    ]

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
                if arr in three_in_a_row_conditions:
                    # print('the last move taken can convert into a win')
                    # print(arr)
                    possible_conversions_this_way += 1
            except:
                continue
        total_num_conversions += possible_conversions_this_way
    # print(total_num_conversions)

    return total_num_conversions




'''
Returns the number of 2 in a rows that can be converted into a win![
'''
def count_2s_that_can_win(game, lastMove):

    two_in_a_row_conditions = [

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


    row = lastMove[0]
    column = lastMove[1]
    # game.print_board()
    chip = game.get_chip(row, column)
    # print(chip)

    up_to_7_horiz = game.get_up_to_7_horizontal(row, column)
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
                if arr in two_in_a_row_conditions:

                    # print('the last move taken can convert into a win')
                    # print(arr)
                    possible_conversions_this_way += 1
            except:
                continue
        total_num_conversions += possible_conversions_this_way
    # print(total_num_conversions)

    return total_num_conversions



'''
Scores the entire board

Weighted sum of heuristic 3 and 4
'''
def heuristic5(game, player):

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


    # print('R_2s, R_3s, B_2s, B_3s')
    # print(red_twos_that_can_win, red_threes_that_can_win, blue_twos_that_can_win, blue_threes_that_can_win)
    if player == 'R':
        return 10 * (red_threes_that_can_win - blue_threes_that_can_win) + 1 * (red_twos_that_can_win - blue_twos_that_can_win)
    else:
        return 10*(blue_threes_that_can_win - red_threes_that_can_win) + 1*(blue_twos_that_can_win - red_twos_that_can_win)

'''
Scores the entire board

Only considers 3 in a row streaks
'''
def heuristic4(game, player):
    blue_threes_that_can_win = 0
    red_threes_that_can_win = 0

    for row in range(game.rows):
        for col in range(game.columns):

            if game.get_chip(row, col) is None:
                continue
            elif game.get_chip(row, col) == 'B':
                # print('adding to blues score')
                blue_threes_that_can_win += count_3s_that_can_win(game, (row, col))
            else:
                # print('adding to reds score')
                red_threes_that_can_win += count_3s_that_can_win(game, (row, col))

    # print('R_2s, R_3s, B_2s, B_3s')
    # print(red_twos_that_can_win, red_threes_that_can_win, blue_twos_that_can_win, blue_threes_that_can_win)
    if player == 'R':
        return red_threes_that_can_win - blue_threes_that_can_win
    else:
        return blue_threes_that_can_win - red_threes_that_can_win


'''
Scores the entire board

Only considers 2 in a row streaks
'''
def heuristic3(game, player):
    red_twos_that_can_win = 0
    blue_twos_that_can_win = 0

    for row in range(game.rows):
        for col in range(game.columns):

            if game.get_chip(row, col) is None:
                continue
            elif game.get_chip(row, col) == 'B':
                # print('adding to blues score')
                blue_twos_that_can_win += count_2s_that_can_win(game, (row, col))
            else:
                # print('adding to reds score')
                red_twos_that_can_win += count_2s_that_can_win(game, (row, col))

    # print('R_2s, R_3s, B_2s, B_3s')
    # print(red_twos_that_can_win, red_threes_that_can_win, blue_twos_that_can_win, blue_threes_that_can_win)
    if player == 'R':
        return red_twos_that_can_win - blue_twos_that_can_win
    else:
        return blue_twos_that_can_win - red_twos_that_can_win

'''
Makes an instance of the game with 20 randomly dropped chips in it
If the game is over, recursively call this
'''
def drop_20_chips():

    game = Connect4()
    count = 20

    while count > 0:

        # get the games available moves
        valid_moves = game.available_moves()
        # print(valid_moves)
        random_index = randint(0, len(valid_moves) - 1)
        random_move = valid_moves[random_index]
        game.drop_chip(random_move)
        if game.turn == 'R_WINS' or game.turn == 'B_WINS':
            return drop_20_chips()
        count -= 1

    if game.turn == 'R' or game.turn == 'B':
        # print('RETURNING GAME')
        # print(game.turn)
        return game

    else:
        return drop_20_chips()
    # game.new_print_board()




def record_time(AIobj, game):
    # print('recording time')
    current_time = time.time()

    AIobj.find_move(game)

    elapsed_time = time.time() - current_time
    return elapsed_time


'''
Randomly generates 20 unfinished games 
records the time it takes for each heuristic function to run 
'''
def compare_heuristics():

    mm_1 = Minimax(4, heuristic3, 'R')
    mm_2 = Minimax(4, heuristic4, 'R')
    mm_3 = Minimax(4, heuristic3, 'R')
    mm_4 = Minimax(4, heuristic4, 'R')
    mm_5 = Minimax(4, heuristic5, 'R')


    twenty_random_games = [drop_20_chips() for x in range(20)]
    mm_1_average_time = sum([record_time(mm_1, game) for game in twenty_random_games])/20.0
    mm_2_average_time = sum([record_time(mm_2, game) for game in twenty_random_games])/20.0
    mm_3_average_time = sum([record_time(mm_3, game) for game in twenty_random_games])/20.0
    mm_4_average_time = sum([record_time(mm_4, game) for game in twenty_random_games])/20.0
    mm_5_average_time = sum([record_time(mm_5, game) for game in twenty_random_games])/20.0

    print(mm_1_average_time)
    print(mm_2_average_time)
    print(mm_3_average_time)
    print(mm_4_average_time)
    print(mm_5_average_time)

    performance = [mm_1_average_time, mm_2_average_time, mm_3_average_time, mm_4_average_time, mm_5_average_time]
    objects = ['1', '2', '3', '4', '5']

    plt.bar([x for x in range(5)], performance, align='center', color=('red', 'blue', 'green', 'purple', 'black'))
    plt.xticks([x for x in range(5)], objects)
    plt.ylabel('Average Heuristic Running Time')
    plt.xlabel('Heuristic Function Used at Max Depth = 4')
    plt.title('Recording Average Running Times on 20 Random Games')
    plt.show()


'''
Records running time of heuristic 5 on 20 random boards for various max depths
'''
def compare_depth_times():
    mm_1 = Minimax(1, heuristic5, 'R')
    mm_2 = Minimax(2, heuristic5, 'R')
    mm_3 = Minimax(3, heuristic5, 'R')
    mm_4 = Minimax(4, heuristic5, 'R')
    mm_5 = Minimax(5, heuristic5, 'R')
    mm_6 = Minimax(6, heuristic5, 'R')

    num_games = 10

    twenty_random_games = [drop_20_chips() for x in range(num_games)]
    mm_1_average_time = sum([record_time(mm_1, game) for game in twenty_random_games]) / float(num_games)
    print('done depth 1')
    mm_2_average_time = sum([record_time(mm_2, game) for game in twenty_random_games]) / float(num_games)
    print('done depth 2')

    mm_3_average_time = sum([record_time(mm_3, game) for game in twenty_random_games]) / float(num_games)
    print('done depth 3')

    mm_4_average_time = sum([record_time(mm_4, game) for game in twenty_random_games]) / float(num_games)
    print('done depth 4')


    mm_5_average_time = sum([record_time(mm_5, game) for game in twenty_random_games]) / float(num_games)
    print('done depth 5')

    mm_6_average_time = sum([record_time(mm_6, game) for game in twenty_random_games]) / float(num_games)
    print('done depth 6')


    x_vals = [1, 2, 3, 4, 5, 6]
    y_vals = [mm_1_average_time, mm_2_average_time, mm_3_average_time, mm_4_average_time, mm_5_average_time, mm_6_average_time]

    plt.plot(x_vals, y_vals)
    plt.xticks([1, 2, 3, 4, 5, 6], ('1', '2', '3', '4', '5', '6'))
    plt.ylabel('Average Running Time of Heuristic 5')
    plt.xlabel('Minimax Max Depth')
    plt.title('Recording Heuristic 5 Run Time on 20 Random Games at Various Max Depths')
    plt.show()


'''
Records running time of heuristic 5 on 20 random boards for various max depths
'''
def compare_depth_times_ab():
    mm_1 = AlphaBeta(1, heuristic5, 'R')
    mm_2 = AlphaBeta(2, heuristic5, 'R')
    mm_3 = AlphaBeta(3, heuristic5, 'R')
    mm_4 = AlphaBeta(4, heuristic5, 'R')
    mm_5 = AlphaBeta(5, heuristic5, 'R')
    mm_6 = AlphaBeta(6, heuristic5, 'R')

    num_games = 10

    twenty_random_games = [drop_20_chips() for x in range(num_games)]
    mm_1_average_time = sum([record_time(mm_1, game) for game in twenty_random_games]) / float(num_games)
    print('done depth 1')
    mm_2_average_time = sum([record_time(mm_2, game) for game in twenty_random_games]) / float(num_games)
    print('done depth 2')

    mm_3_average_time = sum([record_time(mm_3, game) for game in twenty_random_games]) / float(num_games)
    print('done depth 3')

    mm_4_average_time = sum([record_time(mm_4, game) for game in twenty_random_games]) / float(num_games)
    print('done depth 4')


    mm_5_average_time = sum([record_time(mm_5, game) for game in twenty_random_games]) / float(num_games)
    print('done depth 5')

    mm_6_average_time = sum([record_time(mm_6, game) for game in twenty_random_games]) / float(num_games)
    print('done depth 6')


    x_vals = [1, 2, 3, 4, 5, 6]
    y_vals = [mm_1_average_time, mm_2_average_time, mm_3_average_time, mm_4_average_time, mm_5_average_time, mm_6_average_time]

    plt.plot(x_vals, y_vals)
    plt.xticks([1, 2, 3, 4, 5, 6], ('1', '2', '3', '4', '5', '6'))
    plt.ylabel('Average Running Time of Heuristic 5')
    plt.xlabel('Alpha Beta Max Depth')
    plt.title('Recording Heuristic 5 Run Time on 20 Random Games at Various Max Depths')
    plt.show()

def compare_mm_to_ab():

    num_games = 10

    twenty_random_games = [drop_20_chips() for x in range(num_games)]

    ab_1 = AlphaBeta(1, heuristic5, 'R')
    ab_2 = AlphaBeta(2, heuristic5, 'R')
    ab_3 = AlphaBeta(3, heuristic5, 'R')
    ab_4 = AlphaBeta(4, heuristic5, 'R')
    ab_5 = AlphaBeta(5, heuristic5, 'R')
    ab_6 = AlphaBeta(6, heuristic5, 'R')

    mm_1 = Minimax(1, heuristic5, 'R')
    mm_2 = Minimax(2, heuristic5, 'R')
    mm_3 = Minimax(3, heuristic5, 'R')
    mm_4 = Minimax(4, heuristic5, 'R')
    mm_5 = Minimax(5, heuristic5, 'R')
    mm_6 = Minimax(6, heuristic5, 'R')



    ab_1_average_time = sum([record_time(ab_1, game) for game in twenty_random_games]) / float(num_games)
    print('done depth 1')
    ab_2_average_time = sum([record_time(ab_2, game) for game in twenty_random_games]) / float(num_games)
    print('done depth 2')
    ab_3_average_time = sum([record_time(ab_3, game) for game in twenty_random_games]) / float(num_games)
    print('done depth 3')
    ab_4_average_time = sum([record_time(ab_4, game) for game in twenty_random_games]) / float(num_games)
    print('done depth 4')
    ab_5_average_time = sum([record_time(ab_5, game) for game in twenty_random_games]) / float(num_games)
    print('done depth 5')
    ab_6_average_time = sum([record_time(ab_6, game) for game in twenty_random_games]) / float(num_games)
    print('finished ab')




    mm_1_average_time = sum([record_time(mm_1, game) for game in twenty_random_games]) / float(num_games)
    print('done depth 1')
    mm_2_average_time = sum([record_time(mm_2, game) for game in twenty_random_games]) / float(num_games)
    print('done depth 2')
    mm_3_average_time = sum([record_time(mm_3, game) for game in twenty_random_games]) / float(num_games)
    print('done depth 3')
    mm_4_average_time = sum([record_time(mm_4, game) for game in twenty_random_games]) / float(num_games)
    print('done depth 4')
    mm_5_average_time = sum([record_time(mm_5, game) for game in twenty_random_games]) / float(num_games)
    print('done depth 5')
    mm_6_average_time = sum([record_time(mm_6, game) for game in twenty_random_games]) / float(num_games)
    print('done depth 6')


    x_vals = [1, 2, 3, 4, 5, 6]
    y_vals = [ab_1_average_time, ab_2_average_time, ab_3_average_time, ab_4_average_time, ab_5_average_time, ab_6_average_time]
    y_vals_mm = [mm_1_average_time, mm_2_average_time, mm_3_average_time, mm_4_average_time, mm_5_average_time, mm_6_average_time]



    plt.plot(x_vals, y_vals, label='Alpha Beta', color='orange')
    plt.plot(x_vals, y_vals_mm, label='Minimax', color='blue')
    plt.legend()
    plt.xticks([1, 2, 3, 4, 5, 6], ('1', '2', '3', '4', '5', '6'))
    plt.ylabel('Average Running Time of Finding Move')
    plt.xlabel('Max Depth')
    plt.title('Comparing Alpha Beta to Minimax Runtime')
    plt.show()




if __name__ == '__main__':

    print('look at function calls below')
    # game = drop_20_chips()
    # game.new_print_board()
    # print(game.turn)
    # compare_heuristics()

    # compare_depth_times()

    # compare_depth_times_ab()

    # compare_mm_to_ab()






