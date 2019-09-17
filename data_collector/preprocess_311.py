'''
Process and merge 311 dataset
Xuan Bu
Peng Wei
'''

import pandas as pd
import data_loader as dl
import logging
import sys
import numpy as np
import argparse
import os


logger = logging.getLogger('preprocessing 311 data')
ch = logging.StreamHandler(sys.stdout)
fh = logging.FileHandler('../data_collector/log/debug.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
fh.setFormatter(formatter)
logger.addHandler(ch)
logger.addHandler(fh)
logger.setLevel(logging.INFO)


DATA_IDS = {'Alley Lights Out': 't28b-ys7j', 'Tree Debris': 'mab8-y9h3',\
         'Abandoned Vehicles': '3c9v-pnva',\
         'Garbage Carts': '9ksk-na4q', 'Graffiti Removal': 'hec5-y4x5',\
         'Rodent Baiting': '97t6-zrhs', 'Tree Trims': 'uxic-zsuj',\
         'Sanitation Code Complaints': 'me59-5fac',\
         'Street Lights - All Out': 'zuxi-7xem',\
         'Street Lights - One Out': '3aav-uy2v'}


def process_311(data_ids):
    '''
    Process and merge 311 data set.
    Inputs:
        data_ids: (dictionary) of different complaint and its id
    Returns:
        (dataframe) of different type of 311 complaint
    '''
    logger.info('start to merge the data')
    pd.options.mode.chained_assignment = None 
    merged_df = pd.DataFrame(columns=['zip_code','year']) 
    for c, d_id in data_ids.items():
        df = dl.get_311(d_id)
        df['year'] = df['creation_date'].str[:4]
        ndf = calculate_completion_rate(df, c)
        merged_df = pd.merge(merged_df, ndf, how='outer',\
                    left_on=['zip_code','year'], right_on = ['zip_code','year'])
    merged_df = merged_df.astype({'year': int})
    processed_df = merged_df[(merged_df['year'] >= 2010) & (merged_df['year'] <= 2017)]
    processed_df = processed_df.fillna(0)
    processed_df = processed_df.astype({'zip_code': str})
    processed_df = processed_df[processed_df['zip_code'] != '0']
    # impute data of 2008 and 2009 using data of 2010
    df_2010 = processed_df[processed_df['year'] == 2010]
    for year in [2008, 2009]:
        temp = df_2010.copy()
        temp['year'] = year
        processed_df = pd.concat([processed_df, temp])
    processed_df = processed_df.reset_index(drop=True)
    return processed_df


def calculate_completion_rate(df, complaint):
    '''
    Calculate the completion rate of each complaint type.
    Inputs:
        df: (dataframe) of each complaint type
        complaint: (str) of the name of complaint type
    Returns:
        (dataframe) of each complaint type with completion rate
    '''
    logger.info('start to calculate the rates')
    col_name_1 = complaint + '_completed'
    df[col_name_1] = df['completion_date'].apply(lambda x: 0 if pd.isnull(x) else 1)
    df_complete = df.groupby(['zip_code', 'year'])[col_name_1]\
                    .sum().reset_index().rename(columns={0: complaint})
    df_total = df.groupby(['zip_code', 'year']).size()\
                 .reset_index().rename(columns={0: complaint})
    merged_df = pd.merge(df_total, df_complete, how='outer',\
                         left_on=['zip_code','year'], right_on = ['zip_code','year'])
    col_name_2 = complaint + '_completion_rate'
    merged_df[col_name_2] = merged_df.apply(lambda x: x[col_name_1]/x[complaint], axis=1)
    merged_df = merged_df.drop([col_name_1], axis=1)
    
    return merged_df


if __name__ == "__main__":
    logger.info('begin to preprocessing the 311 data')
    df = process_311(DATA_IDS)
    df.to_csv('311.csv', sep=',')


