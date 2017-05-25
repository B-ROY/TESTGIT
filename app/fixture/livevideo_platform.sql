-- MySQL dump 10.13  Distrib 5.6.25, for osx10.10 (x86_64)
--
-- Host: localhost    Database: livevideo_platform
-- ------------------------------------------------------
-- Server version	5.6.25

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
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `auth_group_permissions_5f412f9a` (`group_id`),
  KEY `auth_group_permissions_83d7f98b` (`permission_id`),
  CONSTRAINT `group_id_refs_id_f4b32aac` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `permission_id_refs_id_6ba0f519` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  KEY `auth_permission_37ef4eb4` (`content_type_id`),
  CONSTRAINT `content_type_id_refs_id_d043b34a` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=136 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add permission',1,'add_permission'),(2,'Can change permission',1,'change_permission'),(3,'Can delete permission',1,'delete_permission'),(4,'Can add group',2,'add_group'),(5,'Can change group',2,'change_group'),(6,'Can delete group',2,'delete_group'),(7,'Can add user',3,'add_user'),(8,'Can change user',3,'change_user'),(9,'Can delete user',3,'delete_user'),(10,'Can add content type',4,'add_contenttype'),(11,'Can change content type',4,'change_contenttype'),(12,'Can delete content type',4,'delete_contenttype'),(13,'Can add session',5,'add_session'),(14,'Can change session',5,'change_session'),(15,'Can delete session',5,'delete_session'),(16,'Can add log entry',6,'add_logentry'),(17,'Can change log entry',6,'change_logentry'),(18,'Can delete log entry',6,'delete_logentry'),(19,'Can add 等级',7,'add_level'),(20,'Can change 等级',7,'change_level'),(21,'Can delete 等级',7,'delete_level'),(22,'Can add 用户',8,'add_user'),(23,'Can change 用户',8,'change_user'),(24,'Can delete 用户',8,'delete_user'),(25,'Can add 用户关注关系',9,'add_userfollow'),(26,'Can change 用户关注关系',9,'change_userfollow'),(27,'Can delete 用户关注关系',9,'delete_userfollow'),(28,'Can add 私信简介列表',10,'add_usersummerymessage'),(29,'Can change 私信简介列表',10,'change_usersummerymessage'),(30,'Can delete 私信简介列表',10,'delete_usersummerymessage'),(31,'Can add 私信',11,'add_userprivatemessage'),(32,'Can change 私信',11,'change_userprivatemessage'),(33,'Can delete 私信',11,'delete_userprivatemessage'),(34,'Can add 用户账户',12,'add_account'),(35,'Can change 用户账户',12,'change_account'),(36,'Can delete 用户账户',12,'delete_account'),(40,'Can add 充值规则',14,'add_tradebalancerule'),(41,'Can change 充值规则',14,'change_tradebalancerule'),(42,'Can delete 充值规则',14,'delete_tradebalancerule'),(43,'Can add 充值交易记录',15,'add_tradebalanceorder'),(44,'Can change 充值交易记录',15,'change_tradebalanceorder'),(45,'Can delete 充值交易记录',15,'delete_tradebalanceorder'),(46,'Can add 充值交易记录',16,'add_withdrawbalanceorder'),(47,'Can change 充值交易记录',16,'change_withdrawbalanceorder'),(48,'Can delete 充值交易记录',16,'delete_withdrawbalanceorder'),(49,'Can add 礼物',17,'add_gift'),(50,'Can change 礼物',17,'change_gift'),(51,'Can delete 礼物',17,'delete_gift'),(52,'Can add 经验上报种类',18,'add_userexperiencetype'),(53,'Can change 经验上报种类',18,'change_userexperiencetype'),(54,'Can delete 经验上报种类',18,'delete_userexperiencetype'),(55,'Can add 经验上报日志',19,'add_userexperiencelog'),(56,'Can change 经验上报日志',19,'change_userexperiencelog'),(57,'Can delete 经验上报日志',19,'delete_userexperiencelog'),(58,'Can add 举报',20,'add_report'),(59,'Can change 举报',20,'change_report'),(60,'Can delete 举报',20,'delete_report'),(61,'Can add 房间',21,'add_liveroom'),(62,'Can change 房间',21,'change_liveroom'),(63,'Can delete 房间',21,'delete_liveroom'),(64,'Can add 房间里的成员',22,'add_roommember'),(65,'Can change 房间里的成员',22,'change_roommember'),(66,'Can delete 房间里的成员',22,'delete_roommember'),(67,'Can add 用礼物管理',23,'add_roomusergift'),(68,'Can change 用礼物管理',23,'change_roomusergift'),(69,'Can delete 用礼物管理',23,'delete_roomusergift'),(70,'Can add 广告',24,'add_adv'),(71,'Can change 广告',24,'change_adv'),(72,'Can delete 广告',24,'delete_adv'),(73,'Can add 好友关系',25,'add_userfriends'),(74,'Can change 好友关系',25,'change_userfriends'),(75,'Can delete 好友关系',25,'delete_userfriends'),(76,'Can add 启动图',26,'add_startupimage'),(77,'Can change 启动图',26,'change_startupimage'),(78,'Can delete 启动图',26,'delete_startupimage'),(79,'Can add 第三方绑定',27,'add_thridpard'),(80,'Can change 第三方绑定',27,'change_thridpard'),(81,'Can delete 第三方绑定',27,'delete_thridpard'),(82,'Can add 白名单',28,'add_whitelist'),(83,'Can change 白名单',28,'change_whitelist'),(84,'Can delete 白名单',28,'delete_whitelist'),(85,'Can add 用户账户',29,'add_wechatfillnotice'),(86,'Can change 用户账户',29,'change_wechatfillnotice'),(87,'Can delete 用户账户',29,'delete_wechatfillnotice'),(91,'Can add 充值交易记录',31,'add_tradediamondrecord'),(92,'Can change 充值交易记录',31,'change_tradediamondrecord'),(93,'Can delete 充值交易记录',31,'delete_tradediamondrecord'),(94,'Can add ticket交易记录',32,'add_tradeticketrecord'),(95,'Can change ticket交易记录',32,'change_tradeticketrecord'),(96,'Can delete ticket交易记录',32,'delete_tradeticketrecord'),(97,'Can add 商户统计',33,'add_businessstatistics'),(98,'Can change 商户统计',33,'change_businessstatistics'),(99,'Can delete 商户统计',33,'delete_businessstatistics'),(100,'Can add 苹果支付回调',34,'add_appleverify'),(101,'Can change 苹果支付回调',34,'change_appleverify'),(102,'Can delete 苹果支付回调',34,'delete_appleverify'),(103,'Can add 苹果支付回调',35,'add_appleverifyresult'),(104,'Can change 苹果支付回调',35,'change_appleverifyresult'),(105,'Can delete 苹果支付回调',35,'delete_appleverifyresult'),(106,'Can add 对某个用户的贡献',36,'add_rankcontributeuser'),(107,'Can change 对某个用户的贡献',36,'change_rankcontributeuser'),(108,'Can delete 对某个用户的贡献',36,'delete_rankcontributeuser'),(109,'Can add 微信提现记录',37,'add_wechatwithdrawresult'),(110,'Can change 微信提现记录',37,'change_wechatwithdrawresult'),(111,'Can delete 微信提现记录',37,'delete_wechatwithdrawresult'),(112,'Can add 苹果支付回调',38,'add_wexinjsverify'),(113,'Can change 苹果支付回调',38,'change_wexinjsverify'),(114,'Can delete 苹果支付回调',38,'delete_wexinjsverify'),(115,'Can add 用户通知',39,'add_usernotice'),(116,'Can change 用户通知',39,'change_usernotice'),(117,'Can delete 用户通知',39,'delete_usernotice'),(118,'Can add ugc',40,'add_ugcandbrand'),(119,'Can change ugc',40,'change_ugcandbrand'),(120,'Can delete ugc',40,'delete_ugcandbrand'),(121,'Can add 用户付费统计',41,'add_premiumuser'),(122,'Can change 用户付费统计',41,'change_premiumuser'),(123,'Can delete 用户付费统计',41,'delete_premiumuser'),(124,'Can add 用户',42,'add_userdypass'),(125,'Can change 用户',42,'change_userdypass'),(126,'Can delete 用户',42,'delete_userdypass'),(127,'Can add revenue',43,'add_revenue'),(128,'Can change revenue',43,'change_revenue'),(129,'Can delete revenue',43,'delete_revenue'),(130,'Can add FillInOrder',44,'add_fillinorder'),(131,'Can change FillInOrder',44,'change_fillinorder'),(132,'Can delete FillInOrder',44,'delete_fillinorder'),(133,'Can add FillInPayType',45,'add_fillinpaytype'),(134,'Can change FillInPayType',45,'change_fillinpaytype'),(135,'Can delete FillInPayType',45,'delete_fillinpaytype');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(75) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$12000$GEu0DaKAbEAv$0H2DOahGk/EE4HgvOgNpfASt6P9cvdAoStI5bia7pyI=','2016-05-03 11:15:03',1,'admin','','','admin@1.conm',1,1,'2016-03-06 18:25:36');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`group_id`),
  KEY `auth_user_groups_6340c63c` (`user_id`),
  KEY `auth_user_groups_5f412f9a` (`group_id`),
  CONSTRAINT `group_id_refs_id_274b862c` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `user_id_refs_id_40c41112` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`permission_id`),
  KEY `auth_user_user_permissions_6340c63c` (`user_id`),
  KEY `auth_user_user_permissions_83d7f98b` (`permission_id`),
  CONSTRAINT `permission_id_refs_id_35d9ac25` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `user_id_refs_id_4dc23c39` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer_account`
--

DROP TABLE IF EXISTS `customer_account`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `customer_account` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `diamond` int(11) NOT NULL,
  `last_diamond` int(11) NOT NULL,
  `update_time` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  KEY `customer_account_c3bd43a2` (`update_time`),
  CONSTRAINT `user_id_refs_id_88703c35` FOREIGN KEY (`user_id`) REFERENCES `customer_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer_account`
--

LOCK TABLES `customer_account` WRITE;
/*!40000 ALTER TABLE `customer_account` DISABLE KEYS */;
INSERT INTO `customer_account` VALUES (1,165,9257,9556,'2016-04-29 15:43:09'),(2,166,0,0,'2016-04-28 20:52:29'),(3,167,2,1,'2016-04-29 12:51:26'),(4,168,0,0,'2016-04-28 21:08:35'),(5,169,0,0,'2016-04-28 21:08:50'),(6,170,0,0,'2016-04-28 21:30:06'),(7,171,0,0,'2016-04-28 21:30:40'),(8,172,0,0,'2016-04-28 21:40:01'),(9,173,0,0,'2016-04-28 21:55:59'),(10,178,0,0,'2016-04-28 22:02:08'),(11,183,0,0,'2016-04-29 09:39:49'),(12,185,0,0,'2016-04-29 09:44:35'),(13,209,0,0,'2016-04-29 09:57:55'),(14,225,8857,8858,'2016-05-03 17:41:35'),(15,226,0,0,'2016-04-29 10:35:00'),(16,227,1,0,'2016-04-29 11:05:07'),(17,228,0,0,'2016-04-29 10:54:17'),(18,229,0,0,'2016-04-29 11:02:51'),(19,230,0,0,'2016-04-29 11:35:24'),(20,231,0,0,'2016-04-29 12:11:42'),(21,232,0,0,'2016-04-29 12:19:24'),(22,233,0,0,'2016-04-29 12:43:23'),(23,234,0,0,'2016-04-29 13:20:37'),(24,235,0,0,'2016-04-29 14:08:28'),(25,236,1813,4479,'2016-04-29 15:52:26'),(26,237,0,0,'2016-04-29 18:42:20'),(27,238,0,0,'2016-04-29 19:04:42'),(28,239,0,0,'2016-04-29 19:53:05'),(29,240,0,0,'2016-04-30 10:00:34'),(30,241,2200,2202,'2016-05-03 21:17:54'),(31,242,0,0,'2016-04-30 17:41:02'),(32,243,0,0,'2016-04-30 21:53:50'),(33,244,0,0,'2016-05-03 11:06:49'),(34,245,0,0,'2016-05-03 11:45:28');
/*!40000 ALTER TABLE `customer_account` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer_adv`
--

DROP TABLE IF EXISTS `customer_adv`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `customer_adv` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `status` int(11) NOT NULL,
  `adv_info` varchar(256) NOT NULL,
  `adv_type` int(11) NOT NULL,
  `image` varchar(256) NOT NULL,
  `seq` int(11) NOT NULL,
  `title` varchar(50) DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer_adv`
--

LOCK TABLES `customer_adv` WRITE;
/*!40000 ALTER TABLE `customer_adv` DISABLE KEYS */;
INSERT INTO `customer_adv` VALUES (1,1,'http://www.youku.com',0,'http://picture01-10022394.image.myqcloud.com/1457262001_f05a5f4a9d016eade74deb7c2b685531',3,'test'),(2,0,'http://www.baidu.com',1,'http://picture01-10022394.image.myqcloud.com/1457318067_f3ccdd27d2000e3f9255a7e3e2c48800',2,'test'),(3,1,'http://www.baidu.com/',0,'http://facelive-10023919.image.myqcloud.com/1460965218_b5e3ea091d43d49c79ee614b7e6fde45',1,'test');
/*!40000 ALTER TABLE `customer_adv` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer_appleverify`
--

DROP TABLE IF EXISTS `customer_appleverify`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `customer_appleverify` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `out_trade_no` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `pay_receipt` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime NOT NULL,
  `status` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `customer_appleverify_c6fd446c` (`out_trade_no`),
  KEY `customer_appleverify_96511a37` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer_appleverify`
--

LOCK TABLES `customer_appleverify` WRITE;
/*!40000 ALTER TABLE `customer_appleverify` DISABLE KEYS */;
/*!40000 ALTER TABLE `customer_appleverify` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer_appleverifyresult`
--

DROP TABLE IF EXISTS `customer_appleverifyresult`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `customer_appleverifyresult` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `out_trade_no` varchar(32) NOT NULL,
  `bid` varchar(32) DEFAULT NULL,
  `bvrs` varchar(32) DEFAULT NULL,
  `item_id` varchar(32) DEFAULT NULL,
  `original_purchase_date` varchar(32) DEFAULT NULL,
  `original_purchase_date_ms` varchar(32) DEFAULT NULL,
  `original_purchase_date_pst` varchar(64) DEFAULT NULL,
  `original_transaction_id` varchar(32) DEFAULT NULL,
  `product_id` varchar(32) DEFAULT NULL,
  `purchase_date` varchar(32) DEFAULT NULL,
  `purchase_date_ms` varchar(32) DEFAULT NULL,
  `purchase_date_pst` varchar(64) DEFAULT NULL,
  `quantity` varchar(32) DEFAULT NULL,
  `transaction_id` varchar(32) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `customer_appleverifyresult_c6fd446c` (`out_trade_no`),
  KEY `customer_appleverifyresult_96511a37` (`created_at`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer_appleverifyresult`
--

LOCK TABLES `customer_appleverifyresult` WRITE;
/*!40000 ALTER TABLE `customer_appleverifyresult` DISABLE KEYS */;
INSERT INTO `customer_appleverifyresult` VALUES (1,'497','com.heydo.lizi','1','1097285854','2016-04-17 11:18:30 Etc/GMT','1460891910505','2016-04-17 04:18:30 America/Los_Angeles','1000000206303916','040601000','2016-04-17 11:18:30 Etc/GMT','1460891910505','2016-04-17 04:18:30 America/Los_Angeles','1','1000000206303916','2016-04-17 19:19:42'),(2,'498','com.heydo.lizi','1','1097285846','2016-04-17 11:20:56 Etc/GMT','1460892056424','2016-04-17 04:20:56 America/Los_Angeles','1000000206303925','030300500','2016-04-17 11:20:56 Etc/GMT','1460892056424','2016-04-17 04:20:56 America/Los_Angeles','1','1000000206303925','2016-04-17 19:21:04'),(3,'499','com.heydo.lizi','1','1097285846','2016-04-17 11:21:19 Etc/GMT','1460892079877','2016-04-17 04:21:19 America/Los_Angeles','1000000206303927','030300500','2016-04-17 11:21:19 Etc/GMT','1460892079877','2016-04-17 04:21:19 America/Los_Angeles','1','1000000206303927','2016-04-17 19:21:21'),(4,'501','com.heydo.lizi','1','1097285846','2016-04-17 11:25:15 Etc/GMT','1460892315407','2016-04-17 04:25:15 America/Los_Angeles','1000000206303940','030300500','2016-04-17 11:25:15 Etc/GMT','1460892315407','2016-04-17 04:25:15 America/Los_Angeles','1','1000000206303940','2016-04-17 19:25:17'),(5,'503','com.heydo.lizi','1','1095606147','2016-04-17 11:27:07 Etc/GMT','1460892427794','2016-04-17 04:27:07 America/Los_Angeles','1000000206303951','010060100','2016-04-17 11:27:07 Etc/GMT','1460892427794','2016-04-17 04:27:07 America/Los_Angeles','1','1000000206303951','2016-04-17 19:27:09'),(6,'504','com.heydo.lizi','1','1095606147','2016-04-17 11:27:17 Etc/GMT','1460892437057','2016-04-17 04:27:17 America/Los_Angeles','1000000206303952','010060100','2016-04-17 11:27:17 Etc/GMT','1460892437057','2016-04-17 04:27:17 America/Los_Angeles','1','1000000206303952','2016-04-17 19:27:19'),(7,'505','com.heydo.lizi','1','1095606147','2016-04-17 11:27:23 Etc/GMT','1460892443843','2016-04-17 04:27:23 America/Los_Angeles','1000000206303954','010060100','2016-04-17 11:27:23 Etc/GMT','1460892443843','2016-04-17 04:27:23 America/Los_Angeles','1','1000000206303954','2016-04-17 19:27:25'),(8,'506','com.heydo.lizi','1','1097285846','2016-04-17 11:35:55 Etc/GMT','1460892955818','2016-04-17 04:35:55 America/Los_Angeles','1000000206304000','030300500','2016-04-17 11:35:55 Etc/GMT','1460892955818','2016-04-17 04:35:55 America/Los_Angeles','1','1000000206304000','2016-04-17 19:35:57'),(9,'507','com.heydo.lizi','1','1095606147','2016-04-17 11:37:23 Etc/GMT','1460893043155','2016-04-17 04:37:23 America/Los_Angeles','1000000206304011','010060100','2016-04-17 11:37:23 Etc/GMT','1460893043155','2016-04-17 04:37:23 America/Los_Angeles','1','1000000206304011','2016-04-17 19:37:25'),(10,'508','com.heydo.lizi','1','1097285854','2016-04-17 11:37:40 Etc/GMT','1460893060858','2016-04-17 04:37:40 America/Los_Angeles','1000000206304012','040601000','2016-04-17 11:37:40 Etc/GMT','1460893060858','2016-04-17 04:37:40 America/Los_Angeles','1','1000000206304012','2016-04-17 19:37:43');
/*!40000 ALTER TABLE `customer_appleverifyresult` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer_businessstatistics`
--

DROP TABLE IF EXISTS `customer_businessstatistics`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `customer_businessstatistics` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `total` decimal(19,2) NOT NULL,
  `harvest_total` decimal(19,2) NOT NULL,
  `diamond_total` int(11) NOT NULL,
  `withdraw_ticket` int(11) NOT NULL,
  `withdraw_outflow` decimal(19,2) NOT NULL,
  `withdraw_inflow` decimal(19,2) NOT NULL,
  `ticket` int(11) NOT NULL,
  `diamond` int(11) NOT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer_businessstatistics`
--

LOCK TABLES `customer_businessstatistics` WRITE;
/*!40000 ALTER TABLE `customer_businessstatistics` DISABLE KEYS */;
/*!40000 ALTER TABLE `customer_businessstatistics` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer_gift`
--

DROP TABLE IF EXISTS `customer_gift`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `customer_gift` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) NOT NULL,
  `price` int(11) NOT NULL,
  `status` int(11) NOT NULL,
  `experience` int(11) NOT NULL,
  `ticket` int(11) NOT NULL,
  `continuity` int(11) NOT NULL,
  `animation_type` int(11) NOT NULL,
  `logo` varchar(256) NOT NULL,
  `is_flower` int(11) NOT NULL DEFAULT '0',
  `seq` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer_gift`
--

LOCK TABLES `customer_gift` WRITE;
/*!40000 ALTER TABLE `customer_gift` DISABLE KEYS */;
INSERT INTO `customer_gift` VALUES (1,'爱的城堡',2666,1,2666,2666,0,1,'http://facelive-10023919.image.myqcloud.com/1461047569_504d810bc9424deeea157b9edda77dd7',0,23),(2,'小火箭',19999,1,19999,19999,0,1,'http://facelive-10023919.image.myqcloud.com/1461047461_7a54eb056677e9dc15d9141fb35c90d9',0,25),(3,'烟火',1666,1,1666,1666,0,0,'http://facelive-10023919.image.myqcloud.com/1461047639_8bc7ece8b355baa9fa845d349c940c79',0,22),(4,'兰博基尼',5000,1,5000,5000,0,1,'http://facelive-10023919.image.myqcloud.com/1459843117_dc2f0cdc4a214ddf8e3d9c0725ee70c4',0,24),(5,'蓝色妖姬',99,1,99,99,0,0,'http://facelive-10023919.image.myqcloud.com/1459849932_af3ffcc6276fa120255806769386acc9',1,9),(6,'星空',521,1,521,521,0,0,'http://facelive-10023919.image.myqcloud.com/1461047751_380c7cacdf17621d1019e66f990688ec',0,20),(7,'桃花猫',66,1,66,66,1,0,'http://facelive-10023919.image.myqcloud.com/1459850034_e58706c74d2bf10964d0196b85e4d485',0,17),(8,'卡布奇诺',15,1,15,15,1,0,'http://facelive-10023919.image.myqcloud.com/1459850074_4a89298950dbe2699ff59af6a010c96a',0,16),(9,'小饼干',3,1,3,3,1,0,'http://facelive-10023919.image.myqcloud.com/1459850111_01e024adb8e80ae8fefc225a9f945c78',0,12),(10,'热气球',5,1,5,5,1,0,'http://facelive-10023919.image.myqcloud.com/1459850167_ac804a0852b2d5ebf3508634eb540f7b',0,14),(11,'冰淇淋',5,1,5,5,1,0,'http://facelive-10023919.image.myqcloud.com/1459850279_8ab68ce296763390477d103cc481f1ae',0,13),(12,'口红',10,1,10,10,1,0,'http://facelive-10023919.image.myqcloud.com/1459850314_473f58e5833292e811c66f74fe1402e5',0,15),(13,'棒棒糖',2,1,2,2,1,0,'http://facelive-10023919.image.myqcloud.com/1459850352_040d26acd37389c6e9608ba96527837d',0,11),(14,'情书',99,1,99,99,1,0,'http://facelive-10023919.image.myqcloud.com/1459850393_8bfd67d2aa9ba44fbf1cf9ee3d412e39',0,18),(15,'桃花',1,1,1,1,1,0,'http://facelive-10023919.image.myqcloud.com/1459850444_4234e4d86eeeecaac24c0d2e43c49a63',0,10),(16,'钻戒',299,1,299,299,1,0,'http://facelive-10023919.image.myqcloud.com/1459850477_e9496be040ef42e711c7377b46fcbf3b',0,19),(17,'流星',999,1,999,999,0,0,'http://facelive-10023919.image.myqcloud.com/1461047703_944548160d5789aadcad74c2de3a5586',0,21),(18,'百合花',2,1,2,2,0,0,'http://facelive-10023919.image.myqcloud.com/1460632307_f1c1934df074c9be6af2d44c373ed259',1,1),(19,'粉玫瑰',6,1,6,6,0,0,'http://facelive-10023919.image.myqcloud.com/1460632525_3fd619653ef95232b629f236cab7676f',1,6),(20,'蒲公英',5,1,5,5,0,0,'http://facelive-10023919.image.myqcloud.com/1460632547_0af2002aea2208363852e8467b8d35a5',1,5),(21,'红玫瑰',9,1,9,9,0,0,'http://facelive-10023919.image.myqcloud.com/1460632624_8390ee213a74321ad079573fbd3baf7d',1,8),(22,'四叶草',4,1,4,4,0,0,'http://facelive-10023919.image.myqcloud.com/1460632662_62ba194684075c0f71b5670c751b8087',1,3),(23,'向日葵',8,1,8,8,0,0,'http://facelive-10023919.image.myqcloud.com/1460632683_0b3f54164d7ed2157caeb3254365010f',1,7),(24,'薰衣草',3,1,3,3,0,0,'http://facelive-10023919.image.myqcloud.com/1460632760_be9a478273fe076b980bbfbbaf47611c',1,2),(25,'郁金香',4,1,4,4,0,0,'http://facelive-10023919.image.myqcloud.com/1460632811_109760342ba673d81129027138fc2174',1,4);
/*!40000 ALTER TABLE `customer_gift` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer_level`
--

