import unittest

import pandas as pd
from pandas.util.testing import assert_frame_equal

from misc import get_traffic as traffic, Paths as path


class GetTrafficTest(unittest.TestCase):

    trajectories_df = None

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
        self.trajectories_df = pd.read_csv(path.trajectories_training_file)

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

    def test_pandas_equal(self):
        weekdays_para = self.weekdays

        times_para = [[(0, 0), (24, 00)]]

        df = traffic.get_traffic(weekdays_para, times_para)

        df_original = self.trajectories_df
        df_original = df_original.set_index(['intersection_id', 'tollgate_id', 'vehicle_id'])
        df_original['starting_time'] = pd.to_datetime(df_original['starting_time'])

        assert_frame_equal(df, df_original)

    def test_pandas_equal_weekday_3(self):
        weekdays_para = [3]

        times_para = [[(0, 0), (24, 0)]]

        df = traffic.get_traffic(weekdays_para, times_para)

        df_original = self.trajectories_df
        df_original = df_original.set_index(['intersection_id', 'tollgate_id', 'vehicle_id'])
        df_original['starting_time'] = pd.to_datetime(df_original['starting_time'])

        df_original = df_original[df_original['starting_time'].dt.dayofweek == weekdays_para]
        df_original['starting_time'] = pd.to_datetime(df_original['starting_time'])

        assert_frame_equal(df, df_original)

    def test_pandas_equal_weekday_1_tw_59(self):
        weekdays_para = [1]

        times_para = [[(14, 59), (14, 60)]]

        df = traffic.get_traffic(weekdays_para, times_para)

        df_original = self.trajectories_df
        df_original = df_original.set_index(['intersection_id', 'tollgate_id', 'vehicle_id'])
        df_original['starting_time'] = pd.to_datetime(df_original['starting_time'])

        df_original = df_original[df_original['starting_time'].dt.dayofweek == weekdays_para]
        df_original = df_original[
            (df_original['starting_time'].dt.hour >= 14) & (df_original['starting_time'].dt.hour <= 14) &
            (df_original['starting_time'].dt.minute >= 59) & (df_original['starting_time'].dt.minute <= 59)]

        assert_frame_equal(df, df_original)


if __name__ == '__main__':
    unittest.main()
