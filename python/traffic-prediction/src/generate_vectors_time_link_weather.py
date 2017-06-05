"""
Created on June May 03 01:10:00 2017

@author: Christian

If the wind_speed is lower or equal to 0.2 then the wind_direction has the value of 999017.0.
This is a error in the data. Actually there is no wind_direction without wind_speed.
Actually it is NaN. But does this help?

"""
import Paths as path
import pandas as pd
import numpy as np

from datetime import timedelta
from datetime import time
from datetime import date
from datetime import datetime


def generate_vectors_time_link_weather():
    """
    x = time information + travel time/link + weather information
    y = prediction travel time
    for each 20 minutes

    Returns:

    """
    x = None
    y = None
    weather_df = pd.read_csv(path.weather_training_file)
    # clean data: wind_direction
    weather_df['wind_direction2'] = np.where(weather_df['wind_speed'] <= 0.2, np.nan, weather_df['wind_speed'])
    # clean data: add a datetime column by combining date and hour
    weather_df['datetime'] = pd.to_datetime(weather_df['date']) + pd.to_timedelta(weather_df['hour'], unit='h')
    # call task 4


    # add / append weather data



    return (x, y)
