'''
Created on April 29, 2014
@author: Colin Taylor
Run multiple randomized logistic regression experiment for a given lead and lag. Used to determine feature weights
'''
import numpy as np

from randomized_logistic_regression import run_regression

cohorts = ["wiki_only", "forum_only", "forum_and_wiki", "no_collab"]
# cohorts = ["wiki_only"]
data_file_prefix = "data/"
features_base = "features_"
results_prefix = "results/randomized_logistic_reg_"
data_file_suffix = ".csv"

for cohort in cohorts:
	data_file = data_file_prefix + features_base + cohort + data_file_suffix
	for lead in range (1,15):
		for lag in range(1, 16 - lead):
			try:
				weights = run_regression(data_file, lead, lag)
				print "Weights for %s lead %s lag %s" % (cohort, lead, lag)
				print weights
			except Exception as e:
				# print e
				pass


