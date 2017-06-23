import pandas as pd
from sklearn import linear_model
from src.misc import evaluation as eval
import numpy as np
import sklearn.pipeline as Pipeline
from sklearn.externals import joblib

##load data
x_train = pd.read_csv('train_X.csv')
x_test = pd.read_csv('test_X.csv')
y_train = pd.read_csv('train_Y.csv')
y_test = pd.read_csv('test_Y.csv')

#generate model
clf = linear_model.MultiTaskElasticNet(l1_ratio=[.1, .5, .7, .9, .95, .99, 1])

#train model with training vectors
clf.fit(x_train, y_train)


y_pred = clf.predict(x_test)

#calculate error
error = eval.mape(y_pred, y_test)
print(error)
print(np.mean(np.array(error)))

#save model
#joblib.dump(clf, 'MultiTaskElasticNetCurrentSituationWithTime.pkl')
