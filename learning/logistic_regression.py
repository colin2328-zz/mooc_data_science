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

from sklearn import linear_model, cross_validation
from sklearn.metrics import roc_curve, auc
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

import flatten_featureset
import utils

def load_data(train_file, test_file, lead, lag):
	intermediate_file1 = "data/train.csv"
	intermediate_file2 = "data/test.csv"

	flatten_featureset.create_features(intermediate_file1, train_file, lead, lag)
	train_data = np.genfromtxt(intermediate_file1, delimiter = ',', skip_header = 1)
	os.remove(intermediate_file1)

	flatten_featureset.create_features(intermediate_file2, test_file, lead, lag)
	test_data = np.genfromtxt(intermediate_file2, delimiter = ',', skip_header = 1)
	os.remove(intermediate_file2)
	
	X_train = train_data[:,1:] #file format is [label list_of_features]
	Y_train = train_data[:,0]
	X_test = test_data[:,1:] #file format is [label list_of_features]
	Y_test = test_data[:,0]

	return X_train, Y_train, X_test, Y_test

def load_and_run_regression(train_file, test_file, lead, lag):
	X_train, Y_train, X_test, Y_test = load_data(train_file, test_file, lead, lag)
	return run_regression(X_train, Y_train, X_test, Y_test, lead, lag)

def run_regression(X_train, Y_train, X_test, Y_test, lead, lag):
	num_crossval = 10
	start_time = time.time()
	logreg = Pipeline([('scale', StandardScaler()), ('logreg', linear_model.LogisticRegression())])

	#do cross-validation
	try:
		auc_crossval =  np.mean(cross_validation.cross_val_score(logreg, X_train, Y_train, scoring='roc_auc', cv=num_crossval))
	except:
		auc_crossval = 0.0

	#do training on train
	logreg.fit(X_train, Y_train)

	desired_label = 0 # want to predict if student will dropout
	desired_label_index = logreg.steps[-1][1].classes_.tolist().index(desired_label) 

	try:
		predicted_probs = logreg.predict_proba(X_train)
		fpr, tpr, thresholds = roc_curve(Y_train, predicted_probs[:, desired_label_index],  pos_label=desired_label)
		auc_train = auc(fpr, tpr)
	except:
		auc_train = 0.0

	try:
		predicted_probs = logreg.predict_proba(X_test)
		fpr, tpr, thresholds = roc_curve(Y_test, predicted_probs[:, desired_label_index],  pos_label=desired_label)
		auc_test = auc(fpr, tpr)
	except:
		auc_test = 0.0

	print "ran logistic regression for lead %s lag %s in %s seconds" % (lead, lag, time.time() - start_time)
	return (float(auc_train), float(auc_test), auc_crossval)

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Create feature csv with given lead and lag.')
	parser.add_argument('--train_file',type=str, default="data/features_wiki_only_train.csv") # input csv
	parser.add_argument('--test_file',type=str, default="data/features_wiki_only_test.csv") # input csv
	parser.add_argument('--lead',type=int, default=8)  # number of weeks ahead to predict
	parser.add_argument('--lag',type=int, default=4)  # number of weeks of features to use
	args = parser.parse_args()

	train_auc, test_auc = load_and_run_regression(args.train_file, args.test_file, args.lead, args.lag)
	print "Test auc: %s. Train auc: %s" % (test_auc, train_auc)