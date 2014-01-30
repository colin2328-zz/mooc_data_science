-- Takes 2700 seconds to execute
-- Created on August 23, 2013
-- @author: Franck for ALFA, MIT lab: franck.dernoncourt@gmail.com
-- Feature 15: Duration of longest observed event

INSERT INTO mock.dropout_feature_values(dropout_feature_id, user_id, dropout_feature_value_week, dropout_feature_value)
	
SELECT 15, 	
	users.user_id, 
	FLOOR((UNIX_TIMESTAMP(observed_events.observed_event_timestamp) 
			- UNIX_TIMESTAMP('2012-03-05 12:00:00')) / (3600 * 24 * 7)) AS week,
	MAX(observed_events.observed_event_duration)
FROM mock.users AS users
INNER JOIN mock.observed_events AS observed_events
 ON observed_events.user_id = users.user_id
WHERE users.user_dropout_week IS NOT NULL 
	-- AND users.user_id < 100
	AND FLOOR((UNIX_TIMESTAMP(observed_events.observed_event_timestamp) 
			- UNIX_TIMESTAMP('2012-03-05 12:00:00')) / (3600 * 24 * 7)) < 16
GROUP BY users.user_id, week
;

