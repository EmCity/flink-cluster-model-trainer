import pandas as pd
import generate_vectors_time_link_weather as weather
import numpy as np
import Paths as path


def generate_vector():

    #use als input later
    trajectories_df = pd.read_csv(path.trajectories_testing_file)
    df_orig = trajectories_df

    #Generate X
    df = weather.prepare_df_travelseq()
    df['starting_time'] = df['starting_time'].astype('datetime64[ns]')
    df_group = df.groupby([pd.Grouper(key='starting_time', freq='20min')])
    df['link_travel_time'] = pd.to_numeric(df['link_travel_time'])

    mylist_X = []
    for name, group in df_group:
        df_temp = group.groupby(['link'])['link_travel_time'].mean().reset_index(name="avg_travel_time")
        np_arr = df_temp.as_matrix(columns=['avg_travel_time'])
        mylist_X.append(np_arr)
    X = np.array(mylist_X)

    #Generate Y
    df_orig['starting_time'] = df_orig['starting_time'].astype('datetime64[ns]')
    df_orig_group = df_orig.groupby([pd.Grouper(key='starting_time', freq='20min')])
    mylist_Y = []
    for name, group in df_orig_group:
        df_temp = group.groupby(['intersection_id', 'tollgate_id'])['travel_time'].mean().reset_index(name="avg_travel_time")
        np_arr = df_temp.as_matrix(columns=['avg_travel_time'])
        mylist_Y.append(np_arr)
    Y = np.array(mylist_Y)
    return X, Y

generate_vector()