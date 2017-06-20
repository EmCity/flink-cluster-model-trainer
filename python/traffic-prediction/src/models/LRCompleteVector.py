#import src.vector_gen.generateWeatherVectors as vec
import src.vector_gen.generateCurrentSituationWithTime as vec
import src.vector_gen.generate_VectorY as vecY
import src.misc.split_train_valid as split
import src.misc.paths as path
import pandas as pd
from sklearn import linear_model
from src.misc import evaluation as eval
import numpy as np
from sklearn.externals import joblib


df = pd.read_csv(path.trajectories_training_file)
df_w = pd.read_csv(path.weather_training_file)
training, validation, testing = split.split_dataset(df)
X = vec.generate_vector(training)


y = vecY.generate_VectorY_df(training)
y#_1 = y['2', 'A2']

#print(X)
clf = linear_model.MultiTaskElasticNet()
clf.fit(X, y)

joblib.dump(clf, 'MultiTaskElasticNetCurrentSituationWithTime.pkl')

X_test = vec.generate_vector(testing)
y_test = vecY.generate_VectorY_df(training)
y_pred = clf.predict(X)

#print (X)
#print(X_test)

#print(len(y_pred))
#print (len(y_test_1))
error = eval.mape(y_pred, y)
print(error)
print(np.mean(np.array(error)))
