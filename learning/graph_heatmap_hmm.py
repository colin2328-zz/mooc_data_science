import matplotlib.pyplot as pl
import pandas as pd
import numpy as np
import os
import utils

cohorts = ["no_collab_pca", "wiki_only", "forum_and_wiki_pca", "forum_only_pca"]
cohorts +=["no_collab", "forum_and_wiki", "forum_only"]
AUC_fontsize = 8
med_fontsize = 15
fontsize = 22

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


for cohort in cohorts:
	num_supports = 14
	num_leads = 13
	data=np.zeros([num_supports, num_leads])
	support_dict = cohort_dict[cohort]
	for support in range(3, 30, 2):
		for lead in range(1, num_leads + 1):
			try:
				data[support/2 - 1,lead -1] = support_dict[support][float(lead)]
			except:
				pass

	for x in range(num_supports):
		for y in range(num_leads):
				if data[x,y] > 0:
					pl.text(x - .3, y -.1,((int)(100*data[x][y]))/100.0,fontsize=AUC_fontsize)

	ax = pl.gca()
	pl.imshow(np.transpose(data), interpolation='nearest',origin='lower', vmin=0, vmax=1)
	ax.set_xlabel("Number of hidden support", fontsize=fontsize)
	ax.set_ylabel("Lead", fontsize=fontsize)
	# ax.set_title('HMM AUC: %s' % cohort, fontsize=fontsize)

	ax.set_xticks(range(num_supports))
	ax.set_yticks(range(num_leads))
	ax.set_xticklabels(range(3, 30, 2), fontsize=med_fontsize)
	ax.set_yticklabels(range(1,num_leads), fontsize=med_fontsize)

	cb = pl.colorbar()
	for t in cb.ax.get_yticklabels():
		t.set_fontsize(med_fontsize)
	# pl.show()

	utils.save_fig("/home/colin/evo/papers/thesis/figures/hmm/%s" % cohort)

	

for cohort in cohorts:
	#plot mean AUC over support:
	benchmarks = {
	"no_collab": 0.775938784743,
	"wiki_only": 0.609065848058,
	"forum_and_wiki": 0.648563087051,
	"forum_only": 0.76697590925}

	support_dict = cohort_dict[cohort]
	means = {}
	for support in range(3, 30,2):
		data = support_dict[support]
		mean = np.nanmean([ y for (x,y) in data.items()])
		means[support] = mean

	pl.clf()
	ax = pl.gca()
	pl.plot(range(3, 30,2), [means[support] for support in range(3, 30,2)])
	# pl.title('HMM: %s' % cohort, fontsize=fontsize)
	ax.set_xlabel("Number of support", fontsize=fontsize)
	ax.set_ylabel("Mean AUC over all leads", fontsize=fontsize)
	pl.tick_params(axis="both", which='major', labelsize=med_fontsize)
	ax.set_ylim([0.4, 1.0])
	ax.set_xlim([2, 30])
	benchmark_auc = benchmarks[cohort.replace("_pca", "")]
	pl.plot([0, 30], [benchmark_auc, benchmark_auc], color='k', linestyle='--', linewidth=2, label='Logistic regression benchmark AUC: %s' % np.around(benchmark_auc, decimals=2))
	pl.legend(loc="lower center", ncol=3)
	utils.save_fig("/home/colin/evo/papers/thesis/figures/hmm/%s_support_over_time" % (cohort))
	# pl.show()

	# break
