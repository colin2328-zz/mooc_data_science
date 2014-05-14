'''
Created on April 24, 2013
@author: Colin Taylor

Runs logistic regression using the hidden state distribution of HMM as probabilities
'''
import numpy as np
import time
import subprocess
import os
import sys

from sklearn.metrics import roc_curve, auc
from sklearn import linear_model
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import pylab as pl
import run_train_hmm

def plotROC(fpr, tpr, roc_auc, lead, lag):
	pl.clf()
	pl.plot(fpr, tpr, label='ROC curve (area = %0.3f)' % roc_auc)
	pl.plot([0, 1], [0, 1], 'k--')
	pl.xlim([0.0, 1.0])
	pl.ylim([0.0, 1.0])
	pl.xlabel('False Positive Rate')
	pl.ylabel('True Positive Rate')
	pl.title('ROC- lead = %s lag = %s' % (lead, lag))
	pl.legend(loc="lower right")
	pl.show()

def add_to_data(old_data, new_data):
	if old_data == None:
		return new_data
	else:
		return np.vstack((old_data, new_data))

def run_log_reg_hmm(data_file_base, num_support, num_pools, num_iterations, lead, lag, train=False, do_parallel=True):
	start_time = time.time()
	num_weeks = 15
	plot_roc = False

	data_prefix = "data/"
	data_suffix = ".csv"
	models_prefix = "models/"
	models_suffix = "_support_%s_logreg" % (num_support)
	data_file_train_input = data_prefix + data_file_base + "_train" + data_suffix
	data_file_train_hmm = data_prefix + data_file_base + "_train_logreg" + data_suffix
	data_file_test = data_prefix + data_file_base + "_test" + data_suffix
	models_dir = models_prefix + data_file_base + models_suffix

	train_data = np.genfromtxt(data_file_train_input, delimiter = ';', skip_header = 0)
	test_data = np.genfromtxt(data_file_test, delimiter = ";", skip_header = 0)

	#split into train 1 and train 2
	num_students = len(train_data) / num_weeks
	num_students_train_hmm =  num_students / 2
	train_hmm_data = train_data[: num_students_train_hmm * num_weeks]
	train_logreg_data = train_data[num_students_train_hmm * num_weeks :]

	#train hmm on train_hmm_data
	np.savetxt(data_file_train_hmm, train_hmm_data, fmt="%d", delimiter=";")

	if not os.path.exists(models_dir) or train:
		run_train_hmm.train_model(data_file_base, num_support, num_pools=num_pools, num_iterations=num_iterations, logreg=True, do_parallel=do_parallel)

	assert os.path.exists(models_dir), "There is no trained model in directory %s" % (models_dir)

	def get_log_reg_features(data):
		dropout_value = 0 #bin value for a student dropped out
		command_base = ["./HMM_EM", "PredictStateDistribution", models_dir]

		logreg_X = None
		logreg_Y = []
		for student in range(len(data) / num_weeks):
			stud_data = data[student * num_weeks: (student + 1) * num_weeks]

			end_week = lag -1
			label_week = lead + end_week
			X = stud_data[0: end_week + 1, :].flatten()
			truth_val = stud_data[label_week, 0]
			
			if stud_data[end_week, 0] == dropout_value:
				continue #student has already dropped out

			features = np.array([])
			for prediction_week in range(end_week + 1):
				# get hidden state distribution for each prediction_week
				command = command_base + [str(prediction_week)]+ X.astype(str).tolist() #need to pass lead+end_week in- API asks for week to predict
				results = subprocess.check_output(command)
				state_dist = np.fromstring(results, sep=";")[1:-1]
				prediction_week_features = state_dist[:-1]
				features = np.concatenate([features, np.atleast_1d(prediction_week_features)])
			logreg_X = add_to_data(logreg_X, features)
			logreg_Y += [truth_val]
		return logreg_X, logreg_Y

	# do inference on hmm to get features for logreg
	X_train, Y_train = get_log_reg_features(train_logreg_data)
	print "got train log_reg features for lead %s lag %s cohort %s support %s" % (lead, lag, data_file_base, num_support), time.time() - start_time, "seconds"

	#train log_reg
	logreg = Pipeline([('scale', StandardScaler()), ('logreg', linear_model.LogisticRegression())])
	logreg.fit(X_train, Y_train)

	desired_label = 0 # want to predict if student will dropout
	desired_label_index = logreg.steps[-1][1].classes_.tolist().index(desired_label) 

	#do inference on test set to get logreg features
	start_time = time.time()
	X_test, Y_test = get_log_reg_features(test_data)
	print "got test log_reg features for lead %s lag %s cohort %s support %s" % (lead, lag, data_file_base, num_support), time.time() - start_time, "seconds"

	predicted_probs = logreg.predict_proba(X_train)
	fpr, tpr, thresholds = roc_curve(Y_train, predicted_probs[:, desired_label_index],  pos_label=desired_label)
	roc_auc_train = auc(fpr, tpr)

	predicted_probs = logreg.predict_proba(X_test)
	fpr, tpr, thresholds = roc_curve(Y_test, predicted_probs[:, desired_label_index],  pos_label=desired_label)
	roc_auc_test = auc(fpr, tpr)

	if plot_roc:
		plotROC(fpr, tpr, roc_auc_test, lead, lag)

	return (roc_auc_train, roc_auc_test)

if __name__ == "__main__":
	data_file_base = "features_wiki_only_bin_5"
	num_support = 7
	num_pools = 2
	num_iterations = 20
	lead = 1
	lag = 4

	(roc_auc_train, roc_auc_test) = run_log_reg_hmm(data_file_base, num_support, num_pools, num_iterations, lead, lag, train=True, do_parallel= True)

	print (roc_auc_train, roc_auc_test)
