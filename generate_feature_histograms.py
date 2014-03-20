'''
Created on March 19, 2013
@author: Colin Taylor
'''
import time
import numpy as np
import pylab as pl
import csv

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
	pl.subplot( num_features / 5 + 1, min(5,num_features), feature_index) #nrows, ncols, plot num
	pl.hist(dist, bins=50)

	# pl.setp(patches, 'facecolor', 'g', 'alpha', 0.75)
	# pl.xlabel('Feature values')
	pl.ylabel('Frequency')
	pl.title("%s: Count: %s" % (feature_number, dist.count()))

def generate_histograms():
	num_weeks = 15
	num_features = 25
	in_file = "features.csv"

	feature_set = validate_csv(in_file)	

	data = np.genfromtxt(in_file, delimiter = ',', skip_header = 1)
	start_time = time.time()
	print "loaded data in", time.time() - start_time, "seconds"	

	pl.clf()
	feature_index = 1
	while feature_index <= num_features:
		feature_distribution = data[:, feature_index]
		start_time = time.time()
		graph_distribution(np.ma.masked_where(feature_distribution == -1, feature_distribution), feature_set[feature_index -1], feature_index, num_features)
		print "Ran Feature %s in" % (feature_set[feature_index -1]), time.time() - start_time, "seconds"	
		feature_index+=1
	pl.subplots_adjust(hspace=.5)
	pl.show()

if __name__ == "__main__":
	generate_histograms()