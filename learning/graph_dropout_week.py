import numpy as np
import pylab as pl

def graph_dropout_week(in_file):
	dropout_weeks = np.genfromtxt(in_file, delimiter = ',', skip_header = 1, usecols=(1))
	n = 16
	ax = pl.gca()
	pl.hist(dropout_weeks,bins=range(0,n+1))
	pl.ylabel('Number of students')
	pl.xlabel('Stopout week')
	pl.title("Stopout week for all 6.002x students")
	

	ax.set_xticks(range(1, n))
	ax.set_xticklabels(range(1,n),ha='center')
	ax.set_xlim([1,16])
	
	pl.show()

if __name__ == "__main__":
	in_file = "results/dropout_week_features.csv"
	graph_dropout_week(in_file)