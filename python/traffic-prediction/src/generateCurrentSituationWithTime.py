import pandas as pd
import numpy as np
import Paths as path
import generateCurrentSituationVector as vec

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
        print(len(list))

        #Add the averages per link to the List
        mylist_X.append(list)

    #Concatenate the X vector (np array) from the list of numpy arrays
    X = np.concatenate(mylist_X)

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

    #Delete the first 6 elements because we are not interested in the first 6 time windows (first 2 hours)
    #del mylist_Y[0:5]

    #Concatenate the Y vector (np array) from the list of numpy arrays
    Y = np.concatenate(mylist_Y)
    return X, Y

generate_vector(pd.read_csv(path.trajectories_training_file))