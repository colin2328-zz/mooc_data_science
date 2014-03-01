-- Takes 1000 seconds to execute 
-- Created on July 2, 2013
-- @author: Franck for ALFA, MIT lab: franck.dernoncourt@gmail.com
-- Feature 12: average(max(attempt.timestamp) - min(attempt.timestamp) for each problem in a week) 
-- 196966 rows

INSERT INTO moocdb.dropout_feature_values(dropout_feature_id, user_id, dropout_feature_value_week, dropout_feature_value)

SELECT 12, 	
	users.user_id, 
	FLOOR((UNIX_TIMESTAMP(submissions.submission_timestamp) 
			- UNIX_TIMESTAMP('2012-03-05 12:00:00')) / (3600 * 24 * 7)) AS week,
	AVG(submissions.submission_attempt_number - submissions3.submission_attempt_number)
FROM moocdb.users AS users
INNER JOIN moocdb.submissions AS submissions
 ON submissions.user_id = users.user_id
INNER JOIN moocdb.submissions AS submissions3
 ON submissions3.user_id = users.user_id
	AND submissions3.problem_id = submissions.problem_id
WHERE users.user_dropout_week IS NOT NULL 
	AND submissions.submission_attempt_number = (
			SELECT MAX(submissions2.submission_attempt_number)
			FROM moocdb.submissions AS submissions2
			WHERE submissions2.problem_id = submissions.problem_id
				AND submissions2.user_id = submissions.user_id
		)
	AND submissions3.submission_attempt_number = (
			SELECT MIN(submissions2.submission_attempt_number)
			FROM moocdb.submissions AS submissions2
			WHERE submissions2.problem_id = submissions.problem_id
				AND submissions2.user_id = submissions.user_id
		)
	-- AND users.user_id <  1000
	AND FLOOR((UNIX_TIMESTAMP(submissions.submission_timestamp) 
			- UNIX_TIMESTAMP('2012-03-05 12:00:00')) / (3600 * 24 * 7)) < 16
	
GROUP BY users.user_id, week
HAVING week < 16
AND week > 0
;
