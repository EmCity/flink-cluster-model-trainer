import unittest
import get_traffic as traffic
import pandas as pd


class GetTrafficTest(unittest.TestCase):

    training_files = "../../../dataset/training/"
    trajectories_file = "trajectories(table 5)_training.csv"

    trajectories_df= None

    # all weekdays
    weekdays = [0, 1, 2, 3, 4, 5, 6]

    # all 20 min windows
    times = [[(8, 00), (8, 20)], [(8, 20), (8, 40)], [(8, 40), (9, 00)], [(9, 00), (9, 20)], [(9, 20), (9, 40)],
             [(9, 40), (10, 00)],
             [(17, 00), (17, 20)], [(17, 20), (17, 40)], [(17, 40), (18, 00)], [(18, 00), (18, 20)],
             [(18, 20), (18, 40)], [(18, 40), (19, 00)]]

    # tw_set1
    # times_para = [[self.times[0][0], self.times[11][1]]]

    def setUp(self):
        self.trajectories_df = pd.read_csv(self.training_files + self.trajectories_file)

    def test_get_simple_result(self):
        weekdays_para = [self.weekdays[0]]
        times_para = [[self.times[0][0], self.times[0][1]]]

        df = traffic.get_traffic(weekdays_para, times_para)
        self.assertIsNotNone(df)

    def test_number_of_results(self):
        weekdays_para = self.weekdays

        times_para = [[(0, 0), (24, 00)]]

        df = traffic.get_traffic(weekdays_para, times_para)

        self.assertEqual(len(df), len(self.trajectories_df))


if __name__ == '__main__':
    unittest.main()
