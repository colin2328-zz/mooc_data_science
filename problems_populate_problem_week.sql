-- Created on Jan 30, 204
-- @author:  Colin Taylor
-- Populate problem_week field of problems table
-- Meant to be run in order to run before pset feature scripts, such as feature_204

DROP PROCEDURE IF EXISTS moocdb.AlterTable;
DELIMITER $$
CREATE PROCEDURE moocdb.AlterTable()
BEGIN
    DECLARE _count INT;
    SET _count = ( SELECT count(*) FROM INFORMATION_SCHEMA.COLUMNS 
                   WHERE TABLE_SCHEMA = 'moocdb' AND 
                         TABLE_NAME = 'problems' AND 
                         COLUMN_NAME = 'problem_week');
    IF _count = 0 THEN
    ALTER TABLE `moocdb`.`problems` 
    ADD COLUMN `problem_week` INT(11) NULL ;
    END IF;
END $$
DELIMITER ;

CALL moocdb.AlterTable();
DROP PROCEDURE IF EXISTS moocdb.AlterTable;

UPDATE moocdb.problems AS a
  INNER JOIN moocdb.problems AS b ON b.problem_id = a.problem_id
  SET a.problem_week = FLOOR((UNIX_TIMESTAMP(b.problem_hard_deadline) - UNIX_TIMESTAMP('2012-03-18 12:00:00')) / (3600 * 24 * 7)) + 1
