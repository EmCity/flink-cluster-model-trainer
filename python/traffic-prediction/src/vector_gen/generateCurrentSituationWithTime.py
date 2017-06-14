import vector_gen.generateCurrentSituationVector as vec
import vector_gen.generateTimeInformationVector as vec2
import vector_gen.generate_VectorY as vecY

import numpy as np
import pandas as pd
from misc import paths as path
def generate_vector(df):
    x = vec.generate_x(df)
    x_2, _ = vec2.generate_timeInformationVector(df)
    list3 = []
    while len(x) != 0 or len(x_2) != 0:
        list3.extend(x_2[:3])
        x_2 = x_2[3:]
        list3.extend(x[:24])
        x = x[24:]
    print (x)
    print (x_2)
    return np.array(list3), vecY.generate_VectorY_df(df)

#df = pd.read_csv(path.trajectories_training_file2)
#x, y = generate_vector(df)
