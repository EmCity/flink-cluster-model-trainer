
import pandas as pd
import numpy as np
#import seaborn as sns
import src.misc.paths as path


import src.vector_gen.generateTimeInformationVector as gtiv
import src.vector_gen.generateCurrentSituationWithTime as gtcswt
import src.vector_gen.generate_VectorY as gvy

training_files = "../../../../../dataset/training/"
trajectories_file = "trajectories(table 5)_training.csv"
trajectories_df = pd.read_csv(training_files+trajectories_file)


# # prepare data
# prepare time information vector
df_ti = gtiv.generate_timeInformation_df(trajectories_df)
# prepare current situation vector
df_cswt = gtcswt.generate_vector(trajectories_df)
#print ("df_cswt: ", df_cswt)
print ("df_cswt columns: ", df_cswt.columns)
print ("df_cswt columns: ", df_cswt.columns.values)
df_y = gvy.generate_VectorY_df(trajectories_df)

df_all = df_cswt.join(df_y)
print ("df_cswt columns: ", df_cswt.columns.values)


# # Features

#feature_cols = ['hour', 'minute', 'weekday', '100', '101', '102', '103', '104', '105', '106', '107', '108', '109', '110', '111', '112', '113', '114', '115', '116', '117', '118', '119', '120', '121', '122', '123']
y_cols = [('0', 'A2'), ('0', 'A3'),
       ('0', 'B1'), ('0', 'B3'), ('0', 'C1'), ('0', 'C3'), ('1', 'A2'),
       ('1', 'A3'), ('1', 'B1'), ('1', 'B3'), ('1', 'C1'), ('1', 'C3'),
       ('2', 'A2'), ('2', 'A3'), ('2', 'B1'), ('2', 'B3'), ('2', 'C1'),
       ('2', 'C3'), ('3', 'A2'), ('3', 'A3'), ('3', 'B1'), ('3', 'B3'),
       ('3', 'C1'), ('3', 'C3'), ('4', 'A2'), ('4', 'A3'), ('4', 'B1'),
       ('4', 'B3'), ('4', 'C1'), ('4', 'C3'), ('5', 'A2'), ('5', 'A3'),
       ('5', 'B1'), ('5', 'B3'), ('5', 'C1'), ('5', 'C3')]



# split
train_weeks = 12 # of 13 weeks
train_rows = train_weeks*7*12

train = df_all[:train_rows]
test = df_all[train_rows:]

# define
x_train = train.drop(y_cols, axis=1)
y_train = train[y_cols]
x_test = test.drop(y_cols, axis=1)
y_test = test[y_cols]

print("x_train: ", x_train.columns.values)
print("y_train: ", y_train.columns.values)
print("x_test: ", x_test.columns.values)
print("y_test: ", y_test.columns.values)

# # train model

from sklearn import svm
from sklearn.multioutput import MultiOutputRegressor

clf = svm.SVR(C=30, epsilon=0.005, cache_size=2000)

regr_multi_svr = MultiOutputRegressor(clf, n_jobs=1) #getting a error with n_jobs > 1

regr_multi_svr.fit(x_train, y_train)

# load
#svr_rbf = joblib.load('svr_rbf.pkl')

# # save models

#from sklearn.externals import joblib
#joblib.dump(regr_multi_svr, 'regr_multi_svr_timeInformation.pkl')


# # evaluate

y_test_predict = regr_multi_svr.predict(x_test)
print("Score: ", regr_multi_svr.score(x_test, y_test))

y_test_predict_df = pd.DataFrame(y_test_predict, columns=y_cols)
y_test_df = pd.DataFrame(y_test, columns=y_cols)
print("y_test_predict_df.head(): ", y_test_predict_df.head())
print("y_test", y_test_df.head())

from sklearn import metrics

#print(metrics.mean_absolute_error(y_test_predict, y_test))
#print(metrics.mean_squared_error(y_test_predict, y_test))

import src.misc.evaluation as ev
mymape = ev.mape(y_test_predict, y_test)
print("MAPE error: ", np.mean(np.array(mymape)))

