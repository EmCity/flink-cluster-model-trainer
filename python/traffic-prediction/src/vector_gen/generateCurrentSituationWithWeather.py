import src.vector_gen.generateWeatherVectors as gwv
import pandas as pd
import src.misc.paths as path

def generate_x(trajectories_df, weather_df):
    x = gwv.generate_TimeInformationCurrentSituationWeatherVectors(trajectories_df, weather_df)

    #delete time information from dataframe
    x = x.drop(['weekday', 'hour', 'minute'], axis=1)
    return x

# test
# generate_x(pd.read_csv(path.trajectories_training_file2), pd.read_csv(path.weather_training_file2))