DROP TABLE IF EXISTS `customer_level`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `customer_level` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) NOT NULL,
  `grade` int(11) NOT NULL,
  `status` int(11) NOT NULL,
  `experience` int(11) NOT NULL,
  `created_time` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `customer_level_d91b8533` (`grade`),
  KEY `customer_level_41e5f0d8` (`created_time`)
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer_level`
--

LOCK TABLES `customer_level` WRITE;
/*!40000 ALTER TABLE `customer_level` DISABLE KEYS */;
INSERT INTO `customer_level` VALUES (1,'P1',1,1,20,'2016-03-06 18:27:59'),(2,'P2',2,1,38,'2016-03-06 18:28:06'),(3,'P3',3,1,63,'2016-03-06 18:28:16'),(4,'P4',4,1,100,'2016-03-06 18:28:26'),(5,'P5',5,1,150,'2016-04-05 21:04:57'),(6,'P6',6,1,220,'2016-04-05 21:05:15'),(7,'P7',7,1,315,'2016-04-05 21:05:27'),(8,'P8',8,1,444,'2016-04-05 21:05:46'),(9,'P9',9,1,617,'2016-04-05 21:06:16'),(10,'P10',10,1,849,'2016-04-05 21:06:41'),(11,'P11',11,1,1158,'2016-04-19 15:17:13'),(12,'P12',12,1,1569,'2016-04-19 15:17:32'),(13,'P13',13,1,2113,'2016-04-19 15:17:42'),(14,'P14',14,1,2831,'2016-04-19 15:17:57'),(15,'P15',15,1,3775,'2016-04-19 15:18:14'),(16,'P16',16,1,5014,'2016-04-19 15:18:25'),(17,'P17',17,1,6637,'2016-04-19 15:18:34'),(18,'P18',18,1,8758,'2016-04-19 15:18:46'),(19,'P19',19,1,11525,'2016-04-19 15:18:56'),(20,'P20',20,1,15127,'2016-04-19 15:19:07'),(21,'P21',21,1,19809,'2016-04-19 15:19:20'),(22,'P22',22,1,25888,'2016-04-19 15:19:29'),(23,'P23',23,1,33768,'2016-04-19 15:19:43'),(24,'P24',24,1,43969,'2016-04-19 15:19:54'),(25,'P25',25,1,57160,'2016-04-19 15:20:08'),(26,'P26',26,1,74199,'2016-04-19 15:20:19'),(27,'P27',27,1,96184,'2016-04-19 15:20:31'),(28,'P28',28,1,124525,'2016-04-19 15:20:44'),(29,'P29',29,1,161025,'2016-04-19 15:20:56'),(30,'P30',30,1,207991,'2016-04-19 15:21:10'),(31,'P31',31,1,268376,'2016-04-19 15:21:29'),(32,'P32',32,1,345954,'2016-04-19 15:21:43'),(33,'P33',33,1,445547,'2016-04-19 15:21:59'),(34,'P34',34,1,573315,'2016-04-19 15:22:10'),(35,'P35',35,1,737120,'2016-04-19 15:22:22'),(36,'P36',36,1,946995,'2016-04-19 15:22:33'),(37,'P37',37,1,1215738,'2016-04-19 15:22:49'),(38,'P38',38,1,1559664,'2016-04-19 15:23:01'),(39,'P39',39,1,1999570,'2016-04-19 15:23:11'),(40,'P40',40,1,2561950,'2016-04-19 15:23:26'),(41,'P41',41,1,3280546,'2016-04-19 15:23:37'),(42,'P42',42,1,4198319,'2016-04-19 15:24:00'),(43,'P43',43,1,5369943,'2016-04-19 15:24:20'),(44,'P44',44,1,6864985,'2016-04-19 15:24:38'),(45,'P45',45,1,8771925,'2016-04-19 15:24:49'),(46,'P46',46,1,11203275,'2016-04-19 15:25:03'),(47,'P47',47,1,14302054,'2016-04-19 15:25:15'),(48,'P48',48,1,18250017,'2016-04-19 15:25:29'),(49,'P49',49,1,23278084,'2016-04-19 15:25:41'),(50,'P50',50,1,29679558,'2016-04-19 15:25:55');
/*!40000 ALTER TABLE `customer_level` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer_rankcontributeuser`
--

DROP TABLE IF EXISTS `customer_rankcontributeuser`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `customer_rankcontributeuser` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `contribute_user_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `total_ticket` int(11) NOT NULL,
  `experience` int(11) NOT NULL,
  `cost` int(11) NOT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `customer_rankcontributeuser_517dc05a` (`contribute_user_id`),
  KEY `customer_rankcontributeuser_6340c63c` (`user_id`),
  KEY `customer_rankcontributeuser_96511a37` (`created_at`),
  CONSTRAINT `contribute_user_id_refs_id_5d44764d` FOREIGN KEY (`contribute_user_id`) REFERENCES `customer_user` (`id`),
  CONSTRAINT `user_id_refs_id_5d44764d` FOREIGN KEY (`user_id`) REFERENCES `customer_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer_rankcontributeuser`
--

LOCK TABLES `customer_rankcontributeuser` WRITE;
/*!40000 ALTER TABLE `customer_rankcontributeuser` DISABLE KEYS */;
INSERT INTO `customer_rankcontributeuser` VALUES (1,165,229,743,743,743,'2016-04-29 15:42:53'),(2,236,165,5521,5521,5521,'2016-04-29 15:47:02'),(3,236,230,2666,2666,2666,'2016-04-29 15:52:26'),(4,225,209,52,52,52,'2016-04-29 16:23:04'),(5,241,244,5017,5017,5017,'2016-05-03 14:53:55'),(6,241,165,111,111,111,'2016-05-03 15:21:59'),(7,225,245,1091,1091,1091,'2016-05-03 17:34:26'),(8,241,170,2669,2669,2669,'2016-05-03 19:48:28'),(9,241,229,3,3,3,'2016-05-03 21:17:35');
/*!40000 ALTER TABLE `customer_rankcontributeuser` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer_report`
--

DROP TABLE IF EXISTS `customer_report`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `customer_report` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `reportor_id` int(11) NOT NULL,
  `wrongdoer_id` int(11) NOT NULL,
  `liveRoom_id` int(11) NOT NULL,
  `description` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `result` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `status` int(11) NOT NULL,
  `created_time` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `customer_report_af9d5c41` (`reportor_id`),
  KEY `customer_report_35f2d103` (`wrongdoer_id`),
  KEY `customer_report_6aad92d2` (`liveRoom_id`),
  KEY `customer_report_41e5f0d8` (`created_time`),
  CONSTRAINT `liveRoom_id_refs_id_ad539a01` FOREIGN KEY (`liveRoom_id`) REFERENCES `live_liveroom` (`id`),
  CONSTRAINT `reportor_id_refs_id_2acd6c9d` FOREIGN KEY (`reportor_id`) REFERENCES `customer_user` (`id`),
  CONSTRAINT `wrongdoer_id_refs_id_2acd6c9d` FOREIGN KEY (`wrongdoer_id`) REFERENCES `customer_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer_report`
--

