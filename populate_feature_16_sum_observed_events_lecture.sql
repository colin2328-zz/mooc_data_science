-- Takes 1500 seconds to execute
-- Created on August 23, 2013
-- @author: Franck for ALFA, MIT lab: franck.dernoncourt@gmail.com
-- Feature 16: Total time spent on all resources - lecture only - during the week
-- edited by Colin Taylor to include correct resource_type

INSERT INTO moocdb.dropout_feature_values(dropout_feature_id, user_id, dropout_feature_value_week, dropout_feature_value)
	
SELECT 16, 	
	users.user_id, 
	FLOOR((UNIX_TIMESTAMP(observed_events.observed_event_timestamp) 
			- UNIX_TIMESTAMP('2012-03-05 12:00:00')) / (3600 * 24 * 7)) AS week,
	SUM(observed_events.observed_event_duration)
FROM moocdb.users AS users
INNER JOIN moocdb.observed_events AS observed_events
 ON observed_events.user_id = users.user_id
INNER JOIN moocdb.resources AS resources
 ON resources.resource_id = observed_events.resource_id
INNER JOIN moocdb.resource_types AS resource_types
 ON resource_types.resource_type_id = resources.resource_type_id
WHERE users.user_dropout_week IS NOT NULL 
	-- AND users.user_id < 100
	AND resource_types.resource_type_id = 1 -- 1 is lecture
	AND FLOOR((UNIX_TIMESTAMP(observed_events.observed_event_timestamp) 
			- UNIX_TIMESTAMP('2012-03-05 12:00:00')) / (3600 * 24 * 7)) < 16
GROUP BY users.user_id, week
HAVING week < 16
AND week > 0
;

