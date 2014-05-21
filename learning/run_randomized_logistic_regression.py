'''
Created on April 29, 2014
@author: Colin Taylor
Run multiple randomized logistic regression experiment for a given lead and lag. Used to determine feature weights
'''
import numpy as np
from randomized_logistic_regression import run_regression
import utils

cohorts = ["wiki_only", "forum_only", "forum_and_wiki", "no_collab"]
features_base = "features_"

data_file_prefix = "data/"
data_file_suffix = ".csv"
results_prefix = "results/randomized_logistic_reg_"
results_suffix = ".csv"

results_file = results_prefix + features_base + "averaged" + results_suffix
raw_results_file = results_prefix + features_base + results_suffix

header = "cohort,lead,lag," + ",".join(["feature_%s" % x for x in range(2,29)])

data = None
for cohort in cohorts:
	data_file = data_file_prefix + features_base + cohort + data_file_suffix
	total_weights = [0]*27
	num_weights = 0
	with open(raw_results_file, "w") as myfile:
		for lead in range (1,14):
			for lag in range(1, 15 - lead):
				try:
					myfile.write("cohort: %s, lead: %s, lag: %s" % (cohort, lead, lag))
					weights = run_regression(data_file, lead, lag)
					myfile.write(weights)
					averaged_weights = np.mean(np.reshape(weights, (-1, 27)), axis=0)
					data = utils.add_to_data(data, [cohort, lead, lag] + averaged_weights.tolist())
					total_weights += averaged_weights
					num_weights += 1
				except Exception as e:
					print e
					pass

	average_weights = [weight / num_weights for weight in  total_weights]
	data = utils.add_to_data(data, [cohort, "-", "-"] + average_weights)

np.savetxt(results_file, np.atleast_2d(data), fmt="%s", delimiter=",", header= header, comments='')


