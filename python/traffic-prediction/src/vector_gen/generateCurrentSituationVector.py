import numpy as np
import pandas as pd
from vector_gen import generateWeatherVectors as vec


def generate_vector(df):
    return generate_x(df), generate_y(df)


def generate_x(df):
    vec.prepare_df_travelseq(df)
    df['starting_time'] = df['starting_time'].astype('datetime64[ns]')
    # Get a 20 min sliding window for the dataframe
    df_group = df.groupby([pd.Grouper(key='starting_time', freq='20min')])
    df['link_travel_time'] = pd.to_numeric(df['link_travel_time'])
    x = []
    # Iterate over a sliding window dataframe
    for name, group in df_group:
        # Get the averages travel time per link
        df_temp = group.groupby(['link'])['link_travel_time'].mean().reset_index(name="avg_travel_time")
        x_temp = calculate_list(df_temp)
        # Add the averages per link to the List
        x.append(x_temp)
    # Concatenate the X vector (np array) from the list of numpy arrays
    np_x = np.concatenate(x)
    # delete last 2h of X -> no prediction is available, 6 time windows * 23 values = 138
    return np_x[:-138]


def generate_y(df):
    # Get 20 min sliding windows for the data frame
    df['starting_time'] = df['starting_time'].astype('datetime64[ns]')
    df_orig_group = df.groupby([pd.Grouper(key='starting_time', freq='20min')])
    y = []
    # Iterate over a sliding window data frame
    for name, group in df_orig_group:
        # Get the averages travel time route
        df_temp = group.groupby(['intersection_id', 'tollgate_id'])['travel_time'].mean().reset_index(
            name="avg_travel_time")
        y_temp = df_temp['avg_travel_time'].tolist()
        y.append(y_temp)
    # Concatenate the Y vector (np array) from the list of numpy arrays
    np_y = np.concatenate(y)
    # delete first 2h of Y -> no data is available, 6 routes for 2h
    return np_y[36:]

def calculate_list(df_temp):
    vec = [None] * 23
    pd.to_numeric(df_temp['link'])
    df_temp['link'] = df_temp['link'].astype(int)
    df_temp['link'] = df_temp['link'] - 100
    dict_link_avg = pd.Series(df_temp.avg_travel_time.values, index=df_temp.link).to_dict()
    for key, value in dict_link_avg.items():
        vec[key-1] = value
    return vec
