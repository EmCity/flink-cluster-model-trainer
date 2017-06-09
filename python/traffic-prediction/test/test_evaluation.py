import unittest

import numpy as np

from misc import evaluation as evaluation


class TestEvaluation(unittest.TestCase):

    def test_get_simple_result(self):
        y_true = np.array([1, 2, 3, 4])
        y_pred = np.array([-1, -2, -3, -4])
        self.assertEqual(evaluation.mape(y_true, y_pred), 2)

    def self_test(self):
        y_true = np.array([1, 2, 3, 4])
        self.assertEqual(evaluation.mape(y_true, y_true), 0.0)
        
if __name__ == '__main__':
    unittest.main()