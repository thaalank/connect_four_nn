# packages for
import numpy as np
from time import time
from colorama import Fore, Back, Style, init
from random import randint
from sty import fg, bg, ef, rs
init()
# print(Fore.RED + 'hello')



'''
JUST HAVE EMPTY LISTS THAT WE 
'''
class Connect4:
    rows = 6
    columns = 7
    most_recent_move = None
    turn = None
    total_moves = 0


    def __init__(self, board=None, turn=None, last_move=None, total_moves=0):

        if board is None and turn is None and last_move is None:
            self.last_move = last_move
            self.board = self.new_board()
            self.turn = "B" if randint(0, 1) else "R"
            #for saving each round
            self.black_round = 0
            self.red_round = 0
            self.first = self.turn 

            self.total_moves = 0

        else:
             #for saving each round
            self.black_round = 0
            self.red_round = 0
            self.first = self.turn 
            self.board = board
            self.turn = turn
            self.last_move = last_move
            self.total_moves = total_moves

        #creating file name for black states 
        time_str = (str(time()))
        self.filename_black = ('./black_games/' 
        + (time_str)
        + '.npy')
        #creating file for red states
        self.filename_red = ('./red_games/' 
        + (time_str)
        + '.npy')

    def __deepcopy__(self, memodict={}):
        return Connect4(self.board, self.turn)

    def make_column(self):
        return [None for i in range(self.rows)]

    def new_board(self):
        return [self.make_column() for i in range(self.columns)]
    
    def get_board(self):
        return self.board
    
    def get_turn(self):
        return self.turn 

    def get_col(self, col):
        return self.board[col]

    def get_row(self, row):
        return [self.board[j][row] for j in range(self.columns)]

    def get_chip(self, row, col):
        return self.board[col][row]

    def new_print_board(self):
        from termcolor import colored, cprint
        if (self.total_moves == 0):
            cprint("Hello! Welcome to Connect Four!", color='red', on_color=None, attrs=['bold'])
            cprint("Choose a valid move to begin playing", color='red', on_color=None, attrs=['blink'])
        # print('Hello There welcome to the board printing function')

        # cprint('Hello, World!', 'green', 'on_red', end='')

        board = self.board

        # print(chr(175) + chr(175) + chr(175) + chr(175) + chr(175) + chr(175) + chr(175) + chr(175))
        for i in range(len(board[0])):
            cprint('|', 'white', 'on_cyan', end='')
            # row_string = "|"
            for j in range(len(board)):
                if board[j][i] is None:
                    # print('FOUND A  NULL')
                    cprint('  |', 'white', 'on_cyan', end='')
                    # row_string += " |"
                else:
                    # print(board[j][i])
                    # print blue chip
                    chip = board[j][i]
                    red_circle = u"\U0001F534"
                    black_circle = u"\U000026AB"
                    if (chip == 'R'):
                        choose = red_circle
                    else:
                        choose = black_circle
                    cprint(choose, 'white', 'on_cyan',end='') # 'grey', 'on_blue' if chip == 'B' else 'on_red'
                    cprint('|', 'white', 'on_cyan', end='')
            print()
            # row_string += board[j][i] + "|"
            # print(row_string)

            # self.prCyan(row_string)
        cprint('  0  1  2  3  4  5  6')
        print()

        # print('Goodbye from the board printing function')

    def print_board(self):
        board = self.board

        # print(chr(175) + chr(175) + chr(175) + chr(175) + chr(175) + chr(175) + chr(175) + chr(175))
        for i in range(len(board[0])):
            row_string = "|"
            for j in range(len(board)):
                if(board[j][i] == None):
                    row_string += " |"
                else:
                    row_string += board[j][i] + "|"
            print(row_string)
            # self.prCyan(row_string)
        print(' 0 1 2 3 4 5 6')

        # print(chr(175) + chr(175) + chr(175) + chr(175) + chr(175) + chr(175) + chr(175) + chr(175))



    def is_tie_condition(self):
        # print('calling is tie')
        # everything will be true
        # if total length of all the arrays is 7*6 then it's a tie
        # print(self.total_moves)

        if self.total_moves == 42:
            return True

        # column_fulls = [self.is_column_full(col) for col in range(self.columns)]
        # print(column_fulls)
        # if False in column_fulls:
        #     return False
        # else:
        #     return True



            # check if every single column is full... do this after you check for win conditions since the checks happen within drop_chip


    def flip_turn(self):
        if self.turn == "B":
            self.turn = "R"
        else:
            self.turn = "B"


    def drop_chip(self, col):
        self.total_moves += 1

        # instead of having an array of values preset...
        # just have a list that you append to in drop_chip
        # only print_board is what really matters to a human
        # if everything else works it's much more memory efficient - wider loops
        col_to_drop_in = self.board[col]
        col_to_drop_in.reverse()
        index = 0
        # print(col_to_drop_in)
        for row in col_to_drop_in:
            if row == None:
                col_to_drop_in[index] = self.turn
                break
            index += 1
        col_to_drop_in.reverse()
        # print(self.rows - index - 1, col)
        self.board[col] = col_to_drop_in

        # print(f"chip went into position: {self.rows-index-1, col}")
        self.last_move = ((self.rows - index - 1), col)
        if self.check_win_conditions(self.rows - index - 1, col, self.turn):
            # print("GAME OVER")
            self.turn = self.turn + "_WINS"
        elif self.is_tie_condition():
            # print("GAME IS A TIE")
            self.turn = "TIE"
        else:
            self.flip_turn()

        #saving the states of each game 
        state = np.array(np.transpose(self.board))
        if self.black_round == 0: 
            current_board = np.zeros((30,6,7))
            np.save(self.filename_black, current_board)
        if self.red_round == 0:
            game_history = np.zeros((30,6,7))
            np.save(self.filename_red, game_history)
        if self.black_round == 0 and self.first == "B":
            self.black_round += 1
        if self.red_round == 0 and self.first == "R":
            self.red_round += 1 
        else:
            current_board = np.load(self.filename_black)
            game_history = np.load(self.filename_red)

        if self.turn == "B":
            for row in range(6):
                for col in range(7):
                    if state[row][col] == "B":
                        current_board[self.black_round][row][col] = 1
                    elif state[row][col] == "R":
                        current_board[self.black_round][row][col] = -1
            np.save(self.filename_black, current_board)
            self.black_round += 1
        elif self.turn == "R":
            for row in range(6):
                for col in range(7):
                    if state[row][col] == "R":
                        game_history[self.red_round][row][col] = 1
                    elif state[row][col] == "B":
                        game_history[self.red_round][row][col] = -1     
            np.save(self.filename_red, game_history) 
            self.red_round += 1    
        #end of saving states

        # print(self.board)
        self.most_recent_move = col
        # self.total_moves += 1
        return self.rows - index -1, col



    def prCyan(self, skk):
        print("\033[96m {}\033[00m".format(skk))

    # return True if column col is full, False otherwise
    # list.index(el) throws ValueError if el not in list
    def is_column_full(self, col):
        full_column = self.board[col]

        is_full = True

        for elt in full_column:
            if elt is None:
                is_full = False
                break
        return is_full

        # try:
        #     x = self.board[col].index(None)
        # except ValueError:
        #     x = -1
        # return x == -1

    def available_moves(self):
        """
        :return: returns the list of valid column indices one may drop a chip into
        """
        moves = [col for col in range(self.columns) if not self.is_column_full(col)]
        return moves

    def win_down(self, row, col):

        if row + 3 < self.rows:
            # print("row - 3 >= 0")
        #     dont have to deal with negative indices
            return self.get_chip(row, col) == self.get_chip(row+1, col) == \
                   self.get_chip(row+2, col) == self.get_chip(row+3, col)

        return False

    def get_up_to_7_vertical(self, row, col):

        the_list_of_seven = [self.get_chip(row, col)]

        # do 3 times if possible
        # go LEFT 3 times
        # PREPEND THESE CHIPS
        for x in range(3):
            next_index = (row - x - 1, col)
            # print(next_index)
            # see if getting the chip is possible
            if next_index[0] >= 0:
                the_list_of_seven.insert(0, self.get_chip(next_index[0], next_index[1]))

        for x in range(3):
            next_index = (row + x + 1, col)
            # print(next_index)
            # see if getting the chip is possible
            if next_index[0] < self.rows:
                the_list_of_seven.append(self.get_chip(next_index[0], next_index[1]))

        return the_list_of_seven

    def get_up_to_7_horizontal(self, row, col):
        the_list_of_seven = [self.get_chip(row, col)]

        # do 3 times if possible
        # go LEFT 3 times
        # PREPEND THESE CHIPS
        for x in range(3):
            next_index = (row, col - x - 1)
            # print(next_index)
            # see if getting the chip is possible
            if next_index[1] >= 0:
                the_list_of_seven.insert(0, self.get_chip(next_index[0], next_index[1]))

        for x in range(3):
            next_index = (row, col + x + 1)
            # print(next_index)
            # see if getting the chip is possible
            if next_index[1] < self.columns:
                the_list_of_seven.append(self.get_chip(next_index[0], next_index[1]))

        return the_list_of_seven


    # def win_horizontal(self, row, turns):
    #
    #     for i, chip in enumerate(self.get_row(row)):
    #         if chip == turns:
    #             try:
    #                 if self.get_chip(row, i) == self.get_chip(row, i+1) == self.get_chip(row, i+2) == self.get_chip(row, i+3):
    #                     return True
    #             except IndexError as e:
    #                 return False

    '''
    Checks a list for 4 of the same thing in a row 
    '''
    def check_list_for_win(self, lst):

        if len(lst) < 4:
            return False
        else:
            is_winner = False
            for index, chip in enumerate(lst):
                if index + 3 == len(lst):
                    break
                if lst[index] == lst[index+1] == lst[index+2] == lst[index+3]:
                    is_winner = True
                    break

            return is_winner

    '''
    From a given chip position 
    Go left and up pre-pending chips
    then go right and down appending chips
    '''
    def win_diagonal_backward_slash(self, row, col):

        # print(self.get_chip(row, col))
        the_list_of_seven = [self.get_chip(row, col)]

        # do 3 times if possible
        # go up and left 3 times
        # PREPEND THESE CHIPS
        for x in range(3):
            next_index = (row - x - 1, col - x - 1)
            # print(next_index)
            # see if getting the chip is possible
            if next_index[0] >= 0 and next_index[1] >= 0:
                the_list_of_seven.insert(0, self.get_chip(next_index[0], next_index[1]))

        # do this 3 times if possible
        # go down and to the right 3 times
        # APPEND THESE CHIPS
        for x in range(3):
            next_index = (row + x + 1, col + x + 1)
            # print(next_index)
            if next_index[0] < self.rows and next_index[1] < self.columns:
                # print(next_index)
                the_list_of_seven.append(self.get_chip(next_index[0], next_index[1]))

        # print(self.check_list_for_win(the_list_of_seven))
        return the_list_of_seven

    '''
    From a given chip position 
    Go left and down pre-pending chips
    then go right and up appending chips
    '''
    def win_diagonal_forward_slash(self, row, col):

        the_list_of_seven = [self.get_chip(row, col)]

        # prepend 3 chips
        for x in range(3):
            next_index = (row+x+1, col-x-1)
            # see if getting the chip is possible
            if next_index[0] < self.rows and next_index[1] >= 0:
                the_list_of_seven.insert(0, self.get_chip(next_index[0], next_index[1]))

        # append 3 chips
        for x in range(3):
            next_index = (row-x-1, col+x+1)
            # see if getting the chip is possible
            if next_index[0] >= 0 and next_index[1] < self.columns:
                the_list_of_seven.append(self.get_chip(next_index[0], next_index[1]))

        return the_list_of_seven

    '''
    Overall check for win condition
    Whenever a chip is dropped, immediately check if it has won the game
    If we check whenever a chip is dropped - more efficient
    '''
    def check_win_conditions(self, row, col, chip):
        is_win = self.check_list_for_win(self.get_up_to_7_horizontal(row, col)) or \
               self.win_down(row, col) or \
               self.check_list_for_win(self.win_diagonal_forward_slash(row, col)) or \
               self.check_list_for_win(self.win_diagonal_backward_slash(row, col))
        #
        # if is_win:
        #     print("GAME OVER")
        return is_win





