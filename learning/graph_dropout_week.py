import numpy as np
import pylab as pl

def graph_dropout_week(in_file):
	dropout_weeks = np.genfromtxt(in_file, delimiter = ',', skip_header = 1, usecols=(1))

	# pl.hist(dropout_weeks,bins=np.arange(16))
	# pl.ylabel('Students')
	# pl.xlabel('Stopout week')
	# pl.title("Stopout week for all 6.002x students")
	# pl.clf()
	
	pl.plot(np.arange(len(dropout_weeks)), dropout_weeks, 'r')
	pl.show()

if __name__ == "__main__":
	in_file = "results/dropout_week_features.csv"
	graph_dropout_week(in_file)