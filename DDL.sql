
CREATE DATABASE IF NOT EXISTS `dataset`
DEFAULT CHARACTER SET = utf8;

CREATE TABLE IF NOT EXISTS `dataset`.`death` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `date` DATE NULL,
  `country` VARCHAR(45) NULL,
  `departament` VARCHAR(45) NULL,
  `municipality` VARCHAR(45) NULL,
  `new_deaths` INT NULL,
  `cumulative_deaths` INT NULL,
  `register_type` ENUM('summary', 'municipality') NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;

DROP TABLE IF EXISTS `dataset`.`death`;

desc death;
SELECT * FROM dataset.death;

GRANT CREATE, ALTER, DROP, INSERT, UPDATE, INDEX, DELETE, SELECT, REFERENCES, RELOAD on *.* TO 'erikssonherlo'@'localhost' WITH GRANT OPTION;
GRANT ALL PRIVILEGES ON *.* TO 'erikssonherlo'@'localhost' WITH GRANT OPTION;