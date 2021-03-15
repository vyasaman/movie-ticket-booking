-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               8.0.22 - MySQL Community Server - GPL
-- Server OS:                    Win64
-- HeidiSQL Version:             11.2.0.6213
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Dumping database structure for ticketbooking
CREATE DATABASE IF NOT EXISTS `ticketbooking` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `ticketbooking`;

-- Dumping structure for table ticketbooking.booking
CREATE TABLE IF NOT EXISTS `booking` (
  `book_id` int NOT NULL AUTO_INCREMENT,
  `book_mov` varchar(50) NOT NULL,
  `book_th` varchar(50) NOT NULL,
  `book_seats` varchar(50) DEFAULT NULL,
  `book_time` time NOT NULL,
  `book_city` varchar(50) NOT NULL,
  `book_user` int DEFAULT NULL,
  PRIMARY KEY (`book_id`),
  KEY `FK_booking_user_data` (`book_user`),
  CONSTRAINT `FK_booking_user_data` FOREIGN KEY (`book_user`) REFERENCES `user_data` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=100020330 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table ticketbooking.booking: ~9 rows (approximately)
/*!40000 ALTER TABLE `booking` DISABLE KEYS */;
INSERT INTO `booking` (`book_id`, `book_mov`, `book_th`, `book_seats`, `book_time`, `book_city`, `book_user`) VALUES
	(100020315, 'Tom and Jerry', 'Fun Cinemas', NULL, '12:00:00', 'Bhopal', NULL),
	(100020316, 'Bel Bottom', 'Fun Cinemas', NULL, '12:00:00', 'Bhopal', NULL),
	(100020320, 'Bel Bottom', 'Fun Cinemas', 'A4, A5, A6', '12:00:00', 'Bhopal', NULL),
	(100020324, 'Bel Bottom', 'PVR', 'A1, A2', '12:00:00', 'South Delhi', NULL),
	(100020325, 'Tom and Jerry', 'INOX', 'B8, B9', '15:00:00', 'Bhopal', NULL),
	(100020326, 'Tom and Jerry', 'PVR', 'B9', '12:00:00', 'South Delhi', NULL),
	(100020327, 'Bel Bottom', 'Fun Cinemas', 'A1, A2', '12:00:00', 'Bhopal', NULL),
	(100020328, 'Tom and Jerry', 'INOX', 'A7, A8, A9', '15:00:00', 'Bhopal', NULL),
	(100020329, 'Bel Bottom', 'Fun Cinemas', 'B6', '18:00:00', 'Bhopal', 5);
/*!40000 ALTER TABLE `booking` ENABLE KEYS */;

-- Dumping structure for table ticketbooking.movie
CREATE TABLE IF NOT EXISTS `movie` (
  `mov_id` int NOT NULL AUTO_INCREMENT,
  `mov_name` varchar(100) NOT NULL,
  `theatre` int NOT NULL DEFAULT '0',
  `ticket_price` int NOT NULL DEFAULT '100',
  `time1` time NOT NULL DEFAULT '12:00:00',
  PRIMARY KEY (`mov_id`),
  KEY `FK_movie_theatre` (`theatre`),
  CONSTRAINT `FK_movie_theatre` FOREIGN KEY (`theatre`) REFERENCES `theatre` (`th_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table ticketbooking.movie: ~8 rows (approximately)
/*!40000 ALTER TABLE `movie` DISABLE KEYS */;
INSERT INTO `movie` (`mov_id`, `mov_name`, `theatre`, `ticket_price`, `time1`) VALUES
	(1, 'Bel Bottom', 1, 100, '12:00:00'),
	(2, 'Tom and Jerry', 1, 100, '12:00:00'),
	(3, 'Bel Bottom', 2, 100, '12:00:00'),
	(4, 'Bel Bottom', 3, 100, '12:00:00'),
	(5, 'Tom and Jerry', 2, 100, '07:00:00'),
	(6, 'Tom and Jerry', 3, 100, '12:00:00'),
	(7, 'Tom and Jerry', 4, 100, '15:00:00'),
	(8, 'Bel Bottom', 1, 200, '18:00:00');
/*!40000 ALTER TABLE `movie` ENABLE KEYS */;

-- Dumping structure for table ticketbooking.theatre
CREATE TABLE IF NOT EXISTS `theatre` (
  `th_id` int NOT NULL AUTO_INCREMENT,
  `th_name` varchar(100) NOT NULL,
  `th_address` varchar(150) NOT NULL,
  `City` varchar(100) NOT NULL,
  `State` varchar(100) NOT NULL,
  PRIMARY KEY (`th_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table ticketbooking.theatre: ~4 rows (approximately)
/*!40000 ALTER TABLE `theatre` DISABLE KEYS */;
INSERT INTO `theatre` (`th_id`, `th_name`, `th_address`, `City`, `State`) VALUES
	(1, 'Fun Cinemas', 'DB Mall, Board Office Square,Mp Nagar', 'Bhopal', 'MP'),
	(2, 'PVR', 'Treasure Island', 'Indore', 'MP'),
	(3, 'PVR', 'Sector 21', 'South Delhi', 'Delhi'),
	(4, 'INOX', 'C21 Mall,Hoshangabad Road', 'Bhopal', 'MP');
/*!40000 ALTER TABLE `theatre` ENABLE KEYS */;

-- Dumping structure for table ticketbooking.user_data
CREATE TABLE IF NOT EXISTS `user_data` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `user_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `user_email` varchar(100) NOT NULL,
  `user_pass` varchar(50) NOT NULL,
  `user_mob` bigint NOT NULL DEFAULT '0',
  `user_role` varchar(50) NOT NULL DEFAULT 'User',
  `user_city` varchar(50) NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `user_email` (`user_email`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dumping data for table ticketbooking.user_data: ~3 rows (approximately)
/*!40000 ALTER TABLE `user_data` DISABLE KEYS */;
INSERT INTO `user_data` (`user_id`, `user_name`, `user_email`, `user_pass`, `user_mob`, `user_role`, `user_city`) VALUES
	(1, 'Abc', 'abc@gmail.com', '12345', 0, 'Admin', 'South Delhi'),
	(5, 'Aman', 'amanvyas@gmail.com', '12345', 7974294474, 'User', 'Bhopal'),
	(6, 'Raj Kapoor', 'raj@abc.com', '12345', 7779999123, 'User', 'South Delhi');
/*!40000 ALTER TABLE `user_data` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
