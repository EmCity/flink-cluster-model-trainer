from vector_gen import generateCurrentSituationVector as vec
from vector_gen import generateTimeInformationVector as vec2
import numpy as np


def generate_vector(df):
    X, Y = vec.generate_vector(df)
    X_2, Y_2 = vec2.generate_timeInformationVector(df)
    list3 = []
    while len(X) != 0 or len(X_2) != 0:
        list3.extend(X_2[:3])
        X_2 = X_2[3:]
        list3.extend(X[:23])
        X = X[23:]
    return np.array(list3), Y