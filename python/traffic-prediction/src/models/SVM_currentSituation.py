from sklearn import neighbors, model_selection
import vector_gen.generateCurrentSituationVector as vec
#import misc.split_train_valid as split
import misc.paths as path
import pandas as pd


df = pd.DataFrame.from_csv(path.trajectories_training_file)
print(df)
#X,Y = vec.generate_vector(df)
#print(X,Y)
#X_train, X_test, Y_train, Y_test = model_selection.train_test_split(X,Y,test_size=0.2)
#training, validation, testing = split.split_dataset(df, 0.8, 0.1)
# X_train,Y_train = vec.generate_vector(training)
# X_test,Y_test = vec.generate_vector(testing)

# clf = neighbors.KNeighborsClassifier()
# clf.fit(X_train,Y_train)
#
# accuracy = clf.score(X_test,Y_test)
# print(accuracy)