'''
Created on July 02, 2013

@author: Colin for ALFA, MIT lab: colin2328@gmail.com

Modifications:
 2013-07-04 - Franck Dernoncourt - franck.dernoncourt@gmail.com - fixed a few typos + add a TODO which needs to be fixed

'''

import MySQLdb as mdb
import math


def main():
	connection=mdb.connect(user="root",passwd="edx2013",db="mock")
	cursor = connection.cursor()

	connection2=mdb.connect(user="root",passwd="edx2013",db="mock")
	cursor2 = connection2.cursor()

	#get all the observed events times for a user for a week
	print "Executing query (get all the observed events times for a user for a week)"
	sql = '''SELECT observed_events.user_id, FLOOR((UNIX_TIMESTAMP(observed_events.observed_event_timestamp) 
			- UNIX_TIMESTAMP('2012-03-05 12:00:00')) / (3600 * 24 * 7)) 
			AS week, observed_event_timestamp
			FROM mock.observed_events AS observed_events
			GROUP BY observed_events.user_id, week, observed_event_timestamp ASC
			'''

	cursor.execute(sql)

	print "Starting parsing results"

	sql2 = '''SELECT observed_events.user_id, FLOOR((UNIX_TIMESTAMP(observed_events.observed_event_timestamp) 
			- UNIX_TIMESTAMP('2012-03-05 12:00:00')) / (3600 * 24 * 7)) 
			AS week, observed_event_timestamp
			FROM mock.observed_events AS observed_events
			GROUP BY observed_events.user_id, week, observed_event_timestamp ASC
			LIMIT 1
			'''
	cursor2.execute(sql2)
	first = cursor2.fetchone()
	times = []
	old_week = first[1]
	old_user_id = first[0]

	for i in range(cursor.rowcount):
		row = cursor.fetchone()
		user_id = row[0]
		week = row[1]
		timestamp = row[2]

		if (week != old_week or user_id != old_user_id):
			#if either have changed, compute entropy for list, insert entropy into database, and clear list before adding
			entropy = compute_deviation(times)
			insert_deviation(entropy, user_id, week, cursor2, connection2)
			times = []

		time = timestamp.time()
		seconds = ((time.hour * 60 + time.minute) * 60) + time.second
		times.append(seconds)
		old_week = week
		old_user_id = user_id

	entropy = compute_deviation(times)

	print "Inserting new feature"
	insert_deviation(entropy, user_id, week, cursor2, connection2)
	connection.close()

def compute_deviation(times):
	mean = sum(times, 0.0) / len(times)
	d = [(i - mean) ** 2 for i in times]
	std_dev = math.sqrt(sum(d) / len(d))
	return std_dev

def insert_deviation(entropy, user_id, week, cursor, connection):
	sql = '''INSERT INTO mock.dropout_feature_values(dropout_feature_id, user_id, dropout_feature_value_week, dropout_feature_value)
	VALUES (13, %s, %s, %s)
	''' % (user_id, week, entropy)
	cursor.execute(sql)
	connection.commit()

if __name__ == "__main__":
	main()
