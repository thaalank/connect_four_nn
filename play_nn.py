from connect4 import Connect4
from neural_net_v1 import neural_move
from neural_net_v1 import NeuralNetwork



neural_obj = NeuralNetwork()

game = Connect4()

final_states = ('B_WINS', 'R_WINS', 'TIE')



while game.turn not in final_states:
  game.new_print_board()


  if game.turn == 'R':
    # print(game.board)
    nn_column = neural_obj.find_move(game.board, 'R')
    game.drop_chip(nn_column)

  else:
    human_move = int(input('It is your turn, enter a valid column \n'))
    game.drop_chip(human_move)

game.new_print_board()
print(game.turn)