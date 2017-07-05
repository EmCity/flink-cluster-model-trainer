import numpy as np
import pandas as pd
import src.vector_gen.generateCurrentSituationWithWeather as vecX
import src.vector_gen.generate_VectorY as vecY
import src.misc.split_train_valid_notRandom as split
import src.misc.evaluation as evaluation
import src.misc.paths as paths
from sklearn import linear_model
from sklearn.svm import SVR
from sklearn.multioutput import MultiOutputRegressor
from sklearn.cross_decomposition import PLSRegression

df_trajectories = pd.read_csv(paths.trajectories_training_file)
df_weather = pd.read_csv(paths.weather_training_file)


# Create dataset
df_X = vecX.generate_x(df_trajectories, df_weather)
df_Y = vecY.generate_VectorY_df(df_trajectories)


# Split data into training, validation and testing sets
split.split_dataset(df_X, df_Y)


training_Y = pd.read_csv("../../../../python/traffic-prediction/src/misc/splitting_csv_files/train_Y.csv", index_col =0)
validation_Y = pd.read_csv("../../../../python/traffic-prediction/src/misc/splitting_csv_files/valid_Y.csv", index_col =0)
testing_Y = pd.read_csv("../../../../python/traffic-prediction/src/misc/splitting_csv_files/test_Y.csv", index_col =0)

training_X = pd.read_csv("../../../../python/traffic-prediction/src/misc/splitting_csv_files/train_X.csv", index_col =0)
validation_X = pd.read_csv("../../../../python/traffic-prediction/src/misc/splitting_csv_files/valid_X.csv", index_col =0)
testing_X = pd.read_csv("../../../../python/traffic-prediction/src/misc/splitting_csv_files/test_X.csv", index_col =0)

#-------------------------------------------------------------------------------
# Linear Model
LR = linear_model.LinearRegression()
LR.fit(training_X, training_Y)

print("\n Linear Regression: \n")
print("Coefficients b0.0,...,b0.6:")
print(LR.intercept_)
print("Coefficients b1.1,...,b6.6:")
print(LR.coef_)
print("R^2 score: %.5f" % LR.score(testing_X, testing_Y))
mape_LR = evaluation.mape(LR.predict(testing_X), testing_Y)
mean_mape_LR = np.mean(np.array(mape_LR))
print("MAPE's:")
print(mape_LR)
print("Mean of MAPE's: %.5f" % mean_mape_LR)

#-------------------------------------------------------------------------------
# Partial leas squares regression
pls = PLSRegression(n_components=2)
pls.fit(training_X,training_Y)

print("\n PLS Regression: \n")
print("Coefficients b1.1,..,b6.6:")
print(pls.coef_)
print("R^2 score: %.5f" % pls.score(testing_X, testing_Y))
mape_pls = evaluation.mape(pls.predict(testing_X), testing_Y)
mean_mape_pls = np.mean(np.array(mape_pls))
print("MAPE's:")
print(mape_pls)
print("Mean of MAPE's: %.5f" % mean_mape_pls)

#---------------------------------------------------------------------------------
# SVM -> SVR
svr = MultiOutputRegressor(SVR(C=10, epsilon=0.05))
svr.fit(training_X, training_Y)

print("\n SVM - SVR: \n")
print("R^2 score: %.5f" % svr.score(testing_X, testing_Y))
mape_svr = evaluation.mape(svr.predict(testing_X), testing_Y)
mean_mape_svr = np.mean(np.array(mape_svr))
print("MAPE's:")
print(mape_svr)
print("Mean of MAPE's: %.5f" % mean_mape_svr)
