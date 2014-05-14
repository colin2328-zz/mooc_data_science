'''
Created on March 17, 2013
@author: Colin Taylor

Flatten a multi data point, multi time sequenced dataset with a given lead and lag
'''

import csv
import argparse
import numpy as np
		
def create_features(out_file, in_file, lead, lag):
	out_csv = open(out_file, "wb") #file format is [label list_of_features ]
	# infile format is [features] (includes feature 1, no header)
	csv_writer = csv.writer(out_csv, delimiter= ',')
	
	data = np.genfromtxt(in_file, delimiter = ',', skip_header = 0)
	num_weeks = 15
	num_students = len(data) / num_weeks
	num_cols = (data.shape[1] - 1 ) * lag + 1

	header = ["dropout"]
	for feature_num in range(2, num_cols + 1):
		header += ["feature_%s" % (feature_num)]
	csv_writer.writerow(header)

	for student in range(num_students):
		stud_data = data[student * num_weeks: (student + 1) * num_weeks]
		predict_week = lead + lag - 1
		label = stud_data[predict_week][0]
		last_label = stud_data[lag -1, 0]
		if last_label == 0:
			continue  #if the previous label is 0, don't want to include this student- prediction problem is too easy!
		write_array = [label]
		active_week = 0
		while active_week < lag: #add data from each lag week
			write_array += stud_data[active_week, 1:].tolist()
			active_week+=1
		csv_writer.writerow(write_array)
	
if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Create feature csv with given lead and lag.')
	parser.add_argument('--in_file',type=str, default="data/features_forum_and_wiki_train.csv") #  # input csv. No header, no week number.
	parser.add_argument('--out_file',type=str, default="tmp.csv") # output csv
	parser.add_argument('--lead',type=int, default=14)  # number of weeks ahead to predict
	parser.add_argument('--lag',type=int, default=1)  # number of weeks of features to use
	args = parser.parse_args()

	create_features(args.out_file, args.in_file, args.lead, args.lag)