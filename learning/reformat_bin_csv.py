'''
Reformat a csv into fast_bnet new form
from
0;1;2
2;2;3

to 0 1 2 2 2 3
'''
import numpy as np
import utils

in_file = "data/features_cut_no_collab_bin_5_train.csv"
out_file = "/home/colin/evo/fast_bnet/temp.csv"

data = np.genfromtxt(in_file, delimiter = ";")
num_weeks = 15
num_students = len(data) / 15
num_features = data.shape[1]

with open(out_file, 'w') as f:
	pass
with open(out_file, 'a') as f:
	for student in range(num_students):
		stud_data = data[student * num_weeks: (student+1) * num_weeks]
		dropout_dist = stud_data[:,0].tolist()
		try:
			dropout_week = dropout_dist.index(0)
		except:
			dropout_week = num_weeks - 1
		student_combined = stud_data[:dropout_week + 1].ravel().tolist()
		new_line = ";".join([str(int(x)) for x in student_combined]) + "\n"

		f.write(new_line)
