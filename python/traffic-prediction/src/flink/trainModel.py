import sklearn
import sys
import json as json
from sklearn import linear_model
from sklearn.multioutput import MultiOutputRegressor
from keras.layers import Dense
from keras.models import Sequential
from sklearn import preprocessing
from src.misc.evaluation import mape
import numpy as np
import pandas as pd

def trainModel(data, algorithms):
    df_x_train = pd.read_csv(data['train_X'], index_col=0)
    df_x_test = pd.read_csv(data['test_x'], index_col=0)
    #df_x_valid = pd.read_csv(data['valid_x'], index_col=0)

    df_y_train = pd.read_csv(data['train_y'], index_col=0)
    df_y_test = pd.read_csv(data['test_y'], index_col=0)
    #df_y_valid = pd.read_csv(data['valid_y'], index_col=0)


    if "LR" in algorithms.keys():
        trainLR(df_x_train, df_x_test, df_y_train, df_y_test, algorithms['LR'])
    if "SVM" in algorithms.keys():
        trainSVM(df_x_train, df_x_test, df_y_train, df_y_test, algorithms['SVM'])
    if "NN" in algorithms.keys():
        trainNN(df_x_train, df_x_test, df_y_train, df_y_test, algorithms['NN'])


def trainLR(df_x_train, df_x_test, df_y_train, df_y_test, params):
    #todo: get params
    lr = linear_model.LinearRegression()
    lr.fit(df_x_train, df_y_train)
    print("Linear Regression Error:")
    getError(lr, df_x_test, df_y_test)


def trainSVM(df_x_train, df_x_test, df_y_train, df_y_test, params):
    #todo: get params
    svr = sklearn.svm.SVR()
    regr_multi_svr = MultiOutputRegressor(svr)
    regr_multi_svr.fit(df_x_train, df_y_train)
    print("SVM Error:")
    getError(regr_multi_svr, df_x_test, df_y_test)


def trainNN(df_x_train, df_x_test, df_y_train, df_y_test, params):
    matrix_x_train = df_x_train.as_matrix()
    matrix_y_train = df_y_train.as_matrix()
    matrix_x_test = df_x_test.as_matrix()
    matrix_y_test = df_y_test.as_matrix()

    error = params["error"]
    optimizer = params["optimizer"]
    batch_size = params["batch_size"]
    epochs = params["epochs"]

    #todo:get params
    min_max_scaler = preprocessing.MinMaxScaler()
    min_max_scaler.fit(np.concatenate((matrix_x_train, matrix_x_test)))
    X_train_scale = min_max_scaler.transform(matrix_x_train)
    X_test_scale = min_max_scaler.transform(matrix_x_test)

    model = Sequential()
    model.add(Dense(input_dim=147, output_dim=200, activation='relu'))
    model.add(Dense(input_dim=200, output_dim=500, activation='relu'))
    model.add(Dense(input_dim=500, output_dim=36, activation='relu'))

    model.compile(loss=error, optimizer=optimizer)

    model.fit(X_train_scale, matrix_y_train,
              batch_size=batch_size, epochs=epochs, verbose=2,
              validation_data=(X_test_scale, matrix_y_test), shuffle=False)

    y = model.predict(X_test_scale, batch_size=1)
    error = mape(y, matrix_y_test)
    print(error)

def getError(model, df_x_test, df_y_test):
    df_y_prediction= model.predict(df_x_test)
    error = mape(df_y_prediction, df_y_test)
    sys.stdout(np.mean(error))

#print('Number of args: ', len(sys.argv))
#print('args: ',str(sys.argv))
#jsonString = sys.argv[0]
with open('JobDef.json') as data_file:
    jsonDict = json.load(data_file)
algorithms = jsonDict['algorithms']
data = jsonDict['data']
trainModel(data, algorithms)
