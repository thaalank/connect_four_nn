from connect4 import Connect4
import random

def manage_human_input(c):
    x = input("it is " + c.turn + "'s turn enter a column\n")
    if x != '' and (int(x) in range(c.columns)) and (not c.is_column_full(int(x))):

        c.drop_chip(int(x))
        c.print_board()
    else:
        print("invalid input")
        return False
    return True

'''
THIS IS A RANDOM AI... RANDOMLY CHOOSE A COLUMN TO DROP IT IN 
'''
def manage_ai_input(c):


    # get the available columns
    valid_moves = c.available_moves()
    # an array of boolean values: [true, true, false....

    # randomly pick a number within the number of columns
    rand1 = random.randint(0, len(valid_moves)-1)

    # randomly pick one


    # drop the chip in that column
    c.drop_chip(valid_moves[rand1])
    # print the board
    # c.print_board()

def runPVE():
    x = input("would you like to play a game against our random ai? yes or no\n")
    if x == 'yes':
        print("playing game")

        c = Connect4()
        c.print_board()

        # human is always blue
        human = "B"

        while c.turn != "B_WINS" and c.turn != "R_WINS":

            if c.turn == human:
                # if it is the humans turn: manage the humans input
                # TODO: bug here
                if not manage_human_input(c): continue

            else:
                #         manage the ai's input
                manage_ai_input(c)

        print("GAME IS OVER")
        print(c.turn)


if __name__ == "__main__":
    runPVE()