import src.vector_gen.generateCurrentSituationVector as gcsv


def generate_x_df(df):

	df_cs = gcsv.generate_x_df(df)
	df = df_cs.copy()
	df['weekday'] = df_cs.index.dayofweek
	df['hour'] = df_cs.index.hour
	df['minute'] = df_cs.index.minute
	return df