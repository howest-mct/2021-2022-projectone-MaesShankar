CREATE DATABASE  IF NOT EXISTS `ProjectDB` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `ProjectDB`;
-- MySQL dump 10.13  Distrib 5.7.37, for Win64 (x86_64)
--
-- Host: localhost    Database: ProjectDB
-- ------------------------------------------------------
-- Server version	5.5.5-10.5.15-MariaDB-0+deb11u1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Actie`
--

DROP TABLE IF EXISTS `Actie`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Actie` (
  `ActieID` int(11) NOT NULL AUTO_INCREMENT,
  `ActieBeschrijving` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`ActieID`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Actie`
--

LOCK TABLES `Actie` WRITE;
/*!40000 ALTER TABLE `Actie` DISABLE KEYS */;
INSERT INTO `Actie` VALUES (1,'Relais Aansturen'),(2,'LCD aansturen');
/*!40000 ALTER TABLE `Actie` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Device`
--

DROP TABLE IF EXISTS `Device`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Device` (
  `DeviceID` int(11) NOT NULL,
  `Naam` varchar(75) NOT NULL,
  `DeviceMerk` varchar(75) DEFAULT NULL,
  `DeviceBeschrijving` varchar(75) NOT NULL,
  `Type` varchar(75) DEFAULT NULL,
  `Kostprijs` int(11) DEFAULT NULL,
  `Meeteenheid` varchar(75) DEFAULT NULL,
  PRIMARY KEY (`DeviceID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Device`
--

LOCK TABLES `Device` WRITE;
/*!40000 ALTER TABLE `Device` DISABLE KEYS */;
INSERT INTO `Device` VALUES (1,'MQ-3','Arduino','AlcoholgasSensor meet alcohol in adem','mq-3',5,'Promille'),(2,'Temperatuursensor','Arduino','Temperatuurssensor meet temperatuur','DS18B20',7,'°C'),(3,'RFID','Arduino','Identiteitscontrole','RC522',6,''),(4,'StartButton','Arduino','StartControle','B3F-1020',0,''),(5,'ShutdownButton','Arduino','StutdownControle','B3F-1021',0,'');
/*!40000 ALTER TABLE `Device` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Historiek`
--

DROP TABLE IF EXISTS `Historiek`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Historiek` (
  `HistoriekID` int(11) NOT NULL AUTO_INCREMENT,
  `DeviceID` int(11) DEFAULT NULL,
  `ActieID` int(11) DEFAULT NULL,
  `Datum` datetime NOT NULL DEFAULT current_timestamp(),
  `Waarde` int(11) NOT NULL,
  `Commentaar` varchar(75) DEFAULT NULL,
  PRIMARY KEY (`HistoriekID`),
  KEY `fk_Historiek_Device_idx` (`DeviceID`),
  KEY `fk_Historiek_Actie1_idx` (`ActieID`),
  CONSTRAINT `fk_Historiek_Actie1` FOREIGN KEY (`ActieID`) REFERENCES `Actie` (`ActieID`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_Historiek_Device` FOREIGN KEY (`DeviceID`) REFERENCES `Device` (`DeviceID`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Historiek`
--

LOCK TABLES `Historiek` WRITE;
/*!40000 ALTER TABLE `Historiek` DISABLE KEYS */;
INSERT INTO `Historiek` VALUES (1,4,2,'2022-04-01 17:07:39',1,'Start'),(2,3,NULL,'2022-04-02 14:46:06',1,'Identificatie'),(3,1,1,'2022-04-03 21:52:44',3,'Meting Alcohol'),(4,2,NULL,'2022-04-04 18:14:43',25,'Meting Temperatuur'),(5,5,NULL,'2022-04-06 12:25:49',1,'Shutdown'),(6,4,2,'2022-04-06 20:31:43',1,'Start'),(7,3,NULL,'2022-04-07 10:08:24',1,'Identificatie'),(8,1,1,'2022-04-08 00:20:01',0,'Meting Alcohol'),(9,2,NULL,'2022-04-08 06:38:42',18,'Meting Temperatuur'),(10,5,NULL,'2022-04-09 19:29:39',1,'Shutdown'),(11,4,2,'2022-04-10 04:47:35',1,'Start'),(12,3,NULL,'2022-04-11 23:28:17',1,'Identificatie'),(13,1,1,'2022-04-12 07:16:54',2,'Meting Alcohol'),(14,2,NULL,'2022-04-13 16:30:09',20,'Meting Temperatuur'),(15,5,NULL,'2022-04-14 14:37:01',1,'Shutdown'),(16,4,2,'2022-04-15 10:20:20',1,'Start'),(17,3,NULL,'2022-04-15 18:17:12',1,'Identificatie'),(18,1,1,'2022-04-16 05:31:49',0,'Meting Alcohol'),(19,2,NULL,'2022-04-17 22:52:36',25,'Meting Temperatuur'),(20,5,NULL,'2022-04-18 22:48:05',1,'Shutdown'),(21,4,2,'2022-04-19 02:47:58',1,'Start'),(22,3,NULL,'2022-04-22 09:21:05',1,'Identificatie'),(23,1,1,'2022-04-23 02:33:05',1,'Meting Alcohol'),(24,2,NULL,'2022-04-23 20:46:32',24,'Meting Temperatuur'),(25,5,NULL,'2022-04-25 19:48:58',1,'Shutdown'),(26,4,2,'2022-04-26 10:36:56',1,'Start'),(27,3,NULL,'2022-04-26 17:52:37',1,'Identificatie'),(28,1,1,'2022-04-30 15:37:55',0,'Meting Alcohol'),(29,2,NULL,'2022-04-30 17:20:30',23,'Meting Temperatuur'),(30,5,NULL,'2022-05-02 10:27:17',1,'Shutdown'),(31,4,2,'2022-05-02 12:40:53',1,'Start'),(32,3,NULL,'2022-05-02 14:30:37',1,'Identificatie'),(33,1,1,'2022-05-03 08:57:18',3,'Meting Alcohol'),(34,2,NULL,'2022-05-03 21:09:45',22,'Meting Temperatuur'),(35,5,NULL,'2022-05-04 19:23:39',1,'Shutdown'),(36,4,2,'2022-05-05 20:27:20',1,'Start'),(37,3,NULL,'2022-05-05 23:15:23',1,'Identificatie'),(38,1,1,'2022-05-06 07:30:04',2,'Meting Alcohol'),(39,2,NULL,'2022-05-08 17:22:08',18,'Meting Temperatuur'),(40,5,NULL,'2022-05-09 03:53:25',1,'Shutdown'),(41,4,2,'2022-05-09 10:36:23',1,'Start'),(42,3,NULL,'2022-05-10 15:24:23',1,'Identificatie'),(43,1,1,'2022-05-12 05:09:03',2,'Meting Alcohol'),(44,2,NULL,'2022-05-12 21:13:23',17,'Meting Temperatuur'),(45,5,NULL,'2022-05-16 09:08:23',1,'Shutdown'),(46,4,2,'2022-05-17 00:47:36',1,'Start'),(47,3,NULL,'2022-05-17 05:40:16',1,'Identificatie'),(48,1,1,'2022-05-18 19:28:55',2,'Meting Alcohol'),(49,2,NULL,'2022-05-21 18:38:31',24,'Meting Temperatuur'),(50,5,NULL,'2022-05-23 13:48:21',1,'Shutdown');
/*!40000 ALTER TABLE `Historiek` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-05-23 11:01:44
