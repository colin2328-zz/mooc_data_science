-- Takes 2 seconds to execute
-- Created on June 30, 2013
-- @author: Franck for ALFA, MIT lab: franck.dernoncourt@gmail.com
-- Feature 3: number of forum posts
-- (supported by http://francky.me/mit/moocdb/all/forum_posts_per_day_date_labels_cutoff120_with_and_without_cert.html)

INSERT INTO moocdb.dropout_feature_values(dropout_feature_id, user_id, dropout_feature_value_week, dropout_feature_value)
	
SELECT 3, 	
	users.user_id, 
	FLOOR((UNIX_TIMESTAMP(collaborations.collaboration_timestamp) 
			- UNIX_TIMESTAMP('2012-03-05 12:00:00')) / (3600 * 24 * 7)) AS week,
	COUNT(*) 
FROM moocdb.users AS users
INNER JOIN moocdb.collaborations AS collaborations
 ON collaborations.user_id = users.user_id
WHERE users.user_dropout_week IS NOT NULL 
	-- AND users.user_id < 100
	AND collaborations.collaboration_parent_id = 1 -- = 1 mean forum posts
	AND FLOOR((UNIX_TIMESTAMP(collaborations.collaboration_timestamp) 
			- UNIX_TIMESTAMP('2012-03-05 12:00:00')) / (3600 * 24 * 7)) < 16
GROUP BY users.user_id, week
;

