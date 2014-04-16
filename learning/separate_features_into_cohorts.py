'''
Created on April 16, 2014
@author: Colin Taylor

Creates cohorts datasets
'''
import numpy as np
import time

in_file_prefix = "data/features"

file_suffix = ".csv"
in_file = in_file_prefix + file_suffix

cohorts = ["forum_only", "wiki_only", "no_collab", "forum_and_wiki", "all_dropouts"]

data = np.genfromtxt(in_file, delimiter = ',', skip_header = 1)

start_idx = 0
end_idx = len(data)
num_weeks = 15
forum_post_idx = 3 #number of forum posts is feature number 3
wiki_idx = 4 #number of wiki edits is feature number 4
dropout_idx = 1 #dropout feature number

def add_to_data(old_data, new_data):
	if old_data == None:
		return new_data
	else:
		return np.concatenate((old_data, new_data))

def write_and_print(cohort):
	data = cohort_datas[cohort]
	print "%s length: %s" % (cohort, len(data) /num_weeks)
	out_file = in_file_prefix + "_"  + cohort + file_suffix
	np.savetxt(out_file, data, fmt="%s", delimiter=",")

start_time = time.time()

cohort_datas = {}
for cohort in cohorts:
	cohort_datas[cohort] = None

while start_idx < end_idx:
	stud_data = data[start_idx: start_idx + num_weeks]
	ever_posted_forum = np.any(stud_data[:,forum_post_idx])
	ever_posted_wiki = np.any(stud_data[:,wiki_idx])
	always_dropout = not stud_data[0][dropout_idx]
	stud_data = stud_data[:, 1:] # Remove week number

	if always_dropout:
		cohort_datas["all_dropouts"] = add_to_data(cohort_datas["all_dropouts"], stud_data)
	elif ever_posted_forum and not ever_posted_wiki:
		cohort_datas["forum_only"] = add_to_data(cohort_datas["forum_only"], stud_data)
	elif ever_posted_forum and ever_posted_wiki:
		cohort_datas["forum_and_wiki"] = add_to_data(cohort_datas["forum_and_wiki"], stud_data)
	elif not ever_posted_forum and ever_posted_wiki:
		cohort_datas["wiki_only"] = add_to_data(cohort_datas["wiki_only"], stud_data)
	else:
		cohort_datas["no_collab"] = add_to_data(cohort_datas["no_collab"], stud_data)

	start_idx += num_weeks #move to next student


for cohort in cohorts:
	write_and_print(cohort)

print "ran in", time.time() - start_time, "seconds"


# Results:
# forum only: 7860
# wiki only: 112
# both: 441
# neither, but started in the course: 44526
# neither, started dropped out 52682