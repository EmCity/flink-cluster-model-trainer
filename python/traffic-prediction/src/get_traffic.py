"""
Created on Wed May 17 14:40:12 2017

@author: Mihaela
"""

import csv as csv
import numpy as np
import pandas as pd
import os
from datetime import datetime

def get_traffic(weekdays, times):
    if os.name == 'nt':
        #if operating system is Windows
        path_trajectories = 'D:/Docs/Master/Semester 2/Big Data Science Praktikum/datasets/training/trajectories(table 5)_training.csv'
    else:
        #Unix filesystem
        path_trajectories = '../../../dataset/training/trajectories(table 5)_training.csv'

    df = pd.DataFrame.from_csv(path_trajectories, index_col=[0,1,2])

    # transform starting_time column from string to timestamp
    df['starting_time'] = pd.to_datetime(df['starting_time'])

    # extract separately date and time from timestamp
    extracted_time = df['starting_time'].dt.hour
    extracted_day = df['starting_time'].dt.dayofweek

    # add 'extracted_day' and 'extracted_time' columns to dataset
    df['extracted_day'] = extracted_day
    df['extracted_time'] = extracted_time

    # craete day_mask
    day_mask = df['extracted_day'].isin(weekdays)

    # create time_mask
    time_mask = [False] * df.shape[0]
    for i in times:
        time_mask = time_mask | ((df['extracted_time'] + 1 > int(i[0])) & (df['extracted_time'] + 1 <= int(i[1])))

    #create complete_mask
    complete_mask = day_mask & time_mask

    #take last added columns out
    del df['extracted_time']
    del df['extracted_day']

    #output
    print(df.loc[complete_mask])


#test
days = [0,1]
hours = [(0,2), (5,8), (20,21)]
get_traffic(weekdays=days, times=hours)


        
    
