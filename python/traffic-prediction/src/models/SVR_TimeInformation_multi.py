
import pandas as pd
import numpy as np
import seaborn as sns
import src.misc.paths as path


import src.vector_gen.generateTimeInformationVector as gtiv
import src.vector_gen.generate_VectorY as gvy

training_files = "../../../../dataset/training/"
trajectories_file = "trajectories(table 5)_training.csv"
trajectories_df = pd.read_csv(training_files+trajectories_file)


# # prepare data

df_ti = gtiv.generate_timeInformation_df(trajectories_df)
df_y = gvy.generate_VectorY_df(trajectories_df)

df_all = df_ti.join(df_y)



# # Features

feature_cols = ['hour', 'minute', 'weekday']
y_cols = [('0', 'A2'), ('0', 'A3'),
       ('0', 'B1'), ('0', 'B3'), ('0', 'C1'), ('0', 'C3'), ('1', 'A2'),
       ('1', 'A3'), ('1', 'B1'), ('1', 'B3'), ('1', 'C1'), ('1', 'C3'),
       ('2', 'A2'), ('2', 'A3'), ('2', 'B1'), ('2', 'B3'), ('2', 'C1'),
       ('2', 'C3'), ('3', 'A2'), ('3', 'A3'), ('3', 'B1'), ('3', 'B3'),
       ('3', 'C1'), ('3', 'C3'), ('4', 'A2'), ('4', 'A3'), ('4', 'B1'),
       ('4', 'B3'), ('4', 'C1'), ('4', 'C3'), ('5', 'A2'), ('5', 'A3'),
       ('5', 'B1'), ('5', 'B3'), ('5', 'C1'), ('5', 'C3')]


# # plots
#sns.pairplot(df_all, x_vars=feature_cols, y_vars=y_cols, size=6, aspect=1.3, kind='reg')


# # split train and test

# not working!?!?!
#import src.misc.split_train_valid as split
#training, validation, testing = split.split_dataset(df_all, train = 0.9, validation = 0.000001)


#from sklearn.model_selection import train_test_split
#x_train, x_test, y_train, y_test = train_test_split(df[feature_cols], df['avg_travel_time'], test_size=0.2, random_state=42)

'''
from sklearn.model_selection import KFold
# split per week
splits=[]
kf = KFold(n_splits=5, random_state=None, shuffle=False)
for train_idxs, test_idxs in kf.split(df_all):
    splits.append((df_all.iloc[train_idxs], df_all.iloc[test_idxs]))
    print(len(train_idxs), len(test_idxs))

a = splits[0][0]
a
'''

# split
train_weeks = 12 # of 13 weeks
train_rows = train_weeks*7*12

train = df_all[:train_rows]
test = df_all[train_rows:]

# define
x_train = train[feature_cols]
y_train = train[y_cols]
x_test = test[feature_cols]
y_test = test[y_cols]

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

y_test_predict_df = pd.DataFrame(y_test_predict, columns=y_cols)
y_test_predict_df.head()

from sklearn import metrics

print(metrics.mean_absolute_error(y_test_predict, y_test))
print(metrics.mean_squared_error(y_test_predict, y_test))

import src.misc.evaluation as ev
mymape = ev.mape(y_test_predict, y_test)
print(np.mean(np.array(mymape)))


# #plot
# import matplotlib.pyplot as plt
# alpha=0.8
# lw=0.7
# 
# fig, ax = plt.subplots(figsize = (26,8))
# 
# ax.scatter(res.index.values, res['y_test'], color='green', label='y_test', s=0.8)
# 
# ax.plot(res.index.values, res['y_pred_rbf'], color='red', label='y_pred_rbf', alpha=alpha, lw=lw)
# #plt.plot(res.index.values, res['y_pred_sigmoid'], color='blue', label='y_pred_sigmoid', alpha=alpha, lw=lw)
# ax.plot(res.index.values, res['y_pred_lin'], color='orange', label='y_pred_lin', alpha=alpha, lw=lw)
# #plt.plot(res.index.values, res['y_pred'], color='darkorange', label='y_pred_rbf')
# ax.set_title('SVN on TimeInformation with rbf and linear kernel')
# ax.set_xlabel('index(route,dayofweek,hour,minute)')
# ax.set_ylabel('avg_travel_time')
# ax.set_ylim(0,200)
# ax.set_xlim(0)
# 
# ax.legend(shadow=True, fancybox=True)
# 
# #fig.legend()
# 
# '''
# I also want to share my recent results. Maybe it helps or inspire someone.
# 
# SVN on TimeInformation with rbf and linear kernel.
# Trained on the first 8 weeks and tested with the remaining data. (not shuffled)
# 
# '''
# 

# # SVN Parameter Finding

'''
from sklearn.multioutput import MultiOutputRegressor
from sklearn.svm import SVR
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

pipe_svr = Pipeline([ ('reg', MultiOutputRegressor(SVR()))])

grid_param_svr = {
    'reg__estimator__C': np.arange(20, 40.0, 2.0), 
    "reg__estimator__epsilon": [0.001, 0.0025, 0.005]
}

gs_svr = (GridSearchCV(estimator=pipe_svr, 
                      param_grid=grid_param_svr, 
                      cv=2,
                      scoring = 'neg_mean_squared_error',
                      n_jobs = -1))

gs_svr = gs_svr.fit(x_train,y_train)



print(gs_svr.best_estimator_)
print(gs_svr.best_params_)
pd.DataFrame(gs_svr.cv_results_).sort_values('rank_test_score')

'''