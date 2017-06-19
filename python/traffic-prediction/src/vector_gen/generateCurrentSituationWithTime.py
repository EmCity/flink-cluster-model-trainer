import src.vector_gen.generateCurrentSituationVector as gcsv


import numpy as np
import pandas as pd

def generate_vector(df):
	
	df_cs = gcsv.generate_x_df(df)
	df = df_cs.copy()
	df['datetime'] = pd.to_datetime(df_cs.index.values)
	df['weekday'] = df['datetime'].dt.dayofweek
	df['hour'] = df['datetime'].dt.hour
	df['minute'] = df['datetime'].dt.minute
	df = df.drop('datetime',axis=1)
	return df
