import unittest
import pandas as pd
import test_path as path
from vector_gen import generateCurrentSituationWithTime as gen

class TestVector(unittest.TestCase):
    df = pd.read_csv(path.trajectories_training_file2)
    x, y = gen.generate_vector(df)

    def test_on_training2Y(self):
        # days*hours*window/h*values - 2h
        number_Y = 7 * 24 * 3 * 6 - 1 * 2 * 3 * 6
        self.assertEqual(len(self.y), number_Y)

    def test_on_training2X(self):
        # days*hours*window/h*values -2h
        number_X = 7 * 24 * 3 * 27 - 1 * 2 * 3 * 27
        self.assertEqual(len(self.x), number_X)

if __name__ == '__main__':
    unittest.main()