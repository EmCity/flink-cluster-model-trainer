import vector_gen.generateCurrentSituationVector as vec
import vector_gen.generateTimeInformationVector as vec2
import vector_gen.generate_VectorY as vecY

import numpy as np
import pandas as pd
from misc import paths as path
def generate_vector(df):
    x = vec.generate_x_df(df)
    x_2 = vec2.generate_timeInformationVector(df)
    print(x)
    print("hhhhhhhhhhhhh")
    print(x_2)
    print(type(x_2))
    #x_3 =  pd.concat([x, x_2], axis=1)
    #print(x_3)

    return x

df = pd.read_csv(path.trajectories_training_file2)
x = generate_vector(df)
#print(x.to_string)