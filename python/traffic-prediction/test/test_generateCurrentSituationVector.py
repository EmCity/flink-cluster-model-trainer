import unittest
import test_path as path
import pandas as pd
from vector_gen import generateCurrentSituationVector as gen

class TestVector(unittest.TestCase):
    df = pd.read_csv(path.trajectories_training_file2)
    x, y = gen.generate_vector(df)

    def test_on_training2Y(self):
        # days*hours*window/h*values - 2h
        number_Y = 7 * 24 * 3 * 6 - 1 * 2 * 3 * 6
        self.assertEqual(len(self.y), number_Y)
    def test_on_training2X(self):
        # days*hours*window/h*values -2h
        number_X = 7 * 24 * 3 * 24 - 1 * 2 * 3 * 24
        self.assertEqual(len(self.x), number_X)

    #def test_get_simple_result(self):
     #   df = pd.read_csv("test.csv")
        #x, y = gen.generate_vector(df)
        #np.testing.assert_array_equal(x, np.array([1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]))
        #np.testing.assert_array_equal(y, np.array([6,8,9,5,12,8]))

if __name__ == '__main__':
    unittest.main()