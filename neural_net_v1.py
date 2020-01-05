import sys 
import numpy as np
import os 
import time 
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior() 

class NeuralNetwork:
  model_folder = './neural_nets/'

  x = tf.placeholder(tf.float32, shape=[None, 6, 7], name='input_placeholder')
        
  nn = tf.layers.flatten(x, name='input')
  nn = tf.layers.dense(nn, 256, activation=tf.nn.relu)
  nn = tf.layers.dense(nn, 256, activation=tf.nn.relu)
  nn = tf.layers.dense(nn, 256, activation=tf.nn.relu)
  last_layer = tf.layers.dense(nn, 7, name='output')
  saver = tf.train.Saver()


  def convert_board(self, board, turn):
    state = np.array(np.transpose(board))
    if turn == "B":
      for row in range(6):
        for col in range(7):
          if state[row][col] == "B":
            state[row][col] = 1
          elif state[row][col] == "R":
            state[row][col] = -1
          elif state[row][col] == None:
            state[row][col] = 0
    elif turn == "R":
      for row in range(6):
        for col in range(7):
          if state[row][col] == "R":
            state[row][col] = 1
          elif state[row][col] == "B":
            state[row][col] = -1  
          elif state[row][col] == None:
            state[row][col] = 0   
    return state

    

  def find_move(self, board, turn):
      state = self.convert_board(board, turn)
      input_data = state
      input_data = input_data.reshape([1, input_data.shape[0], input_data.shape[1]])
  
      with tf.Session() as sess:

          self.saver.restore(sess, self.model_folder)

          output = sess.run(self.last_layer, feed_dict={self.x: input_data})
          move = np.argmax(output)
      return int(move)


"takes in a board state and returns the col_idx the neural net chooses."
def neural_move(board, turn):
  print(board)
  print(turn)
  model_folder = './neural_nets/'
  x = tf.placeholder(tf.float32, shape=[None, 6, 7], name='input_placeholder')
        
  nn = tf.layers.flatten(x, name='input')
  nn = tf.layers.dense(nn, 256, activation=tf.nn.relu)
  nn = tf.layers.dense(nn, 256, activation=tf.nn.relu)
  nn = tf.layers.dense(nn, 256, activation=tf.nn.relu)
  last_layer = tf.layers.dense(nn, 7, name='output')

  #change board to correct form
  state = np.array(np.transpose(board))
  if turn == "B":
    for row in range(6):
      for col in range(7):
        if state[row][col] == "B":
          state[row][col] = 1
        elif state[row][col] == "R":
          state[row][col] = -1
        elif state[row][col] == None:
          state[row][col] = 0
  elif turn == "R":
    for row in range(6):
      for col in range(7):
        if state[row][col] == "R":
          state[row][col] = 1
        elif state[row][col] == "B":
          state[row][col] = -1  
        elif state[row][col] == None:
          state[row][col] = 0   

  saver = tf.train.Saver()

  input_data = state
  input_data = input_data.reshape([1, input_data.shape[0], input_data.shape[1]])
  
  with tf.Session() as sess:

      saver.restore(sess, model_folder)

      output = sess.run(last_layer, feed_dict={x: input_data})
      move = np.argmax(output)

  return move


# board = [
  
#   [None, None, None, "R", "R", "R"], 
#   [None, None, None, "B", "B", "B"], 
#   [None, None, None, None, None, None], 
#   [None, None, None, None, None, None], 
#   [None, None, None, None, None, None], 
#   [None, None, None, None, None, None], 
#   [None, None, None, None, None, None]
#   ]
if __name__ == '__main__':
  board = [
    
    [None, None, None, None, None, None], 
    [None, None, None, 'R', 'R', 'R'], 
    [None, None, None, None, None, None], 
    [None, None, None, 'B', 'B', 'B'], 
    [None, None, None, None, None, None], 
    [None, None, None, None, None, None], 
    [None, None, None, None, None, None]
    ]

  board = [[None, None, None, None, None, None], [None, None, None, None, None, None], [None, None, None, None, None, None], [None, None, None, None, None, 'R'], [None, None, None, None, None, None], [None, None, None, None, 'B', 'B'], [None, None, None, None, None, None]]
  turn = "R"

  print("turn is " + str(neural_move(board, turn)))