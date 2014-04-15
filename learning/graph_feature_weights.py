import numpy as np
import csv

in_file = "results/logistic_regression_results_weights.csv"
datareader = csv.reader(open(in_file, 'r'))
data = None
num_features = 27

def add_to_data(old_data, new_data):
	if old_data == None:
		return new_data
	else:
		return np.vstack((old_data, new_data))

for row in datareader:
	new_data = np.array([ float(elem) for elem in row])
	length = len(new_data)
	new_data = np.reshape(new_data, ( length / num_features, num_features))
	data = add_to_data(data, new_data)

number_mean_std = None
for col_number in range(num_features):
	col_values = data[:, col_number]
	number_mean_std = add_to_data(number_mean_std, [col_number + 2, np.mean(col_values), np.std(col_values)])

number_mean_std = number_mean_std[number_mean_std[:,1].argsort()]


print number_mean_std