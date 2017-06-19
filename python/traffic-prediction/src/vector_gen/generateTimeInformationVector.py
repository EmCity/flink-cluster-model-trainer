"""
The generate_timeInformationVector() function generates two numpy arrays:
        1. x array
                contains information about the weekday, the hour and the minutes
                example: [1 2 0 1 4 20] means [Tuesday 2:00am Tuesday 4:20am]
"""
import numpy as np
import pandas as pd


def generate_timeInformationVector(df):
    df['starting_time'] = df['starting_time'].astype('datetime64[ns]')
    #Get a 20 min sliding window for the dataframe
    df_group = df.groupby([pd.Grouper(key='starting_time', freq='2h')])

    #Generate X
    X = []
    for name, group in df_group:
        list = [name.weekday(), name.hour, name.minute]
        X.append(list)

    #build X array
    X = np.array(X)
    #build  X
    X = np.concatenate(X)
    #delete last 2h of X -> no prediction is available 3 values
    X = X[:-3]
    return X

