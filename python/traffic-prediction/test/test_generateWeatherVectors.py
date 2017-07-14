import unittest

import src.vector_gen.generateWeatherVectors as gwv
import pandas as pd
from test import test_path as path

class GenerateWeatherVectorsTest(unittest.TestCase):

    trajectories_df = None
    weather_df = None

    def setUp(self):
        self.trajectories_df = pd.read_csv(path.trajectories_training_file2)
        self.weather_df = pd.read_csv(path.weather_training_file)

    def test_get_simple_result(self):

        X = gwv.generate_TimeInformationCurrentSituationWeatherVectors(self.trajectories_df, self.weather_df)
        self.assertIsNotNone(X)

    def test_length_of_timeIimeInformationCurrentSituationWeatherVector_X(self):
        X = gwv.generate_TimeInformationCurrentSituationWeatherVectors(self.trajectories_df, self.weather_df)

        # 91 days of training data, 12*2hours per day(
        number = 7*12
        self.assertEqual(len(X), number)


if __name__ == '__main__':
    unittest.main()
