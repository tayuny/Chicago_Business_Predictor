'''
transform  dataframe 
'''
from collections import OrderedDict
from itertools import product
import logging
import sys
import numpy as np
import argparse
import gc
from pipeline.get_dummy import *
from pipeline.community_mean_imputer import *
from pipeline.minmax_scaler import *


logger = logging.getLogger('start to transform the data')
ch = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.INFO)

def transform(config,X_train,X_test):
    '''
    perform all the tranform ops on the data   
    Input: 
        config: OrdedDict with the key as the name of op, value as params
    Return:
        dataframe
    '''
    logger.info('begin to transform')
    #pdb.set_trace()
    categorical_col = config['imputation']['cols']
    time_column = config['imputation']['time_col'][0]
    loc_column = config['imputation']['loc_col'][0]
    
    logger.info('start to imputation')
    imputer = community_mean_imputer()
    X_train, X_test = imputer.filled_categorical(X_train, X_test, categorical_col)
    X_train = imputer.train_regional_mean(X_train, loc_column, time_column)
    X_test = imputer.transform_test(X_test, loc_column, time_column) 

    dummies_cols  = config['dummy']['cols']
    k = config['dummy']['k'][0]

    # Drop year column
    X_train = X_train.drop(columns=[time_column])
    X_test = X_test.drop(columns=[time_column])
        
    #Scaling
    continuous_columns = list(set(X_train.columns) - set(categorical_col))
    logger.info('start to scaling')
    X_train, X_test = min_max_transformation(X_train, X_test, continuous_columns)
    
    logger.info('start to get dummies')
    #get dummies
    for col in dummies_cols:
        X_train, X_test = get_dummies(X_train, X_test, col, k)
    gc.collect()
    return X_train, X_test
