"""
The generate_timeInformationVector() function generates two numpy arrays:
        1. x array
                contains information about the weekday and the hour for every 2 hours
                example: [1 2 1 4] means [Tuesday 2am Tuesday 4am]

        2. y array
                contains the average travel time for every 20 minutes
                each row is a subarray containing
                    6 x avg_traveltime = [avg_traveltime(first_20min), avg_traveltime(second_20min), ... ]
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
    X = np.array(X)

    #Generate Y
    average_time = list(df_group['travel_time'].mean())
    Y = [average_time[n:n+6] for n in range(0, len(average_time), 6)]
    Y = np.array(Y)


    return(X, Y)

#test
#print(generate_timeInformationVector(pd.read_csv(path.trajectories_testing_file)))

