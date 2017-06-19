import vector_gen.generateCurrentSituationVector as vec
import vector_gen.generateTimeInformationVector as vec2
import vector_gen.generate_VectorY as vecY

import numpy as np
import pandas as pd
from misc import paths as path
def generate_vector(df):
    x = vec.generate_x_df(df)
    x_2 = vec2.generate_timeInformationVector(df)
    weekdays = x_2[0::3]
    hours = x_2[1::3]
    minutes = x_2[2::3]
    x['weekday'] = weekdays
    x['hours'] = hours
    x['minutes'] = minutes

    return x

df = pd.read_csv(path.trajectories_training_file2)
x = generate_vector(df)
print(x.to_string)