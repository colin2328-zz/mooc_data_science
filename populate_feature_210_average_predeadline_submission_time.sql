-- Created on Feb 17, 2014
-- @author: Colin Taylor colin2328@gmail.com
-- Feature 210- Average time between problem submission and problem due date (in seconds)

INSERT INTO mock.dropout_feature_values(dropout_feature_id, user_id, dropout_feature_value_week, dropout_feature_value)
	
SELECT 210,
	users.user_id,
	FLOOR((UNIX_TIMESTAMP(submissions.submission_timestamp) 
			- UNIX_TIMESTAMP('2012-03-05 12:00:00')) / (3600 * 24 * 7)) AS week,
	AVG((UNIX_TIMESTAMP(submissions.submission_timestamp) 
			- UNIX_TIMESTAMP(problems.problem_hard_deadline))) AS time_difference
FROM mock.submissions
INNER JOIN mock.users
	ON submissions.user_id = users.user_id
INNER JOIN mock.problems
	ON submissions.problem_id = problems.problem_id
AND users.user_dropout_week IS NOT NULL
GROUP BY users.user_id, week
HAVING week < 15
AND week > 0;