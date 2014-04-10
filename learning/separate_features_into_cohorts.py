# Results:
# forum only: 7860
# wiki only: 112
# both: 441
# neither, but started in the course: 44526
# neither, started dropped out 52682

import numpy as np

in_file = "features.csv"

data = np.genfromtxt(in_file, delimiter = ',', skip_header = 1)

start_idx = 0
end_idx = len(data)
num_weeks = 15
forum_post_idx = 3 #number of forum posts is feature number 3
wiki_idx = 4 #number of wiki edits is feature number 4
dropout_idx = 1 #dropout feature number

forum_post_count = 0
wiki_count = 0
neither_count = 0
both_count = 0
dropout_count = 0
while start_idx < end_idx:
	stud_data = data[start_idx: start_idx + num_weeks]
	ever_posted_forum = np.any(stud_data[:,forum_post_idx])
	ever_posted_wiki = np.any(stud_data[:,wiki_idx])
	always_dropout = not stud_data[0][1]

	if always_dropout:
		dropout_count +=1
		start_idx += num_weeks #move to next student
		continue

	if ever_posted_forum and not ever_posted_wiki:
		forum_post_count +=1
	elif ever_posted_forum and ever_posted_wiki:
		both_count += 1
	elif not ever_posted_forum and ever_posted_wiki:
		wiki_count +=1
	else:
		neither_count += 1

	start_idx += num_weeks #move to next student

print "forum only:", forum_post_count
print "wiki only:", wiki_count
print "both:", both_count
print "neither, but started in the course:", neither_count
print "neither, started dropped out", dropout_count