import numpy as np
import time
import matplotlib.pyplot as plt
import os

# Parameters
total_games = 12000

# Variables
move_count = 0
total_dud_rounds = 0
move_history_input = np.zeros((total_games * 30, 6, 7))
move_history_output = np.zeros((total_games * 30, 7, 1))

# Filepaths
red_load_folder = './red_games/'
black_load_folder = './black_games/'
save_folder = './processed_games/'

# Get a list of all files in the load folder. (not including hidden files)
def get_all_files(flder):
  return [f for f in os.listdir(flder) if not f.startswith('.')]
  

all_games_red = get_all_files(red_load_folder)
all_games_black = get_all_files(black_load_folder)

assert len(all_games_red) == len(all_games_black)

if total_games > len(all_games_red):
    print('Warning: Restricting total games from {} to {}'.format(total_games, len(all_games_red)))
    total_games = len(all_games_red)

#find last round
def find_last_round(board):
  for round in range(board.shape[0]):
    if round == 0:
      first_round = True 
    else:
      first_round = False
    current_game_abs = np.abs(board[round])
    current_game_sum = np.sum(current_game_abs)
    if current_game_sum == 0 and (not first_round):
        round -= 1
        break
  return round 

def plot_board(board):
    ''' This function reads a saved board and plots Red and black tokens in 
    their correct positions.

    Input: Numpy Array of Shape(6,7) containing:

    1 represents bots tokens
    -1 represents others tokens
    0 represents an open space

    Returns:
    Shows a plot of the current board
    '''
    
    # Create New Figure
    plt.figure() 
    
    # Iterate over all board rows
    for row in range(board.shape[0]):
        
        # Iterate over all board rows
        for col in range(board.shape[1]):
            
            # Plot all tokens that = 1 as black
            if board[5-row][col] == 1:
                plt.scatter(col, row, c='Black', s=500, edgecolors='black')
            
            # Plot all tokens that = -1 as red
            if board[5-row][col] == -1:
                plt.scatter(col, row, c='Blue', s=500, edgecolors='black')
    
    plot_margin = 0.4                         # Padding around edges
    plt.grid()                                # Turn on grid
    plt.ylim(-plot_margin, 5 + plot_margin)   # Set Y Limits
    plt.xlim(-plot_margin, 6 + plot_margin)   # Set X Limits
    plt.show()                                # Show Plot

def find_winning_moves(board):

    move_idx = []                                       # List to hold any winning moves
    valid_cols = np.where(board[0] == 0)[0]             # Calculate valid columns we can put token in
    win_flag = False
    any_win_flag = False

    # Iterate over all valid columns
    for col in valid_cols:
        new_board = board.copy()                        # Copy the current board to a new board
        row_options = np.where(board[:, col] == 0)[0]   # For each column, calc which rows are empty
        lowest_row = np.max(row_options)                # The lowest row will be the maximum index row
        new_board[lowest_row][col] = 1                  # Put a token in the new position

        win_flag = four_in_a_row(new_board)             # Check if this play would win the game. Win_flag will be true if so

        # If Win, record column as a winning play
        if win_flag is True:
            any_win_flag = True
            move_idx.append(col)                        # Add the win to the list of possible winning moves

    return any_win_flag, np.array(move_idx)             # Convert list of possible moves to a numpy array

def four_in_a_row(board):

    win_flag = False

    # Check Diagonal (P1 = Bottom Left - P4 = Top Right)
    for p1_col in range(4):
        p2_col = p1_col + 1
        p3_col = p2_col + 1
        p4_col = p3_col + 1

        for p1_row in range(3, 6):
            p2_row = p1_row - 1
            p3_row = p2_row - 1
            p4_row = p3_row - 1

            p1 = board[p1_row][p1_col]
            p2 = board[p2_row][p2_col]
            p3 = board[p3_row][p3_col]
            p4 = board[p4_row][p4_col]

            if np.sum([p1, p2, p3, p4]) == 4:
                win_flag = True

    # Check Diagonal (P1 = Top Left - P4 = Bottom Right)
    for p1_col in range(3):
        p2_col = p1_col + 1
        p3_col = p2_col + 1
        p4_col = p3_col + 1

        for p1_row in range(3):
            p2_row = p1_row + 1  # Careful, we swap sign to +
            p3_row = p2_row + 1  # Careful, we swap sign to +
            p4_row = p3_row + 1  # Careful, we swap sign to +

            p1 = board[p1_row][p1_col]
            p2 = board[p2_row][p2_col]
            p3 = board[p3_row][p3_col]
            p4 = board[p4_row][p4_col]

            if np.sum([p1, p2, p3, p4]) == 4:
                win_flag = True

    # Check for row win
    for row in range(board.shape[0]):
        for p1 in range(4):
            p4 = p1 + 3

            section = board[row][p1:p4+1]

            if np.sum(section) == 4:
                win_flag = True

    # Check for column win
    for col in range(board.shape[1]):
        for p1 in range(3):
            p4 = p1 + 3
            section = board[:, col][p1:p4+1]
            if np.sum(section) == 4:
                win_flag = True

    return win_flag

