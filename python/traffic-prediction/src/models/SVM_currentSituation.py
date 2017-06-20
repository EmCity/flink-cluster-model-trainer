from sklearn import svm, model_selection
import src.vector_gen.generateCurrentSituationVector as vec
import misc.split_train_valid as split
import misc.paths as path
import pandas as pd
import numpy
numpy.set_printoptions(threshold=numpy.nan)


df = pd.read_csv(path.trajectories_training_file2)
#print(df)
#X,Y = vec.generate_vector(df)
#print(X,Y)
#X_train, X_test, Y_train, Y_test = model_selection.train_test_split(X,Y,test_size=0.2)
training, validation, testing = split.split_dataset(df)
X_train,Y_train = vec.generate_vector(training)
# X_train = vec.generate_x_df(training)
# Y_train = vec.convertY(training)
X_test,Y_test = vec.generate_vector(testing)

print(X_train)
print("############")
print(Y_train)
clf = svm.SVC()
#X_train.reshape(2988,84)

clf.fit(X_train,Y_train)

accuracy = clf.score(X_test,Y_test)
print(accuracy)