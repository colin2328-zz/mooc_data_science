'''
Created on April 17, 2014
@author: Colin Taylor
'''

import numpy as np
import pylab as pl
import run_train_hmm, run_inference_hmm, run_hmm_cross_val
import utils

def run_hmm(data_file_base, num_support, num_pools, num_iterations, train=True):
	#run crossval
	run_hmm_cross_val.do_crossval(data_file_base, num_support, num_iterations=num_iterations, num_pools=num_pools)

	#If train is true- actually build the model
	if train:
		run_train_hmm.train_model(data_file_base, num_support, num_pools=num_pools, num_iterations=num_iterations)	

	header = "lead,auc"

	#create results_file name
	train_results_file = "results/hmm_" + data_file_base + "_support_%s_train.csv" % (num_support)
	test_results_file = "results/hmm_" + data_file_base + "_support_%s_test.csv" % (num_support)

	train_data = None
	test_data = None
	for lead in range(1,15):
		try:
			train_roc = run_inference_hmm.run_inference(data_file_base, num_support, "train", lead, plot_roc=False)
			train_data = utils.add_to_data(train_data, [lead, train_roc])
			np.savetxt(train_results_file, np.atleast_2d(train_data), fmt="%s", delimiter=",", header= header, comments='')
		except:
			pass
		try:
			test_roc = run_inference_hmm.run_inference(data_file_base, num_support, "test", lead, plot_roc=False)	
			test_data = utils.add_to_data(test_data, [lead, test_roc])
			np.savetxt(test_results_file, np.atleast_2d(test_data), fmt="%s", delimiter=",", header= header, comments='')
		except:
			pass
	np.savetxt(train_results_file, np.atleast_2d(train_data), fmt="%s", delimiter=",", header= header, comments='')
	np.savetxt(test_results_file, np.atleast_2d(test_data), fmt="%s", delimiter=",", header= header, comments='')

if __name__ == "__main__":
	train = True
	data_file_base = "features_cut_wiki_only_bin_5"
	num_support = 5
	num_pools = 10
	num_iterations = 5

	run_hmm(data_file_base, num_support, num_pools=num_pools, num_iterations=num_iterations, train=train)