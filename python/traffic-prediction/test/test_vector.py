import unittest

import numpy as np
import pandas as pd

from vector_gen import generateCurrentSituationVector as gen


class TestVector(unittest.TestCase):

    def test_get_simple_result(self):
        df = pd.read_csv("test.csv")
        x, y = gen.generate_vector(df)
        np.testing.assert_array_equal(x, np.array([1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]))
        np.testing.assert_array_equal(y, np.array([6,8,9,5,12,8]))

if __name__ == '__main__':
    unittest.main()