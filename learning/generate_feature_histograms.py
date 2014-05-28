'''
Created on March 19, 2013
@author: Colin Taylor
'''
import time
import numpy as np
import pylab as pl
import csv
import utils

def generate_histograms(start_feature, end_feature, features_base):
	num_weeks = 15
	num_features = end_feature - start_feature +1
	in_file = "data/%s.csv" % features_base

	feature_set = validate_csv(in_file)	

	start_time = time.time()
	data = np.genfromtxt(in_file, delimiter = ',', skip_header = 1)	
	print "loaded data in", time.time() - start_time, "seconds"	

	pl.clf()
	dropout_vector = data[:, 1]
	for feature_index in range(start_feature, end_feature + 1):
		feature_distribution = data[:, feature_index]
		start_time = time.time()

		m1 = feature_distribution == -1 # remove default values
		masked = np.ma.masked_array(feature_distribution, m1)

		for x, value in enumerate(masked):
			if (x % num_weeks == 0 and  dropout_vector[x] == 0) or (x % num_weeks != 0 and dropout_vector[x - 1] == 0) : #remove values where the student was always dropped out or has already dropped out the prior week
				masked.mask[x] = True

		graph_distribution(masked.compressed(), feature_set[feature_index -1], feature_index - start_feature + 1, num_features)
		print "Ran Feature %s in" % (feature_set[feature_index -1]), time.time() - start_time, "seconds"	
	pl.subplots_adjust(hspace=.5)
	pl.subplots_adjust(wspace=.5)
	# pl.show()
	utils.save_fig("/home/colin/evo/papers/thesis/figures/feature_distributions/%s_%s_%s" % (features_base, start_feature, end_feature))

def validate_csv(in_file):
	prefix = 'feature_'
	in_csv = open(in_file)
	csv_reader = csv.DictReader(in_csv)
	in_header = csv_reader.fieldnames
	feature_set = [] 
	assert('week_number' == in_header[0])
	for string in in_header[1:]:
	    assert(prefix in string)
	    feature_set.append(int(string[len(prefix):]))
	in_csv.close()

	return feature_set


def graph_distribution(dist, feature_number, feature_index,  num_features):
	# n, bins, patches = pl.hist(dist, 50, normed=1)
	pl.subplot( num_features / 3, min(3,num_features), feature_index) #nrows, ncols, plot num
	pl.hist(dist, bins=50)

	# pl.setp(patches, 'facecolor', 'g', 'alpha', 0.75)
	# pl.xlabel('Feature values')
	# pl.ylabel('Frequency')
	ax = pl.gca()
	ax.set_xticks([np.around(min(dist),decimals=3), np.around(max(dist), decimals=3)])
	pl.title("%s: Count: %s" % (feature_number, len(dist)))

if __name__ == "__main__":
	for features_base in ["features", "features_bin_5"]:
		for start_feature in range(2, 28+1, 9):
			end_feature = start_feature + 8
			generate_histograms(start_feature, end_feature, features_base)
		# 	break
		# break