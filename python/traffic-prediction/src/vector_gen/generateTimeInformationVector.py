import pandas as pd
import src.vector_gen.createTW as ctw
from src.misc import paths


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
	return df3[['weekday', 'hour', 'minute']][:-1]


