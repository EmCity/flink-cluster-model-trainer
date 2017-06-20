import src.vector_gen.generateWeatherVectors as vec
import src.vector_gen.generate_VectorY as vecY
import src.misc.split_train_valid as split
import src.misc.paths as path
import pandas as pd
from sklearn.svm import SVR


df = pd.read_csv(path.trajectories_training_file)
df_w = pd.read_csv(path.weather_training_file)
training, validation, testing = split.split_dataset(df)
X = vec.generate_TimeInformationCurrentSituationWeatherVectors(training, df_w)

print(X.isnull().any())

y = vecY.generate_VectorY_df(training)
y_1 = y['2', 'A2']

#print(X)
clf = SVR(C=1.0, epsilon=0.2)
clf.fit(X, y_1)

X_test = vec.generate_TimeInformationCurrentSituationWeatherVectors(testing)
y_test = vecY.generate_VectorY_df(training)
y_pred = clf.predict(X)

#print (X)
#print(X_test)

#print(len(y_pred))
#print (len(y_test_1))
error = eval.mape(y_pred, y_1)
print (error)

