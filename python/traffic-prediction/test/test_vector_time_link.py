import unittest
import numpy as np
import pandas as pd
from vector_gen import generateCurrentSituationWithTime as oldGen
from vector_gen import generateCurrentSituationWithTime2 as newGen
from vector_gen import generateTimeInformationVector as timeGen


class TestVector(unittest.TestCase):
    df = pd.read_csv("../../../new_dataset/testing_phase/trajectories(table 5)_test2.csv")

    def checkXVectors(self):
        x, y = oldGen.generate_vector(self.df)
        x2, y2 = newGen.generate_vector(self.df)
        np.testing.assert_array_equal(x, x2)

    def checkYVectors(self):
        x, y = oldGen.generate_vector(self.df)
        x2, y2 = timeGen.generate_timeInformationVector(self.df)
        np.testing.assert_array_equal(y, y2)

if __name__ == '__main__':
    unittest.main()