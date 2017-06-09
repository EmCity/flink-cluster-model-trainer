"""
Created on June May 03 01:10:00 2017

@author: Christian

If the wind_speed is lower or equal to 0.2 then the wind_direction has the value of 999017.0.
This is a error in the data. Actually there is no wind_direction without wind_speed.
Actually it is NaN. But does this help?

"""
import numpy as np
import pandas as pd

from misc import Paths as path


def prepare_df_travelseq():
    '''
    splits the travel_seq

    Returns: a df with ['trajectorie', 'itersection_id', 'tollgate_id', 'vehicle_id',
       'starting_time', 'travel_seq', 'travel_time', 'link',
       'link_starting_time', 'link_travel_time'] as coloumns

    @author: Christian

    '''
    trajectories_df = pd.read_csv(path.trajectories_testing_file)
    df = trajectories_df


    df_seq = df.travel_seq.str.split(';', expand=True)
    df = df.join(df_seq)

    # iterate... the slow way... :-/
    mylist = []
    for index, row in df.iterrows():
        new_row = [index]
        new_row.extend(row[:6])
        # print(new_row)
        for ele in row[6:]:
            if ele is not None:
                row_tmp = ele.split('#')
                res_row = list(new_row)
                res_row.extend(row_tmp)
                # print(res_row)
                mylist.append(res_row)

    res_columns = ['trajectorie', 'itersection_id', 'tollgate_id', 'vehicle_id', 'starting_time', 'travel_seq',
                   'travel_time']
    res_columns.extend(['link', 'link_starting_time', 'link_travel_time'])

    link_df = pd.DataFrame(mylist, columns=res_columns)
    return link_df

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


# test print 10 rows
print(prepare_df_travelseq()[:20])