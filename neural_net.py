import numpy as np
import matplotlib.pyplot as plt
import time
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior() 

def plot_winner_board(board):
    plt.figure()
    for row in range(board.shape[0]):
        for col in range(board.shape[1]):
            if board[5-row][col] == 1:
                plt.scatter(col, row, c='Black', s=500, edgecolors='black')

            if board[5-row][col] == -1:
                plt.scatter(col, row, c='Blue', s=500, edgecolors='black')
    plt.grid()
    plt.ylim(-1, 6)
    plt.xlim(-1, 7)
    plt.show()
    plt.close()

# NN Parameters
lr = 0.0001
epochs = 200
val_split = 0.1
eval_split = 0.05
batch_size = 1024

# Folder Paths
data_load_folder = './processed_games/'
nn_save_folder = './neural_nets/'

# Load Data
move_history_input = np.load(data_load_folder + 'input_data.npy')
move_history_output = np.load(data_load_folder + 'output_data.npy')

# Check Number Of Samples
# print('Input Data Shape = {}:'.format(move_history_input.shape))
# print('Output Data Shape = {}:'.format(move_history_output.shape))

# Reshape output to shape (7, )
move_history_output = move_history_output.reshape(move_history_output.shape[0], move_history_output.shape[1])


def split_data(move_history_input, move_history_output, val_split, eval_split):

    # Calculate the number of training/validation and evaluation samples
    num_val = int(move_history_input.shape[0] * val_split)
    num_eval = int(move_history_input.shape[0] * eval_split)
    num_train = move_history_input.shape[0] - num_val - num_eval

    # Create an array from 0 -> total number of samples
    all_idx = np.arange(0, move_history_input.shape[0], 1)

    # Randomly shuffle the index's (Just the array we created, not the actual data)
    np.random.shuffle(all_idx)

    # Assign training/validation/evaluation index's
    train_idx = all_idx[:num_train]
    val_idx = all_idx[num_train: num_train + num_val]
    eval_idx = all_idx[num_train + num_val:]

    # Create Training/Validation/Evaluation Data by assigning the data from Move_History at each index
    train_input_data, train_output_data = move_history_input[train_idx], move_history_output[train_idx]
    val_input_data, val_output_data = move_history_input[val_idx], move_history_output[val_idx]
    eval_input_data, eval_output_data = move_history_input[eval_idx], move_history_output[eval_idx]
    
    print('Training Samples = {}, Validation Samples = {}, Evaluation Samples = {}'.format(train_input_data.shape[0], val_input_data.shape[0], eval_input_data.shape[0]))
    return train_input_data, train_output_data, val_input_data, val_output_data, eval_input_data, eval_output_data


# Split data into training, validation and evaluation
train_in_data, train_out_data, val_in_data, val_out_data, eval_in_data, eval_out_data = split_data(move_history_input, move_history_output, val_split, eval_split)

# # Look at an example Input/Output
# example_num = 1
# print('\nExample Output #{}:\n  {}'.format(example_num, move_history_output[example_num]))
# print('\nExample Input #{}:'.format(example_num))
# plot_winner_board(move_history_input[example_num])

# Create Placeholders
x = tf.placeholder(tf.float32, shape=[None, 6, 7], name='input_placeholder')
y = tf.placeholder(tf.float32, shape=[None, 7], name='output_placeholder')

# Create Network
nn = tf.layers.flatten(x, name='input')                 # Flatten Board
nn = tf.layers.dense(nn, 256, activation=tf.nn.relu)    # Layer 1 - Fully Connected with 256 Nodes
nn = tf.layers.dense(nn, 256, activation=tf.nn.relu)    # Layer 2 - Fully Connected with 256 Nodes
nn = tf.layers.dense(nn, 256, activation=tf.nn.relu)    # Layer 3 - Fully Connected with 256 Nodes
last_layer = tf.layers.dense(nn, 7, name='output')      # Output Layer


# print(x)
# print(y)
# print(last_layer)

# Define Loss Function
loss_function = tf.nn.softmax_cross_entropy_with_logits_v2(logits=last_layer, labels=y)
loss = tf.reduce_mean(loss_function)

# Create Optimiser
learning_step = tf.train.AdamOptimizer(lr)
optimiser = learning_step.minimize(loss)

# Create Accuracy Evaluation
correct = tf.equal(tf.argmax(last_layer, axis=1), tf.argmax(y, axis=1))
acc = tf.reduce_mean(tf.cast(correct, 'float'))

def split_into_batches(train_in_data, train_out_data, batch_size):

    num_batches = int(np.floor(train_in_data.shape[0]/batch_size))

    train_in_batches = np.zeros((num_batches, batch_size, train_in_data.shape[1], train_in_data.shape[2]))
    train_out_batches = np.zeros((num_batches, batch_size, train_out_data.shape[1]))

    samples = np.arange(0, num_batches * batch_size, step=1)
    np.random.shuffle(samples)

    for i in range(train_in_batches.shape[0]):
        start_num = i * batch_size
        end_num = start_num + batch_size

        batch_samples = samples[start_num:end_num]

        train_in_batches[i] = train_in_data[batch_samples]
        train_out_batches[i] = train_out_data[batch_samples]

    return train_in_batches, train_out_batches

# Create Saver
saver = tf.train.Saver()
best_acc = 0

# Train Network
with tf.Session() as sess:

    # Initialise Variables
    sess.run(tf.global_variables_initializer())
    
    epoch_train_acc = sess.run(acc, feed_dict={x: train_in_data, y: train_out_data})
    epoch_val_acc = sess.run(acc, feed_dict={x: val_in_data, y: val_out_data})
    
    print('Randomly Initialised Weight/Biases: Train Acc = {:.3f}%, Val Acc = {:.3f}%'.format(epoch_train_acc * 100, epoch_val_acc * 100))

    # Iterate over all Epochs
    for epoch in range(epochs):

        # Split training data into batches
        train_in_batches, train_out_batches = split_into_batches(train_in_data, train_out_data, batch_size)

        # Iterate over all batches
        for batch in range(train_in_batches.shape[0]):

            _, batch_cost = sess.run([optimiser, loss], feed_dict={x: train_in_batches[batch], y: train_out_batches[batch]})

        # Evaluate Training and Validation Accuracy
        epoch_train_acc = sess.run(acc, feed_dict={x: train_in_data, y: train_out_data})
        epoch_val_acc = sess.run(acc, feed_dict={x: val_in_data, y: val_out_data})

        # Save model if it is an improvement
        if epoch_val_acc > best_acc:
            best_acc = epoch_val_acc
            saver.save(sess, nn_save_folder)
        
        # Print results every 50 epochs
        if epoch < 10 or epoch % 25 == 0:
            print('After {} Epochs: Single Batch Cost = {:.3f}, Train Acc = {:.3f}%, Val Acc = {:.3f}%'.format(epoch+1, batch_cost, epoch_train_acc * 100, epoch_val_acc * 100))

    # Load Saved Session
    saver.restore(sess, nn_save_folder)

    # After Training, Check Evaluation Accuracy
    eval_acc = sess.run(acc, feed_dict={x: eval_in_data, y: eval_out_data})
    print('Evaluation Acc = {:.3f}%'.format(eval_acc * 100))