from sklearn.multioutput import MultiOutputRegressor
import pandas as pd
import sklearn.svm as svm
from src.misc.evaluation import mape
import numpy as np

x_train = pd.read_csv('train_X.csv', index_col =0)
x_test = pd.read_csv('test_X.csv', index_col =0)
y_train = pd.read_csv('train_Y.csv', index_col =0)
y_test = pd.read_csv('test_Y.csv', index_col =0)

clf = svm.SVR(C=8, epsilon=0.0, cache_size=2000, kernel='rbf', tol=0.001, verbose=False)
regr_multi_svr = MultiOutputRegressor(clf, n_jobs=-1)
regr_multi_svr.fit(x_train, y_train)
y_test_predict = regr_multi_svr.predict(x_test)
mymape = mape(y_test_predict, y_test)
print(np.mean(np.array(mymape)))