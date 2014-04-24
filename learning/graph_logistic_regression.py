'''
Created on April 5, 2014
@author: Colin Taylor
'''

import numpy as np
import pylab as pl
import csv

import utils


def graph_logreg(in_file, graph_file):	
	reader = csv.DictReader(open(in_file, 'r'), delimiter= ",")
	assert (reader.fieldnames == ["lead", "lag", "auc"])

	#initialize lags
	lags = {}
	for lag in range(1,15):
		lags[lag] = {}

	for row in reader:
		lags[round(float(row["lag"]))][round(float(row["lead"]))] = float(row["auc"])

	for lag in lags:
		lead_aucs= lags[lag]
		pl.plot(lead_aucs.keys(), lead_aucs.values(), label='lag = %s' % lag)

	# Plot AUC curve
	pl.plot([0, 16], [0.5,0.5], 'k--')
	pl.ylim([0.0, 1.0])
	pl.xlabel('Lead')
	pl.ylabel('AUC of ROC')
	pl.title('Logistic Regression AUC as lead and lag vary')
	pl.legend(loc="lower center", ncol=3)
	# pl.show()
	utils.save_fig(graph_file)

if __name__ == "__main__":
	in_file = "results/logistic_reg_features_cut_wiki_only_train.csv"
	graph_file = "results/images/logist_reg_features_cut_wiki_only_train"
	graph_logreg(in_file, graph_file)