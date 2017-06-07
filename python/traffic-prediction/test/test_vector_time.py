import unittest
import VectorGeneration_xAsTimeInformation as vector
import pandas as pd
import Paths as path


class TestVectorTime(unittest.TestCase):

    def test_get_result(self):
        df = pd.read_csv(path.trajectories_testing_file)
        result = vector.generate_timeInformationVector(df)

        self.assertIsNotNone(result)

    def test_length_results(self):
        df = pd.read_csv(path.trajectories_testing_file)
        result = vector.generate_timeInformationVector(df)

        self.assertEqual(len(result[0]), len(result[1])*2)

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

        avg_first_20min = df[0:9]['travel_time'].mean()

        self.assertEqual(avg_first_20min, result[1][0][0])



if __name__ == '__main__':
    unittest.main()

