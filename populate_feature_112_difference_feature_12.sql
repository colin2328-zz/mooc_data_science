-- Takes 8 seconds to execute
-- Created on July 2, 2013
-- @author: Franck for ALFA, MIT lab: franck.dernoncourt@gmail.com
-- Feature 112: difference of Feature 12 (number of problem attempted (feature 6) / number of correct problems (feature 8))
-- 130667 rows

INSERT INTO moocdb.dropout_feature_values(dropout_feature_id, user_id, dropout_feature_value_week, dropout_feature_value)

SELECT 112, 	
	dropout_feature_values.user_id, 
	dropout_feature_values2.dropout_feature_value_week,
	-- dropout_feature_values.dropout_feature_value,
	-- dropout_feature_values2.dropout_feature_value,
	dropout_feature_values2.dropout_feature_value  / dropout_feature_values.dropout_feature_value
FROM moocdb.dropout_feature_values AS dropout_feature_values,
	moocdb.dropout_feature_values AS dropout_feature_values2
WHERE 
	-- same user
	dropout_feature_values.user_id = dropout_feature_values2.user_id
	-- 2 successive weeks
	AND dropout_feature_values.dropout_feature_value_week = dropout_feature_values2.dropout_feature_value_week - 1
	-- we are only interested in feature 5 (average length of forum posts)
	AND dropout_feature_values.dropout_feature_id = 12
	AND dropout_feature_values2.dropout_feature_id = 12

-- LIMIT 1000