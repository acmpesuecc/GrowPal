-- MariaDB dump 10.19  Distrib 10.6.5-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: growpal
-- ------------------------------------------------------
-- Server version	10.6.5-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `credit_card_transactions`
--

DROP TABLE IF EXISTS `credit_card_transactions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `credit_card_transactions` (
  `username` varchar(50) DEFAULT NULL,
  `item` varchar(50) DEFAULT NULL,
  `price` varchar(50) DEFAULT NULL,
  `card_number` varchar(50) DEFAULT NULL,
  `cvv` varchar(50) DEFAULT NULL,
  `flat_number` varchar(400) DEFAULT NULL,
  `image_url` varchar(500) DEFAULT NULL,
  `order_id` int(11) DEFAULT NULL,
  `deleted` varchar(5) DEFAULT 'False'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `credit_card_transactions`
--

--
-- Table structure for table `debit_card_transactions`
--

DROP TABLE IF EXISTS `debit_card_transactions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `debit_card_transactions` (
  `username` varchar(50) DEFAULT NULL,
  `item` varchar(50) DEFAULT NULL,
  `price` varchar(50) DEFAULT NULL,
  `card_number` varchar(50) DEFAULT NULL,
  `cvv` varchar(50) DEFAULT NULL,
  `flat_number` varchar(400) DEFAULT NULL,
  `image_url` varchar(500) DEFAULT NULL,
  `order_id` int(11) DEFAULT NULL,
  `deleted` varchar(5) DEFAULT 'False'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `debit_card_transactions`
--
--
-- Table structure for table `listed_items`
--

DROP TABLE IF EXISTS `listed_items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `listed_items` (
  `product_name` varchar(50) DEFAULT NULL,
  `product_price` varchar(50) DEFAULT NULL,
  `product_description` varchar(1000) DEFAULT NULL,
  `seller_username` varchar(50) DEFAULT NULL,
  `seller_name` varchar(50) DEFAULT NULL,
  `seller_phone_number` varchar(10) DEFAULT NULL,
  `seller_email` varchar(50) DEFAULT NULL,
  `seller_address` varchar(500) DEFAULT NULL,
  `seller_upi_id` varchar(100) DEFAULT NULL,
  `product_image_address` varchar(500) DEFAULT NULL,
  `deleted` varchar(5) DEFAULT 'False',
  `item_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `listed_items`
--

--
-- Table structure for table `login_details`
--

DROP TABLE IF EXISTS `login_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `login_details` (
  `username` varchar(50) NOT NULL,
  `password` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `phone_number` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `login_details`
--

--
-- Table structure for table `net_bank_transactions`
--

DROP TABLE IF EXISTS `net_bank_transactions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `net_bank_transactions` (
  `username` varchar(50) DEFAULT NULL,
  `item` varchar(50) DEFAULT NULL,
  `price` varchar(50) DEFAULT NULL,
  `account_number` varchar(50) DEFAULT NULL,
  `CIF_num` varchar(50) DEFAULT NULL,
  `branch_code` varchar(50) DEFAULT NULL,
  `flat_number` varchar(400) DEFAULT NULL,
  `image_url` varchar(500) DEFAULT NULL,
  `order_id` int(11) DEFAULT NULL,
  `deleted` varchar(5) DEFAULT 'False'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `net_bank_transactions`
--

--
-- Table structure for table `numbers`
--

DROP TABLE IF EXISTS `numbers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `numbers` (
  `item_id_num` int(11) DEFAULT NULL,
  `order_id_num` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `numbers`
--

LOCK TABLES `numbers` WRITE;
/*!40000 ALTER TABLE `numbers` DISABLE KEYS */;
INSERT INTO `numbers` VALUES (0,0);
/*!40000 ALTER TABLE `numbers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `upi_transactions`
--

DROP TABLE IF EXISTS `upi_transactions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `upi_transactions` (
  `username` varchar(50) DEFAULT NULL,
  `item` varchar(50) DEFAULT NULL,
  `price` varchar(50) DEFAULT NULL,
  `UPI_ID` varchar(50) DEFAULT NULL,
  `flat_number` varchar(400) DEFAULT NULL,
  `image_url` varchar(500) DEFAULT NULL,
  `order_id` int(11) DEFAULT NULL,
  `deleted` varchar(5) DEFAULT 'False'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `upi_transactions`
--

LOCK TABLES `upi_transactions` WRITE;
/*!40000 ALTER TABLE `upi_transactions` DISABLE KEYS */;
INSERT INTO `upi_transactions` VALUES ('Tamanna Singh','ASUS ZenBook Duo 14 (2021)','100000','9945692772@upi','B-3','https://ik.imagekit.io/bule8zjn18b/4.jpeg?ik-sdk-version=python-2.2.8',3,'False'),('Tamanna Singh','t-shirt','295','9945692772@upi','B-3','https://ik.imagekit.io/bule8zjn18b/1.jpeg?ik-sdk-version=python-2.2.8',4,'False'),('Tamanna Singh','Table Lamp','599','9945692772@upi','B-3','https://ik.imagekit.io/bule8zjn18b/3.jpeg?ik-sdk-version=python-2.2.8',5,'False'),('Tamanna Singh','Table Lamp','599','9945692772@upi','B-3','https://ik.imagekit.io/bule8zjn18b/3.jpeg?ik-sdk-version=python-2.2.8',6,'False');
/*!40000 ALTER TABLE `upi_transactions` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-01-31 17:14:02
