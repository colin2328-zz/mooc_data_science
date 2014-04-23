'''
Created on April 22, 2013
@author: Colin Taylor

Run flatten_featureset for all cohorts to create a set of flattened datasets
Name pattern of flattened featureset is: data/flat/features_cut_wiki_only_lead_5_lag_2_train.csv
Name pattern of input featureset is: data/features_cut_wiki_only_train.csv
'''
import flatten_featureset
import time

cohorts = ["forum_only", "wiki_only", "forum_and_wiki", "no_collab"]
trains = ["train", "test"]

features_base = "features_"
in_data_file_prefix = "data/" + features_base
out_data_file_prefix = "data/flat/" + features_base
data_file_suffix = ".csv"

for cohort in cohorts:
	for train in trains:
		start_time = time.time()
		for lead in range (1,15):
			for lag in range(1, 16 -lead):
				in_data_file = in_data_file_prefix + cohort + "_" + train + data_file_suffix
				out_data_file = out_data_file_prefix + cohort + "_lead_%s_lag_%s_" % (lead, lag) + train + data_file_suffix
				flatten_featureset.create_features(out_data_file, in_data_file, lead, lag)
		print "Ran flatten %s, %s in %s seconds" % (cohort, train, time.time() - start_time)
		



