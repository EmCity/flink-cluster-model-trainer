from sklearn import svm, model_selection
import src.vector_gen.generateCurrentSituationVector as vecX
import src.vector_gen.generate_VectorY as vecY
import src.misc.split_train_valid as split
import src.misc.paths as path
import pandas as pd
import numpy
numpy.set_printoptions(threshold=numpy.nan)


df = pd.read_csv(path.trajectories_training_file2)
#print(df)
#X,Y = vec.generate_vector(df)
#print(X,Y)
#X_train, X_test, Y_train, Y_test = model_selection.train_test_split(X,Y,test_size=0.2)
training, validation, testing = split.split_dataset(df)
X_train = vecX.generate_x_df(training)
Y_train = vecY.generate_VectorY_df(training)
X_test = vecX.generate_x_df(testing)
Y_test = vecY.generate_VectorY_df(testing)

print(X_train)
print("############")
print(Y_train)
clf = svm.LinearSVC()
#X_train.reshape(2988,84)
print(X_train.shape)
print(Y_train.shape)

clf.fit(X_train,Y_train)

accuracy = clf.score(X_test,Y_test)
print(accuracy)