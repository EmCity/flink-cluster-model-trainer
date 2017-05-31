import unittest
import pandas as pd
import numpy as np
import split_train_valid as split

"""
Test method for split_train_valid.py
"""
class TestDatasetSplit(unittest.TestCase):

    #def setUp(self):
        #df1 = pd.DataFrame(np.random.randn(10, 5), columns=['a', 'b', 'c', 'd', 'e'])

    def test_normal_split(self):
        df1 = pd.DataFrame(np.random.randn(10, 5), columns=['a', 'b', 'c', 'd', 'e'])
        train_df, valid_df, test_df = split.split_dataset(df1, 0.6, 0.2)
        self.assertEquals(len(train_df.index), 6)
        self.assertEquals(len(valid_df.index), 2)
        self.assertEquals(len(test_df.index), 2)


    def test_no_validation_set(self):
        df1 = pd.DataFrame(np.random.randn(10, 5), columns=['a', 'b', 'c', 'd', 'e'])
        train_df, valid_df, test_df = split.split_dataset(df1, 0.6, 0.0)
        self.assertEquals(len(train_df.index), 6)
        self.assertEquals(valid_df, pd.DataFrame.empty)
        self.assertEquals(len(test_df.index), 4)


    def test_wrong_params(self):
        df1 = pd.DataFrame(np.random.randn(10, 5), columns=['a', 'b', 'c', 'd', 'e'])
        """
        Validation set has a parameter that is too big
        """
        self.assertRaises(ValueError, lambda: split.split_dataset(df1, 0.6, 0.6))

if __name__ == '__main__':
    unittest.main()