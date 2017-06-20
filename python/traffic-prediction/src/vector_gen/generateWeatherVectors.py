"""
Created on June May 03 01:10:00 2017


@author: Christian

If the wind_speed is lower or equal to 0.2 then the wind_direction has the value of 999017.0.
This is a error in the data. Actually there is no wind_direction without wind_speed.
Actually it is NaN. But does this help?

"""

import pandas as pd
import numpy as np
import datetime
import src.vector_gen.generate_VectorY as genY
import src.vector_gen.generateCurrentSituationVector as gcsv
import src.vector_gen.generateCurrentSituationWithTime as gcst


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


def generate_VectorY_df(trajectories_df):
    """
    TODO remove, use src.vector_gen.generate_VectorY

    with 6 time windows (20-min time windows in 2 hours)
    and 6 routes (A-2, A-3, B-1, B-3, C-1, C-3)
    m = 6 * 6

    Args:
        trajectories_df:
    Returns:

        df: [route1_avg_travel_time(time_window_1), routeB_avg_travel_time(time_window_1), ... , route6_avg_travel_time(time_window_6)]
    """

    df = trajectories_df

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
    # TODO fill NaN values

    # remove first 2h -> 12*3 rows
    df3 = df3[12 * 3:]
    # df3['avg_travel_time'].tolist()

    return df3


def prepare_weather_df(weather_df):
    # prepare weather_df
    # no_wind_dir_value = np.nan
    no_wind_dir_value = 0
    weather_df['wind_direction'] = np.where(weather_df['wind_speed'] <= 0.2, no_wind_dir_value,
                                            weather_df['wind_speed'])
    # weather_df[weather_df['wind_speed'] <= 0.3]

    weather_df['datetime'] = pd.to_datetime(weather_df['date']) + pd.to_timedelta(weather_df['hour'], unit='h')

    # make weather for each tw
    weather_df1 = weather_df.copy()
    delta = pd.Timedelta('1h')

    for i in range(3 * 1 - 1):
        cpy = weather_df.copy()
        cpy['datetime'] = weather_df['datetime'] + delta
        weather_df1 = weather_df1.append(cpy, ignore_index=True)
        delta = delta + pd.Timedelta('1h')

    weather_df1 = weather_df1.sort_values('datetime').set_index('datetime')
    return weather_df1


def generate_timeInformationVectorX_df(trajectories_df, add_datetime=False, remove_last_2h=True):
    """
    Args:

        trajectories_df:
        add_datetime:
        remove_last_2h:

    Returns:

        df: [dayofweek	hour	minute]
    """

    df = trajectories_df
    date_start = df['starting_time'].min()
    date_end = df['starting_time'].max()

    # enddate is next day midnight #normalize=True sets it to midnight
    date_end = pd.to_datetime(date_end) + datetime.timedelta(days=1)
    daterange = pd.date_range(start=date_start, end=date_end, normalize=True, closed='left', freq='20min')

    df = pd.DataFrame(daterange, columns=['datetime'])
    df['datetime'] = pd.to_datetime(df['datetime'])
    df['dayofweek'] = df['datetime'].dt.dayofweek
    df['hour'] = df['datetime'].dt.hour
    df['minute'] = df['datetime'].dt.minute

    if not add_datetime:
        df = df[['dayofweek', 'hour', 'minute']]

    # remove last 2h
    if remove_last_2h:
        df = df[:-6]

    return df


def generate_timeInformationVectors(trajectories_df):
    """
    Args:
        trajectories_df:

    Returns:
        X: [weekday, hour, minute]
        Y: [route1_avg_travel_time(time_window_1), routeB_avg_travel_time(time_window_1), ... , route6_avg_travel_time(time_window_6)]
    """

    df = trajectories_df
    X_df = generate_timeInformationVectorX_df(df)
    # Y_df = generate_VectorY_df(df)

    # to vector
    X = X_df[['dayofweek', 'hour', 'minute']].as_matrix().reshape(len(X_df) * 3)
    # Y = np.array(Y_df['avg_travel_time'].tolist())
    Y = genY.generate_VectorY_df(trajectories_df)

    return (X, Y)


def generate_timeInformationWeatherVectors(trajectories_df, weather_df):
    """

    Args:
        trajectories_df:
        weather_df:

    Returns:
        X: [weekday, hour, minute, pressure, sea_pressure, wind_direction, wind_speed, temperature, rel_humidity, precipitation, ...]
        Y: [route1_avg_travel_time(time_window_1), routeB_avg_travel_time(time_window_1), ... , route6_avg_travel_time(time_window_6)]

    """

    X_df = generate_timeInformationVectorX_df(trajectories_df, add_datetime=True)
    weather_df1 = prepare_weather_df(weather_df)

    # add weather
    weather_df1 = weather_df1.drop(['date', 'hour'], 1)
    weather_df2 = X_df.merge(weather_df1.reset_index(), how='left', on='datetime')
    weather_df2 = weather_df2.drop(['datetime'], 1)

    # to vector
    X = weather_df2.as_matrix()
    X = X.reshape(len(weather_df2) * len(weather_df2.columns))

    # Y_df = generate_VectorY_df(trajectories_df)
    # Y = np.array(Y_df['avg_travel_time'].tolist())
    Y = genY.generate_VectorY_df(trajectories_df)

    return (X, Y)


