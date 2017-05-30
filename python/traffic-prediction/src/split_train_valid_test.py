import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

#This function splits the data set into a train, validation and test data set
#Parameters: df: The pandas dataframe
#train: How much of df should be training data;
#validation_share: How much of remaining data should be used for validation

def split_dataset(df, train = 0.6, validation_share = 0.5):
	train, rest = train_test_split(df, test_size = (1 - train)) #split in test and rest
	valid, test = train_test_split(rest, test_size = (1 - validation_share)) #split rest into validation & test set
	return train, valid, test

df3 = pd.DataFrame(np.random.randn(10, 5), columns=['a', 'b', 'c', 'd', 'e'])
print(df3)
train_df, valid_df, test_df = split_dataset(df3)
print("Here comes the train_df")
print(train_df)
print("Here comes the valid_df")
print(valid_df)
print("Her comes the test_df")
print(test_df)

