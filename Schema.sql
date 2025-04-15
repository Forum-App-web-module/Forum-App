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
-- Table `forum_app`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forum_app`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(15) NOT NULL,
  `email` VARCHAR(40) NOT NULL,
  `password` VARCHAR(45) NOT NULL,
  `bio` VARCHAR(45) NULL,
  `is_admin` BIT(1) NULL,
  `is_active` BIT(1) NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `username_UNIQUE` (`username` ASC) VISIBLE,
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `forum_app`.`categories`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forum_app`.`categories` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `is_private` BIT(1) NULL,
  `lock` BIT(1) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `forum_app`.`replies`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forum_app`.`replies` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `created_on` DATETIME NOT NULL,
  `text` VARCHAR(400) NOT NULL,
  `topic_id` INT NOT NULL,
  `creator_id` INT NOT NULL,
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
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `forum_app`.`topics`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forum_app`.`topics` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(45) NOT NULL,
  `categories_id` INT NOT NULL,
  `author_id` INT NOT NULL,
  `best_reply_id` INT NULL,
  `lock` BIT(1) NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_topics_categories1_idx` (`categories_id` ASC) VISIBLE,
  INDEX `fk_topics_users1_idx` (`author_id` ASC) VISIBLE,
  INDEX `fk_topics_replies1_idx` (`best_reply_id` ASC) VISIBLE,
  CONSTRAINT `fk_topics_categories1`
    FOREIGN KEY (`categories_id`)
    REFERENCES `forum_app`.`categories` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_topics_users1`
    FOREIGN KEY (`author_id`)
    REFERENCES `forum_app`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_topics_replies1`
    FOREIGN KEY (`best_reply_id`)
    REFERENCES `forum_app`.`replies` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `forum_app`.`messages`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forum_app`.`messages` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `text` VARCHAR(200) NOT NULL,
  `sent_on` DATETIME NOT NULL,
  `sender_id` INT NOT NULL,
  `receiver_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_messages_users1_idx` (`sender_id` ASC) VISIBLE,
  INDEX `fk_messages_users2_idx` (`receiver_id` ASC) VISIBLE,
  UNIQUE INDEX `sender_id_UNIQUE` (`sender_id` ASC) VISIBLE,
  UNIQUE INDEX `receiver_id_UNIQUE` (`receiver_id` ASC) VISIBLE,
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
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `forum_app`.`votes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forum_app`.`votes` (
  `vote` TINYINT NULL,
  `replies_id` INT NOT NULL,
  `users_id` INT NOT NULL,
  PRIMARY KEY (`replies_id`, `users_id`),
  INDEX `fk_votes_replies1_idx` (`replies_id` ASC) VISIBLE,
  INDEX `fk_votes_users1_idx` (`users_id` ASC) VISIBLE,
  UNIQUE INDEX `replies_id_UNIQUE` (`replies_id` ASC) VISIBLE,
  UNIQUE INDEX `users_id_UNIQUE` (`users_id` ASC) VISIBLE,
  CONSTRAINT `fk_votes_replies1`
    FOREIGN KEY (`replies_id`)
    REFERENCES `forum_app`.`replies` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_votes_users1`
    FOREIGN KEY (`users_id`)
    REFERENCES `forum_app`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `forum_app`.`category_members`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `forum_app`.`category_members` (
  `categories_id` INT NOT NULL,
  `users_id` INT NOT NULL,
  `can_write` BIT(1) NULL,
  PRIMARY KEY (`categories_id`, `users_id`),
  INDEX `fk_category_members_categories1_idx` (`categories_id` ASC) VISIBLE,
  INDEX `fk_category_members_users1_idx` (`users_id` ASC) VISIBLE,
  UNIQUE INDEX `categories_id_UNIQUE` (`categories_id` ASC) VISIBLE,
  UNIQUE INDEX `users_id_UNIQUE` (`users_id` ASC) VISIBLE,
  CONSTRAINT `fk_category_members_categories1`
    FOREIGN KEY (`categories_id`)
    REFERENCES `forum_app`.`categories` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_category_members_users1`
    FOREIGN KEY (`users_id`)
    REFERENCES `forum_app`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