# Iterate over the total number of games we want to store
for game_num in range(total_games):

    # Load Red and black player's history
    board_red = np.load(red_load_folder + all_games_red[game_num])
    board_black = np.load(black_load_folder + all_games_black[game_num])

    # Find Longest Round
    last_round_black = find_last_round(board_black)
    last_round_red = find_last_round(board_red)
    last_round = np.maximum(last_round_black, last_round_red)

    # Keep a copy of the last board
    if last_round_black == last_round:
        final_board = board_black[last_round]
        board = board_black.copy()
        next_turn = 'black'
    elif last_round_red == last_round:
        final_board = board_red[last_round]
        board = board_red.copy()
        next_turn = 'red'

    # Keep a Copy of black and Red Tokens
    black_idx = np.where(final_board == 1)
    red_idx = np.where(final_board == -1)

    # Determine Winner
    win_flag = False
    blank_board = np.zeros_like(board_black[0])
    if next_turn == 'black':

        blank_board[black_idx] = 1
        blank_board[red_idx] = -1

        win_flag, move_idx = find_winning_moves(blank_board)

        if win_flag is True:
            winner = 'black'
        else:
            winner = 'red'
    elif next_turn == 'red':

        blank_board[black_idx] = -1
        blank_board[red_idx] = 1

        win_flag, move_idx = find_winning_moves(blank_board)

        if win_flag is True:
            winner = 'red'
        else:
            winner = 'black'

    # Store index's of winning and loser player
    if winner == 'black':
        win_idx = np.where(board == 1)
        lose_idx = np.where(board == -1)
    elif winner == 'red':
        win_idx = np.where(board == -1)
        lose_idx = np.where(board == 1)

    # Create Winner Board
    winner_board = np.zeros_like(board)
    winner_board[win_idx] = 1
    winner_board[lose_idx] = -1

    # Skip dud matches
    if last_round <= 2:
        total_dud_rounds += 1
        print('Total Dud Matches = {}. Game {} is tiny'.format(total_dud_rounds, game_num))
        continue

    # Iterate over all rounds
    for round in range(last_round+1):
        current_board = winner_board[round]                             # Get the current Board
        move = None                                                     # Set move to none, we can then check that the move is not none as a bug check

        # If we aren't in the last round, determine the move we should make
        if round != last_round:
            next_board = winner_board[round + 1]                        # Get the next board
            board_diff = next_board - current_board                     # Calculate the difference between boards
            board_diff[board_diff == -1] = 0                            # Remove the opponents move for now
            col_sum = np.sum(board_diff, axis=0)                        # Reduce the 2D matrix to 1D Matrix by summing columns. Only 1 column will have a 1
            move = np.where(col_sum == 1)[0]                            # Find the column we should place the token

        # If this is the last Round, determine the winning move
        elif round == last_round:

            any_win_flag, move_idx = find_winning_moves(current_board)

            # If it's the last round and we can't find a winning move, delete game
            if any_win_flag is False:
                total_dud_rounds += 1
                print('Total Dud Matches = {}. No winner in game {}'.format(total_dud_rounds, game_num))
                dud_rounds = round
                blank_board = np.zeros_like(move_history_input[0])
                blank_output = np.zeros_like(move_history_output[0])
                for dud_round in range(dud_rounds):
                    move_history_input[move_count] = blank_board
                    move_history_output[move_count] = blank_output
                    move_count -= 1
                continue

            np.random.shuffle(move_idx)                                 # Shuffle the array
            move = move_idx[0]                                          # Select the shuffled array's first index as the winning move

        # Record History
        move_history_input[move_count] = winner_board[round]            # Set the input data to the current board
        move_history_output[move_count][move] = 1                       # Set the output data to the move made by the winning player
        move_count += 1                                                 # Increment the move count by 1

# Constrain the total number of rounds to the number we have calculated
move_history_input = move_history_input[:move_count-1]
move_history_output = move_history_output[:move_count-1]

# Save Data
np.save(save_folder + 'input_data.npy', move_history_input)
np.save(save_folder + 'output_data.npy', move_history_output)
