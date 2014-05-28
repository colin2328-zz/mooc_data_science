'''
Created on April 16, 2014
@author: Colin Taylor

'''

import numpy as np
import orange
import sys

num_bins = 5
file_prefix = "data/"
file_suffix = ".csv"
file_base = "features"
in_file = file_prefix + file_base + file_suffix
out_file = file_prefix + file_base + "_bin_%s" % (num_bins) + file_suffix

data = np.genfromtxt(in_file, delimiter = ',', skip_header = 1)

num_features = data.shape[1]
attributes = np.ndarray((1,num_features),  buffer=np.array(range(1,num_features + 1)))
classes = np.ndarray((1,num_features), buffer=np.array(["continuous" for i in range(num_features)]))
orange_data = np.concatenate((attributes, classes, data))

data_binned = orange.Preprocessor_discretize(orange_data,\
  method=orange.EquiNDiscretization(numberOfIntervals=num_bins)) #find cutoffs from orange

for i in range(num_features):
	cutoffs_string =  str(data_binned.domain.attributes[i].getValueFrom.transformer.points).lstrip('<').rstrip('>')
	bins = [ float(ele) for ele in cutoffs_string.split(", ")]

	digitized = np.digitize(data[:, i], bins)
	data[:,i] = digitized


np.savetxt(out_file, data, fmt="%d", delimiter=",")





