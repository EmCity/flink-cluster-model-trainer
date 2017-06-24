from sklearn import svm, model_selection
import src.vector_gen.generateCurrentSituationVector as vecX
import src.vector_gen.generate_VectorY as vecY
import src.misc.split_train_valid as split
import src.misc.paths as path
import pandas as pd
import numpy as np

np.set_printoptions(threshold=np.nan)

df = pd.read_csv(path.trajectories_training_file2)

training, validation, testing = split.split_dataset(df)

X_train = vecX.generate_x_df(training)
Y_train = vecY.generate_VectorY_df(training)

X_test = vecX.generate_x_df(testing)
Y_test = vecY.generate_VectorY_df(testing)


#model

from sklearn.multioutput import MultiOutputRegressor

clf = svm.SVR(C=30, epsilon=0.005)

regr_multi_svr = MultiOutputRegressor(clf)

regr_multi_svr.fit(X_train, Y_train)
Y_pred= regr_multi_svr.predict(X_test)

#print(Y_pred)
#print(len(Y_pred))


#MAPE

from src.misc import evaluation as eval
error = eval.mape(Y_pred, Y_test)

print(error)
print(np.mean(np.array(error)))

