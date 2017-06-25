from sklearn.multioutput import MultiOutputRegressor
from sklearn.svm import SVR
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
import sklearn.linear_model as linear_model

import pandas as pd
import numpy as np

if __name__ == '__main__':

    ##load data
    x_train = pd.read_csv('train_X.csv', index_col =0)
    x_test = pd.read_csv('test_X.csv', index_col =0)
    y_train = pd.read_csv('train_Y.csv', index_col =0)
    y_test = pd.read_csv('test_Y.csv', index_col =0)

    pipe_svr = Pipeline([ ('reg', linear_model.MultiTaskElasticNetCV())])

    print(pipe_svr.get_params().keys())

    grid_param_svr = {
        "reg__alphas": np.arange(0.0, 2, 0.1),
        'reg__l1_ratio': np.arange(0, 1, 0.01),
    }

    gs_svr = (GridSearchCV(estimator=pipe_svr,
                          param_grid=grid_param_svr,
                          cv=2,
                          scoring = 'neg_mean_absolute_error',
                          n_jobs = 8))

    gs_svr = gs_svr.fit(x_train,y_train)
    print(gs_svr.best_params_)
    values = pd.DataFrame(gs_svr.cv_results_).sort_values('rank_test_score')
    print(values)
    print(gs_svr.best_estimator_)
