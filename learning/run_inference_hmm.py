'''
Created on April 17, 2014
@author: Colin Taylor
'''

import numpy as np
import subprocess
import time
import os

from sklearn.metrics import roc_curve, auc
import pylab as pl

def plotROC(fpr, tpr, roc_auc, lead):
	# Plot ROC curve
	pl.clf()
	pl.plot(fpr, tpr, label='ROC curve (area = %0.3f)' % roc_auc)
	pl.plot([0, 1], [0, 1], 'k--')
	pl.xlim([0.0, 1.0])
	pl.ylim([0.0, 1.0])
	pl.xlabel('False Positive Rate')
	pl.ylabel('True Positive Rate')
	pl.title('ROC- lead = %s ' % (lead))
	pl.legend(loc="lower right")
	pl.show()

def run_inference(data_file_base, num_support, train_test, lead, plot_roc=False, crossval=False, crossval_num=0):
	start_time = time.time()
	data_prefix = "data/"
	data_suffix = ".csv"

	if crossval:
		models_dir = "./"
		data_file = "../" + data_prefix + data_file_base + "_%s_%s_%s" % ("train", crossval_num, "test") + data_suffix
		command_base = ["./../HMM_EM", "PredictObservationDistribution", models_dir]
	else:
		models_prefix = "models/"
		models_suffix = "_support_%s" % (num_support)
		data_file = data_prefix + data_file_base + "_" + train_test + data_suffix
		models_dir = models_prefix + data_file_base + models_suffix
		command_base = ["./HMM_EM", "PredictObservationDistribution", models_dir]

	assert os.path.exists(models_dir), "There is no trained model in directory %s" % (models_dir)

	data = np.genfromtxt(data_file, delimiter = ';', skip_header = 0)

	num_weeks = 15
	num_students = len(data) / num_weeks
	dropout_value = 0 #bin value for a student dropped out	

	predicted_list = []
	labels_list = []

	for student in range(num_students):
		if student % 250 == 25:
			print "Predicting student %s out of %s students" % (student, num_students)
		stud_data = data[student * num_weeks: (student + 1) * num_weeks]

		for end_week in range(num_weeks - lead -1): #try to predict lead weeks ahead, given all prior weeks
			X = stud_data[0: end_week + 1, :].flatten()
			truth_val = stud_data[end_week + lead, 0]

			if stud_data[end_week, 0] == dropout_value:
				break #student has already dropped out

			command = command_base + [str(lead + end_week)]+ X.astype(str).tolist() #need to pass lead+end_week in- API asks for week to predict
			observration_dist = subprocess.check_output(command)

			lines = observration_dist.split("\n")[0:-1]
			dropout_dist =  np.fromstring(lines[0], sep=";")

			labels_list.append(truth_val)
			predicted_list.append(dropout_dist[dropout_value])

	print "ran train inference in for lead %s cohort %s support %s" % (lead, data_file_base, num_support), time.time() - start_time, "seconds"

	fpr, tpr, thresholds = roc_curve(labels_list, predicted_list,  pos_label=dropout_value)
	roc_auc = auc(fpr, tpr)
	print "roc:", roc_auc

	if plot_roc:
		plotROC(fpr, tpr, roc_auc, lead)
	return roc_auc

if __name__ == "__main__":
	data_file_base = "features_cut_wiki_only_bin_5"
	num_support = 5
	run_inference(data_file_base, num_support, "train", 1, plot_roc =False)