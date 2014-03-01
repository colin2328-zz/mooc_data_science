-- Takes 4 seconds to execute
-- Created on Jun 30, 2013
-- @author: Franck for ALFA, MIT lab: franck.dernoncourt@gmail.com
-- Edited by Colin Taylor on Nov 27, 2013 to include missing last submission id
-- Meant to be run after create_dropout_feature_values.sql is ran
DROP PROCEDURE IF EXISTS moocdb.AlterTable;
DELIMITER $$
CREATE PROCEDURE moocdb.AlterTable()
BEGIN
    DECLARE _count INT;
    SET _count = ( SELECT count(*) FROM INFORMATION_SCHEMA.COLUMNS 
                   WHERE TABLE_SCHEMA = 'moocdb' AND 
                         TABLE_NAME = 'users' AND 
                         COLUMN_NAME = 'user_dropout_week');
    IF _count = 0 THEN
    ALTER TABLE `moocdb`.`users` 
    ADD COLUMN `user_dropout_week` INT(2) NULL ;
    ALTER TABLE `moocdb`.`users` 
    ADD COLUMN `user_dropout_timestamp` DATETIME NULL ;
    ALTER TABLE `moocdb`.`users` 
    ADD COLUMN `user_last_submission_id` INT(11) NULL ;
    END IF;
END $$
DELIMITER ;

CALL moocdb.AlterTable();
DROP PROCEDURE IF EXISTS moocdb.AlterTable;

use `moocdb`;
UPDATE `moocdb`.`users` 
SET users.user_last_submission_id = (
    SELECT submission_id
    FROM submissions t1
    WHERE t1.submission_timestamp = (
        SELECT MAX(t2.submission_timestamp)
         FROM submissions t2
         WHERE t2.user_id = t1.user_id
    ) AND users.user_id = t1.user_id
)
;

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