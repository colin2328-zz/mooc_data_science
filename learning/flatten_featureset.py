'''
Created on March 17, 2013
@author: Colin Taylor

Flatten a multi data point, multi time sequenced dataset with a given lead and lag
'''

import csv
import argparse
import numpy as np
		
def create_features(out_file, in_file, lead, lag):
	num_weeks = 15

	out_csv = open(out_file, "wb") #file format is [start_week list_of_features label]
	csv_writer = csv.writer(out_csv, delimiter= ',')
	
	data = np.genfromtxt(in_file, delimiter = ',', skip_header = 0)

	start_idx = 0
	end_idx = len(data)


	while start_idx < end_idx:
		#for each student
		stud_data = data[start_idx:start_idx + num_weeks]
		start_week = 0
		while start_week <= num_weeks - (lead + lag):
			write_array = [start_week]
			active_week = start_week
			while active_week - start_week < lag: #add data from each lag week
				write_array += stud_data[active_week, 1:].tolist()
				active_week+=1
			label = stud_data[start_week + lead + lag - 1][0]
			write_array += [label]
			csv_writer.writerow(write_array)
			if label == 0:
				start_week = num_weeks - (lead + lag) #if the label is 0, don't want to include any more of this student's weeks!
			start_week+=1

		start_idx += num_weeks #move to next student
	
if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Create feature csv with given lead and lag.')
	parser.add_argument('in_file',type=str)  # input csv
	parser.add_argument('out_file',type=str) # output csv
	parser.add_argument('lead',type=int)  # number of weeks ahead to predict
	parser.add_argument('lag',type=int)  # number of weeks of features to use
	args = parser.parse_args()

	create_features(args.out_file, args.in_file, args.lead, args.lag)