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

    res = res.apply(lambda x: x.fillna(x.mean()),axis=0)

    return res
    


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
