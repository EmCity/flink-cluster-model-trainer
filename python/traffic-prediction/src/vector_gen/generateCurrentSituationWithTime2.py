from vector_gen import generateCurrentSituationVector as vec
from vector_gen import generateTimeInformationVector as vec2
import numpy as np

def generate_vector(df):
    X, Y = vec.generate_vector(df)
    X_2, _ = vec2.generate_timeInformationVector(df)
    list3 = []
    while len(X) != 0 or len(X_2) != 0:
        list3.extend(X_2[0:3])
        X_2 = np.delete(X_2, range(3))
        list3.extend(X[0:23])
        X = np.delete(X, range(23))
    return np.array([list3]), Y