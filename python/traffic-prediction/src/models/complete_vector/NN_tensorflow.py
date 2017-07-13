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
weights = {
    'h1': tf.Variable(tf.random_normal([x_dim, 200])),
    'h2': tf.Variable(tf.random_normal([200, 500])),
    'out': tf.Variable(tf.random_normal([500, y_dim]))
}
biases = {
    'b1': tf.Variable(tf.random_normal([200])),
    'b2': tf.Variable(tf.random_normal([500])),
    'out': tf.Variable(tf.random_normal([y_dim]))
}

# Construct model
pred = multilayer_perceptron(x, weights, biases)

# Define loss and optimizer
cost_func = tf.reduce_mean(tf.div(tf.abs(pred - y), y))
optimizer = tf.train.AdagradOptimizer(learning_rate=0.001).minimize(cost_func)

# Initializing the variables
init = tf.global_variables_initializer()

# Launch the graph
with tf.Session() as sess:
    sess.run(init)

    batch_size=1
    # Training cycle
    for epoch in range(50):
        avg_cost = 0.
        for batch in range(int(len(training_X)/batch_size)):
            x_batch = training_X[batch * batch_size: batch * batch_size + batch_size]
            y_batch = training_Y[batch * batch_size: batch * batch_size + batch_size]
            # Run optimization op (backprop) and cost op (to get loss value)
            _, c = sess.run([optimizer, cost_func], feed_dict={x: x_batch, y: y_batch})
            # Compute average loss
            avg_cost += c
    # Test model
    prediction = pred.eval(feed_dict={x: testing_X}, session=sess)
    mape = eval.mape(prediction, testing_Y)

    print(mape)
    print(np.mean(mape))
