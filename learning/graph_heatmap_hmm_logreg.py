import matplotlib.pyplot as pl
import numpy as np
import os
import csv
import utils

cohorts = ["no_collab_pca", "wiki_only", "forum_and_wiki_pca", "forum_only_pca"]
AUC_fontsize = 8
med_fontsize = 12
fontsize = 18

hmm_results_dir = "/home/colin/evo/hmm_results/combined/"
task_dirs =  os.listdir(hmm_results_dir)

n = 13
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
		for x in range(n):
			for y in range(n):
				if (n - x) + y <=  n:
					data[x,y] = 0.0
				else:
					data[x,y] = None

		with open(in_file) as f:
			in_csv = csv.DictReader(f)
			header = in_csv.fieldnames
			assert header[-1] == "auc"
			for row in in_csv:
				lead, lag, auc = row["lead"], row["lag"], row["auc"]
				lead = int(float((lead)))-1
				lag = int(float((lag)))-1
				week= lead+lag
				data[week,lag] = float(auc)
		support_dict[support] = data

for cohort in cohorts:
	support_dict = cohort_dict[cohort]
	max_support = 3
	means = {}
	for support in range(3, 30,2):
		data = support_dict[support]
		mean = np.nanmean(data)
		means[support] = mean
		if mean > means[max_support]:
			max_support = support

	data = support_dict[max_support]
	for week in range(n):
		for lag in range(n):
				if week >= lag:
					pl.text(week - .3, lag - .1,((int)(100*data[week][lag]))/100.0,fontsize=AUC_fontsize)

	ax = pl.gca()
	pl.imshow(np.transpose(data), interpolation='nearest',origin='lower', vmin=0, vmax=1, cmap='RdBu')
	ax.set_xlabel("The predicted week number", fontsize=fontsize)
	ax.set_ylabel("Lag", fontsize=fontsize)
	# pl.title('Logistic Regression AUC: %s' % cohort, fontsize=fontsize)

	ax.set_xticks(range(n))
	ax.set_yticks(range(n))
	ax.set_xticklabels(range(2,n+2),fontsize=med_fontsize)
	ax.set_yticklabels(range(1,n+1),fontsize=med_fontsize)
	
	cb = pl.colorbar()
	for t in cb.ax.get_yticklabels():
		t.set_fontsize(med_fontsize)

	utils.save_fig("/home/colin/evo/papers/thesis/figures/hmm_logreg/%s_support_%s" % (cohort, max_support))


	#plot mean AUC over support:
	benchmarks = {
	"no_collab": 0.775938784743,
	"wiki_only": 0.609065848058,
	"forum_and_wiki": 0.648563087051,
	"forum_only": 0.76697590925}

	pl.clf()
	ax = pl.gca()
	pl.plot(range(3, 30,2), [means[support] for support in range(3, 30,2)])
	# pl.title('HMM logreg: %s' % cohort, fontsize=fontsize)
	ax.set_xlabel("Number of support", fontsize=fontsize)
	ax.set_ylabel("Mean AUC of all leads and lags", fontsize=fontsize)
	ax.set_ylim([0.4, 1.0])
	ax.set_xlim([2, 30])
	benchmark_auc = benchmarks[cohort.replace("_pca", "")]
	pl.plot([2, 30], [benchmark_auc, benchmark_auc], color='k', linestyle='--', linewidth=2, label='Logistic regression benchmark AUC: %s' % np.around(benchmark_auc, decimals=2))
	pl.legend(loc="lower center", ncol=3)
	# pl.show()
	utils.save_fig("/home/colin/evo/papers/thesis/figures/hmm_logreg/%s_support_over_time" % (cohort))

	# break
