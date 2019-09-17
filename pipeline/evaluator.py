import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.metrics import roc_curve
from sklearn.metrics import roc_auc_score
from sklearn.metrics import auc
from sklearn.metrics import precision_recall_curve
import matplotlib.pyplot as plt

def compute_acc(y_true, y_scores, k):
    '''
    Compute accuracy score based on threshold
    :param pred_scores: (np array) an array of predicted score
    :param threshold: (float) the threshold of labeling predicted results
    :param y_test: test set

    :return: (float) an accuracy score
    '''
    y_scores_sorted, y_true_sorted = joint_sort_descending(np.array(y_scores), np.array(y_true))
    preds_at_k = generate_binary_at_k(y_scores_sorted, k)

    return accuracy_score(y_true_sorted, preds_at_k)


def compute_f1(y_true, y_scores, k):
    '''
    Compute f1 score based on threshold
    :param pred_scores: (np array) an array of predicted score
    :param threshold: (float) the threshold of labeling predicted results
    :param y_test: test set

    :return: (float) an f1 score
    '''
    y_scores_sorted, y_true_sorted = joint_sort_descending(np.array(y_scores), np.array(y_true))
    preds_at_k = generate_binary_at_k(y_scores_sorted, k)

    return f1_score(y_true_sorted, preds_at_k)

def compute_auc_roc(y_true, y_scores, k):
    '''
    Compute area under Receiver Operator Characteristic Curve
    :param pred_scores: (np array) an array of predicted score
    :param threshold: (float) the threshold of labeling predicted results
    :param y_test: test set

    :return: (float) an auc_roc score
    '''
    y_scores_sorted, y_true_sorted = joint_sort_descending(np.array(y_scores), np.array(y_true))
    preds_at_k = generate_binary_at_k(y_scores_sorted, k)

    return roc_auc_score(y_true_sorted, preds_at_k)


def compute_auc(pred_scores, true_labels):
    '''
    Compute auc score
    :param pred_scores: an array of predicted scores
    :param true_labels: an array of true labels

    :return: area under curve score
    '''
    fpr, tpr, thresholds = roc_curve(true_labels, pred_scores, pos_label=2)
    return auc(fpr, tpr)


# The following functions are referenced from:
# https://github.com/rayidghani/magicloops/blob/master/mlfunctions.py

def joint_sort_descending(l1, l2):
    '''
    Sort two arrays together
    :param l1:  numpy array
    :param l2:  numpy array

    :return: two sorted arrays
    '''
    idx = np.argsort(l1)[::-1]
    return l1[idx], l2[idx]


def generate_binary_at_k(y_scores, k):
    '''
    predict labels based on thresholds
    :param y_scores: the predicted scores
    :param k: (int or float) threshold

    :return: predicted labels
    '''
    cutoff_index = int(len(y_scores) * (k / 100.0))
    predictions_binary = [1 if x < cutoff_index else 0 for x in range(len(y_scores))]
    return predictions_binary


def precision_at_k(y_true, y_scores, k):
    '''
    Compute precision based on threshold (percentage)
    :param y_true: the true labels
    :param y_scores: the predicted labels
    :param k: (int or float) the threshold

    :return: (float) precision score
    '''
    y_scores_sorted, y_true_sorted = joint_sort_descending(np.array(y_scores), np.array(y_true))
    preds_at_k = generate_binary_at_k(y_scores_sorted, k)
    return precision_score(y_true_sorted, preds_at_k)


def recall_at_k(y_true, y_scores, k):
    '''
    Compute recall based on threshold (percentage)
    :param y_true: the true labels
    :param y_scores: the predicted labels
    :param k: (int or float) the threshold

    :return: (float) recall score
    '''
    y_scores_sorted, y_true_sorted = joint_sort_descending(np.array(y_scores), np.array(y_true))
    preds_at_k = generate_binary_at_k(y_scores_sorted, k)
    return recall_score(y_true_sorted, preds_at_k)


def plot_precision_recall_n(y_true, y_prob, name, save_name, output_type):
    #pdb.set_trace()    
    y_score = y_prob
    precision_curve, recall_curve, pr_thresholds = precision_recall_curve(y_true, y_score)
    precision_curve = precision_curve[:-1]
    recall_curve = recall_curve[:-1]
    pct_above_per_thresh = []
    number_scored = len(y_score)
    for value in pr_thresholds:
        num_above_thresh = len(y_score[y_score >= value])
        pct_above_thresh = num_above_thresh / float(number_scored)
        pct_above_per_thresh.append(pct_above_thresh)
    pct_above_per_thresh = np.array(pct_above_per_thresh)

    plt.clf()
    fig, ax1 = plt.subplots()
    ax1.plot(pct_above_per_thresh, precision_curve, 'b')
    ax1.set_xlabel('percent of population')
    ax1.set_ylabel('precision', color='b')
    ax2 = ax1.twinx()
    ax2.plot(pct_above_per_thresh, recall_curve, 'r')
    ax2.set_ylabel('recall', color='r')
    ax1.set_ylim([0, 1])
    ax1.set_ylim([0, 1])
    ax2.set_xlim([0, 1])

    plt.title(name)
    if (output_type == 'save'):
        plt.savefig(save_name)
        plt.close()
    elif (output_type == 'show'):
        plt.show()
    else:
        plt.show()


def plot_roc(name, save_name, probs, y_true, output_type):
    
    fpr, tpr, thresholds = roc_curve(y_true, probs)
    roc_auc = auc(fpr, tpr)
    plt.clf()
    plt.plot(fpr, tpr, label='ROC curve (area = %0.2f)' % roc_auc)
    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlim([0.0, 1.05])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title(name)
    plt.legend(loc="lower right")
    if (output_type == 'save'):
        plt.savefig(save_name, close=True)
        plt.close()
    elif (output_type == 'show'):
        plt.show()
    else:
        plt.show()

