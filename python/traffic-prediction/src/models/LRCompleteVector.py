from sklearn import linear_model
import vector_gen.generateCurrentSituationWithTime as vec
import misc.split_train_valid as split
import misc.Paths as path
import pandas as pd

df = pd.DataFrame.from_csv(path.trajectories_training_file)
training, validation, testing = split.split_dataset(df, 0.8, 0.1)
X,Y = vec.generate_vector(training)
regression = linear_model.LinearRegression()
regression.fit(X,Y)
