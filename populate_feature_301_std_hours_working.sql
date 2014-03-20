## time the script takes to run on moocdb db:  xx seconds
## date:  12/10/2013
## author: Josep Marc Mingot  
## email:  jm.mingot@gmail.com
## description of feature:
## Standard deviation of the hours the user produces events and collaborations. 
## Pretends to capture how regular a student is in her schedule while doing a MOOC
## name for feature: std_hours_working
## would you like to be cited, and if so, how?
##
## Modified by Colin Taylor (3/5/2014) to insert into database with feature number 301

use moocdb
INSERT INTO moocdb.dropout_feature_values(dropout_feature_id, user_id, dropout_feature_value_week, dropout_feature_value)
SELECT 301,
	user_id,
	FLOOR((UNIX_TIMESTAMP(event_timestamp) - UNIX_TIMESTAMP('2012-03-05 12:00:00')) / (3600 * 24 * 7)) AS week,
	std(hours) AS std_hours_working
	
FROM
	(SELECT 
		user_id,
			hour(observed_event_timestamp) AS hours,
			observed_event_timestamp as event_timestamp
	FROM
		moocdb.observed_events UNION ALL SELECT 
		user_id,
			hour(collaboration_timestamp) AS hours,
			collaboration_timestamp as event_timestamp
	FROM
		collaborations) AS A
GROUP BY user_id , week
;