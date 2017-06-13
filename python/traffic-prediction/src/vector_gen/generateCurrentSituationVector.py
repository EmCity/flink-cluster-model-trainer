import numpy as np
import pandas as pd
from vector_gen import generateWeatherVectors as vec
from misc import paths as path
import datetime

def generate_vector(df):
    return generate_x(df), generate_y(df)


def generate_x(df):
    df = vec.prepare_df_travelseq(df)
    df['starting_time'] = pd.to_datetime(df['starting_time'])
    df['tw'] = df['starting_time'].apply(lambda x: add_tw(x))
    date_start = df['starting_time'].min()
    date_end = df['starting_time'].max()
    date_end = pd.to_datetime(date_end) + datetime.timedelta(days=1)
    daterange = pd.date_range(start=date_start, end=date_end, normalize=True, closed='left', freq='20min')
    df['link_travel_time'] = pd.to_numeric(df['link_travel_time'])
    df2 = df.groupby(['tw', 'link'])['link_travel_time'].mean().reset_index(name='link_avg')
    df2 = df2.set_index(['tw', 'link'])

    # gen tuples with tw
    tuples = []
    for tw in daterange:
            for i in range(100, 124):
                tuples.append((tw, i))

    # multi_index
    multi_index = pd.MultiIndex.from_tuples(tuples, names=['tw', 'link'])
    # set multi_index
    df3 = pd.DataFrame(data=df2, index=multi_index, columns=['link_avg'])
    # remove first 2h -> 6*26 values
    df3 = df3[:6*26]
    return  df3['link_avg'].tolist()


def generate_y(df):
    df['starting_time'] = pd.to_datetime(df['starting_time'])
    df['tw'] = df['starting_time'].apply(lambda x: add_tw(x))
    date_start = df['starting_time'].min()
    date_end = df['starting_time'].max()
    date_end = pd.to_datetime(date_end) + datetime.timedelta(days=1)
    daterange = pd.date_range(start=date_start, end=date_end, normalize=True, closed='left', freq='20min')
    df2 = df.groupby(['tw', 'intersection_id', 'tollgate_id'])['travel_time'].mean().reset_index(name="avg_travel_time")
    df2 = df2.set_index(['tw', 'intersection_id', 'tollgate_id'])
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

x,y = generate_vector(pd.read_csv(path.trajectories_training_file2))
# 91 days of training data, 24hours per day, 3 tw per hour, 6 routes per tw, 1 value (avg_travel_time)
number_Y = 7*24*3*6
# - 2h
number_Y -= 2*3*6
print (len(y))
print(number_Y)

number_X = 91*24*3*26
# - 2h
number_X -= 2*3*26
print (x)
print (len(x))
print(number_X)