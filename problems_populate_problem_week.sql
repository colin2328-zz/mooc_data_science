-- Created on Jan 30, 204
-- @author:  Colin Taylor
-- Populate problem_week field of problems table
-- Meant to be run in order to run before pset feature scripts, such as feature_204

DROP PROCEDURE IF EXISTS mock.AlterTable;
DELIMITER $$
CREATE PROCEDURE mock.AlterTable()
BEGIN
    DECLARE _count INT;
    SET _count = ( SELECT count(*) FROM INFORMATION_SCHEMA.COLUMNS 
                   WHERE TABLE_SCHEMA = 'mock' AND 
                         TABLE_NAME = 'problems' AND 
                         COLUMN_NAME = 'problem_week');
    IF _count = 0 THEN
    ALTER TABLE `mock`.`problems` 
    ADD COLUMN `problem_week` INT(11) NULL ;
    END IF;
END $$
DELIMITER ;

CALL mock.AlterTable();
DROP PROCEDURE IF EXISTS mock.AlterTable;

UPDATE mock.problems AS a
  INNER JOIN mock.problems AS b ON b.problem_id = a.problem_id
  SET a.problem_week = FLOOR((UNIX_TIMESTAMP(b.problem_hard_deadline) - UNIX_TIMESTAMP('2012-03-18 12:00:00')) / (3600 * 24 * 7)) + 1
