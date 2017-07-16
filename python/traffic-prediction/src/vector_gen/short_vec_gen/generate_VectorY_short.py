from decimal import *
import pandas as pd
import numpy as np
import datetime
import itertools

from src.vector_gen.createTW import createTW as create


def generate(y_list, df):
    date_start = df['starting_time'].min()
    date_end = df['starting_time'].max()
    # enddate is next day midnight #normalize=True sets it to midnight
    date_end = pd.to_datetime(date_end) + datetime.timedelta(days=1)
    daterange = pd.date_range(start=date_start, end=date_end, normalize=True, closed='left', freq='20min')

    routes = ['A2', 'A3', 'B1', 'B3', 'C1', 'C3']
    df_1 = pd.DataFrame(index=daterange, columns=routes, dtype='float64')
    i = 0
    while len(y_list) != 0:
        df_1.loc[daterange[i]] = np.array(y_list[:6])
        y_list = y_list[6:]
        i = i + 1
    return df_1


def generate_VectorY_df(trajectories_df):
    df = trajectories_df

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

    # add tw
    df['starting_time'] = pd.to_datetime(df['starting_time'])
    df['tw'] = df['starting_time'].apply(lambda x: add_tw(x))

    # get daterange
    date_start = df['starting_time'].min()
    date_end = df['starting_time'].max()
    # enddate is next day midnight #normalize=True sets it to midnight
    date_end = pd.to_datetime(date_end) + datetime.timedelta(days=1)
    daterange = pd.date_range(start=date_start, end=date_end, normalize=True, closed='left', freq='20min')

    # gen tw_avg
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

    df3[np.isnan(df3)] = 0

    # extract avg_travel_time column as list
    y_zero = df3['avg_travel_time'].tolist()

    df4 = df.groupby(['intersection_id', 'tollgate_id'])['travel_time'].mean().reset_index(name="avg_travel_time")
    route_avg = df4['avg_travel_time'].tolist()

    # compute all avarages for every 20 minutes among all days
    # 3 groups a 20 min x 24 h x 6 routes = 432 averages a 20 min per day
    avg_20min = []
    for index in range(0,432):
        average = np.mean(y_zero[index::432])
        if average == 0:
            avg_20min.append(route_avg[index % 6])
        else:
            avg_20min.append(average)

    # create sublists for each day
    y_zero = [y_zero[i:i+432] for i in range(0,len(y_zero),432)]

    # fill in NaN's with avg_20min
    for list in y_zero:
        for index, item in enumerate(list):
            if item == 0:
                list[index] = avg_20min[index]
    y = np.concatenate(y_zero)

    # round by 2 digits
    roundedList = [float(Decimal("%.2f" % e)) for e in y]

    y = generate(roundedList, df)
    df3[np.isnan(df3)] = 0
    print(len(y))
    return y
