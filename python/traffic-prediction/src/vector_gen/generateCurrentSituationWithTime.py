import numpy as np
import pandas as pd

from misc import Paths as path
from vector_gen import generateCurrentSituationVector as vec


def generate_vector(df_orig):
    #Generate X
    df = vec.prepare_df_travelseq(df_orig)
    df['starting_time'] = df['starting_time'].astype('datetime64[ns]')

    #Get a 20 min sliding window for the dataframe
    df_group = df.groupby([pd.Grouper(key='starting_time', freq='20min')])
    df['link_travel_time'] = pd.to_numeric(df['link_travel_time'])

    mylist_X = []
    #Iterate over a sliding window dataframe
    for name, group in df_group:
        #Get the averages travel time per link
        df_temp = group.groupby(['link'])['link_travel_time'].mean().reset_index(name="avg_travel_time")
        list = [name.weekday(), name.hour, name.minute] + df_temp['avg_travel_time'].tolist()

        #Add the averages per link to the List
        mylist_X.append(list)

    #Generate Y
    df_orig['starting_time'] = df_orig['starting_time'].astype('datetime64[ns]')

    #Get a 20 min sliding window for the dataframe
    df_orig_group = df_orig.groupby([pd.Grouper(key='starting_time', freq='20min')])

    mylist_Y = []
    #Iterate over a sliding window dataframe
    for name, group in df_orig_group:
        #Get the averages travel time route
        df_temp = group.groupby(['intersection_id', 'tollgate_id'])['travel_time'].mean().reset_index(name="avg_travel_time")
        np_arr = df_temp['avg_travel_time'].tolist()
        mylist_Y.append(np_arr)

    #Concatenate the X vector (np array) from the list of numpy arrays
    X = np.concatenate(mylist_X)

    #Concatenate the Y vector (np array) from the list of numpy arrays
    Y = np.concatenate(mylist_Y)

    # delete first 2h of Y -> no data is available, 6 routes for 2h
    Y = Y[36:]
    # delete last 2h of X -> no prediction is available, 6 time windows * 26 values = 156
    X = X[:-156]
    return X, Y