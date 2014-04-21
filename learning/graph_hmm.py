'''
Created on April 21, 2014
@author: Colin Taylor
'''

import numpy as np
import pylab as pl
import csv


def graph_hmm(base_file):
	train_file = base_file + "_train.csv"
	test_file = base_file + "_test.csv"

	reader = csv.DictReader(open(train_file, 'r'), delimiter= ",")
	assert (reader.fieldnames == ["lead", "auc"])

	data = np.genfromtxt(train_file, delimiter = ',', skip_header = 1)
	pl.plot(data[:,0], data[:,1], label='Train')

	data = np.genfromtxt(test_file, delimiter = ',', skip_header = 1)
	pl.plot(data[:,0], data[:,1], 'r--', label='Test')

	# Plot AUC curve
	pl.ylim([0.0, 1.0])
	pl.xlabel('Lead')
	pl.ylabel('AUC of ROC')
	pl.title('HMM inference AUC as lead varies')
	pl.legend(loc="lower center", ncol=3)
	pl.show()

if __name__ == "__main__":
	base_file = "results/hmm_features_no_collab_bin_5_support_9"
	graph_hmm(base_file)