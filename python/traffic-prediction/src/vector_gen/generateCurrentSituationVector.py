import pandas as pd
import numpy as np
from vector_gen import generate_VectorY as vec_1
from misc import paths as path
import datetime


def generate_vector(df):
    return generate_x(df), vec_1.generate_VectorY_df(df)


def generate_x(df):
    return generate_x_df(df).tolist();


def generate_x_df(df):
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

    df = prepare_df_travelseq(df)
    df['link_starting_time'] = pd.to_datetime(df['link_starting_time'])
    df['tw'] = df['link_starting_time'].apply(lambda x: add_tw(x))
    date_start = df['link_starting_time'].min()
    date_end = df['link_starting_time'].max()
    date_end = pd.to_datetime(date_end) + datetime.timedelta(days=1)
    daterange = pd.date_range(start=date_start, end=date_end, normalize=True, closed='left', freq='20min')
    df['link_travel_time'] = pd.to_numeric(df['link_travel_time'])
    df2 = df.groupby(['tw', 'link'])['link_travel_time'].mean().reset_index(name='link_avg')
    df2 = df2.set_index(['tw', 'link'])

    # links (24)
    links = list(range(100, 124))
    links = np.array(links).astype('str')  # as string
    # gen tuples with tw
    tuples = []
    for tw in daterange:
        for link in links:
            tuples.append((tw, link))

    # multi_index
    multi_index = pd.MultiIndex.from_tuples(tuples, names=['tw', 'link'])
    # set multi_index
    df3 = pd.DataFrame(data=df2, index=multi_index, columns=['link_avg'])
    # remove first 2h -> 6*23 values
    df3 = df3[:-6 * 23]
    return df3['link_avg']


def prepare_df_travelseq(df):
    '''
    splits the travel_seq

    Returns: a df with ['trajectorie', 'itersection_id', 'tollgate_id', 'vehicle_id',
       'starting_time', 'travel_seq', 'travel_time', 'link',
       'link_starting_time', 'link_travel_time'] as coloumns

    @author: Christian

    '''

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

    res_columns = ['trajectorie', 'intersection_id', 'tollgate_id', 'vehicle_id', 'starting_time', 'travel_seq',
                   'travel_time']
    res_columns.extend(['link', 'link_starting_time', 'link_travel_time'])

    link_df = pd.DataFrame(mylist, columns=res_columns)
    return link_df

x,y = generate_vector(pd.read_csv(path.trajectories_training_file))
# days*hours*window/h*values - 2h
number_Y = 7*24*3*6 - 1*2*3*6
print(y)
print (len(y))
print(number_Y)

# days*hours*window/h*values -2h
number_X = 7*24*3*23 - 1*2*3*23
print (x)
print (len(x))
print(number_X)