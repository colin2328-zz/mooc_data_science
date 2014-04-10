import numpy as np
import subprocess
from sklearn.metrics import roc_curve, auc
import pylab as pl

in_file = "features_bin_cut.csv"
data = np.genfromtxt(in_file, delimiter = ';', skip_header = 0)

start_idx = 0
end_idx = len(data)
num_weeks = 15
lead = 2
num_students = end_idx / 15

dropout_value = 1 #bin value for a student dropped out

command_base = ["./HMM_EM", "PredictObservationDistribution", "./", str(lead)]

actual_dropouts = 0
predicted_dropouts = 0
lines_prev_count = 0
lines_prev = ""
command_prev = ""
command_prev_count = 0

predicted_list = []
labels_list = []

while start_idx < end_idx:	
	#for each student
	stud_data = data[start_idx:start_idx + num_weeks, :]

	# first check if student is even in lead weeks ahead
	if stud_data[0][0] == dropout_value:
		start_idx += num_weeks #move to next student because the student dropped out already! can't predict
		num_students -= 1
		continue

	X = stud_data[0: lead, :].flatten()
	truth_val = stud_data[lead][0]

	command = command_base + X.astype(str).tolist()
	results = subprocess.check_output( command)

	lines = results.split("\n")[0:-1]
	dropout_dist =  np.fromstring(lines[0], sep=";")
	
	if dropout_dist[dropout_value] > .7:
		predicted_dropouts+=1

	if truth_val == dropout_value:
		actual_dropouts+=1

	if lines_prev == lines:
		lines_prev_count+=1
	lines_prev = lines

	if command_prev == command:
		command_prev_count+=1
	command_prev = command

	labels_list.append(truth_val)
	predicted_list.append(dropout_dist[dropout_value])
	start_idx += num_weeks #move to next student

# print np.column_stack((labels_list, predicted_list))
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



print "predicted_dropouts", predicted_dropouts
print "actual_dropouts", actual_dropouts
print "num_students", num_students
print "lines_prev_count", lines_prev_count
print "command_prev_count", command_prev_count