import pandas as pd
import datetime

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

    df, daterange = createTW(df)

    df3 = pd.DataFrame(index=daterange, columns=['weekday', 'hour', 'minute'])
    df3['datetime'] = pd.to_datetime(df3.index.values)
    df3['weekday'] = df3['datetime'].dt.dayofweek
    df3['hour'] = df3['datetime'].dt.hour
    df3['minute'] = df3['datetime'].dt.minute
    return df3[['weekday', 'hour', 'minute']]

def createTW(df):
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

    return df, daterange


