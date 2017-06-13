import numpy as np
import pandas as pd
from vector_gen import generateWeatherVectors as vec
from misc import paths as path
import datetime

def generate_vector(df):
    return generate_x(df), generate_y(df)


def generate_x(df):
    df = vec.prepare_df_travelseq(df)
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
    df['starting_time'] = pd.to_datetime(df['starting_time'])
    df['tw'] = df['starting_time'].apply(lambda x: add_tw(x))
    date_start = df['starting_time'].min()
    date_end = df['starting_time'].max()
    date_end = pd.to_datetime(date_end) + datetime.timedelta(days=1)
    daterange = pd.date_range(start=date_start, end=date_end, normalize=True, closed='left', freq='20min')
    df2 = df.groupby(['tw', 'intersection_id', 'tollgate_id'])['travel_time'].mean().reset_index(name="avg_travel_time")
    df2 = df2.set_index(['tw', 'intersection_id', 'tollgate_id'])

    # route_tuples
    route_touples = [('A', 2), ('A', 3), ('B', 1), ('B', 3), ('C', 1), ('C', 3)]
    # gen tuples with tw
    tuples = []

    for tw in daterange:
        for r in route_touples:
            tuples.append((tw, r[0], r[1]))

    # multi_index
    multi_index = pd.MultiIndex.from_tuples(tuples, names=['tw', 'intersection_id', 'tollgate_id'])
    # set multi_index
    df3 = pd.DataFrame(df2, index=multi_index, columns=['avg_travel_time'])
    # remove first 2h -> 12*3 rows
    df3 = df3[12 * 3:]
    return df3['avg_travel_time'].tolist()


def calculate_list(df_temp):
    vec = [None] * 23
    pd.to_numeric(df_temp['link'])
    df_temp['link'] = df_temp['link'].astype(int)
    df_temp['link'] = df_temp['link'] - 100
    dict_link_avg = pd.Series(df_temp.avg_travel_time.values, index=df_temp.link).to_dict()
    for key, value in dict_link_avg.items():
        vec[key-1] = value
    return vec

def add_tw(x):
    minute = x.minute
    tw_minute = -1
    if minute < 20:
        tw_minute = 0
    elif minute < 40:
        tw_minute = 20
    elif minute <= 60:
        tw_minute = 40
    return x.replace(minute=tw_minute, second=0)

x,y = generate_vector(pd.read_csv(path.trajectories_testing_file))
print (y)
