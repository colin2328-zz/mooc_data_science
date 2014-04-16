'''
Created on April 16, 2014
@author: Colin Taylor

Creates train and test datasets for already seperated cohorts
'''

import numpy as np
import time
import random

def add_to_data(old_data, new_data):
	if old_data == None:
		return new_data
	else:
		return np.concatenate((old_data, new_data))

def seperate_train_test(file_base):
	print "seperating cohort: %s" % (file_base)
	file_suffix = ".csv"
	file_prefix = "data/"
	in_file = file_prefix + file_base + file_suffix
	data = np.genfromtxt(in_file, delimiter = ',', skip_header = 0)

	start_idx = 0
	end_idx = len(data)
	num_weeks = 15
	num_students = end_idx / num_weeks

	#get number of dropouts per dropout week: first week is week 0
	dropout_count = [0] * num_weeks
	while start_idx < end_idx:	
		dropouts = data[start_idx : start_idx + num_weeks, 0].tolist()
		try:
			dropout_week = dropouts.index(0) 
		except ValueError:
			dropout_week = num_weeks - 1
		dropout_count[dropout_week] +=1
		start_idx += num_weeks #move to next student

	def write_and_print(cohort, data):
		print "number of students in %s: %s. Percent of students: %s" % (cohort, len(data) / num_weeks, float(len(data) / num_weeks) / num_students)
		out_file = file_prefix + file_base + "_"  + cohort + file_suffix
		np.savetxt(out_file, data, fmt="%s", delimiter=",")

	start_idx = 0
	dropout_count_train = [0] * num_weeks
	dropout_count_test = [0] * num_weeks
	train_data = None
	test_data = None
	while start_idx < end_idx:
		stud_data = data[start_idx : start_idx + num_weeks]
		dropouts = data[start_idx : start_idx + num_weeks, 0].tolist()

		try:
			dropout_week = dropouts.index(0) 
		except ValueError:
			dropout_week = num_weeks - 1

		train_test_ratio = float(dropout_count_train[dropout_week]) / max(1,(dropout_count_test[dropout_week]))
		if train_test_ratio < .7/.3:
			dropout_count_train[dropout_week]+=1
			train_data = add_to_data(train_data, stud_data)
		else:
			dropout_count_test[dropout_week]+=1
			test_data = add_to_data(test_data, stud_data)

		start_idx += num_weeks #move to next student

	print "train percent by dropout_week:", [float(dropout_count_train[dropout_week]) / max(1,dropout_count[dropout_week]) for dropout_week in range(15)]
	print "totals by dropout_week:", dropout_count

	write_and_print("train", train_data)
	write_and_print("test", test_data)
	print ""


cohorts = ["forum_only", "wiki_only", "no_collab", "forum_and_wiki"]
for cohort in cohorts:
	file_base = "features_" + cohort
	seperate_train_test(file_base)