def test_diagonal_backwards():
    c1 = Connect4()
    c1.drop_chip(6)
    c1.drop_chip(5)
    c1.drop_chip(5)
    c1.drop_chip(4)
    c1.drop_chip(4)
    c1.drop_chip(3)
    c1.drop_chip(4)
    c1.drop_chip(3)
    c1.drop_chip(3)
    c1.drop_chip(0)
    c1.drop_chip(3)

    c1.print_board()
    print(c1.win_diagonal_backward_slash(row=2, col=3))
    print(c1.check)



def test_diagonal_forward():

    c1 = Connect4()
    c1.drop_chip(0)
    c1.drop_chip(1)
    c1.drop_chip(1)
    c1.drop_chip(2)
    c1.drop_chip(2)
    c1.drop_chip(6)
    c1.drop_chip(2)
    c1.drop_chip(3)
    c1.drop_chip(3)
    c1.drop_chip(3)
    c1.drop_chip(3)
    if c1.turn in ['R', 'B']:
        raise Exception
    print(c1.turn)
    c1.print_board()


def test_is_column_full():
    game = Connect4()
    for x in range(6):
        game.drop_chip(0)

    for x in range(6):
        game.drop_chip(1)

    for x in range(6):
        game.drop_chip(2)

    for x in range(6):
        game.drop_chip(3)

    for x in range(6):
        game.drop_chip(4)

    for x in range(6):
        game.drop_chip(5)

    for x in range(6):
        game.drop_chip(6)

    # print(game.is_column_full(0))
    print(game.turn)

if __name__ == '__main__':
    # test_diagonal_forward()
    # test_diagonal_backwards()
    # test_diagonal_forward()
    # print('finished testing')

    test_is_column_full()




# p1 = Connect4()
#
# p1.drop_chip(0)
# p1.print_board()
# print(p1.get_forward_diag(5, 0))
#
#
# p1.drop_chip(1)
# p1.drop_chip(1)
# p1.print_board()
# print(p1.get_forward_diag(5, 0))

# p1.print_board()
