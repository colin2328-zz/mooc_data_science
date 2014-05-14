'''Used to remove users who are never in the course'''
import numpy as np

in_file = "data/features_no_collab.csv"
out_file = "data/out.csv"
data = np.genfromtxt(in_file, delimiter=",")

num_weeks = 15
num_students = len(data) / num_weeks
delete_rows = []
for student in range(num_students):
	stud_data = data[student * num_weeks: (student + 1) * num_weeks]
	feature_7_dist = stud_data[:, 6]
	if not np.any(feature_7_dist):
		delete_rows += range(student * num_weeks, (student + 1) * num_weeks)

data = np.delete(data, delete_rows, axis=0)
print "done", len(delete_rows) / num_weeks

num_students = len(data) / num_weeks
for student in range(num_students):
	stud_data = data[student * num_weeks: (student + 1) * num_weeks]
	feature_7_dist = stud_data[:, 6]
	if not np.any(feature_7_dist):
		print student, "has no feature 7"
		print feature_7_dist, len(feature_7_dist)

np.savetxt(out_file, np.atleast_2d(data), fmt="%s", delimiter=",")
