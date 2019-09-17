#!/usr/bin/env python3
'''
Get the data from the web
'''
from sodapy import Socrata
import pandas as pd
import numpy as np
import datetime as dt
from census import Census
from us import states

def get_311(data_id):
    '''
    Get 2012 and 2017 311 data from chicago data portal
    Input:
        data_id: id of different type of report
    Return:
        pandas dataframe with the columns and dtypes as COL_TYPES
    '''   
    '''COL_TYPES = {'sr_type': str, 
                 #'created_date': str,
                 'zip_code': int,
                 'longitude': float,
                 'latitude': float,
                  'legacy_record': bool} '''
    #cols = [item for item in COL_TYPES.keys()]
    client = Socrata('data.cityofchicago.org',
                     'E0eO5nY1aKuEY1pVrunfqFhDz',
                     username='pengwei715@gmail.com',
                     password='1QAZ2wsx3edc')

    conds = '''legacy_sr_number IS NULL'''
    res = client.get(data_id, 
                     #where= conds,
                     limit = 1000000)
    client.close()
    df = pd.DataFrame.from_records(res)
#     df['created_date'] = pd.to_datetime(df['created_date'])
#     df = df[df['created_date']>start_year]
#     df = df[df['created_date']<end_year]
    return df



def get_business(start_date, end_date):
    '''
    Get 2013 to 2018 business data
    start_date: "'2019-12-18T20:00:05'"
    end_date: "'2019-12-18T20:00:05'"
    '''
    DATA_ID = "xqx5-8hwx"
    client = Socrata('data.cityofchicago.org',
                     'E0eO5nY1aKuEY1pVrunfqFhDz',
                     username='pengwei715@gmail.com',
                     password='1QAZ2wsx3edc')

    conds = '''date_issued between "{}" and "{}"'''\
            .format(start_date, end_date)  
    res = client.get(DATA_ID, 
    	where = conds,
    	limit = 1000000)
    client.close()
    df = pd.DataFrame.from_records(res)
    return df

def get_acs_data(start_year, end_year):
    '''
    Get the information from census data
    Total population, white population, black population,
    high school degree population, household income
    Return:
        pandas dataframe
    '''
    NAMES_DIC = {'B01001_001E': "population", 
             'B19013_001E': "median_household_income", 
             'B19083_001E': "gini_index", 
             'B992701_002E': "health_coverage_population",
             'B07012_005E': 'same_house_one_year_ago',
             'B10059_002E': 'income_in_the past_12_months_below_poverty_rate'}  
    c = Census('3eb1575454b4de2cf12e0072bd946ecb852579d2')
    lst_df = []

    for item in range(start_year, end_year+1):
        res = c.acs5.get(('NAME', 
                   'B01001_001E',
                   'B19013_001E',
                   'B19083_001E',
                   'B992701_002E',
                   'B07012_005E',
                   'B10059_002E'
                   ),
                   {'for': 'block group',
                   'in': 'state: {} county: {}'.format('17','031')},
                   year = item)
        df = pd.DataFrame.from_records(res)
        df.rename(columns=NAMES_DIC,inplace=True)
        df.drop(columns =['NAME'], axis=1, inplace=True)
        df['geoid'] = df["state"] + df["county"] + df["tract"]
        df['year'] = item
        lst_df.append(df)
    return pd.concat(lst_df)

def get_crime(start_year, end_year):
    '''
    Get 2013 to 2018 crime data from chicago data portal
    Return:
        pandas dataframe with the columns and dtypes as COL_TYPES
    '''
    crime_type = ["HOMICIDE",
                  "CRIM SEXUAL ASSAULT",
                  "ROBBERY","ASSAULT",
                  "BATTERY",
                  "BURGLARY",
                  "ARSON", 
                  "MOTOR VEHICLE THEFT",
                  "THEFT"]
    COL_TYPES = {'block': str, 
                 'case_number': str,
                 'primary_type': 'category',
                 'date': str,
                 'latitude': float,
                 'longitude': float,
                 'year': int}
    MAX_ROWS = 100000000 # the total rows of the original data
    CRIME_DATA_ID = "6zsd-86xi"
    cols = [item for item in COL_TYPES.keys()]
    client = Socrata('data.cityofchicago.org',
                     'E0eO5nY1aKuEY1pVrunfqFhDz',
                     username='pengwei715@gmail.com',
                     password='1QAZ2wsx3edc')
    conds = "year >= {} AND year <= {}".format(start_year, end_year)
    res = client.get(CRIME_DATA_ID, 
                     select=",".join(cols),
                     where= conds,
                     limit = MAX_ROWS)
    client.close()
    df = pd.DataFrame.from_records(res)
    #df['date'] = pd.to_datetime(df['date'])
    df = df[df.primary_type.isin(crime_type)]
    df = df.astype(COL_TYPES)
    return df
