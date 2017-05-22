"""
Created on Wed May 20 11:40:00 2017

@author: Christian

Creates a Submission with the average of the last two hours. Uses the training-dataset.
"""
import pandas as pd
import numpy as np
import os
from datetime import timedelta
from datetime import time
from datetime import date
from datetime import datetime

from TravelTimeSubmission import TravelTimeSubmission


#import os
#print(os.getcwd())

#training_files = "../../../dataset/testing_phase1/"
if os.name == 'nt':
    training_files = "../dataset/testing_phase1/"
else:
    training_files = "../../../dataset/testing_phase1/"
trajectories_testing_file = "trajectories(table 5)_test1.csv"

trajectories_df = pd.read_csv(training_files+trajectories_testing_file)


df = trajectories_df

df['starting_time'] = pd.to_datetime(df['starting_time'])

# filter day
predict_days = [date(2016, 10, 18), date(2016, 10, 19), date(2016, 10, 20), date(2016, 10, 21), date(2016, 10, 22),
                date(2016, 10, 23), date(2016, 10, 24)]

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
tts.travel_time_submission(days_list, predict_days[0])
