-- Takes 80 seconds to execute
-- Created on July 1, 2013
-- @author: Franck for ALFA, MIT lab: franck.dernoncourt@gmail.com
-- Feature 7: number of attempts
-- (supported by http://francky.me/mit/moocdb/all/forum_posts_per_day_date_labels_cutoff120_with_and_without_cert.html)

INSERT INTO moocdb.dropout_feature_values(dropout_feature_id, user_id, dropout_feature_value_week, dropout_feature_value)
	
SELECT 7, 	
	users.user_id, 
	FLOOR((UNIX_TIMESTAMP(submissions.submission_timestamp) 
			- UNIX_TIMESTAMP('2012-03-05 12:00:00')) / (3600 * 24 * 7)) AS week,
	COUNT(*)
FROM moocdb.users AS users
INNER JOIN moocdb.submissions AS submissions
 ON submissions.user_id = users.user_id
WHERE users.user_dropout_week IS NOT NULL 
	-- AND users.user_id < 100
	AND FLOOR((UNIX_TIMESTAMP(submissions.submission_timestamp) 
			- UNIX_TIMESTAMP('2012-03-05 12:00:00')) / (3600 * 24 * 7)) < 16
GROUP BY users.user_id, week
;

