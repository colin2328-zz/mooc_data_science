''' 
Created on Nov 21, 2013
@author: Colin Taylor colin2328@gmail.com
Feature 201- number of forum responses per week (also known as CF1)
Requires that populate_feature_7_number_of_attempts.sql has already been run!
'''

from  scipy.stats import percentileofscore
import MySQLdb as mdb

def main():
	# connection=mdb.connect(user="root",passwd="edx2013",db="moocdb")
	# cursor = connection.cursor()

	data = [1, 2, 3, 4]
	print percentileofscore(data , 3)

	percentiles = [percentileofscore(data, i) for i in data]
	print percentiles

if __name__ == "__main__":
	main()