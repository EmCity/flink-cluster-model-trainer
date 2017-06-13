import src.vector_gen.generateCurrentSituationVector as vec
import src.vector_gen.generateTimeInformationVector as vec2
import numpy as np
import pandas as pd
from misc import paths as path


def generate_vector(df):
    x = vec.generate_x(vec.prepare_df_travelseq(df))
    x_2, y = vec2.generate_timeInformationVector(df)
    list3 = []
    while len(x) != 0 or len(x_2) != 0:
        list3.extend(x_2[:3])
        x_2 = x_2[3:]
        list3.extend(x[:23])
        x = x[23:]
    return np.array(list3), y

