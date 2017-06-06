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
import itertools
import get_traffic as traffic
import Paths as path



def create_20min_partitions(hours):
    """
    splits a timestamp in 20 minutes intervals

    :param hours:
                tuple containing start and end time
                example: (3,5)  start time = 3am; end time = 5am

    :return: list with 20 minutes time intervals
                example: for hours=(2,3), output = [[(2, 0), (2, 20)], [(2, 20), (2, 40)], [(2, 40), (3, 0)]]
    """


    h = list(range(hours[0],hours[1]))
    m = [0, 20, 40]

    times = list(itertools.product(h, m))
    times_list = [list(i) for i in zip(times, times[1:])]
    times_list.append([(hours[1]-1,40), (hours[1],0)])

    return(times_list)


print(create_20min_partitions((2,4)))

def generate_timeInformationVector(hours, days):
    """
    generates
    x = time information
    y = avarage travel time

    !!! uses trajectories_training_file as dataset !!!

    :param hours:
                tuple containing start and end time
                example: (3,5)  start time = 3am; end time = 5am
    :param days:
                list of weekdays
                example: [0,1] takes ony Monday and Tuesdays into consideration

    :return:
    """


    trajectories_df = pd.read_csv(path.trajectories_training_file)
    df = trajectories_df

    df['starting_time'] = pd.to_datetime(df['starting_time'])


    x_initial = np.array([]).astype(int)
    y_initial = np.array([])
    for d in days:
        for t in create_20min_partitions(hours):
            partition_20min = traffic.get_traffic([d], [t])
            x_initial = np.append(x_initial, (d, t[0][0]))
            y_initial = np.append(y_initial, partition_20min['travel_time'].mean())


    x = np.array([]).astype(int)
    for v, w in zip(x_initial[::12],x_initial[1::12]):
        x = np.append(x, (v, w))

    y = [y_initial[n:n+6] for n in range(0, len(y_initial), 6)]

    return(x, y)

#test
#print(generate_timeInformationVector(hours = (2,4), days = [1,2]))
