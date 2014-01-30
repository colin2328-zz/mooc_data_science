-- Takes 8 seconds to execute
-- Created on July 6, 2013
-- @author: Franck for ALFA, MIT lab: franck.dernoncourt@gmail.com

SELECT dropout_feature_values.dropout_feature_id, COUNT(*)
FROM mock.dropout_feature_values AS dropout_feature_values
 INNER JOIN mock.users AS users
 ON users.user_id = dropout_feature_values.user_id
WHERE users.user_dropout_week > 2 
GROUP BY dropout_feature_values.dropout_feature_id
ORDER BY dropout_feature_values.dropout_feature_id ASC
;