from sklearn import linear_model
import vector_gen.generateCurrentSituationWithTime as vec
import misc.split_train_valid as split
import misc.Paths as path
import pandas as pd

df = pd.DataFrame.from_csv(path.trajectories_training_file, index_col=[0, 1, 2])
training, validation, testing = split.split_dataset(df, 0.8, 0.1)
X,Y = vec.generate_vector(training)
regression2 = linear_model.LinearRegression()
regression2.fit(X,Y)
