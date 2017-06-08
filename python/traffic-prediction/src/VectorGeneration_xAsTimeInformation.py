"""
The generate_timeInformationVector() function generates two numpy arrays:
        1. x array
                contains information about the weekday and the hour for every 2 hours
                example: [1 2 1 4] means [Tuesday 2am Tuesday 4am]

        2. y array
                contains the average travel time for every 20 minutes
                [route1_avg_travel_time(time_window_1), route2_avg_travel_time(time_window_1), ... , route6_avg_travel_time(time_window_6)]
                array length per 2 hours = 6 time windows a 20 minutes * 6 routes = 36
"""
import numpy as np
import pandas as pd
import Paths as path


def generate_timeInformationVector(df):
    df['starting_time'] = df['starting_time'].astype('datetime64[ns]')

    #Get a 20 min sliding window for the dataframe
    df_group = df.groupby([pd.Grouper(key='starting_time', freq='20min')])

    #Generate X
    first_row = list(df_group['starting_time'].first())
    day_hour_tuple = [[first_row[i].dayofweek, first_row[i].hour] for i in range(0, len(first_row))]
    X = day_hour_tuple[::6]
    X = [j for i in X for j in i]

    #delete last 2 h of X -> no prediction can be made on this data
    #del X[-2:]

    #build X array
    X = np.array(X)

    Y = []
    #Generate Y
    for name, group in df_group:
        df_temp = group.groupby(['intersection_id', 'tollgate_id'])['travel_time'].mean().reset_index(name="avg_travel_time")
        np_arr = df_temp['avg_travel_time'].tolist()
        Y.append(np_arr)

    #delete first 2h of Y -> no prediction can be made on this data
    #del Y[0:5]

    #build  Y
    Y = np.concatenate(Y)
    return(X, Y)

#test
#print(generate_timeInformationVector(pd.read_csv(path.trajectories_testing_file)))

