import numpy as np
import pylab as pl
import run_train_hmm, run_inference_hmm


def add_to_data(old_data, new_data):
	if old_data == None:
		return new_data
	else:
		return np.vstack((old_data, new_data))

def run_hmm(data_file_base, num_support, num_iterations, train):
	#If train is true- actually build the model
	if train:
		run_train_hmm.train_model(data_file_base, num_support, num_iterations)

	header = "lead,auc"

	#create results_file name
	train_results_file = "results/hmm_" + data_file_base + "_support_%s_train.csv" % (num_support)
	test_results_file = "results/hmm_" + data_file_base + "_support_%s_test.csv" % (num_support)

	train_data = None
	test_data = None
	for lead in range (1,15):
		try:
			train_roc = run_inference_hmm.run_inference(data_file_base, num_support, "train", lead, plot_roc=False)
			train_data = add_to_data(train_data, [lead, train_roc])
		except:
			pass
		try:
			test_roc = run_inference_hmm.run_inference(data_file_base, num_support, "test", lead, plot_roc=False)	
			test_data = add_to_data(test_data, [lead, test_roc])
		except:
			pass

	np.savetxt(train_results_file, np.atleast_2d(train_data), fmt="%s", delimiter=",", header= header, comments='')
	np.savetxt(test_results_file, np.atleast_2d(test_data), fmt="%s", delimiter=",", header= header, comments='')

	

if __name__ == "__main__":
	train = True
	data_file_base = "features_cut_wiki_only_bin_5"
	num_support = 5
	num_iterations = 5
	run_hmm(data_file_base, num_support, num_iterations, train)

