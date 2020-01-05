from randomAI import manage_ai_input
import minimax
from connect4 import Connect4
import time

# play the random ai against another random ai and print the board after each move

# do this 10 times and record the number of times blue won and the number of times red won
NUM_TRIALS = 100

# define the AIs and the number of total wins
AI1 = "B"


# MINIMAX IS RED
AI2 = "R"
num_red_wins = 0
num_blue_wins = 0
num_ties = 0





current_time = time.time()
i = 0
while i < NUM_TRIALS:


    c = Connect4()
    # c.print_board()

    while c.turn != "B_WINS" and c.turn != "R_WINS" and c.turn != "TIE":

        if c.turn == 'B':
            manage_ai_input(c)
        else:
            minimax.manage_minimax_input(c)
            # c.print_board()

    # print("GAME IS OVER")
    # print("FINAL STATE")
    # c.print_board()
    # print(c.turn)

    if c.turn == "B_WINS":
        num_blue_wins += 1
        # print(num_blue_wins)
    elif c.turn == "R_WINS":
        num_red_wins += 1
    else:
        num_ties += 1

    i += 1


elapsed_time = time.time() - current_time
print(elapsed_time)

print("Final Results Below")
print('Number of ties is: ' + str(num_ties))
print('Number of AI1 wins is: ' + str(num_blue_wins))
print('Number of AI2 wins is: ' + str(num_red_wins))




