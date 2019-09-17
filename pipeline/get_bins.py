'''
Get some features from the original col
    -- binize some continuous variable
'''
import pandas as pd 
import numpy as np

def binize(df, col, bins=None, labels=None):
    '''
    Cut the col into categories
    Input:
        df: dataframe 
        col: continous column that needs to be cut
        col_bins: list of numbers, boundaries of each bin
        col_labels: list of string to fill the new col
        new_name: the categories col 's new name
    Return:
        dataframe with a new categorical column
    '''
    if not bins and not labels:
        series = pd.qcut(df[col], q=4)
    elif not labels and bins != None:
        series = pd.qcut(df[col], q=bins)
    elif not bins and labels != None:
        series = pd.qcut(df[col], q=len(labels), labels=labels)
    else:
        series = pd.qcut(df[col], q=bins, labels=labels)
    return series
