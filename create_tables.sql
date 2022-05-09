CREATE DATABASE IF NOT EXISTS `pylogin` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `pylogin`;

CREATE TABLE IF NOT EXISTS `accounts` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
  	`password` varchar(255) NOT NULL,
  	`email` varchar(100) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

INSERT INTO `accounts` (`id`, `password`, `email`) VALUES (1, 'test', 'test@test.com');

