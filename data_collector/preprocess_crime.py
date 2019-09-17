'''
preprocessing the crime data

Peng Wei
'''

import data_loader as lo
import util as ut
import pandas as pd
import logging
import sys
import numpy as np
import argparse
import os


logger = logging.getLogger('preprocessing crime data')
ch = logging.StreamHandler(sys.stdout)
fh = logging.FileHandler('./log/debug.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
fh.setFormatter(formatter)
logger.addHandler(ch)
logger.addHandler(fh)
logger.setLevel(logging.INFO)


ZIPCODES_ID = 'unjd-c2ca'
NEIGHS_ID = 'y6yq-dbs2'


def run(args):
    '''
    preprocess the crime data from start year to end year

    Input:
        start_year: int
        end_year: int

    Return:
        df: dataframe that ready to do record linkage
    '''
    logger.info('begin to preprocessing the crime data')

    try:
        start_year = args.start_year
        end_year = args.end_year
        crime_df = lo.get_crime(start_year, end_year)
        geo_df = ut.convert_to_geodf(crime_df, 'longitude','latitude')
        target_geo = ut.import_geometries(ZIPCODES_ID)
        df = ut.link_two_geos(geo_df, target_geo)
        lst = []
        for year in range(start_year, end_year+1):
            temp = df[df['year'] == year]
            res = temp.groupby(['primary_type','zip']).count().reset_index().drop_duplicates(['primary_type','zip'])
            res = res[['primary_type','zip','block']]
            res.rename(columns = {'block':'count'},inplace=True)
            lst.append(res)
        total = pd.concat(lst)
        total.to_csv(args.filename)
        return True
    except:
        logger.error("Error: %s" % sys.exc_info()[0])
        traceback.print_exc()  
    return False
 
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=
       'Preprocessing the crime data,'
       'it contains get data, '
       'transfrom data into geo data,'
       'spaical join with the zipcode geo coundaries,' 
       'Aggregate the data to get the useful information')
    parser.add_argument('--start_year', dest='start_year', type=int, default=2008,
        help='start year of the crime data')
    parser.add_argument('--end_year', dest='end_year', type=int, default=2017,
        help='end year of the crime data')
    parser.add_argument('--load_file', help='The csv file to save from',default='dataset/crime.csv')
    args = parser.parse_args()
    run(args)

