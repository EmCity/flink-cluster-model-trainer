import numpy as np

def mape(y_pred, y_true):
    return np.mean(np.abs((y_true - y_pred) / y_true))