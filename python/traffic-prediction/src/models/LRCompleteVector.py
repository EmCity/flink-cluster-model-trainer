import vector_gen.generateCurrentSituationVector as vec
import misc.split_train_valid as split
import misc.paths as path
import pandas as pd
from misc import evaluation as eval
from sklearn.ensemble import RandomForestRegressor
from sklearn.multioutput import MultiOutputRegressor

df = pd.read_csv(path.trajectories_training_file)
training, validation, testing = split.split_dataset(df)
X = vec.generate_x_df(training)
Y = vec.convertY(training)

X_test = vec.generate_x_df(testing)
y_test = vec.convertY(testing)


max_depth = 30
regr_multirf = MultiOutputRegressor(RandomForestRegressor(max_depth=max_depth,
                                                          random_state=0))
regr_multirf.fit(X, Y)

regr_rf = RandomForestRegressor(max_depth=max_depth, random_state=2)
regr_rf.fit(X, Y)

# Predict on new data
y_multirf = regr_multirf.predict(X_test)
y_rf = regr_rf.predict(X_test)

error = eval.mape(y_multirf, y_test)
print(error)

