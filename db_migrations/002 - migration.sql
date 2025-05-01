ALTER TABLE `forum_app`.`category_members`
DROP FOREIGN KEY `fk_category_members_categories1`,
DROP FOREIGN KEY `fk_category_members_users1`;

ALTER TABLE `forum_app`.`topics`
DROP FOREIGN KEY `fk_topics_categories1`;

ALTER TABLE `forum_app`.`votes`
DROP FOREIGN KEY `fk_votes_replies1`,
DROP FOREIGN KEY `fk_votes_users1`;

ALTER TABLE `forum_app`.`categories`
CHANGE COLUMN `is_private` `is_private` TINYINT(4) NULL DEFAULT 0 ,
CHANGE COLUMN `lock` `locked` TINYINT(4) NULL DEFAULT 0 ;

ALTER TABLE `forum_app`.`category_members`
CHANGE COLUMN `categories_id` `category_id` INT(11) NOT NULL ,
CHANGE COLUMN `users_id` `user_id` INT(11) NOT NULL ,
CHANGE COLUMN `can_write` `can_write` TINYINT(4) NULL DEFAULT 0 ;

ALTER TABLE `forum_app`.`messages`
CHANGE COLUMN `sent_on` `sent_on` DATETIME NOT NULL ;

ALTER TABLE `forum_app`.`topics`
CHANGE COLUMN `categories_id` `category_id` INT(11) NOT NULL ,
CHANGE COLUMN `lock` `locked` TINYINT(4) NULL DEFAULT 0 ;

ALTER TABLE `forum_app`.`votes`
CHANGE COLUMN `replies_id` `reply_id` INT(11) NOT NULL ,
CHANGE COLUMN `users_id` `user_id` INT(11) NOT NULL ;

ALTER TABLE `forum_app`.`category_members`
ADD CONSTRAINT `fk_category_members_categories1`
  FOREIGN KEY (`category_id`)
  REFERENCES `forum_app`.`categories` (`id`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION,
ADD CONSTRAINT `fk_category_members_users1`
  FOREIGN KEY (`user_id`)
  REFERENCES `forum_app`.`users` (`id`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;

ALTER TABLE `forum_app`.`topics`
ADD CONSTRAINT `fk_topics_categories1`
  FOREIGN KEY (`category_id`)
  REFERENCES `forum_app`.`categories` (`id`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;

ALTER TABLE `forum_app`.`votes`
ADD CONSTRAINT `fk_votes_replies1`
  FOREIGN KEY (`reply_id`)
  REFERENCES `forum_app`.`replies` (`id`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION,
ADD CONSTRAINT `fk_votes_users1`
  FOREIGN KEY (`user_id`)
  REFERENCES `forum_app`.`users` (`id`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;