from alpha_beta_class import AlphaBeta
from heuristics_final import heuristic5
from connect4 import Connect4
from random import randint





def run_game():
  game = Connect4()
  ab_obj1 = AlphaBeta(2, heuristic5, 'B')
  ab_obj2 = AlphaBeta(2, heuristic5, 'R')

  stop_conditions = ('B_WINS', 'R_WINS', 'TIE')

  while game.turn not in stop_conditions:

    # force random column on first move
    if game.total_moves == 0:
      random_column = randint(0, 6)
      game.drop_chip(random_column)

    elif game.turn == 'R':

      score, move = ab_obj2.find_move(game)
      game.drop_chip(move)

    elif game.turn == 'B':
      score, move = ab_obj1.find_move(game)
      game.drop_chip(move)

  game.new_print_board()
  print(game.turn)


def run_many_games(amount):


  while amount > 0:

    run_game()

    amount -= 1
      


if __name__ == '__main__':
  run_many_games(3)


