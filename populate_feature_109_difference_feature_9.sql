-- Takes 7 seconds to execute
-- Created on July 2, 2013
-- @author: Franck for ALFA, MIT lab: franck.dernoncourt@gmail.com
-- Feature 109: difference of Feature 9 (Average number of attempts)
-- 130600 rows

INSERT INTO mock.dropout_feature_values(dropout_feature_id, user_id, dropout_feature_value_week, dropout_feature_value)

SELECT 109, 	
	dropout_feature_values.user_id, 
	dropout_feature_values2.dropout_feature_value_week,
	-- dropout_feature_values.dropout_feature_value,
	-- dropout_feature_values2.dropout_feature_value,
	dropout_feature_values2.dropout_feature_value  / dropout_feature_values.dropout_feature_value
FROM mock.dropout_feature_values AS dropout_feature_values,
	mock.dropout_feature_values AS dropout_feature_values2

WHERE 
	-- same user
	dropout_feature_values.user_id = dropout_feature_values2.user_id
	-- 2 successive weeks
	AND dropout_feature_values.dropout_feature_value_week = dropout_feature_values2.dropout_feature_value_week - 1
	-- we are only interested in feature 9
	AND dropout_feature_values.dropout_feature_id = 9
	AND dropout_feature_values2.dropout_feature_id = 9

-- LIMIT 1000