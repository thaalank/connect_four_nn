from connect4 import Connect4

def manage_input(c):

    x = input("it is " + c.turn + "'s turn enter a column\n")
    if (int(x) in range(c.columns)) and (not c.is_column_full(int(x))):

        c.drop_chip(int(x))
        c.print_board()
    else:
        print("invalid input")
        return False
    return True

def runPVP():
    x = input("would you like to play a game? yes or no\n")
    if x == 'yes':
        print("playing game")

        c = Connect4()
        c.print_board()

        while c.turn != "B_WINS" and c.turn != "R_WINS" and c.turn != "TIE":
            if not manage_input(c): continue

        print("GAME IS OVER")

        print(c.turn)

runPVP()