'''
Created on March 17, 2014
@author: Colin Taylor
Run a single logistic regression experiment for a given lead and lag
'''
import numpy as np
import pylab as pl
import argparse
import time
import os

from sklearn import linear_model
from sklearn.metrics import roc_curve, auc

import flatten_featureset

def run_regression(train_file, test_file, lead, lag):
	start_time = time.time()
	intermediate_file = "data/tmp.csv"

	flatten_featureset.create_features(intermediate_file, train_file, lead, lag)
	train_data = np.genfromtxt(intermediate_file, delimiter = ',', skip_header = 1)
	os.remove(intermediate_file)

	flatten_featureset.create_features(intermediate_file, test_file, lead, lag)
	test_data = np.genfromtxt(intermediate_file, delimiter = ',', skip_header = 1)
	os.remove(intermediate_file)
	
	X_train = train_data[:,1:] #file format is [label list_of_features]
	Y_train = train_data[:,0]
	X_test = test_data[:,1:] #file format is [label list_of_features]
	Y_test = test_data[:,0]

	logreg = linear_model.LogisticRegression()
	logreg.fit(X_train, Y_train)

	desired_label = 0 # want to predict if student will dropout
	desired_label_index = logreg.classes_.tolist().index(desired_label) 

	predicted_probs = logreg.predict_proba(X_train)
	fpr, tpr, thresholds = roc_curve(Y_train, predicted_probs[:, desired_label_index],  pos_label=desired_label)
	roc_auc_train = auc(fpr, tpr)

	predicted_probs = logreg.predict_proba(X_test)
	fpr, tpr, thresholds = roc_curve(Y_test, predicted_probs[:, desired_label_index],  pos_label=desired_label)
	roc_auc_test = auc(fpr, tpr)

	return (float(roc_auc_train), float(roc_auc_test))

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Create feature csv with given lead and lag.')
	parser.add_argument('--train_file',type=str, default="data/features_cut_forum_and_wiki_train.csv") # input csv
	parser.add_argument('--test_file',type=str, default="data/features_cut_forum_and_wiki_test.csv") # input csv
	parser.add_argument('--lead',type=int, default=1)  # number of weeks ahead to predict
	parser.add_argument('--lag',type=int, default=1)  # number of weeks of features to use
	args = parser.parse_args()

	train_auc, test_auc = run_regression(args.train_file, args.test_file, args.lead, args.lag)
	print "Test auc: %s. Train auc: %s" % (train_auc, test_auc)