-- Takes 60 seconds to execute (depends on how many features we have)
-- Created on July 2, 2013
-- @author: Franck for ALFA, MIT lab: franck.dernoncourt@gmail.com
-- Shift all week number by -1


UPDATE moocdb.dropout_feature_values AS dropout_feature_values
SET dropout_feature_values.dropout_feature_value_week = dropout_feature_values.dropout_feature_value_week - 1
