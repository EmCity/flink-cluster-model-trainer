
# coding: utf-8

# In[1]:

import pandas as pd
import numpy as np
import tensorflow as tf

import src.misc.evaluation as evaluation


# In[2]:

# read data
#training_files = "../../dataset/training/"
#trajectories_file = "trajectories(table 5)_training.csv"
#volume_file = "volume(table 6)_training.csv"
#trajectories_df = pd.read_csv(training_files+trajectories_file)
#volume_df = pd.read_csv(training_files+volume_file)

#import src.vector_gen.generateCurrentSituationWithTime as gcswt
#import src.vector_gen.generate_VectorY as gvy
#y_df = gvy.generate_VectorY_df(trajectories_df)


# splited
training_Y = pd.read_csv("src/misc/train_Y.csv", index_col =0)
testing_Y = pd.read_csv("src/misc/test_Y.csv", index_col =0)
training_X = pd.read_csv("src/misc/train_X.csv", index_col =0)
testing_X = pd.read_csv("src/misc/test_X.csv", index_col =0)


# In[3]:

print(len(training_X), len(testing_Y))
print(training_X.shape, training_Y.shape)
x_dim = len(training_X.columns)
y_dim = len(training_Y.columns)
print('x: ', x_dim)
print('y: ', y_dim)


# In[4]:

# http://radiostud.io/beat-rush-hour-traffic-with-tensorflow-machine-learning/
# https://www.youtube.com/watch?v=PwAGxqrXSCs
# https://www.tensorflow.org/get_started/mnist/beginners


# In[5]:

# model
x = tf.placeholder(tf.float32, [None, x_dim], name="x")
y = tf.placeholder(tf.float32, [None, y_dim], name="y")


# one layer
# y_pred = x * weight + bias
weights = tf.Variable(tf.ones([x_dim, y_dim], dtype=tf.float32), name="weight")
biases = tf.Variable(tf.zeros([y_dim], dtype=tf.float32), name="bias")

y_pred = tf.add(tf.matmul(x, weights), biases)

# activation function, relu rectified linear
# https://www.tensorflow.org/api_guides/python/nn
#y_pred = tf.nn.relu(y_pred)


# cost
with tf.name_scope("cost_func"):
    # def cost/loss function
    #cost_func = tf.reduce_mean(evaluation.mape2(y_pred=y_pred, y_true=y))
    #cost_func = tf.metrics.mean_absolute_error(y_pred, y)
    #cost_func = tf.reduce_mean(tf.metrics.mean_absolute_error(y_pred, y))
    #cost_func = -tf.reduce_sum(y*tf.log(y_pred))
    cost_func = tf.reduce_mean(tf.div(tf.abs(y_pred-y), y))

#train
with tf.name_scope("train"):
    optimizer = tf.train.GradientDescentOptimizer(0.05).minimize(cost_func)
    #optimizer = tf.train.AdamOptimizer().minimize(cost_func)


# In[6]:

# start session and train
epochs = 30
batch_size = 1


sess = tf.Session()
sess.run(tf.global_variables_initializer())

tf.summary.scalar('cost', cost_func)
tf.summary.histogram('weights', weights)
tf.summary.histogram('biases', biases)
merged_summary = tf.summary.merge_all()
writer = tf.summary.FileWriter('./tftrain', sess.graph)
#test_writer = tf.summary.FileWriter('./tftest')

for epoch in range(epochs):
    epoch_loss = 0
    for batch in range(0, int(len(training_X)/batch_size)):
        x_batch = training_X[batch*batch_size: batch*batch_size+batch_size]
        y_batch = training_Y[batch*batch_size: batch*batch_size+batch_size]
        
        # Occasionally report accuracy
        #if batch % 100 == 0:
        #    [train_accuracy] = sess.run([cost_func], feed_dict={x: x_batch, y: y_batch})
        #    print("epoch %d, batchstep %d, training accuracy %g" % (epoch, batch, train_accuracy))
            

        #run_options = tf.RunOptions(trace_level=tf.RunOptions.FULL_TRACE)
        #run_metadata = tf.RunMetadata()
        #
        
        # train
        _, c = sess.run([optimizer, cost_func], feed_dict={x: x_batch, y: y_batch})
        
        epoch_loss += c
        
    [train_accuracy] = sess.run([cost_func], feed_dict={x: x_batch, y: y_batch})
    print("epoch %d, loss %d, training accuracy %g" % (epoch, epoch_loss, train_accuracy))
    s = sess.run(merged_summary, feed_dict={x: x_batch, y: y_batch})
    writer.add_summary(s, epoch)

print('Epoch', epoch, 'loss', epoch_loss)

# TODO FALSCH!!!???
prediction = y_pred.eval(feed_dict={x: testing_X}, session = sess)
mape = evaluation.mape(prediction, testing_Y)

print('mean MAPE\n', np.mean(mape))

print('MAPE\n', mape)



# In[7]:

#pd.DataFrame(prediction, index=testing_Y.index, columns=testing_Y.columns)


# In[8]:

#testing_Y