def generate_CurrentSituationWeatherVectors(trajectories_df, weather_df):
    """
    CurrentSituationWeather
    Args:
        trajectories_df:
        weather_df:

    Returns:
        X: 'link_avg_withoutNaN', 'pressure', 'sea_pressure', 'wind_direction', 'wind_speed', 'temperature',
                 'rel_humidity', 'precipitation' for each link on each timewindow
    """
    X_df = generate_CurrentSituationWeatherVectorX_df(trajectories_df, weather_df)
    X_df = X_df[['link_avg_withoutNaN', 'pressure', 'sea_pressure', 'wind_direction', 'wind_speed', 'temperature',
                 'rel_humidity', 'precipitation']]
    X = np.array(X_df)
    X = X.reshape((len(X_df.columns) * len(X_df), 1))

    # Y_df = generate_VectorY_df(trajectories_df)
    # Y = np.array(Y_df['avg_travel_time'].tolist())
    Y = genY.generate_VectorY_df(trajectories_df)

    return (X, Y)


def generate_CurrentSituationWeatherVectorX_df(trajectories_df, weather_df):
    x_df = gcsv.generate_x_df(trajectories_df)
    x_df = pd.DataFrame(x_df)

    w_df = prepare_weather_df(weather_df)
    w_df.index.names = ['tw']
    w_df = w_df.reset_index()

    x_df2 = x_df.reset_index()

    df = pd.merge(x_df2, w_df, how='left')
    df = df.set_index(['tw', 'link'])

    return df


def generate_TimeInformationCurrentSituationWeatherVectors(trajectories_df, weather_df):
    """
    TimeInformationCurrentSituationWeather

    Args:
        trajectories_df:
        weather_df:

    """
    df_data = trajectories_df
    df_weather2 = prepare_weather_df(weather_df)
    
    df2 = df_weather2[1::2]
    df2.index = df2.index - pd.Timedelta('1h')
    df2.index.names = ['tw']

    df = gcst.generate_vector(df_data)
    
    
    first_datetime = df.index.min()
    last_datetime = df.index.max()

    w_first_datetime = df2.index.min()
    w_last_datetime = df2.index.max()

    #print(first_datetime, last_datetime)
    #print(w_first_datetime, w_last_datetime)

    df2 = df2[df2.index >= first_datetime]
    df2 = df2[df2.index <= last_datetime]
    
    cols= ['pressure', 'sea_pressure', 'wind_direction', 'wind_speed', 'temperature', 'rel_humidity', 'precipitation']
    res = df
    res[cols] = df2[cols]
    return res
    


def generate_TimeInformationCurrentSituationWeatherVectorX_df(trajectories_df, weather_df):
    csw_df = generate_CurrentSituationWeatherVectorX_df(trajectories_df, weather_df)
    csw_df['datetime'] = csw_df.index.get_level_values('tw')
    csw_df['datetime'] = pd.to_datetime(csw_df['datetime'])
    csw_df['hour'] = csw_df['datetime'].dt.hour
    csw_df['minute'] = csw_df['datetime'].dt.minute
    csw_df['dayofweek'] = csw_df['datetime'].dt.dayofweek
    csw_df = csw_df[['dayofweek', 'hour', 'minute', 'link_avg_withoutNaN', 'pressure', 'sea_pressure', 'wind_direction',
                     'wind_speed', 'temperature', 'rel_humidity', 'precipitation']]

    return csw_df

# test

# from misc import paths as path

# trajectories_file = path.trajectories_training_file
# weather_file = path.weather_training_file

# import os
# print(os.getcwd())
# print(file)

# trajectories_df = pd.read_csv(trajectories_file)
# weather_df = pd.read_csv(weather_file)

# OK
# print('generate_timeInformationVectors')
# print(generate_timeInformationVectors(trajectories_df))

# OK
# print('generate_timeInformationWeatherVectors')
# print(generate_timeInformationWeatherVectors(trajectories_df, weather_df))

# print('generate_CurrentSituationWeatherVectors')
# print(generate_CurrentSituationWeatherVectors(trajectories_df, weather_df))


# print('generate_TimeInformationCurrentSituationWeatherVectors')
# print(generate_TimeInformationCurrentSituationWeatherVectors(trajectories_df.copy(), weather_df.copy()))
