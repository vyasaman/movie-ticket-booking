-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               8.0.19 - MySQL Community Server - GPL
-- Server OS:                    Win64
-- HeidiSQL Version:             10.2.0.5599
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- Dumping database structure for ticketbooking
CREATE DATABASE IF NOT EXISTS `ticketbooking` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `ticketbooking`;

-- Dumping structure for table ticketbooking.movie
CREATE TABLE IF NOT EXISTS `movie` (
  `mov_id` int NOT NULL AUTO_INCREMENT,
  `mov_name` varchar(100) NOT NULL,
  `theatre` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`mov_id`),
  KEY `FK_movie_theatre` (`theatre`),
  CONSTRAINT `FK_movie_theatre` FOREIGN KEY (`theatre`) REFERENCES `theatre` (`th_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table ticketbooking.movie: ~1 rows (approximately)
/*!40000 ALTER TABLE `movie` DISABLE KEYS */;
INSERT INTO `movie` (`mov_id`, `mov_name`, `theatre`) VALUES
	(1, 'Bel Bottom', 1);
/*!40000 ALTER TABLE `movie` ENABLE KEYS */;

-- Dumping structure for table ticketbooking.theatre
CREATE TABLE IF NOT EXISTS `theatre` (
  `th_id` int NOT NULL AUTO_INCREMENT,
  `th_name` varchar(100) NOT NULL,
  `th_address` varchar(150) NOT NULL,
  `City` varchar(100) NOT NULL,
  `State` varchar(100) NOT NULL,
  PRIMARY KEY (`th_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table ticketbooking.theatre: ~1 rows (approximately)
/*!40000 ALTER TABLE `theatre` DISABLE KEYS */;
INSERT INTO `theatre` (`th_id`, `th_name`, `th_address`, `City`, `State`) VALUES
	(1, 'Fun Cinemas', 'DB Mall, Board Office Square,Mp Nagar', 'Bhopal', 'MP');
/*!40000 ALTER TABLE `theatre` ENABLE KEYS */;

-- Dumping structure for table ticketbooking.user_data
CREATE TABLE IF NOT EXISTS `user_data` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `user_email` varchar(100) NOT NULL,
  `user_pass` varchar(50) NOT NULL,
  `user_name` varchar(50) NOT NULL,
  `user_role` varchar(50) NOT NULL DEFAULT 'User',
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `user_email` (`user_email`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table ticketbooking.user_data: ~1 rows (approximately)
/*!40000 ALTER TABLE `user_data` DISABLE KEYS */;
INSERT INTO `user_data` (`user_id`, `user_email`, `user_pass`, `user_name`, `user_role`) VALUES
	(1, 'abc@gmail.com', '12345', 'Abc', 'Admin');
/*!40000 ALTER TABLE `user_data` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
