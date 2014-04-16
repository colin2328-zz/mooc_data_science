'''
Created on April 9, 2014
@author: Colin Taylor

Generates csv for a student id, dropout week given an input feature file. Input file contains header!
'''

import numpy as np
import csv

import graph_dropout_week

file_base = "features"
in_file = "data/" + file_base + ".csv"
data = np.genfromtxt(in_file, delimiter = ',', skip_header = 1)

out_file = "results/" "dropout_week_" + file_base +  ".csv"
headers = ["student_id", "dropout_week"]
f = open(out_file, 'wb')
writer = csv.DictWriter(f, delimiter= ",", fieldnames=headers)
writer.writeheader()

start_idx = 0
end_idx = len(data)
num_weeks = 15

values = {"student_id": 1}
while start_idx < end_idx:	
	dropouts = data[start_idx : start_idx + num_weeks, 1].tolist()
	try:
		values["dropout_week"] = dropouts.index(0) + 1
	except ValueError:
		values["dropout_week"] = 15
	writer.writerow(values)

	start_idx += num_weeks #move to next student
	values["student_id"] +=1

f.close()

graph_dropout_week.graph_dropout_week(out_file)
