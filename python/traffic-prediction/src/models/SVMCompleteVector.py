from sklearn.svm import SVR
import sklearn
import vector_gen.generateCurrentSituationWithTime as vec
import misc.split_train_valid as split
import misc.Paths as path
import pandas as pd

df = pd.DataFrame.from_csv(path.trajectories_training_file, index_col=[0, 1, 2])
training, validation, testing = split.split_dataset(df, 0.8, 0.1)
X,Y = vec.generate_vector(training)

clf = SVR(C=1.0, epsilon=0.2)
clf.fit(X, Y)
y_pred = clf.predict(X)
print("Error of radial basis function model")
print(sklearn.metrics.mean_squared_error(Y, y_pred))

clf = SVR(kernel='linear', C=1.0, epsilon=0.2)
clf.fit(X, Y)
y_pred = clf.predict(X)
print("Error of linear model: ")
print(sklearn.metrics.mean_squared_error(Y, y_pred))

clf = SVR(kernel='poly', C=1.0, epsilon=0.2)
clf.fit(X, Y)
y_pred = clf.predict(X)
print("Error of polynomial model: ")
print(sklearn.metrics.mean_squared_error(Y, y_pred))

clf = SVR(kernel='sigmoid', C=1.0, epsilon=0.2)
clf.fit(X, Y)
y_pred = clf.predict(X)
print("Error of sigmoid model: ")
print(sklearn.metrics.mean_squared_error(Y, y_pred))


