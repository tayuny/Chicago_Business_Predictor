'''
Main function for the pipeline
'''
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import BaggingClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import LinearSVC
import yaml
from collections import OrderedDict
from itertools import product
import logging
import sys
import numpy as np
import argparse
import os
from pipeline import model_factory
from pipeline import evaluator
import transformer
import pandas as pd
import gc


logger = logging.getLogger('main function')
ch = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.INFO)

def run(config):
    '''
    run the pipeline and save the result to csv file as well as graphs

    Input:
        config: yml file contains all the parameters of the pipeline
    Return:
        save the results to the file
    '''
    logger.info("starting to run the pipeline")
    config = args.config
    with open (config) as config_file:
        configs = yaml.safe_load(config_file)
    df = pd.read_csv(configs['io']['input_path'])
    cols_config = configs['cols']
    time_config = configs['time']
    trans_configs = configs['transform']
    model_configs = configs['models']
    matrix_configs = configs['matrix']
    count = 1
    for data in split(cols_config, time_config, df):
        X_train, X_test, y_train, y_test = data
        X_train, X_test = transformer.transform(trans_configs, X_train, X_test)
        results_df = pd.DataFrame(columns=matrix_configs['col_list'])
        for name, model in model_factory.get_models(model_configs):
            logger.info('start to run the model {}'.format(model))
            model.fit(X_train, y_train)
            print(sys.getsizeof(model))
            if name == 'LinearSVC':
               y_pred_probs = model.decision_function(X_test)
            else:
               y_pred_probs = model.predict_proba(X_test)[:, 1]
            index = len(results_df)
            results_df.loc[index] = get_matrix(results_df, y_pred_probs, y_test, name, model, count,index, matrix_configs)
            del model
            gc.collect()
        results_df.to_csv(matrix_configs['out_path'] + str(count) + ".csv")
        count += 1

def split(cols_config, time_config, df):
    '''
    split the dataset based on the time
    
    Input: 
        cols_config: xs and y
        time_config: start time, end time, time window
        df : dataframe 

    return: 4 dataframes
    '''
    logger.info('starging to split the dataframe')
    X = df[cols_config['x_cols']]
    y = df[cols_config['y_col'][0]]
    min_year = time_config['start_year']
    max_year = time_config['end_year']
    for year in range(min_year + 1, max_year - 3, 2):
        X_train = X[X['year'] <= year]
        X_test = X[(X['year'] == year + 3) | (X['year'] == year + 4)]
        y_train = y[X['year'] <= year].ravel()
        y_test = y[(X['year'] == year + 3) | (X['year'] == year + 4)].ravel()
        logger.info('delivering data to pipeline')
        yield X_train, X_test, y_train, y_test


def get_matrix(results_df, y_pred_probs, y_test, name, model, count, index, matrix_configs):
    '''
    calculate the evaluation matrixs
 
    Input:
        results_df: used to store the result
        y_pred_probs: get the score from the model
        y_test: true y
        name: model's name
        model: model obj
        count: number of train test set
    Return:
        one row of record for the result dataframe 
    '''
    # Sort true y labels and predicted scores at the same time
    y_pred_probs_sorted, y_test_sorted = zip(*sorted(zip(y_pred_probs, y_test), reverse=True))
    # Write the evaluation results into data frame
    threshold = matrix_configs['percentage']
    record = [name, str(model),
              evaluator.precision_at_k(y_test_sorted, y_pred_probs_sorted, 100),
              evaluator.compute_acc(y_test_sorted, y_pred_probs_sorted, threshold),
              evaluator.compute_f1(y_test_sorted, y_pred_probs_sorted, threshold),
              evaluator.compute_auc_roc(y_test_sorted, y_pred_probs_sorted, threshold)]

    threshold_list = [1, 2, 5, 10, 20, 30, 50]
    for t in threshold_list:
    	record.append(evaluator.precision_at_k(y_test_sorted, y_pred_probs_sorted, t))
    	record.append(evaluator.recall_at_k(y_test_sorted, y_pred_probs_sorted, t))
    graph_name_pr = matrix_configs['pr_path'] + r'''precision_recall_curve_{}_{}_{}'''.format(name,count,index)
    evaluator.plot_precision_recall_n(y_test, y_pred_probs, str(model), graph_name_pr, 'save')
    graph_name_roc = matrix_configs['roc_path'] + r'''roc_curve__{}_{}_{}'''.format(name,count,index)
    evaluator.plot_roc(str(model), graph_name_roc, y_pred_probs, y_test, 'save')
    return record

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Do a simple machine learning pipeline, load data, split the data, transform data, build models, run models, get the performace matix results')
    parser.add_argument('--config', dest='config', help='config file for this run', default ='./test_simple.yml')
    args = parser.parse_args()
    run(args)
