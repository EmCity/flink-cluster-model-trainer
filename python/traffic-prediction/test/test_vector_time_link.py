import unittest
import numpy as np
import pandas as pd
import test_paths as path
from vector_gen import generateCurrentSituationWithTime as oldGen
from vector_gen import generateCurrentSituationWithTime2 as newGen
from vector_gen import generateTimeInformationVector as timeGen


class TestVector(unittest.TestCase):
    df = pd.read_csv(path.trajectories_training_file)

    def test_checkXVectors(self):
        x, y = oldGen.generate_vector(self.df)
        x2, y2 = newGen.generate_vector(self.df)
        np.testing.assert_array_equal(x, x2)

    def test_checkYVectors(self):
        x, y = oldGen.generate_vector(self.df)
        x2, y2 = timeGen.generate_timeInformationVector(self.df)
        np.testing.assert_array_equal(y, y2)

if __name__ == '__main__':
    unittest.main()