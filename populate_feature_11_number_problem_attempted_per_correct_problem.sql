-- Takes 10 seconds to execute (if index below is created!)
-- Created on July 1, 2013
-- @author: Franck for ALFA, MIT lab: franck.dernoncourt@gmail.com
-- Feature 11: number of problem attempted (feature 6) / number of correct problems (feature 8)


-- You need to create this index, otherwise it will take for ever
-- Takes 10 seconds to execute
-- ALTER TABLE `moocdb`.`dropout_feature_values` 
-- ADD INDEX `user_week_idx` (`user_id` ASC, `dropout_feature_value_week` ASC) ;


INSERT INTO moocdb.dropout_feature_values(dropout_feature_id, user_id, dropout_feature_value_week, dropout_feature_value)
	
SELECT 11, 	
	dropout_feature_values.user_id, 
	dropout_feature_values.dropout_feature_value_week,
	dropout_feature_values2.dropout_feature_value  / dropout_feature_values.dropout_feature_value
FROM moocdb.dropout_feature_values AS dropout_feature_values,
	moocdb.dropout_feature_values AS dropout_feature_values2
WHERE dropout_feature_values.user_id = dropout_feature_values2.user_id
	AND dropout_feature_values.dropout_feature_value_week = dropout_feature_values2.dropout_feature_value_week 
	AND dropout_feature_values.dropout_feature_id = 8
	AND dropout_feature_values2.dropout_feature_id = 6
HAVING week < 16
AND week > 0
;

