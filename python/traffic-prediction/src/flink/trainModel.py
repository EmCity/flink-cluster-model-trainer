import sklearn
import sys
import json
from sklearn import linear_model
from sklearn.multioutput import MultiOutputRegressor
import numpy as np
import pandas as pd
import io as io
import pymongo as mongo


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
    train_y_io = io.StringIO(data['train_y'])
    test_y_io = io.StringIO(data['test_y'])

    df_x_train = pd.read_csv(train_x_io, index_col=0, sep=',', lineterminator='\n', header=0)
    df_x_test = pd.read_csv(test_x_io, index_col=0, sep=',', lineterminator='\n', header=0)
    df_y_train = pd.read_csv(train_y_io, index_col=0, sep=',',lineterminator='\n', header=0)
    df_y_test = pd.read_csv(test_y_io, index_col=0, sep=',',lineterminator='\n', header=0)

    result_mape = "{error}"
    if "LR" == algorithms:
        result_mape = train_lr(df_x_train, df_x_test, df_y_train, df_y_test, jsonDict)
    if "SVM" == algorithms:
        result_mape = train_svm(df_x_train, df_x_test, df_y_train, df_y_test, jsonDict)
    if "NN" == algorithms:
        result_mape = train_nn(df_x_train, df_x_test, df_y_train, df_y_test, jsonDict)

    # add mape
    result_json['mape'] = result_mape
    # print (return) jsonresultstring!!!
    print(json.dumps(result_json))


def train_svm(df_x_train, df_x_test, df_y_train, df_y_test, params):
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
    return get_error(regr_multi_svr, df_x_test, df_y_test)


def train_lr(df_x_train, df_x_test, df_y_train, df_y_test, params):
    lr = linear_model.LinearRegression(normalize=params["normalize"], fit_intercept=params["fit_intercept"])
    lr.fit(df_x_train, df_y_train)
    return get_error(lr, df_x_test, df_y_test)


def train_nn(df_x_train, df_x_test, df_y_train, df_y_test, params):
    return 999


def get_error(model, df_x_test, df_y_test):
    mape = np.mean(np.abs((df_y_test - model.predict(df_x_test)) / df_y_test))
    return np.mean(np.array(mape))

json_string = sys.argv[1]
json_param = json.loads(json_string)
train_model(json_param)
