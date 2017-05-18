"""
Created on Wed May 17 14:40:12 2017

@author: Mihaela
"""

import csv as csv
import numpy as np
import pandas as pd
from datetime import datetime


path_trajectories = 'D:/Docs/Master/Semester 2/Big Data Science Praktikum/datasets/training/trajectories(table 5)_training.csv'


def get_traffic(weekday, times):
    #read csv to pandas dataframe
    start_time, end_time = times
    df = pd.DataFrame.from_csv(path_trajectories)

    #transform starting_time column from string to timestamp
    df['starting_time'] = pd.to_datetime(df['starting_time'])

    #define starting_time column as timestamp
    timestamp = df['starting_time']

    #extract separately date and time from timestamp
    extracted_time = timestamp.dt.hour
    extracted_day = timestamp.dt.dayofweek

    #create mask
    mask = (extracted_time+1 > start_time) & (extracted_time+1 <= end_time) & (extracted_day == weekday)

    print(df.loc[mask])


#test
start = 6 #start time = 6 o'cklock
end = 7 #end_time = 7 o'cklock
day = 0 #day = Monday
get_traffic(day,(start, end))






        
    
