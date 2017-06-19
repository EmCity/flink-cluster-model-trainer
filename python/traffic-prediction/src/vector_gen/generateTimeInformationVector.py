"""
The generate_timeInformationVector() function generates two numpy arrays:
        1. x array
                contains information about the weekday, the hour and the minutes
                example: [1 2 0 1 4 20] means [Tuesday 2:00am Tuesday 4:20am]
"""
import datetime
import numpy as np
import pandas as pd
import src.vector_gen.createTW as ctw


def generate_timeInformation_df(df):
	'''
	idx weekday hour minute
	2016-07-19 00:00:00	1	0	0
	2016-07-19 02:00:00	1	2	0
	2016-07-19 04:00:00	1	4	0
	2016-07-19 06:00:00	1	6	0
	2016-07-19 08:00:00	1	8	0
	2016-07-19 10:00:00	1	10	0
	2016-07-19 12:00:00	1	12	0
	2016-07-19 14:00:00	1	14	0

	'''
	
	df, daterange = ctw.createTW(df)

	df3 = pd.DataFrame(index=daterange, columns=['weekday', 'hour', 'minute'])
	df3['datetime'] = pd.to_datetime(df3.index.values)
	df3['weekday'] = df3['datetime'].dt.dayofweek
	df3['hour'] = df3['datetime'].dt.hour
	df3['minute'] = df3['datetime'].dt.minute
	return df3[['weekday', 'hour', 'minute']]

def generate_timeInformationVector(df):
    df['starting_time'] = df['starting_time'].astype('datetime64[ns]')
    #Get a 20 min sliding window for the dataframe
    df_group = df.groupby([pd.Grouper(key='starting_time', freq='2h')])

    #Generate X
    X = []
    for name, group in df_group:
        list = [name.weekday(), name.hour, name.minute]
        X.append(list)

    #build X array
    X = np.array(X)
    #build  X
    X = np.concatenate(X)
    #delete last 2h of X -> no prediction is available 3 values
    X = X[:-3]
    return X

