import pandas as pd
import numpy as np
import Paths as path


def generate_vector(df_orig):
    #Generate X
    df = prepare_df_travelseq(df_orig)
    df['starting_time'] = df['starting_time'].astype('datetime64[ns]')
    df_group = df.groupby([pd.Grouper(key='starting_time', freq='20min')])
    df['link_travel_time'] = pd.to_numeric(df['link_travel_time'])

    mylist_X = []
    for name, group in df_group:
        df_temp = group.groupby(['link'])['link_travel_time'].mean().reset_index(name="avg_travel_time")
        np_arr = df_temp.as_matrix(columns=['avg_travel_time'])
        mylist_X.append(np_arr)
    X = np.array(mylist_X)

    #Generate Y
    df_orig['starting_time'] = df_orig['starting_time'].astype('datetime64[ns]')
    df_orig_group = df_orig.groupby([pd.Grouper(key='starting_time', freq='20min')])

    mylist_Y = []
    for name, group in df_orig_group:
        df_temp = group.groupby(['intersection_id', 'tollgate_id'])['travel_time'].mean().reset_index(name="avg_travel_time")
        np_arr = df_temp.as_matrix(columns=['avg_travel_time'])
        mylist_Y.append(np_arr)
    Y = np.array(mylist_Y)
    return X, Y


def prepare_df_travelseq(df):

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

generate_vector(pd.read_csv(path.trajectories_testing_file))