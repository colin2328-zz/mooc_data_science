-- Created on Feb 3rd, 2014
-- @author:  Colin Taylor
-- Feature 205: Pset Grade over time: pset grade - avg (pset grade from previos weeks)
-- Meant to be run in order to run after populate_feature_204_pset_grade.sql

use moocdb;

DELIMITER $$
DROP PROCEDURE IF EXISTS Populate_205$$
CREATE PROCEDURE Populate_205()
	BEGIN
		DECLARE x  INT;
		SET x = 1;
		WHILE x  <= 13 DO
			INSERT INTO moocdb.dropout_feature_values(dropout_feature_id, user_id, dropout_feature_value_week, dropout_feature_value)
			SELECT 205, d1.user_id, x AS week, d1.dropout_feature_value -
				(SELECT AVG(dropout_feature_value)
				FROM moocdb.dropout_feature_values AS d2 WHERE dropout_feature_id = 204 AND dropout_feature_value_week < x AND d1.user_id = d2.user_id)
			FROM dropout_feature_values AS d1 WHERE dropout_feature_id = 204 AND dropout_feature_value_week = x;
			SET  x = x + 1; 
		END WHILE;
	END$$
DELIMITER ;

CALL Populate_205();
DROP PROCEDURE IF EXISTS Populate_205

