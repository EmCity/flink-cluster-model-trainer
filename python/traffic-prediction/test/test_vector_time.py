import unittest

from vector_gen import generateTimeInformationVector as vector
import pandas as pd
import test_paths as path


class TestVectorTime(unittest.TestCase):

    def test_get_result(self):
        df = pd.read_csv(path.trajectories_testing_file)
        result = vector.generate_timeInformationVector(df)

        self.assertIsNotNone(result)

    def test_validity_of_hour_minute(self):
        df = pd.read_csv(path.trajectories_training_file)
        result = vector.generate_timeInformationVector(df)

        weekdays = list(set(result[0][::2]))
        hours = list(set(result[0][1::2]))

        self.assertEqual(weekdays, list(range(0,7)))
        self.assertEqual(hours, list(range(0,24)))

    def test_average_Y(self):
        df = pd.read_csv(path.trajectories_testing_file)
        result = vector.generate_timeInformationVector(df)

        list_index = [0, 2, 7, 8]
        avg_first_20min_routeA2 = df.ix[list_index]['travel_time'].mean()

        self.assertEqual(avg_first_20min_routeA2, result[1][0])

if __name__ == '__main__':
    unittest.main()

