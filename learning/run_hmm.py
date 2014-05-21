'''
Created on April 17, 2014
@author: Colin Taylor
'''

import numpy as np
import pylab as pl
import run_train_hmm, run_inference_hmm, run_hmm_cross_val
import utils
from multiprocessing import Pool

def execute_hmm(params):
	data_file_base, num_support, lead = params.split("___")
	return run_inference_hmm.run_inference(data_file_base, int(num_support), "train", int(lead), plot_roc=False)

def run_hmm(data_file_base, num_support, num_pools, num_iterations, train=True):
	#run crossval
	run_hmm_cross_val.do_crossval(data_file_base, num_support, num_iterations=num_iterations, num_pools=num_pools)

	#If train is true- actually build the model
	if train:
		run_train_hmm.train_model(data_file_base, num_support, num_pools=num_pools, num_iterations=num_iterations)	

	header = "lead,auc"

	#create results_file name
	test_results_file = "results/hmm_" + data_file_base + "_support_%s_test.csv" % (num_support)

	test_data = None

	pool = Pool(num_pools)
	rocs = pool.map(execute_hmm, ["___".join([data_file_base, str(num_support), str(lead)]) for lead in range(1,14)])
	for idx, roc in enumerate(rocs):
		lead = idx + 1
		if roc is not None:
			test_data = utils.add_to_data(test_data, [lead, roc])

	np.savetxt(test_results_file, np.atleast_2d(test_data), fmt="%s", delimiter=",", header= header, comments='')

if __name__ == "__main__":
	train = True
	data_file_base = "features_forum_and_wiki_pca_bin_5"
	num_support = 3
	num_pools = 12
	num_iterations = 3

	run_hmm(data_file_base, num_support, num_pools=num_pools, num_iterations=num_iterations, train=train)