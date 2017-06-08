"""
The generate_timeInformationVector() function generates two numpy arrays:
        1. x array
                contains information about the weekday, the hour and the minutes
                example: [1 2 0 1 4 20] means [Tuesday 2:00am Tuesday 4:20am]

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
    X = []
    for name, group in df_group:
        list = [name.weekday(), name.hour, name.minute]
        X.append(list)

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

    #build  X and Y
    X = np.concatenate(X)
    Y = np.concatenate(Y)
    return X, Y

#test
#print(generate_timeInformationVector(pd.read_csv(path.trajectories_testing_file)))

