import matplotlib.pyplot as pl
import pandas as pd
import numpy as np
import os

hmm_results_dir = "/home/colin/evo/hmm_results/combined/"
task_dirs =  os.listdir(hmm_results_dir)


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
	if not logreg:
		file_name = "hmm_features_%s_bin_5_support_%s_test.csv" % (cohort, support)
		df = pd.read_csv(hmm_results_dir + task_dir + "/" + file_name)
		header = df.columns.values
		lead_dict = df.set_index("lead").to_dict()["auc"]
		support_dict[support] = lead_dict

# cohorts = ["wiki_only", "forum_and_wiki_pca", "no_collab_pca", "forum_only_pca"]
cohorts = ["no_collab_pca"]
for cohort in cohorts:
	data=np.zeros([14, 13])
	support_dict = cohort_dict[cohort]
	for support in range(3, 30, 2):
		for lead in range(1, 14):
			try:
				data[support/2 - 1,lead -1] = support_dict[support][float(lead)]
			except:
				pass

	ax = pl.gca()
	print data.shape	
	pl.imshow(np.transpose(data), interpolation='nearest',origin='lower', vmin=0, vmax=1, cmap='binary')
	ax.set_xlabel("support", fontsize=20)
	ax.set_ylabel("lead", fontsize=20)
	ax.set_title('HMM AUC: %s' % cohort, fontsize=20)
	ax.set_xticks(range(14))
	ax.set_yticks(range(13))
	ax.set_xticklabels(range(3, 30, 2))
	ax.set_yticklabels(range(1,14))
	pl.colorbar()
	pl.show()
	break
