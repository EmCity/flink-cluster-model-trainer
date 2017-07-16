import tensorflow as tf
import pandas as pd
import src.misc.evaluation as eval
import numpy as np

training_X = pd.read_csv("train_x.csv", index_col=0)
training_Y = pd.read_csv("train_y.csv", index_col=0)

testing_X = pd.read_csv("test_x.csv", index_col=0)
testing_Y = pd.read_csv("test_y.csv", index_col=0)

x_dim = len(training_X.columns)
y_dim = len(training_Y.columns)

x = tf.placeholder(tf.float32, [None, x_dim])
y = tf.placeholder(tf.float32, [None, y_dim])

#tf.nn.l2_normalize(x, dim=0)

# Create model
def multilayer_perceptron(x, weights, biases):
    # Hidden layer with RELU activation
    layer_1 = tf.add(tf.matmul(x, weights['h1']), biases['b1'])
    layer_1 = tf.nn.relu(layer_1)
    # Hidden layer with RELU activation
    layer_2 = tf.add(tf.matmul(layer_1, weights['h2']), biases['b2'])
    layer_2 = tf.nn.relu(layer_2)
    # Output layer with linear activation
    out_layer = tf.matmul(layer_2, weights['out']) + biases['out']
    return out_layer

# Store layers weight & bias
neurons = 150
weights = {
    'h1': tf.Variable(tf.random_normal([x_dim, neurons])),
    'h2': tf.Variable(tf.random_normal([neurons, neurons])),
    'out': tf.Variable(tf.random_normal([neurons, y_dim]))
}
biases = {
    'b1': tf.Variable(tf.random_normal([neurons])),
    'b2': tf.Variable(tf.random_normal([neurons])),
    'out': tf.Variable(tf.random_normal([y_dim]))
}
# Construct model
pred = multilayer_perceptron(x, weights, biases)

# Define loss and optimizer
cost_func = tf.reduce_mean(tf.abs(tf.div((y-pred), y)))
optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.05).minimize(cost_func)

# Initializing the variables
init = tf.global_variables_initializer()

# Launch the graph
with tf.Session() as sess:
    sess.run(init)
    batch_size = 1
    # Training cycle
    for epoch in range(25):
        avg_cost = 0.
        for batch in range(int(len(training_X)/batch_size)):
            x_batch = training_X[batch * batch_size: batch * batch_size + batch_size]
            #tf.nn.batch_normalization(x_batch)
            y_batch = training_Y[batch * batch_size: batch * batch_size + batch_size]
            #tf.nn.batch_normalization(y_batch)
            # Run optimization op (backprop) and cost op (to get loss value)
            _, c = sess.run([optimizer, cost_func], feed_dict={x: x_batch, y: y_batch})
            # Compute average loss
            avg_cost += c/int(len(training_X)/batch_size)
        print(avg_cost)
    # Test model
    prediction = pred.eval(feed_dict={x: testing_X}, session=sess)
    mape = eval.mape(prediction, testing_Y)

    print(mape)
    print(np.mean(mape))