LOCK TABLES `customer_report` WRITE;
/*!40000 ALTER TABLE `customer_report` DISABLE KEYS */;
/*!40000 ALTER TABLE `customer_report` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer_startupimage`
--

DROP TABLE IF EXISTS `customer_startupimage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `customer_startupimage` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `status` int(11) NOT NULL,
  `image` varchar(256) NOT NULL,
  `url` varchar(256) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer_startupimage`
--

LOCK TABLES `customer_startupimage` WRITE;
/*!40000 ALTER TABLE `customer_startupimage` DISABLE KEYS */;
INSERT INTO `customer_startupimage` VALUES (1,0,'http://picture01-10022394.image.myqcloud.com/1457425929_6c4944dd6b1347651e4aca33c472149c','http://wx.mi.youku.com/i/c'),(2,0,'http://facelive-10023919.image.myqcloud.com/1460966136_8e5ce104ca6c3cb51b821159124acda1','');
/*!40000 ALTER TABLE `customer_startupimage` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer_thridpard`
--

DROP TABLE IF EXISTS `customer_thridpard`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `customer_thridpard` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `weixin_openid` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `weixin_access_token` longtext COLLATE utf8mb4_unicode_ci,
  `sina_openid` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `sina_access_token` longtext COLLATE utf8mb4_unicode_ci,
  `qq_openid` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `qq_access_token` longtext COLLATE utf8mb4_unicode_ci,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  KEY `customer_thridpard_cea95e79` (`weixin_openid`),
  KEY `customer_thridpard_fc46bebf` (`sina_openid`),
  KEY `customer_thridpard_6864beb9` (`qq_openid`),
  CONSTRAINT `user_id_refs_id_ce571766` FOREIGN KEY (`user_id`) REFERENCES `customer_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer_thridpard`
--

LOCK TABLES `customer_thridpard` WRITE;
/*!40000 ALTER TABLE `customer_thridpard` DISABLE KEYS */;
INSERT INTO `customer_thridpard` VALUES (1,165,'329C7D5F974323B07FDFADBC34352DBB','FA5E99B33C1F2DC4E0FFA350D8C3DA0B',NULL,NULL,NULL,NULL),(2,166,'1E88998DB1F1CA96DE4A79750DC5C05E','1E73E89EB6C19D8FF5C4507989F3D45C',NULL,NULL,NULL,NULL),(3,168,'B25B280E8A5FBD39B7BAD9C7CECAEB9E','A20AADEEB5FA5CC9888D63CC7F49CDD2',NULL,NULL,NULL,NULL),(4,169,'FD9D0EAAAB6A240F9886815FEA0FD6BA','88982F4977D25C926B1145E0D207D6D0',NULL,NULL,NULL,NULL),(5,170,'21119F614C16FFDDC97C00BF45CD8E0C','E6A2D15A45441F495801424F83F89E1F',NULL,NULL,NULL,NULL),(6,171,'oq8Dvs4M9vQ8nzWHltg9oGYBggBM','OezXcEiiBSKSxW0eoylIeODb-NDdJA8evRJ73cQZI9dsE01EnotY4xXGESuNiq2AbgtPje_Ni7E2CvTHmNDRD1nbjruPDPMsZXiwzbsvmxe7GBSmiIS_0IXxTydEnRlep2Hj4BiV8Tgixjur4m6g-A',NULL,NULL,NULL,NULL),(7,172,'E9C0E7376C67E99AEA76CD58D295CCDA','E3FB29F3135E07D9AA2117E45F5DB6EC',NULL,NULL,NULL,NULL),(8,173,'oq8Dvs9gXT0IHivYcMAVORjD6cPM','OezXcEiiBSKSxW0eoylIeODb-NDdJA8evRJ73cQZI9c9S7JhTUMRmRBzd44KcasUAMf7QIvwospb1YmMtkTgKm_oRvrv88IWpzv9kReGyvvM-t4OCA5MvAuDPScv22nravSOAvX3f4XbbpxZp06y-w',NULL,NULL,NULL,NULL),(9,178,'CB01F153EAA6C22A5008A3F2D4E5E6D4','FB2851856F6CE13A3E964F16560919D2',NULL,NULL,NULL,NULL),(10,183,'o26BPwQr-1N-biWAc1aTpKbxMWIw','56J2GiZmD08wwnypViE5qwP-xIVyr6SV2gmRsHhkZpcaAR_ZpEiN08ka_v5ZELfypNvbuKQ9hbLR98vNFK01dUvB32RMFrb1oaQgfbLHeFI_C_xaR4qWQCYsQkibMAgLRWEiACAYDL',NULL,NULL,NULL,NULL),(11,185,'o26BPwVfgxBhL2QC3MtTvWNNYSK8','56J2GiZmD08wwnypViE5qwP-xIVyr6SV2gmRsHhkZpcaAR_ZpEiN08ka_v5ZELfypNvbuKQ9hbLR98vNFK01dUvB32RMFrb1oaQgfbLHeFI_C_xaR4qWQCYsQkibMAgLRWEiACAYDL',NULL,NULL,NULL,NULL),(12,209,'oq8DvswJ0cfSrIpmiYOPxUHBHw1s','OezXcEiiBSKSxW0eoylIeODb-NDdJA8evRJ73cQZI9fHlK20Jknmw1C0RrOj1OJ4UHpFlx_ALoMm8dY_GJrT-uf2WqHUD05gpXxjsQtNwDK0DrACnwWunPKdGXrBpa32M-3K9WayoHMvVwK-sM2ciQ',NULL,NULL,NULL,NULL),(13,225,'39022AD1F273A6FDB451EE06C6523F13','C46352BA0A5A91022C614AEF39E985A0',NULL,NULL,NULL,NULL),(14,226,'9AFF1B06DD00DC75D114763F101003E0','53C808DA458515865862C53D98043040',NULL,NULL,NULL,NULL),(15,227,'o26BPwchoXh96Cjfk0-LabvpfdjE','56J2GiZmD08wwnypViE5qwP-xIVyr6SV2gmRsHhkZpcaAR_ZpEiN08ka_v5ZELfypNvbuKQ9hbLR98vNFK01dUvB32RMFrb1oaQgfbLHeFI_C_xaR4qWQCYsQkibMAgLRWEiACAYDL',NULL,NULL,NULL,NULL),(16,228,'oq8DvsxxHk-gNpLykOuhN6iJ_Mns','OezXcEiiBSKSxW0eoylIeODb-NDdJA8evRJ73cQZI9d5iZe7Mo_jDaiXbJIPOBST-pTTPWI-pr0gglXme8ytDFkpd77ItjHducEx_f0OWaZQipzDBI42bzjRuKY5k1kdGmD_hh_tPOQBlo6aj2q9Zw',NULL,NULL,NULL,NULL),(17,229,'2F25F60BBA58CB887F59D007E0EAD14A','52D55356CB1DFA9D57424313CD6B6B52',NULL,NULL,NULL,NULL),(18,230,'8BF53B942416280C2222BA064ACE750B','8F6DC75F366DC39B86A7C42F03E473BA',NULL,NULL,NULL,NULL),(19,231,'oq8Dvs02FDnXPyA3ryrdbNfbJBWQ','OezXcEiiBSKSxW0eoylIeODb-NDdJA8evRJ73cQZI9cPhSdPG8fuROFMc3izLuXUvpc6x2iLDmgSG-_ByOXekhs4zQv2YuMdXyZ1pPTlmTbJcty4XW3IVgM5XnODvc8cHyOwtTuj9jc7SICymsaZ8w',NULL,NULL,NULL,NULL),(20,232,'oq8Dvs7BqSEk4RFC0plq_O_MqSy8','OezXcEiiBSKSxW0eoylIeODb-NDdJA8evRJ73cQZI9fkjtWODkRxN1dIZ1764OMBPWwf8abonk4N5CNdequUkeF9SLu4xqufN3zrlvd2QtBnF8Yiv4IJ68ihSP4hJQ8r_pu4Sl4Kuz4YHVYZkRtZMQ',NULL,NULL,NULL,NULL),(21,233,'o26BPwchoXh96Cjfk0-LabvpfdjE','rAa6GEGS3TErYFlSdyrixaqpDCOaxC5SyDvKMbenHrfaAu5K-GaAoSHPN40unnO6xRYZAVEN90x2J2J5TJz4-04utCqo3aowJDv2uWrV_Im3rc4t3fEyh9huV3FcYAKAKANaAJAYOB',NULL,NULL,NULL,NULL),(22,234,'oq8Dvs02FDnXPyA3ryrdbNfbJBWQ','OezXcEiiBSKSxW0eoylIeODb-NDdJA8evRJ73cQZI9cPhSdPG8fuROFMc3izLuXUvpc6x2iLDmgSG-_ByOXekhs4zQv2YuMdXyZ1pPTlmTbJcty4XW3IVgM5XnODvc8cHyOwtTuj9jc7SICymsaZ8w',NULL,NULL,NULL,NULL),(23,235,'o26BPwQmgSAg6kVxDyFp2dARkJ_c','2tQ606EF9NhevP7VIqnGJ2Mw_PDY3_HhpTCn-Pq2eHuNnu4TOFV9neMQIl8FEmTQS2lVXa-NrSxT8cT3t8KIqtbBvAtNdkR5MVhFWA9Y-IPraGM7ba8-n-xHOAuNFzayIYQjADAZPH',NULL,NULL,NULL,NULL),(24,236,'o26BPwVfgxBhL2QC3MtTvWNNYSK8','2tQ606EF9NhevP7VIqnGJ2Mw_PDY3_HhpTCn-Pq2eHuNnu4TOFV9neMQIl8FEmTQS2lVXa-NrSxT8cT3t8KIqtbBvAtNdkR5MVhFWA9Y-IPraGM7ba8-n-xHOAuNFzayIYQjADAZPH',NULL,NULL,NULL,NULL),(25,237,'oq8Dvs9gXT0IHivYcMAVORjD6cPM','OezXcEiiBSKSxW0eoylIeODb-NDdJA8evRJ73cQZI9c9S7JhTUMRmRBzd44KcasUDTgY5fXVjYSKpdDrf7btpncRZjeZIbcchf4rvNoPxxuYi9CkOibcrl_Jgy0vtgzZLHnwFLiLxJNRf-obvunavA',NULL,NULL,NULL,NULL),(26,238,'oq8Dvs1DYFxL9RsMwkhsjNYveA3k','OezXcEiiBSKSxW0eoylIeODb-NDdJA8evRJ73cQZI9dR0gLdw06mjXwdG_GOI7e9Aa8gAfE2u6f6def_kZNBV9gkwArxmbIlwi4SzDAsU04c7vXFLDQQBbNgH3vZrBa3Ot0EbJoVjTEtOeU7GHUMbw',NULL,NULL,NULL,NULL),(27,239,'o26BPwfpaFS0PO_v1QC-fgswDtOY','BEk3dOiogv-P1ojmkUOf1tHnEln21Am8Y5QEuf2tNjl40aHiG_x__rj-tuYxTQ4KwEAiWjDLGKiUR0WPszFmALLYooiKC1tB3dLU2YyN7yrLYluTpT2kYXfsPbpY9r-IALGfAAANYT',NULL,NULL,NULL,NULL),(28,240,'61E343CF1906F9DE17303CFFD9920B46','2ABBF09AF605CBEB9F988B66A8790002',NULL,NULL,NULL,NULL),(29,241,'oq8Dvs4M9vQ8nzWHltg9oGYBggBM','OezXcEiiBSKSxW0eoylIeODb-NDdJA8evRJ73cQZI9dsE01EnotY4xXGESuNiq2A8mu3LeZavZlwVMVsNRr-4GLIJ-6EL29p3liHa9eY1IvzyLFbmIs0jnYFP_hlNH0GdqDciDr2UAeaQt2krkkgAw',NULL,NULL,NULL,NULL),(30,242,'oq8DvsxVdzQT9pyhfmdTpxKfIfTg','OezXcEiiBSKSxW0eoylIeODb-NDdJA8evRJ73cQZI9eeqFEtS7l2swNi2I4vqQaRJJjj2hqQMZaohlr8ELZPzFhymodrqPRg_7uP91d0tUjiupczLjji1UCUBIid6z2Mrg9b5uSk5W9LT1D5hCvOGA',NULL,NULL,NULL,NULL),(31,243,'080C0F9D045D1A1D82C558EF9BE97493','DF05530BB38B83B426FBB3E3837B2118',NULL,NULL,NULL,NULL),(32,244,'oq8DvswJ0cfSrIpmiYOPxUHBHw1s','OezXcEiiBSKSxW0eoylIeODb-NDdJA8evRJ73cQZI9fHlK20Jknmw1C0RrOj1OJ4tlfDAwiBTUFb_DldR1VpkkktoiHLsi0v6BXMRjJGCx9e_qTmInv6mG_dLCSZbFMTNBLejsNASg0aB_m37evImw',NULL,NULL,NULL,NULL),(33,245,'F31247F857309E5B39C872B3ED441A9F','D0114C5671D119289635B5672D21B0A2',NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `customer_thridpard` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer_tradebalanceorder`
--

DROP TABLE IF EXISTS `customer_tradebalanceorder`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `customer_tradebalanceorder` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `rule_id` int(11) NOT NULL,
  `diamon` int(11) NOT NULL,
  `money` int(11) NOT NULL,
  `desc` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `buy_time` datetime NOT NULL,
  `filled_time` datetime DEFAULT NULL,
  `trade_type` int(11) NOT NULL,
  `fill_in_type` int(11) NOT NULL,
  `platform` int(11) NOT NULL,
  `status` int(11) NOT NULL,
  `order_id` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `out_order_id` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `order_id` (`order_id`),
  UNIQUE KEY `out_order_id` (`out_order_id`),
  KEY `customer_tradebalanceorder_6340c63c` (`user_id`),
  KEY `customer_tradebalanceorder_fb21b565` (`rule_id`),
  KEY `customer_tradebalanceorder_beeb1022` (`buy_time`),
  KEY `customer_tradebalanceorder_24267cf5` (`filled_time`),
  CONSTRAINT `rule_id_refs_id_1cf79518` FOREIGN KEY (`rule_id`) REFERENCES `customer_tradebalancerule` (`id`),
  CONSTRAINT `user_id_refs_id_6acef6dc` FOREIGN KEY (`user_id`) REFERENCES `customer_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1015 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer_tradebalanceorder`
--

LOCK TABLES `customer_tradebalanceorder` WRITE;
/*!40000 ALTER TABLE `customer_tradebalanceorder` DISABLE KEYS */;
INSERT INTO `customer_tradebalanceorder` VALUES (1,227,3,1,1,'充值创建订单','2016-04-29 10:41:47',NULL,0,3,4,0,NULL,NULL),(2,227,3,1,1,'充值创建订单','2016-04-29 10:42:00',NULL,0,3,4,0,NULL,NULL),(3,227,3,1,1,'充值创建订单','2016-04-29 10:43:24',NULL,0,3,4,0,NULL,NULL),(4,227,3,1,1,'充值创建订单','2016-04-29 10:43:26',NULL,0,3,4,0,NULL,NULL),(5,227,3,1,1,'充值创建订单','2016-04-29 10:44:59',NULL,0,3,4,0,NULL,NULL),(6,227,3,1,1,'充值创建订单','2016-04-29 10:50:36',NULL,0,3,4,0,NULL,NULL),(7,227,3,1,1,'充值创建订单','2016-04-29 10:50:55',NULL,0,3,4,0,NULL,NULL),(8,227,3,1,1,'充值创建订单','2016-04-29 10:51:09',NULL,0,3,4,0,NULL,NULL),(1000,227,3,1,1,'充值创建订单','2016-04-29 11:04:58','2016-04-29 11:05:07',0,3,4,1,NULL,NULL),(1001,167,3,1,1,'充值创建订单','2016-04-29 12:44:38','2016-04-29 12:44:44',0,3,4,1,NULL,NULL),(1002,167,3,1,1,'充值创建订单','2016-04-29 12:51:15','2016-04-29 12:51:26',0,3,4,1,NULL,NULL),(1003,165,3,10000,1,'充值创建订单','2016-04-29 15:41:35','2016-04-29 15:41:44',0,1,1,1,NULL,NULL),(1004,229,3,10000,1,'充值创建订单','2016-04-29 15:45:57',NULL,0,1,1,0,NULL,NULL),(1005,236,3,10000,1,'充值创建订单','2016-04-29 15:46:04','2016-04-29 15:46:08',0,1,1,1,NULL,NULL),(1006,225,3,10000,1,'充值创建订单','2016-04-29 16:21:23','2016-04-29 16:21:27',0,1,1,1,NULL,NULL),(1007,238,3,10000,1,'充值创建订单','2016-04-29 19:58:03',NULL,0,1,1,0,NULL,NULL),(1008,170,1,100,100,'充值创建订单','2016-04-29 19:58:37',NULL,0,2,2,0,NULL,NULL),(1009,229,3,10000,1,'充值创建订单','2016-04-29 20:13:48',NULL,0,1,1,0,NULL,NULL),(1010,166,1,100,100,'充值创建订单','2016-04-29 21:40:00',NULL,0,2,2,0,NULL,NULL),(1011,241,3,10000,1,'充值创建订单','2016-04-30 11:19:24','2016-04-30 11:19:33',0,1,1,1,NULL,NULL),(1012,239,3,10000,1,'充值创建订单','2016-05-03 16:55:13',NULL,0,3,4,0,NULL,NULL),(1013,239,3,10000,1,'充值创建订单','2016-05-03 16:55:15',NULL,0,3,4,0,NULL,NULL),(1014,229,3,10000,1,'充值创建订单','2016-05-03 18:44:51',NULL,0,1,1,0,NULL,NULL);
/*!40000 ALTER TABLE `customer_tradebalanceorder` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer_tradebalancerule`
--

DROP TABLE IF EXISTS `customer_tradebalancerule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `customer_tradebalancerule` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `money` int(11) NOT NULL,
  `diamon` int(11) NOT NULL,
  `free_diamon` int(11) NOT NULL,
  `desc` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `apple_product_id` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `update_time` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `customer_tradebalancerule_27069bb5` (`money`),
  KEY `customer_tradebalancerule_c3bd43a2` (`update_time`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer_tradebalancerule`
--

LOCK TABLES `customer_tradebalancerule` WRITE;
/*!40000 ALTER TABLE `customer_tradebalancerule` DISABLE KEYS */;
INSERT INTO `customer_tradebalancerule` VALUES (1,600,100,0,'10元大礼包','010060100','2016-03-29 16:03:28'),(2,1200,200,0,'120元大礼包','020120200','2016-03-29 16:01:36'),(3,1,10000,0,'1分测试','010060100','2016-04-29 13:56:17'),(4,3000,500,0,'30大礼包','030300500','2016-03-29 16:01:33'),(5,6000,1000,0,'60大礼包','040601000','2016-03-29 16:02:04'),(6,16800,2800,0,'168大礼包','051682800','2016-04-29 16:14:17');
/*!40000 ALTER TABLE `customer_tradebalancerule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer_tradediamondrecord`
--

DROP TABLE IF EXISTS `customer_tradediamondrecord`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `customer_tradediamondrecord` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `before_balance` int(11) NOT NULL,
  `after_balance` int(11) NOT NULL,
  `diamon` int(11) NOT NULL,
  `desc` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_time` datetime NOT NULL,
  `trade_type` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `customer_tradediamondrecord_6340c63c` (`user_id`),
  KEY `customer_tradediamondrecord_41e5f0d8` (`created_time`),
  CONSTRAINT `user_id_refs_id_b1d1c3fd` FOREIGN KEY (`user_id`) REFERENCES `customer_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=73 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer_tradediamondrecord`
--

LOCK TABLES `customer_tradediamondrecord` WRITE;
/*!40000 ALTER TABLE `customer_tradediamondrecord` DISABLE KEYS */;
INSERT INTO `customer_tradediamondrecord` VALUES (1,227,0,1,1,'充值','2016-04-29 11:05:07',0),(2,167,0,1,1,'充值','2016-04-29 12:44:44',0),(3,167,1,2,1,'充值','2016-04-29 12:51:26',0),(4,165,0,10000,10000,'充值','2016-04-29 15:41:44',0),(5,165,10000,9985,15,'购买礼物卡布奇诺','2016-04-29 15:42:53',1),(6,165,9985,9970,15,'购买礼物卡布奇诺','2016-04-29 15:42:55',1),(7,165,9970,9955,15,'购买礼物卡布奇诺','2016-04-29 15:42:56',1),(8,165,9955,9940,15,'购买礼物卡布奇诺','2016-04-29 15:42:56',1),(9,165,9940,9925,15,'购买礼物卡布奇诺','2016-04-29 15:42:56',1),(10,165,9925,9910,15,'购买礼物卡布奇诺','2016-04-29 15:42:57',1),(11,165,9910,9895,15,'购买礼物卡布奇诺','2016-04-29 15:42:57',1),(12,165,9895,9880,15,'购买礼物卡布奇诺','2016-04-29 15:42:57',1),(13,165,9880,9865,15,'购买礼物卡布奇诺','2016-04-29 15:42:57',1),(14,165,9865,9850,15,'购买礼物卡布奇诺','2016-04-29 15:42:57',1),(15,165,9850,9835,15,'购买礼物卡布奇诺','2016-04-29 15:42:58',1),(16,165,9835,9820,15,'购买礼物卡布奇诺','2016-04-29 15:42:58',1),(17,165,9820,9754,66,'购买礼物桃花猫','2016-04-29 15:43:00',1),(18,165,9754,9688,66,'购买礼物桃花猫','2016-04-29 15:43:00',1),(19,165,9688,9622,66,'购买礼物桃花猫','2016-04-29 15:43:00',1),(20,165,9622,9556,66,'购买礼物桃花猫','2016-04-29 15:43:01',1),(21,165,9556,9257,299,'购买礼物钻戒','2016-04-29 15:43:09',1),(22,236,0,10000,10000,'充值','2016-04-29 15:46:08',0),(23,236,10000,9479,521,'购买礼物星空','2016-04-29 15:47:01',1),(24,236,9479,4479,5000,'购买礼物兰博基尼','2016-04-29 15:48:17',1),(25,236,4479,1813,2666,'购买礼物爱的城堡','2016-04-29 15:52:26',1),(26,225,0,10000,10000,'充值','2016-04-29 16:21:27',0),(27,225,10000,9985,15,'购买礼物卡布奇诺','2016-04-29 16:23:04',1),(28,225,9985,9970,15,'购买礼物卡布奇诺','2016-04-29 16:23:25',1),(29,225,9970,9955,15,'购买礼物卡布奇诺','2016-04-29 16:23:30',1),(30,225,9955,9950,5,'购买礼物冰淇淋','2016-04-29 16:24:05',1),(31,225,9950,9948,2,'购买礼物棒棒糖','2016-04-29 16:26:04',1),(32,241,0,10000,10000,'充值','2016-04-30 11:19:33',0),(33,241,10000,9998,2,'购买礼物棒棒糖','2016-05-03 14:53:55',1),(34,241,9998,9995,3,'购买礼物小饼干','2016-05-03 14:53:58',1),(35,241,9995,9992,3,'购买礼物小饼干','2016-05-03 14:54:00',1),(36,241,9992,9987,5,'购买礼物冰淇淋','2016-05-03 14:54:02',1),(37,241,9987,4987,5000,'购买礼物兰博基尼','2016-05-03 14:54:23',1),(38,241,4987,4986,1,'购买礼物桃花','2016-05-03 14:56:07',1),(39,241,4986,4985,1,'购买礼物桃花','2016-05-03 14:59:23',1),(40,241,4985,4983,2,'购买礼物棒棒糖','2016-05-03 15:17:23',1),(41,241,4983,4981,2,'购买礼物棒棒糖','2016-05-03 15:21:59',1),(42,241,4981,4978,3,'购买礼物小饼干','2016-05-03 15:22:01',1),(43,241,4978,4973,5,'购买礼物冰淇淋','2016-05-03 15:22:02',1),(44,241,4973,4958,15,'购买礼物卡布奇诺','2016-05-03 15:22:06',1),(45,241,4958,4948,10,'购买礼物口红','2016-05-03 15:22:06',1),(46,241,4948,4938,10,'购买礼物口红','2016-05-03 15:22:07',1),(47,241,4938,4872,66,'购买礼物桃花猫','2016-05-03 15:22:08',1),(48,225,9948,8949,999,'购买礼物流星','2016-05-03 17:34:26',1),(49,225,8949,8948,1,'购买礼物桃花','2016-05-03 17:34:31',1),(50,225,8948,8946,2,'购买礼物桃花','2016-05-03 17:34:32',1),(51,225,8946,8943,3,'购买礼物桃花','2016-05-03 17:34:33',1),(52,225,8943,8939,4,'购买礼物桃花','2016-05-03 17:34:34',1),(53,225,8939,8934,5,'购买礼物桃花','2016-05-03 17:34:35',1),(54,225,8934,8928,6,'购买礼物桃花','2016-05-03 17:34:36',1),(55,225,8928,8921,7,'购买礼物桃花','2016-05-03 17:34:37',1),(56,225,8921,8913,8,'购买礼物桃花','2016-05-03 17:34:37',1),(57,225,8913,8904,9,'购买礼物桃花','2016-05-03 17:34:38',1),(58,225,8904,8894,10,'购买礼物桃花','2016-05-03 17:34:39',1),(59,225,8894,8893,1,'购买礼物桃花','2016-05-03 17:38:00',1),(60,225,8893,8891,2,'购买礼物桃花','2016-05-03 17:38:01',1),(61,225,8891,8888,3,'购买礼物桃花','2016-05-03 17:38:02',1),(62,225,8888,8884,4,'购买礼物桃花','2016-05-03 17:38:03',1),(63,225,8884,8879,5,'购买礼物桃花','2016-05-03 17:38:04',1),(64,225,8879,8873,6,'购买礼物桃花','2016-05-03 17:38:05',1),(65,225,8873,8866,7,'购买礼物桃花','2016-05-03 17:38:06',1),(66,225,8866,8858,8,'购买礼物桃花','2016-05-03 17:38:07',1),(67,225,8858,8857,1,'购买礼物桃花','2016-05-03 17:41:35',1),(68,241,4872,4871,1,'购买礼物桃花','2016-05-03 19:48:28',1),(69,241,4871,4869,2,'购买礼物棒棒糖','2016-05-03 19:48:32',1),(70,241,4869,2203,2666,'购买礼物爱的城堡','2016-05-03 19:48:37',1),(71,241,2203,2202,1,'购买礼物桃花','2016-05-03 21:17:35',1),(72,241,2202,2200,2,'购买礼物棒棒糖','2016-05-03 21:17:54',1);
/*!40000 ALTER TABLE `customer_tradediamondrecord` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer_tradeticketrecord`
--

DROP TABLE IF EXISTS `customer_tradeticketrecord`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `customer_tradeticketrecord` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `before_balance` int(11) NOT NULL,
  `after_balance` int(11) NOT NULL,
  `ticket` int(11) NOT NULL,
  `desc` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_time` datetime NOT NULL,
  `trade_type` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `customer_tradeticketrecord_6340c63c` (`user_id`),
  KEY `customer_tradeticketrecord_41e5f0d8` (`created_time`),
  CONSTRAINT `user_id_refs_id_83490645` FOREIGN KEY (`user_id`) REFERENCES `customer_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=73 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer_tradeticketrecord`
--

LOCK TABLES `customer_tradeticketrecord` WRITE;
/*!40000 ALTER TABLE `customer_tradeticketrecord` DISABLE KEYS */;
INSERT INTO `customer_tradeticketrecord` VALUES (1,229,0,15,15,'收到礼物卡布奇诺','2016-04-29 15:42:53',0),(2,229,0,15,15,'收到礼物卡布奇诺','2016-04-29 15:42:55',0),(3,229,0,15,15,'收到礼物卡布奇诺','2016-04-29 15:42:56',0),(4,229,0,15,15,'收到礼物卡布奇诺','2016-04-29 15:42:56',0),(5,229,0,15,15,'收到礼物卡布奇诺','2016-04-29 15:42:56',0),(6,229,0,15,15,'收到礼物卡布奇诺','2016-04-29 15:42:57',0),(7,229,0,15,15,'收到礼物卡布奇诺','2016-04-29 15:42:57',0),(8,229,0,15,15,'收到礼物卡布奇诺','2016-04-29 15:42:57',0),(9,229,0,15,15,'收到礼物卡布奇诺','2016-04-29 15:42:57',0),(10,229,0,15,15,'收到礼物卡布奇诺','2016-04-29 15:42:58',0),(11,229,0,15,15,'收到礼物卡布奇诺','2016-04-29 15:42:58',0),(12,229,0,15,15,'收到礼物卡布奇诺','2016-04-29 15:42:58',0),(13,229,0,66,66,'收到礼物桃花猫','2016-04-29 15:43:00',0),(14,229,0,66,66,'收到礼物桃花猫','2016-04-29 15:43:00',0),(15,229,0,66,66,'收到礼物桃花猫','2016-04-29 15:43:00',0),(16,229,0,66,66,'收到礼物桃花猫','2016-04-29 15:43:01',0),(17,229,0,299,299,'收到礼物钻戒','2016-04-29 15:43:09',0),(18,229,743,183,560,'提现','2016-04-29 15:44:12',3),(19,165,9257,9778,521,'收到礼物星空','2016-04-29 15:47:02',0),(20,165,9257,14257,5000,'收到礼物兰博基尼','2016-04-29 15:48:17',0),(21,165,5521,4961,560,'提现','2016-04-29 15:49:28',3),(22,165,4961,4401,560,'提现','2016-04-29 15:50:07',3),(23,230,0,2666,2666,'收到礼物爱的城堡','2016-04-29 15:52:26',0),(24,230,2666,2106,560,'提现','2016-04-29 15:52:51',3),(25,230,2106,1546,560,'提现','2016-04-29 15:55:00',3),(26,165,4401,3841,560,'提现','2016-04-29 16:14:26',3),(27,165,3841,3281,560,'提现','2016-04-29 16:21:11',3),(28,209,0,15,15,'收到礼物卡布奇诺','2016-04-29 16:23:04',0),(29,209,0,15,15,'收到礼物卡布奇诺','2016-04-29 16:23:25',0),(30,209,0,15,15,'收到礼物卡布奇诺','2016-04-29 16:23:30',0),(31,209,0,5,5,'收到礼物冰淇淋','2016-04-29 16:24:05',0),(32,209,0,2,2,'收到礼物棒棒糖','2016-04-29 16:26:04',0),(33,244,0,2,2,'收到礼物棒棒糖','2016-05-03 14:53:55',0),(34,244,0,3,3,'收到礼物小饼干','2016-05-03 14:53:58',0),(35,244,0,3,3,'收到礼物小饼干','2016-05-03 14:54:00',0),(36,244,0,5,5,'收到礼物冰淇淋','2016-05-03 14:54:02',0),(37,244,0,5000,5000,'收到礼物兰博基尼','2016-05-03 14:54:23',0),(38,244,0,1,1,'收到礼物桃花','2016-05-03 14:56:07',0),(39,244,0,1,1,'收到礼物桃花','2016-05-03 14:59:23',0),(40,244,0,2,2,'收到礼物棒棒糖','2016-05-03 15:17:23',0),(41,165,9257,9259,2,'收到礼物棒棒糖','2016-05-03 15:21:59',0),(42,165,9257,9260,3,'收到礼物小饼干','2016-05-03 15:22:02',0),(43,165,9257,9262,5,'收到礼物冰淇淋','2016-05-03 15:22:02',0),(44,165,9257,9272,15,'收到礼物卡布奇诺','2016-05-03 15:22:06',0),(45,165,9257,9267,10,'收到礼物口红','2016-05-03 15:22:06',0),(46,165,9257,9267,10,'收到礼物口红','2016-05-03 15:22:07',0),(47,165,9257,9323,66,'收到礼物桃花猫','2016-05-03 15:22:08',0),(48,245,0,999,999,'收到礼物流星','2016-05-03 17:34:26',0),(49,245,0,1,1,'收到礼物桃花','2016-05-03 17:34:31',0),(50,245,0,2,2,'收到礼物桃花','2016-05-03 17:34:32',0),(51,245,0,3,3,'收到礼物桃花','2016-05-03 17:34:33',0),(52,245,0,4,4,'收到礼物桃花','2016-05-03 17:34:34',0),(53,245,0,5,5,'收到礼物桃花','2016-05-03 17:34:35',0),(54,245,0,6,6,'收到礼物桃花','2016-05-03 17:34:36',0),(55,245,0,7,7,'收到礼物桃花','2016-05-03 17:34:37',0),(56,245,0,8,8,'收到礼物桃花','2016-05-03 17:34:37',0),(57,245,0,9,9,'收到礼物桃花','2016-05-03 17:34:38',0),(58,245,0,10,10,'收到礼物桃花','2016-05-03 17:34:39',0),(59,245,0,1,1,'收到礼物桃花','2016-05-03 17:38:00',0),(60,245,0,2,2,'收到礼物桃花','2016-05-03 17:38:01',0),(61,245,0,3,3,'收到礼物桃花','2016-05-03 17:38:02',0),(62,245,0,4,4,'收到礼物桃花','2016-05-03 17:38:03',0),(63,245,0,5,5,'收到礼物桃花','2016-05-03 17:38:04',0),(64,245,0,6,6,'收到礼物桃花','2016-05-03 17:38:05',0),(65,245,0,7,7,'收到礼物桃花','2016-05-03 17:38:06',0),(66,245,0,8,8,'收到礼物桃花','2016-05-03 17:38:07',0),(67,245,0,1,1,'收到礼物桃花','2016-05-03 17:41:35',0),(68,170,0,1,1,'收到礼物桃花','2016-05-03 19:48:28',0),(69,170,0,2,2,'收到礼物棒棒糖','2016-05-03 19:48:32',0),(70,170,0,2666,2666,'收到礼物爱的城堡','2016-05-03 19:48:37',0),(71,229,0,1,1,'收到礼物桃花','2016-05-03 21:17:35',0),(72,229,0,2,2,'收到礼物棒棒糖','2016-05-03 21:17:54',0);
/*!40000 ALTER TABLE `customer_tradeticketrecord` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer_user`
--

DROP TABLE IF EXISTS `customer_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `customer_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nickname` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `desc` varchar(20) COLLATE utf8mb4_bin NOT NULL,
  `phone` varchar(15) COLLATE utf8mb4_bin DEFAULT NULL,
  `email` varchar(75) COLLATE utf8mb4_bin DEFAULT NULL,
  `gender` int(11) DEFAULT NULL,
  `image` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `image_small` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `platform` int(11) NOT NULL,
  `longitude` double NOT NULL,
  `latitude` double NOT NULL,
  `area` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `ip` varchar(255) COLLATE utf8mb4_bin NOT NULL,
  `level_id` int(11) NOT NULL,
  `level_desc` varchar(10) COLLATE utf8mb4_bin NOT NULL,
  `last_experience` varchar(10) COLLATE utf8mb4_bin NOT NULL,
  `source` int(11) NOT NULL,
  `has_message_unread` int(11) NOT NULL,
  `experience` int(11) NOT NULL,
  `ticket` int(11) NOT NULL,
  `locked_ticket` int(12) DEFAULT '0',
  `cost` int(11) NOT NULL,
  `contribute_experience` int(11) NOT NULL,
  `contribute_ticket` int(11) NOT NULL,
  `created_at` datetime NOT NULL,
  `is_block` int(12) DEFAULT NULL,
  `identity` int(11) DEFAULT NULL,
  `province` varchar(20) COLLATE utf8mb4_bin DEFAULT NULL,
  `city` varchar(20) COLLATE utf8mb4_bin DEFAULT NULL,
  `country` varchar(20) COLLATE utf8mb4_bin DEFAULT NULL,
  `openid` varchar(64) COLLATE utf8mb4_bin DEFAULT NULL,
  `total_ticket` int(12) DEFAULT '0',
  `cid` varchar(128) COLLATE utf8mb4_bin DEFAULT '',
  `osver` varchar(10) COLLATE utf8mb4_bin DEFAULT '',
  `is_premium` int(11) NOT NULL DEFAULT '0',
  `first_purchase_at` datetime DEFAULT NULL,
  `first_gift_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `phone` (`phone`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `uk_t_1` (`identity`),
  UNIQUE KEY `index_customer_user_nick_open` (`nickname`,`openid`),
  KEY `customer_user_f8168153` (`nickname`),
  KEY `customer_user_b8f3f94a` (`level_id`),
  KEY `customer_user_96511a37` (`created_at`),
  KEY `customer_user_open_id` (`openid`),
  CONSTRAINT `level_id_refs_id_797b1ea6` FOREIGN KEY (`level_id`) REFERENCES `customer_level` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=246 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer_user`
--

LOCK TABLES `customer_user` WRITE;
/*!40000 ALTER TABLE `customer_user` DISABLE KEYS */;
INSERT INTO `customer_user` VALUES (165,'傻狍子','',NULL,NULL,NULL,'http://facelive-10023919.image.myqcloud.com/e30d7643e0ef638be63d0605f438937e','',0,0,0,'','125.33.204.70',17,'17','6637',3,0,6375,3392,2240,743,743,743,'2016-04-28 20:51:17',0,2000165,'吉林','长春',NULL,'329C7D5F974323B07FDFADBC34352DBB',5632,'c39dfd7a31d78dc12587fe66e4cc6330','4.4.4',0,NULL,'2016-04-29 15:42:53'),(166,'Manong','',NULL,NULL,NULL,'http://facelive-10023919.image.myqcloud.com/b1bfd37e9a321e2ff22bb986f19d9080','',1,0,0,'','125.33.204.70',1,'1','20',3,0,0,0,0,0,0,0,'2016-04-28 20:52:29',0,2000166,'北京','朝阳',NULL,'1E88998DB1F1CA96DE4A79750DC5C05E',0,'3cea90654e64f6996147c9e001e4aeed','9.3',0,NULL,NULL),(167,'test100','',NULL,NULL,1,'','',0,0,0,'','127.0.0.1',1,'1','20',100,0,0,0,0,0,0,0,'2016-04-28 20:52:35',0,2000167,'','','','1234567890',0,'','',0,NULL,NULL),(168,'Time。斤斤计较','',NULL,NULL,NULL,'http://facelive-10023919.image.myqcloud.com/a8f8ebf0e7dc5dfcf777830f146ec06f','',1,0,0,'','125.33.204.70',1,'1','20',3,0,0,0,0,0,0,0,'2016-04-28 21:08:35',0,2000168,'北京','海淀',NULL,'B25B280E8A5FBD39B7BAD9C7CECAEB9E',0,'6e365316e43a8060b638988aee4df5c8','9.3.1',0,NULL,NULL),(169,'甲乙','',NULL,NULL,NULL,'http://facelive-10023919.image.myqcloud.com/a5abdd32157684e272d1c43f8b3d9aa1','',0,0,0,'','125.33.204.70',1,'1','20',3,0,0,0,0,0,0,0,'2016-04-28 21:08:50',0,2000169,'北京','东城',NULL,'FD9D0EAAAB6A240F9886815FEA0FD6BA',0,'','4.4.4',0,NULL,NULL),(170,'Kris','',NULL,NULL,1,'http://facelive-10023919.image.myqcloud.com/4d591f64374604b81612521128d5343e','',1,0,0,'','125.33.204.70',14,'14','2831',3,0,2669,2669,0,0,0,0,'2016-04-28 21:30:06',0,2000170,'北京','海淀',NULL,'21119F614C16FFDDC97C00BF45CD8E0C',2669,'e1c874eeda76b5216e1bc76940bd6204','9.3.1',0,NULL,NULL),(171,'禅道','',NULL,NULL,1,'http://facelive-10023919.image.myqcloud.com/532bcac408b545eadac3df519665e266','',0,0,0,'','114.242.249.67',1,'1','20',1,0,0,0,0,0,0,0,'2016-04-28 21:30:40',0,2000171,'Beijing','East','CN','oq8Dvs4M9vQ8nzWHltg9oGYBggBM',0,'21cd37bd1c6c8bb67a1eeca385017bef','6.0.1',0,NULL,NULL),(172,'逗牛','',NULL,NULL,NULL,'http://facelive-10023919.image.myqcloud.com/a4b952ad7fe098b8c955ba37e3373e27','',1,0,0,'','114.245.107.14',1,'1','20',3,0,0,0,0,0,0,0,'2016-04-28 21:40:01',0,2000172,'北京','海淀',NULL,'E9C0E7376C67E99AEA76CD58D295CCDA',0,'','9.2.1',0,NULL,NULL),(173,'赵胜军@点客传媒','',NULL,NULL,1,'http://facelive-10023919.image.myqcloud.com/53eadfbb0bd15c3ea71e686ae5e64647','',1,0,0,'','123.116.48.238',1,'1','20',1,0,0,0,0,0,0,0,'2016-04-28 21:55:59',0,2000173,'Beijing','Chaoyang','CN','oq8Dvs9gXT0IHivYcMAVORjD6cPM',0,'','9.3.1',0,NULL,NULL),(178,'柯春林','',NULL,NULL,NULL,'http://facelive-10023919.image.myqcloud.com/a07367b07fe956a6825315171ad6d5c5','',0,0,0,'','123.206.49.67',1,'1','20',3,0,0,0,0,0,0,0,'2016-04-28 22:02:08',0,2000178,'','',NULL,'CB01F153EAA6C22A5008A3F2D4E5E6D4',0,'','',0,NULL,NULL),(183,'牛了个牛不好惹?','',NULL,NULL,2,'http://facelive-10023919.image.myqcloud.com/0fb2b303471e0e1455b0d862f1d276ea','',0,0,0,'','123.206.49.67',1,'1','20',1,0,0,0,0,0,0,0,'2016-04-29 09:39:49',0,2000183,'首尔','','韩国','o26BPwQr-1N-biWAc1aTpKbxMWIw',0,'','',0,NULL,NULL),(185,'黑洞小助理','',NULL,NULL,2,'http://facelive-10023919.image.myqcloud.com/06b10e47052be532e81bf0ecf9b56b1e','',0,0,0,'','123.206.49.67',1,'1','20',1,0,0,0,0,0,0,0,'2016-04-29 09:44:35',0,2000185,'','','中国','o26BPwVfgxBhL2QC3MtTvWNNYSK8',0,'','',0,NULL,NULL),(209,'牛了个牛不好惹?','',NULL,NULL,2,'http://facelive-10023919.image.myqcloud.com/60814cfdeba16e22d063c380740249d4','',1,0,0,'北京市','125.33.204.70',3,'3','63',1,0,52,52,0,0,0,0,'2016-04-29 09:57:55',0,2000209,'','','CN','oq8DvswJ0cfSrIpmiYOPxUHBHw1s',52,'71521c0cd0b1e18fc78f18c0cf90ab43','9.3.1',0,NULL,NULL),(225,'Rose','',NULL,NULL,2,'http://facelive-10023919.image.myqcloud.com/a11689d6-fb97-4578-8653-2e9d9f61196a','',1,0,0,'大北京','125.33.204.70',11,'11','1158',3,0,1070,0,0,1143,1143,1143,'2016-04-29 10:25:16',0,2000225,'上海','黄浦',NULL,'39022AD1F273A6FDB451EE06C6523F13',0,'','9.3.1',0,NULL,'2016-04-29 16:23:04'),(226,'emoji?','',NULL,NULL,NULL,'http://facelive-10023919.image.myqcloud.com/d6cf69aceefe3795333545bf3c3f3b71','',1,0,0,'','125.33.204.70',1,'1','20',3,0,0,0,0,0,0,0,'2016-04-29 10:35:00',0,2000226,'北京','东城',NULL,'9AFF1B06DD00DC75D114763F101003E0',0,'67f023cad2ffa9945d7ca83f36f58d6f','9.3.1',0,NULL,NULL),(227,'伟展','',NULL,NULL,1,'http://facelive-10023919.image.myqcloud.com/7b1b596d9534421af5946622633d0a5a','',0,0,0,'','123.206.49.67',1,'1','20',1,0,0,0,0,0,0,0,'2016-04-29 10:40:39',0,2000227,'北京','海淀','中国','o26BPwchoXh96Cjfk0-LabvpfdjE',0,'','',0,NULL,NULL),(228,'黑洞小助理','',NULL,NULL,2,'http://facelive-10023919.image.myqcloud.com/28f93a0e76f3e3809b224b9b903f2d02','',0,0,0,'','125.33.204.70',1,'1','20',1,0,0,0,0,0,0,0,'2016-04-29 10:54:17',0,2000228,'','','CN','oq8DvsxxHk-gNpLykOuhN6iJ_Mns',0,'','5.0.2',0,NULL,NULL),(229,'Milkee','',NULL,NULL,2,'http://facelive-10023919.image.myqcloud.com/bee1ce55-9221-4a7a-94ed-5eadbd2844db','',0,0,0,'爸爸','125.33.204.70',10,'10','849',3,0,746,186,560,0,0,0,'2016-04-29 11:02:51',0,2000229,'','费利杜',NULL,'2F25F60BBA58CB887F59D007E0EAD14A',746,'e1b642d581f7c0491161d593479c75d6','4.4.2',0,NULL,NULL),(230,'夢一场','',NULL,NULL,NULL,'http://facelive-10023919.image.myqcloud.com/1e7d73c0249c217de691d3498837540f','',0,0,0,'','125.33.204.70',14,'14','2831',3,0,2666,1546,1120,0,0,0,'2016-04-29 11:35:24',0,2000230,'','',NULL,'8BF53B942416280C2222BA064ACE750B',2666,'','5.0.2',0,NULL,NULL),(231,'小狍子','',NULL,NULL,0,'http://facelive-10023919.image.myqcloud.com/cdffefce592d0a248a0a39ea7ea436dd','',0,0,0,'','125.33.204.70',1,'1','20',1,0,0,0,0,0,0,0,'2016-04-29 12:11:42',0,2000231,'','','CN','oq8Dvs02FDnXPyA3ryrdbNfbJBWQ',0,'','',0,NULL,NULL),(232,'伟展','',NULL,NULL,1,'http://facelive-10023919.image.myqcloud.com/f7848ae50f5faf754de52e2b1e2be9ab','',1,0,0,'','123.116.91.21',1,'1','20',1,0,0,0,0,0,0,0,'2016-04-29 12:19:24',0,2000232,'Beijing','Haidian','CN','oq8Dvs7BqSEk4RFC0plq_O_MqSy8',0,'','9.2.1',0,NULL,NULL),(233,'伟展','',NULL,NULL,1,'http://facelive-10023919.image.myqcloud.com/ac5f4e82345499df36d3d73f41f317a7','',1,0,0,'','123.206.49.67',1,'1','20',1,0,0,0,0,0,0,0,'2016-04-29 12:43:23',0,2000233,'北京','海淀','中国','odjoSwSsfuP1lzETMcy4ZJmfPh4E',0,'ed209c4cdce42f5db36fa1b299fe2245','9.2.1',0,NULL,NULL),(234,'小狍子','',NULL,NULL,0,'http://facelive-10023919.image.myqcloud.com/6a80e61ccf716c4272a65ac319804ffa','',0,0,0,'','125.33.204.70',1,'1','20',1,0,0,0,0,0,0,0,'2016-04-29 13:20:37',0,2000234,'','','CN','odjoSwb5zg-he8ygJiGN_j07LaN4',0,'c39dfd7a31d78dc12587fe66e4cc6330','4.4.4',0,NULL,NULL),(235,'柳争','',NULL,NULL,1,'http://facelive-10023919.image.myqcloud.com/e450165195aab453c8a4cb2855df3a65','',0,0,0,'','123.206.49.67',1,'1','20',1,0,0,0,0,0,0,0,'2016-04-29 14:08:28',0,2000235,'北京','昌平','中国','odjoSwamnxQrr9lhZh2p3Ryf24xg',0,'','',0,NULL,NULL),(236,'黑洞小助理','',NULL,NULL,2,'http://facelive-10023919.image.myqcloud.com/87c4665f4dafcd40fc8826a62e9baf2a','',0,0,0,'','123.206.49.67',18,'18','8758',1,0,8187,0,0,8187,8187,8187,'2016-04-29 14:49:04',0,2000236,'','','中国','odjoSwWM7mG09d7mUCSyBsemRK5w',0,'','',0,NULL,'2016-04-29 15:47:02'),(237,'赵胜军@点客传媒','',NULL,NULL,1,'http://facelive-10023919.image.myqcloud.com/b48960b265fda73988188e64f6c25075','',1,0,0,'','114.242.249.7',1,'1','20',1,0,0,0,0,0,0,0,'2016-04-29 18:42:20',0,2000237,'Beijing','Chaoyang','CN','odjoSwRy3aPBnbCfMNarY0l_JVYE',0,'baa275eadc727974a0e5001f59f12c37','9.3.1',0,NULL,NULL),(238,'星辰','',NULL,NULL,1,'http://facelive-10023919.image.myqcloud.com/02eedacc767f93f0a95935e3a5fe2f13','',0,0,0,'','125.33.204.70',1,'1','20',1,0,0,0,0,0,0,0,'2016-04-29 19:04:42',0,2000238,'Beijing','East','CN','odjoSwbFFtZ7RGU_3jsZHoiXWf20',0,'21cd37bd1c6c8bb67a1eeca385017bef','6.0.1',0,NULL,NULL),(239,'Elina.晓倩','',NULL,NULL,2,'http://facelive-10023919.image.myqcloud.com/c784b82ef9118aa8926e3b48e6e3dcaf','',0,0,0,'','123.206.49.67',1,'1','20',1,0,0,0,0,0,0,0,'2016-04-29 19:53:05',0,2000239,'北京','海淀','中国','odjoSwQi3-L5S8FpN4JxWQoNNHX4',0,'','',0,NULL,NULL),(240,'你妈妈','',NULL,NULL,NULL,'http://facelive-10023919.image.myqcloud.com/b6471ff8607909c05b2a9e6971632f33','',0,0,0,'','123.206.49.67',1,'1','20',3,0,0,0,0,0,0,0,'2016-04-30 10:00:34',0,2000240,'四川','成都',NULL,'61E343CF1906F9DE17303CFFD9920B46',0,'','',0,NULL,NULL),(241,'禅道','',NULL,NULL,1,'http://facelive-10023919.image.myqcloud.com/8e28da7aa6c7291aab63332aed453078','',0,0,0,'','114.242.248.111',18,'18','8758',1,0,7800,0,0,7800,7800,7800,'2016-04-30 11:19:06',0,2000241,'Beijing','East','CN','odjoSwRn-zvGw-pyRBApXBYigpjc',0,'21cd37bd1c6c8bb67a1eeca385017bef','6.0.1',0,NULL,'2016-05-03 14:53:55'),(242,'小小','',NULL,NULL,2,'http://facelive-10023919.image.myqcloud.com/39daef3d342f55aa4365ec21f8fa5c89','',0,0,0,'','123.117.37.252',1,'1','20',1,0,0,0,0,0,0,0,'2016-04-30 17:41:02',0,2000242,'','','CN','odjoSwRzVHT31eEKom4snwswVyO4',0,'','',0,NULL,NULL),(243,'技术','',NULL,NULL,NULL,'http://facelive-10023919.image.myqcloud.com/227123026bdcf7a6943ff2211c6e836b','',0,0,0,'','14.131.2.47',1,'1','20',3,0,0,0,0,0,0,0,'2016-04-30 21:53:50',0,2000243,'广东','广州',NULL,'080C0F9D045D1A1D82C558EF9BE97493',0,'7dfc90aef132a725b0ebf93576c18295','5.0.2',0,NULL,NULL),(244,'牛了个牛不好惹?','',NULL,NULL,2,'http://facelive-10023919.image.myqcloud.com/4587fa702d3e6d34730aba8494d2154a','',1,0,0,'','61.51.131.224',17,'17','6637',1,0,5017,5017,0,0,0,0,'2016-05-03 11:06:49',0,2000244,'','','CN','odjoSwUQv_s4-MVxf2W4DY_MnlOs',5017,'71521c0cd0b1e18fc78f18c0cf90ab43','9.3.1',0,NULL,NULL),(245,'黑洞小助理','',NULL,NULL,NULL,'http://facelive-10023919.image.myqcloud.com/6c189978ead2517abd314dec49adb1f9','',0,0,0,'','61.51.131.224',11,'11','1158',3,0,1018,1091,0,0,0,0,'2016-05-03 11:45:28',0,2000245,'北京','东城',NULL,'F31247F857309E5B39C872B3ED441A9F',1091,'29840dd6d0a0fec3c33c05c89fd7ad12','5.0.2',0,NULL,NULL);
/*!40000 ALTER TABLE `customer_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer_userdypass`
--

DROP TABLE IF EXISTS `customer_userdypass`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `customer_userdypass` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uid` int(11) NOT NULL,
  `password` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uid` (`uid`),
  KEY `customer_userdypass_c74d05a8` (`password`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer_userdypass`
--

LOCK TABLES `customer_userdypass` WRITE;
/*!40000 ALTER TABLE `customer_userdypass` DISABLE KEYS */;
INSERT INTO `customer_userdypass` VALUES (1,1,'bcd30a717586'),(2,167,'de568a8ebd39'),(3,168,'5bbd88f2d953'),(4,166,'a022bfb5d610'),(5,170,'b20093212946');
/*!40000 ALTER TABLE `customer_userdypass` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer_userexperiencelog`
--

DROP TABLE IF EXISTS `customer_userexperiencelog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `customer_userexperiencelog` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ex_type_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `liveRoom_id` int(11) DEFAULT NULL,
  `experience` int(11) NOT NULL,
  `created_time` datetime NOT NULL,
  `idate` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `customer_userexperiencelog_56e750da` (`ex_type_id`),
  KEY `customer_userexperiencelog_6340c63c` (`user_id`),
  KEY `customer_userexperiencelog_6aad92d2` (`liveRoom_id`),
  KEY `customer_userexperiencelog_41e5f0d8` (`created_time`),
  KEY `customer_userexperiencelog_933a486e` (`idate`),
  CONSTRAINT `ex_type_id_refs_id_6e46ea67` FOREIGN KEY (`ex_type_id`) REFERENCES `customer_userexperiencetype` (`id`),
  CONSTRAINT `liveRoom_id_refs_id_1aa3ba9b` FOREIGN KEY (`liveRoom_id`) REFERENCES `live_liveroom` (`id`),
  CONSTRAINT `user_id_refs_id_b80da52f` FOREIGN KEY (`user_id`) REFERENCES `customer_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer_userexperiencelog`
--

LOCK TABLES `customer_userexperiencelog` WRITE;
/*!40000 ALTER TABLE `customer_userexperiencelog` DISABLE KEYS */;
/*!40000 ALTER TABLE `customer_userexperiencelog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer_userexperiencetype`
--

DROP TABLE IF EXISTS `customer_userexperiencetype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `customer_userexperiencetype` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `status` int(11) NOT NULL,
  `identifier` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `experience` int(11) NOT NULL,
  `limit_count` int(11) NOT NULL,
  `created_time` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `customer_userexperiencetype_41e5f0d8` (`created_time`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer_userexperiencetype`
--

LOCK TABLES `customer_userexperiencetype` WRITE;
/*!40000 ALTER TABLE `customer_userexperiencetype` DISABLE KEYS */;
INSERT INTO `customer_userexperiencetype` VALUES (1,'share',1,'分享',50,3,'2016-04-29 11:06:31');
/*!40000 ALTER TABLE `customer_userexperiencetype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer_userfollow`
--

DROP TABLE IF EXISTS `customer_userfollow`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `customer_userfollow` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `follower_id` int(11) NOT NULL,
  `followee_id` int(11) NOT NULL,
  `follow_time` datetime NOT NULL,
  `valid` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `follower_id` (`follower_id`,`followee_id`),
  KEY `customer_userfollow_c5e64013` (`follower_id`),
  KEY `customer_userfollow_9683117f` (`followee_id`),
  KEY `customer_userfollow_7b8ced7a` (`follow_time`),
  KEY `customer_userfollow_b7517c44` (`valid`),
  CONSTRAINT `followee_id_refs_id_619bbb8d` FOREIGN KEY (`followee_id`) REFERENCES `customer_user` (`id`),
  CONSTRAINT `follower_id_refs_id_619bbb8d` FOREIGN KEY (`follower_id`) REFERENCES `customer_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer_userfollow`
--

LOCK TABLES `customer_userfollow` WRITE;
/*!40000 ALTER TABLE `customer_userfollow` DISABLE KEYS */;
INSERT INTO `customer_userfollow` VALUES (1,170,171,'2016-04-28 21:32:42',0),(2,226,165,'2016-04-29 10:49:48',1),(3,165,226,'2016-04-29 10:51:45',1),(4,228,225,'2016-04-29 10:54:56',1),(5,225,228,'2016-04-29 10:55:04',1),(6,225,226,'2016-04-29 10:56:45',1),(7,228,226,'2016-04-29 10:58:04',1),(8,226,225,'2016-04-29 10:58:51',1),(9,226,228,'2016-04-29 10:58:53',1),(10,225,229,'2016-04-29 11:06:58',0),(11,225,170,'2016-04-29 11:21:06',1),(12,230,226,'2016-04-29 11:35:38',1),(13,226,230,'2016-04-29 11:39:51',1),(14,209,229,'2016-04-29 11:58:07',1),(15,234,228,'2016-04-29 13:25:08',1),(16,228,234,'2016-04-29 13:44:59',1),(17,166,228,'2016-04-29 13:48:01',0),(18,168,230,'2016-04-29 13:51:13',1),(19,209,230,'2016-04-29 13:56:51',1),(20,229,165,'2016-04-29 15:17:06',0),(21,165,229,'2016-04-29 17:40:09',1),(22,237,170,'2016-04-29 18:43:59',1),(23,229,209,'2016-05-03 13:53:22',1),(24,229,225,'2016-05-03 13:53:23',1),(25,244,245,'2016-05-03 14:47:23',0),(26,241,241,'2016-05-03 14:58:03',0),(27,170,241,'2016-05-03 15:03:07',0),(28,244,229,'2016-05-03 15:14:57',0),(29,244,241,'2016-05-03 15:15:01',0),(30,244,168,'2016-05-03 15:15:03',0),(31,244,170,'2016-05-03 15:15:05',0),(32,229,168,'2016-05-03 15:15:53',0),(33,170,237,'2016-05-03 19:47:14',1),(34,170,225,'2016-05-03 19:47:17',1),(35,170,229,'2016-05-03 21:18:35',1);
/*!40000 ALTER TABLE `customer_userfollow` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer_userfriends`
--

DROP TABLE IF EXISTS `customer_userfriends`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `customer_userfriends` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `friend_id` int(11) NOT NULL,
  `follow_time` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `customer_userfriends_6340c63c` (`user_id`),
  KEY `customer_userfriends_db2d0ac4` (`friend_id`),
  KEY `customer_userfriends_7b8ced7a` (`follow_time`),
  CONSTRAINT `friend_id_refs_id_8e902746` FOREIGN KEY (`friend_id`) REFERENCES `customer_user` (`id`),
  CONSTRAINT `user_id_refs_id_8e902746` FOREIGN KEY (`user_id`) REFERENCES `customer_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=47 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer_userfriends`
--

LOCK TABLES `customer_userfriends` WRITE;
/*!40000 ALTER TABLE `customer_userfriends` DISABLE KEYS */;
INSERT INTO `customer_userfriends` VALUES (1,165,226,1461898305),(2,226,165,1461898305),(7,226,228,1461898733),(8,228,226,1461898733),(9,225,226,1461900189),(10,226,225,1461900189),(11,226,230,1461901191),(12,230,226,1461901191),(21,234,228,1461909458),(22,228,234,1461909458),(23,225,228,1461920530),(24,228,225,1461920530),(41,170,237,1462276034),(42,237,170,1462276034),(43,170,225,1462276037),(44,225,170,1462276037),(45,229,209,1462283699),(46,209,229,1462283699);
/*!40000 ALTER TABLE `customer_userfriends` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer_usernotice`
--

DROP TABLE IF EXISTS `customer_usernotice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `customer_usernotice` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `to_user_id` int(11) NOT NULL,
  `notice_type` int(11) DEFAULT NULL,
  `created_at` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `customer_usernotice_6340c63c` (`user_id`),
  KEY `customer_usernotice_bc172800` (`to_user_id`),
  KEY `customer_usernotice_96511a37` (`created_at`),
  CONSTRAINT `to_user_id_refs_id_205463f2` FOREIGN KEY (`to_user_id`) REFERENCES `customer_user` (`id`),
  CONSTRAINT `user_id_refs_id_205463f2` FOREIGN KEY (`user_id`) REFERENCES `customer_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=65 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer_usernotice`
--

LOCK TABLES `customer_usernotice` WRITE;
/*!40000 ALTER TABLE `customer_usernotice` DISABLE KEYS */;
INSERT INTO `customer_usernotice` VALUES (1,170,171,1,1461850362),(2,226,165,1,1461898188),(3,165,226,1,1461898305),(4,228,225,1,1461898496),(5,225,228,1,1461898504),(6,225,226,1,1461898605),(7,228,226,1,1461898684),(8,226,225,1,1461898731),(9,226,228,1,1461898733),(10,225,229,1,1461899218),(11,225,170,1,1461900066),(12,225,226,1,1461900189),(13,230,226,1,1461900938),(14,230,226,1,1461901107),(15,230,226,1,1461901149),(16,230,226,1,1461901152),(17,226,230,1,1461901191),(18,226,230,1,1461901196),(19,209,229,1,1461902287),(20,209,229,1,1461902299),(21,209,229,1,1461902334),(22,234,228,1,1461907508),(23,228,234,1,1461908699),(24,228,234,1,1461908717),(25,166,228,1,1461908881),(26,168,230,1,1461909073),(27,168,230,1,1461909222),(28,209,230,1,1461909411),(29,234,228,1,1461909441),(30,234,228,1,1461909446),(31,234,228,1,1461909458),(32,229,165,1,1461914226),(33,225,229,1,1461920313),(34,225,229,1,1461920320),(35,225,229,1,1461920429),(36,225,229,1,1461920442),(37,225,228,1,1461920530),(38,165,229,1,1461922809),(39,237,170,1,1461926639),(40,229,209,1,1462254802),(41,229,225,1,1462254803),(42,229,209,1,1462256969),(43,229,225,1,1462256970),(44,229,209,1,1462257043),(45,229,209,1,1462257094),(46,229,225,1,1462257095),(47,244,245,1,1462258043),(48,241,241,1,1462258683),(49,241,241,1,1462258785),(50,170,241,1,1462258987),(51,244,229,1,1462259697),(52,244,241,1,1462259701),(53,244,168,1,1462259703),(54,244,170,1,1462259705),(55,229,168,1,1462259753),(56,229,165,1,1462261645),(57,165,229,1,1462262171),(58,225,170,1,1462262313),(59,170,237,1,1462276034),(60,170,225,1,1462276037),(61,170,229,1,1462281515),(62,229,209,1,1462283699),(63,229,209,1,1462283700),(64,229,209,1,1462283701);
/*!40000 ALTER TABLE `customer_usernotice` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer_userprivatemessage`
--

DROP TABLE IF EXISTS `customer_userprivatemessage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `customer_userprivatemessage` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sender_id` int(11) NOT NULL,
  `reciver_id` int(11) NOT NULL,
  `send_time` datetime NOT NULL,
  `content` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `status` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `customer_userprivatemessage_0a681a64` (`sender_id`),
  KEY `customer_userprivatemessage_9318a772` (`reciver_id`),
  KEY `customer_userprivatemessage_93ad473b` (`send_time`),
  CONSTRAINT `reciver_id_refs_id_bbbad6d7` FOREIGN KEY (`reciver_id`) REFERENCES `customer_user` (`id`),
  CONSTRAINT `sender_id_refs_id_bbbad6d7` FOREIGN KEY (`sender_id`) REFERENCES `customer_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer_userprivatemessage`
--

LOCK TABLES `customer_userprivatemessage` WRITE;
/*!40000 ALTER TABLE `customer_userprivatemessage` DISABLE KEYS */;
/*!40000 ALTER TABLE `customer_userprivatemessage` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer_usersummerymessage`
--

DROP TABLE IF EXISTS `customer_usersummerymessage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `customer_usersummerymessage` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sender_id` int(11) NOT NULL,
  `reciver_id` int(11) NOT NULL,
  `send_time` datetime NOT NULL,
  `read_time` datetime NOT NULL,
  `last_content` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `unread_count` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `customer_usersummerymessage_0a681a64` (`sender_id`),
  KEY `customer_usersummerymessage_9318a772` (`reciver_id`),
  KEY `customer_usersummerymessage_93ad473b` (`send_time`),
  KEY `customer_usersummerymessage_ac0f90a0` (`read_time`),
  CONSTRAINT `reciver_id_refs_id_20d21f01` FOREIGN KEY (`reciver_id`) REFERENCES `customer_user` (`id`),
  CONSTRAINT `sender_id_refs_id_20d21f01` FOREIGN KEY (`sender_id`) REFERENCES `customer_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer_usersummerymessage`
--

LOCK TABLES `customer_usersummerymessage` WRITE;
/*!40000 ALTER TABLE `customer_usersummerymessage` DISABLE KEYS */;
/*!40000 ALTER TABLE `customer_usersummerymessage` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer_wechatfillnotice`
--

DROP TABLE IF EXISTS `customer_wechatfillnotice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `customer_wechatfillnotice` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `out_trade_no` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `appid` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `bank_type` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `cash_fee` int(11) DEFAULT NULL,
  `fee_type` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `is_subscribe` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `mch_id` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `nonce_str` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `device_info` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `openid` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `result_code` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `return_code` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `sign` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `time_end` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `total_fee` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `trade_type` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `transaction_id` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `err_code_des` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `attach` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `coupon_fee` int(11) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `customer_wechatfillnotice_b3ce4aab` (`appid`),
  KEY `customer_wechatfillnotice_96511a37` (`created_at`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer_wechatfillnotice`
--

LOCK TABLES `customer_wechatfillnotice` WRITE;
/*!40000 ALTER TABLE `customer_wechatfillnotice` DISABLE KEYS */;
INSERT INTO `customer_wechatfillnotice` VALUES (1,'1000',NULL,'CFT',1,'CNY','Y','1322289701','l8d1wj0nvfzu36sx',NULL,'o26BPwchoXh96Cjfk0-LabvpfdjE','SUCCESS','SUCCESS','526E14498AF89E3084060B0B0F983A72','20160429110507',NULL,'JSAPI','4000062001201604295331350162',NULL,NULL,NULL,'2016-04-29 11:05:07'),(2,'1001',NULL,'CFT',1,'CNY','Y','1322289701','ou20jpzr1fst6yqg',NULL,'o26BPwchoXh96Cjfk0-LabvpfdjE','SUCCESS','SUCCESS','A715759EF8CF45C2967CC42250F96D3B','20160429124443',NULL,'JSAPI','4000062001201604295335231336',NULL,NULL,NULL,'2016-04-29 12:44:44'),(3,'1002',NULL,'CFT',1,'CNY','Y','1322289701','mtx5qsfep2nz613u',NULL,'o26BPwchoXh96Cjfk0-LabvpfdjE','SUCCESS','SUCCESS','ADA025951442B647F04FE683DBB73731','20160429125126',NULL,'JSAPI','4000062001201604295335362339',NULL,NULL,NULL,'2016-04-29 12:51:26'),(4,'1003',NULL,'CITIC_DEBIT',1,'CNY','N','1322576001','jtmcy5n78iguwd2x',NULL,'oq8Dvs02FDnXPyA3ryrdbNfbJBWQ','SUCCESS','SUCCESS','28AF76849D4C81135555690B29C10614','20160429154144',NULL,'APP','4008502001201604295340609946',NULL,NULL,NULL,'2016-04-29 15:41:44'),(5,'1005',NULL,'CFT',1,'CNY','N','1322576001','4tmvurioyfxeh8g6',NULL,'oq8DvsxxHk-gNpLykOuhN6iJ_Mns','SUCCESS','SUCCESS','619ED1CB6D00FFCCE14BA6A8EDD80B09','20160429154607',NULL,'APP','4003672001201604295340026062',NULL,NULL,NULL,'2016-04-29 15:46:08'),(6,'1006',NULL,'CFT',1,'CNY','N','1322576001','s4vhae1o2jyb8l0f',NULL,'oq8DvsxxHk-gNpLykOuhN6iJ_Mns','SUCCESS','SUCCESS','4348C81AD8BAC11A45FC3F45CAE06814','20160429162127',NULL,'APP','4003672001201604295341196116',NULL,NULL,NULL,'2016-04-29 16:21:27'),(7,'1011',NULL,'CFT',1,'CNY','N','1322576001','v8l305rjpoy7hgdk',NULL,'oq8Dvs4M9vQ8nzWHltg9oGYBggBM','SUCCESS','SUCCESS','631E33E63D9BE34CCA276D7021764C8E','20160430111932',NULL,'APP','4007092001201604305366378724',NULL,NULL,NULL,'2016-04-30 11:19:33');
/*!40000 ALTER TABLE `customer_wechatfillnotice` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer_wechatwithdrawresult`
--

DROP TABLE IF EXISTS `customer_wechatwithdrawresult`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `customer_wechatwithdrawresult` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `return_code` varchar(16) COLLATE utf8mb4_unicode_ci NOT NULL,
  `return_msg` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `mch_appid` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `mchid` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `device_info` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `nonce_str` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `result_code` varchar(16) COLLATE utf8mb4_unicode_ci NOT NULL,
  `err_code` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `err_code_des` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `partner_trade_no` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `payment_no` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `payment_time` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer_wechatwithdrawresult`
--

LOCK TABLES `customer_wechatwithdrawresult` WRITE;
/*!40000 ALTER TABLE `customer_wechatwithdrawresult` DISABLE KEYS */;
/*!40000 ALTER TABLE `customer_wechatwithdrawresult` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer_wexinjsverify`
--

DROP TABLE IF EXISTS `customer_wexinjsverify`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `customer_wexinjsverify` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `out_trade_no` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `pay_receipt` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime NOT NULL,
  `status` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `customer_wexinjsverify_c6fd446c` (`out_trade_no`),
  KEY `customer_wexinjsverify_96511a37` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer_wexinjsverify`
--

LOCK TABLES `customer_wexinjsverify` WRITE;
/*!40000 ALTER TABLE `customer_wexinjsverify` DISABLE KEYS */;
/*!40000 ALTER TABLE `customer_wexinjsverify` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer_whitelist`
--

DROP TABLE IF EXISTS `customer_whitelist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `customer_whitelist` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `lister_id` int(11) NOT NULL,
  `position` int(11) NOT NULL,
  `status` int(11) NOT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `customer_whitelist_a562094a` (`lister_id`),
  KEY `customer_whitelist_1f456125` (`position`),
  KEY `customer_whitelist_96511a37` (`created_at`),
  CONSTRAINT `lister_id_refs_id_d27aee42` FOREIGN KEY (`lister_id`) REFERENCES `customer_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer_whitelist`
--

LOCK TABLES `customer_whitelist` WRITE;
/*!40000 ALTER TABLE `customer_whitelist` DISABLE KEYS */;
/*!40000 ALTER TABLE `customer_whitelist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer_withdrawbalanceorder`
--

DROP TABLE IF EXISTS `customer_withdrawbalanceorder`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `customer_withdrawbalanceorder` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `ticket` int(11) NOT NULL,
  `money` decimal(19,2) NOT NULL,
  `harvest` decimal(19,2) NOT NULL,
  `desc` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `withdraw_time` datetime NOT NULL,
  `filled_time` datetime DEFAULT NULL,
  `trade_type` int(11) NOT NULL,
  `fill_in_type` int(11) NOT NULL,
  `platform` int(11) NOT NULL,
  `status` int(11) NOT NULL,
  `dismiss_reason` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `alipay_acccount` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `name` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `phone` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `alipay_order_id` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `alipay_order_image` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `customer_withdrawbalanceorder_6340c63c` (`user_id`),
  KEY `customer_withdrawbalanceorder_f2753304` (`withdraw_time`),
  KEY `customer_withdrawbalanceorder_24267cf5` (`filled_time`),
  CONSTRAINT `user_id_refs_id_809db334` FOREIGN KEY (`user_id`) REFERENCES `customer_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer_withdrawbalanceorder`
--

LOCK TABLES `customer_withdrawbalanceorder` WRITE;
/*!40000 ALTER TABLE `customer_withdrawbalanceorder` DISABLE KEYS */;
INSERT INTO `customer_withdrawbalanceorder` VALUES (1,229,560,10.00,23.60,'申请提现','2016-04-29 15:44:12',NULL,1,0,1,0,'','上去了','噢噢噢','','',''),(2,165,560,10.00,23.60,'申请提现','2016-04-29 15:49:28',NULL,1,0,1,0,'','啊的','爸爸','','',''),(3,165,560,10.00,23.60,'申请提现','2016-04-29 15:50:07',NULL,1,0,1,0,'','12222','级了','','',''),(4,230,560,10.00,23.60,'申请提现','2016-04-29 15:52:51',NULL,1,0,1,0,'','111','1111','','',''),(5,230,560,10.00,23.60,'申请提现','2016-04-29 15:55:00',NULL,1,0,1,0,'','家','萝莉控','','',''),(6,165,560,10.00,23.60,'申请提现','2016-04-29 16:14:26',NULL,1,0,1,0,'','yyu','ghh','','',''),(7,165,560,10.00,23.60,'申请提现','2016-04-29 16:21:11',NULL,1,0,1,0,'','好','1','','','');
/*!40000 ALTER TABLE `customer_withdrawbalanceorder` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_6340c63c` (`user_id`),
  KEY `django_admin_log_37ef4eb4` (`content_type_id`),
  CONSTRAINT `content_type_id_refs_id_93d2d1f8` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `user_id_refs_id_c0d12874` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2016-03-10 15:15:19',1,3,'1','admin',2,'已修改 password 。'),(2,'2016-04-07 20:31:51',1,3,'2','guming',1,''),(3,'2016-04-18 12:26:16',1,3,'2','guming',3,'');
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `app_label` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=46 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'permission','auth','permission'),(2,'group','auth','group'),(3,'user','auth','user'),(4,'content type','contenttypes','contenttype'),(5,'session','sessions','session'),(6,'log entry','admin','logentry'),(7,'等级','customer','level'),(8,'用户','customer','user'),(9,'用户关注关系','customer','userfollow'),(10,'私信简介列表','customer','usersummerymessage'),(11,'私信','customer','userprivatemessage'),(12,'用户账户','customer','account'),(14,'充值规则','customer','tradebalancerule'),(15,'充值交易记录','customer','tradebalanceorder'),(16,'充值交易记录','customer','withdrawbalanceorder'),(17,'礼物','customer','gift'),(18,'经验上报种类','customer','userexperiencetype'),(19,'经验上报日志','customer','userexperiencelog'),(20,'举报','customer','report'),(21,'房间','live','liveroom'),(22,'房间里的成员','live','roommember'),(23,'用礼物管理','live','roomusergift'),(24,'广告','customer','adv'),(25,'好友关系','customer','userfriends'),(26,'启动图','customer','startupimage'),(27,'第三方绑定','customer','thridpard'),(28,'白名单','customer','whitelist'),(29,'用户账户','customer','wechatfillnotice'),(31,'充值交易记录','customer','tradediamondrecord'),(32,'ticket交易记录','customer','tradeticketrecord'),(33,'商户统计','customer','businessstatistics'),(34,'苹果支付回调','customer','appleverify'),(35,'苹果支付回调','customer','appleverifyresult'),(36,'对某个用户的贡献','customer','rankcontributeuser'),(37,'微信提现记录','customer','wechatwithdrawresult'),(38,'苹果支付回调','customer','wexinjsverify'),(39,'用户通知','customer','usernotice'),(40,'ugc','statistics','ugcandbrand'),(41,'用户付费统计','statistics','premiumuser'),(42,'用户','customer','userdypass'),(43,'revenue','statistics','revenue'),(44,'FillInOrder','statistics','fillinorder'),(45,'FillInPayType','statistics','fillinpaytype');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_b7b81f0c` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('0ia4umwk4zed4yardmnrj4z3kboiniy3','MDA1MjU0NjA2MWNmZDg1NWVmYWE4NDAzYjZhZjAyODIxYWVhMGI3Njp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6MX0=','2016-04-28 16:02:47'),('2nnzd7duprtq09rrlou08v3ow1czp2je','MDA1MjU0NjA2MWNmZDg1NWVmYWE4NDAzYjZhZjAyODIxYWVhMGI3Njp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6MX0=','2016-04-22 09:56:32'),('33x8tfyuhddkhy44jzcojv05hjlvqqq2','MDA1MjU0NjA2MWNmZDg1NWVmYWE4NDAzYjZhZjAyODIxYWVhMGI3Njp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6MX0=','2016-04-12 17:42:54'),('6c3ijewhbvbahnxuokell9yz0qvwfg45','MDA1MjU0NjA2MWNmZDg1NWVmYWE4NDAzYjZhZjAyODIxYWVhMGI3Njp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6MX0=','2016-04-22 11:06:41'),('6w7en5n7rysn0dey9134gq0uib45jnwq','MDA1MjU0NjA2MWNmZDg1NWVmYWE4NDAzYjZhZjAyODIxYWVhMGI3Njp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6MX0=','2016-05-17 11:15:03'),('8jd7l8gt4r090dyscx37t55w9jhumrxl','MDA1MjU0NjA2MWNmZDg1NWVmYWE4NDAzYjZhZjAyODIxYWVhMGI3Njp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6MX0=','2016-03-25 15:01:25'),('9c106ak91qlxyyuevxthpb9slvlxfwc1','MDA1MjU0NjA2MWNmZDg1NWVmYWE4NDAzYjZhZjAyODIxYWVhMGI3Njp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6MX0=','2016-04-21 20:53:30'),('9utn7cvmskmm2on6h33gnk815t7pgq0d','MDA1MjU0NjA2MWNmZDg1NWVmYWE4NDAzYjZhZjAyODIxYWVhMGI3Njp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6MX0=','2016-05-11 19:29:42'),('ch29mq6151m3gtgtnhdcmjqtfzpglxq6','MDA1MjU0NjA2MWNmZDg1NWVmYWE4NDAzYjZhZjAyODIxYWVhMGI3Njp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6MX0=','2016-05-02 13:36:00'),('crb2ei2h23fzjz6ayg1k3flniisx53hl','MDA1MjU0NjA2MWNmZDg1NWVmYWE4NDAzYjZhZjAyODIxYWVhMGI3Njp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6MX0=','2016-05-11 16:20:56'),('d5rdl8ort32fozjpdk8x5p257j2zmnzn','MDA1MjU0NjA2MWNmZDg1NWVmYWE4NDAzYjZhZjAyODIxYWVhMGI3Njp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6MX0=','2016-05-11 16:19:22'),('dt448rqhye1j22zb7qu3pvxu6rmisnqf','MDA1MjU0NjA2MWNmZDg1NWVmYWE4NDAzYjZhZjAyODIxYWVhMGI3Njp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6MX0=','2016-04-12 10:33:39'),('edm86s5amuuoaikzn8mgncm9m0qfqonr','MDA1MjU0NjA2MWNmZDg1NWVmYWE4NDAzYjZhZjAyODIxYWVhMGI3Njp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6MX0=','2016-04-12 15:59:19'),('erisss2lp2a6nqzdgzho7nd8oxnahe1v','YmVmYTcwNzFjNDkyZTFjYjQ3OTI0ZjlmNWJhYmE0MTg2NGQ0YzQwMTp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6Mn0=','2016-04-21 20:46:57'),('hb5c8xq5vzih9ce39my29rmr2ub4f8o1','MDA1MjU0NjA2MWNmZDg1NWVmYWE4NDAzYjZhZjAyODIxYWVhMGI3Njp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6MX0=','2016-04-19 14:34:04'),('kpw3vvr8mhgsqtvriagnzg5b9huk6hix','MDA1MjU0NjA2MWNmZDg1NWVmYWE4NDAzYjZhZjAyODIxYWVhMGI3Njp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6MX0=','2016-04-23 16:01:48'),('lfb0meswz9802q46sfj77bpznqv4ktpk','MDA1MjU0NjA2MWNmZDg1NWVmYWE4NDAzYjZhZjAyODIxYWVhMGI3Njp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6MX0=','2016-04-12 14:24:44'),('ob3gdmmmwv7zdqbz3u5ozjx69ka1wf1d','MDA1MjU0NjA2MWNmZDg1NWVmYWE4NDAzYjZhZjAyODIxYWVhMGI3Njp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6MX0=','2016-05-17 11:14:47'),('ordks7pj1bzwi1ftw74pwvk9mmzm347c','MDA1MjU0NjA2MWNmZDg1NWVmYWE4NDAzYjZhZjAyODIxYWVhMGI3Njp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6MX0=','2016-03-23 13:50:45'),('p0qn885lfj4w970scbkgcyxoszzc7ujs','MDA1MjU0NjA2MWNmZDg1NWVmYWE4NDAzYjZhZjAyODIxYWVhMGI3Njp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6MX0=','2016-03-24 14:32:25'),('sd3x6oxwt3xiyf5dshkxnv4h73kgoxww','MDA1MjU0NjA2MWNmZDg1NWVmYWE4NDAzYjZhZjAyODIxYWVhMGI3Njp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6MX0=','2016-04-13 11:35:35'),('sf8auejep3uocl0n14j6tm0vcwdr28qd','MDA1MjU0NjA2MWNmZDg1NWVmYWE4NDAzYjZhZjAyODIxYWVhMGI3Njp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6MX0=','2016-03-24 15:14:39'),('tkwboz70hswplgfdz6h7ag1hl0v933jf','MDA1MjU0NjA2MWNmZDg1NWVmYWE4NDAzYjZhZjAyODIxYWVhMGI3Njp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6MX0=','2016-05-11 22:43:39'),('ubwe5bx4979twgsk67q061tu3kjpq0gk','MDA1MjU0NjA2MWNmZDg1NWVmYWE4NDAzYjZhZjAyODIxYWVhMGI3Njp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6MX0=','2016-05-10 21:00:56'),('uj2u719kmnroifti09ddvwkqdzu9hg1u','YmVmYTcwNzFjNDkyZTFjYjQ3OTI0ZjlmNWJhYmE0MTg2NGQ0YzQwMTp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6Mn0=','2016-04-21 20:32:08'),('yptxudzunjkad14lqmzuj5s1wlbbtna9','MDA1MjU0NjA2MWNmZDg1NWVmYWE4NDAzYjZhZjAyODIxYWVhMGI3Njp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6MX0=','2016-03-20 18:26:24');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `live_liveroom`
--

DROP TABLE IF EXISTS `live_liveroom`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `live_liveroom` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `owner_id` int(11) NOT NULL,
  `name` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `member_count` int(11) NOT NULL,
  `chat_id` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `max_member_count` int(11) NOT NULL,
  `love_count` int(11) NOT NULL,
  `experience` int(11) NOT NULL,
  `ticket` int(11) NOT NULL,
  `is_top` tinyint(1) NOT NULL,
  `topped_at` datetime DEFAULT NULL,
  `seq` double NOT NULL,
  `position` int(11) NOT NULL,
  `is_secret` int(11) NOT NULL,
  `secret_uids` longtext COLLATE utf8mb4_unicode_ci,
  `status` int(11) NOT NULL,
  `created_at` int(11) NOT NULL,
  `closed_at` int(11) DEFAULT NULL,
  `report_at` int(11) DEFAULT NULL,
  `url` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `rtmp_url` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `channel_id` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  KEY `live_liveroom_cb902d83` (`owner_id`),
  KEY `live_liveroom_4da47e07` (`name`),
  KEY `live_liveroom_be6cfb50` (`topped_at`),
  KEY `live_liveroom_a6e577e1` (`seq`),
  KEY `live_liveroom_1f456125` (`position`),
  KEY `live_liveroom_66d0cbbb` (`is_secret`),
  KEY `live_liveroom_96511a37` (`created_at`),
  KEY `live_liveroom_32241063` (`closed_at`),
  KEY `live_liveroom_3d784664` (`report_at`),
  CONSTRAINT `owner_id_refs_id_fbc7e705` FOREIGN KEY (`owner_id`) REFERENCES `customer_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=223 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `live_liveroom`
--

LOCK TABLES `live_liveroom` WRITE;
/*!40000 ALTER TABLE `live_liveroom` DISABLE KEYS */;
INSERT INTO `live_liveroom` VALUES (1,165,'',0,'@TGS#3AGXBUAE5',0,0,0,0,0,NULL,0,2147483647,0,'',2,1461848865,1461848884,1461848881,'','',''),(2,165,'',0,'@TGS#337VCUAE5',0,0,0,0,0,NULL,0,2147483647,0,'',2,1461848940,1461849011,1461849001,'','',''),(3,169,'',1,'@TGS#3PZWCUAEB',1,0,0,0,0,NULL,0,2147483647,0,'',2,1461849240,1461849749,1461849745,'','',''),(4,170,'',1,'@TGS#3V3XBUAE6',1,36,0,0,0,NULL,0.9,2147483647,0,'',2,1461850254,1461850295,1461850293,'','',''),(6,171,'',1,'@TGS#3MDYCUAEJ',1,55,0,0,0,NULL,0.272277227722772,2147483647,0,'',2,1461850305,1461850517,1461850506,'http://2632.liveplay.myqcloud.com/2632_c8aa957f0d4511e6b91fa4dcbef5e35a.m3u8','rtmp://2632.liveplay.myqcloud.com/live/2632_c8aa957f0d4511e6b91fa4dcbef5e35a','16093104850682369073'),(7,170,'哈哈哈哈',0,'@TGS#3OGZCUAEP',0,0,0,0,0,NULL,0,2147483647,0,'',2,1461850864,1461892992,NULL,'','',''),(8,172,'qwe',0,'@TGS#3FJYBUAEH',1,0,0,0,0,NULL,0,2147483647,0,'',2,1461850919,1461851586,1461851580,'http://2632.liveplay.myqcloud.com/2632_06f741dd0d4711e6b91fa4dcbef5e35a.m3u8','rtmp://2632.liveplay.myqcloud.com/live/2632_06f741dd0d4711e6b91fa4dcbef5e35a','16093104850682369182'),(9,171,'',0,'@TGS#3KJZCUAEO',0,0,0,0,0,NULL,0,2147483647,0,'',2,1461851056,1461851152,1461851145,'http://2632.liveplay.myqcloud.com/2632_4f4e8fd80d4711e6b91fa4dcbef5e35a.m3u8','rtmp://2632.liveplay.myqcloud.com/live/2632_4f4e8fd80d4711e6b91fa4dcbef5e35a','-2353639223027182410'),(10,171,'',0,'@TGS#3LXZCUAE5',0,0,0,0,0,NULL,0,2147483647,0,'',2,1461851323,1461851362,NULL,'','',''),(11,171,'',0,'@TGS#3APYBUAEI',0,0,0,0,0,NULL,0,2147483647,0,'',2,1461851362,1461851480,1461851468,'http://2632.liveplay.myqcloud.com/2632_4f4e8fd80d4711e6b91fa4dcbef5e35a.m3u8','rtmp://2632.liveplay.myqcloud.com/live/2632_4f4e8fd80d4711e6b91fa4dcbef5e35a','-2353639223027182410'),(12,173,'',0,'@TGS#3FCZBUAEB',0,0,0,0,0,NULL,0,2147483647,0,'',2,1461851766,1461851793,1461851782,'','',''),(13,170,'',0,'@TGS#3KDQDUAEA',0,0,0,0,0,NULL,0,2147483647,0,'',2,1461892999,1461926569,NULL,'','',''),(14,169,'',0,'@TGS#3MLSDUAEM',0,0,0,0,0,NULL,0,2147483647,0,'',2,1461896046,1461896065,1461896063,'','',''),(15,165,'',0,'@TGS#3Q7QCUAEX',0,0,0,0,0,NULL,0,2147483647,0,'',2,1461896598,1461896635,1461896630,'','',''),(16,168,'',0,'@TGS#3X5QCUAE4',0,0,0,0,0,NULL,0,2147483647,0,'',2,1461896744,1461896809,1461896759,'','',''),(17,168,'',0,'',0,0,0,0,0,NULL,0,2147483647,0,'',2,1461896771,1461897072,NULL,'','',''),(18,169,'',0,'@TGS#3UHRCUAEO',0,0,0,0,0,NULL,0,2147483647,0,'',2,1461896828,1461897602,1461897236,'','',''),(19,168,'',0,'@TGS#3EFRCUAE3',0,0,0,0,0,NULL,0,2147483647,0,'',2,1461897072,1461897783,1461897780,'http://2632.liveplay.myqcloud.com/2632_8ebca0050db211e6b91fa4dcbef5e35a.m3u8','rtmp://2632.liveplay.myqcloud.com/live/2632_8ebca0050db211e6b91fa4dcbef5e35a','16093104850682372004'),(20,225,'',0,'@TGS#3B4RCUAEG',0,0,0,0,0,NULL,0,2147483647,0,'',2,1461897740,1461898402,1461898401,'','',''),(21,165,'',1,'@TGS#3R3RCUAEV',1,0,0,0,0,NULL,0,2147483647,0,'',2,1461897774,1461898164,1461898155,'','',''),(22,168,'',0,'@TGS#3UGSCUAEO',0,0,0,0,0,NULL,0,2147483647,0,'',2,1461898286,1461898427,1461898332,'http://2632.liveplay.myqcloud.com/2632_4829d17e0db511e6b91fa4dcbef5e35a.m3u8','rtmp://2632.liveplay.myqcloud.com/live/2632_4829d17e0db511e6b91fa4dcbef5e35a','16093104850682372197'),(23,165,'',0,'@TGS#3V7RCUAE5',0,0,0,0,0,NULL,0,2147483647,0,'',2,1461898310,1461898338,1461898327,'','',''),(24,226,'',0,'@TGS#3ENSCUAEF',0,0,0,0,0,NULL,0,2147483647,0,'',2,1461898329,1461898424,1461898421,'','',''),(25,226,'',0,'@TGS#3BMSCUAEB',0,0,0,0,0,NULL,0,2147483647,0,'',2,1461898432,1461898542,1461898493,'','',''),(26,228,'',0,'@TGS#3XDSCUAEO',0,0,0,0,0,NULL,0,2147483647,0,'',2,1461898521,1461898620,1461898613,'','',''),(27,226,'',0,'@TGS#3TKSCUAER',0,0,0,0,0,NULL,0,2147483647,0,'',2,1461898542,1461898598,1461898589,'','',''),(28,226,'',0,'@TGS#3R4SCUAEX',0,0,0,0,0,NULL,0,2147483647,0,'',2,1461898610,1461898689,1461898687,'','',''),(29,168,'',0,'@TGS#35DUDUAEN',0,0,0,0,0,NULL,0,2147483647,0,'',2,1461898655,1461899203,1461899121,'http://2632.liveplay.myqcloud.com/2632_4829d17e0db511e6b91fa4dcbef5e35a.m3u8','rtmp://2632.liveplay.myqcloud.com/live/2632_4829d17e0db511e6b91fa4dcbef5e35a','16093104850682372197'),(30,226,'',1,'@TGS#3YDUDUAES',1,0,0,0,0,NULL,0,2147483647,0,'',2,1461898693,1461898719,1461898709,'','',''),(31,226,'',0,'@TGS#3L4TDUAET',0,0,0,0,0,NULL,0,2147483647,0,'',2,1461898748,1461898859,1461898794,'','',''),(32,228,'',0,'@TGS#3GCTCUAE4',0,0,0,0,0,NULL,0,2147483647,0,'',2,1461898893,1461899053,NULL,'','',''),(33,229,'',0,'@TGS#3OYTDUAE4',1,0,0,0,0,NULL,0,2147483647,0,'',2,1461898991,1461899298,1461899292,'','',''),(34,228,'',0,'@TGS#3SITCUAEP',0,0,0,0,0,NULL,0,2147483647,0,'',2,1461899053,1461899086,1461899084,'','',''),(35,226,'',0,'@TGS#3ZKUDUAE2',0,0,0,0,0,NULL,0,2147483647,0,'',2,1461899089,1461899324,1461899316,'','',''),(36,168,'',0,'@TGS#3JJUDUAEJ',0,0,0,0,0,NULL,0,2147483647,0,'',2,1461899215,1461899386,1461899306,'http://2632.liveplay.myqcloud.com/2632_4829d17e0db511e6b91fa4dcbef5e35a.m3u8','rtmp://2632.liveplay.myqcloud.com/live/2632_4829d17e0db511e6b91fa4dcbef5e35a','16093104850682372197'),(37,166,'',0,'@TGS#3UOTCUAEX',0,0,0,0,0,NULL,0,2147483647,0,'',2,1461899307,1461900003,1461899996,'http://2632.liveplay.myqcloud.com/2632_a70ee4070db711e6b91fa4dcbef5e35a.m3u8','rtmp://2632.liveplay.myqcloud.com/live/2632_a70ee4070db711e6b91fa4dcbef5e35a','16093104850682372363'),(38,229,'',0,'@TGS#35HUDUAER',0,0,0,0,0,NULL,0,2147483647,0,'',2,1461899309,1461899349,1461899340,'','',''),(39,229,'',0,'@TGS#37GUDUAES',0,0,0,0,0,NULL,0,2147483647,0,'',2,1461899353,1461899385,1461899384,'','',''),(40,229,'',0,'@TGS#3WDTCUAEO',1,26,0,0,0,NULL,0.00906555090655509,2147483647,0,'',2,1461899388,1461902262,1461902255,'','',''),(41,168,'',0,'@TGS#3ZGUDUAEW',0,0,0,0,0,NULL,0,2147483647,0,'',2,1461899394,1461899852,1461899785,'http://2632.liveplay.myqcloud.com/2632_4829d17e0db511e6b91fa4dcbef5e35a.m3u8','rtmp://2632.liveplay.myqcloud.com/live/2632_4829d17e0db511e6b91fa4dcbef5e35a','16093104850682372197'),(42,168,'',0,'@TGS#3YEVDUAEU',0,0,0,0,0,NULL,0,2147483647,0,'',2,1461899971,1461900220,1461900152,'http://2632.liveplay.myqcloud.com/2632_4829d17e0db511e6b91fa4dcbef5e35a.m3u8','rtmp://2632.liveplay.myqcloud.com/live/2632_4829d17e0db511e6b91fa4dcbef5e35a','16093104850682372197'),(43,168,'',0,'@TGS#3FXTCUAER',0,0,0,0,0,NULL,0,2147483647,0,'',2,1461900229,1461900454,1461900440,'http://2632.liveplay.myqcloud.com/2632_4829d17e0db511e6b91fa4dcbef5e35a.m3u8','rtmp://2632.liveplay.myqcloud.com/live/2632_4829d17e0db511e6b91fa4dcbef5e35a','16093104850682372197'),(44,166,'',0,'@TGS#3DGUCUAE6',0,0,0,0,0,NULL,0,2147483647,0,'',2,1461900585,1461901873,1461901861,'','',''),(45,226,'',0,'@TGS#3F6TCUAEO',0,0,0,0,0,NULL,0,2147483647,0,'',2,1461900608,1461900642,1461900639,'','',''),(46,226,'',0,'@TGS#3RFUCUAEM',0,0,0,0,0,NULL,0,2147483647,0,'',2,1461900649,1461900669,1461900666,'','',''),(47,226,'',0,'@TGS#3HUUCUAER',0,0,0,0,0,NULL,0,2147483647,0,'',2,1461900677,1461900714,1461900708,'','',''),(48,226,'',1,'@TGS#3VLUCUAEW',1,0,0,0,0,NULL,0,2147483647,0,'',2,1461900721,1461900772,1461900769,'','',''),(49,226,'',0,'@TGS#3T4TCUAE2',0,0,0,0,0,NULL,0,2147483647,0,'',2,1461900783,1461900805,1461900799,'','',''),(50,226,'',0,'@TGS#3BDUCUAEZ',0,0,0,0,0,NULL,0,2147483647,0,'',2,1461900821,1461900948,1461900943,'','',''),(51,226,'',0,'@TGS#32PVDUAEX',0,0,0,0,0,NULL,0,2147483647,0,'',2,1461900958,1461901018,1461901005,'','',''),(52,209,'',0,'@TGS#3NVVDUAE2',0,0,0,0,0,NULL,0,2147483647,0,'',2,1461901025,1461901331,1461901326,'','',''),(53,226,'',0,'@TGS#3IVVDUAEV',0,0,0,0,0,NULL,0,2147483647,0,'',2,1461901043,1461901113,1461901104,'','',''),(54,226,'',0,'@TGS#3MUVDUAEY',0,0,0,0,0,NULL,0,2147483647,0,'',2,1461901118,1461901157,1461901149,'','',''),(55,226,'',0,'@TGS#3LLVDUAEO',0,0,0,0,0,NULL,0,2147483647,0,'',2,1461901240,1461901548,1461901286,'','',''),(56,230,'',0,'@TGS#34RVDUAE3',0,0,0,0,0,NULL,0,2147483647,0,'',2,1461901283,1461901342,1461901330,'','',''),(57,230,'',0,'@TGS#3NCWDUAEI',0,0,0,0,0,NULL,0,2147483647,0,'',2,1461901380,1461901482,1461901472,'','',''),(58,209,'',0,'@TGS#3RAVCUAEI',0,0,0,0,0,NULL,0,2147483647,0,'',2,1461901394,1461901781,1461901769,'http://2632.liveplay.myqcloud.com/2632_83aff1330dbc11e6b91fa4dcbef5e35a.m3u8','rtmp://2632.liveplay.myqcloud.com/live/2632_83aff1330dbc11e6b91fa4dcbef5e35a','16093104850682372800'),(59,230,'',0,'@TGS#32IWDUAER',1,0,0,0,0,NULL,0,2147483647,0,'',2,1461901528,1461902732,1461902729,'','',''),(60,226,'',1,'',1,0,0,0,0,NULL,0,2147483647,0,'',2,1461901548,1461903902,1461903330,'','',''),(61,209,'',0,'@TGS#3FEVCUAEA',1,0,0,0,0,NULL,0,2147483647,0,'',2,1461902269,1461902307,1461902300,'','',''),(62,209,'',0,'@TGS#3EVVCUAEQ',1,0,0,0,0,NULL,0,2147483647,0,'',2,1461902316,1461902480,1461902466,'','',''),(63,228,'',0,'@TGS#3CJYCUAEF',0,0,0,0,0,NULL,0,2147483647,0,'',2,1461907515,1461907515,NULL,'','',''),(64,228,'',0,'@TGS#32K4DUAEP',0,0,0,0,0,NULL,0,2147483647,0,'',2,1461907515,1461907667,1461907666,'','',''),(65,234,'',0,'@TGS#3DIYCUAEF',0,0,0,0,0,NULL,0,2147483647,0,'',2,1461907580,1461907586,NULL,'','',''),(66,228,'',0,'@TGS#33R4DUAEX',0,0,0,0,0,NULL,0,2147483647,0,'',2,1461907671,1461907750,1461907747,'','',''),(67,234,'',0,'',0,0,0,0,0,NULL,0,2147483647,0,'',2,1461907701,1461909723,NULL,'','',''),(68,228,'',0,'@TGS#3UQYCUAE6',0,0,0,0,0,NULL,0,2147483647,0,'',2,1461907791,1461907823,1461907822,'','',''),(69,228,'',0,'@TGS#3HQYCUAER',0,0,0,0,0,NULL,0,2147483647,0,'',2,1461907826,1461908684,1461908683,'','',''),(70,230,'',0,'@TGS#3Q4ZCUAE5',0,0,0,0,0,NULL,0,2147483647,0,'',2,1461909083,1461909093,NULL,'','',''),(71,230,'',0,'@TGS#3UJ2CUAEP',0,0,0,0,0,NULL,0,2147483647,0,'',2,1461909096,1461909104,NULL,'','',''),(72,230,'',0,'@TGS#3JM5DUAEL',0,0,0,0,0,NULL,0,2147483647,0,'',2,1461909423,1461909436,NULL,'','',''),(73,230,'',0,'@TGS#3PL5DUAEQ',1,0,0,0,0,NULL,0,2147483647,0,'',2,1461909440,1461910802,1461910446,'','',''),(74,168,'',0,'@TGS#3426DUAEZ',0,0,0,0,0,NULL,0,2147483647,0,'',2,1461909685,1461909705,1461909700,'','',''),(75,234,'',0,'@TGS#3HA3CUAEZ',0,0,0,0,0,NULL,0,2147483647,0,'',2,1461909723,1461909765,1461909754,'','',''),(76,234,'',0,'@TGS#3F72CUAEM',0,0,0,0,0,NULL,0,2147483647,0,'',2,1461909799,1461909810,NULL,'','',''),(77,228,'',1,'@TGS#3646DUAE5',1,0,0,0,0,NULL,0,2147483647,0,'',2,1461910177,1461910258,1461910256,'','',''),(78,228,'',1,'@TGS#3ES3CUAEJ',1,0,0,0,0,NULL,0,2147483647,0,'',2,1461910476,1461910501,1461910500,'','',''),(79,228,'',1,'@TGS#33T7DUAE4',1,0,0,0,0,NULL,0,2147483647,0,'',2,1461910675,1461910696,1461910691,'','',''),(80,165,'',1,'@TGS#3ZO7DUAEA',1,0,0,0,0,NULL,0,2147483647,0,'',2,1461910938,1461910985,1461910984,'','',''),(81,165,'',0,'@TGS#3XF4CUAEQ',0,0,0,0,0,NULL,0,2147483647,0,'',2,1461911176,1461911492,1461911492,'','',''),(82,165,'',0,'@TGS#36LAEUAED',0,0,0,0,0,NULL,0,2147483647,0,'',2,1461911561,1461911571,NULL,'','',''),(83,165,'',0,'@TGS#342AEUAEG',0,0,0,0,0,NULL,0,2147483647,0,'',2,1461911577,1461911581,NULL,'','',''),(84,168,'',0,'@TGS#3OZAEUAEL',0,0,0,0,0,NULL,0,2147483647,0,'',2,1461911654,1461911664,NULL,'','',''),(85,229,'',1,'@TGS#35NBEUAEF',1,0,0,0,0,NULL,0,2147483647,0,'',2,1461912752,1461912797,1461912795,'','',''),(86,165,'',1,'@TGS#33DCEUAEZ',1,0,0,0,0,NULL,0,2147483647,0,'',2,1461912831,1461912858,1461912847,'','',''),(87,229,'',0,'@TGS#363CEUAEL',0,0,0,0,0,NULL,0,2147483647,0,'',2,1461913544,1461913560,NULL,'','',''),(88,165,'',1,'@TGS#37BDEUAE4',1,0,0,0,0,NULL,0,2147483647,0,'',2,1461913700,1461913734,1461913732,'','',''),(89,165,'',0,'@TGS#3NVDEUAEJ',0,0,0,0,0,NULL,0,2147483647,0,'',2,1461914229,1461914407,1461914395,'','',''),(90,229,'',1,'@TGS#3DJ7CUAED',1,0,0,743,0,NULL,0,2147483647,0,'',2,1461915730,1461915795,1461915792,'','',''),(91,165,'',0,'@TGS#3JIFEUAEZ',1,16,0,521,0,NULL,0.207792207792208,2147483647,0,'',2,1461915977,1461916062,1461916053,'','',''),(92,165,'',0,'@TGS#35XFEUAET',1,0,0,5000,0,NULL,0,2147483647,0,'',2,1461916082,1461916142,1461916129,'','',''),(93,229,'',0,'@TGS#3SQ7CUAEZ',0,0,0,0,0,NULL,0,2147483647,0,'',2,1461916106,1461916136,1461916122,'','',''),(94,236,'',0,'@TGS#3DO7CUAEI',1,0,0,0,0,NULL,0,2147483647,0,'',2,1461916236,1461916310,1461916298,'','',''),(95,230,'',1,'@TGS#3POFEUAEG',1,0,0,2666,0,NULL,0,2147483647,0,'',2,1461916302,1461916350,1461916349,'','',''),(96,236,'',0,'@TGS#36IGEUAEG',1,0,0,0,0,NULL,0,2147483647,0,'',2,1461916903,1461917013,1461917009,'','',''),(97,229,'',0,'@TGS#33FGEUAEA',0,0,0,0,0,NULL,0,2147483647,0,'',2,1461917115,1461917124,NULL,'','',''),(98,209,'',0,'@TGS#3SMBDUAEC',1,0,0,50,0,NULL,0,2147483647,0,'',2,1461918168,1461918263,1461918259,'','',''),(99,209,'',0,'@TGS#3CTBDUAEY',1,0,0,52,0,NULL,0,2147483647,0,'',2,1461918277,1461918369,1461918367,'','',''),(100,209,'',0,'@TGS#3RQCDUAEG',0,0,0,0,0,NULL,0,2147483647,0,'',2,1461918755,1461918767,NULL,'','',''),(101,209,'',0,'@TGS#3GWCDUAEB',0,0,0,52,0,NULL,0,2147483647,0,'',2,1461918807,1461918948,1461918928,'http://2632.liveplay.myqcloud.com/2632_0ffa456e0de511e6b91fa4dcbef5e35a.m3u8','rtmp://2632.liveplay.myqcloud.com/live/2632_0ffa456e0de511e6b91fa4dcbef5e35a','16093104850682376476'),(102,168,'',0,'@TGS#3Z2HEUAEU',0,0,0,0,0,NULL,0,2147483647,0,'',2,1461919072,1461919232,1461919223,'','',''),(103,209,'',0,'@TGS#3U4CDUAEL',0,0,0,52,0,NULL,0,2147483647,0,'',2,1461919121,1461919236,1461919227,'http://2632.liveplay.myqcloud.com/2632_0ffa456e0de511e6b91fa4dcbef5e35a.m3u8','rtmp://2632.liveplay.myqcloud.com/live/2632_0ffa456e0de511e6b91fa4dcbef5e35a','16093104850682376476'),(104,225,'',0,'@TGS#3C6DDUAE3',0,0,0,0,0,NULL,0,2147483647,0,'',2,1461920702,1461921441,1461921439,'','',''),(105,209,'哈喽',0,'@TGS#3EGEDUAEQ',0,0,0,52,0,NULL,0,2147483647,0,'',2,1461920802,1461920835,1461920827,'','',''),(106,209,'',0,'',0,0,0,0,0,NULL,0,2147483647,0,'',2,1461920844,1461920907,NULL,'','',''),(107,209,'',0,'@TGS#3XLEDUAEJ',0,0,0,52,0,NULL,0,2147483647,0,'',2,1461920907,1461921731,1461920977,'','',''),(108,225,'',0,'@TGS#33WLEUAEW',0,0,0,0,0,NULL,0,2147483647,0,'',2,1461921636,1461921643,NULL,'','',''),(109,165,'',0,'@TGS#3OWLEUAET',0,0,0,0,0,NULL,0,2147483647,0,'',2,1461921656,1461921785,1461921672,'','',''),(110,225,'',0,'@TGS#325LEUAES',0,0,0,0,0,NULL,0,2147483647,1,'228',2,1461921714,1461922256,1461922244,'http://2632.liveplay.myqcloud.com/2632_5bab6e190dec11e6b91fa4dcbef5e35a.m3u8','rtmp://2632.liveplay.myqcloud.com/live/2632_5bab6e190dec11e6b91fa4dcbef5e35a','-2353639223027174365'),(111,209,'',0,'@TGS#3O5LEUAEQ',0,0,0,52,0,NULL,0,2147483647,0,'',2,1461921737,1461922146,1461921962,'','',''),(112,165,'',0,'',0,0,0,0,0,NULL,0,2147483647,0,'',2,1461921785,1461921822,NULL,'','',''),(113,165,'',1,'@TGS#3M4LEUAEN',1,0,0,0,0,NULL,0,2147483647,0,'',2,1461921822,1461922053,1461922045,'','',''),(114,165,'',1,'@TGS#3HAFDUAEO',1,0,0,0,0,NULL,0,2147483647,0,'',2,1461922058,1461922497,1461922423,'','',''),(115,209,'',0,'@TGS#3JBMEUAEZ',0,0,0,52,0,NULL,0,2147483647,0,'',2,1461922148,1461922240,1461922238,'','',''),(116,165,'',0,'@TGS#3TRFDUAEM',1,0,0,0,0,NULL,0,2147483647,0,'',2,1461922497,1461922792,1461922708,'','',''),(117,165,'',1,'@TGS#36PMEUAET',1,0,0,0,0,NULL,0,2147483647,0,'',2,1461922792,1461923693,1461923692,'','',''),(118,165,'',1,'@TGS#3LGNEUAEC',1,0,0,0,0,NULL,0,2147483647,0,'',2,1461923693,1461923929,1461923840,'','',''),(119,165,'',1,'@TGS#336NEUAEW',1,0,0,0,0,NULL,0,2147483647,0,'',2,1461923929,1461924103,1461924098,'','',''),(120,165,'',1,'@TGS#3BHHDUAER',1,0,0,0,0,NULL,0,2147483647,0,'',2,1461924103,1461924221,1461924217,'','',''),(121,229,'',0,'@TGS#366PEUAE3',0,0,0,0,0,NULL,0,2147483647,0,'',2,1461926152,1461926168,1461926168,'','',''),(122,229,'',0,'@TGS#3CGJDUAET',0,0,0,0,0,NULL,0,2147483647,0,'',2,1461926172,1461926319,1461926282,'','',''),(123,229,'',0,'@TGS#3DEJDUAES',0,0,0,0,0,NULL,0,2147483647,0,'',2,1461926319,1461927001,1461926500,'','',''),(124,173,'',0,'@TGS#35CQEUAEJ',0,0,0,0,0,NULL,0,2147483647,0,'',2,1461926373,1461926384,NULL,'','',''),(125,170,'',0,'@TGS#33SQEUAEX',0,0,0,0,0,NULL,0,2147483647,0,'',2,1461926587,1461926720,1461926678,'','',''),(126,170,'',0,'@TGS#32XQEUAE3',0,0,0,0,0,NULL,0,2147483647,0,'',2,1461926756,1461926908,1461926907,'','',''),(127,170,'',1,'@TGS#37YREUAED',1,0,0,0,0,NULL,0,2147483647,0,'',2,1461927784,1461927908,1461927907,'','',''),(128,229,'',1,'@TGS#33WREUAE4',2,390,0,0,0,NULL,0.209339774557166,2147483647,0,'',2,1461927910,1461929783,1461929772,'','',''),(129,170,'',0,'@TGS#3OKSEUAEO',0,0,0,0,0,NULL,0,2147483647,0,'',2,1461927919,1461927962,1461927950,'','',''),(130,238,'',0,'@TGS#3TMKDUAEM',0,0,0,0,0,NULL,0,2147483647,0,'',2,1461928234,1461928239,NULL,'','',''),(131,238,'',0,'@TGS#34AUEUAEK',0,0,0,0,0,NULL,0,2147483647,0,'',2,1461928429,1461928545,1461928544,'http://2632.liveplay.myqcloud.com/2632_75750b5b0dfb11e6b91fa4dcbef5e35a.m3u8','rtmp://2632.liveplay.myqcloud.com/live/2632_75750b5b0dfb11e6b91fa4dcbef5e35a','-2353639223027172928'),(132,229,'',1,'@TGS#3DHMDUAEY',2,0,0,0,0,NULL,0,2147483647,0,'',2,1461929888,1461929996,1461929994,'','',''),(133,229,'',0,'@TGS#3VRMDUAEV',0,0,0,0,0,NULL,0,2147483647,0,'',2,1461930376,1461930478,1461930438,'','',''),(134,229,'',0,'@TGS#353VEUAE5',0,0,0,0,0,NULL,0,2147483647,0,'',2,1461930478,1461930497,1461930495,'','',''),(135,229,'',0,'@TGS#34RVEUAE4',0,0,0,0,0,NULL,0,2147483647,0,'',2,1461930503,1461931022,1461930551,'','',''),(136,166,'',0,'@TGS#3QUTDUAE2',0,0,0,0,0,NULL,0,2147483647,0,'',2,1461938059,1461938091,1461938090,'','',''),(137,229,'',0,'@TGS#37XEMUAE4',0,0,0,0,0,NULL,0,2147483647,0,'',2,1462242978,1462243110,1462243100,'','',''),(138,229,'',0,'@TGS#34NEMUAEP',0,0,0,0,0,NULL,0,2147483647,0,'',2,1462243155,1462243337,1462243336,'','',''),(139,229,'',0,'@TGS#3GN3KUAEO',0,0,0,0,0,NULL,0,2147483647,0,'',2,1462243696,1462244740,1462244733,'','',''),(140,229,'',0,'@TGS#3ZKGMUAEV',0,0,0,0,0,NULL,0,2147483647,0,'',2,1462244830,1462244841,NULL,'','',''),(141,229,'',0,'@TGS#3LDGMUAEA',0,0,0,0,0,NULL,0,2147483647,0,'',2,1462244898,1462244907,NULL,'','',''),(142,229,'',0,'@TGS#3UT4KUAEE',0,0,0,0,0,NULL,0,2147483647,0,'',2,1462245220,1462245392,1462245341,'','',''),(143,229,'',0,'@TGS#3VR4KUAED',0,0,0,0,0,NULL,0,2147483647,0,'',2,1462245392,1462245546,1462245513,'','',''),(144,229,'',0,'@TGS#3DQ4KUAEP',0,0,0,0,0,NULL,0,2147483647,0,'',2,1462245546,1462245548,NULL,'','',''),(145,229,'',0,'@TGS#3CQ4KUAEO',0,0,0,0,0,NULL,0,2147483647,0,'',2,1462245548,1462246014,1462245999,'','',''),(146,168,'',0,'@TGS#3QMELUAEL',0,0,0,0,0,NULL,0,2147483647,0,'',2,1462253791,1462253822,1462253822,'','',''),(147,168,'',0,'@TGS#3JRNMUAET',0,0,0,0,0,NULL,0,2147483647,0,'',2,1462255532,1462255811,1462255728,'','',''),(148,244,'',0,'@TGS#34MQMUAE2',4,0,0,5017,0,NULL,0,2147483647,0,'',2,1462258411,1462259882,1462259868,'','',''),(149,241,'',0,'@TGS#3LYQMUAEA',0,0,0,0,0,NULL,0,2147483647,0,'',2,1462258798,1462258812,NULL,'','',''),(150,229,'',1,'@TGS#364RMUAEE',1,0,0,0,0,NULL,0,2147483647,0,'',2,1462259934,1462260059,1462260055,'','',''),(151,165,'',0,'',0,0,0,0,0,NULL,0,2147483647,0,'',2,1462260066,1462260082,NULL,'','',''),(152,165,'',2,'@TGS#3JUSMUAE3',3,0,0,111,0,NULL,0,2147483647,0,'',2,1462260082,1462260706,1462260699,'','',''),(153,165,'',2,'@TGS#3TBKLUAEJ',2,0,0,0,0,NULL,0,2147483647,0,'',2,1462260738,1462260857,1462260848,'','',''),(154,229,'',0,'@TGS#3VQKLUAE2',0,0,0,0,0,NULL,0,2147483647,0,'',2,1462260944,1462261631,NULL,'','',''),(155,229,'',1,'@TGS#3ATKLUAEI',1,0,0,0,0,NULL,0,2147483647,0,'',2,1462261631,1462261855,1462261845,'','',''),(156,229,'',0,'@TGS#3COLLUAEG',0,0,0,0,0,NULL,0,2147483647,0,'',2,1462261951,1462261975,1462261967,'','',''),(157,229,'',0,'@TGS#3RXLLUAE6',0,0,0,0,0,NULL,0,2147483647,0,'',2,1462262001,1462262013,NULL,'','',''),(158,229,'',0,'@TGS#3DXLLUAEQ',0,0,0,0,0,NULL,0,2147483647,0,'',2,1462262017,1462262024,NULL,'','',''),(159,229,'',0,'@TGS#3R6LLUAE3',0,0,0,0,0,NULL,0,2147483647,0,'',2,1462262056,1462262086,1462262072,'','',''),(160,229,'',0,'@TGS#3GMLLUAEI',0,0,0,0,0,NULL,0,2147483647,0,'',2,1462262091,1462262100,NULL,'','',''),(161,170,'',0,'',0,0,0,0,0,NULL,0,2147483647,0,'',2,1462262101,1462262295,NULL,'','',''),(162,229,'',0,'@TGS#35KUMUAE5',0,0,0,0,0,NULL,0,2147483647,0,'',2,1462262104,1462262120,NULL,'','',''),(163,229,'',0,'@TGS#3C4LLUAEK',0,0,0,0,0,NULL,0,2147483647,0,'',2,1462262207,1462262213,NULL,'','',''),(164,229,'',0,'@TGS#32IUMUAEY',0,0,0,0,0,NULL,0,2147483647,0,'',2,1462262223,1462262233,NULL,'','',''),(165,170,'',0,'@TGS#37GUMUAE3',0,0,0,0,0,NULL,0,2147483647,0,'',2,1462262295,1462262329,1462262326,'','',''),(166,229,'',0,'@TGS#3DIMLUAEC',0,0,0,0,0,NULL,0,2147483647,0,'',2,1462262441,1462262783,1462262772,'','',''),(167,168,'',0,'@TGS#37TVMUAEK',0,0,0,0,0,NULL,0,2147483647,0,'',2,1462263240,1462263251,NULL,'','',''),(168,168,'',0,'@TGS#3ITZMUAEB',0,0,0,0,0,NULL,0,2147483647,0,'',2,1462264614,1462264753,1462264750,'','',''),(169,168,'',0,'@TGS#3KX2MUAE5',0,0,0,0,0,NULL,0,2147483647,0,'',2,1462264762,1462267470,1462265963,'','',''),(170,229,'',2,'@TGS#3IJ4MUAEP',2,0,0,0,0,NULL,0,2147483647,0,'',2,1462265613,1462265805,1462265802,'','',''),(171,229,'',2,'@TGS#3QSRLUAE6',2,0,0,0,0,NULL,0,2147483647,0,'',2,1462265809,1462266568,1462266560,'','',''),(172,229,'',2,'@TGS#3XGTLUAE3',2,0,0,0,0,NULL,0,2147483647,0,'',2,1462266717,1462266875,1462266867,'','',''),(173,226,'',0,'@TGS#3LP7MUAE3',0,0,0,0,0,NULL,0,2147483647,0,'',2,1462266882,1462266914,1462266913,'','',''),(174,226,'',0,'@TGS#36F7MUAE2',0,0,0,0,0,NULL,0,2147483647,0,'',2,1462266921,1462266963,1462266952,'','',''),(175,226,'',0,'@TGS#3IE7MUAEN',0,0,0,0,0,NULL,0,2147483647,0,'',2,1462266970,1462267258,1462267256,'','',''),(176,226,'',0,'@TGS#3WSTLUAEH',0,0,0,0,0,NULL,0,2147483647,0,'',2,1462267266,1462267500,1462267492,'','',''),(177,165,'',2,'@TGS#3G2TLUAEU',2,0,0,0,0,NULL,0,2147483647,0,'',2,1462267289,1462273202,1462272881,'','',''),(178,229,'',0,'@TGS#32FANUAEC',0,0,0,0,0,NULL,0,2147483647,0,'',2,1462267297,1462267413,NULL,'','',''),(179,229,'',0,'@TGS#3SPTLUAEA',0,0,0,0,0,NULL,0,2147483647,0,'',2,1462267413,1462267435,NULL,'','',''),(180,229,'',0,'@TGS#3T7TLUAEH',0,0,0,0,0,NULL,0,2147483647,0,'',2,1462267435,1462267461,1462267451,'','',''),(181,229,'',0,'@TGS#33UANUAES',0,0,0,0,0,NULL,0,2147483647,0,'',2,1462267466,1462267470,NULL,'','',''),(182,229,'',0,'@TGS#3NOANUAEI',0,0,0,0,0,NULL,0,2147483647,0,'',2,1462267474,1462267477,NULL,'','',''),(183,229,'',0,'@TGS#37NANUAEP',0,0,0,0,0,NULL,0,2147483647,0,'',2,1462267489,1462267492,NULL,'','',''),(184,245,'',0,'@TGS#3BKULUAEK',1,109,0,1091,0,NULL,0.0342444234998429,2147483647,0,'',2,1462268000,1462271183,1462271182,'','',''),(185,226,'',0,'@TGS#3RGWLUAEY',0,0,0,0,0,NULL,0,2147483647,0,'',2,1462268777,1462269458,1462269453,'','',''),(186,168,'',0,'@TGS#3LTCNUAEN',0,0,0,0,0,NULL,0,2147483647,0,'',2,1462269190,1462269213,1462269206,'','',''),(187,226,'',0,'@TGS#3KYFNUAEU',0,0,0,0,0,NULL,0,2147483647,0,'',2,1462271004,1462272048,1462272040,'','',''),(188,226,'',0,'@TGS#3LDINUAED',1,0,0,0,0,NULL,0,2147483647,0,'',2,1462272712,1462273011,1462272998,'','',''),(189,170,'',0,'@TGS#3BK6LUAEK',0,0,0,0,0,NULL,0,2147483647,0,'',2,1462275998,1462276005,NULL,'','',''),(190,170,'',0,'@TGS#3HJ6LUAEP',1,0,0,2669,0,NULL,0,2147483647,0,'',2,1462276051,1462281351,1462276681,'','',''),(191,241,'',2,'',2,0,0,0,0,NULL,0,2147483647,0,'',2,1462276666,1462284001,1462283654,'','',''),(192,229,'',0,'@TGS#36LNNUAEZ',0,0,0,0,0,NULL,0,2147483647,0,'',2,1462277466,1462277821,NULL,'','',''),(193,229,'',0,'@TGS#36FNNUAET',0,0,0,0,0,NULL,0,2147483647,0,'',2,1462277821,1462277921,1462277883,'','',''),(194,229,'',0,'@TGS#34SNNUAE6',0,0,0,0,0,NULL,0,2147483647,0,'',2,1462278308,1462278334,1462278328,'','',''),(195,229,'',0,'@TGS#3FWBMUAEI',0,0,0,0,0,NULL,0,2147483647,0,'',2,1462278757,1462278766,NULL,'','',''),(196,226,'',2,'@TGS#3U2CMUAES',2,0,0,0,0,NULL,0,2147483647,0,'',2,1462279617,1462279670,1462279669,'','',''),(197,226,'',0,'@TGS#3YGPNUAE2',2,0,0,0,0,NULL,0,2147483647,0,'',2,1462279860,1462280177,1462280175,'','',''),(198,229,'',0,'@TGS#3D2DMUAEC',0,0,0,0,0,NULL,0,2147483647,0,'',2,1462280187,1462280192,NULL,'','',''),(199,229,'',0,'@TGS#3C2DMUAEB',0,0,0,0,0,NULL,0,2147483647,0,'',2,1462280192,1462280193,NULL,'','',''),(200,229,'',0,'@TGS#3RKDMUAEK',0,0,0,0,0,NULL,0,2147483647,0,'',2,1462280193,1462280273,NULL,'','',''),(201,229,'',1,'@TGS#3XBEMUAEI',1,0,0,0,0,NULL,0,2147483647,0,'',2,1462280222,1462280256,1462280238,'','',''),(202,229,'',0,'@TGS#3ARDMUAEA',0,0,0,0,0,NULL,0,2147483647,0,'',2,1462280260,1462280266,NULL,'','',''),(203,229,'',1,'@TGS#3UQDMUAET',2,1,0,0,0,NULL,0.0024390243902439,2147483647,0,'',2,1462280276,1462280693,1462280685,'','',''),(204,226,'',0,'@TGS#3FUEMUAEJ',0,0,0,0,0,NULL,0,2147483647,0,'',2,1462280724,1462280739,NULL,'','',''),(205,229,'',0,'@TGS#3E3EMUAEF',0,0,0,0,0,NULL,0,2147483647,0,'',2,1462280746,1462280752,NULL,'','',''),(206,229,'',0,'@TGS#3WLEMUAER',0,0,0,0,0,NULL,0,2147483647,0,'',2,1462280752,1462280766,NULL,'','',''),(207,229,'',0,'@TGS#3V2EMUAEV',0,0,0,0,0,NULL,0,2147483647,0,'',2,1462280766,1462280818,1462280812,'','',''),(208,229,'',0,'@TGS#3WJEMUAEP',0,0,0,0,0,NULL,0,2147483647,0,'',2,1462280822,1462280828,NULL,'','',''),(209,229,'',0,'@TGS#3XZEMUAEB',0,0,0,0,0,NULL,0,2147483647,0,'',2,1462280832,1462280841,NULL,'','',''),(210,229,'',0,'@TGS#3NCQNUAEM',1,3,0,0,0,NULL,0.00678733031674208,2147483647,0,'',2,1462280855,1462281308,1462281296,'','',''),(211,229,'',2,'@TGS#3PXQNUAEE',3,60,0,3,0,NULL,0.434782608695652,2147483647,0,'',2,1462281401,1462281539,1462281538,'','',''),(212,229,'',0,'@TGS#3P6QNUAEB',0,0,0,0,0,NULL,0,2147483647,0,'',2,1462281585,1462281594,NULL,'','',''),(213,229,'',0,'@TGS#345QNUAED',0,0,0,0,0,NULL,0,2147483647,0,'',2,1462281614,1462281633,1462281632,'','',''),(214,229,'',0,'@TGS#3UQFMUAEV',2,164,0,0,0,NULL,0.611940298507463,2147483647,0,'',2,1462281639,1462281913,1462281906,'','',''),(215,165,'',0,'@TGS#3GZFMUAEQ',3,287,0,0,0,NULL,1.44949494949495,2147483647,0,'',2,1462281850,1462282050,1462282047,'http://2632.liveplay.myqcloud.com/2632_885d252a113211e6b91fa4dcbef5e35a.m3u8','rtmp://2632.liveplay.myqcloud.com/live/2632_885d252a113211e6b91fa4dcbef5e35a','16093104850682423826'),(216,170,'',0,'@TGS#3YGRNUAE4',0,0,0,2669,0,NULL,0,2147483647,0,'',2,1462282041,1462283067,1462283062,'http://2632.liveplay.myqcloud.com/2632_885d252a113211e6b91fa4dcbef5e35a.m3u8','rtmp://2632.liveplay.myqcloud.com/live/2632_885d252a113211e6b91fa4dcbef5e35a','16093104850682423826'),(217,229,'',0,'@TGS#32YRNUAEH',1,46,0,0,0,NULL,0.5,2147483647,0,'',2,1462282056,1462282151,1462282147,'','',''),(218,226,'',0,'@TGS#32ORNUAE4',3,0,0,0,0,NULL,0,2147483647,0,'',2,1462282156,1462283557,1462283552,'','',''),(219,229,'',0,'@TGS#3MJTNUAEV',0,0,0,0,0,NULL,0,2147483647,0,'',2,1462283318,1462283340,1462283334,'','',''),(220,229,'',0,'@TGS#3ZRTNUAEL',0,0,0,0,0,NULL,0,2147483647,0,'',2,1462283563,1462283579,1462283579,'','',''),(221,165,'',0,'@TGS#357TNUAEJ',0,0,0,0,0,NULL,0,2147483647,0,'',2,1462284595,1462284601,NULL,'','',''),(222,165,'',0,'@TGS#3HRIMUAEM',0,0,0,0,0,NULL,0,2147483647,0,'',1,1462284601,NULL,NULL,'','','');
/*!40000 ALTER TABLE `live_liveroom` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `live_roommember`
--

DROP TABLE IF EXISTS `live_roommember`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `live_roommember` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `member_id` int(11) NOT NULL,
  `room_id` int(11) NOT NULL,
  `valid` tinyint(1) NOT NULL,
  `join_time` datetime NOT NULL,
  `exit_time` datetime NOT NULL,
  `is_admin` int(11) NOT NULL,
  `is_block_speak` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `live_roommember_b3c09425` (`member_id`),
  KEY `live_roommember_c9f5884f` (`room_id`),
  KEY `live_roommember_b7517c44` (`valid`),
  KEY `live_roommember_a85e7d75` (`join_time`),
  KEY `live_roommember_8346fd6d` (`exit_time`),
  KEY `live_roommember_32512944` (`is_admin`),
  KEY `live_roommember_39699a2d` (`is_block_speak`),
  CONSTRAINT `member_id_refs_id_8c364c08` FOREIGN KEY (`member_id`) REFERENCES `customer_user` (`id`),
  CONSTRAINT `room_id_refs_id_0d358492` FOREIGN KEY (`room_id`) REFERENCES `live_liveroom` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=140 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `live_roommember`
--

LOCK TABLES `live_roommember` WRITE;
/*!40000 ALTER TABLE `live_roommember` DISABLE KEYS */;
INSERT INTO `live_roommember` VALUES (1,165,3,0,'2016-04-28 21:19:55','2016-04-28 21:22:29',0,0),(2,171,4,0,'2016-04-28 21:31:03','2016-04-28 21:31:35',0,0),(3,170,6,0,'2016-04-28 21:32:37','2016-04-28 21:35:17',0,0),(4,171,8,0,'2016-04-28 21:45:58','2016-04-28 21:46:22',0,0),(5,169,13,1,'2016-04-29 10:13:41','2016-04-29 10:13:31',0,0),(6,165,13,0,'2016-04-29 10:13:32','2016-04-29 10:13:35',0,0),(7,165,14,0,'2016-04-29 10:14:13','2016-04-29 10:14:22',0,0),(8,166,15,0,'2016-04-29 10:23:23','2016-04-29 10:23:28',0,0),(9,166,13,1,'2016-04-29 10:24:17','2016-04-29 10:24:17',0,0),(10,169,17,0,'2016-04-29 10:26:49','2016-04-29 10:27:04',0,0),(11,166,18,0,'2016-04-29 10:27:14','2016-04-29 10:27:21',0,0),(12,226,20,0,'2016-04-29 10:42:43','2016-04-29 10:42:52',0,0),(13,226,21,0,'2016-04-29 10:43:15','2016-04-29 10:49:20',0,0),(14,168,20,0,'2016-04-29 10:45:08','2016-04-29 10:45:21',0,0),(15,225,30,0,'2016-04-29 10:58:15','2016-04-29 10:59:04',0,0),(16,225,33,0,'2016-04-29 11:07:11','2016-04-29 11:07:35',0,0),(17,225,37,1,'2016-04-29 11:19:35','2016-04-29 11:19:19',0,0),(18,225,42,0,'2016-04-29 11:20:06','2016-04-29 11:20:12',0,0),(19,225,13,1,'2016-04-29 11:20:57','2016-04-29 11:20:14',0,0),(20,225,40,0,'2016-04-29 11:23:41','2016-04-29 11:24:06',0,0),(21,228,47,0,'2016-04-29 11:31:38','2016-04-29 11:31:44',0,0),(22,228,48,0,'2016-04-29 11:32:41','2016-04-29 11:32:52',0,0),(23,209,40,0,'2016-04-29 11:55:20','2016-04-29 11:56:04',0,0),(24,229,61,0,'2016-04-29 11:57:57','2016-04-29 11:58:27',0,0),(25,229,62,0,'2016-04-29 11:58:46','2016-04-29 11:59:40',0,0),(26,209,59,0,'2016-04-29 12:01:48','2016-04-29 12:03:11',0,0),(27,228,60,0,'2016-04-29 12:14:45','2016-04-29 12:15:38',0,0),(28,234,68,0,'2016-04-29 13:30:12','2016-04-29 13:30:19',0,0),(29,168,13,1,'2016-04-29 14:42:44','2016-04-29 13:52:17',0,0),(30,209,74,0,'2016-04-29 14:01:37','2016-04-29 14:01:45',0,0),(31,168,75,0,'2016-04-29 14:02:36','2016-04-29 14:03:12',0,0),(32,166,75,0,'2016-04-29 14:02:39','2016-04-29 14:06:48',0,0),(33,168,73,0,'2016-04-29 14:03:18','2016-04-29 14:03:21',0,0),(34,228,76,0,'2016-04-29 14:03:25','2016-04-29 14:03:30',0,0),(35,234,77,0,'2016-04-29 14:10:04','2016-04-29 14:10:58',0,0),(36,234,78,0,'2016-04-29 14:14:45','2016-04-29 14:15:01',0,0),(37,165,79,0,'2016-04-29 14:18:06','2016-04-29 14:22:16',0,0),(38,228,80,0,'2016-04-29 14:22:50','2016-04-29 14:23:05',0,0),(39,228,81,0,'2016-04-29 14:26:33','2016-04-29 14:26:42',0,0),(40,168,82,0,'2016-04-29 14:32:47','2016-04-29 14:32:51',0,0),(41,165,85,1,'2016-04-29 14:52:59','2016-04-29 14:52:59',0,0),(42,229,86,0,'2016-04-29 14:53:57','2016-04-29 14:54:12',0,0),(43,165,87,1,'2016-04-29 15:05:50','2016-04-29 15:05:50',0,0),(44,229,88,1,'2016-04-29 15:08:48','2016-04-29 15:08:45',0,0),(45,165,90,1,'2016-04-29 15:42:46','2016-04-29 15:42:37',0,0),(46,236,91,0,'2016-04-29 15:47:55','2016-04-29 15:47:58',0,0),(47,236,92,0,'2016-04-29 15:48:10','2016-04-29 15:48:23',0,0),(48,165,94,1,'2016-04-29 15:50:39','2016-04-29 15:50:39',0,0),(49,236,95,0,'2016-04-29 15:52:07','2016-04-29 15:52:30',0,0),(50,230,94,0,'2016-04-29 16:02:40','2016-04-29 16:02:43',0,0),(51,230,96,0,'2016-04-29 16:02:49','2016-04-29 16:03:01',0,0),(52,225,98,0,'2016-04-29 16:22:56','2016-04-29 16:24:23',0,0),(53,225,99,0,'2016-04-29 16:24:44','2016-04-29 16:26:09',0,0),(54,209,102,0,'2016-04-29 16:37:58','2016-04-29 16:38:24',0,0),(55,229,113,1,'2016-04-29 17:26:09','2016-04-29 17:26:09',0,0),(56,165,113,1,'2016-04-29 17:27:25','2016-04-29 17:27:25',0,0),(57,229,114,0,'2016-04-29 17:28:13','2016-04-29 17:33:52',0,0),(58,168,115,0,'2016-04-29 17:29:24','2016-04-29 17:29:27',0,0),(59,168,114,0,'2016-04-29 17:29:28','2016-04-29 17:29:31',0,0),(60,229,116,0,'2016-04-29 17:35:03','2016-04-29 17:35:16',0,0),(61,229,117,0,'2016-04-29 17:51:22','2016-04-29 17:55:14',0,0),(62,229,118,1,'2016-04-29 17:55:20','2016-04-29 17:55:20',0,0),(63,229,119,0,'2016-04-29 17:59:08','2016-04-29 18:01:48',0,0),(64,229,120,1,'2016-04-29 18:01:52','2016-04-29 18:01:52',0,0),(65,237,123,1,'2016-04-29 18:42:37','2016-04-29 18:42:37',0,0),(66,170,123,1,'2016-04-29 18:45:29','2016-04-29 18:42:55',0,0),(67,237,125,0,'2016-04-29 18:45:10','2016-04-29 18:45:41',0,0),(68,237,126,0,'2016-04-29 18:47:39','2016-04-29 18:48:21',0,0),(69,238,127,0,'2016-04-29 19:05:26','2016-04-29 19:05:32',0,0),(70,238,128,1,'2016-04-29 19:17:25','2016-04-29 19:09:19',0,0),(71,170,128,0,'2016-04-29 19:17:25','2016-04-29 19:18:53',0,0),(72,165,132,1,'2016-04-29 19:38:18','2016-04-29 19:38:18',0,0),(73,166,132,0,'2016-04-29 19:38:31','2016-04-29 19:39:44',0,0),(74,229,135,1,'2016-04-29 19:56:45','2016-04-29 19:56:45',0,0),(75,229,136,0,'2016-04-29 21:54:28','2016-04-29 21:54:36',0,0),(76,168,139,0,'2016-05-03 11:02:32','2016-05-03 11:02:39',0,0),(77,241,148,0,'2016-05-03 15:17:12','2016-05-03 15:17:27',1,1),(78,170,148,0,'2016-05-03 15:15:22','2016-05-03 15:18:02',1,0),(79,229,148,0,'2016-05-03 15:13:41','2016-05-03 15:17:55',1,1),(80,168,148,0,'2016-05-03 15:10:33','2016-05-03 15:17:16',1,1),(81,165,150,1,'2016-05-03 15:19:21','2016-05-03 15:19:21',0,0),(82,229,152,0,'2016-05-03 15:21:28','2016-05-03 15:27:49',0,0),(83,241,152,1,'2016-05-03 15:21:46','2016-05-03 15:21:46',0,0),(84,166,152,0,'2016-05-03 15:21:54','2016-05-03 15:31:46',0,0),(85,229,153,1,'2016-05-03 15:32:23','2016-05-03 15:32:23',0,0),(86,166,153,0,'2016-05-03 15:32:28','2016-05-03 15:34:14',0,0),(87,165,155,1,'2016-05-03 15:47:15','2016-05-03 15:47:15',0,0),(88,170,159,1,'2016-05-03 15:54:46','2016-05-03 15:54:46',0,0),(89,225,162,0,'2016-05-03 15:55:08','2016-05-03 15:55:12',0,0),(90,225,165,0,'2016-05-03 15:58:29','2016-05-03 15:58:35',0,0),(91,166,168,0,'2016-05-03 16:38:59','2016-05-03 16:39:08',0,0),(92,166,169,0,'2016-05-03 16:39:28','2016-05-03 17:12:35',0,0),(93,165,170,1,'2016-05-03 16:53:42','2016-05-03 16:53:42',0,0),(94,229,170,1,'2016-05-03 16:56:39','2016-05-03 16:56:39',0,0),(95,165,171,1,'2016-05-03 16:57:18','2016-05-03 16:57:18',0,0),(96,226,171,0,'2016-05-03 17:00:29','2016-05-03 17:09:28',0,0),(97,165,172,1,'2016-05-03 17:12:42','2016-05-03 17:12:40',0,0),(98,226,172,0,'2016-05-03 17:12:58','2016-05-03 17:14:28',0,0),(99,229,173,1,'2016-05-03 17:15:11','2016-05-03 17:15:11',0,0),(100,229,174,1,'2016-05-03 17:15:53','2016-05-03 17:15:53',0,0),(101,229,175,1,'2016-05-03 17:20:53','2016-05-03 17:20:53',0,0),(102,225,177,1,'2016-05-03 17:31:31','2016-05-03 17:30:33',0,0),(103,225,184,0,'2016-05-03 17:33:35','2016-05-03 17:56:44',0,0),(104,229,187,1,'2016-05-03 18:32:51','2016-05-03 18:23:32',0,0),(105,168,188,0,'2016-05-03 18:55:23','2016-05-03 18:55:27',0,0),(106,241,177,1,'2016-05-03 18:55:19','2016-05-03 18:54:11',0,0),(107,168,177,0,'2016-05-03 18:55:28','2016-05-03 18:55:35',0,0),(108,241,188,0,'2016-05-03 18:55:44','2016-05-03 18:56:01',0,0),(109,241,190,1,'2016-05-03 19:57:27','2016-05-03 19:48:21',1,0),(110,165,196,1,'2016-05-03 20:47:19','2016-05-03 20:47:19',1,0),(111,229,196,1,'2016-05-03 20:47:19','2016-05-03 20:47:19',1,0),(112,229,197,1,'2016-05-03 20:55:03','2016-05-03 20:55:01',1,0),(113,165,197,1,'2016-05-03 20:51:22','2016-05-03 20:51:22',1,0),(114,226,200,0,'2016-05-03 20:56:50','2016-05-03 20:56:56',0,0),(115,226,201,0,'2016-05-03 20:57:09','2016-05-03 20:57:28',0,0),(116,229,200,1,'2016-05-03 20:57:50','2016-05-03 20:57:50',0,0),(117,226,203,0,'2016-05-03 21:02:53','2016-05-03 21:04:53',0,0),(118,165,203,0,'2016-05-03 21:03:55','2016-05-03 21:04:07',0,0),(119,229,204,1,'2016-05-03 21:05:28','2016-05-03 21:05:28',0,0),(120,226,207,1,'2016-05-03 21:06:45','2016-05-03 21:06:45',0,0),(121,226,210,0,'2016-05-03 21:07:41','2016-05-03 21:11:05',0,0),(122,226,211,0,'2016-05-03 21:17:26','2016-05-03 21:18:15',0,0),(123,170,211,0,'2016-05-03 21:16:55','2016-05-03 21:18:59',0,0),(124,241,211,1,'2016-05-03 21:17:28','2016-05-03 21:17:28',0,0),(125,226,213,1,'2016-05-03 21:20:24','2016-05-03 21:20:24',0,0),(126,226,214,0,'2016-05-03 21:21:03','2016-05-03 21:24:16',0,0),(127,165,214,0,'2016-05-03 21:22:06','2016-05-03 21:24:07',0,0),(128,226,215,0,'2016-05-03 21:24:47','2016-05-03 21:27:24',0,0),(129,229,215,0,'2016-05-03 21:26:01','2016-05-03 21:27:20',0,0),(130,170,215,0,'2016-05-03 21:25:36','2016-05-03 21:27:18',0,0),(131,226,217,0,'2016-05-03 21:28:57','2016-05-03 21:29:07',0,0),(132,229,218,0,'2016-05-03 21:51:07','2016-05-03 21:52:28',1,0),(133,165,217,1,'2016-05-03 21:29:39','2016-05-03 21:29:39',0,0),(134,165,218,1,'2016-05-03 21:45:32','2016-05-03 21:30:16',1,0),(135,241,191,1,'2016-05-03 21:30:46','2016-05-03 21:30:46',0,0),(136,241,218,0,'2016-05-03 21:33:36','2016-05-03 21:33:45',0,0),(137,244,218,0,'2016-05-03 21:45:51','2016-05-03 21:46:00',0,0),(138,226,220,0,'2016-05-03 21:52:50','2016-05-03 21:52:53',0,0),(139,229,191,1,'2016-05-03 21:53:59','2016-05-03 21:53:59',0,0);
/*!40000 ALTER TABLE `live_roommember` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `live_roomusergift`
--

DROP TABLE IF EXISTS `live_roomusergift`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `live_roomusergift` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `room_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `sender_id` int(11) NOT NULL,
  `gift_id` int(11) NOT NULL,
  `num` int(11) NOT NULL,
  `cost` int(11) NOT NULL,
  `ticket` int(11) NOT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `live_roomusergift_c9f5884f` (`room_id`),
  KEY `live_roomusergift_6340c63c` (`user_id`),
  KEY `live_roomusergift_0a681a64` (`sender_id`),
  KEY `live_roomusergift_46862fea` (`gift_id`),
  KEY `live_roomusergift_96511a37` (`created_at`),
  CONSTRAINT `gift_id_refs_id_bea6cf0a` FOREIGN KEY (`gift_id`) REFERENCES `customer_gift` (`id`),
  CONSTRAINT `room_id_refs_id_7b73b91e` FOREIGN KEY (`room_id`) REFERENCES `live_liveroom` (`id`),
  CONSTRAINT `sender_id_refs_id_ac8436e5` FOREIGN KEY (`sender_id`) REFERENCES `customer_user` (`id`),
  CONSTRAINT `user_id_refs_id_ac8436e5` FOREIGN KEY (`user_id`) REFERENCES `customer_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `live_roomusergift`
--

LOCK TABLES `live_roomusergift` WRITE;
/*!40000 ALTER TABLE `live_roomusergift` DISABLE KEYS */;
INSERT INTO `live_roomusergift` VALUES (1,90,229,165,8,12,180,180,'2016-04-29 15:42:53'),(2,90,229,165,7,4,264,264,'2016-04-29 15:43:00'),(3,90,229,165,16,1,299,299,'2016-04-29 15:43:09'),(4,91,165,236,6,1,521,521,'2016-04-29 15:47:02'),(5,92,165,236,4,1,5000,5000,'2016-04-29 15:48:17'),(6,95,230,236,1,1,2666,2666,'2016-04-29 15:52:26'),(7,98,209,225,8,3,45,45,'2016-04-29 16:23:04'),(8,98,209,225,11,1,5,5,'2016-04-29 16:24:05'),(9,99,209,225,13,1,2,2,'2016-04-29 16:26:04'),(10,148,244,241,13,2,4,4,'2016-05-03 14:53:55'),(11,148,244,241,9,2,6,6,'2016-05-03 14:53:58'),(12,148,244,241,11,1,5,5,'2016-05-03 14:54:02'),(13,148,244,241,4,1,5000,5000,'2016-05-03 14:54:23'),(14,148,244,241,15,2,2,2,'2016-05-03 14:56:07'),(15,152,165,241,13,1,2,2,'2016-05-03 15:21:59'),(16,152,165,241,9,1,3,3,'2016-05-03 15:22:02'),(17,152,165,241,11,1,5,5,'2016-05-03 15:22:02'),(18,152,165,241,8,1,15,15,'2016-05-03 15:22:06'),(19,152,165,241,12,2,20,20,'2016-05-03 15:22:06'),(20,152,165,241,7,1,66,66,'2016-05-03 15:22:08'),(21,184,245,225,17,1,999,999,'2016-05-03 17:34:26'),(22,184,245,225,15,92,92,19,'2016-05-03 17:34:31'),(23,190,170,241,15,1,1,1,'2016-05-03 19:48:28'),(24,190,170,241,13,1,2,2,'2016-05-03 19:48:32'),(25,190,170,241,1,1,2666,2666,'2016-05-03 19:48:37'),(26,211,229,241,15,1,1,1,'2016-05-03 21:17:35'),(27,211,229,241,13,1,2,2,'2016-05-03 21:17:54');
/*!40000 ALTER TABLE `live_roomusergift` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `live_systemmessage`
--

DROP TABLE IF EXISTS `live_systemmessage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `live_systemmessage` (
  `id` int(11) NOT NULL DEFAULT '0',
  `desc` text NOT NULL,
  `created_time` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `live_systemmessage`
--

LOCK TABLES `live_systemmessage` WRITE;
/*!40000 ALTER TABLE `live_systemmessage` DISABLE KEYS */;
INSERT INTO `live_systemmessage` VALUES (0,'禁止黄色赌博等非法','2016-03-25 12:52:44');
/*!40000 ALTER TABLE `live_systemmessage` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `statistics_fillinorder`
--

DROP TABLE IF EXISTS `statistics_fillinorder`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `statistics_fillinorder` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sale_day` double NOT NULL,
  `buyer_day` int(11) NOT NULL,
  `order_day` int(11) NOT NULL,
  `sale_total` double NOT NULL,
  `buyer_total` int(11) NOT NULL,
  `order_total` int(11) NOT NULL,
  `date` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `statistics_fillinorder`
--

LOCK TABLES `statistics_fillinorder` WRITE;
/*!40000 ALTER TABLE `statistics_fillinorder` DISABLE KEYS */;
INSERT INTO `statistics_fillinorder` VALUES (1,0,0,0,7,6,20,'20160502'),(2,0,0,0,7,6,23,'20160503');
/*!40000 ALTER TABLE `statistics_fillinorder` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `statistics_fillinpaytype`
--

DROP TABLE IF EXISTS `statistics_fillinpaytype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `statistics_fillinpaytype` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `iap_day` double DEFAULT NULL,
  `wechat_day` double DEFAULT NULL,
  `wechat_js_day` double DEFAULT NULL,
  `total_day` double DEFAULT NULL,
  `iap_total` double DEFAULT NULL,
  `wechat_total` double DEFAULT NULL,
  `wechat_js_total` double DEFAULT NULL,
  `total` double DEFAULT NULL,
  `date` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `statistics_fillinpaytype`
--

LOCK TABLES `statistics_fillinpaytype` WRITE;
/*!40000 ALTER TABLE `statistics_fillinpaytype` DISABLE KEYS */;
INSERT INTO `statistics_fillinpaytype` VALUES (1,0,4,0,4,10,15,8,33,'20160426'),(2,0,6,0,6,10,20,8,38,'20160427'),(3,0,0,0,0,0,4,3,7,'20160502'),(4,0,0,0,0,0,4,3,7,'20160503');
/*!40000 ALTER TABLE `statistics_fillinpaytype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `statistics_premiumuser`
--

DROP TABLE IF EXISTS `statistics_premiumuser`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `statistics_premiumuser` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `premium_users` int(11) NOT NULL,
  `total_users` int(11) NOT NULL,
  `premium_rate` double NOT NULL,
  `purchase_time` int(11) NOT NULL,
  `gift_time` int(11) NOT NULL,
  `time_stamp` datetime NOT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `statistics_premiumuser`
--

LOCK TABLES `statistics_premiumuser` WRITE;
/*!40000 ALTER TABLE `statistics_premiumuser` DISABLE KEYS */;
INSERT INTO `statistics_premiumuser` VALUES (1,0,32,0,0,0,'2016-05-03 00:00:00','2016-05-03 15:39:29'),(2,0,34,0,0,0,'2016-05-04 00:00:00','2016-05-04 00:00:02');
/*!40000 ALTER TABLE `statistics_premiumuser` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `statistics_revenue`
--

DROP TABLE IF EXISTS `statistics_revenue`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `statistics_revenue` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `arpl_day` int(11) NOT NULL,
  `arpu_month` double NOT NULL,
  `arpp_total` double NOT NULL,
  `arpu_total` double NOT NULL,
  `date` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `statistics_revenue`
--

LOCK TABLES `statistics_revenue` WRITE;
/*!40000 ALTER TABLE `statistics_revenue` DISABLE KEYS */;
INSERT INTO `statistics_revenue` VALUES (1,0,0,0.205882352941176,0,'20160502'),(2,0,0,0.205882352941176,0,'20160503');
/*!40000 ALTER TABLE `statistics_revenue` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `statistics_ugcandbrand`
--

DROP TABLE IF EXISTS `statistics_ugcandbrand`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `statistics_ugcandbrand` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `anchor_count` int(11) NOT NULL,
  `anchor_rate` double NOT NULL,
  `share_count` int(11) NOT NULL,
  `share_rate` double NOT NULL,
  `date` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `statistics_ugcandbrand`
--

LOCK TABLES `statistics_ugcandbrand` WRITE;
/*!40000 ALTER TABLE `statistics_ugcandbrand` DISABLE KEYS */;
INSERT INTO `statistics_ugcandbrand` VALUES (1,19,0.558823529411765,0,0,'20160502'),(2,20,0.588235294117647,0,0,'20160503');
/*!40000 ALTER TABLE `statistics_ugcandbrand` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-05-04 14:56:22
