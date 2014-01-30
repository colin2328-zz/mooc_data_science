-- Takes 12 seconds 
-- Created on June 30, 2013
-- @author: Franck for ALFA, MIT lab: franck.dernoncourt@gmail.com
-- Feature 1: has the student dropped out (binary, that's what we try to predict)
-- Edited by Colin Taylor on Nov 27, 2013 to include missing last submission id
-- Meant to be run after users_populate_dropout_week.sql is run

TRUNCATE TABLE mock.dropout_feature_values;
ALTER TABLE mock.dropout_feature_values AUTO_INCREMENT = 1;

drop procedure if exists mock.compute_feature_1;

delimiter $$

create procedure mock.compute_feature_1()
begin

-- http://stackoverflow.com/questions/5125096/for-loop-in-mysql
declare v_max int unsigned default 16;
declare v_counter int unsigned default 0;

  -- start transaction;
  while v_counter < v_max do
    
	-- 
	INSERT INTO mock.dropout_feature_values(dropout_feature_id, user_id, dropout_feature_value_week, dropout_feature_value)
	SELECT 1, users.user_id, v_counter, 0 
	FROM mock.users AS users
	WHERE users.user_dropout_week <= v_counter
		AND users.user_dropout_week IS NOT NULL 
	-- AND user_id < 100
	;

	INSERT INTO mock.dropout_feature_values(dropout_feature_id, user_id, dropout_feature_value_week, dropout_feature_value)
	SELECT 1, users.user_id, v_counter, 1 
	FROM mock.users AS users
	WHERE users.user_dropout_week > v_counter
		AND users.user_dropout_week  IS NOT NULL 
	-- AND user_id < 100
	;
	


    set v_counter=v_counter+1;
  end while;
  -- commit;
end $$

delimiter ;

call mock.compute_feature_1();
drop procedure if exists mock.compute_feature_1;