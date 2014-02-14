-- Created on Feb 14, 2014
-- @author: Colin Taylor colin2328@gmail.com
-- Feature 209- Percentage of total submissions that were correct (feature 208 / feature 7)
-- Must have run populate_feature_208 and populate_feature_7 first!

INSERT INTO mock.dropout_feature_values(dropout_feature_id, user_id, dropout_feature_value_week, dropout_feature_value)
	
SELECT 209, 	
	dropout_feature_values.user_id, 
	dropout_feature_values.dropout_feature_value_week,
	dropout_feature_values2.dropout_feature_value  / dropout_feature_values.dropout_feature_value
FROM mock.dropout_feature_values AS dropout_feature_values,
	mock.dropout_feature_values AS dropout_feature_values2
WHERE dropout_feature_values.user_id = dropout_feature_values2.user_id
	AND dropout_feature_values.dropout_feature_value_week = dropout_feature_values2.dropout_feature_value_week 
	AND dropout_feature_values.dropout_feature_id = 7
	AND dropout_feature_values2.dropout_feature_id = 208
;
