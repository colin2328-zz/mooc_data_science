'''
Created on April 17, 2014
@author: Colin Taylor
'''
import numpy as np
import subprocess
import utils
import time
import os
import shutil
from sklearn import cross_validation
import run_inference_hmm

from multiprocessing import Pool

def execute_hmm(params):
	config_prefix, config_suffix, data_file_base, num_support, crossval_num = params.split("___")
	config_file = config_prefix + data_file_base + "_%s" % crossval_num + config_suffix
	temp_dir = "temp_%s" % (crossval_num)
	time.sleep(1 * int(crossval_num))
	utils.remove_and_make_dir(temp_dir)
	os.chdir(temp_dir)
	HMM_command = ["./../HMM_EM", "Train", "../" + config_file] # need to concatenate since we are running binary
	results = subprocess.check_output(HMM_command)
	test_data = None
	for lead in range(1,14):
		try:
			roc = run_inference_hmm.run_inference(data_file_base, num_support, "test", lead, plot_roc=False, crossval=True, crossval_num=crossval_num)
			test_data = utils.add_to_data(test_data, [lead, roc])
		except:
			pass	
	os.chdir("..")
	return np.atleast_2d(test_data)

def do_crossval(data_file_base, num_support, num_iterations=100, num_pools=12):
	num_crossval = 10
	num_weeks = 15

	data_prefix = "data/"
	config_prefix = "configs/"	
	data_suffix = ".csv"
	config_suffix = ".txt"

	in_data_file = data_prefix + data_file_base + "_train" + data_suffix
	assert os.path.exists(in_data_file), "There is no data file %s" % (in_data_file)
	train_data = np.genfromtxt(in_data_file, delimiter = ';', skip_header = 0)

	#split into 5 folds
	num_students = len(train_data) / num_weeks
	rs = cross_validation.ShuffleSplit(num_students, n_iter=num_crossval, test_size=0.1, indices=True)

	crossval_train = None
	crossval_test = None
	crossval_num = 0
	for train_index, test_index in rs:
		data_file_crossval_train = data_prefix + data_file_base + "_train_%s_train" % crossval_num +  data_suffix
		data_file_crossval_test = data_prefix + data_file_base + "_train_%s_test" % crossval_num +  data_suffix
		config_file = config_prefix + data_file_base + "_%s" % crossval_num + config_suffix

		for stud_idx in train_index:
			stud_data = train_data[stud_idx * num_weeks: (stud_idx + 1) * num_weeks]
			crossval_train = utils.add_to_data(crossval_train, stud_data)
		for stud_idx in test_index:
			stud_data = train_data[stud_idx * num_weeks : (stud_idx + 1) * num_weeks]
			crossval_test = utils.add_to_data(crossval_test, stud_data)

		np.savetxt(data_file_crossval_train, crossval_train, fmt="%d", delimiter=";")
		np.savetxt(data_file_crossval_test, crossval_test, fmt="%d", delimiter=";")
		crossval_num +=1
		crossval_train = None
		crossval_test = None		

		config_file_contents = \
	"""28
2 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5
%s
%s
%s
.0000001
0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 22 23 24 25 26 27
OTHER""" % (num_support, num_iterations, "../" + data_file_crossval_train)	

		with open(config_file, "w") as text_file:
			text_file.write(config_file_contents)

	pool = Pool(num_pools)
	crossval_rocs = pool.map(execute_hmm, ["___".join([config_prefix, config_suffix, data_file_base, str(num_support), str(crossval_num)]) for crossval_num in range(num_crossval)])
	
	for x in range(num_crossval):
		shutil.rmtree("temp_%s/" % x)

	header = "crossval,lead,auc"
	crossval_file = "results/hmm_" + data_file_base + "_support_%s_crossval.csv" % (num_support)
	data = None
	for crossval_num, rocs in enumerate(crossval_rocs):
		if not rocs[0][0] == None:
			for (lead, auc) in rocs:
				data = utils.add_to_data(data, [crossval_num, lead, auc])
				np.savetxt(crossval_file, np.atleast_2d(data), fmt="%s", delimiter=",", header=header, comments='')
	np.savetxt(crossval_file, np.atleast_2d(data), fmt="%s", delimiter=",", header=header, comments='')
if __name__ == "__main__":
	data_file_base = "features_cut_wiki_only_bin_5"
	num_support = 5
	num_pools = 10
	num_iterations = 100
	do_crossval(data_file_base, num_support, num_pools=num_pools, num_iterations=num_iterations)
