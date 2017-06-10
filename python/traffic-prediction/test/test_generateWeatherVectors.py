import unittest

import src.vector_gen.generateWeatherVectors as gwv
import pandas as pd
from pandas.util.testing import assert_frame_equal

from misc import get_traffic as traffic, Paths as path


class GenerateWeatherVectorsTest(unittest.TestCase):

    trajectories_df = None
    weather_df = None

    def setUp(self):
        self.trajectories_df = pd.read_csv(path.trajectories_training_file[3:])
        self.weather_df = pd.read_csv(path.weather_training_file[3:])

    def test_get_simple_result(self):

        X, Y = gwv.generate_timeInformationWeatherVectors(self.trajectories_df, self.weather_df)
        self.assertIsNotNone(X)
        self.assertIsNotNone(Y)

    def test_length_of_Y(self):
        X, Y = gwv.generate_timeInformationWeatherVectors(self.trajectories_df, self.weather_df)

        # 90 days of training data, 24hours per day, 3 tw per hour, 6 routes per tw, 1 value (avg_travel_time)
        number = 90*24*3*6
        # - 2h
        number -= 2*3*6

        self.assertEqual(len(Y), number)

    def test_length_of_timeInformationWeatherVector_X(self):
        X, Y = gwv.generate_timeInformationWeatherVectors(self.trajectories_df, self.weather_df)

        # 90 days of training data, 24hours per day, 3 tw per hour, 10 values (
        # weekday ,hour, minute, pressure, sea_pressure, wind_direction, wind_speed, temperature, rel_humidity, precipitation)
        number = 90*24*3*10
        # - 2h
        number -= 2*3*10

        self.assertEqual(len(X), number)


if __name__ == '__main__':
    unittest.main()
