#intersection_id, tollgate_id, vehicle_id, starting_time, travel_seq
import pandas as pd
import Paths as path
#
def generateVector(df):
    df = df.travel_seq.str.split(';',)
    #print (df)

    #pd.to_datetime(df['starting_time'], format='%Y%m%d%H%M%S')
    #df['starting_time'] = pd.to_datetime(df['starting_time'])
    #df_1 = df.groupby([pd.Grouper(key='starting_time', freq='30min')])
    #print (df_1)

df = pd.DataFrame.from_csv("../../../dataset/training2/trajectories(table_5)_training2.csv")
generateVector(df)