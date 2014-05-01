'''
Created on April 17, 2014
@author: Colin Taylor

Runs the training of an HMM given data_file, num_support and num_iterations. Runs in parallel
data_file_base is of the form "features_cut_wiki_only_bin_5_train" and exists in data/ dir
Model is created in models/ dir
'''
import numpy as np
import subprocess
import utils
import time
import os
import shutil

from multiprocessing import Pool

def execute_hmm(config_file_iter):
	config_file, iter_number = config_file_iter.split("___")
	temp_dir = "temp_%s" % (iter_number)
	utils.remove_and_make_dir(temp_dir)
	os.chdir(temp_dir)
	HMM_command = ["./../HMM_EM", "Train", "../" + config_file] # need to concatenate since we are running binary
	results = subprocess.check_output(HMM_command)
	lines = results.split("\n")
	last_line = ""
	for line in lines:
		if "Log-likelihood" in line:
			last_line = line
	start_idx = last_line.find(" -")
	log_liklihood = float(last_line[start_idx:])
	os.chdir("..")
	return log_liklihood

def train_model(data_file_base, num_support, num_pools=12, num_iterations=100, logreg=False, do_parallel=True):
	start_time = time.time()
	num_trainings = num_pools

	data_prefix = "../data/" #have to go down directory because we are launching this from temp directory
	config_prefix = "configs/"	
	models_prefix = "models/"
	if logreg:
		num_weeks = 15

		data_prefix = "data/"
		data_suffix = ".csv"
		data_file_train_input = data_prefix + data_file_base + "_train" + data_suffix
		data_file_train_hmm = data_prefix + data_file_base + "_train_logreg" + data_suffix

		train_data = np.genfromtxt(data_file_train_input, delimiter = ';', skip_header = 0)

		#split into train 1 and train 2 - only train on half of the train data if logreg!
		num_students = len(train_data) / num_weeks
		num_students_train_hmm =  num_students / 2
		train_hmm_data = train_data[: num_students_train_hmm * num_weeks]
		train_logreg_data = train_data[num_students_train_hmm * num_weeks :]

		#train hmm on train_hmm_data
		np.savetxt(data_file_train_hmm, train_hmm_data, fmt="%d", delimiter=";")

		data_prefix = "../data/" #have to go down directory because we are launching this from temp directory
		data_suffix = "_train_logreg.csv"
		config_suffix = "_logreg.txt"
		models_suffix = "_support_%s_logreg" % (num_support)
	else:
		data_suffix = "_train.csv"
		config_suffix = ".txt"
		models_suffix = "_support_%s" % (num_support)

	data_file = data_prefix + data_file_base + data_suffix
	config_file = config_prefix + data_file_base + config_suffix
	models_dir = models_prefix + data_file_base + models_suffix

	assert os.path.exists(data_file[3:]), "There is no data file %s" % (data_file[3:])

	config_file_contents = \
	"""28
2 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5
%s
%s
%s
.0000001
0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 22 23 24 25 26 27
OTHER""" % (num_support, num_iterations, data_file)

	with open(config_file, "w") as text_file:
		text_file.write(config_file_contents)

	if do_parallel:
		pool = Pool(num_pools)
		log_liklihoods = pool.map(execute_hmm, [config_file + "___%s" % (x) for x in range(num_trainings)])
		
	else:
		log_liklihoods = map(execute_hmm, [config_file + "___%s" % (x) for x in range(num_trainings)])

	max_iter = log_liklihoods.index(max(log_liklihoods))
	utils.move_emissions_transitions("temp_%s/" % max_iter, models_dir)
	print "built model for %s support %s" % (data_file_base, num_support), time.time() - start_time, "seconds"

	for x in range(num_trainings):
		shutil.rmtree("temp_%s/" % x)

if __name__ == "__main__":
	data_file_base = "features_cut_wiki_only_bin_5"
	num_support = 5
	num_pools = 10
	num_iterations = 100
	train_model(data_file_base, num_support, num_pools, num_iterations, logreg=True, do_parallel=True)

