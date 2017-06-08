from sklearn.svm import SVR
import sklearn
import numpy as np
n_samples, n_features = 10, 5
np.random.seed(0)
y = np.random.randn(n_samples)
X = np.random.randn(n_samples, n_features)
clf = SVR(C=1.0, epsilon=0.2)
clf.fit(X, y) 
y_pred = clf.predict(X)
print("Error of radial basis function model")
print(sklearn.metrics.mean_squared_error(y, y_pred))

clf = SVR(kernel='linear', C=1.0, epsilon=0.2)
clf.fit(X, y) 
y_pred = clf.predict(X)
print("Error of linear model: ")
print(sklearn.metrics.mean_squared_error(y, y_pred))

clf = SVR(kernel='poly', C=1.0, epsilon=0.2)
clf.fit(X, y) 
y_pred = clf.predict(X)
print("Error of polynomial model: ")
print(sklearn.metrics.mean_squared_error(y, y_pred))

clf = SVR(kernel='sigmoid', C=1.0, epsilon=0.2)
clf.fit(X, y) 
y_pred = clf.predict(X)
print("Error of sigmoid model: ")
print(sklearn.metrics.mean_squared_error(y, y_pred))