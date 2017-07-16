import src.misc.split_train_valid_notRandom as split
import src.vector_gen.short_vec_gen.generateTimeInformationVector_short as gwv
import src.vector_gen.short_vec_gen.generate_VectorY_short as vecY
import pandas as pd

trajectories_df = pd.read_csv('../../../../../dataset/training/trajectories(table 5)_training.csv')
#weather_df = pd.read_csv('../../../../../dataset/training2/weather (table 7)_training_update.csv')
x = gwv.generate_timeInformation_df(trajectories_df)
y = vecY.generate_VectorY_df(trajectories_df)

split.split_dataset(df_X=x, df_Y=y, train=0.9, test=0.1, validation=0.0)