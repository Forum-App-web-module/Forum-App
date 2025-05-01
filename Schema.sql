-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema forum_app
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema forum_app
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `forum_app` DEFAULT CHARACTER SET latin1 ;
USE `forum_app` ;

-- -----------------------------------------------------
-- Table `forum_app`.`categories`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forum_app`.`categories` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `is_private` TINYINT NULL DEFAULT 0,
  `locked` TINYINT NULL DEFAULT 0,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 2
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `forum_app`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forum_app`.`users` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(15) NOT NULL,
  `email` VARCHAR(40) NOT NULL,
  `password` VARCHAR(65) NOT NULL,
  `bio` VARCHAR(150) NULL DEFAULT NULL,
  `is_admin` TINYINT(4) NULL DEFAULT 0,
  `is_active` TINYINT(4) NULL DEFAULT 1,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `username_UNIQUE` (`username` ASC) VISIBLE,
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE)
ENGINE = InnoDB
AUTO_INCREMENT = 3
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `forum_app`.`category_members`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forum_app`.`category_members` (
  `category_id` INT(11) NOT NULL,
  `user_id` INT(11) NOT NULL,
  `can_write` TINYINT NULL DEFAULT 0,
  PRIMARY KEY (`category_id`, `user_id`),
  UNIQUE INDEX `categories_id_UNIQUE` (`category_id` ASC) VISIBLE,
  UNIQUE INDEX `users_id_UNIQUE` (`user_id` ASC) VISIBLE,
  INDEX `fk_category_members_categories1_idx` (`category_id` ASC) VISIBLE,
  INDEX `fk_category_members_users1_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_category_members_categories1`
    FOREIGN KEY (`category_id`)
    REFERENCES `forum_app`.`categories` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_category_members_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `forum_app`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `forum_app`.`messages`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forum_app`.`messages` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `text` VARCHAR(200) NOT NULL,
  `sent_on` DATETIME NOT NULL,
  `sender_id` INT(11) NOT NULL,
  `receiver_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `sender_id_UNIQUE` (`sender_id` ASC) VISIBLE,
  UNIQUE INDEX `receiver_id_UNIQUE` (`receiver_id` ASC) VISIBLE,
  INDEX `fk_messages_users1_idx` (`sender_id` ASC) VISIBLE,
  INDEX `fk_messages_users2_idx` (`receiver_id` ASC) VISIBLE,
  CONSTRAINT `fk_messages_users1`
    FOREIGN KEY (`sender_id`)
    REFERENCES `forum_app`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_messages_users2`
    FOREIGN KEY (`receiver_id`)
    REFERENCES `forum_app`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `forum_app`.`topics`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forum_app`.`topics` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(45) NOT NULL,
  `category_id` INT(11) NOT NULL,
  `author_id` INT(11) NOT NULL,
  `best_reply_id` INT(11) NULL DEFAULT NULL,
  `locked` TINYINT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  INDEX `fk_topics_categories1_idx` (`category_id` ASC) VISIBLE,
  INDEX `fk_topics_users1_idx` (`author_id` ASC) VISIBLE,
  INDEX `fk_topics_replies1_idx` (`best_reply_id` ASC) VISIBLE,
  CONSTRAINT `fk_topics_categories1`
    FOREIGN KEY (`category_id`)
    REFERENCES `forum_app`.`categories` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_topics_replies1`
    FOREIGN KEY (`best_reply_id`)
    REFERENCES `forum_app`.`replies` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_topics_users1`
    FOREIGN KEY (`author_id`)
    REFERENCES `forum_app`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 2
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `forum_app`.`replies`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forum_app`.`replies` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `created_on` DATETIME NOT NULL,
  `text` VARCHAR(400) NOT NULL,
  `topic_id` INT(11) NOT NULL,
  `creator_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_replies_topics1_idx` (`topic_id` ASC) VISIBLE,
  INDEX `fk_replies_users1_idx` (`creator_id` ASC) VISIBLE,
  CONSTRAINT `fk_replies_topics1`
    FOREIGN KEY (`topic_id`)
    REFERENCES `forum_app`.`topics` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_replies_users1`
    FOREIGN KEY (`creator_id`)
    REFERENCES `forum_app`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 7
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `forum_app`.`votes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forum_app`.`votes` (
  `vote` TINYINT(4) NULL DEFAULT NULL,
  `reply_id` INT(11) NOT NULL,
  `user_id` INT(11) NOT NULL,
  PRIMARY KEY (`reply_id`, `user_id`),
  UNIQUE INDEX `replies_id_UNIQUE` (`reply_id` ASC) VISIBLE,
  UNIQUE INDEX `users_id_UNIQUE` (`user_id` ASC) VISIBLE,
  INDEX `fk_votes_replies1_idx` (`reply_id` ASC) VISIBLE,
  INDEX `fk_votes_users1_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_votes_replies1`
    FOREIGN KEY (`reply_id`)
    REFERENCES `forum_app`.`replies` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_votes_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `forum_app`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
