import numpy as np
import pylab as pl
import csv

in_file = "results/logistic_regression_results.csv"
reader = csv.DictReader(open(in_file, 'r'), delimiter= ",")
assert (reader.fieldnames == ["lead", "lag", "auc"])

#initialize lags
lags = {}
for lag in range(1,15):
	lags[lag] = {}

for row in reader:
	lags[int(row["lag"])][int(row["lead"])] = float(row["auc"])

for lag in lags:
	lead_aucs= lags[lag]
	pl.plot(lead_aucs.keys(), lead_aucs.values(), label='lag = %s' % lag)

# Plot AUC curve
pl.ylim([0.0, 1.0])
pl.xlabel('Lead')
pl.ylabel('AUC of ROC')
pl.title('Logistic Regression AUC as lead and lag vary')
pl.legend(loc="lower center", ncol=3)
pl.show()