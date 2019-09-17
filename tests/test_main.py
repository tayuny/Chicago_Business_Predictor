'''
test code for main function
'''
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from collections import OrderedDict
import unittest
import pandas as pd
import main
import pdb

CONFIG_FILE = './acs_geo_basic.yml'

class TestMain(unittest.TestCase):
    '''
    test the main function using the basic models
    '''
    def test_(self):
        
        main.run(CONFIG_FILE)
        
if __name__ == '__main__':
    unittest.main()
           
        
