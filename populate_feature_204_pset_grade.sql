-- Created on Jan 31, 204
-- @author:  Colin Taylor
-- Feature 204: Pset Grade: Number of homework problems correct in a week's problems / number of homework problems in a week
-- Meant to be run in order to run after problem_populate_module_week.sql

use mock;
INSERT INTO mock.dropout_feature_values(dropout_feature_id, user_id, dropout_feature_value_week, dropout_feature_value)

SELECT 204, submissions.user_id, problems.problem_week + 1 AS week_number, COUNT(*) /
	(SELECT COUNT(*)  FROM problems AS p2 WHERE p2.problem_type_id = 1 
		AND p2.problem_week = problems.problem_week GROUP BY problem_week) AS pset_grade
FROM submissions, problems, assessments 
WHERE submissions.problem_id = problems.problem_id AND problem_type_id = 1 
AND assessments.submission_id = submissions.submission_id AND assessments.assessment_grade = 0
GROUP BY submissions.user_id, problems.problem_week;