-- Takes 100 seconds to execute IF THE FOLLOWING INDEX IS CREATED (will take forever otherwise)
-- Created on Jun 27, 2013
-- @author: Franck Dernoncourt for ALFA, MIT lab: franck.dernoncourt@gmail.com

-- First create index:  (takes 250 seconds to run)
-- ALTER TABLE `mock`.`submissions` 
-- ADD INDEX `user-timestamp_idx` (`user_id` ASC, `submission_timestamp` ASC) ;

DROP PROCEDURE IF EXISTS mock.Alter_Table;

DELIMITER $$
CREATE PROCEDURE mock.Alter_Table()
BEGIN

	DECLARE _count INT;

	SET _count = (  SELECT COUNT(*) 
						FROM INFORMATION_SCHEMA.COLUMNS
						WHERE   TABLE_SCHEMA = 'mock' AND
								TABLE_NAME = 'users' AND 
								COLUMN_NAME = 'user_last_submission_id');

	IF _count = 0 THEN
		ALTER TABLE `mock`.`users` 
			ADD COLUMN `user_last_submission_id` INT(11) NULL;
	END IF;

	UPDATE mock.users AS users
		SET users.user_last_submission_id = (
			SELECT 
				submissions.submission_id
			FROM
				mock.submissions AS submissions
			WHERE
				users.user_id = submissions.user_id
-- 					AND users.user_id < 1000
					AND submissions.submission_timestamp = (SELECT 
						MAX(submissions.submission_timestamp)
					FROM
						mock.submissions AS submissions
					WHERE
						users.user_id = submissions.user_id)
			GROUP BY submissions.user_id

		);


END $$
DELIMITER ;

CALL mock.Alter_Table();
DROP PROCEDURE IF EXISTS mock.Alter_Table;
