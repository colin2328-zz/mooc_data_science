-- Takes 2 seconds to execute
-- Created on August 23, 2013
-- @author: Franck for ALFA, MIT lab: franck.dernoncourt@gmail.com
-- Feature 14: number of collaborations 

INSERT INTO moocdb.dropout_feature_values(dropout_feature_id, user_id, dropout_feature_value_week, dropout_feature_value)
	
SELECT 14, 	
	users.user_id, 
	FLOOR((UNIX_TIMESTAMP(collaborations.collaboration_timestamp) 
			- UNIX_TIMESTAMP('2012-03-05 12:00:00')) / (3600 * 24 * 7)) AS week,
	COUNT(*) 
FROM moocdb.users AS users
INNER JOIN moocdb.collaborations AS collaborations
 ON collaborations.user_id = users.user_id
WHERE users.user_dropout_week IS NOT NULL 
	AND FLOOR((UNIX_TIMESTAMP(collaborations.collaboration_timestamp) 
			- UNIX_TIMESTAMP('2012-03-05 12:00:00')) / (3600 * 24 * 7)) < 15
GROUP BY users.user_id, week
HAVING week < 15
AND week >= 0
;

