-- Takes 1 seconds to execute
-- Created on Jun 30, 2013
-- @author: Franck for ALFA, MIT lab: franck.dernoncourt@gmail.com

DROP TABLE if exists `mock`.`dropout_feature_values`;

CREATE TABLE `mock`.`dropout_feature_values` (
  `dropout_feature_value_id` INT NOT NULL AUTO_INCREMENT ,  
  `dropout_feature_id` INT(3) NULL ,
  `user_id` INT(6) NULL ,
  `dropout_feature_value_week` INT(2) NULL ,
  `dropout_feature_value` DOUBLE NULL ,
  PRIMARY KEY (`dropout_feature_value_id`) );

ALTER TABLE `mock`.`dropout_feature_values` CHANGE COLUMN `dropout_feature_id` `dropout_feature_id` INT(3) NULL  
, ADD INDEX `dropout_feature_id_idx` (`dropout_feature_id` ASC) ;

ALTER TABLE `mock`.`dropout_feature_values` 
ADD INDEX `user_week_idx` (`user_id` ASC, `dropout_feature_value_week` ASC) ;