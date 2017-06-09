from datetime import datetime

import pandas as pd

from misc import TravelTimeSubmission as submission, get_traffic as traffic


def from_index_to_prediction_day(day, h):
    if day > 0:
        start = datetime(2016, 10, 24 + day, h[0][0], h[0][1], 0)
        end = datetime(2016, 10, 24 + day, h[1][0], h[1][1], 0)
    else: #monday (0) is the 31.10.2016
        start = datetime(2016, 10, 31 + day, h[0][0], h[0][1], 0)
        end = datetime(2016, 10, 31 + day, h[1][0], h[1][1], 0)
    return "[" + str(start) + "," + str(end) + ")"

#we are interested in all weekdays
weekdays = [0, 1, 2, 3, 4, 5, 6]

# all 20 min windows
times = [[(8, 00), (8, 20)], [(8, 20), (8, 40)], [(8, 40), (9, 00)], [(9, 00), (9, 20)], [(9, 20), (9, 40)],[(9, 40), (10, 00)],
         [(17, 00), (17, 20)], [(17, 20), (17, 40)], [(17, 40), (18, 00)], [(18, 00), (18, 20)], [(18, 20), (18, 40)],[(18, 40), (19, 00)]]

# the result panda data frame
dfResult = pd.DataFrame(columns=["intersection_id", "tollgate_id", "avg_travel_time", "time_window"])

# iterate over all weekday - timeWindow pairs
for day in weekdays:
    for hours in times:
        # calculate for each timewindow the avg_travel_time based on the data in this time window
        df2 = traffic.get_traffic([day], [[(hours[0][0], hours[0][1]), (hours[1][0], hours[1][1])]]).groupby(['intersection_id', 'tollgate_id'])[
            'travel_time'].mean().reset_index(name="avg_travel_time")
        df3 = pd.DataFrame(df2, columns=["intersection_id", "tollgate_id", "avg_travel_time", "time_window"])
        # add the time window column to the dataframe
        df3["time_window"] = from_index_to_prediction_day(day, hours)
        # add the time window data to the result data frame
        dfResult = pd.concat([dfResult, df3], axis=0, ignore_index=1)

dfResult = dfResult[["intersection_id", "tollgate_id", "avg_travel_time", "time_window"]]
submission.TravelTimeSubmission.save_df_travel_time_submission(submission.TravelTimeSubmission, dfResult)

