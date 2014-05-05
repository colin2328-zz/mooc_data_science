import pylab as pl
import numpy as np
import csv

cohorts = ["wiki_only", "no_collab", "forum_only", "forum_and_wiki"]

for cohort in cohorts:
	in_file = "results/logistic_reg_features_%s_test.csv" % cohort
	# in_file = "results/"
	with open(in_file) as f:
		in_csv = csv.DictReader(f)
		header = in_csv.fieldnames
		assert header[-1] == "auc"
		x_axis = header[0]
		y_axis = header[1]
		data = np.zeros([14, 14])
		for row in in_csv:
			x, y, auc = row[x_axis], row[y_axis], row["auc"]
			data[int(float((x))) -1][int(float((y)))-1] = auc

	pl.pcolor(data)
	pl.xlabel(y_axis)
	pl.ylabel(x_axis)
	pl.title('Logistic Regression AUC: %s' % cohort)
	pl.colorbar()
	pl.show()