from sklearn.multioutput import MultiOutputRegressor
from sklearn.svm import SVR
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
import pandas as pd
import sklearn.svm as svm
from src.misc import paths as path
from src.misc.evaluation import mape
import numpy as np
if __name__ == '__main__':

    ##load data
    x_train = pd.read_csv('train_X.csv', index_col =0)
    x_test = pd.read_csv('test_X.csv', index_col =0)
    y_train = pd.read_csv('train_Y.csv', index_col =0)
    y_test = pd.read_csv('test_Y.csv', index_col =0)

    #MultiOutputRegressor(estimator=SVR(C=4.0, cache_size=200, coef0=0.0, degree=3, epsilon=0.0,
  #gamma=0.0069444444444444441, kernel='rbf', max_iter=-1, shrinking=True,
  #tol=0.001, verbose=False),
    clf = svm.SVR(C=8, epsilon=0.0, cache_size=2000, kernel='rbf', tol=0.001, verbose=False)

    regr_multi_svr = MultiOutputRegressor(clf, n_jobs=-1)

    regr_multi_svr.fit(x_train, y_train)

    y_test_predict = regr_multi_svr.predict(x_test)
    mymape = mape(y_test_predict, y_test)
    print(np.mean(np.array(mymape)))