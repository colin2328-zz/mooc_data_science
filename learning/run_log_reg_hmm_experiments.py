'''
Created on April 24, 2013
@author: Colin Taylor

Runs logistic_reg_hmm experiments over leads, lags and support. Runs in parallel
'''
import time
import numpy as np
import argparse

from run_logistic_regression_on_hmm_state import run_log_reg_hmm 
import run_train_hmm
from multiprocessing import Pool

def add_to_data(old_data, new_data):
	if old_data == None:
		return new_data
	else:
		return np.vstack((old_data, new_data))

def execute_log_reg_hmm(features_base_cohort_support_lead_lag_pools_iterations):
	features_base, cohort, num_support, lead, lag, num_pools, num_iterations = features_base_cohort_support_lead_lag_pools_iterations.split("___")
	data_file_base = features_base + cohort + "_bin_5"
	try:
		train, test = run_log_reg_hmm(data_file_base, int(num_support), int(num_pools), int(num_iterations), int(lead), int(lag), train=False, do_parallel= False)
		return "___".join([lead, lag, str(train), str(test)])
	except Exception as e:
		print e

def run_experiments(cohort):
	header = "lead,lag,support,auc"
	features_base = "features_"
	num_pools = 12
	num_iterations = 100

	start_time = time.time()
	train_results_file = "results/logistic_reg_hmm_" + features_base + cohort + "_bin_5_train" + ".csv"
	test_results_file = "results/logistic_reg_hmm_" + features_base + cohort + "_bin_5_test"  + ".csv"

	train_data = None
	test_data = None
	for num_support in range(3,30,2):
		data_file_base = features_base + cohort + "_bin_5"
		run_train_hmm.train_model(data_file_base, num_support, num_pools=num_pools, num_iterations=num_iterations, logreg=True, do_parallel=True)
		pool = Pool(num_pools)
		args_list = []
		for lead in range (1,14):
			for lag in range(1, 15 - lead):
				args_list += ["___".join([features_base, cohort, str(num_support), str(lead), str(lag), str(num_pools), str(num_iterations)])]
		lead_lag_train_tests = pool.map(execute_log_reg_hmm, args_list)
		for lead_lag_train_test in lead_lag_train_tests:
			if lead_lag_train_test:
				lead, lag, train_auc, test_auc = lead_lag_train_test.split("___")
				if train_auc:
					train_data = add_to_data(train_data, [int(lead), int(lag), num_support, float(train_auc)])
				if test_auc:
					test_data = add_to_data(test_data, [int(lead), int(lag), num_support, float(test_auc)])
		print "Ran logistic regression for %s support %s in %s seconds" % (cohort, num_support, time.time() - start_time)
		start_time = time.time()
		np.savetxt(train_results_file, np.atleast_2d(train_data), fmt="%s", delimiter=",", header= header, comments='')
		np.savetxt(test_results_file, np.atleast_2d(test_data), fmt="%s", delimiter=",", header= header, comments='')

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Create feature csv with given lead and lag.')
	parser.add_argument('--cohort',type=str, default="no_collab") # input csv
	args = parser.parse_args()

	run_experiments(args.cohort)