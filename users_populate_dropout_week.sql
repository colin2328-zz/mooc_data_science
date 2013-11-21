-- Takes 4 seconds to execute
-- Created on Jun 30, 2013
-- @author: Franck for ALFA, MIT lab: franck.dernoncourt@gmail.com

ALTER TABLE `moocdb`.`users` 
ADD COLUMN `user_dropout_week` INT(2) NULL ;

ALTER TABLE `moocdb`.`users` 
ADD COLUMN `user_dropout_timestamp` DATETIME NULL ;

-- Takes 2 seconds to execute
UPDATE `moocdb`.`users` 
SET users.user_dropout_week = (
	SELECT FLOOR((UNIX_TIMESTAMP(submissions.submission_timestamp) - UNIX_TIMESTAMP('2012-03-05 12:00:00')) / (3600 * 24 * 7)) + 1 AS week
	FROM moocdb.submissions AS submissions
	WHERE submissions.submission_id = users.user_last_submission_id	
)
;

-- Takes 2 seconds to execute
UPDATE `moocdb`.`users` 
SET users.user_dropout_timestamp = (
	SELECT submissions.submission_timestamp
	FROM moocdb.submissions AS submissions
	WHERE submissions.submission_id = users.user_last_submission_id	
)
;