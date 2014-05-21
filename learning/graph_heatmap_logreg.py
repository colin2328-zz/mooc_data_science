import pylab as pl
import numpy as np
import csv
import utils

cohorts = ["no_collab", "wiki_only", "forum_and_wiki", "forum_only"]
AUC_fontsize = 8
med_fontsize = 12
fontsize = 18

for cohort in cohorts:
	n = 13
	in_file = "results/logistic_reg_features_%s_test.csv" % cohort
	data = np.zeros([n, n])
	for x in range(n):
		for y in range(n):
			data[x,y] = None

	with open(in_file) as f:
		in_csv = csv.DictReader(f)
		header = in_csv.fieldnames
		assert header[-1] == "auc"
		for row in in_csv:
			lead, lag, auc = row["lead"], row["lag"], row["auc"]
			lead = int(float((lead))) -1
			lag = int(float((lag)))-1
			week= lead+lag
			data[week,lag] = float(auc)

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
	ax.set_xticklabels(range(1,n+1),fontsize=med_fontsize)
	ax.set_yticklabels(range(1,n+1),fontsize=med_fontsize)
	
	cb = pl.colorbar()
	for t in cb.ax.get_yticklabels():
		t.set_fontsize(med_fontsize)

	utils.save_fig("/home/colin/evo/papers/thesis/figures/logreg/%s" % cohort)
	
	# print cohort, np.nanmean(data)
	# pl.show()

	# break