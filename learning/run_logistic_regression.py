'''
Created on April 24, 2013
@author: Colin Taylor

Run logistic_regression for all cohorts and leads and lags
Name pattern of input featureset is: data/features_cut_wiki_only_train.csv
'''
import numpy as np
import logistic_regression
import graph_logistic_regression
import time

def add_to_data(old_data, new_data):
	if old_data == None:
		return new_data
	else:
		return np.vstack((old_data, new_data))

header = "lead,lag,auc"

cohorts = ["forum_only", "wiki_only", "forum_and_wiki", "no_collab"]

features_base = "features_"
data_file_prefix = "data/" + features_base
data_file_suffix = ".csv"


for cohort in cohorts:
	start_time = time.time()
	# figure out how to save and graph both train and test set
	train_results_file = "results/logistic_reg_" + features_base + cohort + "_train" + ".csv"
	train_graph_file = "results/images/logistic_reg_" + features_base + cohort + "_train"
	test_results_file = "results/logistic_reg_" + features_base + cohort + "_test" + ".csv"
	test_graph_file = "results/images/logistic_reg_" + features_base + cohort + "_test"

	train_data = None
	test_data = None
	for lead in range (1,15):
		for lag in range(1, 16 - lead):
			train_file = data_file_prefix + cohort + "_train" + data_file_suffix
			test_file = data_file_prefix + cohort + "_test" + data_file_suffix
			try:
				train_auc, test_auc = logistic_regression.run_regression(train_file, test_file, lead, lag)
				train_data = add_to_data(train_data, [lead, lag, train_auc])
				test_data = add_to_data(test_data, [lead, lag, test_auc])
			except:
				pass
	print "Ran logistic regression for %s in %s seconds" % (cohort, time.time() - start_time)

	np.savetxt(train_results_file, np.atleast_2d(train_data), fmt="%s", delimiter=",", header= header, comments='')
	graph_logistic_regression.graph_logreg(train_results_file, train_graph_file)
	np.savetxt(test_results_file, np.atleast_2d(test_data), fmt="%s", delimiter=",", header= header, comments='')
	graph_logistic_regression.graph_logreg(test_results_file, test_graph_file)
