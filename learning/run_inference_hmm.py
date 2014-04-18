import numpy as np
import subprocess
from sklearn.metrics import roc_curve, auc
import pylab as pl
import sys

in_file = "data/features_cut_no_collab_bin_5_train_cut.csv"
data = np.genfromtxt(in_file, delimiter = ';', skip_header = 0)


num_weeks = 15
lead = 2
num_students = len(data) / num_weeks

dropout_value = 0 #bin value for a student dropped out

command_base = ["./HMM_EM", "PredictObservationDistribution", "./"]

actual_dropouts = 0
predicted_dropouts = 0
num_predictions = 0
predicted_list = []
labels_list = []

for student in range(num_students):
	stud_data = data[student * num_weeks: (student + 1) * num_weeks]
	for end_week in range(num_weeks - lead):
		X = stud_data[0: end_week +1, :].flatten()
		truth_val = stud_data[end_week + lead][0]

		command = command_base + [str(lead)]+ X.astype(str).tolist()
		results = subprocess.check_output( command)

		lines = results.split("\n")[0:-1]
		dropout_dist =  np.fromstring(lines[0], sep=";")
		
		if dropout_dist[dropout_value] > .65:
			predicted_dropouts+=1

		if truth_val == dropout_value:
			actual_dropouts+=1

		labels_list.append(truth_val)
		predicted_list.append(dropout_dist[dropout_value])
		num_predictions+=1

print "predicted_dropouts", predicted_dropouts
print "actual_dropouts", actual_dropouts
print "num_predictions", num_predictions

try:
	fpr, tpr, thresholds = roc_curve(labels_list, predicted_list,  pos_label=dropout_value)
	roc_auc = auc(fpr, tpr)

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

	print roc_auc
except ValueError:
	print "no ROC! There are no positive (dropout) samples!"



