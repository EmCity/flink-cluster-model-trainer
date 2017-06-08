"""
The diabetes dataset consists of 442 total samples, having
    X = 10 physiological variables (e.g. age, sex, weight, blood pressure, ...)
    Y = indication of disease progression after one year

=> TASK: predict disease progression from physiological variables
"""

import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, linear_model

# Load the diabetes dataset
diabetes = datasets.load_diabetes()

#Use only one variable (3rd)
diabetes_X = diabetes.data[:, np.newaxis, 2]

# Split the data into training/testing sets; test=80%, train=20%
diabetes_X_train = diabetes_X[:-20]
diabetes_X_test = diabetes_X[-20:]

# Split the targets into training/testing sets; test=80%, train=20%
diabetes_y_train = diabetes.target[:-20]
diabetes_y_test = diabetes.target[-20:]

#-----------------------------------------------------------------------------------------------------------------------
#Linear Regression by hand:
#y = b0 + b1 * x

#Mean
def mean(values):
    return sum(values) / float(len(values))

#Variance
def variance(values, mean):
    return sum([(x-mean)**2 for x in values])

#Covariance
def covariance(x, mean_x, y, mean_y):
    covar = 0.0
    for i in range(len(x)):
        covar += (x[i] - mean_x) * (y[i] - mean_y)
    return covar

mean_x = mean(diabetes_X_train)
mean_y = mean(diabetes_y_train)
var_x = variance(diabetes_X_train, mean_x)
var_y = variance(diabetes_y_train, mean_y)
cov_xy = covariance(diabetes_X_train, mean_x, diabetes_y_train, mean_y)

print("Computations by hand:")
print("Mean x: %.5f" % mean_x)
print("Mean y: %.5f" % mean_y)
print("Variance x: %.5f" % var_x)
print("Variance y: %.5f" % var_y)
print("Covariance xy: %.5f" % cov_xy)

#Coefficients b0 and b1
b1 = covariance(diabetes_X_train, mean_x, diabetes_y_train, mean_y) / variance(diabetes_X_train, mean_x)
b0 = mean(diabetes_y_train) - b1 * mean(diabetes_X_train)

print("b0: %.5f" % b0)
print("b1: %.5f" % b1)

#-----------------------------------------------------------------------------------------------------------------------
#Linear Regression with functions in Python:

# Create linear regression object
regression1 = linear_model.LinearRegression()

# Train the model using the training sets
regression1.fit(diabetes_X_train, diabetes_y_train)

# The coefficients b0, b1
print("\nComputations by sklearn function:")
print("Coefficient b0: %.5f" % regression1.intercept_)
print("Coefficient b1: %.5f" % regression1.coef_)
print("Mean squared error: %.5f"
      % np.mean((regression1.predict(diabetes_X_test) - diabetes_y_test) ** 2))
print('Variance score: %.5f' % regression1.score(diabetes_X_test, diabetes_y_test))

# # Plot outputs
# plt.scatter(diabetes_X_test, diabetes_y_test,  color='black')
# plt.plot(diabetes_X_test, regression1.predict(diabetes_X_test), color='blue',
#          linewidth=3)
#
# plt.xticks(())
# plt.yticks(())
#
# plt.show()

#-----------------------------------------------------------------------------------------------------------------------
#Linear Regression for whole dataset in sklearn

diabetes_X_train_whole = diabetes.data[:-20]
diabetes_X_test_whole = diabetes.data[-20:]

regression2 = linear_model.LinearRegression()
regression2.fit(diabetes_X_train_whole, diabetes_y_train)

print("\nLinear Regression for whole dataset:")
print("Coefficient b0: %.5f" % regression2.intercept_)
print("Coefficients b1,..,b10:")
print(regression2.coef_)
print("Mean squared error: %.5f" % np.mean((regression2.predict(diabetes_X_test_whole)-diabetes_y_test)**2))
print("Variance score: %.5f" % regression2.score(diabetes_X_test_whole, diabetes_y_test))

