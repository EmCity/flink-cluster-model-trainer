import numpy as np
import pandas as pd
from misc import paths as path
from vector_gen import generateWeatherVectors as vec


def generate_vector(df):
    return generate_x(df), vec.generate_y(df)


def generate_x(df):
    df = vec.prepare_df_travelseq(df)
    df['starting_time'] = df['starting_time'].astype('datetime64[ns]')
    # Get a 20 min sliding windows for the data frame
    df_group = df.groupby([pd.Grouper(key='starting_time', freq='20min')])
    df['link_travel_time'] = pd.to_numeric(df['link_travel_time'])
    x = []
    # Iterate over a sliding window data frame
    for name, group in df_group:
        # Get the averages travel time per link
        df_temp = group.groupby(['link'])['link_travel_time'].mean().reset_index(name="avg_travel_time")
        x_temp = [name.weekday(), name.hour, name.minute] + vec.calculate_list(df_temp)
        # Add the averages per link to the List
        x.append(x_temp)
    # Concatenate the X vector (np array) from the list of numpy arrays
    np_x = np.concatenate(x)
    # delete last 2h of X -> no prediction is available, 6 time windows * 26 values = 156
    return np_x[:-156]

generate_vector(pd.read_csv(path.trajectories_testing_file))

