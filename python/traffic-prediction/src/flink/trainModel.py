import sklearn
import sys
import json
from sklearn import linear_model
from sklearn.multioutput import MultiOutputRegressor
import numpy as np
import pandas as pd

def trainModel(jsonDict):

    # crate result json
    result_json = json.loads("{}")
    result_json['parameter_set'] = jsonDict

    algorithms = jsonDict['algorithm']
    data = jsonDict['data']

    train_x = data['train_X']
    test_x = data['test_x']
    train_y = data['train_y']
    test_y = data['test_y']

    #TODO: fix paths!
    #df_x_train = pd.read_csv('C:/Users/Effi2/Documents/sose17-small-data/python/traffic-prediction/src/flink/train_x.csv', index_col=0)
    #df_x_test = pd.read_csv('C:/Users/Effi2/Documents/sose17-small-data/python/traffic-prediction/src/flink/test_x.csv', index_col=0)
    #df_x_valid = pd.read_csv(data['valid_x'], index_col=0)

    #df_y_train = pd.read_csv('C:/Users/Effi2/Documents/sose17-small-data/python/traffic-prediction/src/flink/train_y.csv', index_col=0)
    #df_y_test = pd.read_csv('C:/Users/Effi2/Documents/sose17-small-data/python/traffic-prediction/src/flink/test_y.csv', index_col=0)
    #df_y_valid = pd.read_csv(data['valid_y'], index_col=0)

    # meine
    df_x_train = pd.read_csv('/home/l/lemkec/BigDataScience/sose17-small-data/python/traffic-prediction/src/flink/train_x.csv', index_col=0)
    df_x_test = pd.read_csv('/home/l/lemkec/BigDataScience/sose17-small-data/python/traffic-prediction/src/flink/test_x.csv', index_col=0)
    #df_x_valid = pd.read_csv(data['valid_x'], index_col=0)

    df_y_train = pd.read_csv('/home/l/lemkec/BigDataScience/sose17-small-data/python/traffic-prediction/src/flink/train_y.csv', index_col=0)
    df_y_test = pd.read_csv('/home/l/lemkec/BigDataScience/sose17-small-data/python/traffic-prediction/src/flink/test_y.csv', index_col=0)
    #df_y_valid = pd.read_csv(data['valid_y'], index_col=0)
    #print('reading csv files')

    result_mape = ""

    if "LR" == algorithms:
        result_mape = trainLR(df_x_train, df_x_test, df_y_train, df_y_test, jsonDict)
    if "SVM" == algorithms:
        result_mape = trainSVM(df_x_train, df_x_test, df_y_train, df_y_test, jsonDict)
    if "NN" == algorithms:
        #result_mape = trainNN(df_x_train, df_x_test, df_y_train, df_y_test, algorithms['NN'])
        print("NO NN IMPLEMENTED YET")

    # add mape
    result_json['mape'] = result_mape


    # print (return) jsonresultstring!!!
    print(json.dumps(result_json))

def trainSVM(df_x_train, df_x_test, df_y_train, df_y_test, params):
    C = params["C"];
    epsilon = params["epsilon"];
    kernel = params["kernel"];
    degree = params["degree"];
    gamma = params["gamma"];
    coef0 = params["coef0"];
    shrinking = params["shrinking"];
    tol = params["tol"];
    cache_size = params["cache_size"];
    max_iter = params["max_iter"];

    svr = sklearn.svm.SVR(C=C, epsilon=epsilon, kernel=kernel, degree=degree, gamma=gamma, coef0=coef0,
                                       shrinking=shrinking, tol=tol, cache_size=cache_size, max_iter=max_iter)
    regr_multi_svr = MultiOutputRegressor(svr)
    regr_multi_svr.fit(df_x_train, df_y_train)

    return (get_error(regr_multi_svr, df_x_test, df_y_test))


def trainLR(df_x_train, df_x_test, df_y_train, df_y_test, params):
    lr = linear_model.LinearRegression(normalize=params["normalize"], fit_intercept=params["fit_intercept"])
    lr.fit(df_x_train, df_y_train)

    return (get_error(lr, df_x_test, df_y_test))


def get_error(model, df_x_test, df_y_test):
    mape = np.mean(np.abs((df_y_test - model.predict(df_x_test)) / df_y_test))
    return np.mean(np.array(mape))


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


json_string = sys.argv[1]
json_string = json_string.replace('?', '"')
trainModel(json.loads(json_string))
