'''
test code for the model_factory.py
'''
from collections import OrderedDict
import unittest
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from pipeline import model_factory as fa
import pdb

ONE_DICT = {'LinearSVC': {'C': [0.1], 'penalty': ['l2']}}
MANY_DICT =  {'LinearSVC': {'C': [0.1, 1], 'penalty': ['l2']},
              'LogisticRegression': {'C': [0.1], 'penalty': ['l1','l2']}}

class TestModelFactory(unittest.TestCase):
    '''
    unit test for the modelFactory

    '''
    def test_one_model(self):
        temp = LinearSVC(C=0.1,penalty ='l2').get_params()
        model = next(fa.get_models(ONE_DICT)).get_params()
        self.assertEqual(temp, model, "models don't match")

    def test_many_models(self):
        expected = [LinearSVC(C=0.1, penalty = 'l2'),
                  LinearSVC(C=1 , penalty = 'l2'),
                  LogisticRegression(C = 0.1, penalty = 'l1'),
                  LogisticRegression(C = 0.1, penalty = 'l2')]
        models = fa.get_models(MANY_DICT)
        i = 0
        for model in models:
           self.assertEqual(expected[i].get_params(), model.get_params(), 'Number {} is not match'.format(i+1))
           i += 1

if __name__ == '__main__':
    unittest.main()
           
        
