import pandas as pd
import datetime
from src.vector_gen import generate_VectorY as vecY
from src.vector_gen import generateTimeInformationVector as vecX
from src.misc import paths
import csv
import os, glob

def split_dataset(df_X, df_Y, train = 0.6, validation = 0.1, test = 0.3):
    if(train < 0.0 or validation < 0.0 or test < 0.0 or train > 1.0 or validation > 1.0 or test > 1.0):
        #print error message
        raise ValueError("Train, validation and test parameters have to be in the range [0.0,1.0]")
    if(train+validation+test != 1):
        #print error message
        raise ValueError("Train, validation and test parameters have to sum up to 1")

    min_date = min(df_Y.index).date()
    max_date = max(df_Y.index).date()

    delta = max_date - min_date

    if validation == 0.0:
        train_start = min_date
        train_end = train_start + datetime.timedelta(days=int(round((delta.days + 1) * train)) - 1)

        test_start = train_end + datetime.timedelta(days=1)
        test_end = test_start + datetime.timedelta(days=int(round((delta.days + 1) * test)) - 1)

        train_X = df_X.loc[train_start : train_end][:-1]
        train_Y = df_Y.loc[train_start : train_end][1:]

        test_X = df_X.loc[test_start : test_end][:-1]
        test_Y = df_Y.loc[test_start : test_end][1:]

        files = [file for file in glob.glob("../../../../python/traffic-prediction/src/misc/splitting_csv_files/*.csv") if not file.startswith("valid")]
        for file in files:
            os.remove(file)

        train_X.to_csv(path_or_buf= "../../../../python/traffic-prediction/src/misc/splitting_csv_files/train_X.csv")
        train_Y.to_csv(path_or_buf= "../../../../python/traffic-prediction/src/misc/splitting_csv_files/train_Y.csv")
        test_X.to_csv(path_or_buf= "../../../../python/traffic-prediction/src/misc/splitting_csv_files/test_X.csv")
        test_Y.to_csv(path_or_buf= "../../../../python/traffic-prediction/src/misc/splitting_csv_files/test_Y.csv")


    else:
        train_start = min_date
        train_end = train_start + datetime.timedelta(days=int(round((delta.days + 1) * train)))

        valid_start = train_end
        valid_end = valid_start + datetime.timedelta(days=int(round((delta.days + 1) * validation)))

        test_start = valid_end
        test_end = test_start + datetime.timedelta(days=int(round((delta.days + 1) * test)))

        train_X = df_X.loc[train_start : train_end][:-1]
        train_Y = df_Y.loc[train_start : train_end][1:]

        validation_X = df_X.loc[valid_start : valid_end][:-1]
        validation_Y = df_Y.loc[valid_start : valid_end][1:]

        test_X = df_X.loc[test_start : test_end][:-1]
        test_Y = df_Y.loc[test_start : test_end][1:]

        train_X.to_csv(path_or_buf= "../../../../python/traffic-prediction/src/misc/splitting_csv_files/train_X.csv")
        train_Y.to_csv(path_or_buf= "../../../../python/traffic-prediction/src/misc/splitting_csv_files/train_Y.csv")
        validation_X.to_csv(path_or_buf= "../../../../python/traffic-prediction/src/misc/splitting_csv_files/valid_X.csv")
        validation_Y.to_csv(path_or_buf= "../../../../python/traffic-prediction/src/misc/splitting_csv_files/valid_Y.csv")
        test_X.to_csv(path_or_buf= "../../../../python/traffic-prediction/src/misc/splitting_csv_files/test_X.csv")
        test_Y.to_csv(path_or_buf= "../../../../python/traffic-prediction/src/misc/splitting_csv_files/test_Y.csv")



# test
# df_trajectories = pd.read_csv(paths.trajectories_training_file)
# Y = vecY.generate_VectorY_df(df_trajectories)
# X = vecX.generate_timeInformation_df(df_trajectories)
# split_dataset(df_X=X, df_Y=Y, train=0.6, test=0.4, validation=0.0)
