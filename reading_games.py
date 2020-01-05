import numpy as np
import matplotlib.pyplot as plt
import os

def plot_board(board):
    ''' This function reads a saved board and plots Red and Yellow tokens in 
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
            
            # Plot all tokens that = 1 as yellow
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

# Get a list of all files in the load folder. (not including hidden files)
def get_all_files(flder):
  return [f for f in os.listdir(flder) if not f.startswith('.')]

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

#parameters to change 
folder = './black_games/'
game_num_to_plot = 0
round_to_plot = 9 

games = get_all_files(folder)
current_game = np.load(folder + games[game_num_to_plot])

round = find_last_round(current_game)


print('Final Round = {}'.format(round))
final_board = current_game[round]
# Plot Board
plot_board(final_board)