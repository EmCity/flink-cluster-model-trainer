#import src.vector_gen.generateWeatherVectors as vec
import src.vector_gen.generateCurrentSituationWithTime as vec
import src.vector_gen.generate_VectorY as vecY
import src.misc.split_train_valid as split
import pandas as pd
from sklearn import linear_model
from src.misc import evaluation as eval
import numpy as np
from sklearn.externals import joblib

##load data
df = pd.read_csv('../../../../../dataset/training/trajectories(table 5)_training.csv')
#df_w = pd.read_csv('../../../../../dataset/training2/weather (table 7)_training_update.csv')

##split into training, validation, testing
training, validation, testing = split.split_dataset(df)

#generate training vectors
X = vec.generate_vector(training).as_matrix()
y = vecY.generate_VectorY_df(training).as_matrix()

#generate model
clf = linear_model.MultiTaskElasticNet()

#train model with training vectors
clf.fit(X, y)

#generate test vectors
X_test = vec.generate_vector(testing).as_matrix()
y_test = vecY.generate_VectorY_df(training).as_matrix()

#
y_pred = clf.predict(X)

#calculate error
error = eval.mape(y_pred, y)
print(error)
print(np.mean(np.array(error)))

#save model
joblib.dump(clf, 'MultiTaskElasticNetCurrentSituationWithTime.pkl')
