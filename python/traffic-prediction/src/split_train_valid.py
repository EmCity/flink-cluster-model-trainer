import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

"""
This function splits the data set into a train, validation and test data set
Parameters: df: The pandas dataframe
train: How much of df should be training data
validation: How much of data should be used for validation
"""

def split_dataset(df, train = 0.6, validation = 0.1):
	"""
	split_dataset performs a random three-way split on the given split_dataset
	Returns three data frames
	train and validation have to sum up to a maximum of 1.0
	e.g. split_dataset(df_example, 0.8, 0.1) will split the data with the distribution (0.8, 0.1, 0.1)
	"""
	#check if the parameters are in the right range
	if(train < 0.0 or train > 1.0):
		#print error message
		raise ValueError("train has to be in the range [0.0,1.0]")
	if(train + validation > 1.0):
		raise ValueError("train + validation cannot be larger than 1.0")
	this_rest_size = 1.0 - train
	this_test_size = 1.0 - (validation / this_rest_size)
	#print(this_test_size)
	#print(this_train_size)
	train, rest = train_test_split(df, test_size = this_rest_size) #split in test and rest
	#print(1.0 - train - validation)
	if(this_test_size < 1.0):
		valid, test = train_test_split(rest, test_size = this_test_size) #split rest into validation & test set
	else:
		valid = pd.DataFrame.empty
		test = rest #test set will be the whole of the rest after tking a away the training set
	return train, valid, test

"""
df3 = pd.DataFrame(np.random.randn(10, 5), columns=['a', 'b', 'c', 'd', 'e'])
print(df3)
train_df, valid_df, test_df = split_dataset(df3)
print("Here comes the train_df")
print(train_df)
print("Here comes the valid_df")
print(valid_df)
print("Her comes the test_df")
print(test_df)
print(type(test_df))

#Try different parameters
print("Try different parameters for train and validation_share")
train_df, valid_df, test_df = split_dataset(df3, train = 0.8, validation=0.5)
print("Here comes the train_df")
print(train_df)
print("Here comes the valid_df")
print(valid_df)
print("Her comes the test_df")
print(test_df)
print(type(test_df))

"""
