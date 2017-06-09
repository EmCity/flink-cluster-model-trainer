import unittest

import numpy as np
import pandas as pd
from misc import Paths as path

from vector_gen import generateCurrentSituationWithTime as old_gen
from vector_gen import generateTimeInformationVector as time_gen

from vector_gen import generateCurrentSituationWithTime2 as new_gen


class TestVector(unittest.TestCase):

    def test_get_simple_result(self):
        df = pd.read_csv(path.trajectories_testing_file)
        x, y = old_gen.generate_vector(df)
        x2, y2 = new_gen.generate_vector(df)
        x3, y3 = time_gen.generate_timeInformationVector(df)
        np.testing.assert_array_equal(x, x2)
        np.testing.assert_array_equal(y, y3)

if __name__ == '__main__':
    unittest.main()