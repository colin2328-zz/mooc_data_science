'''
Created on April 16, 2014
@author: Colin Taylor

Creates seperate discretized datasets given a continous datasets. Meant to be run after dividing dataset into cohorts and after train and test!
'''

import numpy as np
import orange
import sys

def create_dataset(file_base, num_bins):
	file_prefix = "data/"
	file_suffix = ".csv"
	train_in_file = file_prefix + file_base + "_train" + file_suffix
	train_out_file = file_prefix + file_base + "_bin_%s_train" % (num_bins) + file_suffix
	test_in_file = file_prefix + file_base + "_test" + file_suffix
	test_out_file = file_prefix + file_base + "_bin_%s_test" % (num_bins) + file_suffix

	train_data = np.genfromtxt(train_in_file, delimiter = ',', skip_header = 0)
	test_data = np.genfromtxt(train_in_file, delimiter = ',', skip_header = 0)

	num_features = train_data.shape[1]
	attributes = np.ndarray((1,num_features),  buffer=np.array(range(1,num_features + 1)))
	classes = np.ndarray((1,num_features), buffer=np.array(["continuous" for i in range(num_features)]))
	orange_data = np.concatenate((attributes, classes, train_data))

	data_binned = orange.Preprocessor_discretize(orange_data,\
	  method=orange.EquiNDiscretization(numberOfIntervals=num_bins)) #find cutoffs from orange

	for i in range(num_features):
		cutoffs_string =  str(data_binned.domain.attributes[i].getValueFrom.transformer.points).lstrip('<').rstrip('>')
		bins = [ float(ele) for ele in cutoffs_string.split(", ")]

		train_digitized = np.digitize(train_data[:, i], bins)
		train_data[:,i] = train_digitized

		test_digitized = np.digitize(test_data[:, i], bins)
		train_data[:,i] = test_digitized

	np.savetxt(train_out_file, train_data, fmt="%d", delimiter=";")
	np.savetxt(test_out_file, test_data, fmt="%d", delimiter=";")

# cohorts = ["forum_only", "wiki_only", "no_collab", "forum_and_wiki"]
cohorts = ["no_collab"]
for cohort in cohorts:
	for num_bins in [5, 10]:
		file_base = "features_%s_pca" % cohort
		create_dataset(file_base, num_bins)



