"""
Created on Wed May 20 11:40:00 2017

@author: Christian

Creates a Submission with the average of the last two hours. Uses the training-dataset.
"""
from datetime import date
from datetime import datetime
from datetime import time

import pandas as pd

from misc import Paths as path
from misc.TravelTimeSubmission import TravelTimeSubmission

trajectories_df = pd.read_csv(path.trajectories_testing_file)

df = trajectories_df

df['starting_time'] = pd.to_datetime(df['starting_time'])

# filter day
predict_days = [date(2016, 10, 25), date(2016, 10, 26), date(2016, 10, 27), date(2016, 10, 28), date(2016, 10, 29),
                date(2016, 10, 30), date(2016, 10, 31)]

# tw_set1
tw_sets = ((time(6, 0), time(8, 0)), (time(15, 0), time(17, 0)))

days_list = []
for day in predict_days:
    tw_per_tw_sets = []
    for tw_set in tw_sets:
        # print(day,tw_set)
        datetime1 = datetime.combine(day, tw_set[0])
        datetime2 = datetime.combine(day, tw_set[1])
        df2 = df[(df['starting_time'] >= datetime1) & (df['starting_time'] < datetime2)]
        df3 = df2.groupby(['intersection_id', 'tollgate_id'])['travel_time'].mean()

        average_per_route = [df3[0], df3[1], df3[2], df3[3], df3[4], df3[5]]
        tw_per_tw_sets.append(
            [average_per_route, average_per_route, average_per_route, average_per_route, average_per_route,
             average_per_route])

    days_list.append(tw_per_tw_sets)

print(days_list)

# create it!
tts = TravelTimeSubmission()
tts.travel_time_submission(days_list, predict_days[0], file_name='submission_travelTime_2h_tw_avg.csv')
