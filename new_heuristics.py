from connect4 import Connect4
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
                if arr in three_in_a_row_conditions:
                    # print('the last move taken can convert into a win')
                    # print(arr)
                    possible_conversions_this_way += 1
            except:
                continue
        total_num_conversions += possible_conversions_this_way
    # print(total_num_conversions)

    return total_num_conversions









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


'''
Returns the number of 2 in a rows that can be converted into a win![
'''
def count_2s_that_can_win(game, lastMove):
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
'''
def score_entire_board(game, player):

    red_twos_that_can_win = 0
    blue_twos_that_can_win = 0
    blue_threes_that_can_win = 0
    red_threes_that_can_win = 0

    indexed_chips = []

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


def heuristic1(game, player):
    return score_entire_board(game, player)


def test_score_board():
    game = Connect4()
    chip = game.turn
    print(chip)
    opposite_chip = 'B' if chip == 'R' else 'R'
    game.drop_chip(3)
    game.drop_chip(0)
    game.drop_chip(3)
    # game.drop_chip(0)
    # game.drop_chip(3)
    game.new_print_board()
    print('Score for Player: ' + chip + ' is: ' + str(score_entire_board(game, chip)))
    print('Score for Player: ' + opposite_chip + ' is: ' + str(score_entire_board(game, opposite_chip)))

if __name__ == '__main__':
    test_score_board()