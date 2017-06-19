import src.vector_gen.generateCurrentSituationVector as vec
import src.vector_gen.generate_VectorY as vecY
import src.misc.split_train_valid as split
import src.misc.paths as path
import pandas as pd
from src.misc import evaluation as eval
from sklearn.svm import SVR
from sklearn.multioutput import MultiOutputRegressor

df = pd.read_csv(path.trajectories_training_file)
training, validation, testing = split.split_dataset(df)
X = vec.generate_x_df(training)
y = vecY.generate_VectorY_df(training)
print(X)
print(y)
X_test = vec.generate_x_df(testing)
y_test = vecY.generate_VectorY_df(training)

max_depth = 30
regr_multirf = MultiOutputRegressor(SVR(C=1.0, epsilon=0.2))
regr_multirf.fit(X, y)

regr_rf = SVR(C=1.0, epsilon=0.2)
regr_rf.fit(X, y)

# Predict on new data
y_multirf = regr_multirf.predict(X_test)
y_rf = regr_rf.predict(X_test)

error = eval.mape(y_multirf, y_test)
print(error)

