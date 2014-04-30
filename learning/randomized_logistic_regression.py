'''
Created on April 29, 2014
@author: Colin Taylor
Run a single randomized logistic regression experiment for a given lead and lag. Used to determine feature weights
'''

import numpy as np
import argparse
import time
import os

from sklearn import linear_model
from sklearn.metrics import roc_curve, auc

import flatten_featureset

def run_regression(data_file, lead, lag):
	start_time = time.time()
	intermediate_file = "data/tmp.csv"

	flatten_featureset.create_features(intermediate_file, data_file, lead, lag)
	train_data = np.genfromtxt(intermediate_file, delimiter = ',', skip_header = 1)
	os.remove(intermediate_file)
	
	X_train = train_data[:,1:] #file format is [label list_of_features]
	Y_train = train_data[:,0]

	logreg = linear_model.RandomizedLogisticRegression()
	logreg.fit(X_train, Y_train)

	return logreg.scores_

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Create feature csv with given lead and lag.')
	parser.add_argument('--data_file',type=str, default="data/features_cut_forum_and_wiki.csv") # input csv
	parser.add_argument('--lead',type=int, default=1)  # number of weeks ahead to predict
	parser.add_argument('--lag',type=int, default=1)  # number of weeks of features to use
	args = parser.parse_args()

	run_regression(args.data_file, args.lead, args.lag)
