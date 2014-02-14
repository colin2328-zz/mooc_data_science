-- Created on Feb 14, 2014
-- @author: Colin Taylor colin2328@gmail.com
-- Feature 208- number of attempts that were correct 


INSERT INTO mock.dropout_feature_values(dropout_feature_id, user_id, dropout_feature_value_week, dropout_feature_value)
	
SELECT 208, 	
	users.user_id, 
	FLOOR((UNIX_TIMESTAMP(submissions.submission_timestamp) 
			- UNIX_TIMESTAMP('2012-03-05 12:00:00')) / (3600 * 24 * 7)) AS week,
	COUNT(*)
FROM mock.users AS users
INNER JOIN mock.submissions AS submissions
 ON submissions.user_id = users.user_id
INNER JOIN mock.assessments
 ON assessments.submission_id = submissions.submission_id
WHERE users.user_dropout_week IS NOT NULL
AND assessments.assessment_grade = 1
AND FLOOR((UNIX_TIMESTAMP(submissions.submission_timestamp) 
		- UNIX_TIMESTAMP('2012-03-05 12:00:00')) / (3600 * 24 * 7)) < 16
GROUP BY users.user_id, week
;