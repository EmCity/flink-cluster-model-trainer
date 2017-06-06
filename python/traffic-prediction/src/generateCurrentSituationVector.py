import pandas as pd
import generate_vectors_time_link_weather as weather
import numpy as np


def generate_vector():
    #Generate X
    df = weather.prepare_df_travelseq()
    df['starting_time'] = df['starting_time'].astype('datetime64[ns]')
    mylist = []
    df_group = df.groupby([pd.Grouper(key='starting_time', freq='20min')])
    for name, group in df_group:
        group['link_travel_time'] = pd.to_numeric(group['link_travel_time'])
        df_temp = group.groupby(['link'])['link_travel_time'].mean().reset_index(name="avg_travel_time")
        np_arr = df_temp.as_matrix(columns=['avg_travel_time'])
        mylist.append(np_arr)
    X = np.array(mylist)

    #Generate Y
    Y = np.array([])
    return X, Y

generate_vector()