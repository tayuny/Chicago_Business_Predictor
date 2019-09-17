"""
Project: preprocess_business
Yuwei Zhang
"""

import pandas as pd
import numpy as np


logger = logging.getLogger('preprocessing business data')
ch = logging.StreamHandler(sys.stdout)
fh = logging.FileHandler('./log/debug.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
fh.setFormatter(formatter)
logger.addHandler(ch)
logger.addHandler(fh)
logger.setLevel(logging.INFO)


def read_data(path, indexcol, datecol, datatype):
    df = pd.read_csv(path, index_col=indexcol, parse_dates=datecol, dtype=datatype)
    return df


def compute_period(date_issued, change_date, expiration_date):
    if pd.isnull(change_date):
        early_date = expiration_date
    elif pd.isnull(expiration_date):
        early_date = change_date
    else:
        early_date = min(change_date, expiration_date)
    return early_date - date_issued


def check_death(df, date_issued, change_date, expiration_date, outcome_col, year_period):
    df['death_period'] = df.apply(lambda x: compute_period(x[date_issued], x[change_date], x[expiration_date]), axis=1)
    df[outcome_col] = np.where(df['death_period'] < year_period, 1, 0)


def filter_year(df, start_year, end_year, issue_date):
    df['start_year'] = pd.to_numeric(df[issue_date].dt.year)
    return df[(df['start_year'] >= start_year) & (df['start_year'] <= end_year)]


def create_indicator(df, issue_date, change_date, expiration_date, year):
    df['start_year'] = pd.to_numeric(df[issue_date].dt.year)
    df['end_year'] = df.apply(lambda x: x[expiration_date] if x[expiration_date] <= x[change_date] or pd.isnull(x[change_date]) else x[change_date], axis=1)
    df['end_year'] = pd.to_numeric(df['end_year'].dt.year)
    df[str(year) + "ind"] = 0
    df.loc[((year >= df['start_year']) & (year <= df['end_year'])), str(year) + "ind"] = 1
    sub_df = df[df[str(year) + "ind"] == 1]
    sub_df['year'] = year
    sub_df = sub_df.drop(columns=[str(year) + "ind"])
    df = df.drop(columns=[str(year) + "ind"])
    return df, sub_df


def duplicate(df, issue_date, change_date, expiration_date, min_year, max_year):
    new_df = pd.DataFrame(data=None, columns=df.columns)
	
    for year in range(min_year, max_year + 1):
        df, sub_df = create_indicator(df, issue_date, change_date, expiration_date, year)
        new_df = pd.concat([new_df, sub_df])
    new_df['year'] = new_df['year'] - 1
	
    return new_df
	   

def drop_record(df, zipcol):
    df = df[~df[zipcol].isnull()]
    zip_code_list = list(range(60601, 60662)) + [60706,60607,60803,60804,60827]
    pop_list = [60627, 60635, 60650, 60658]
    for zip_unit in pop_list:
        zip_code_list.remove(zip_unit)
		
    for i in range(0, len(zip_code_list)):
        zip_code_list[i] = str(zip_code_list[i])

    df['in_zip'] = df.apply(lambda x: True if x[zipcol] in zip_code_list else False, axis=1)
    df = df[(df['in_zip']) & (df['CITY'] == 'CHICAGO')]
    return df.drop(columns=['in_zip'])
	
#This loop is used for pivoting all the crime data into wide type and concat them
def concat_and_pivot(min_year, max_year)
    for year in range(min_year, max_year):
        file_path = "/mnt/d/UChicago/'2019 spring'/CAPP30254/assignments/Project/crime data/{}_res.csv".format(year)
        df = pd.read_csv(file_path, dtype={'zip': 'str', 'year': 'str'})
        df = df.pivot(index='zip', columns='primary_type', values='count')
        df = df.reset_index()
        df['year'] = str(year)
        df['zip'] = df.apply(lambda x: re.match(r"(\d{5})(.0)", x['zip']).group(1), axis=1)
        if year == min_year:
            crime_data = df
        else:
            crime_data = pd.concat([crime_data, df])
    return crime_data.rename(columns={'zip': 'zip_code'})


def create_outcome(df, outcome, date_issued, change_date, expiration_date):
    '''
    Define the whether a license dies in a year and define its duration
    :param df: a data frame
    :param outcome: 1 is dead and 0 is alive
    :param date_issued: the colname of license issue date
    :param change_date: the colname of license status change date
    :param expiration_date: the colname of license term expiration date

    :return: a modified data frame
    '''
    df['cut_off_date'] = df.apply(lambda x: pd.Timestamp(x['year'] + 2, 12, 31), axis=1)
    df['end_date'] = df.apply(lambda x: x[expiration_date] if x[expiration_date] <= x[change_date] or pd.isnull(x[change_date]) else x[change_date], axis=1)
    df[outcome] = np.where(df['end_date'] < df['cut_off_date'], 1, 0)
    df['early_date'] = df.apply(lambda x: min(x['end_date'], x['cut_off_date']), axis=1)
    df['duration'] = df['early_date'] - df[date_issued]
    return df.drop(columns=['early_date', 'end_date', 'cut_off_date'])


def rename_cols(df):
    '''
    Rename the columns of the dataframe.
    Inputs:
        df: dataframe
    Returns:
        dataframe with renamed columns
    '''
    cols = list(df.columns)
    for col in cols:
        ncol = col.lower()
        ncol = ncol.replace('_', ' ')
        df = df.rename(columns={col: ncol})
    return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=
       'Preprocessing the business data,'
       'it contains get data, '
       'transfrom data into geo data,'
       'spaical join with the zipcode geo coundaries,' 
       'Aggregate the data to get the useful information')
    parser.add_argument('--crime_file', dest='crime_file', type=int, default=2008,
        help='crime file that used for merging')
    parser.add_argument('--311_file', dest='311_file', type=int, default=2017,
        help='311 file that used for merging')
    parser.add_argument('--save_file', help='The csv file to save',default='dataset/total.csv')
    args = parser.parse_args()
    run(args)

