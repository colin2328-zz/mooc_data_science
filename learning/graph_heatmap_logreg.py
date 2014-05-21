import pylab as pl
import numpy as np
import csv

cohorts = ["wiki_only", "no_collab", "forum_only", "forum_and_wiki"]
# cohorts = ["no_collab"]

run = 0
for cohort in cohorts:
	n = 13
	in_file = "results/logistic_reg_features_%s_test.csv" % cohort
	data = np.zeros([n, n])
	with open(in_file) as f:
		in_csv = csv.DictReader(f)
		header = in_csv.fieldnames
		assert header[-1] == "auc"
		for row in in_csv:
			x, y, auc = row["lead"], row["lag"], row["auc"]
			x = int(float((x))) -1
			y = int(float((y)))-1
			week= x+y
			data[week,y] = float(auc)

	
	run +=1
	ax = pl.gca()
	# pl.pcolor(data, vmin=0, vmax=1)
	pl.imshow(np.transpose(data), interpolation='nearest',origin='lower', vmin=0, vmax=1, cmap='Reds')
	pl.xlabel("lag")
	pl.ylabel("lead")
	ax.set_xticks(range(13))
	ax.set_yticks(range(13))
	ax.set_xticklabels(range(1,14))
	ax.set_yticklabels(range(1,14))
	pl.title('Logistic Regression AUC: %s' % cohort)
	pl.colorbar()

	for x in range(n):
		for y in range(n):
				if data[x,y] > 0:
					pl.text(x - .2, y,((int)(100*data[x][y]))/100.0,fontsize=15)

	break

	
pl.show()