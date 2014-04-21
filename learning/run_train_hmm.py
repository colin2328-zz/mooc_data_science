'''
Created on April 17, 2014
@author: Colin Taylor

Runs the training of an HMM given data_file, num_support and num_iterations
data_file_base is of the form "features_cut_wiki_only_bin_5_train" and exists in data/ dir
Model is created in models/ dir
'''
import subprocess
import utils
import time

def train_model(data_file_base, num_support, num_iterations=100):
	start_time = time.time()

	data_prefix = "data/"
	data_suffix = "_train.csv"
	config_prefix = "configs/"
	config_suffix = ".txt"
	models_prefix = "models/"
	models_suffix = "_support_%s" % (num_support)

	data_file = data_prefix + data_file_base + data_suffix
	config_file = config_prefix + data_file_base + config_suffix
	models_dir = models_prefix + data_file_base + models_suffix

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

	HMM_command = ["./HMM_EM", "Train", config_file] # need to concatenate since we are running binary
	subprocess.call(HMM_command)

	utils.move_emissions_transitions(models_dir)
	print "built model in", time.time() - start_time, "seconds"

if __name__ == "__main__":
	data_file_base = "features_cut_wiki_only_bin_5"
	num_support = 5
	num_iterations = 5
	train_model(data_file_base, num_support, num_iterations)

