'''
Created on April 24, 2013
@author: Colin Taylor

Runs logistic_reg_hmm experiments over leads, lags and support. Runs in parallel
'''
import time
import numpy as np
import argparse
import utils

from run_logistic_regression_on_hmm_state import run_log_reg_hmm 
import run_train_hmm
from multiprocessing import Pool


def execute_log_reg_hmm(features_base_cohort_support_lead_lag_pools_iterations):
	features_base, cohort, num_support, lead, lag, num_pools, num_iterations = features_base_cohort_support_lead_lag_pools_iterations.split("___")
	data_file_base = features_base + cohort + "_bin_5"
	try:
		train, test, crossval = run_log_reg_hmm(data_file_base, int(num_support), int(num_pools), int(num_iterations), int(lead), int(lag), train=False, do_parallel= False)
		return "___".join([lead, lag, str(train), str(test), str(crossval)])
	except Exception as e:
		print e

def run_experiments(data_file_base, num_support, num_pools, num_iterations):
	header = "lead,lag,support,auc"
	features_base = "features_"
	cohort = data_file_base[len(features_base):len("_bin_5") * -1]

	start_time = time.time()
	train_results_file = "results/logistic_reg_hmm_" + features_base + cohort + "_bin_5_support_%s_train" % num_support + ".csv"
	test_results_file = "results/logistic_reg_hmm_" + features_base + cohort + "_bin_5_support_%s_test" % num_support + ".csv"
	crossval_results_file = "results/logistic_reg_hmm_" + features_base + cohort + "_bin_5_support_%s_crossval" % num_support + ".csv"

	train_data = None
	test_data = None
	crossval_data = None
	data_file_base = features_base + cohort + "_bin_5"
	run_train_hmm.train_model(data_file_base, num_support, num_pools=num_pools, num_iterations=num_iterations, logreg=True, do_parallel=True)
	pool = Pool(num_pools)
	args_list = []
	for lead in range (1,14):
		for lag in range(1, 15 - lead):
			args_list += ["___".join([features_base, cohort, str(num_support), str(lead), str(lag), str(num_pools), str(num_iterations)])]
	lead_lag_train_test_crossvals = pool.map(execute_log_reg_hmm, args_list)
	for lead_lag_train_test_crossval in lead_lag_train_test_crossvals:
		if lead_lag_train_test_crossval:
			lead, lag, train_auc, test_auc, crossval_auc = lead_lag_train_test_crossval.split("___")
			if train_auc:
				train_data = utils.add_to_data(train_data, [int(lead), int(lag), num_support, float(train_auc)])
			if test_auc:
				test_data = utils.add_to_data(test_data, [int(lead), int(lag), num_support, float(test_auc)])
			if crossval_auc:
				crossval_data = utils.add_to_data(crossval_data, [int(lead), int(lag), num_support, float(crossval_auc)])

	print "Ran logistic regression for %s support %s in %s seconds" % (cohort, num_support, time.time() - start_time)
	start_time = time.time()
	np.savetxt(train_results_file, np.atleast_2d(train_data), fmt="%s", delimiter=",", header= header, comments='')
	np.savetxt(test_results_file, np.atleast_2d(test_data), fmt="%s", delimiter=",", header= header, comments='')
	np.savetxt(crossval_results_file, np.atleast_2d(crossval_data), fmt="%s", delimiter=",", header= header, comments='')

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Create feature csv with given lead and lag.')
	parser.add_argument('--data_file_base',type=str, default="features_cut_no_collab_pca_bin_5")
	parser.add_argument('--support',type=str, default=5)
	args = parser.parse_args()

	num_pools = 12
	num_iterations = 10

	run_experiments(args.data_file_base, args.support, num_pools, num_iterations)