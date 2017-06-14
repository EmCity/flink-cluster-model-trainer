<<<<<<< HEAD
import numpy as np
import pandas as pd
import misc.Paths as path

def generate_vector(df):
    df['starting_time'] = df['starting_time'].astype('datetime64[ns]')
    x = generate_x(prepare_df_travelseq(df))
    y = generate_y(df)
    return x, y


def generate_x(df):
    # Get a 20 min sliding window for the dataframe
    df_group = df.groupby([pd.Grouper(key='starting_time', freq='20min')])
    df['link_travel_time'] = pd.to_numeric(df['link_travel_time'])
    x = []
    # Iterate over a sliding window dataframe
    for name, group in df_group:
        # Get the averages travel time per link
        df_temp = group.groupby(['link'])['link_travel_time'].mean().reset_index(name="avg_travel_time")
        x_temp = calculate_list(df_temp)
        # Add the averages per link to the List
        x.append(x_temp)
    # Concatenate the X vector (np array) from the list of numpy arrays
    np_x = np.concatenate(x)
    # delete last 2h of X -> no prediction is available, 6 time windows * 23 values = 138
    return np_x[:-138]


def generate_y(df):
    # Get 20 min sliding windows for the data frame
    df_orig_group = df.groupby([pd.Grouper(key='starting_time', freq='20min')])
    y = []
    # Iterate over a sliding window data frame
    for name, group in df_orig_group:
        # Get the averages travel time route
        df_temp = group.groupby(['intersection_id', 'tollgate_id'])['travel_time'].mean().reset_index(
            name="avg_travel_time")
        y_temp = df_temp['avg_travel_time'].tolist()
        y.append(y_temp)
    # Concatenate the Y vector (np array) from the list of numpy arrays
    np_y = np.concatenate(y)
    # delete first 2h of Y -> no data is available, 6 routes for 2h
    return np_y[36:]


def prepare_df_travelseq(df):

    df_seq = df.travel_seq.str.split(';', expand=True)
    df = df.join(df_seq)
    mylist = []
    for index, row in df.iterrows():
        new_row = [index]
        new_row.extend(row[:6])
        for ele in row[7:]:
            if ele is not None:
                row_tmp = ele.split('#')
                res_row = list(new_row)
                res_row.extend(row_tmp)
                mylist.append(res_row)
    res_columns = ['trajectorie', 'itersection_id', 'tollgate_id', 'vehicle_id', 'starting_time', 'travel_seq',
                   'travel_time']
    res_columns.extend(['link', 'link_starting_time', 'link_travel_time'])
    link_df = pd.DataFrame(mylist, columns=res_columns)
    return link_df


def calculate_list(df_temp):
    vec = [None] * 23
    pd.to_numeric(df_temp['link'])
    df_temp['link'] = df_temp['link'].astype(int)
    df_temp['link'] = df_temp['link'] - 100
    dict_link_avg = pd.Series(df_temp.avg_travel_time.values, index=df_temp.link).to_dict()
    for key, value in dict_link_avg.items():
        vec[key-1] = value
    return vec

X,Y = generate_vector(pd.DataFrame.from_csv(path.trajectories_training_file))
=======
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
    df = df.groupby(['tw', 'link'])['link_travel_time'].mean().reset_index(name='link_avg')
    df = df.set_index(['tw', 'link'])

    # links (24)
    links = np.array(list(range(100, 124))).astype('str')  # as string

    # multi_index
    multi_index = pd.MultiIndex.from_product([daterange, links], names=['tw', 'link'])
    # set multi_index
    df = pd.DataFrame(data=df, index=multi_index, columns=['link_avg'])
    # remove first 2h -> 6*23 values
    df = df[:-6 * 24]
    return df['link_avg']


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

>>>>>>> ca50fe602aea3be8e6018cc6f214e9f0f79154b6
