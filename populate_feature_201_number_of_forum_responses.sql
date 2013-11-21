-- Created on Nov 21, 2013
-- @author: Colin Taylor colin2328@gmail.com
-- Feature 201- number of forum responses per week (also known as CF1)

INSERT INTO moocdb.dropout_feature_values(dropout_feature_id, user_id, dropout_feature_value_week, dropout_feature_value)
	
SELECT 201, 	
	users.user_id, 
	FLOOR((UNIX_TIMESTAMP(collaborations.collaboration_timestamp) 
			- UNIX_TIMESTAMP('2012-03-05 12:00:00')) / (3600 * 24 * 7)) AS week,
	COUNT(*) 
FROM moocdb.users AS users
INNER JOIN moocdb.collaborations AS collaborations
 ON collaborations.user_id = users.user_id
WHERE users.user_dropout_week IS NOT NULL 
	-- AND users.user_id < 100
	-- AND collaborations.collaboration_parent_id = 1 -- = 1 mean forum posts
	AND FLOOR((UNIX_TIMESTAMP(collaborations.collaboration_timestamp) 
			- UNIX_TIMESTAMP('2012-03-05 12:00:00')) / (3600 * 24 * 7)) < 16
GROUP BY users.user_id, week
;

