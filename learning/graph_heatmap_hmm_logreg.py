import matplotlib.pyplot as pl
import numpy as np
import os
import csv

hmm_results_dir = "/home/colin/evo/hmm_results/combined/"
task_dirs =  os.listdir(hmm_results_dir)

n = 14
cohort_dict = {}
for task_dir in task_dirs:
	if "features" not in task_dir:
		continue
	cohort = task_dir[task_dir.index("features_") + len("features_"):task_dir.index("_bin_5")]
	logreg = "logreg" in task_dir
	support = int(task_dir[task_dir.index("support"):].split("_")[1])
	if not cohort in cohort_dict:
		cohort_dict[cohort] = {}

	support_dict = cohort_dict[cohort]
	if logreg:
		file_name = "logistic_reg_hmm_features_%s_bin_5_support_%s_test.csv" % (cohort, support)
		in_file = hmm_results_dir + task_dir + "/" + file_name
		data = np.zeros([n, n])
		with open(in_file) as f:
			in_csv = csv.DictReader(f)
			header = in_csv.fieldnames
			assert header[-1] == "auc"
			x_axis = header[0]
			y_axis = header[1]
			for row in in_csv:
				x, y, auc = row[x_axis], row[y_axis], row["auc"]
				data[int(float((y))) -1,int(float((x)))-1] = float(auc)
		support_dict[support] = data

cohorts = ["wiki_only", "forum_and_wiki_pca", "no_collab_pca", "forum_only_pca"]
for cohort in cohorts:
	support_dict = cohort_dict[cohort]
	max_support = 0
	max_total = 0
	for support in range(3, 30,2):
		data = support_dict[support]
		total = np.sum(data)
		if total > max_total:
			max_support = support
			max_total = total
	data = data = support_dict[max_support]
	pl.pcolor(data, vmin=0, vmax=1)
	pl.ylabel("lag", fontsize=20)
	pl.xlabel("lead", fontsize=20)
	pl.title('HMM logreg AUC: %s, support %s' % (cohort, max_support), fontsize=20)
	pl.xticks(range(1,n))
	pl.yticks(range(1,n))
	pl.colorbar()
	pl.show()
