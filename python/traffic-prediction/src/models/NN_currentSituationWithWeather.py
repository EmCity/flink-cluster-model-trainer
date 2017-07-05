import tensorflow as tf
import numpy as np
import pandas as pd
import src.vector_gen.generateCurrentSituationWithWeather as vecX
import src.vector_gen.generate_VectorY as vecY
import src.misc.split_train_valid_notRandom as split
import src.misc.evaluation as evaluation
import src.misc.paths as paths

df_trajectories = pd.read_csv(paths.trajectories_training_file)
df_weather = pd.read_csv(paths.weather_training_file)


# Create dataset
df_X = vecX.generate_x(df_trajectories, df_weather)
df_Y = vecY.generate_VectorY_df(df_trajectories)


# Split data into training, validation and testing sets
split.split_dataset(df_X, df_Y)


training_Y = pd.read_csv("../../../../python/traffic-prediction/src/misc/splitting_csv_files/train_Y.csv", index_col =0)
validation_Y = pd.read_csv("../../../../python/traffic-prediction/src/misc/splitting_csv_files/valid_Y.csv", index_col =0)
testing_Y = pd.read_csv("../../../../python/traffic-prediction/src/misc/splitting_csv_files/test_Y.csv", index_col =0)

training_X = pd.read_csv("../../../../python/traffic-prediction/src/misc/splitting_csv_files/train_X.csv", index_col =0)
validation_X = pd.read_csv("../../../../python/traffic-prediction/src/misc/splitting_csv_files/valid_X.csv", index_col =0)
testing_X = pd.read_csv("../../../../python/traffic-prediction/src/misc/splitting_csv_files/test_X.csv", index_col =0)

#-------------------------------------------------------------------------------------------------------------------------
# Tensorflow - linear regression

def feature_normalize(train_X):
    global mean, std
    mean = np.mean(train_X, axis=0)
    std = np.std(train_X, axis=0)

    return abs((train_X - mean) / std)

def run_regression(X_train, Y_train, X_test, Y_test, lambda_value = 0.1, normalize=False, batch_size=10, alpha=1e-8):
    x_train = feature_normalize(X_train) if normalize else X_train
    y_train = Y_train
    x_test = X_test
    y_test = Y_test
    session = tf.Session()

    number_rows = training_X.shape[0]
    number_col_x = training_X.shape[1]
    number_col_y = training_Y.shape[1]

    X = tf.placeholder('float', [None, number_col_x], name="X")
    Y = tf.placeholder('float', [None, number_col_y], name="Y")
    theta = tf.Variable(tf.random_normal([number_col_x, number_col_y], stddev=0.01), name="Theta")
    lambda_val = tf.constant(lambda_value)

    y_predicted = tf.matmul(X, theta)


    with tf.name_scope('cost') as scope:
        cost_func = (tf.nn.l2_loss(y_predicted - Y) + lambda_val * tf.nn.l2_loss(theta))/float(batch_size)
        cost_summary = tf.summary.scalar('cost', cost_func)

    training_func = tf.train.GradientDescentOptimizer(alpha).minimize(cost_func)

    with tf.name_scope("test") as scope:
        correct_prediction = tf.subtract(tf.cast(1, 'float'), tf.reduce_mean(tf.subtract(y_predicted, Y)))
        accuracy = tf.cast(correct_prediction, "float")

    saver = tf.train.Saver()
    merged = tf.summary.merge_all()
    writer = tf.summary.FileWriter("/tmp", session.graph)

    init = tf.global_variables_initializer()
    session.run(init)

    for i in range(1, int(len(x_train)/batch_size)):
        session.run(training_func, feed_dict={X: x_train[i*batch_size:i*batch_size+batch_size], Y: y_train[i*batch_size:i*batch_size+batch_size]})
        if i % batch_size == 0:
            print("test accuracy %g"%session.run(accuracy, feed_dict={X: x_test, Y: y_test}))
        print("final test accuracy %g"%session.run(accuracy, feed_dict={X: x_test, Y: y_test}))

    prediction = y_predicted.eval(feed_dict={X: x_test}, session = session)

    mape = evaluation.mape(prediction, y_test)
    mean_mape = np.mean(np.array(mape))

    print("MAPE: %g" % mean_mape)


    session.close()


run_regression(training_X, training_Y, testing_X, testing_Y, normalize=False, lambda_value = 0.1, batch_size=10)
