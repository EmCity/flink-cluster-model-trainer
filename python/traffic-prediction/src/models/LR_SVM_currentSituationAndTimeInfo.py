from sklearn import svm, model_selection
from sklearn.multioutput import MultiOutputRegressor
import src.vector_gen.generateCurrentSituationWithTime as vecX
import src.vector_gen.generate_VectorY as vecY
import src.misc.split_train_valid as split
import src.misc.paths as path
from sklearn import linear_model
import pandas as pd
import numpy as np
from sklearn.externals import joblib
from src.misc import evaluation as eval


np.set_printoptions(threshold=np.nan)

df = pd.read_csv(path.trajectories_training_file2)

#X_train, X_test, Y_train, Y_test = model_selection.train_test_split(X,Y,test_size=0.2)
training, validation, testing = split.split_dataset(df)
X_train = vecX.generate_x_df(training)
Y_train = vecY.generate_VectorY_df(training)

X_test = vecX.generate_x_df(testing)
Y_test = vecY.generate_VectorY_df(testing)

clf = linear_model.MultiTaskElasticNet()
clf.fit(X_train, Y_train)


Y_pred = clf.predict(X_test)


error = eval.mape(Y_pred, Y_test)

print(error)
print("MAPE Linear Regression: ", np.mean(np.array(error)))

print("From here the SVM starts")

svm = svm.SVR(C=30, epsilon=0.005, cache_size=2000)
svm = MultiOutputRegressor(svm, n_jobs=1) #getting a error with n_jobs > 1
svm.fit(X_train, Y_train)


Y_pred = svm.predict(X_test)


error = eval.mape(Y_pred, Y_test)

print(error)
print("MAPE SVM: ", np.mean(np.array(error)))


