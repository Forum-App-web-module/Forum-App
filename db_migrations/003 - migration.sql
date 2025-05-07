ALTER TABLE `forum_app`.`messages` 
CHANGE COLUMN `sent_on` `sent_on` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP;

ALTER TABLE `forum_app`.`messages` 
DROP INDEX `receiver_id_UNIQUE` ,
DROP INDEX `sender_id_UNIQUE` ;