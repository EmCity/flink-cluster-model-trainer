from sklearn.metrics import mean_absolute_error
import numpy as np

def mape(y_pred, y_true):
    return np.mean(np.abs((y_true - y_pred) / y_true))