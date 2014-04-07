import numpy as np
import subprocess

in_file = "features_bin_cut.csv"
data = np.genfromtxt(in_file, delimiter = ',', skip_header = 0)

start_idx = 0
end_idx = len(data)
num_weeks = 15
lead = 4
num_students = end_idx / 15

dropout_value = 4 #bin value for a student dropped out

command_base = ["./HMM_EM", "PredictObservationDistribution", "./", str(lead)]

actual_dropouts = 0
predicted_dropouts = 0
lines_prev_count = 0
lines_prev = ""
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
	print " ".join(command)
	results = subprocess.check_output( command)

	lines = results.split("\n")[0:-1]
	# print lines[0]
	if lines[0] < .5:
		predicted_dropouts+=1
	if truth_val == dropout_value:
		actual_dropouts+=1

	if lines_prev == lines:
		lines_prev_count+=1
	lines_prev = lines


	start_idx += num_weeks #move to next student
	# start_idx = end_idx

print predicted_dropouts, actual_dropouts, num_students, lines_prev_count