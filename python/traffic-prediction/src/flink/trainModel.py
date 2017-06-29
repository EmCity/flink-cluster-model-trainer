import sklearn
import sys
import json
from sklearn import linear_model
from sklearn.multioutput import MultiOutputRegressor
import numpy as np
import pandas as pd

def trainModel(jsonDict):
    algorithms = jsonDict['algorithm']
    data = jsonDict['data']

    train_x = data['train_X']
    test_x = data['test_x']
    train_y = data['train_y']
    test_y = data['test_y']

    #TODO: fix paths!
    df_x_train = pd.read_csv('C:/Users/Effi2/Documents/sose17-small-data/python/traffic-prediction/src/flink/train_x.csv', index_col=0)
    df_x_test = pd.read_csv('C:/Users/Effi2/Documents/sose17-small-data/python/traffic-prediction/src/flink/test_x.csv', index_col=0)
    #df_x_valid = pd.read_csv(data['valid_x'], index_col=0)

    df_y_train = pd.read_csv('C:/Users/Effi2/Documents/sose17-small-data/python/traffic-prediction/src/flink/train_y.csv', index_col=0)
    df_y_test = pd.read_csv('C:/Users/Effi2/Documents/sose17-small-data/python/traffic-prediction/src/flink/test_y.csv', index_col=0)
    #df_y_valid = pd.read_csv(data['valid_y'], index_col=0)


    if "LR" == algorithms:
        trainLR(df_x_train, df_x_test, df_y_train, df_y_test, jsonDict)
    if "SVM" == algorithms:
        trainSVM(df_x_train, df_x_test, df_y_train, df_y_test, jsonDict)
    if "NN" == algorithms.keys():
        #trainNN(df_x_train, df_x_test, df_y_train, df_y_test, algorithms['NN'])
        print("NO NN IMPLEMENTED YET")

def trainSVM(df_x_train, df_x_test, df_y_train, df_y_test, params):
    c = params("C");
    epsilon = params("epsilon");
    kernel = params("kernel");
    degree = params("degree");
    gamma = params("gamma");
    coef0 = params("coef0");
    shrinking = params("shrinking");
    tol = params("tol");
    cache_size = params("cache_size");
    max_iter = params("max_iter");

    svr = sklearn.svm.SVR(c=c, epsilon=epsilon, kernel=kernel, degree=degree, gamma=gamma, coef0=coef0,
                                       shrinking=shrinking, tol=tol, cache_size=cache_size, max_iter=max_iter)
    regr_multi_svr = MultiOutputRegressor(svr)
    regr_multi_svr.fit(df_x_train, df_y_train)

    print("SVM Error:")
    print(get_error(regr_multi_svr, df_x_test, df_y_test))


def trainLR(df_x_train, df_x_test, df_y_train, df_y_test, params):
    lr = linear_model.LinearRegression(normalize=params("normalize"), fit_intercept=params("fit_intercept"))
    lr.fit(df_x_train, df_y_train)
    print("Linear Regression Error:")
    print(get_error(lr, df_x_test, df_y_test))


def get_error(model, df_x_test, df_y_test):
    return  np.mean(np.abs((df_y_test - model.predict(df_x_test)) / df_y_test))


#TODO: implement tensorflow NN here
# def trainNN(df_x_train, df_x_test, df_y_train, df_y_test, params):
#     matrix_x_train = df_x_train.as_matrix()
#     matrix_y_train = df_y_train.as_matrix()
#     matrix_x_test = df_x_test.as_matrix()
#     matrix_y_test = df_y_test.as_matrix()
#
#     error = params["error"]
#     optimizer = params["optimizer"]
#     batch_size = params["batch_size"]
#     epochs = params["epochs"]
#
#     min_max_scaler = preprocessing.MinMaxScaler()
#     min_max_scaler.fit(np.concatenate((matrix_x_train, matrix_x_test)))
#     X_train_scale = min_max_scaler.transform(matrix_x_train)
#     X_test_scale = min_max_scaler.transform(matrix_x_test)
#
#     model = Sequential()
#     model.add(Dense(input_dim=147, output_dim=200, activation='relu'))
#     model.add(Dense(input_dim=200, output_dim=500, activation='relu'))
#     model.add(Dense(input_dim=500, output_dim=36, activation='relu'))
#
#     model.compile(loss=error, optimizer=optimizer)
#
#     model.fit(X_train_scale, matrix_y_train,
#               batch_size=batch_size, epochs=epochs, verbose=2,
#               validation_data=(X_test_scale, matrix_y_test), shuffle=False)
#
#     y = model.predict(X_test_scale, batch_size=1)
#     error = mape(y, matrix_y_test)
#     print(error)


json_string = sys.argv[1].replace('?', '"')
trainModel(json.loads(json_string))
