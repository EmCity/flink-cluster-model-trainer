import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import random as rd
import math
"""
This function splits the data set into a train, validation and test data set
Parameters: df: The pandas dataframe
train: How much of df should be training data
validation: How much of data should be used for validation
"""

def split_dataset(df, train = 0.6, validation = 0.1):
	"""
	split_dataset first divides the incoming data frame in k buckets
	It then takes one bucket as test data, the second bucket as validation data
	The rest in training data
	Returns three data frames
	train and validation have to sum up to a maximum of 1.0
	e.g. split_dataset(df_example, 0.8, 0.1) will split the data with the distribution (0.8, 0.1, 0.1)
	"""
	print "The length of the original data frame is : " , len(df.index)
	#sorted_df = df.sort(['starting_time'], ascending=[1]) #sort data set by time stamps
	#print np.array_split(sorted_df, 10)
	#check if the parameters are in the right range
	if(train < 0.0 or train > 1.0):
		#print error message
		raise ValueError("train has to be in the range [0.0,1.0]")
	if(train + validation > 1.0):
		raise ValueError("train + validation cannot be larger than 1.0")
	#Split data set in k buckets
	if(validation == 0.0):
		test_start = int(rd.randint(0, (len(df.index) - len(df.index) * train))) #start of the training set
		test_end = int(test_start + (1 - train) * len(df.index)) #end of the training set
		test_set = df[test_start : test_end]
		#now select the rest of the data frame as your training data
		train_set = pd.concat([df[0 : test_start], df[test_end : len(df.index)]])
		valid_set = pd.DataFrame.empty
		return train_set, valid_set, test_set
	else: #This is if a validation data set exists
		k = int(round(1 / min(train, validation)))
		print "The data set is being split into " , k , "buckets"
		validation_idx = rd.randint(0, k-1)
		datasets_splitted = np.array_split(df, k)
		#n buckets for test set 
		n = int((1 - train - validation) * k)
		print("The number n of test buckets is " + str(n))
		valid_set = datasets_splitted[validation_idx]
		test_idx = rd.randint(0, k)
		test_end = test_idx + n - 1 #because the same index already consitutes an element in the set
		print "Bucket " , str(validation_idx) , "will be used as validation set"
		#print "The test end" , test_end
		while test_idx == validation_idx or test_idx >= (k - 1 - n) or (test_end >= validation_idx and test_idx <= validation_idx):
			test_idx = rd.randint(0, k-1) #find a new randomly generated index for the test set
			test_end = test_idx + n -1 #the last bucket of the test set
			#print(test_idx)
		print "The test_idx " , test_idx
		print "The test_end " , test_end
		#Check which type the dataset_splitted method has
		print "The dataset_splitted variable has the type " , type(datasets_splitted)
		test_frames = datasets_splitted[int(test_idx) : int(test_end) + 1]
		test_set = pd.concat(test_frames)
		print "Slicing data set from " , test_idx, " to ", test_end
		print "The type of validation set is " , type(valid_set)
		print "The length of the validation set is " , len(valid_set.index)
		print "The type of test set is ", type(test_set)
		print "The length of the test set is " , len(test_set.index)
		print "k is " , k
		bad_indices = range(0, k)
		good_indices = []
		print bad_indices
		for i in bad_indices:
			print i, type(i)
			if i != validation_idx and i!= test_idx and i!= test_end and not (i> test_idx and i < test_end):
				good_indices.append(i)
			
			
		print good_indices
		train_list = [datasets_splitted[i] for i in good_indices]
		train_set = pd.concat(train_list) 
		#print "The type of the train set is " , type(train_set)
		print "The length of the training set is ", len(train_set.index)
		#return "The comeplete amount of indices is " , train_set + valid_set + test_set
		return train_set, valid_set, test_set





	#this_rest_size = 1.0 - train
	#this_test_size = 1.0 - (validation / this_rest_size)
	#print(this_test_size)
	#print(this_train_size)
	#train, rest = train_test_split(df, test_size = this_rest_size) #split in test and rest
	#print(1.0 - train - validation)
	
	#if(this_test_size < 1.0):
	#	valid, test = train_test_split(rest, test_size = this_test_size) #split rest into validation & test set
	#else:
	#	valid = pd.DataFrame.empty
	#	test = rest #test set will be the whole of the rest after tking a away the training set
	
	#return train_set, valid_set, test_set

def common_vals(df1, df2, df3):
        #Helper method for checking if therer is overlap in the data frames
        print "Shapes of data frames : ", df1.shape, df2.shape, df3.shape
        overlap_df12 = pd.merge(df1, df2, on=['starting_time'], how='inner')
        overlap_df123 = pd.merge(overlap_df12, df3, on=['starting_time'], how='inner')
        print "Overlap of df1 and df2: ", overlap_df12
        print "Overlap of df1, df2 and df3: " , overlap_df123
        #print "This is the overlap of the data frames ", overlap_df12
        return overlap_df123
