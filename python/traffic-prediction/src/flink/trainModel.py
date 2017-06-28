from sklearn import linear_model
from sklearn.svm import SVR
import sys
import json as json
from keras.layers import Dense, Activation
from keras.models import Sequential
from sklearn import preprocessing
from src.misc.evaluation import mape
import numpy as np
import pandas as pd

def trainModel(x_train, y_train, x_test, y_test, x_valid, y_valid, algorithms):
    df_x_train = pd.read_csv(x_train, index_col=0)
    df_x_test = pd.read_csv(x_test, index_col=0)
    df_x_valid = pd.read_csv(x_valid, index_col=0)

    df_y_train = pd.read_csv(y_train, index_col=0)
    df_y_test = pd.read_csv(y_test, index_col=0)
    df_y_valid = pd.read_csv(y_valid, index_col=0)

    if "LR" in algorithms.keys():
        trainLR(df_x_train, df_x_test, df_x_test, df_y_train, df_y_test, algorithms['LR'])
    if "SVM" in algorithms.keys():
        trainSVM(df_x_train, df_x_test, df_x_test, df_y_train, df_y_test, algorithms['SVM'])
    if "NN" in algorithms.keys():
        trainNN(df_x_train, df_x_test, df_x_test, df_y_train, df_y_test, algorithms['NN'])


def trainLR(df_x_train, df_x_test, df_y_train, df_y_test, params):
    #todo: get params
    lr = linear_model.LinearRegression()
    lr.fit(df_x_train, df_y_train)
    getError(lr, df_x_test, df_y_test)


def trainSVM(df_x_train, df_x_test, df_y_train, df_y_test, params):
    #todo: get params
    svr = linear_model.SVR()
    svr.fit(df_x_train, df_y_train)
    getError(svr, df_x_test, df_y_test)


def trainNN(df_x_train, df_y_train, df_x_test, df_y_test, params):
    #todo:get params
    min_max_scaler = preprocessing.MinMaxScaler()
    min_max_scaler.fit(np.concatenate((df_x_train, df_x_test)))
    X_train_scale = min_max_scaler.transform(df_x_train)
    X_test_scale = min_max_scaler.transform(df_x_test)

    model = Sequential()
    model.add(Dense(input_dim=154, output_dim=200, activation='relu'))
    model.add(Dense(input_dim=200, output_dim=500, activation='relu'))
    model.add(Dense(input_dim=500, output_dim=36, activation='relu'))

    model.compile(loss='mean_absolute_percentage_error', optimizer='rmsprop')

    model.fit(X_train_scale, df_y_train,
              batch_size=1, epochs=100, verbose=2,
              validation_data=(X_test_scale, df_y_test), shuffle=False)

    y = model.predict(X_test_scale, batch_size=1)
    error = mape(y, y_test)
    print(error)

def getError(model, df_x_test, df_y_test):
    df_y_prediction= model.predict(df_x_test)
    error = mape(df_y_prediction, df_y_test)
    print(error)

print('Number of args: ', len(sys.argv))
print('args: ',str(sys.argv))
#jsonString = sys.argv[0]
with open('JobDef.json') as data_file:
    jsonDict = json.load(data_file)
algorithms = jsonDict['algorithms']
data = jsonDict['data']

x_train = data['train_X']
y_train = data['train_y']
x_test = data['test_x']
y_test = data['test_y']
x_valid = data['valid_x']
y_valid = data['valid_y']

trainModel(x_train, y_train, x_test, y_test, x_valid, y_valid, algorithms)
