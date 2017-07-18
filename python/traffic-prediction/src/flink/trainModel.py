import sklearn
import sys
import json
from sklearn import linear_model
from sklearn.multioutput import MultiOutputRegressor
import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

import io as io
import pymongo as mongo
import tensorflow as tf
import pandas as pd
import numpy as np


def train_model(jsonDict):
    uri = "mongodb://sambauser:teamsamba@sambahost.dyndns.lrz.de:27017/samba"
    client = mongo.MongoClient(uri)
    db = client.samba
    jobs = db.jobs
    jobname = jsonDict['job_name']
    cursor = jobs.find({'job_name': jobname})
    json_data = None
    for doc in cursor:
        json_data = doc

    data = json_data['data']

    # crate result json
    result_json = json.loads("{}")
    result_json['parameter_set'] = jsonDict
    result_json['job_name'] = jobname
    algorithms = jsonDict['algorithm']

    train_x_io = io.StringIO(data['train_x'])
    test_x_io = io.StringIO(data['test_x'])
    valid_x_io = io.StringIO(data['valid_x'])
    train_y_io = io.StringIO(data['train_y'])
    test_y_io = io.StringIO(data['test_y'])
    valid_y_io = io.StringIO(data['valid_y'])

    df_x_train = pd.read_csv(train_x_io, index_col=0, sep=',', lineterminator='\n', header=0)
    df_x_test = pd.read_csv(test_x_io, index_col=0, sep=',', lineterminator='\n', header=0)
    df_x_valid = pd.read_csv(valid_x_io, index_col=0, sep=',', lineterminator='\n', header=0)
    df_y_train = pd.read_csv(train_y_io, index_col=0, sep=',',lineterminator='\n', header=0)
    df_y_test = pd.read_csv(test_y_io, index_col=0, sep=',',lineterminator='\n', header=0)
    df_y_valid = pd.read_csv(valid_y_io, index_col=0, sep=',', lineterminator='\n', header=0)

    result_mape = "{error}"
    result_mape_valid = "{error}"
    if "LR" == algorithms:
        result_mape,result_mape_valid = train_lr(df_x_train, df_x_test, df_x_valid, df_y_train, df_y_test, df_y_valid, jsonDict)
    if "SVM" == algorithms:
        result_mape,result_mape_valid = train_svm(df_x_train, df_x_test, df_x_valid, df_y_train, df_y_test, df_y_valid,jsonDict)
    if "NN" == algorithms:
        result_mape,result_mape_valid = train_nn(df_x_train, df_x_test, df_x_valid, df_y_train, df_y_test, df_y_valid, jsonDict)

    # add mape
    result_json['mape'] = result_mape
    result_json['mape_valid'] = result_mape_valid

    # print (return) jsonresultstring!!!
    print(json.dumps(result_json))


def train_svm(df_x_train, df_x_test, df_x_valid, df_y_train, df_y_test, df_y_valid, params):
    C = params["C"];
    epsilon = params["epsilon"];
    kernel = params["kernel"];
    gamma = params["gamma"];
    shrinking = params["shrinking"];
    tol = params["tolerance"];
    cache_size = params["cache_size"];
    max_iter = params["max_iter"];

    svr = sklearn.svm.SVR(C=C, epsilon=epsilon, kernel=kernel, gamma=gamma,
                            shrinking=shrinking, tol=tol, cache_size=cache_size, max_iter=max_iter)
    regr_multi_svr = MultiOutputRegressor(svr)
    regr_multi_svr.fit(df_x_train, df_y_train)
    return get_error(regr_multi_svr, df_x_test, df_y_test),get_error(regr_multi_svr, df_x_valid, df_y_valid)


def train_lr(df_x_train, df_x_test, df_x_valid, df_y_train, df_y_test, df_y_valid, params):
    lr = linear_model.LinearRegression(normalize=params["normalize"], fit_intercept=params["fit_intercept"])
    lr.fit(df_x_train, df_y_train)
    return get_error(lr, df_x_test, df_y_test),get_error(lr, df_x_valid, df_y_valid)


def train_nn(df_x_train, df_x_test, df_x_valid, df_y_train, df_y_test, df_y_valid,  params):
    x_dim = len(df_x_train.columns)
    y_dim = len(df_y_train.columns)
    x = tf.placeholder(tf.float32, [None, x_dim])
    y = tf.placeholder(tf.float32, [None, y_dim])


    normalization = params["normalization"]
    if normalization == True:
        tf.nn.l2_normalize(x, dim=0)

    learning_rate = params["learning_rate"];
    epochs = params["epochs"]
    cost_function = params["cost_function"]
    neurons = 200


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

    cost_func = tf.reduce_mean(tf.div(tf.abs(pred-y), y))
    # Define loss and optimizer
    if "mean_squared_error" == cost_function :
        cost_func = tf.sqrt(tf.reduce_mean(tf.square(tf.subtract(pred, y))))

    if "mean_absolute_percentage_error" == cost_function :
        cost_func = tf.reduce_mean(tf.div(tf.abs(pred-y), y))

    optimizer = tf.train.GradientDescentOptimizer(learning_rate=learning_rate).minimize(cost_func)

    # Initializing the variables
    init = tf.global_variables_initializer()

    # Launch the graph
    with tf.Session() as sess:
        sess.run(init)
        batch_size = 1
        # Training cycle
        for epoch in range(epochs):
            # Loop over all batches
            for batch in range(int(len(df_x_train) / batch_size)):
                x_batch = df_x_train[batch * batch_size: batch * batch_size + batch_size]
                y_batch = df_y_train[batch * batch_size: batch * batch_size + batch_size]
                # Run optimization op (backprop) and cost op (to get loss value)
                _, c = sess.run([optimizer, cost_func], feed_dict={x: x_batch, y: y_batch})
                # Compute average loss
        # Test model
        prediction = pred.eval(feed_dict={x: df_x_test}, session=sess)
        prediction_valid = pred.eval(feed_dict={x: df_x_valid}, session=sess)
        mape = np.mean(np.abs((df_y_test - prediction) / df_y_test))
        mape_valid = np.mean(np.abs((df_y_valid - prediction_valid) / df_y_valid))
        return np.mean(mape),np.mean(mape_valid)


def get_error(model, df_x, df_y):
    mape = np.mean(np.abs((df_y - model.predict(df_x)) / df_y))
    return np.mean(np.array(mape))

json_string = sys.argv[1]
json_param = json.loads(json_string)
train_model(json_param)
