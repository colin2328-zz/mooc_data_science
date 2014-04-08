import numpy as np
import pylab as pl

in_file = "dropout_week.csv"
dropout_weeks = np.genfromtxt(in_file, delimiter = ',', skip_header = 1, usecols=(1))

pl.hist(dropout_weeks,bins=np.arange(16))
pl.ylabel('Students')
pl.xlabel('Stopout week')
pl.title("Stopout week for all 6.002x students")
pl.show()
