from sklearn import linear_model
from sklearn.svm import SVR
import sys
import json as json


print('Number of args: ', len(sys.argv))
print('args: ',str(sys.argv))

jsonString = sys.argv[0]
jsonDict = json.load(jsonString)


def trainModel(df_x_train, df_x_test, df_y_train, df_y_test, df_x_valid, df_y_valid, args):
    x_train = df_x_train
    x_test = df_x_test
    x_valid = df_x_valid

    y_train = df_y_train
    y_test = df_y_test
    y_valid = df_y_valid

    algorithms = args[0]

    if "LR" in algorithms:
        trainLR(x_train, x_test, x_valid, y_train, y_test, y_valid)
    if "SVM" in algorithms:
        trainSVM(x_train, x_test, x_valid, y_train, y_test, y_valid)

def trainLR(df_x_train, df_x_test, df_y_train, df_y_test, df_x_valid, df_y_valid, params):
    #extract params

    lr = linear_model.LinearRegression()




def trainSVM(df_x_train, df_x_test, df_y_train, df_y_test, df_x_valid, df_y_valid, params):
    #extract params

    svr = SVR()