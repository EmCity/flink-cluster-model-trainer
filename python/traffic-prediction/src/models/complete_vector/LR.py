import pandas as pd
import sklearn.linear_model as linear_model
from src.misc.evaluation import mape
import numpy as np

x_train = pd.read_csv('train_X.csv', index_col =0)
x_test = pd.read_csv('test_X.csv', index_col =0)
y_train = pd.read_csv('train_Y.csv', index_col =0)
y_test = pd.read_csv('test_Y.csv', index_col =0)
regr_multi_svr = linear_model.MultiTaskElasticNetCV()
regr_multi_svr.fit(x_train, y_train)
test_predict = regr_multi_svr.predict(x_test)
mymape = mape(test_predict, y_test)
print(np.mean(np.array(mymape)))