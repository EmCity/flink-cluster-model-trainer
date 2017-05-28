"""
Created on Wed May 17 14:40:12 2017

@author: Mihaela

Filters the traffic from specific weekdays, between specific hours

Input:
    Structure of lists:
        weekdays =[day_of_week, ...]
                 =[0-6, ...]                                Monday = 0, Tuesday = 1, ..., Sunday = 6


        times = [[(hour, minute), (hour,minute)], ...]
              = [[(0-23,0-59), (0-23,0-59)], ...]           each sublist contains two tuples
                                                            first tuple = start time
                                                            second tuple = end time

    example:
        weekdays = [0,1]
        times = [[(6,00), (7,50)], [(12,00), (12,20)]]

        get_traffic(weekdays, times) filters the traffic from Mondays and Tuesdays between 6:00-7:50 and 12:00-12:20
"""

import csv as csv
import numpy as np
import pandas as pd
import os
from datetime import datetime

def get_traffic(weekdays, times):


    training_files = "../../../dataset/training/"
    #if os.name == 'nt':
    #    training_files = "../dataset/testing_phase1/"
    #else:
    #    training_files = "../../../dataset/testing_phase1/"
    trajectories_training_file = "trajectories(table 5)_training.csv"


    df = pd.DataFrame.from_csv(training_files+trajectories_training_file, index_col=[0,1,2])

    # transform starting_time column from string to timestamp
    df['starting_time'] = pd.to_datetime(df['starting_time'])

    # extract separately date and time (hour, minutes) from timestamp
    extracted_hour = df['starting_time'].dt.hour
    extracted_minute = df['starting_time'].dt.minute
    extracted_day = df['starting_time'].dt.dayofweek

    # add 'extracted_day' and 'hour_min_tuples' columns to dataset
    df['extracted_day'] = extracted_day
    df['hour_min_tuples'] = list(zip(extracted_hour, extracted_minute))

    # craete day_mask
    day_mask = df['extracted_day'].isin(weekdays)

    # create time_mask
    time_mask = [False] * df.shape[0]
    for i in times:
        time_mask = time_mask | ((df['hour_min_tuples'] > i[0]) & (df['hour_min_tuples'] <= tuple(np.subtract(i[1],(0,1)))))

    #create complete_mask
    complete_mask = day_mask & time_mask

    #take last added columns out
    del df['extracted_day']
    del df['hour_min_tuples']

    #output
    return(df.loc[complete_mask])

#test
#weekdays = [0]
#times = [[(6,00), (7,50)]]
#get_traffic(weekdays, times)
        
    
