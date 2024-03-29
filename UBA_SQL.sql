-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               11.4.0-MariaDB - mariadb.org binary distribution
-- Server OS:                    Win64
-- HeidiSQL Version:             12.3.0.6589
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Dumping database structure for uba_test
CREATE DATABASE IF NOT EXISTS `uba_test` /*!40100 DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci */;
USE `uba_test`;

-- Dumping structure for table uba_test.tbl_instruments
CREATE TABLE IF NOT EXISTS `tbl_instruments` (
  `instrument_id` int(10) NOT NULL,
  `instrument_serial_no` char(50) DEFAULT NULL,
  `instrument_name` char(50) DEFAULT NULL,
  `comment` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`instrument_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci COMMENT='resgisters all the lysimeters and other instruments';

-- Data exporting was unselected.

-- Dumping structure for table uba_test.tbl_measurements
CREATE TABLE IF NOT EXISTS `tbl_measurements` (
  `m_id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'measuremnt id in the database',
  `m_date` date DEFAULT NULL COMMENT 'the day measurement was taken',
  `m_type` int(11) DEFAULT NULL COMMENT 'measurement type. this value should be present in measurment types table. from that table we will find the meta info about this type. ie. ph, conductivity',
  `m_instrument_id` int(10) DEFAULT NULL COMMENT 'db id of the instrument used to take the measuremnt',
  `m_value` double DEFAULT NULL COMMENT 'measurement value found',
  `m_person` int(11) DEFAULT NULL COMMENT 'person who took the measurements',
  `db_timestamp` timestamp NULL DEFAULT NULL COMMENT 'time of inserting in the db',
  PRIMARY KEY (`m_id`) USING BTREE,
  KEY `tbl_measurments_fk_mtype` (`m_type`),
  KEY `tbl_measurments_fk_person` (`m_person`),
  KEY `FK_tbl_measurements_tbl_instruments` (`m_instrument_id`),
  CONSTRAINT `FK_tbl_measurements_tbl_instruments` FOREIGN KEY (`m_instrument_id`) REFERENCES `tbl_instruments` (`instrument_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `tbl_measurments_fk_mtype` FOREIGN KEY (`m_type`) REFERENCES `tbl_measurement_types` (`type_id`) ON UPDATE CASCADE,
  CONSTRAINT `tbl_measurments_fk_person` FOREIGN KEY (`m_person`) REFERENCES `tbl_person` (`p_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci COMMENT='holds the measurment parameters in the table';

-- Data exporting was unselected.

-- Dumping structure for table uba_test.tbl_measurement_types
CREATE TABLE IF NOT EXISTS `tbl_measurement_types` (
  `type_id` int(11) NOT NULL AUTO_INCREMENT,
  `parameter_name` varchar(50) NOT NULL DEFAULT 'PARAMETER_NA',
  `param_unit` varchar(50) NOT NULL DEFAULT 'PARAMETER_UNIT_NA',
  `description` text DEFAULT NULL,
  PRIMARY KEY (`type_id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Data exporting was unselected.

-- Dumping structure for table uba_test.tbl_person
CREATE TABLE IF NOT EXISTS `tbl_person` (
  `p_id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'person id in the database',
  `p_name` char(255) DEFAULT NULL COMMENT 'persons name',
  `p_eid` int(11) DEFAULT 0 COMMENT 'organisation employee id',
  PRIMARY KEY (`p_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Data exporting was unselected.

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
