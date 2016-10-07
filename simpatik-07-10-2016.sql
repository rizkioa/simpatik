-- MySQL dump 10.13  Distrib 5.5.51, for Win32 (x86)
--
-- Host: localhost    Database: simpatik
-- ------------------------------------------------------
-- Server version	5.5.51

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
-- Table structure for table `accounts_account`
--

DROP TABLE IF EXISTS `accounts_account`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `accounts_account` (
  `identitaspribadi_ptr_id` int(11) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(40) NOT NULL,
  `foto` varchar(255) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_admin` tinyint(1) NOT NULL,
  PRIMARY KEY (`identitaspribadi_ptr_id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_account`
--

LOCK TABLES `accounts_account` WRITE;
/*!40000 ALTER TABLE `accounts_account` DISABLE KEYS */;
INSERT INTO `accounts_account` VALUES (1,'pbkdf2_sha256$20000$vsrZkkNlIY6c$S5xXXRHtrjxrlCOgh1qClosEOgaBmaxMzCzlrGRP1rU=','2016-10-07 03:26:14',1,'admin','',1,1),(62,'pbkdf2_sha256$20000$f2pqEsz1qWdS$GSD9JbjeHamFgQ10oARnzuH4EDUGMxKuO6ojCn/cy0Y=','2016-10-04 04:52:28',0,'operator','',1,1),(73,'pbkdf2_sha256$20000$XbhKXTllQAho$WmgznsDvf5RidMYFh/dd3ShnadNVMJhxaCtHNVIyF/M=','2016-09-28 05:38:18',0,'inputan','',1,1),(268,'','2016-10-06 07:10:32',0,'195811291989121002','',1,0),(269,'',NULL,0,'196503141992021001','',1,0),(270,'',NULL,0,'195803181985031012','',1,0),(271,'',NULL,0,'196702041993022001','',1,0),(272,'','2016-10-06 05:57:08',0,'198404242010011030','',1,0),(273,'','2016-10-06 06:57:35',0,'197210211997032004','',1,0),(274,'',NULL,0,'197508171994121001','',1,0),(275,'',NULL,0,'198201292005011002','',1,0),(276,'',NULL,0,'196211121986032010','',1,0),(277,'',NULL,0,'197911162005011011','',1,0),(278,'',NULL,0,'198301102005012003','',1,0),(279,'',NULL,0,'195808231985031015','',1,0),(280,'',NULL,0,'196206101982032014','',1,0),(281,'','2016-10-06 03:49:27',0,'197205271992082001','',1,0),(282,'','2016-10-06 04:01:41',0,'197811162005012009','',1,0),(283,'','2016-10-06 03:00:46',0,'198107292005011009','',1,0),(284,'','2016-10-06 03:05:59',0,'197510251996022003','',1,0),(285,'',NULL,0,'197009211994032007','',1,0),(286,'',NULL,0,'197202031993031005','',1,0),(287,'',NULL,0,'197408132005011009','',1,0),(288,'',NULL,0,'196208111983032014','',1,0),(289,'',NULL,0,'198112172010012015','',1,0),(290,'',NULL,0,'197004021993031011','',1,0),(291,'',NULL,0,'197108152009011003','',1,0),(292,'',NULL,0,'198510262009011001','',1,0),(293,'',NULL,0,'198912302010101001','',1,0),(294,'',NULL,0,'198009042011011005','',1,0),(295,'',NULL,0,'199104012012061001','',1,0),(296,'',NULL,0,'197907132002121004','',1,0),(297,'',NULL,0,'197002062007012016','',1,0),(298,'',NULL,0,'197811202008011009','',1,0),(299,'',NULL,0,'198411052010012002','',1,0),(300,'',NULL,0,'196612202009011003','',1,0),(301,'',NULL,0,'198909252015022002','',1,0),(302,'',NULL,0,'198708042015021002','',1,0),(303,'',NULL,0,'3571010907570003','',1,0),(304,'',NULL,0,'3506254102840002','',1,0),(305,'',NULL,0,'3506251009700005','',1,0),(392,'',NULL,0,'1234','',1,0),(414,'',NULL,0,'12123','',1,0),(502,'',NULL,0,'123','',1,0),(505,'',NULL,0,'1234567890','',1,0),(533,'',NULL,0,'12345678901','',1,0),(557,'',NULL,0,'3506214806740001','',1,0),(580,'',NULL,0,'123452354234234','',1,0);
/*!40000 ALTER TABLE `accounts_account` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_account_groups`
--

DROP TABLE IF EXISTS `accounts_account_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `accounts_account_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `account_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `account_id` (`account_id`,`group_id`),
  CONSTRAINT `a_account_id_290d804_fk_accounts_account_identitaspribadi_ptr_id` FOREIGN KEY (`account_id`) REFERENCES `accounts_account` (`identitaspribadi_ptr_id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_account_groups`
--

LOCK TABLES `accounts_account_groups` WRITE;
/*!40000 ALTER TABLE `accounts_account_groups` DISABLE KEYS */;
INSERT INTO `accounts_account_groups` VALUES (1,62,1),(2,73,2),(7,268,5),(11,272,1),(3,273,3),(4,274,3),(5,275,3),(6,281,4),(8,282,7),(9,283,8),(10,284,9);
/*!40000 ALTER TABLE `accounts_account_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_account_user_permissions`
--

DROP TABLE IF EXISTS `accounts_account_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `accounts_account_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `account_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `account_id` (`account_id`,`permission_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_account_user_permissions`
--

LOCK TABLES `accounts_account_user_permissions` WRITE;
/*!40000 ALTER TABLE `accounts_account_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `accounts_account_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_identitaspribadi`
--

DROP TABLE IF EXISTS `accounts_identitaspribadi`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `accounts_identitaspribadi` (
  `nama_lengkap` varchar(100) NOT NULL,
  `tempat_lahir` varchar(30) DEFAULT NULL,
  `tanggal_lahir` date DEFAULT NULL,
  `telephone` varchar(50) DEFAULT NULL,
  `email` varchar(254) DEFAULT NULL,
  `desa_id` int(11) DEFAULT NULL,
  `alamat` varchar(255) DEFAULT NULL,
  `lintang` varchar(255) DEFAULT NULL,
  `bujur` varchar(255) DEFAULT NULL,
  `kewarganegaraan` varchar(100) DEFAULT NULL,
  `pekerjaan` varchar(255) DEFAULT NULL,
  `keterangan` varchar(255) DEFAULT NULL,
  `hp` varchar(50) DEFAULT NULL,
  `atributtambahan_ptr_id` int(11) NOT NULL,
  PRIMARY KEY (`atributtambahan_ptr_id`),
  UNIQUE KEY `email` (`email`),
  KEY `accounts_identitaspribadi_desa_id_6bd293d3_fk_master_desa_id` (`desa_id`),
  CONSTRAINT `accounts_identitaspribadi_desa_id_6bd293d3_fk_master_desa_id` FOREIGN KEY (`desa_id`) REFERENCES `master_desa` (`id`),
  CONSTRAINT `acc_atributtambahan_ptr_id_183e9183_fk_master_atributtambahan_id` FOREIGN KEY (`atributtambahan_ptr_id`) REFERENCES `master_atributtambahan` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_identitaspribadi`
--

LOCK TABLES `accounts_identitaspribadi` WRITE;
/*!40000 ALTER TABLE `accounts_identitaspribadi` DISABLE KEYS */;
INSERT INTO `accounts_identitaspribadi` VALUES ('TAUFAN BUDIMAN',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,1),('OPERATOR','',NULL,'',NULL,1,'Kediri','','','',NULL,NULL,NULL,62),('INPUTAN','',NULL,'',NULL,1,'Kediri','','','',NULL,NULL,NULL,73),('INDRA TARUNA','',NULL,'','',18,'.',NULL,NULL,NULL,NULL,'',NULL,268),('ANDES ERWANTO','',NULL,'','ANDESERWANTO@mail.com',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,269),('NOEGROHO ADI','',NULL,'','NOEGROHOADI@mail.com',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,270),('INDIYAH SETIANI','',NULL,'','INDIYAHSETIANI@mail.com',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,271),('DAMAS DANUR RENDRA','',NULL,'','DAMASDANURRENDRA@mail.com',18,'.',NULL,NULL,NULL,NULL,'',NULL,272),('AL INDAH','',NULL,'','ALINDAH@mail.com',18,'.',NULL,NULL,NULL,NULL,'',NULL,273),('AGUSTIAWAN','',NULL,'','AGUSTIAWAN@mail.com',18,'.',NULL,NULL,NULL,NULL,'',NULL,274),('DEVIN MARSFIAN S','',NULL,'','DEVINMARSFIANS@mail.com',18,'.',NULL,NULL,NULL,NULL,'',NULL,275),('NANIK SRI HANDAYATININGSIH','',NULL,'','NANIKSRIHANDAYATININGSIH@mail.com',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,276),('A. DENNY SETYAWAN','',NULL,'','A.DENNYSETYAWAN@mail.com',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,277),('MERY PURWANTY','',NULL,'','MERYPURWANTY@mail.com',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,278),('MARUF','',NULL,'','MARUF@mail.com',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,279),('JOENIA DEWI KOESTATI','',NULL,'','JOENIADEWIKOESTATI@mail.com',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,280),('EVA DAYANTI LW','',NULL,'','EVADAYANTILW@mail.com',18,'.',NULL,NULL,NULL,NULL,'',NULL,281),('DYAH KIRONOSARI','',NULL,'','DYAHKIRONOSARI@mail.com',18,'.',NULL,NULL,NULL,NULL,'',NULL,282),('ZAKY ZAMRONI','',NULL,'','ZAKYZAMRONI@mail.com',378,'.',NULL,NULL,NULL,NULL,'',NULL,283),('SRI WINARTI','',NULL,'','SRIWINARTI@mail.com',378,'.',NULL,NULL,NULL,NULL,'',NULL,284),('ERNA BUDI HERTANTI','',NULL,'','ERNABUDIHERTANTI@mail.com',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,285),('BUDI HERTANTO','',NULL,'','BUDIHERTANTO@mail.com',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,286),('ALI MASHURI','',NULL,'','ALIMASHURI@mail.com',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,287),('ENI SETYORINI','',NULL,'','ENISETYORINI@mail.com',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,288),('RIGEN PRAMAHERTI','',NULL,'','RIGENPRAMAHERTI@mail.com',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,289),('LAGIONO','',NULL,'','LAGIONO@mai.com',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,290),('DWI AGUS ROCHMADI','',NULL,'','DWIAGUSROCHMADI@mail.com',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,291),('ANDIKA N. YUDHIN','',NULL,'','ANDIKAN.YUDHIN@mail.com',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,292),('BAGUS S. JATMIKO','',NULL,'','BAGUSS.JATMIKO@mail.com',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,293),('HENDRA D. KURNIANTO','',NULL,'','HENDRAD.KURNIANTO@mail.com',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,294),('DZIKIR S. ATMAJA','',NULL,'','DZIKIRS.ATMAJA@mail.com',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,295),('HENRI RISDIANTO','',NULL,'','HENRIRISDIANTO@mail.com',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,296),('NANIK HARIYANI','',NULL,'','NANIKHARIYANI@mail.com',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,297),('ANDI SETIAWAN','',NULL,'','ANDISETIAWAN@mail.com',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,298),('PIPIT NOVIE MA','',NULL,'','PIPITNOVIEMA@mail.com',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,299),('BUDIYONO','',NULL,'','BUDIYONO@mail.com',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,300),('YUDHA RUKMANA KURNIAWATI','',NULL,'','YUDHARUKMANAKURNIAWATI@mail.com',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,301),('AGUNG ARIADI','',NULL,'','AGUNGARIADI@mail.com',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,302),('SAIFUL ANAM','',NULL,'','SAIFULANAM@mail.com',NULL,NULL,NULL,NULL,NULL,NULL,'',NULL,303),('AMALIA RIZKY','',NULL,'','AMALIARIZKY@mail.com',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,304),('CHRISAN NUSANTARA','',NULL,'','CHRISANNUSANTARA@mail.com',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,305),('FEBRI AHMAD NURHIDAYAT','',NULL,'085736662908','febryyachmad@gmail.com',368,'Kediri',NULL,NULL,'indonesia','Swasta',NULL,'',392),('ASD','',NULL,'12','12@mai.com',22,'jksd',NULL,NULL,'1','PNS',NULL,'12',414),('FA','',NULL,'123','E@mail.com',18,'as',NULL,NULL,'indonesia','Swasta',NULL,'',502),('FEBRI AHMAD NURHIDAYAT','',NULL,'085736662908','febryyachmad1@gmail.com',368,'Kediri',NULL,NULL,'indonesia','Swasta',NULL,'',505),('GILANG ROSA','',NULL,'085736660908','gilangros@mail.com',18,'Pamenang',NULL,NULL,'indonesua','Swasta',NULL,'+6234444444444',533),('INDAH SUSTIARI, SE','',NULL,'08563596381','rigenp@gmail.com',129,'Dsn. Kuwik RT 002/RW 002',NULL,NULL,'WNI','Wiraswasta',NULL,'+6299999999999',557),('TUTUT','',NULL,'098',NULL,18,'jalan pamenang',NULL,NULL,'indonesia','Swasta',NULL,'',580);
/*!40000 ALTER TABLE `accounts_identitaspribadi` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_nomoridentitaspengguna`
--

DROP TABLE IF EXISTS `accounts_nomoridentitaspengguna`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `accounts_nomoridentitaspengguna` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nomor` varchar(100) NOT NULL,
  `user_id` int(11) NOT NULL,
  `jenis_identitas_id` int(11) NOT NULL,
  `berkas_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nomor` (`nomor`),
  KEY `accounts_nomoridentitaspengguna_c42e8079` (`berkas_id`),
  CONSTRAINT `accou_berkas_id_1240b289_fk_master_berkas_atributtambahan_ptr_id` FOREIGN KEY (`berkas_id`) REFERENCES `master_berkas` (`atributtambahan_ptr_id`)
) ENGINE=InnoDB AUTO_INCREMENT=94 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_nomoridentitaspengguna`
--

LOCK TABLES `accounts_nomoridentitaspengguna` WRITE;
/*!40000 ALTER TABLE `accounts_nomoridentitaspengguna` DISABLE KEYS */;
INSERT INTO `accounts_nomoridentitaspengguna` VALUES (3,'3506221804900002',21,1,NULL),(5,'452342',9,1,NULL),(44,'195811291989121002',268,3,NULL),(45,'196503141992021001',269,3,NULL),(46,'195803181985031012',270,3,NULL),(47,'196702041993022001',271,3,NULL),(48,'198404242010011030',272,3,NULL),(49,'197210211997032004',273,3,NULL),(50,'197508171994121001',274,3,NULL),(51,'198201292005011002',275,3,NULL),(52,'196211121986032010',276,3,NULL),(53,'197911162005011011',277,3,NULL),(54,'198301102005012003',278,3,NULL),(55,'195808231985031015',279,3,NULL),(56,'196206101982032014',280,3,NULL),(57,'197205271992082001',281,3,NULL),(58,'197811162005012009',282,3,NULL),(59,'198107292005011009',283,3,NULL),(60,'197510251996022003',284,3,NULL),(61,'197009211994032007',285,3,NULL),(62,'197202031993031005',286,3,NULL),(63,'197408132005011009',287,3,NULL),(64,'196208111983032014',288,3,NULL),(65,'198112172010012015',289,3,NULL),(66,'197004021993031011',290,3,NULL),(67,'197108152009011003',291,3,NULL),(68,'198510262009011001',292,3,NULL),(69,'198912302010101001',293,3,NULL),(70,'198009042011011005',294,3,NULL),(71,'199104012012061001',295,3,NULL),(72,'197907132002121004',296,3,NULL),(73,'197002062007012016',297,3,NULL),(74,'197811202008011009',298,3,NULL),(75,'198411052010012002',299,3,NULL),(76,'196612202009011003',300,3,NULL),(77,'198909252015022002',301,3,NULL),(78,'198708042015021002',302,3,NULL),(79,'3571010907570003',303,3,NULL),(80,'3506254102840002',304,1,NULL),(81,'3506251009700005',305,4,NULL),(87,'1234',392,1,411),(88,'12123',414,1,NULL),(89,'123',502,1,NULL),(90,'1234567890',505,1,511),(91,'12345678901',533,1,542),(92,'3506214806740001',557,1,566),(93,'123452354234234',580,1,NULL);
/*!40000 ALTER TABLE `accounts_nomoridentitaspengguna` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `admin_tools_menu_bookmark`
--

DROP TABLE IF EXISTS `admin_tools_menu_bookmark`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `admin_tools_menu_bookmark` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `url` varchar(255) NOT NULL,
  `title` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `adm_user_id_24385082_fk_accounts_account_identitaspribadi_ptr_id` (`user_id`),
  CONSTRAINT `adm_user_id_24385082_fk_accounts_account_identitaspribadi_ptr_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_account` (`identitaspribadi_ptr_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin_tools_menu_bookmark`
--

LOCK TABLES `admin_tools_menu_bookmark` WRITE;
/*!40000 ALTER TABLE `admin_tools_menu_bookmark` DISABLE KEYS */;
/*!40000 ALTER TABLE `admin_tools_menu_bookmark` ENABLE KEYS */;
UNLOCK TABLES;

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
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
INSERT INTO `auth_group` VALUES (8,'Cetak'),(2,'Inputan'),(3,'Kabid'),(5,'Kadin'),(6,'Kasir'),(1,'Operator'),(4,'Pembuat Surat'),(7,'Penomoran'),(9,'Selesai');
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
  KEY `auth_group_permissi_permission_id_23962d04_fk_auth_permission_id` (`permission_id`),
  CONSTRAINT `auth_group_permissions_group_id_58c48ba9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_group_permissi_permission_id_23962d04_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=113 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
INSERT INTO `auth_group_permissions` VALUES (78,1,49),(79,1,50),(76,1,55),(82,1,56),(81,1,73),(75,1,74),(70,1,97),(71,1,98),(77,1,130),(80,1,131),(73,1,136),(74,1,137),(72,1,163),(88,2,88),(89,2,89),(90,2,90),(91,2,91),(92,2,92),(93,2,93),(87,2,163),(84,3,74),(86,3,98),(83,3,137),(85,3,163),(62,4,98),(65,4,137),(60,4,160),(61,4,161),(63,4,163),(64,4,164),(67,5,98),(66,5,137),(69,5,161),(68,5,163),(95,7,97),(96,7,98),(100,7,136),(101,7,137),(94,7,160),(99,7,161),(97,7,163),(98,7,164),(104,8,98),(103,8,137),(102,8,160),(106,8,161),(105,8,163),(109,9,98),(112,9,137),(107,9,160),(108,9,161),(110,9,163),(111,9,164);
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
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permissi_content_type_id_51277a81_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=166 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add bookmark',1,'add_bookmark'),(2,'Can change bookmark',1,'change_bookmark'),(3,'Can delete bookmark',1,'delete_bookmark'),(4,'Can add log entry',2,'add_logentry'),(5,'Can change log entry',2,'change_logentry'),(6,'Can delete log entry',2,'delete_logentry'),(7,'Can add permission',3,'add_permission'),(8,'Can change permission',3,'change_permission'),(9,'Can delete permission',3,'delete_permission'),(10,'Can add group',4,'add_group'),(11,'Can change group',4,'change_group'),(12,'Can delete group',4,'delete_group'),(13,'Can add content type',5,'add_contenttype'),(14,'Can change content type',5,'change_contenttype'),(15,'Can delete content type',5,'delete_contenttype'),(16,'Can add session',6,'add_session'),(17,'Can change session',6,'change_session'),(18,'Can delete session',6,'delete_session'),(19,'Can add tgt',7,'add_tgt'),(20,'Can change tgt',7,'change_tgt'),(21,'Can delete tgt',7,'delete_tgt'),(22,'Can add pgt iou',8,'add_pgtiou'),(23,'Can change pgt iou',8,'change_pgtiou'),(24,'Can delete pgt iou',8,'delete_pgtiou'),(25,'Can add Jenis Pemohon',9,'add_jenispemohon'),(26,'Can change Jenis Pemohon',9,'change_jenispemohon'),(27,'Can delete Jenis Pemohon',9,'delete_jenispemohon'),(28,'Can add Jenis Nomor Identitas',10,'add_jenisnomoridentitas'),(29,'Can change Jenis Nomor Identitas',10,'change_jenisnomoridentitas'),(30,'Can delete Jenis Nomor Identitas',10,'delete_jenisnomoridentitas'),(31,'Can add Setting',11,'add_settings'),(32,'Can change Setting',11,'change_settings'),(33,'Can delete Setting',11,'delete_settings'),(34,'Can add Negara',12,'add_negara'),(35,'Can change Negara',12,'change_negara'),(36,'Can delete Negara',12,'delete_negara'),(37,'Can add Provinsi',13,'add_provinsi'),(38,'Can change Provinsi',13,'change_provinsi'),(39,'Can delete Provinsi',13,'delete_provinsi'),(40,'Can add Kabupaten / Kota',14,'add_kabupaten'),(41,'Can change Kabupaten / Kota',14,'change_kabupaten'),(42,'Can delete Kabupaten / Kota',14,'delete_kabupaten'),(43,'Can add Kecamatan',15,'add_kecamatan'),(44,'Can change Kecamatan',15,'change_kecamatan'),(45,'Can delete Kecamatan',15,'delete_kecamatan'),(46,'Can add Desa / Kelurahan',16,'add_desa'),(47,'Can change Desa / Kelurahan',16,'change_desa'),(48,'Can delete Desa / Kelurahan',16,'delete_desa'),(49,'Can add Identitas Pribadi',17,'add_identitaspribadi'),(50,'Can change Identitas Pribadi',17,'change_identitaspribadi'),(51,'Can delete Identitas Pribadi',17,'delete_identitaspribadi'),(52,'Can add Akun',18,'add_account'),(53,'Can change Akun',18,'change_account'),(54,'Can delete Akun',18,'delete_account'),(55,'Can add Nomor Identitas Pengguna',19,'add_nomoridentitaspengguna'),(56,'Can change Nomor Identitas Pengguna',19,'change_nomoridentitaspengguna'),(57,'Can delete Nomor Identitas Pengguna',19,'delete_nomoridentitaspengguna'),(58,'Can add Jenis Unit Kerja',20,'add_jenisunitkerja'),(59,'Can change Jenis Unit Kerja',20,'change_jenisunitkerja'),(60,'Can delete Jenis Unit Kerja',20,'delete_jenisunitkerja'),(61,'Can add Unit Kerja',21,'add_unitkerja'),(62,'Can change Unit Kerja',21,'change_unitkerja'),(63,'Can delete Unit Kerja',21,'delete_unitkerja'),(64,'Can add Bagian / Bidang / Seksi (Struktural)',22,'add_bidangstruktural'),(65,'Can change Bagian / Bidang / Seksi (Struktural)',22,'change_bidangstruktural'),(66,'Can delete Bagian / Bidang / Seksi (Struktural)',22,'delete_bidangstruktural'),(67,'Can add Jabatan',23,'add_jabatan'),(68,'Can change Jabatan',23,'change_jabatan'),(69,'Can delete Jabatan',23,'delete_jabatan'),(70,'Can add Pegawai',24,'add_pegawai'),(71,'Can change Pegawai',24,'change_pegawai'),(72,'Can delete Pegawai',24,'delete_pegawai'),(73,'Can add Pemohon',25,'add_pemohon'),(74,'Can change Pemohon',25,'change_pemohon'),(75,'Can delete Pemohon',25,'delete_pemohon'),(76,'Can add Jenis Peraturan',26,'add_jenisperaturan'),(77,'Can change Jenis Peraturan',26,'change_jenisperaturan'),(78,'Can delete Jenis Peraturan',26,'delete_jenisperaturan'),(79,'Can add Dasar Hukum',27,'add_dasarhukum'),(80,'Can change Dasar Hukum',27,'change_dasarhukum'),(81,'Can delete Dasar Hukum',27,'delete_dasarhukum'),(82,'Can add Jenis Izin',28,'add_jenisizin'),(83,'Can change Jenis Izin',28,'change_jenisizin'),(84,'Can delete Jenis Izin',28,'delete_jenisizin'),(85,'Can add Kelompok Jenis Izin',29,'add_kelompokjenisizin'),(86,'Can change Kelompok Jenis Izin',29,'change_kelompokjenisizin'),(87,'Can delete Kelompok Jenis Izin',29,'delete_kelompokjenisizin'),(88,'Can add Syarat',30,'add_syarat'),(89,'Can change Syarat',30,'change_syarat'),(90,'Can delete Syarat',30,'delete_syarat'),(91,'Can add Prosedur',31,'add_prosedur'),(92,'Can change Prosedur',31,'change_prosedur'),(93,'Can delete Prosedur',31,'delete_prosedur'),(94,'Can add Jenis Permohonan Izin',32,'add_jenispermohonanizin'),(95,'Can change Jenis Permohonan Izin',32,'change_jenispermohonanizin'),(96,'Can delete Jenis Permohonan Izin',32,'delete_jenispermohonanizin'),(97,'Can add Pengajuan Izin',33,'add_pengajuanizin'),(98,'Can change Pengajuan Izin',33,'change_pengajuanizin'),(99,'Can delete Pengajuan Izin',33,'delete_pengajuanizin'),(106,'Can add atribut tambahan',36,'add_atributtambahan'),(107,'Can change atribut tambahan',36,'change_atributtambahan'),(108,'Can delete atribut tambahan',36,'delete_atributtambahan'),(109,'Can add KBLI',37,'add_kbli'),(110,'Can change KBLI',37,'change_kbli'),(111,'Can delete KBLI',37,'delete_kbli'),(112,'Can add Jenis Perusahaan',38,'add_jenisperusahaan'),(113,'Can change Jenis Perusahaan',38,'change_jenisperusahaan'),(114,'Can delete Jenis Perusahaan',38,'delete_jenisperusahaan'),(115,'Can add Kelembagaan',39,'add_kelembagaan'),(116,'Can change Kelembagaan',39,'change_kelembagaan'),(117,'Can delete Kelembagaan',39,'delete_kelembagaan'),(118,'Can add Produk Utama',40,'add_produkutama'),(119,'Can change Produk Utama',40,'change_produkutama'),(120,'Can delete Produk Utama',40,'delete_produkutama'),(121,'Can add Jenis Penanaman Modal',41,'add_jenispenanamanmodal'),(122,'Can change Jenis Penanaman Modal',41,'change_jenispenanamanmodal'),(123,'Can delete Jenis Penanaman Modal',41,'delete_jenispenanamanmodal'),(124,'Can add Jenis Badan Usaha',42,'add_jenisbadanusaha'),(125,'Can change Jenis Badan Usaha',42,'change_jenisbadanusaha'),(126,'Can delete Jenis Badan Usaha',42,'delete_jenisbadanusaha'),(130,'Can add Perusahaan',44,'add_perusahaan'),(131,'Can change Perusahaan',44,'change_perusahaan'),(132,'Can delete Perusahaan',44,'delete_perusahaan'),(136,'Can add Detil SIUP',46,'add_detilsiup'),(137,'Can change Detil SIUP',46,'change_detilsiup'),(138,'Can delete Detil SIUP',46,'delete_detilsiup'),(142,'Can add Kegiatan Usaha',48,'add_bentukkegiatanusaha'),(143,'Can change Kegiatan Usaha',48,'change_bentukkegiatanusaha'),(144,'Can delete Kegiatan Usaha',48,'delete_bentukkegiatanusaha'),(145,'Can add Berkas',49,'add_berkas'),(146,'Can change Berkas',49,'change_berkas'),(147,'Can delete Berkas',49,'delete_berkas'),(148,'Can add Jenis Legalitas',50,'add_jenislegalitas'),(149,'Can change Jenis Legalitas',50,'change_jenislegalitas'),(150,'Can delete Jenis Legalitas',50,'delete_jenislegalitas'),(151,'Can add Legalitas',51,'add_legalitas'),(152,'Can change Legalitas',51,'change_legalitas'),(153,'Can delete Legalitas',51,'delete_legalitas'),(154,'Can add Jenis Reklame',52,'add_jenisreklame'),(155,'Can change Jenis Reklame',52,'change_jenisreklame'),(156,'Can delete Jenis Reklame',52,'delete_jenisreklame'),(157,'Can add detil reklame',53,'add_detilreklame'),(158,'Can change detil reklame',53,'change_detilreklame'),(159,'Can delete detil reklame',53,'delete_detilreklame'),(160,'Can add sk izin',54,'add_skizin'),(161,'Can change sk izin',54,'change_skizin'),(162,'Can delete sk izin',54,'delete_skizin'),(163,'Can add riwayat',55,'add_riwayat'),(164,'Can change riwayat',55,'change_riwayat'),(165,'Can delete riwayat',55,'delete_riwayat');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cas_pgtiou`
--

DROP TABLE IF EXISTS `cas_pgtiou`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cas_pgtiou` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `pgtIou` varchar(255) NOT NULL,
  `tgt` varchar(255) NOT NULL,
  `created` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `pgtIou` (`pgtIou`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cas_pgtiou`
--

LOCK TABLES `cas_pgtiou` WRITE;
/*!40000 ALTER TABLE `cas_pgtiou` DISABLE KEYS */;
/*!40000 ALTER TABLE `cas_pgtiou` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cas_tgt`
--

DROP TABLE IF EXISTS `cas_tgt`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cas_tgt` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `tgt` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cas_tgt`
--

LOCK TABLES `cas_tgt` WRITE;
/*!40000 ALTER TABLE `cas_tgt` DISABLE KEYS */;
/*!40000 ALTER TABLE `cas_tgt` ENABLE KEYS */;
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
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin__content_type_id_5151027a_fk_django_content_type_id` (`content_type_id`),
  KEY `djan_user_id_1c5f563_fk_accounts_account_identitaspribadi_ptr_id` (`user_id`),
  CONSTRAINT `django_admin__content_type_id_5151027a_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `djan_user_id_1c5f563_fk_accounts_account_identitaspribadi_ptr_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_account` (`identitaspribadi_ptr_id`)
) ENGINE=InnoDB AUTO_INCREMENT=392 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2016-08-24 02:07:25','1','Peraturan Bupati',1,'',26,1),(2,'2016-08-24 02:07:51','1','09',1,'',27,1),(3,'2016-08-24 02:07:57','1','SIUP',1,'',28,1),(4,'2016-08-24 02:09:26','1','SIUP',1,'',29,1),(5,'2016-08-24 02:09:46','1','SIUP',2,'standart_waktu diubah',29,1),(6,'2016-08-24 04:48:34','2','IMB',1,'',28,1),(7,'2016-08-24 04:49:59','2','Badan Hukum',1,'',29,1),(8,'2016-08-24 04:50:14','3','Badan Usaha',1,'',29,1),(9,'2016-08-25 00:58:17','1','BARU',1,'',32,1),(10,'2016-08-25 01:39:04','1','Baru/Pendirian',2,'jenis_permohonan_izin diubah',32,1),(11,'2016-08-25 01:39:25','2','Perpanjangan/Pebaharuan',1,'',32,1),(12,'2016-08-25 01:39:49','3','Perubahan',1,'',32,1),(13,'2016-08-25 01:40:04','4','Baru/Pendirian',1,'',32,1),(14,'2016-08-25 01:42:51','1','1. KTP',1,'',10,1),(15,'2016-08-25 04:34:56','1','Perorangan',1,'',9,1),(16,'2016-08-25 04:37:03','1','Indonesia',1,'',12,1),(17,'2016-08-25 04:37:18','1','Jawa Timur',1,'',13,1),(18,'2016-08-25 04:37:35','1','Kediri',1,'',14,1),(19,'2016-08-25 04:37:56','1','Kota',1,'',15,1),(20,'2016-08-25 04:38:06','1','Kediri',2,'nama_kecamatan diubah',15,1),(21,'2016-08-25 04:38:23','1','Dandangan',1,'',16,1),(22,'2016-08-29 01:19:07','1','Operator',1,'',4,1),(23,'2016-08-29 01:23:26','1','BPM2TSP',1,'',21,1),(24,'2016-08-29 01:33:44','1','Pemilik',2,'jenis_pemohon diubah',9,1),(25,'2016-08-29 01:33:55','2','Penanggung Jawab',1,'',9,1),(26,'2016-08-29 01:34:00','3','Ketua',1,'',9,1),(27,'2016-08-29 01:34:05','4','Direktur',1,'',9,1),(28,'2016-08-29 01:34:11','5','Komisaris',1,'',9,1),(29,'2016-08-29 03:12:29','2','Ngasem',1,'',15,1),(30,'2016-08-29 03:23:09','4','Baru/Pendirian',3,'',32,1),(31,'2016-08-29 03:26:29','1','SIUP',2,'kode diubah',28,1),(32,'2016-08-29 04:28:26','2','2. PASPOR',1,'',10,1),(33,'2016-08-29 05:15:00','15','TAUFAN BUDIMAN',1,'Operator menambahkan IdentitasPribadi baru dari formulir pengajuan baru.',25,1),(34,'2016-08-29 05:16:58','4','TAUFAN BUDIMAN',3,'',25,1),(35,'2016-08-29 05:16:58','15','TAUFAN BUDIMAN',3,'',25,1),(36,'2016-08-29 05:17:04','17','TAUFAN BUDIMAN',1,'Operator menambahkan IdentitasPribadi baru dari formulir pengajuan baru.',25,1),(37,'2016-08-29 05:18:22','17','TAUFAN BUDIMAN',3,'',25,1),(38,'2016-08-29 05:18:27','19','TAUFAN BUDIMAN',1,'Operator menambahkan IdentitasPribadi baru dari formulir pengajuan baru.',25,1),(39,'2016-08-29 05:18:27','1','3506221804900002',1,'Operator menambahkan Nomor Identitas baru dari formulir pengajuan baru.',19,1),(40,'2016-08-29 05:20:48','19','TAUFAN BUDIMAN',3,'',25,1),(41,'2016-08-29 05:21:27','20','TAUFAN BUDIMAN',1,'Operator menambahkan IdentitasPribadi baru dari formulir pengajuan baru.',25,1),(42,'2016-08-29 05:21:27','2','3506221804900002',1,'Operator menambahkan Nomor Identitas baru dari formulir pengajuan baru.',19,1),(43,'2016-08-29 05:22:15','20','TAUFAN BUDIMAN',3,'',25,1),(44,'2016-08-29 05:22:20','21','TAUFAN BUDIMAN',1,'Operator menambahkan IdentitasPribadi baru dari formulir pengajuan baru.',25,1),(45,'2016-08-29 05:22:20','3','3506221804900002',1,'Operator menambahkan Nomor Identitas baru dari formulir pengajuan baru.',19,1),(46,'2016-08-29 06:54:32','1','SIUP - Baru/Pendirian',2,'jenis_permohonan diubah',33,1),(47,'2016-08-31 03:28:29','2','IMB',2,'kode diubah',28,1),(48,'2016-08-31 03:46:16','1','SURAT IZIN USAHA PERDAGANGAN (SIUP)',2,'nama_izin diubah',28,1),(49,'2016-08-31 03:46:28','2','IZIN MENDIRIKAN BANGUNAN (IMB)',2,'nama_izin diubah',28,1),(50,'2016-08-31 03:47:00','1','SIUP PERMOHONAN BARU Perusahaan berbentuk Perseroan Terbatas (PT)',2,'kelompok_jenis_izin diubah',29,1),(51,'2016-08-31 03:47:28','2','Izin Mendirikan Bangunan (IMB) Perumahan',2,'kelompok_jenis_izin diubah',29,1),(52,'2016-08-31 03:47:40','3','Izin Mendirikan Bangunan (IMB) Umum',2,'kelompok_jenis_izin diubah',29,1),(53,'2016-08-31 03:48:00','4','Izin Mendirikan Bangunan (IMB) Bupati',1,'',29,1),(54,'2016-09-01 03:35:22','22','ASDFASFASDF',3,'',25,1),(55,'2016-09-01 07:33:45','24','TESTING',1,'Operator menambahkan IdentitasPribadi baru dari formulir pengajuan baru.',25,1),(56,'2016-09-01 07:33:45','4','21345',1,'Operator menambahkan Nomor Identitas baru dari formulir pengajuan baru.',19,1),(57,'2016-09-03 03:08:46','24','TESTING',3,'',25,1),(58,'2016-09-05 02:51:59','2','ASDFASF',3,'',25,1),(59,'2016-09-05 02:58:38','4','TESTING',1,'',25,1),(60,'2016-09-05 02:59:14','4','TESTING',3,'',25,1),(61,'2016-09-05 03:32:21','21','SIUP PERMOHONAN BARU Perusahaan berbentuk Perseroan Terbatas (PT) - Baru/Pendirian',1,'Operator melakukan pendaftaran pengajuan baru dengan nama pemohon .',33,1),(62,'2016-09-05 03:34:15','23','SIUP PERMOHONAN BARU Perusahaan berbentuk Perseroan Terbatas (PT) - Baru/Pendirian',1,'Operator melakukan pendaftaran pengajuan baru dengan nama pemohon .',33,1),(63,'2016-09-05 03:42:37','25','SIUP PERMOHONAN BARU Perusahaan berbentuk Perseroan Terbatas (PT) - Baru/Pendirian',1,'Operator melakukan pendaftaran pengajuan baru dengan nama pemohon .',33,1),(64,'2016-09-05 03:46:15','27','SIUP PERMOHONAN BARU Perusahaan berbentuk Perseroan Terbatas (PT) - Baru/Pendirian',1,'Operator melakukan pendaftaran pengajuan baru dengan nama pemohon .',33,1),(65,'2016-09-05 03:46:55','29','SIUP PERMOHONAN BARU Perusahaan berbentuk Perseroan Terbatas (PT) - Baru/Pendirian',1,'Operator melakukan pendaftaran pengajuan baru dengan nama pemohon .',33,1),(66,'2016-09-05 03:47:49','5','TAUFAN',2,'negara dan desa diubah Nomor Identitas Pengguna \"232\" ditambahkan.',25,1),(67,'2016-09-05 03:51:41','7','452342444444',1,'Operator menambahkan Nomor Identitas KTP baru dari formulir pengajuan baru.',19,1),(68,'2016-09-05 03:51:41','32','SIUP PERMOHONAN BARU Perusahaan berbentuk Perseroan Terbatas (PT) - Baru/Pendirian',1,'Operator melakukan pendaftaran pengajuan baru dengan nama pemohon .',33,1),(69,'2016-09-05 03:52:59','8','452342444444',1,'Operator menambahkan Nomor Identitas KTP baru dari formulir pengajuan baru.',19,1),(70,'2016-09-05 03:52:59','34','SIUP PERMOHONAN BARU Perusahaan berbentuk Perseroan Terbatas (PT) - Baru/Pendirian',1,'Operator melakukan pendaftaran pengajuan baru dengan nama pemohon .',33,1),(71,'2016-09-05 04:12:27','38','TAUFAN',3,'',25,1),(72,'2016-09-05 04:19:52','39','FIREFOX',2,'nama_lengkap, negara dan desa diubah',25,1),(73,'2016-09-05 06:40:37','57','SIUP PERMOHONAN BARU Perusahaan berbentuk Perseroan Terbatas (PT) - Baru/Pendirian',3,'',33,1),(74,'2016-09-05 06:40:37','55','SIUP PERMOHONAN BARU Perusahaan berbentuk Perseroan Terbatas (PT) - Baru/Pendirian',3,'',33,1),(75,'2016-09-05 06:40:37','53','SIUP PERMOHONAN BARU Perusahaan berbentuk Perseroan Terbatas (PT) - Baru/Pendirian',3,'',33,1),(76,'2016-09-05 06:40:37','51','SIUP PERMOHONAN BARU Perusahaan berbentuk Perseroan Terbatas (PT) - Baru/Pendirian',3,'',33,1),(77,'2016-09-05 06:40:37','49','SIUP PERMOHONAN BARU Perusahaan berbentuk Perseroan Terbatas (PT) - Baru/Pendirian',3,'',33,1),(78,'2016-09-05 06:40:38','47','SIUP PERMOHONAN BARU Perusahaan berbentuk Perseroan Terbatas (PT) - Baru/Pendirian',3,'',33,1),(79,'2016-09-05 06:40:38','45','SIUP PERMOHONAN BARU Perusahaan berbentuk Perseroan Terbatas (PT) - Baru/Pendirian',3,'',33,1),(80,'2016-09-05 06:40:38','43','SIUP PERMOHONAN BARU Perusahaan berbentuk Perseroan Terbatas (PT) - Baru/Pendirian',3,'',33,1),(81,'2016-09-05 06:40:38','40','SIUP PERMOHONAN BARU Perusahaan berbentuk Perseroan Terbatas (PT) - Baru/Pendirian',3,'',33,1),(82,'2016-09-05 06:40:38','34','SIUP PERMOHONAN BARU Perusahaan berbentuk Perseroan Terbatas (PT) - Baru/Pendirian',3,'',33,1),(83,'2016-09-05 06:40:38','32','SIUP PERMOHONAN BARU Perusahaan berbentuk Perseroan Terbatas (PT) - Baru/Pendirian',3,'',33,1),(84,'2016-09-05 06:40:38','29','SIUP PERMOHONAN BARU Perusahaan berbentuk Perseroan Terbatas (PT) - Baru/Pendirian',3,'',33,1),(85,'2016-09-05 06:40:38','27','SIUP PERMOHONAN BARU Perusahaan berbentuk Perseroan Terbatas (PT) - Baru/Pendirian',3,'',33,1),(86,'2016-09-05 06:40:38','25','SIUP PERMOHONAN BARU Perusahaan berbentuk Perseroan Terbatas (PT) - Baru/Pendirian',3,'',33,1),(87,'2016-09-05 06:40:38','23','SIUP PERMOHONAN BARU Perusahaan berbentuk Perseroan Terbatas (PT) - Baru/Pendirian',3,'',33,1),(88,'2016-09-05 06:40:38','21','SIUP PERMOHONAN BARU Perusahaan berbentuk Perseroan Terbatas (PT) - Baru/Pendirian',3,'',33,1),(89,'2016-09-05 06:40:38','19','SIUP PERMOHONAN BARU Perusahaan berbentuk Perseroan Terbatas (PT) - Baru/Pendirian',3,'',33,1),(90,'2016-09-05 06:40:38','17','SIUP PERMOHONAN BARU Perusahaan berbentuk Perseroan Terbatas (PT) - Baru/Pendirian',3,'',33,1),(91,'2016-09-05 06:40:39','15','SIUP PERMOHONAN BARU Perusahaan berbentuk Perseroan Terbatas (PT) - Baru/Pendirian',3,'',33,1),(92,'2016-09-05 06:40:39','13','SIUP PERMOHONAN BARU Perusahaan berbentuk Perseroan Terbatas (PT) - Baru/Pendirian',3,'',33,1),(93,'2016-09-05 07:24:58','62','OPERATOR - operator',1,'',18,1),(94,'2016-09-05 07:25:33','62','OPERATOR - operator',2,'alamat, negara, desa, groups dan is_admin diubah',18,1),(95,'2016-09-05 07:28:17','1','Operator',2,'permissions diubah',4,1),(96,'2016-09-06 02:20:07','4','Pemindahan Tempat Usaha',1,'',32,1),(97,'2016-09-06 02:20:24','5','Perluasan',1,'',32,1),(98,'2016-09-06 02:20:46','6','Penggantian Mesin (Rehabilitasi/ Up-Grading)',1,'',32,1),(99,'2016-09-06 02:21:03','7','Pemindahan Hak Izin Usaha',1,'',32,1),(100,'2016-09-06 02:21:19','8','Pemindahan Hak Kepemilikan',1,'',32,1),(101,'2016-09-06 03:00:09','3','3. NIP',1,'',10,1),(102,'2016-09-06 03:02:41','2','inputan',1,'',4,1),(103,'2016-09-06 03:02:59','73','INPUTAN - inputan',1,'',18,1),(104,'2016-09-06 03:03:25','73','INPUTAN - inputan',2,'alamat, negara, desa, groups, status dan is_admin diubah',18,1),(105,'2016-09-06 03:12:54','1','Baru/Pendirian',2,'jenis_izin diubah',32,1),(106,'2016-09-06 03:13:04','2','Perpanjangan/Pebaharuan',2,'jenis_izin diubah',32,1),(107,'2016-09-06 03:13:14','3','Perubahan',2,'jenis_izin diubah',32,1),(108,'2016-09-06 04:16:27','2','Inputan',2,'name diubah',4,1),(109,'2016-09-06 06:47:42','77','SIUP PERMOHONAN BARU Perusahaan berbentuk Perseroan Terbatas (PT) - Perpanjangan/Pebaharuan',2,'created_by diubah',33,62),(110,'2016-09-07 04:56:31','1','Operator',2,'permissions diubah',4,1),(111,'2016-09-07 05:18:50','1','7',1,'',37,1),(112,'2016-09-07 05:20:25','1','Jasa Konstruksi',1,'',48,1),(113,'2016-09-07 05:23:34','1','Mikro',2,'kegiatan_usaha diubah',48,1),(114,'2016-09-07 05:23:39','2','Makro',1,'',48,1),(115,'2016-09-07 05:24:21','1',' PMA ',1,'',41,1),(116,'2016-09-07 05:24:42','2','PMDN',1,'',41,1),(117,'2016-09-07 05:25:52','1','Perseroan Terbatas (PT)',1,'',42,1),(118,'2016-09-07 05:25:58','2','PERSEKUTUAN KOMANDITER (CV)',1,'',42,1),(119,'2016-09-07 05:26:06','3','Firma',1,'',42,1),(120,'2016-09-07 05:26:11','4','PERUSAHAAN PERORANGAN (PO)',1,'',42,1),(121,'2016-09-07 05:26:16','5','Koperasi',1,'',42,1),(122,'2016-09-07 05:26:21','6','BENTUK USAHA LAINNYA (BUL)',1,'',42,1),(123,'2016-09-07 05:31:11','1','Mikro',1,'',39,1),(124,'2016-09-07 05:31:16','2','Kecil',1,'',39,1),(125,'2016-09-07 05:31:22','3','Menengah',1,'',39,1),(126,'2016-09-07 05:31:26','4','Besar',1,'',39,1),(127,'2016-09-08 01:04:00','2','IZIN GANGGUAN (HO)',2,'kode diubah',28,1),(128,'2016-09-08 01:06:18','7','TANDA DAFTAR PERUSAHAAN (TDP)',2,'kode diubah',28,1),(129,'2016-09-08 01:56:11','83','SIUP PERMOHONAN BARU Perusahaan berbentuk Perseroan Terbatas (PT) - Baru/Pendirian',3,'',33,1),(130,'2016-09-08 01:56:11','81','SIUP PERMOHONAN BARU Perusahaan berbentuk Perseroan Terbatas (PT) - Baru/Pendirian',3,'',33,1),(131,'2016-09-08 01:56:11','79','SIUP PERMOHONAN BARU Perusahaan berbentuk Perseroan Terbatas (PT) - Baru/Pendirian',3,'',33,1),(132,'2016-09-08 01:56:11','77','SIUP PERMOHONAN BARU Perusahaan berbentuk Perseroan Terbatas (PT) - Perpanjangan/Pebaharuan',3,'',33,1),(133,'2016-09-08 01:56:11','75','SIUP PERMOHONAN BARU Perusahaan berbentuk Perseroan Terbatas (PT) - Baru/Pendirian',3,'',33,1),(134,'2016-09-08 01:56:11','72','Izin Mendirikan Bangunan (IMB) Bupati - Perpanjangan/Pebaharuan',3,'',33,1),(135,'2016-09-08 01:56:11','70','Izin Mendirikan Bangunan (IMB) Bupati - Perpanjangan/Pebaharuan',3,'',33,1),(136,'2016-09-08 01:56:11','68','Izin Mendirikan Bangunan (IMB) Bupati - Perpanjangan/Pebaharuan',3,'',33,1),(137,'2016-09-08 01:56:11','66','Izin Mendirikan Bangunan (IMB) Bupati - Perpanjangan/Pebaharuan',3,'',33,1),(138,'2016-09-08 01:56:11','64','Izin Mendirikan Bangunan (IMB) Bupati - Perpanjangan/Pebaharuan',3,'',33,1),(139,'2016-09-08 01:56:12','59','Izin Mendirikan Bangunan (IMB) Bupati - Perpanjangan/Pebaharuan',3,'',33,1),(140,'2016-09-08 03:07:34','1','Operator',2,'permissions diubah',4,1),(141,'2016-09-09 02:02:13','1','Akta Pendirian',1,'',50,1),(142,'2016-09-09 02:02:24','2','Akta perubahan terakhir',1,'',50,1),(143,'2016-09-09 02:02:30','3','Pengesahan Menteri Hukum dan HAM',1,'',50,1),(144,'2016-09-09 02:02:35','4','Persetujuan Menteri Hukum dan HAM Atas Perubahan Anggaran ',1,'',50,1),(145,'2016-09-09 02:02:40','5','Dasar',1,'',50,1),(146,'2016-09-09 02:03:33','6','Penerimaan Laporan Perubahan Anggaran Dasar',1,'',50,1),(147,'2016-09-09 02:03:41','7','Penerimaan Pemberitahuan Perubahan Direksi/ Komisaris',1,'',50,1),(148,'2016-09-09 02:03:53','8','Pengesahan Menteri Koperasi dan UKM',1,'',50,1),(149,'2016-09-09 02:04:02','9','Persetujuan Menteri Koperasi dan UKM atas Akta Perubahan ',1,'',50,1),(150,'2016-09-09 02:04:09','10','Anggaran Dasar',1,'',50,1),(151,'2016-09-10 01:02:25','5','TAUFAN',3,'',25,1),(152,'2016-09-10 01:02:25','39','FIREFOX',3,'',25,1),(153,'2016-09-10 01:02:25','58','APPLICATIONS',3,'',25,1),(154,'2016-09-10 01:02:25','60','MONSEP',3,'',25,1),(155,'2016-09-10 01:02:25','63','SEPTEMBER',3,'',25,1),(156,'2016-09-10 01:02:25','74','BYON',3,'',25,1),(157,'2016-09-10 01:02:25','76','CORE',3,'',25,1),(158,'2016-09-10 01:02:25','78','ACER',3,'',25,1),(159,'2016-09-10 01:02:25','80','HALOHA',3,'',25,1),(160,'2016-09-10 01:02:25','88','JATMIKO',3,'',25,1),(161,'2016-09-10 01:02:25','90','RANGKAP TIGA',3,'',25,1),(162,'2016-09-10 01:02:25','92','RAZOR',3,'',25,1),(163,'2016-09-10 01:14:57','94','TAUFAN BUDIMAN',3,'',25,1),(164,'2016-09-10 01:16:19','87','CV. Pantang Mundur',3,'',44,1),(165,'2016-09-10 01:16:19','96','MAJU MAKMUR',3,'',44,1),(166,'2016-09-10 01:17:17','1','Komputer',1,'',40,1),(167,'2016-09-10 01:28:57','99','MAKMUR',3,'',44,1),(168,'2016-09-20 07:17:31','106','HALO',3,'',49,1),(169,'2016-09-22 04:42:00','117','Pengesahan Menteri Hukum dan HAM',3,'',51,1),(170,'2016-09-22 04:42:00','118','Pengesahan Menteri Hukum dan HAM',3,'',51,1),(171,'2016-09-22 04:42:00','119','Akta perubahan terakhir',3,'',51,1),(172,'2016-09-22 04:42:01','120','Pengesahan Menteri Hukum dan HAM',3,'',51,1),(173,'2016-09-22 04:42:01','121','Pengesahan Menteri Hukum dan HAM',3,'',51,1),(174,'2016-09-22 04:42:01','122','Akta perubahan terakhir',3,'',51,1),(175,'2016-09-26 19:38:07','2','4',1,'',37,1),(176,'2016-09-26 19:38:21','2','hhhhhhhh',1,'',40,1),(177,'2016-09-26 19:38:34','3','sego pecel',1,'',40,1),(178,'2016-09-26 19:38:53','4','sego kuning',1,'',40,1),(179,'2016-09-26 21:21:51','250','Detil SIUP PERMOHONAN BARU Perusahaan berbentuk Perseroan Terbatas (PT) - Baru/Pendirian',2,'kbli diubah',46,1),(180,'2016-09-28 07:42:30','266','Detil SIUP PERMOHONAN BARU Perusahaan berbentuk Perseroan Terbatas (PT) - Baru/Pendirian',2,'no_izin, perusahaan dan produk_utama diubah',46,1),(181,'2016-09-29 02:12:58','1','pelayanan (BPMP2TSP)',1,'',22,1),(182,'2016-09-29 02:13:52','2','pelayanan (BPMP2TSP)',1,'',22,1),(183,'2016-09-29 02:27:29','1','Kepala Dinas',1,'',23,1),(184,'2016-09-29 02:27:42','268','INDRA TARUNA',1,'',24,1),(185,'2016-09-29 02:28:18','2','Sekretaris',1,'',23,1),(186,'2016-09-29 02:29:28','269','ANDES ERWANTO',1,'',24,1),(187,'2016-09-29 02:30:21','3','Kasubag',1,'',23,1),(188,'2016-09-29 02:30:33','270','NOEGROHO ADI',1,'',24,1),(189,'2016-09-29 02:31:23','271','INDIYAH SETIANI',1,'',24,1),(190,'2016-09-29 02:32:57','272','DAMAS DANUR RENDRA',1,'',24,1),(191,'2016-09-29 02:33:32','4','Kabid',1,'',23,1),(192,'2016-09-29 02:33:43','273','AL INDAH',1,'',24,1),(193,'2016-09-29 02:34:25','274','AGUSTIAWAN',1,'',24,1),(194,'2016-09-29 02:35:36','275','DEVIN MARSFIAN S',1,'',24,1),(195,'2016-09-29 02:36:31','5','Kasubid',1,'',23,1),(196,'2016-09-29 02:36:41','276','NANIK SRI HANDAYATININGSIH',1,'',24,1),(197,'2016-09-29 02:38:02','277','A. DENNY SETYAWAN',1,'',24,1),(198,'2016-09-29 02:38:46','278','MERY PURWANTY',1,'',24,1),(199,'2016-09-29 02:39:22','6','staf',1,'',23,1),(200,'2016-09-29 02:39:38','279','MARUF',1,'',24,1),(201,'2016-09-29 02:40:22','6','Staf',2,'nama_jabatan diubah',23,1),(202,'2016-09-29 02:40:49','280','JOENIA DEWI KOESTATI',1,'',24,1),(203,'2016-09-29 02:41:38','281','EVA DAYANTI LW',1,'',24,1),(204,'2016-09-29 02:42:46','282','DYAH KIRONOSARI',1,'',24,1),(205,'2016-09-29 02:44:21','283','ZAKY ZAMRONI',1,'',24,1),(206,'2016-09-29 02:44:57','284','SRI WINARTI',1,'',24,1),(207,'2016-09-29 02:45:33','285','ERNA BUDI HERTANTI',1,'',24,1),(208,'2016-09-29 02:46:02','286','BUDI HERTANTO',1,'',24,1),(209,'2016-09-29 02:46:34','287','ALI MASHURI',1,'',24,1),(210,'2016-09-29 02:47:17','288','ENI SETYORINI',1,'',24,1),(211,'2016-09-29 02:48:12','289','RIGEN PRAMAHERTI',1,'',24,1),(212,'2016-09-29 02:49:15','290','LAGIONO',1,'',24,1),(213,'2016-09-29 02:49:48','291','DWI AGUS ROCHMADI',1,'',24,1),(214,'2016-09-29 02:50:26','292','ANDIKA N. YUDHIN',1,'',24,1),(215,'2016-09-29 02:51:03','293','BAGUS S. JATMIKO',1,'',24,1),(216,'2016-09-29 02:52:19','294','HENDRA D. KURNIANTO',1,'',24,1),(217,'2016-09-29 02:52:58','295','DZIKIR S. ATMAJA',1,'',24,1),(218,'2016-09-29 02:53:28','296','HENRI RISDIANTO',1,'',24,1),(219,'2016-09-29 02:54:04','297','NANIK HARIYANI',1,'',24,1),(220,'2016-09-29 02:54:40','298','ANDI SETIAWAN',1,'',24,1),(221,'2016-09-29 02:55:14','299','PIPIT NOVIE MA',1,'',24,1),(222,'2016-09-29 02:55:48','300','BUDIYONO',1,'',24,1),(223,'2016-09-29 02:56:39','301','YUDHA RUKMANA KURNIAWATI',1,'',24,1),(224,'2016-09-29 02:57:12','302','AGUNG ARIADI',1,'',24,1),(225,'2016-09-29 02:57:52','303','SAIFUL ANAM',1,'',24,1),(226,'2016-09-29 02:58:33','304','AMALIA RIZKY',1,'',24,1),(227,'2016-09-29 02:59:31','4','4. NIK',1,'',10,1),(228,'2016-09-29 02:59:34','305','CHRISAN NUSANTARA',1,'',24,1),(229,'2016-09-29 04:50:40','266','Detil SIUP PERMOHONAN BARU Perusahaan berbentuk Perseroan Terbatas (PT) - Baru/Pendirian',2,'nama_kuasa, no_identitas_kuasa, telephone_kuasa, berkas_tambahan, berkas_foto, berkas_npwp_pemohon, berkas_npwp_perusahaan, legalitas, kbli, kelembagaan, bentuk_kegiatan_usaha, jenis_penanaman_modal, kekayaan_bersih, total_nilai_saham, presentase_saham_nasional dan presentase_saham_asing diubah',46,1),(230,'2016-09-29 05:27:36','3','Kabid',1,'',4,1),(231,'2016-09-29 05:30:17','273','AL INDAH',2,'alamat, negara, desa dan groups diubah',24,1),(232,'2016-09-29 05:31:25','274','AGUSTIAWAN',2,'alamat, negara, desa dan groups diubah',24,1),(233,'2016-09-29 05:32:30','275','DEVIN MARSFIAN S',2,'alamat, negara, desa dan groups diubah',24,1),(234,'2016-09-29 06:01:58','3','Kabid',2,'permissions diubah',4,1),(235,'2016-09-29 07:04:07','266','Detil SIUP PERMOHONAN BARU Perusahaan berbentuk Perseroan Terbatas (PT) - Baru/Pendirian',2,'status diubah',46,62),(236,'2016-09-29 07:12:28','266','Detil SIUP PERMOHONAN BARU Perusahaan berbentuk Perseroan Terbatas (PT) - Baru/Pendirian',2,'status diubah',46,62),(237,'2016-09-29 07:18:03','266','Detil SIUP PERMOHONAN BARU Perusahaan berbentuk Perseroan Terbatas (PT) - Baru/Pendirian',2,'status diubah',46,62),(238,'2016-09-29 07:44:16','266','Detil SIUP PERMOHONAN BARU Perusahaan berbentuk Perseroan Terbatas (PT) - Baru/Pendirian',2,'status diubah',46,1),(239,'2016-09-30 01:46:11','3','Kabid',2,'permissions diubah',4,1),(240,'2016-09-30 02:02:06','266','Detil SIUP PERMOHONAN BARU Perusahaan berbentuk Perseroan Terbatas (PT) - Baru/Pendirian',2,'status diubah',46,273),(241,'2016-09-30 02:07:10','266','SIUP PERMOHONAN BARU Perusahaan berbentuk Perseroan Terbatas (PT) - Baru/Pendirian',3,'',33,1),(242,'2016-09-30 03:38:13','250','Detil SIUP PERMOHONAN BARU Perusahaan berbentuk Perseroan Terbatas (PT) - Baru/Pendirian',2,'berkas_tambahan, perusahaan, berkas_foto, berkas_npwp_pemohon, berkas_npwp_perusahaan dan legalitas diubah',46,273),(243,'2016-09-30 04:35:44','250','Detil SIUP PERMOHONAN BARU Perusahaan berbentuk Perseroan Terbatas (PT) - Baru/Pendirian',2,'legalitas diubah',46,273),(244,'2016-10-01 02:41:44','3','Kabid',2,'permissions diubah',4,1),(245,'2016-10-03 01:43:00','4','Pembuat Surat',1,'',4,1),(246,'2016-10-03 01:44:26','281','EVA DAYANTI LW',2,'alamat, negara, desa dan groups diubah',24,1),(247,'2016-10-03 01:46:11','4','Pembuat Surat',2,'permissions diubah',4,1),(248,'2016-10-03 02:46:53','4','Pembuat Surat',2,'permissions diubah',4,1),(249,'2016-10-03 03:39:44','343','6',3,'',55,1),(250,'2016-10-03 03:39:44','341','6',3,'',55,1),(251,'2016-10-03 03:39:44','338','6',3,'',55,1),(252,'2016-10-03 03:39:44','336','6',3,'',55,1),(253,'2016-10-03 03:39:44','334','6',3,'',55,1),(254,'2016-10-03 03:39:44','332','6',3,'',55,1),(255,'2016-10-03 03:39:44','330','6',3,'',55,1),(256,'2016-10-03 03:39:44','328','6',3,'',55,1),(257,'2016-10-03 03:39:44','326','6',3,'',55,1),(258,'2016-10-03 03:39:44','324','6',3,'',55,1),(259,'2016-10-03 03:40:30','342','6',3,'',54,1),(260,'2016-10-03 03:40:30','340','6',3,'',54,1),(261,'2016-10-03 03:40:30','339','6',3,'',54,1),(262,'2016-10-03 03:40:30','337','6',3,'',54,1),(263,'2016-10-03 03:40:30','335','6',3,'',54,1),(264,'2016-10-03 03:40:30','333','6',3,'',54,1),(265,'2016-10-03 03:40:30','331','6',3,'',54,1),(266,'2016-10-03 03:40:31','329','6',3,'',54,1),(267,'2016-10-03 03:40:31','327','6',3,'',54,1),(268,'2016-10-03 03:40:31','325','6',3,'',54,1),(269,'2016-10-03 03:40:31','323','6',3,'',54,1),(270,'2016-10-03 03:40:31','321','6',3,'',54,1),(271,'2016-10-03 03:40:31','320','6',3,'',54,1),(272,'2016-10-03 03:40:31','319','6',3,'',54,1),(273,'2016-10-03 03:40:31','317','6',3,'',54,1),(274,'2016-10-03 03:40:31','316','6',3,'',54,1),(275,'2016-10-03 03:40:31','315','6',3,'',54,1),(276,'2016-10-03 03:40:31','313','6',3,'',54,1),(277,'2016-10-03 03:40:31','312','6',3,'',54,1),(278,'2016-10-03 03:40:31','311','6',3,'',54,1),(279,'2016-10-03 03:40:32','309','6',3,'',54,1),(280,'2016-10-03 03:40:32','307','6',3,'',54,1),(281,'2016-10-03 03:40:32','306','6',3,'',54,1),(282,'2016-10-03 03:53:11','345','6',3,'',55,1),(283,'2016-10-03 03:53:16','344','6',3,'',54,1),(284,'2016-10-03 04:46:40','254','Detil SIUP PERMOHONAN BARU Perusahaan berbentuk Perseroan Terbatas (PT) - Baru/Pendirian',2,'pemohon, no_izin, perusahaan dan produk_utama diubah',46,281),(285,'2016-10-03 08:10:14','5','Kadin',1,'',4,1),(286,'2016-10-03 08:11:19','268','INDRA TARUNA',2,'alamat, negara, desa dan groups diubah',24,1),(287,'2016-10-03 08:23:29','347','6',3,'',55,1),(288,'2016-10-03 10:33:27','351','Detil SIUP PERMOHONAN BARU Perusahaan berbentuk Perseroan Terbatas (PT) - Baru/Pendirian',2,'status dan no_izin diubah',46,1),(289,'2016-10-03 10:51:00','1','Operator',2,'permissions diubah',4,1),(290,'2016-10-03 10:51:39','3','Kabid',2,'permissions diubah',4,1),(291,'2016-10-03 10:52:54','2','Inputan',2,'permissions diubah',4,1),(292,'2016-10-03 11:15:09','6','Kasir',1,'',4,1),(293,'2016-10-03 11:17:52','351','Detil SIUP PERMOHONAN BARU Perusahaan berbentuk Perseroan Terbatas (PT) - Baru/Pendirian',2,'status diubah',46,273),(294,'2016-10-03 11:21:39','351','Detil SIUP PERMOHONAN BARU Perusahaan berbentuk Perseroan Terbatas (PT) - Baru/Pendirian',2,'status diubah',46,273),(295,'2016-10-03 11:46:22','351','Detil SIUP PERMOHONAN BARU Perusahaan berbentuk Perseroan Terbatas (PT) - Baru/Pendirian',2,'perusahaan diubah',46,273),(296,'2016-10-03 15:32:56','366','SIUP PERMOHONAN BARU Perusahaan berbentuk Perseroan Terbatas (PT) - Baru/Pendirian',3,'',33,1),(297,'2016-10-03 15:32:56','364','SIUP PERMOHONAN BARU Perusahaan berbentuk Perseroan Terbatas (PT) - Baru/Pendirian',3,'',33,1),(298,'2016-10-03 15:33:55','349','SIUP PERMOHONAN BARU Perusahaan berbentuk Perseroan Terbatas (PT) - Baru/Pendirian',3,'',33,1),(299,'2016-10-03 15:33:55','254','SIUP PERMOHONAN BARU Perusahaan berbentuk Perseroan Terbatas (PT) - Baru/Pendirian',3,'',33,1),(300,'2016-10-03 15:33:55','250','SIUP PERMOHONAN BARU Perusahaan berbentuk Perseroan Terbatas (PT) - Baru/Pendirian',3,'',33,1),(301,'2016-10-03 15:33:55','246','SIUP PERMOHONAN BARU Perusahaan berbentuk Perseroan Terbatas (PT) - Baru/Pendirian',3,'',33,1),(302,'2016-10-03 15:33:55','234','SIUP PERMOHONAN BARU Perusahaan berbentuk Perseroan Terbatas (PT) - Baru/Pendirian',3,'',33,1),(303,'2016-10-03 15:33:55','230','SIUP PERMOHONAN BARU Perusahaan berbentuk Perseroan Terbatas (PT) - Baru/Pendirian',3,'',33,1),(304,'2016-10-03 15:33:55','227','SIUP PERMOHONAN BARU Perusahaan berbentuk Perseroan Terbatas (PT) - Baru/Pendirian',3,'',33,1),(305,'2016-10-03 15:33:55','220','SIUP PERMOHONAN BARU Perusahaan berbentuk Perseroan Terbatas (PT) - Baru/Pendirian',3,'',33,1),(306,'2016-10-03 15:33:55','218','SIUP PERMOHONAN BARU Perusahaan berbentuk Perseroan Terbatas (PT) - Baru/Pendirian',3,'',33,1),(307,'2016-10-03 15:33:55','216','SIUP PERMOHONAN BARU Perusahaan berbentuk Perseroan Terbatas (PT) - Baru/Pendirian',3,'',33,1),(308,'2016-10-03 15:33:55','213','SIUP PERMOHONAN BARU Perusahaan berbentuk Perseroan Terbatas (PT) - Baru/Pendirian',3,'',33,1),(309,'2016-10-03 15:33:55','209','SIUP PERMOHONAN BARU Perusahaan berbentuk Perseroan Terbatas (PT) - Baru/Pendirian',3,'',33,1),(310,'2016-10-03 15:33:56','207','SIUP PERMOHONAN BARU Perusahaan berbentuk Perseroan Terbatas (PT) - Baru/Pendirian',3,'',33,1),(311,'2016-10-03 15:33:56','197','SIUP PERMOHONAN BARU Perusahaan berbentuk Perseroan Terbatas (PT) - Baru/Pendirian',3,'',33,1),(312,'2016-10-03 15:33:56','194','SIUP PERMOHONAN BARU Perusahaan berbentuk Perseroan Terbatas (PT) - Baru/Pendirian',3,'',33,1),(313,'2016-10-03 15:33:56','143','SIUP PERMOHONAN BARU Perusahaan berbentuk Perseroan Terbatas (PT) - Baru/Pendirian',3,'',33,1),(314,'2016-10-03 15:33:56','103','SIUP PERMOHONAN BARU Perusahaan berbentuk Perseroan Terbatas (PT) - Baru/Pendirian',3,'',33,1),(315,'2016-10-03 15:33:56','98','SIUP PERMOHONAN BARU Perusahaan berbentuk Perseroan Terbatas (PT) - Baru/Pendirian',3,'',33,1),(316,'2016-10-04 02:01:11','100','MAKMUR',3,'',44,1),(317,'2016-10-04 02:01:11','141','Software Engineering Organization',3,'',44,1),(318,'2016-10-04 02:01:11','144','Seo',3,'',44,1),(319,'2016-10-04 02:01:12','145','Seo',3,'',44,1),(320,'2016-10-04 02:01:12','146','Seo',3,'',44,1),(321,'2016-10-04 02:01:12','147','asd',3,'',44,1),(322,'2016-10-04 02:01:12','148','asd',3,'',44,1),(323,'2016-10-04 02:01:12','149','asd',3,'',44,1),(324,'2016-10-04 02:01:12','195','SEO',3,'',44,1),(325,'2016-10-04 02:01:12','198','SEO',3,'',44,1),(326,'2016-10-04 02:01:12','214','er',3,'',44,1),(327,'2016-10-04 02:01:12','221','Okta',3,'',44,1),(328,'2016-10-04 02:01:12','222','Okta',3,'',44,1),(329,'2016-10-04 02:01:12','223','qwerty',3,'',44,1),(330,'2016-10-04 02:01:13','224','eeeeeee',3,'',44,1),(331,'2016-10-04 02:01:13','225','eeeeeee',3,'',44,1),(332,'2016-10-04 02:01:13','228','sdasd',3,'',44,1),(333,'2016-10-04 02:01:13','231','sdasd',3,'',44,1),(334,'2016-10-04 02:01:13','232','sdasd',3,'',44,1),(335,'2016-10-04 02:01:13','235','Tenggo',3,'',44,1),(336,'2016-10-04 02:01:13','267','ererer',3,'',44,1),(337,'2016-10-04 02:01:13','352','OPH OL',3,'',44,1),(338,'2016-10-04 02:01:13','378','kediri',3,'',44,1),(339,'2016-10-04 02:01:13','384','kediri',3,'',44,1),(340,'2016-10-04 02:01:13','387','Torru',3,'',44,1),(341,'2016-10-04 02:01:13','388','Torru',3,'',44,1),(342,'2016-10-04 02:01:14','389','fg',3,'',44,1),(343,'2016-10-04 02:01:14','390','fg',3,'',44,1),(344,'2016-10-04 02:01:14','391','fg',3,'',44,1),(345,'2016-10-04 02:10:10','386','SIUP PERMOHONAN BARU Perusahaan berbentuk Perseroan Terbatas (PT) - Baru/Pendirian',3,'',33,1),(346,'2016-10-04 02:10:10','368','SIUP PERMOHONAN BARU Perusahaan berbentuk Perseroan Terbatas (PT) - Baru/Pendirian',3,'',33,1),(347,'2016-10-04 02:11:08','97','TAUFAN BUDIMAN',3,'',25,1),(348,'2016-10-04 02:11:08','102','EKA JAYA',3,'',25,1),(349,'2016-10-04 02:11:08','128','ASD',3,'',25,1),(350,'2016-10-04 02:11:08','131','SAD',3,'',25,1),(351,'2016-10-04 02:11:08','140','FEBRI',3,'',25,1),(352,'2016-10-04 02:11:08','142','FEBRI AHMAD NURHIDAYAT',3,'',25,1),(353,'2016-10-04 02:11:09','206','REEE',3,'',25,1),(354,'2016-10-04 02:11:09','212','ERRRRRRR',3,'',25,1),(355,'2016-10-04 02:11:09','217','FEBRI AHMAD NURHIDAYAT',3,'',25,1),(356,'2016-10-04 02:11:09','226','676666',3,'',25,1),(357,'2016-10-04 02:11:10','229','VRT',3,'',25,1),(358,'2016-10-04 02:11:10','253','BAMBANG',3,'',25,1),(359,'2016-10-04 02:11:10','265','UNYIL',3,'',25,1),(360,'2016-10-04 02:11:10','348','OKTAFIA PUTRI HANDAYANI',3,'',25,1),(361,'2016-10-04 02:11:10','363','GILANG',3,'',25,1),(362,'2016-10-04 02:11:10','365','YUYUN',3,'',25,1),(363,'2016-10-04 02:11:10','367','FEBRI AHMAD NURHIDAYAT',3,'',25,1),(364,'2016-10-04 02:11:10','385','TURO',3,'',25,1),(365,'2016-10-04 03:23:40','394','SEO',2,'penanggung_jawab diubah',44,1),(366,'2016-10-04 04:55:44','393','Detil SIUP PERMOHONAN BARU Perusahaan berbentuk Perseroan Terbatas (PT) - Baru/Pendirian',2,'status diubah',46,62),(367,'2016-10-04 05:01:26','393','Detil SIUP PERMOHONAN BARU Perusahaan berbentuk Perseroan Terbatas (PT) - Baru/Pendirian',2,'status dan perusahaan diubah',46,62),(368,'2016-10-04 05:02:37','393','Detil SIUP PERMOHONAN BARU Perusahaan berbentuk Perseroan Terbatas (PT) - Baru/Pendirian',2,'perusahaan diubah',46,62),(369,'2016-10-04 05:09:22','393','Detil SIUP PERMOHONAN BARU Perusahaan berbentuk Perseroan Terbatas (PT) - Baru/Pendirian',2,'status diubah',46,62),(370,'2016-10-04 05:10:53','393','Detil SIUP PERMOHONAN BARU Perusahaan berbentuk Perseroan Terbatas (PT) - Baru/Pendirian',2,'perusahaan diubah',46,62),(371,'2016-10-04 05:39:04','7','Penomoran',1,'',4,1),(372,'2016-10-04 06:28:20','282','DYAH KIRONOSARI',2,'alamat, negara, desa dan groups diubah',24,1),(373,'2016-10-04 06:56:21','486','9',2,'status diubah',54,282),(374,'2016-10-04 07:06:19','486','9',2,'status diubah',54,282),(375,'2016-10-04 07:09:37','486','9',2,'status diubah',54,282),(376,'2016-10-04 07:49:20','8','Cetak',1,'',4,1),(377,'2016-10-04 07:54:58','283','ZAKY ZAMRONI',2,'alamat, negara, desa dan groups diubah',24,1),(378,'2016-10-04 08:11:49','486','10',2,'status diubah',54,1),(379,'2016-10-04 08:18:41','9','Selesai',1,'',4,1),(380,'2016-10-04 08:21:54','284','SRI WINARTI',2,'alamat, negara, desa dan groups diubah',24,1),(381,'2016-10-06 00:30:43','272','DAMAS DANUR RENDRA',2,'alamat, negara, desa dan groups diubah',24,1),(382,'2016-10-06 00:55:29','520','Detil SIUP PERMOHONAN BARU Perusahaan berbentuk Perseroan Terbatas (PT) - Baru/Pendirian',2,'perusahaan diubah',46,281),(383,'2016-10-06 01:12:47','523','10',2,'status diubah',54,1),(384,'2016-10-06 01:16:01','523','10',2,'status diubah',54,1),(385,'2016-10-06 01:18:35','523','10',2,'status diubah',54,1),(386,'2016-10-06 02:20:08','537','Detil SIUP PERMOHONAN BARU Perusahaan berbentuk Perseroan Terbatas (PT) - Baru/Pendirian',2,'status dan no_izin diubah',46,1),(387,'2016-10-06 07:10:05','574','4',2,'status diubah',54,1),(388,'2016-10-06 13:20:49','17','SIUP',2,'kelompok_jenis_izin diubah',29,1),(389,'2016-10-06 19:09:48','17','SIUP',2,'kode diubah',29,1),(390,'2016-10-06 19:20:19','574','9',2,'status diubah',54,1),(391,'2016-10-06 19:24:19','574','9',2,'status diubah',54,1);
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
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_3ec8c61c_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=56 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (18,'accounts','account'),(17,'accounts','identitaspribadi'),(19,'accounts','nomoridentitaspengguna'),(2,'admin','logentry'),(4,'auth','group'),(3,'auth','permission'),(8,'cas','pgtiou'),(7,'cas','tgt'),(5,'contenttypes','contenttype'),(27,'izin','dasarhukum'),(53,'izin','detilreklame'),(46,'izin','detilsiup'),(28,'izin','jenisizin'),(26,'izin','jenisperaturan'),(32,'izin','jenispermohonanizin'),(29,'izin','kelompokjenisizin'),(25,'izin','pemohon'),(33,'izin','pengajuanizin'),(31,'izin','prosedur'),(55,'izin','riwayat'),(54,'izin','skizin'),(30,'izin','syarat'),(22,'kepegawaian','bidangstruktural'),(23,'kepegawaian','jabatan'),(20,'kepegawaian','jenisunitkerja'),(24,'kepegawaian','pegawai'),(21,'kepegawaian','unitkerja'),(36,'master','atributtambahan'),(49,'master','berkas'),(16,'master','desa'),(10,'master','jenisnomoridentitas'),(9,'master','jenispemohon'),(52,'master','jenisreklame'),(14,'master','kabupaten'),(15,'master','kecamatan'),(12,'master','negara'),(13,'master','provinsi'),(11,'master','settings'),(1,'menu','bookmark'),(48,'perusahaan','bentukkegiatanusaha'),(42,'perusahaan','jenisbadanusaha'),(50,'perusahaan','jenislegalitas'),(41,'perusahaan','jenispenanamanmodal'),(38,'perusahaan','jenisperusahaan'),(37,'perusahaan','kbli'),(39,'perusahaan','kelembagaan'),(51,'perusahaan','legalitas'),(44,'perusahaan','perusahaan'),(40,'perusahaan','produkutama'),(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=63 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2016-08-18 03:58:45'),(2,'admin','0001_initial','2016-08-18 03:58:46'),(3,'contenttypes','0002_remove_content_type_name','2016-08-18 03:58:46'),(4,'auth','0001_initial','2016-08-18 03:58:48'),(5,'auth','0002_alter_permission_name_max_length','2016-08-18 03:58:48'),(6,'auth','0003_alter_user_email_max_length','2016-08-18 03:58:48'),(7,'auth','0004_alter_user_username_opts','2016-08-18 03:58:48'),(8,'auth','0005_alter_user_last_login_null','2016-08-18 03:58:48'),(9,'auth','0006_require_contenttypes_0002','2016-08-18 03:58:48'),(10,'sessions','0001_initial','2016-08-18 03:58:49'),(11,'accounts','0001_initial','2016-08-26 00:14:08'),(12,'accounts','0002_remove_identitaspribadi_hp','2016-08-26 00:14:59'),(13,'accounts','0003_auto_20160826_0715','2016-08-26 00:16:04'),(14,'izin','0001_initial','2016-08-26 00:18:00'),(15,'kepegawaian','0001_initial','2016-08-26 00:18:11'),(16,'accounts','0004_remove_identitaspribadi_hp','2016-08-26 00:20:15'),(17,'izin','0002_auto_20160826_0725','2016-08-26 00:25:44'),(18,'accounts','0005_remove_identitaspribadi_hp','2016-08-26 00:27:15'),(19,'izin','0003_jenisizin_kode','2016-08-29 03:26:01'),(20,'izin','0004_auto_20160903_0943','2016-09-03 02:43:44'),(21,'izin','0005_auto_20160903_1006','2016-09-03 03:06:58'),(22,'izin','0005_auto_20160903_1007','2016-09-03 03:08:28'),(23,'izin','0006_auto_20160903_1024','2016-09-03 03:25:23'),(24,'izin','0007_auto_20160903_1036','2016-09-03 03:39:08'),(25,'perusahaan','0001_initial','2016-09-03 03:40:33'),(27,'master','0001_initial','2016-09-03 03:40:33'),(28,'master','0002_atributtambahan','2016-09-05 01:06:29'),(29,'izin','0008_auto_20160905_0749','2016-09-05 01:07:22'),(30,'izin','0009_auto_20160905_0826','2016-09-05 01:29:15'),(31,'izin','0010_detilsiup_kbli','2016-09-05 01:31:08'),(32,'izin','0011_auto_20160905_0831','2016-09-05 01:32:34'),(33,'izin','0012_detilsiup_kbli','2016-09-05 01:35:23'),(34,'accounts','0006_auto_20160905_0813','2016-09-05 02:29:29'),(35,'izin','0013_auto_20160906_1207','2016-09-06 05:09:23'),(36,'perusahaan','0002_auto_20160906_1207','2016-09-06 05:11:19'),(37,'perusahaan','0003_auto_20160906_1210','2016-09-06 05:11:19'),(38,'master','0003_berkas','2016-09-07 03:54:09'),(39,'izin','0014_auto_20160907_1106','2016-09-07 04:09:59'),(40,'perusahaan','0004_jenislegalitas_legalitas','2016-09-08 00:30:28'),(41,'izin','0015_auto_20160908_0729','2016-09-08 00:36:41'),(42,'perusahaan','0005_legalitas_perusahaan','2016-09-08 00:43:52'),(43,'izin','0016_detilsiup_legalitas','2016-09-08 00:43:53'),(44,'izin','0017_auto_20160908_1040','2016-09-08 03:40:38'),(45,'perusahaan','0006_perusahaan_berkas_npwp','2016-09-08 08:15:57'),(46,'perusahaan','0002_perusahaan_berkas_npwp','2016-09-23 00:34:39'),(47,'izin','0002_kelompokjenisizin_kode','2016-09-23 00:35:04'),(48,'izin','0003_detilsiup_jenis_penanaman_modal','2016-09-23 00:35:41'),(49,'izin','0004_detilsiup_berkas_npwp_pemohon','2016-09-23 00:35:41'),(50,'izin','0005_auto_20160908_1209','2016-09-23 00:35:41'),(51,'izin','0006_auto_20160913_1049','2016-09-23 00:35:41'),(52,'izin','0007_detilsiup_berkas_foto','2016-09-23 00:36:03'),(53,'izin','0008_auto_20160913_1054','2016-09-23 00:36:03'),(54,'izin','0009_auto_20160922_1211','2016-09-23 00:36:03'),(55,'izin','0010_auto_20160923_0741','2016-09-23 00:43:24'),(56,'perusahaan','0003_perusahaan_berkas_npwp','2016-09-23 00:43:48'),(57,'perusahaan','0004_perusahaan_berkas_npwp','2016-09-23 00:48:27'),(58,'izin','0011_auto_20160923_0744','2016-09-23 00:48:55'),(59,'izin','0012_detilsiup_perusahaan','2016-09-23 04:25:41'),(60,'accounts','0002_nomoridentitaspengguna_berkas','2016-09-23 07:16:14'),(61,'izin','0013_detilreklame','2016-09-23 07:37:08'),(62,'izin','0014_auto_20161001_0855','2016-10-01 01:55:28');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
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
  KEY `django_session_de54fa62` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('023z0s3gss9lknix59wnd6t7leg6rrts','ZTJjNDQwZWVhNmVkYzc2YTM1ZjU0NzM3ZTQzMjA4YzY4MTZkZGFjMTp7Il9hdXRoX3VzZXJfaGFzaCI6IjhjNjFlODkwY2NhYzg0OTk3MmQzODhiNzhiZjFkN2M2ZjcyODEyOTUiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2016-10-17 06:06:03'),('3gpvpcu7fuz4oizga7k9h7twgweg25te','Mzk1MWM4YjI1MzI3NmE0MGIyMzMyM2NmNTc1MGFjMGQ5NTE4YWQ1Zjp7Il9hdXRoX3VzZXJfaGFzaCI6Ijk5M2JlYzMyNWE0ZmFjZmVlMTNmNTRmYzA5MTI3ZWZjMTQ5ODVmODAiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiI2MiIsImxvZ2luYXNfZnJvbV91c2VyIjoxfQ==','2016-10-01 02:21:38'),('3if4n53u0mjgyejhdj24wi0oay7qv2xm','MTkyODNjYTI3YWY2YTI5ZDcyMGE4NTQwZjQ2NDBmZDA3NDliNmU1MTp7Il9hdXRoX3VzZXJfaGFzaCI6ImY4ZDdmZTdhOWQ5MWRlNWMxYzBkNjllYjFjNWVlZGIwYTRmZGRhOTkiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIyNzMiLCJsb2dpbmFzX2Zyb21fdXNlciI6MX0=','2016-10-15 02:38:23'),('461l1smyvkqyv13vwt2t37n2n5796qti','ZTJjNDQwZWVhNmVkYzc2YTM1ZjU0NzM3ZTQzMjA4YzY4MTZkZGFjMTp7Il9hdXRoX3VzZXJfaGFzaCI6IjhjNjFlODkwY2NhYzg0OTk3MmQzODhiNzhiZjFkN2M2ZjcyODEyOTUiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2016-10-03 05:41:59'),('4q50dr3onw52aoidjpe2zpenw1l3b9u9','MTc4ZWI0ZmFmNDRmMTZjYmU2ZTZjM2Q0Yzk5ODk0MGNhYzRmOGQ0NTp7Il9hdXRoX3VzZXJfaGFzaCI6IjUxNDFjMTY4Yzg1MjBiMzhiZTg2YzA4YjJjN2NkZWUyMzc3Y2MxOGUiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2016-09-01 03:59:47'),('6g1k5xeo5lrfvtrueb0ini5bxxgwlr0o','ZTJjNDQwZWVhNmVkYzc2YTM1ZjU0NzM3ZTQzMjA4YzY4MTZkZGFjMTp7Il9hdXRoX3VzZXJfaGFzaCI6IjhjNjFlODkwY2NhYzg0OTk3MmQzODhiNzhiZjFkN2M2ZjcyODEyOTUiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2016-10-20 01:12:04'),('7agxhixztx8hl9i46ueg2qtyktolmxmo','ZDVmMzM4NjNlZDM2ZTY1YzE3YWFlMDUyYjUyM2VlM2JlYWE5MDBkODp7Il9hdXRoX3VzZXJfaGFzaCI6ImY4ZDdmZTdhOWQ5MWRlNWMxYzBkNjllYjFjNWVlZGIwYTRmZGRhOTkiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIyODQiLCJsb2dpbmFzX2Zyb21fdXNlciI6MX0=','2016-10-18 08:22:27'),('8t16m3n9do15d5jte0vw92youfdw99uk','ZTJjNDQwZWVhNmVkYzc2YTM1ZjU0NzM3ZTQzMjA4YzY4MTZkZGFjMTp7Il9hdXRoX3VzZXJfaGFzaCI6IjhjNjFlODkwY2NhYzg0OTk3MmQzODhiNzhiZjFkN2M2ZjcyODEyOTUiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2016-10-13 02:14:41'),('a8fl2gwr3v9ncn62mdviiorq0hqrcrwl','ZTJjNDQwZWVhNmVkYzc2YTM1ZjU0NzM3ZTQzMjA4YzY4MTZkZGFjMTp7Il9hdXRoX3VzZXJfaGFzaCI6IjhjNjFlODkwY2NhYzg0OTk3MmQzODhiNzhiZjFkN2M2ZjcyODEyOTUiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2016-10-20 11:38:11'),('ahh3x23v5npnw3c01yhl51769vbe40dv','ZTJjNDQwZWVhNmVkYzc2YTM1ZjU0NzM3ZTQzMjA4YzY4MTZkZGFjMTp7Il9hdXRoX3VzZXJfaGFzaCI6IjhjNjFlODkwY2NhYzg0OTk3MmQzODhiNzhiZjFkN2M2ZjcyODEyOTUiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2016-10-07 07:21:17'),('b7on39awyfhoq1x76dbljkl9tglozvui','ZTJjNDQwZWVhNmVkYzc2YTM1ZjU0NzM3ZTQzMjA4YzY4MTZkZGFjMTp7Il9hdXRoX3VzZXJfaGFzaCI6IjhjNjFlODkwY2NhYzg0OTk3MmQzODhiNzhiZjFkN2M2ZjcyODEyOTUiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2016-09-24 01:01:24'),('bklt6kvru4spb8d4tqsy6wf17gvnrcnn','ZTJjNDQwZWVhNmVkYzc2YTM1ZjU0NzM3ZTQzMjA4YzY4MTZkZGFjMTp7Il9hdXRoX3VzZXJfaGFzaCI6IjhjNjFlODkwY2NhYzg0OTk3MmQzODhiNzhiZjFkN2M2ZjcyODEyOTUiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2016-10-13 02:08:04'),('cgk714tnvpvan1n1n7q185sbjdqrvs85','OGRhMmZjNDhmYWZjYWVjMTY2YWMxODk4Mjc0Y2Y5YzMzMDE1MjYxMzp7Il9hdXRoX3VzZXJfaGFzaCI6Ijk5M2JlYzMyNWE0ZmFjZmVlMTNmNTRmYzA5MTI3ZWZjMTQ5ODVmODAiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiI2MiJ9','2016-09-20 03:57:26'),('cll4f0cgqr85qevsi7x2vhkqjkpkvlk0','ZTJjNDQwZWVhNmVkYzc2YTM1ZjU0NzM3ZTQzMjA4YzY4MTZkZGFjMTp7Il9hdXRoX3VzZXJfaGFzaCI6IjhjNjFlODkwY2NhYzg0OTk3MmQzODhiNzhiZjFkN2M2ZjcyODEyOTUiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2016-09-19 02:37:32'),('djajtridibqylmk665kgmszfx1z3jokn','ZTJjNDQwZWVhNmVkYzc2YTM1ZjU0NzM3ZTQzMjA4YzY4MTZkZGFjMTp7Il9hdXRoX3VzZXJfaGFzaCI6IjhjNjFlODkwY2NhYzg0OTk3MmQzODhiNzhiZjFkN2M2ZjcyODEyOTUiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2016-10-21 03:26:14'),('e3j09r3d10upe2b2b3fnf3lqtv7kgum2','ZTJjNDQwZWVhNmVkYzc2YTM1ZjU0NzM3ZTQzMjA4YzY4MTZkZGFjMTp7Il9hdXRoX3VzZXJfaGFzaCI6IjhjNjFlODkwY2NhYzg0OTk3MmQzODhiNzhiZjFkN2M2ZjcyODEyOTUiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2016-10-17 08:21:14'),('f8y2vl1g8zzuzsebrbcwzhmq2wnwmv5y','OGRhMmZjNDhmYWZjYWVjMTY2YWMxODk4Mjc0Y2Y5YzMzMDE1MjYxMzp7Il9hdXRoX3VzZXJfaGFzaCI6Ijk5M2JlYzMyNWE0ZmFjZmVlMTNmNTRmYzA5MTI3ZWZjMTQ5ODVmODAiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiI2MiJ9','2016-09-21 04:12:16'),('fw7on7117sfwwcc10kozwl3pvh9e1rcn','ZTJjNDQwZWVhNmVkYzc2YTM1ZjU0NzM3ZTQzMjA4YzY4MTZkZGFjMTp7Il9hdXRoX3VzZXJfaGFzaCI6IjhjNjFlODkwY2NhYzg0OTk3MmQzODhiNzhiZjFkN2M2ZjcyODEyOTUiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2016-10-14 10:37:16'),('g4ch6dmi4l3cv4y3xg7wrg8lkqa1p3d0','ZTJjNDQwZWVhNmVkYzc2YTM1ZjU0NzM3ZTQzMjA4YzY4MTZkZGFjMTp7Il9hdXRoX3VzZXJfaGFzaCI6IjhjNjFlODkwY2NhYzg0OTk3MmQzODhiNzhiZjFkN2M2ZjcyODEyOTUiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2016-10-20 11:19:46'),('inref58m1rxltysjkjo8mj6klvyqbfsn','Mzk1MWM4YjI1MzI3NmE0MGIyMzMyM2NmNTc1MGFjMGQ5NTE4YWQ1Zjp7Il9hdXRoX3VzZXJfaGFzaCI6Ijk5M2JlYzMyNWE0ZmFjZmVlMTNmNTRmYzA5MTI3ZWZjMTQ5ODVmODAiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiI2MiIsImxvZ2luYXNfZnJvbV91c2VyIjoxfQ==','2016-10-13 07:52:01'),('knld4pqzq1spy2u1xe4u8pezws6o7tfe','ZTJjNDQwZWVhNmVkYzc2YTM1ZjU0NzM3ZTQzMjA4YzY4MTZkZGFjMTp7Il9hdXRoX3VzZXJfaGFzaCI6IjhjNjFlODkwY2NhYzg0OTk3MmQzODhiNzhiZjFkN2M2ZjcyODEyOTUiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2016-10-20 08:23:20'),('nfvbtrwib17avafjqshwh62dnj9yshvt','ZTJjNDQwZWVhNmVkYzc2YTM1ZjU0NzM3ZTQzMjA4YzY4MTZkZGFjMTp7Il9hdXRoX3VzZXJfaGFzaCI6IjhjNjFlODkwY2NhYzg0OTk3MmQzODhiNzhiZjFkN2M2ZjcyODEyOTUiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2016-10-20 07:50:17'),('np3kgmvtddld4rchlqzbf0s7nqklx5e6','ZTJjNDQwZWVhNmVkYzc2YTM1ZjU0NzM3ZTQzMjA4YzY4MTZkZGFjMTp7Il9hdXRoX3VzZXJfaGFzaCI6IjhjNjFlODkwY2NhYzg0OTk3MmQzODhiNzhiZjFkN2M2ZjcyODEyOTUiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2016-10-14 01:26:13'),('oi5vbugdtu94b91d1m05piy0of3h6kfx','ZTJjNDQwZWVhNmVkYzc2YTM1ZjU0NzM3ZTQzMjA4YzY4MTZkZGFjMTp7Il9hdXRoX3VzZXJfaGFzaCI6IjhjNjFlODkwY2NhYzg0OTk3MmQzODhiNzhiZjFkN2M2ZjcyODEyOTUiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2016-09-22 01:00:46'),('qcay2i2c9n1359bdcoclroccqi0dp7i8','YmM3MTUxZGExODIwOGNmZGY5Y2YzN2QxMDcwZDBhYWU4MmE0ZGIwMzp7Il9hdXRoX3VzZXJfaGFzaCI6ImY4ZDdmZTdhOWQ5MWRlNWMxYzBkNjllYjFjNWVlZGIwYTRmZGRhOTkiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIyODMiLCJsb2dpbmFzX2Zyb21fdXNlciI6MX0=','2016-10-18 07:55:39'),('rpc34h3lk7ied4u5fku0bzo2zfr9tsjc','ZTJjNDQwZWVhNmVkYzc2YTM1ZjU0NzM3ZTQzMjA4YzY4MTZkZGFjMTp7Il9hdXRoX3VzZXJfaGFzaCI6IjhjNjFlODkwY2NhYzg0OTk3MmQzODhiNzhiZjFkN2M2ZjcyODEyOTUiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2016-10-13 05:59:43'),('syi2u1cwo6wt24ja7ab40nchpknjware','MTc4ZWI0ZmFmNDRmMTZjYmU2ZTZjM2Q0Yzk5ODk0MGNhYzRmOGQ0NTp7Il9hdXRoX3VzZXJfaGFzaCI6IjUxNDFjMTY4Yzg1MjBiMzhiZTg2YzA4YjJjN2NkZWUyMzc3Y2MxOGUiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2016-09-05 03:09:02'),('v3ar2cnamkmolz497wc3w6657k97wtpg','MTc4ZWI0ZmFmNDRmMTZjYmU2ZTZjM2Q0Yzk5ODk0MGNhYzRmOGQ0NTp7Il9hdXRoX3VzZXJfaGFzaCI6IjUxNDFjMTY4Yzg1MjBiMzhiZTg2YzA4YjJjN2NkZWUyMzc3Y2MxOGUiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2016-09-03 02:53:04'),('wq9kvqx8zfk435xy8mmkhaj7s28gk4n0','ZTJjNDQwZWVhNmVkYzc2YTM1ZjU0NzM3ZTQzMjA4YzY4MTZkZGFjMTp7Il9hdXRoX3VzZXJfaGFzaCI6IjhjNjFlODkwY2NhYzg0OTk3MmQzODhiNzhiZjFkN2M2ZjcyODEyOTUiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2016-10-13 08:12:13'),('ydfi3ci3xioqda9b1n826bwv7ow2c5rl','ZTJjNDQwZWVhNmVkYzc2YTM1ZjU0NzM3ZTQzMjA4YzY4MTZkZGFjMTp7Il9hdXRoX3VzZXJfaGFzaCI6IjhjNjFlODkwY2NhYzg0OTk3MmQzODhiNzhiZjFkN2M2ZjcyODEyOTUiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2016-09-23 00:57:24'),('ygj80y6wwjq528c4a417a2zrldmemikx','MTc4ZWI0ZmFmNDRmMTZjYmU2ZTZjM2Q0Yzk5ODk0MGNhYzRmOGQ0NTp7Il9hdXRoX3VzZXJfaGFzaCI6IjUxNDFjMTY4Yzg1MjBiMzhiZTg2YzA4YjJjN2NkZWUyMzc3Y2MxOGUiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2016-09-08 03:36:19'),('yuy6b074fof4j5wtw4by4vj6j746zx8n','ZTJjNDQwZWVhNmVkYzc2YTM1ZjU0NzM3ZTQzMjA4YzY4MTZkZGFjMTp7Il9hdXRoX3VzZXJfaGFzaCI6IjhjNjFlODkwY2NhYzg0OTk3MmQzODhiNzhiZjFkN2M2ZjcyODEyOTUiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2016-09-21 04:19:26');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `izin_dasarhukum`
--

DROP TABLE IF EXISTS `izin_dasarhukum`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `izin_dasarhukum` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `jenis_peraturan_id` int(11) NOT NULL,
  `instansi` varchar(100) NOT NULL,
  `nomor` varchar(100) NOT NULL,
  `tahun` smallint(5) unsigned NOT NULL,
  `tentang` varchar(255) NOT NULL,
  `keterangan` varchar(255) DEFAULT NULL,
  `berkas` varchar(255) DEFAULT NULL,
  `berkas_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `izin_dasarhukum_c42e8079` (`berkas_id`),
  CONSTRAINT `izin__berkas_id_1a8a7fe1_fk_master_berkas_atributtambahan_ptr_id` FOREIGN KEY (`berkas_id`) REFERENCES `master_berkas` (`atributtambahan_ptr_id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `izin_dasarhukum`
--

LOCK TABLES `izin_dasarhukum` WRITE;
/*!40000 ALTER TABLE `izin_dasarhukum` DISABLE KEYS */;
INSERT INTO `izin_dasarhukum` VALUES (1,1,'Kabupaten Kediri','No. 24/PRT/M/2007',2007,'Tentang Pedoman Teknis Izin Mendirikan Bangunan Gedung','','',NULL),(2,2,'Kabupaten Kediri','Nomor 34 Tahun 2008',2008,'Tentang Organisasi dan Tata Kerja KPPT','','',NULL),(3,2,'Kabupaten Kediri','Nomor 2 Tahun 2009',2009,'Tentang Pelayanan Publik di Kabupaten Kediri','','',NULL),(4,2,'Kabupaten Kediri','Nomor 4 Tahun 2012',2012,'Tentang Retribusi Izin Mendirikan Bangunan','','',NULL),(5,3,'Kabupaten Kediri','Nomor 60 Tahun 2010',2010,'Tentang Penjabaran Tupoksi KPPT Kabupaten Kediri','','',NULL),(6,4,'Kabupaten Kediri','Nomor 188.45/480/418.32/2012',2012,'Tentang Pelimpahan sebagian kewenangan di bidang Pelayanan Perizinan kepada Kantor Kepala Kantor Pelayanan dan Perizinan Terpadu Kabupaten Kediri','','',NULL),(7,5,'Kabupaten Kediri','RI No. 27 Tahun 2009',2009,'Tentang Pedoman Penetapan Izin Gangguan Daerah ','','',NULL),(9,2,'Kabupaten Kediri','Nomor 5 Tahun 2012',2012,'Tentang Retribusi Izin Gangguan','','',NULL),(10,2,'Kabupaten Kediri','Nomor 8 Tahun 2006 ',2006,'Tentang Pajak Reklame','','',NULL),(11,8,'Kabupaten Kediri','Nomor 23 Tahun 2001 ',2001,'Tentang retribusi Perusahaan Penggilingan Padi, Huller dan Penyosohan Beras serta Mesin Perontok Padi dan Jagung','','',NULL),(12,2,'Kabupaten Kediri','Nomor 17 Tahun 2011',2011,'Tentang Retribusi Pemakaian Kekayaan Daerah','','',NULL),(13,8,'Kabupaten Kediri','Nomor 17 Tahun 2011',2011,'Tentang Pemakaian Kekayaan Daerah','','',NULL),(14,9,'Kabupaten Kediri','Nomor 36/M-DAG/PER/12/2011 ',2011,'Tentang penerbitan SIUP','','',NULL),(15,2,'Kabupaten Kediri','Nomor 5 Tahun 2013',2013,'Tentang SIUP, TDP, Izin  Industri dan TDG','','',NULL),(16,9,'Kabupaten Kediri','Nomor 37/M-DAG/PER/9/2007 ',2007,'Tentang Penyelenggaraan Pendaftaran Perusahaan','','',NULL),(17,10,'Kabupaten Kediri','No. 5 Tahun 2013 ',2013,'Tentang Tata Cara Perizinan Penanaman Modal ','','',NULL),(18,11,'Kabupaten Kediri','Nomor 5 Tahun 1960 ',1960,'Tentang Peraturan Dasar Pokok-pokok Agraria','','',NULL),(19,12,'Kabupaten Kediri','Nomor 50 Tahun 2009 ',2009,'Tentang Pedoman Koordinasi Penataan Ruang Daerah','','',NULL),(20,13,'Kabupaten Kediri','Nomor 2 Tahun 2003',2003,'Tentang Norma dan Standart Mekanisme Ketatalaksanaan Kewenangan Pemerintah di Bidang Pertanahan yang Dilaksanakan oleh Pemerintah Kabupaten/Kota','','',NULL);
/*!40000 ALTER TABLE `izin_dasarhukum` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `izin_detilreklame`
--

DROP TABLE IF EXISTS `izin_detilreklame`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `izin_detilreklame` (
  `pengajuanizin_ptr_id` int(11) NOT NULL,
  `judul_reklame` varchar(255) NOT NULL,
  `panjang` decimal(5,2) DEFAULT NULL,
  `lebar` decimal(5,2) DEFAULT NULL,
  `sisi` decimal(5,2) DEFAULT NULL,
  `letak_pemasangan` varchar(255) DEFAULT NULL,
  `lt` varchar(100) DEFAULT NULL,
  `lg` varchar(100) DEFAULT NULL,
  `desa_id` int(11) NOT NULL,
  `jenis_reklame_id` int(11) NOT NULL,
  `perusahaan_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`pengajuanizin_ptr_id`),
  KEY `izin_detilreklame_desa_id_5ba0818c_fk_master_desa_id` (`desa_id`),
  KEY `izin_detilre_jenis_reklame_id_5f8a69e1_fk_master_jenisreklame_id` (`jenis_reklame_id`),
  KEY `ef0fa786430700cd30b4377457555b05` (`perusahaan_id`),
  CONSTRAINT `c855a26f554304c21789a66197bfaadc` FOREIGN KEY (`pengajuanizin_ptr_id`) REFERENCES `izin_pengajuanizin` (`atributtambahan_ptr_id`),
  CONSTRAINT `ef0fa786430700cd30b4377457555b05` FOREIGN KEY (`perusahaan_id`) REFERENCES `perusahaan_perusahaan` (`atributtambahan_ptr_id`),
  CONSTRAINT `izin_detilreklame_desa_id_5ba0818c_fk_master_desa_id` FOREIGN KEY (`desa_id`) REFERENCES `master_desa` (`id`),
  CONSTRAINT `izin_detilre_jenis_reklame_id_5f8a69e1_fk_master_jenisreklame_id` FOREIGN KEY (`jenis_reklame_id`) REFERENCES `master_jenisreklame` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `izin_detilreklame`
--

LOCK TABLES `izin_detilreklame` WRITE;
/*!40000 ALTER TABLE `izin_detilreklame` DISABLE KEYS */;
/*!40000 ALTER TABLE `izin_detilreklame` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `izin_detilsiup`
--

DROP TABLE IF EXISTS `izin_detilsiup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `izin_detilsiup` (
  `pengajuanizin_ptr_id` int(11) NOT NULL,
  `kekayaan_bersih` decimal(10,2) DEFAULT NULL,
  `total_nilai_saham` decimal(10,2) DEFAULT NULL,
  `presentase_saham_nasional` decimal(3,2) DEFAULT NULL,
  `presentase_saham_asing` decimal(5,2) DEFAULT NULL,
  `bentuk_kegiatan_usaha_id` int(11) DEFAULT NULL,
  `jenis_penanaman_modal_id` int(11) DEFAULT NULL,
  `kelembagaan_id` int(11) DEFAULT NULL,
  `berkas_foto_id` int(11) DEFAULT NULL,
  `berkas_npwp_pemohon_id` int(11) DEFAULT NULL,
  `berkas_npwp_perusahaan_id` int(11) DEFAULT NULL,
  `perusahaan_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`pengajuanizin_ptr_id`),
  KEY `izin_detilsiup_b7bb951f` (`berkas_foto_id`),
  KEY `izin_detilsiup_69b22878` (`berkas_npwp_pemohon_id`),
  KEY `izin_detilsiup_27357ea9` (`berkas_npwp_perusahaan_id`),
  KEY `izin_detilsiup_2b796e8b` (`perusahaan_id`),
  CONSTRAINT `bcb1f8649fd4f6416db5f74a4f2572a4` FOREIGN KEY (`pengajuanizin_ptr_id`) REFERENCES `izin_pengajuanizin` (`atributtambahan_ptr_id`),
  CONSTRAINT `be659209f97be78392695232e406febc` FOREIGN KEY (`berkas_npwp_pemohon_id`) REFERENCES `master_berkas` (`atributtambahan_ptr_id`),
  CONSTRAINT `berkas_foto_id_69a56fe2_fk_master_berkas_atributtambahan_ptr_id` FOREIGN KEY (`berkas_foto_id`) REFERENCES `master_berkas` (`atributtambahan_ptr_id`),
  CONSTRAINT `D411ecc5be561f8bccb7c85c2131cf44` FOREIGN KEY (`berkas_npwp_perusahaan_id`) REFERENCES `master_berkas` (`atributtambahan_ptr_id`),
  CONSTRAINT `D7d7d94f90d5514f814b4e3e6a984d6b` FOREIGN KEY (`perusahaan_id`) REFERENCES `perusahaan_perusahaan` (`atributtambahan_ptr_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `izin_detilsiup`
--

LOCK TABLES `izin_detilsiup` WRITE;
/*!40000 ALTER TABLE `izin_detilsiup` DISABLE KEYS */;
INSERT INTO `izin_detilsiup` VALUES (393,1000.00,12.00,1.00,12.00,1,1,1,NULL,407,408,394),(415,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(497,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(500,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(503,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(506,1.00,12222.00,9.00,122.00,1,2,1,NULL,512,513,NULL),(520,23.00,123.00,1.00,1.00,1,1,1,NULL,NULL,NULL,522),(534,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(537,50000000.00,50000000.00,1.00,NULL,1,1,1,NULL,543,544,539),(558,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(561,6000000.00,6000000.00,1.00,NULL,1,2,1,NULL,567,568,563),(581,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(584,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `izin_detilsiup` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `izin_detilsiup_kbli`
--

DROP TABLE IF EXISTS `izin_detilsiup_kbli`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `izin_detilsiup_kbli` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `detilsiup_id` int(11) NOT NULL,
  `kbli_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `detilsiup_id` (`detilsiup_id`,`kbli_id`),
  KEY `izin_detilsiup_kbli_kbli_id_327ab0c8_fk_perusahaan_kbli_id` (`kbli_id`),
  CONSTRAINT `izin_detilsiup_kbli_kbli_id_327ab0c8_fk_perusahaan_kbli_id` FOREIGN KEY (`kbli_id`) REFERENCES `perusahaan_kbli` (`id`),
  CONSTRAINT `izi_detilsiup_id_316b7ce4_fk_izin_detilsiup_pengajuanizin_ptr_id` FOREIGN KEY (`detilsiup_id`) REFERENCES `izin_detilsiup` (`pengajuanizin_ptr_id`)
) ENGINE=InnoDB AUTO_INCREMENT=143 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `izin_detilsiup_kbli`
--

LOCK TABLES `izin_detilsiup_kbli` WRITE;
/*!40000 ALTER TABLE `izin_detilsiup_kbli` DISABLE KEYS */;
INSERT INTO `izin_detilsiup_kbli` VALUES (135,393,1),(136,506,1),(139,520,1),(141,537,1),(142,561,1);
/*!40000 ALTER TABLE `izin_detilsiup_kbli` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `izin_detilsiup_legalitas`
--

DROP TABLE IF EXISTS `izin_detilsiup_legalitas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `izin_detilsiup_legalitas` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `detilsiup_id` int(11) NOT NULL,
  `legalitas_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `detilsiup_id` (`detilsiup_id`,`legalitas_id`),
  KEY `d216e98aee33b02f34a773ba6f887489` (`legalitas_id`),
  CONSTRAINT `d216e98aee33b02f34a773ba6f887489` FOREIGN KEY (`legalitas_id`) REFERENCES `perusahaan_legalitas` (`atributtambahan_ptr_id`),
  CONSTRAINT `izi_detilsiup_id_6ae31e6f_fk_izin_detilsiup_pengajuanizin_ptr_id` FOREIGN KEY (`detilsiup_id`) REFERENCES `izin_detilsiup` (`pengajuanizin_ptr_id`)
) ENGINE=InnoDB AUTO_INCREMENT=144 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `izin_detilsiup_legalitas`
--

LOCK TABLES `izin_detilsiup_legalitas` WRITE;
/*!40000 ALTER TABLE `izin_detilsiup_legalitas` DISABLE KEYS */;
INSERT INTO `izin_detilsiup_legalitas` VALUES (131,393,395),(132,393,396),(133,393,397),(134,393,398),(135,393,399),(136,393,400),(137,393,401),(138,393,402),(139,393,403),(36,415,417),(37,415,418),(38,415,419),(39,415,420),(40,415,421),(41,415,422),(42,415,423),(43,415,424),(44,415,425),(45,415,426),(46,415,427),(47,415,428),(48,415,429),(49,415,430),(50,415,431),(51,415,432),(52,415,433),(53,415,434),(54,415,435),(55,415,436),(56,415,437),(57,415,438),(58,415,439),(59,415,440),(60,415,441),(61,415,442),(62,415,443),(63,415,444),(64,415,445),(65,415,446),(66,415,447),(67,415,448),(68,415,449),(69,415,450),(70,415,451),(71,415,452),(72,415,453),(73,415,454),(74,415,457),(75,415,458),(76,415,459),(77,415,460),(78,415,461),(79,415,462),(80,415,463),(81,415,464),(82,415,465),(83,415,466),(84,415,467),(85,415,468),(86,415,469),(87,415,470),(88,415,471),(89,415,472),(90,415,473),(91,415,474),(92,415,475),(93,415,476),(94,415,477),(140,506,509),(142,537,540),(143,561,564);
/*!40000 ALTER TABLE `izin_detilsiup_legalitas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `izin_detilsiup_produk_utama`
--

DROP TABLE IF EXISTS `izin_detilsiup_produk_utama`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `izin_detilsiup_produk_utama` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `detilsiup_id` int(11) NOT NULL,
  `produkutama_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `detilsiup_id` (`detilsiup_id`,`produkutama_id`)
) ENGINE=InnoDB AUTO_INCREMENT=201 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `izin_detilsiup_produk_utama`
--

LOCK TABLES `izin_detilsiup_produk_utama` WRITE;
/*!40000 ALTER TABLE `izin_detilsiup_produk_utama` DISABLE KEYS */;
INSERT INTO `izin_detilsiup_produk_utama` VALUES (191,393,1),(192,393,3),(193,393,4),(194,506,1),(197,520,2),(199,537,1),(200,561,1);
/*!40000 ALTER TABLE `izin_detilsiup_produk_utama` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `izin_jenisizin`
--

DROP TABLE IF EXISTS `izin_jenisizin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `izin_jenisizin` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nama_izin` varchar(100) NOT NULL,
  `jenis_izin` varchar(20) NOT NULL,
  `keterangan` varchar(255) DEFAULT NULL,
  `kode` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `izin_jenisizin`
--

LOCK TABLES `izin_jenisizin` WRITE;
/*!40000 ALTER TABLE `izin_jenisizin` DISABLE KEYS */;
INSERT INTO `izin_jenisizin` VALUES (1,'IZIN MENDIRIKAN BANGUNAN (IMB)','Izin Daerah','','IMB'),(2,'IZIN GANGGUAN (HO)','Izin Daerah','','HO'),(3,'IZIN REKLAME','Izin Daerah','',NULL),(4,'IZIN PENGGILINGAN PADI, HULLER DAN PENYOSOHAN BERAS','Izin Daerah','',NULL),(5,'IZIN PEMAKAIAN KEKAYAAN DAERAH','Izin Daerah','',NULL),(6,'SURAT IZIN USAHA PERDAGANGAN (SIUP)','Izin Daerah','','SIUP'),(7,'TANDA DAFTAR PERUSAHAAN (TDP)','Izin Daerah','','TDP'),(8,'IZIN PRINSIP PENANAMAN MODAL','Izin Penanaman Modal','',NULL),(9,'IZIN PRINSIP PERLUASAN PENANAMAN MODAL','Izin Penanaman Modal','',NULL),(10,'IZIN PRINSIP PERUBAHAN PENANAMAN MODAL','Izin Penanaman Modal','',NULL),(11,'IZIN USAHA DAN IZIN USAHA PERLUASAN PENANAMAN MODAL','Izin Penanaman Modal','',NULL),(12,'IZIN USAHA PERUBAHAN PENANAMAN MODAL','Izin Daerah','',NULL),(13,'IZIN USAHA PENGGABUNGAN PENANAMAN MODAL','Izin Penanaman Modal','',NULL),(14,'IZIN LOKASI','Izin Daerah','',NULL);
/*!40000 ALTER TABLE `izin_jenisizin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `izin_jenisizin_dasar_hukum`
--

DROP TABLE IF EXISTS `izin_jenisizin_dasar_hukum`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `izin_jenisizin_dasar_hukum` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `jenisizin_id` int(11) NOT NULL,
  `dasarhukum_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `jenisizin_id` (`jenisizin_id`,`dasarhukum_id`)
) ENGINE=InnoDB AUTO_INCREMENT=105 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `izin_jenisizin_dasar_hukum`
--

LOCK TABLES `izin_jenisizin_dasar_hukum` WRITE;
/*!40000 ALTER TABLE `izin_jenisizin_dasar_hukum` DISABLE KEYS */;
INSERT INTO `izin_jenisizin_dasar_hukum` VALUES (87,1,1),(88,1,2),(89,1,3),(90,1,4),(91,1,5),(92,1,6),(93,2,2),(94,2,3),(95,2,5),(96,2,6),(97,2,7),(98,2,9),(66,3,2),(65,3,3),(68,3,5),(67,3,6),(64,3,10),(27,4,2),(26,4,3),(29,4,5),(30,4,6),(28,4,11),(31,5,2),(32,5,3),(33,5,5),(34,5,6),(35,5,12),(36,5,13),(81,6,2),(82,6,3),(83,6,5),(84,6,6),(85,6,14),(86,6,15),(99,7,2),(100,7,3),(101,7,5),(102,7,6),(103,7,15),(104,7,16),(55,8,17),(56,9,17),(57,10,17),(58,11,17),(59,12,17),(60,13,17),(61,14,18),(62,14,19),(63,14,20);
/*!40000 ALTER TABLE `izin_jenisizin_dasar_hukum` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `izin_jenisperaturan`
--

DROP TABLE IF EXISTS `izin_jenisperaturan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `izin_jenisperaturan` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `jenis_peraturan` varchar(100) NOT NULL,
  `keterangan` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `izin_jenisperaturan`
--

LOCK TABLES `izin_jenisperaturan` WRITE;
/*!40000 ALTER TABLE `izin_jenisperaturan` DISABLE KEYS */;
INSERT INTO `izin_jenisperaturan` VALUES (1,'Permen PU RI ',''),(2,'Perda Kabupaten Kediri ',''),(3,'Perbup Kediri ',''),(4,'SK Bupati ',''),(5,'Permendagri RI',''),(8,'Peraturan Daerah Kabupaten Kediri',''),(9,'Peraturan Menteri Perdagangan ',''),(10,'Perka BKPM ',''),(11,'Undang-undang ',''),(12,'Peraturan Menteri Dalam Negeri',''),(13,'Keputusan Kepala Badan Pertanahan Nasional','');
/*!40000 ALTER TABLE `izin_jenisperaturan` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `izin_jenispermohonanizin`
--

DROP TABLE IF EXISTS `izin_jenispermohonanizin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `izin_jenispermohonanizin` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `jenis_permohonan_izin` varchar(255) NOT NULL,
  `keterangan` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `izin_jenispermohonanizin`
--

LOCK TABLES `izin_jenispermohonanizin` WRITE;
/*!40000 ALTER TABLE `izin_jenispermohonanizin` DISABLE KEYS */;
INSERT INTO `izin_jenispermohonanizin` VALUES (1,'Baru/Pendirian',''),(2,'Perpanjangan/Pebaharuan',''),(3,'Perubahan',''),(4,'Pemindahan Tempat Usaha',''),(5,'Perluasan',''),(6,'Penggantian Mesin (Rehabilitasi/ Up-Grading)',''),(7,'Pemindahan Hak Izin Usaha',''),(8,'Pemindahan Hak Kepemilikan','');
/*!40000 ALTER TABLE `izin_jenispermohonanizin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `izin_jenispermohonanizin_jenis_izin`
--

DROP TABLE IF EXISTS `izin_jenispermohonanizin_jenis_izin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `izin_jenispermohonanizin_jenis_izin` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `jenispermohonanizin_id` int(11) NOT NULL,
  `kelompokjenisizin_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `jenispermohonanizin_id` (`jenispermohonanizin_id`,`kelompokjenisizin_id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `izin_jenispermohonanizin_jenis_izin`
--

LOCK TABLES `izin_jenispermohonanizin_jenis_izin` WRITE;
/*!40000 ALTER TABLE `izin_jenispermohonanizin_jenis_izin` DISABLE KEYS */;
INSERT INTO `izin_jenispermohonanizin_jenis_izin` VALUES (14,1,1),(15,1,2),(16,1,17),(17,2,1),(18,2,17),(19,3,1),(20,3,17),(9,4,15),(10,5,15),(11,6,15),(12,7,15),(13,8,15);
/*!40000 ALTER TABLE `izin_jenispermohonanizin_jenis_izin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `izin_kelompokjenisizin`
--

DROP TABLE IF EXISTS `izin_kelompokjenisizin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `izin_kelompokjenisizin` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `jenis_izin_id` int(11) NOT NULL,
  `kelompok_jenis_izin` varchar(100) NOT NULL,
  `biaya` decimal(10,2) NOT NULL,
  `standart_waktu` smallint(5) unsigned DEFAULT NULL,
  `keterangan` varchar(255) DEFAULT NULL,
  `kode` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `izin_kelompokjenisizin`
--

LOCK TABLES `izin_kelompokjenisizin` WRITE;
/*!40000 ALTER TABLE `izin_kelompokjenisizin` DISABLE KEYS */;
INSERT INTO `izin_kelompokjenisizin` VALUES (1,1,'Izin Mendirikan Bangunan (IMB) Bupati',0.00,7,'',NULL),(2,1,'Izin Mendirikan Bangunan (IMB) Umum',0.00,7,'',NULL),(11,1,'Izin Mendirikan Bangunan (IMB) Perumahan',0.00,NULL,'',NULL),(12,2,'Izin Gangguan  (HO) PERMOHONAN BARU',0.00,7,'',NULL),(13,2,'Izin Gangguan  (HO) DAFTAR ULANG',0.00,7,'',NULL),(14,3,'Izin Reklame',0.00,7,'',NULL),(15,4,'Izin Penggilingan Padi, Huller dan Penyosohan Beras',0.00,1,'',NULL),(16,5,'Izin Pemakaian Kekayaan Daerah',0.00,14,'',NULL),(17,6,'SIUP',0.00,7,'','503.08/'),(25,7,'TDP PERMOHONAN BARU ( TDP PT )',0.00,14,'',NULL),(26,7,'TDP PERMOHONAN BARU ( TDP CV  )',0.00,14,'',NULL),(27,7,'TDP PERMOHONAN BARU (TDP Firma)',0.00,14,'',NULL),(28,7,'TDP PERMOHONAN BARU ( TDP Perorangan )',0.00,14,'',NULL),(29,7,'TDP PERMOHONAN BARU ( TDP Koperasi  )',0.00,14,'',NULL),(30,7,'TDP PERMOHONAN BARU ( TDP BUL   )',0.00,14,'',NULL),(31,7,'TDP PERMOHONAN BARU (TDP Kantor Cabang, Kantor Pembantu dan Perwakilan Perusahaan )',0.00,14,'',NULL),(32,7,'(TDP) PERMOHONAN PENDAFTARAN ULANG',0.00,14,'',NULL),(33,8,'Izin Penanaman modal',0.00,3,'',NULL),(35,9,'Izin Prinsip Perluasan Penanaman Modal',0.00,3,'',NULL);
/*!40000 ALTER TABLE `izin_kelompokjenisizin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `izin_pemohon`
--

DROP TABLE IF EXISTS `izin_pemohon`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `izin_pemohon` (
  `account_ptr_id` int(11) NOT NULL,
  `jenis_pemohon_id` int(11) NOT NULL,
  `jabatan_pemohon` varchar(255) DEFAULT NULL,
  `berkas_npwp_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`account_ptr_id`),
  KEY `izin_pemohon_fae0bfe7` (`berkas_npwp_id`),
  CONSTRAINT `berkas_npwp_id_62cc38ca_fk_master_berkas_atributtambahan_ptr_id` FOREIGN KEY (`berkas_npwp_id`) REFERENCES `master_berkas` (`atributtambahan_ptr_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `izin_pemohon`
--

LOCK TABLES `izin_pemohon` WRITE;
/*!40000 ALTER TABLE `izin_pemohon` DISABLE KEYS */;
INSERT INTO `izin_pemohon` VALUES (30,1,NULL,NULL),(35,1,NULL,NULL),(36,1,NULL,NULL),(392,1,NULL,407),(414,1,NULL,NULL),(502,1,NULL,NULL),(505,1,NULL,512),(533,1,NULL,543),(557,1,NULL,567),(580,1,NULL,NULL);
/*!40000 ALTER TABLE `izin_pemohon` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `izin_pemohon_berkas_foto`
--

DROP TABLE IF EXISTS `izin_pemohon_berkas_foto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `izin_pemohon_berkas_foto` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `pemohon_id` int(11) NOT NULL,
  `berkas_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `pemohon_id` (`pemohon_id`,`berkas_id`),
  KEY `izin__berkas_id_485371bd_fk_master_berkas_atributtambahan_ptr_id` (`berkas_id`),
  CONSTRAINT `izin_pemohon__pemohon_id_34c172f2_fk_izin_pemohon_account_ptr_id` FOREIGN KEY (`pemohon_id`) REFERENCES `izin_pemohon` (`account_ptr_id`),
  CONSTRAINT `izin__berkas_id_485371bd_fk_master_berkas_atributtambahan_ptr_id` FOREIGN KEY (`berkas_id`) REFERENCES `master_berkas` (`atributtambahan_ptr_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `izin_pemohon_berkas_foto`
--

LOCK TABLES `izin_pemohon_berkas_foto` WRITE;
/*!40000 ALTER TABLE `izin_pemohon_berkas_foto` DISABLE KEYS */;
INSERT INTO `izin_pemohon_berkas_foto` VALUES (6,392,406),(7,392,410),(8,505,510),(9,533,541),(10,557,565);
/*!40000 ALTER TABLE `izin_pemohon_berkas_foto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `izin_pengajuanizin`
--

DROP TABLE IF EXISTS `izin_pengajuanizin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `izin_pengajuanizin` (
  `izin_induk_id` int(11) DEFAULT NULL,
  `pemohon_id` int(11) DEFAULT NULL,
  `kelompok_jenis_izin_id` int(11) NOT NULL,
  `jenis_permohonan_id` int(11) NOT NULL,
  `status` smallint(5) unsigned NOT NULL,
  `verified_by_id` int(11) DEFAULT NULL,
  `verified_at` datetime DEFAULT NULL,
  `rejected_by_id` int(11) DEFAULT NULL,
  `rejected_at` datetime DEFAULT NULL,
  `updated_at` datetime NOT NULL,
  `nama_kuasa` varchar(255) DEFAULT NULL,
  `no_identitas_kuasa` varchar(255) DEFAULT NULL,
  `no_izin` varchar(255) DEFAULT NULL,
  `no_pengajuan` varchar(255) DEFAULT NULL,
  `telephone_kuasa` varchar(255) DEFAULT NULL,
  `atributtambahan_ptr_id` int(11) NOT NULL,
  `keterangan` varchar(255),
  PRIMARY KEY (`atributtambahan_ptr_id`),
  UNIQUE KEY `izin_pengajuanizin_no_izin_261d6f3e_uniq` (`no_izin`),
  UNIQUE KEY `izin_pengajuanizin_no_pengajuan_4987a69e_uniq` (`no_pengajuan`),
  CONSTRAINT `izin__atributtambahan_ptr_id_b14aa7_fk_master_atributtambahan_id` FOREIGN KEY (`atributtambahan_ptr_id`) REFERENCES `master_atributtambahan` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `izin_pengajuanizin`
--

LOCK TABLES `izin_pengajuanizin` WRITE;
/*!40000 ALTER TABLE `izin_pengajuanizin` DISABLE KEYS */;
INSERT INTO `izin_pengajuanizin` VALUES (NULL,392,17,1,0,NULL,NULL,NULL,NULL,'0000-00-00 00:00:00','','','123/2123.12016','SIUP/0870/1004/2016','',393,''),(NULL,414,17,1,0,NULL,NULL,NULL,NULL,'0000-00-00 00:00:00',NULL,NULL,NULL,'SIUP/7880/1004/2016',NULL,415,NULL),(NULL,392,17,1,0,NULL,NULL,NULL,NULL,'0000-00-00 00:00:00',NULL,NULL,NULL,'SIUP/0730/1005/2016',NULL,497,NULL),(NULL,392,17,1,0,NULL,NULL,NULL,NULL,'0000-00-00 00:00:00',NULL,NULL,NULL,'SIUP/8000/1005/2016',NULL,500,NULL),(NULL,502,17,1,0,NULL,NULL,NULL,NULL,'0000-00-00 00:00:00',NULL,NULL,NULL,'SIUP/5050/1006/2016',NULL,503,NULL),(NULL,505,17,1,0,NULL,NULL,NULL,NULL,'0000-00-00 00:00:00',NULL,NULL,'123/7/123.1/2016','SIUP/3650/1006/2016',NULL,506,NULL),(NULL,392,17,1,0,NULL,NULL,NULL,NULL,'0000-00-00 00:00:00','','','','SIUP/7140/1006/2016','',520,''),(NULL,533,17,1,0,NULL,NULL,NULL,NULL,'0000-00-00 00:00:00',NULL,NULL,NULL,'SIUP/4400/1006/2016',NULL,534,NULL),(NULL,533,17,1,0,NULL,NULL,NULL,NULL,'0000-00-00 00:00:00','deny','123456','123/9/123.1/2016','SIUP/7480/1006/2016','09182992838',537,''),(NULL,557,17,2,0,NULL,NULL,NULL,NULL,'0000-00-00 00:00:00',NULL,NULL,NULL,'SIUP/9470/1006/2016',NULL,558,NULL),(NULL,557,17,2,0,NULL,NULL,NULL,NULL,'0000-00-00 00:00:00',NULL,NULL,'503.08/13/418.71/2016','SIUP/3240/1006/2016',NULL,561,NULL),(NULL,580,17,2,0,NULL,NULL,NULL,NULL,'0000-00-00 00:00:00',NULL,NULL,NULL,'SIUP/7740/1006/2016',NULL,581,NULL),(NULL,580,17,2,0,NULL,NULL,NULL,NULL,'0000-00-00 00:00:00',NULL,NULL,NULL,'SIUP/7720/1006/2016',NULL,584,NULL);
/*!40000 ALTER TABLE `izin_pengajuanizin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `izin_pengajuanizin_berkas_tambahan`
--

DROP TABLE IF EXISTS `izin_pengajuanizin_berkas_tambahan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `izin_pengajuanizin_berkas_tambahan` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `pengajuanizin_id` int(11) NOT NULL,
  `berkas_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `pengajuanizin_id` (`pengajuanizin_id`,`berkas_id`),
  KEY `izin__berkas_id_64aba680_fk_master_berkas_atributtambahan_ptr_id` (`berkas_id`),
  CONSTRAINT `bde3bf5fea02f5f927caca95834b46ee` FOREIGN KEY (`pengajuanizin_id`) REFERENCES `izin_pengajuanizin` (`atributtambahan_ptr_id`),
  CONSTRAINT `izin__berkas_id_64aba680_fk_master_berkas_atributtambahan_ptr_id` FOREIGN KEY (`berkas_id`) REFERENCES `master_berkas` (`atributtambahan_ptr_id`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `izin_pengajuanizin_berkas_tambahan`
--

LOCK TABLES `izin_pengajuanizin_berkas_tambahan` WRITE;
/*!40000 ALTER TABLE `izin_pengajuanizin_berkas_tambahan` DISABLE KEYS */;
INSERT INTO `izin_pengajuanizin_berkas_tambahan` VALUES (24,393,404),(25,506,515),(27,537,546),(28,561,570);
/*!40000 ALTER TABLE `izin_pengajuanizin_berkas_tambahan` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `izin_prosedur`
--

DROP TABLE IF EXISTS `izin_prosedur`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `izin_prosedur` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `jenis_izin_id` int(11) NOT NULL,
  `nomor_urut` int(11) DEFAULT NULL,
  `prosedur` varchar(255) NOT NULL,
  `lama` smallint(5) unsigned DEFAULT NULL,
  `keterangan` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=122 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `izin_prosedur`
--

LOCK TABLES `izin_prosedur` WRITE;
/*!40000 ALTER TABLE `izin_prosedur` DISABLE KEYS */;
INSERT INTO `izin_prosedur` VALUES (1,2,1,'Menyerahkan berkas permohonan',1,''),(2,2,2,'Berkas permohonan yang dinyatakan lengkap dan memenuhi syarat dapat diterima dan diberikan tanda terima permohonan perizinan',1,''),(3,2,3,'Cek lokasi',1,''),(4,2,4,'Pengetikan Surat Keputusan (SK)',1,''),(5,2,5,'Penandatanganan Surat Keputusan (SK)',1,''),(6,2,6,'Pembayaran Retribusi',1,''),(7,2,7,'Penyerahan SK Izin ke pemohon',1,''),(8,12,1,'Formulir isian lengkap dan benar beserta semua kelengkapanya di terima di KPPT dan di hitung perkiraan besarnya retribusi selanjutnya di berikan tanda terima. Berkas lengkap dan benar di catat dan di register',1,''),(9,12,2,'Berkas di teliti dan di verifikasi yang selanjutnya persetujuan pimpinan',1,''),(10,12,3,'Dijadwalkan tinjau lokasi oleh tim pemberi pertimbangan perizinan. Ditetapkan dan dibuatkan undangan tinjau lokasi. Pemberitahuan kepada pemohon izin rencana pelaksanaan tinjau lokasi. Hasil tinjau likasi dirapatkan dan dituangkan dalam berita ac',1,''),(11,12,4,'Proses pengetikan surat izin',1,''),(12,12,5,'Penandatanganan pencatat dan penomoran surat izin',1,''),(13,12,6,'Surat izin siap diberikan kepada pemohon diserahkan kepada bendahara penerimaan, di beritahukan untuk pembayaran retribusi dan pengambilan surat izin.',1,''),(14,14,1,'Formulir isian lengkap dan benar beserta semua kelengkapanya diterima di KPPT dan dibuatkan tanda terima.',1,''),(15,14,2,'Berkas diteliti dan diverifikasi yang selanjudnya persetujuan pimpinan',1,''),(16,14,3,'Untuk reklame insidentil : Proses dan pengetikan surat izin, bagi pemasangan reklame insidentil. Penandatanganan, pencatatan dan penomoran surat izin. Penyerahan surat izin kepada pemohon (1 hari kerja ).',1,''),(17,14,4,'Untuk pemasangan reklame, papan bertiang di jadwalkan tinjau lokasi oleh tim pemberi pertimbangan perizinan. ditetapkan dan dibuatkan   undangan tinjau lokasi. Pemberitahuan kepada pemohon izin rencana pelaksanaan tinjau lokasi. ',1,''),(18,15,1,'Formulir isian lengkap dan benar beserta semua kelengkapanya di terima di KPPT, selanjutnya di buatkan tanda terima. Berkas lengkap dan benar di catat dan di register ( 1 hari kerja ).',1,''),(19,15,2,'Berkas di teliti dan di verifikasi yang selanjutnya persetujuan pimpinan ( 1 hari kerja ).',1,''),(20,15,3,'Proses dan pengetikan surat izin ( 1 hari kerja ).',1,''),(21,15,4,'Penandatanganan, pencatatan, dan penomoran surat izin ( 1 hari kerja ).',1,''),(22,15,5,'Pemberitahuan kepada pemohon untuk pengambilannya ( 1 hari kerja ).',1,''),(23,16,1,'Formulir isian lengkap dan benar beserta semua kelengkapanya diterima di KPPT. Dan di hitung perkiraan besarnya retribusi, selanjutnya dibuatkan tanda terima berkas lengkap dan dicatat dan di register ( 1 hari kerja ).',1,''),(24,16,2,'berkas di teliti dan di verifikasi yang selanjutnya persetujuan pimpinan  (1 hari kerja ).',1,''),(25,16,3,'Dibuatkan nota dinas kepada bupati untuk permohonan persetujuan penerbitan izin (1 hari kerja ).',1,''),(26,16,4,'Permohonan persetujuan penerbitan izin kepada bupati.',1,''),(27,16,5,'Proses dan pengetikan surat izin (1 hari kerja ).',1,''),(28,16,6,'Penandatanganan surat izin, pencatatan, dan penomoran surat izin  (1 hari kerja ).',1,''),(29,16,7,'Pemberitahuan kepada pemohon izin untuk membayar retribusi sebelum retribusi di ambil ( 1 hari kerja )',1,''),(30,16,7,'Penyerahan surat izin kepada pemohon (1 hari kerja )',1,''),(31,17,1,'Menyerahkan berkas permohonan ',1,''),(32,17,2,'Berkas permohonan yang dinyatakan lengkap dan memenuhi syarat dapat diterima dan diberikan tanda terima permohonan perizinan',1,''),(33,17,3,'Cek Lokasi (untuk Perdagangan Besar)',1,''),(34,17,4,'Pengajuan persetujuan  Izin kepada Bupati',1,''),(35,17,5,'Penandatanganan Surat Izin',1,''),(36,17,6,'Penyerahan Surat Izin ke pemohon',1,''),(73,25,1,'Menyerahkan berkas permohonan',1,''),(74,25,2,'Berkas permohonan yang dinyatakan lengkap dan memenuhi syarat dapat diterima dan diberikan tanda terima permohonan perizinan',1,''),(75,25,3,'Cek Lokasi (untuk Perdagangan Besar)',1,''),(76,25,4,'Pengajuan persetujuan Izin kepada Bupati',1,''),(77,25,5,'Penandatanganan Surat Izin',1,''),(78,25,6,'Penyerahan Surat Izin ke prmohon',1,''),(79,26,1,'Menyerahkan berkas permohonan',1,''),(80,26,2,'Berkas permohonan yang dinyatakan lengkap dan memenuhi syarat dapat diterima dan diberikan tanda terima permohonan perizinan',1,''),(81,26,3,'Cek Lokasi (untuk Perdagangan Besar)',1,''),(82,26,4,'Pengajuan persetujuan Izin kepada Bupati',1,''),(83,26,5,'Penandatanganan Surat Izin',1,''),(84,26,6,'Penyerahan Surat Izin ke prmohon',1,''),(85,27,1,'Menyerahkan berkas permohonan',1,''),(86,27,2,'Berkas permohonan yang dinyatakan lengkap dan memenuhi syarat dapat diterima dan diberikan tanda terima permohonan perizinan',1,''),(87,27,3,'Cek Lokasi (untuk Perdagangan Besar)',1,''),(88,27,4,'Pengajuan persetujuan Izin kepada Bupati',1,''),(89,27,6,'Penyerahan Surat Izin ke prmohon',1,''),(90,29,1,'Menyerahkan berkas permohonan',NULL,''),(91,29,2,'Berkas permohonan yang dinyatakan lengkap dan memenuhi syarat dapat diterima dan diberikan tanda terima permohonan perizinan',1,''),(92,29,3,'Cek Lokasi (untuk Perdagangan Besar)',1,''),(93,29,4,'Pengajuan persetujuan Izin kepada Bupat',1,''),(94,29,5,'Penandatanganan Surat Izin',1,''),(95,29,6,'Penyerahan Surat Izin ke prmohon',1,''),(96,30,1,'Menyerahkan berkas permohonan',1,''),(97,30,2,'Berkas permohonan yang dinyatakan lengkap dan memenuhi syarat dapat diterima dan diberikan tanda terima permohonan perizinan',1,''),(98,30,3,'Cek Lokasi (untuk Perdagangan Besar)',1,''),(99,30,4,'Pengajuan persetujuan Izin kepada Bupati',1,''),(100,30,5,'Penandatanganan Surat Izin',1,''),(101,30,6,'Penyerahan Surat Izin ke prmohon',1,''),(102,31,1,'Menyerahkan berkas permohonan',NULL,''),(103,31,2,'Berkas permohonan yang dinyatakan lengkap dan memenuhi syarat dapat diterima dan diberikan tanda terima permohonan perizinan',1,''),(104,31,3,'Cek Lokasi (untuk Perdagangan Besar)',1,''),(105,31,4,'Pengajuan persetujuan Izin kepada Bupati',1,''),(106,31,5,'Penandatanganan Surat Izin',1,''),(107,31,6,'Penyerahan Surat Izin ke prmohon',1,''),(108,32,1,'Menyerahkan berkas permohonan',1,''),(109,32,2,'Berkas permohonan yang dinyatakan lengkap dan memenuhi syarat dapat diterima dan diberikan tanda terima permohonan perizinan',1,''),(110,32,3,'Pengajuan persetujuan  Izin kepada Bupati',1,''),(111,32,4,'Penandatanganan Surat Izin',1,''),(112,32,5,'Penyerahan Surat Izin ke pemohon',1,''),(113,33,1,'Pemohon mencari informasi pada loket informasi perizinan',1,''),(114,33,2,'Pemohon mengisi formulir permohonan dengan dilengkapi semua persyaratan yang telah ditetapkan',1,''),(115,33,3,'Pemohon mengajukan formulir permohonan dan persyaratan ke loket pendaftaran',1,''),(116,33,4,'Petugas di loket pendaftaran melakukan pemeriksaan berkas permohonan dan kelengkapan persyaratan.',1,''),(117,33,5,'Pembahasan dan pemeriksaan lapangan, untuk menetapkan apakah permohonan izin disetujui atau tidak.',1,''),(118,33,6,'Naskah perizinan diterbitkan dan ditanda tangani ',1,''),(119,33,7,'Pemohon menerima informasi bahwa surat izin selesai',1,''),(120,33,8,'Pemohon mengambil surat izin',1,''),(121,33,9,'Petugas loket pengambilan menyerahkan tanda terima dan surat izin',1,'');
/*!40000 ALTER TABLE `izin_prosedur` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `izin_riwayat`
--

DROP TABLE IF EXISTS `izin_riwayat`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `izin_riwayat` (
  `atributtambahan_ptr_id` int(11) NOT NULL,
  `keterangan` varchar(255) DEFAULT NULL,
  `pengajuan_izin_id` int(11),
  `sk_izin_id` int(11),
  PRIMARY KEY (`atributtambahan_ptr_id`),
  KEY `izin_riwayat_dc91ce56` (`pengajuan_izin_id`),
  KEY `izin_riwayat_e2c0f37b` (`sk_izin_id`),
  CONSTRAINT `D24daa4aca8c14f18d9328912fb6c629` FOREIGN KEY (`pengajuan_izin_id`) REFERENCES `izin_pengajuanizin` (`atributtambahan_ptr_id`),
  CONSTRAINT `izin_ri_sk_izin_id_aa50f96_fk_izin_skizin_atributtambahan_ptr_id` FOREIGN KEY (`sk_izin_id`) REFERENCES `izin_skizin` (`atributtambahan_ptr_id`),
  CONSTRAINT `izi_atributtambahan_ptr_id_2d7b9f3f_fk_master_atributtambahan_id` FOREIGN KEY (`atributtambahan_ptr_id`) REFERENCES `master_atributtambahan` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `izin_riwayat`
--

LOCK TABLES `izin_riwayat` WRITE;
/*!40000 ALTER TABLE `izin_riwayat` DISABLE KEYS */;
INSERT INTO `izin_riwayat` VALUES (412,'Draf (Pengajuan)',393,NULL),(416,'Draf (Pengajuan)',415,NULL),(478,'Submitted (Pengajuan)',393,NULL),(479,'Submitted (Pengajuan)',393,NULL),(480,'Submitted (Pengajuan)',393,NULL),(481,'Submitted (Pengajuan)',393,NULL),(483,'Submitted (Pengajuan)',393,NULL),(484,'Submitted (Pengajuan)',393,NULL),(485,'Kabid Verified (Pengajuan)',393,NULL),(487,'Draf (Izin)',393,486),(488,'Kabid Verified (Izin)',393,486),(489,'Kadin Verified (Izin)',393,486),(490,'Registered (Izin)',393,486),(491,'Registered (Izin)',393,486),(492,'Registered (Izin)',393,486),(493,'Printed (Izin)',393,486),(494,'Printed (Izin)',393,486),(495,'Finished (Izin)',393,486),(498,'Draf (Pengajuan)',497,NULL),(501,'Draf (Pengajuan)',500,NULL),(504,'Draf (Pengajuan)',503,NULL),(507,'Draf (Pengajuan)',506,NULL),(516,'Submitted (Pengajuan)',506,NULL),(517,'Submitted (Pengajuan)',506,NULL),(518,'Kabid Verified (Pengajuan)',506,NULL),(521,'Draf (Pengajuan)',520,NULL),(524,'Draf (Izin)',506,523),(525,'Kabid Verified (Izin)',506,523),(526,'Kadin Verified (Izin)',506,523),(527,'Registered (Izin)',506,523),(528,'Printed (Izin)',506,523),(529,'Printed (Izin)',506,523),(530,'Printed (Izin)',506,523),(531,'Printed (Izin)',506,523),(532,'Finished (Izin)',506,523),(535,'Draf (Pengajuan)',534,NULL),(538,'Draf (Pengajuan)',537,NULL),(547,'Submitted (Pengajuan)',537,NULL),(548,'Kabid Verified (Pengajuan)',537,NULL),(549,'Kabid Verified (Pengajuan)',537,NULL),(551,'Draf (Izin)',537,550),(552,'Kabid Verified (Izin)',537,550),(553,'Kadin Verified (Izin)',537,550),(554,'Registered (Izin)',537,550),(555,'Printed (Izin)',537,550),(556,'Finished (Izin)',537,550),(559,'Draf (Pengajuan)',558,NULL),(562,'Draf (Pengajuan)',561,NULL),(571,'Submitted (Pengajuan)',561,NULL),(572,'Kabid Verified (Pengajuan)',561,NULL),(573,'Kabid Verified (Pengajuan)',561,NULL),(575,'Draf (Izin)',561,574),(576,'Kabid Verified (Izin)',561,574),(577,'Kadin Verified (Izin)',561,574),(578,'Registered (Izin)',561,574),(579,'Printed (Izin)',561,574),(582,'Draf (Pengajuan)',581,NULL),(585,'Draf (Pengajuan)',584,NULL),(586,'Registered (Izin)',561,574),(587,'Registered (Izin)',561,574);
/*!40000 ALTER TABLE `izin_riwayat` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `izin_skizin`
--

DROP TABLE IF EXISTS `izin_skizin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `izin_skizin` (
  `atributtambahan_ptr_id` int(11) NOT NULL,
  `isi` longtext,
  `keterangan` varchar(255) DEFAULT NULL,
  `berkas_id` int(11) DEFAULT NULL,
  `pengajuan_izin_id` int(11) NOT NULL,
  PRIMARY KEY (`atributtambahan_ptr_id`),
  KEY `izin__berkas_id_351a0110_fk_master_berkas_atributtambahan_ptr_id` (`berkas_id`),
  KEY `izin_skizin_dc91ce56` (`pengajuan_izin_id`),
  CONSTRAINT `D1ad642f09d70b209c4e9101e640f082` FOREIGN KEY (`pengajuan_izin_id`) REFERENCES `izin_pengajuanizin` (`atributtambahan_ptr_id`),
  CONSTRAINT `izin__berkas_id_351a0110_fk_master_berkas_atributtambahan_ptr_id` FOREIGN KEY (`berkas_id`) REFERENCES `master_berkas` (`atributtambahan_ptr_id`),
  CONSTRAINT `izi_atributtambahan_ptr_id_7f2b3763_fk_master_atributtambahan_id` FOREIGN KEY (`atributtambahan_ptr_id`) REFERENCES `master_atributtambahan` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `izin_skizin`
--

LOCK TABLES `izin_skizin` WRITE;
/*!40000 ALTER TABLE `izin_skizin` DISABLE KEYS */;
INSERT INTO `izin_skizin` VALUES (486,'','',NULL,393),(523,'','',NULL,506),(550,NULL,NULL,NULL,537),(574,'','',NULL,561);
/*!40000 ALTER TABLE `izin_skizin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `izin_syarat`
--

DROP TABLE IF EXISTS `izin_syarat`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `izin_syarat` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `jenis_izin_id` int(11) NOT NULL,
  `syarat` varchar(255) NOT NULL,
  `keterangan` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=148 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `izin_syarat`
--

LOCK TABLES `izin_syarat` WRITE;
/*!40000 ALTER TABLE `izin_syarat` DISABLE KEYS */;
INSERT INTO `izin_syarat` VALUES (1,2,'Mengisi formulir permohonan IMB lengkap dan benar diketahui oleh Kepala Desa/Lurah dan Camat',''),(2,2,'Fotokopi Surat Kepemilikan Tanah atau Surat Penguasaan Hak atas Tanah (Sertifikat / Akte Jual Beli / Petok D / Surat Keterangan Status Tanah)',''),(3,2,'Fotokopi KTP / Identitas',''),(4,2,'Fotokopi NPWP',''),(5,2,'Rencana Teknis Bangunan Gedung (Denah Bangunan, Site Plan, Spesifikasi Teknis) yang disahkan oleh Instansi Teknis yang membidangi',''),(6,1,'Surat Persetujuan/Perjanjian/Izin Pemilik tanah untuk bangunan yang didirikan di atas tanah yang bukan miliknya',''),(7,2,'Surat Persetujuan/Rekomendasi dari FKUB (Forum Komunikasi Umat Beragama) bagi bangunan fungsi keagamaan',''),(8,2,'Rekomendasi dari Instansi Teknis sesuai kegiatan/bangunan yang dimohonkan.',''),(10,12,'Formulir Permohonan Izin',''),(11,12,'Pernyataan Persetujuan Lingkungan',''),(12,12,'Pakta Integritas',''),(13,12,'Foto copy IMB sesuai peruntukanya',''),(14,12,'Foto copy surat kepemilikan tanah / surat penguasaan hak atas tanah (sertifikat/akte jual beli/petok D/surat keterangan status tanah)',''),(15,12,'Rencana Teknis bangunan gedung (denah bangunan, site plan, spefikasi teknis) yang disahkan oleh instansi teknis yang membidangi',''),(16,12,'Foto copy KTP pemohon / penanggung jawab usaha',''),(17,12,'Foto copy NPWP perusahaan / penanggung jawab usaha.',''),(18,12,'Surat kuasa bagi yang mewakili perusahaan/badan hukum',''),(19,12,'SPPL / dokumen UKL-UPL / AMDAL',''),(20,13,'Fotocopy Izin Gangguan yang lama/induk',''),(21,13,'Fotocopy KTP/Identitas',''),(22,13,'Fotocopy NPWP pribadi dan/atau perusahaan',''),(23,13,'Surat keterangan (jika ada perubahan)',''),(24,14,'Gambar konstruksi, foto dan denah lokasi pemasangan reklame.',''),(25,14,'Rekomendasi dari satpol PP atau Berita acara pemeriksaan tim pemberi pertimbangan perizinan bagi reklame permanen bertiang.',''),(26,14,'Surat perjanjian kesepakatan dengan pemilik rumah, tembok, pagar, atau pakarangan bagi reklame tempel atau melekat.',''),(27,14,'Surat keterangan tidak keberatan dari pemilik lahan yang ditempati reklame.',''),(28,14,'Surat pernyataan kesanggupan mengganti rugi.',''),(29,15,'Formulir isian.',''),(30,15,'Foto copy KTP',''),(31,15,'Foto copy IMB.',''),(32,15,'Foto copy izin gangguan. ',''),(33,15,'Foto ukuran 4 x 6 ( 2 lembar ).',''),(34,15,'Rekomendasi teknis dari dinas Pertanian.',''),(35,16,'Formulir isian disetujui / diketahui kepala desa / lurah dan camat setempat',''),(36,16,'Foto copy KTP',''),(37,16,'Rekomendasi persetujuan instansi pengelola',''),(38,17,'Mengisi formulir permohonan',''),(39,17,'Fc. Akta notaris pendirian perusahaan',''),(40,17,'Fc. Akta perubahan perusahaan (apabila ada)',''),(41,17,'Fc. Surat keputusan pengesahan badan hukum Perseroan Terbatas dari Departemen hukum dan hak asasi manusia',''),(42,17,'Fc. KTP dari pemilik/ penanggungjawab/ pengurus/ direktur utama perusahaan',''),(43,17,'Fc. NPWP Perusahaan',''),(44,17,'Fc. Izin usaha/teknis atau surat keterangan yang dipersamakan',''),(45,17,'Surat pernyataan dari pemohon SIUP tentang lokasi usaha perusahaan',''),(46,17,'Foto penanggungjawab atau direktur utama perusahaan ukuran 3x4 atau 4x6 sebanyak 3 lembar',''),(84,25,'Foto Copy Akta Pendirian Perseroan',''),(85,25,'Foto Copy Akta Perubahan Perseroan (Apabila Ada)',''),(86,25,'Foto Copy Surat Keputusan Pengesahan Badan Hukum Dari Departemen Hukum Dari Menteri Kehakiman Dan Hak Asasi Manusia',''),(87,25,'Foto Copy KTP/ Paspor (Dirut/pemilik/ pengurus/ penanggung jawab)',''),(88,25,'Foto Copy Ijin Usaha/ Ijin Teknis atau Surat Keterangan yang dipersamakan',''),(89,25,'Foto Copy Nomor Wajib Pajak (NPWP) Perusahaan',''),(90,25,'Sertifikat Asli TDP (bagi yang Daftar Ulang)',''),(91,25,'Materai Rp. 6000,- 1 lembar',''),(92,26,'Foto Copy Akta Pendirian Perseroan',''),(93,26,'Foto Copy Akta Perubahan Perseroan (Apabila Ada)',''),(94,26,'Foto Copy KTP/ Paspor (Dirut/pemilik/ pengurus/ penanggung jawab)',''),(95,26,'Foto Copy Ijin Usaha/ Ijin Teknis atau Surat Keterangan yang dipersamakan',''),(96,26,'Neraca Perusahaan',''),(97,26,'Foto Copy Nomor Wajib Pajak (NPWP) Perusahaan',''),(98,26,'Sertifikat Asli TDP (bagi yang Daftar Ulang)',''),(99,26,'Materai Rp. 6000,- 1 lembar',''),(100,27,'Foto Copy Akta Pendirian Perseroan',''),(101,27,'Foto Copy Akta Perubahan Perseroan (Apabila Ada)',''),(102,27,'Foto Copy KTP/ Paspor (Dirut/pemilik/ pengurus/ penanggung jawab)',''),(103,27,'Foto Copy Ijin Usaha/ Ijin Teknis atau Surat Keterangan yang dipersamakan',''),(104,27,'Neraca Perusahaan',''),(105,27,'Foto Copy Nomor Wajib Pajak (NPWP) Perusahaan',''),(106,27,'Sertifikat Asli TDP (bagi yang Daftar Ulang)',''),(107,27,'Materai Rp. 6000,- 1 lembar',''),(108,28,'Foto Copy KTP/ Paspor (Pemilik/ Pengurus/ penanggung jawab)',''),(109,28,'Foto Copy Ijin Usaha/ Ijin Teknis atau Surat Keterangan yang dipersamakan',''),(110,28,'Foto Copy Nomor Wajib Pajak (NPWP ) Pribadi',''),(111,28,'Materai Rp. 6000,- 1 lembar',''),(112,29,'Foto Copy Akta Pendirian Koperasi yang telah mendapatkan Pengesahan',''),(113,29,'Foto Copy Akta Perubahan Perseroan (Apabila Ada)',''),(114,29,'Foto Copy KTP (Ketua / penanggung jawab)',''),(115,29,'Foto Copy Ijin Usaha/ Ijin Teknis atau Surat Keterangan yang dipersamakan',''),(116,29,'Neraca Koperasi',''),(117,29,'Susunan Pengurus yang telah mendapatkan Pengesahan',''),(118,29,'Foto Copy Nomor Wajib Pajak (NPWP) Koperasi',''),(119,29,'Sertifikat Asli TDP ',''),(120,29,'Materai Rp. 6000,- 1 lembar',''),(121,29,'Foto Copy Nomor Wajib Pajak (NPWP) Koperasi',''),(122,29,'Sertifikat Asli TDP ',''),(123,29,'Materai Rp. 6000,- 1 lembar',''),(124,30,'Foto Copy Akta Pendirian Perseroan',''),(125,30,'Foto Copy KTP/ Paspor (Dirut/pemilik/ pengurus/ penanggung jawab)',''),(126,30,'Foto Copy Ijin Usaha/ Ijin Teknis atau Surat Keterangan yang dipersamakan',''),(127,30,'Foto Copy Nomor Wajib Pajak (NPWP) Perusahaan',''),(128,30,'Sertifikat Asli TDP (bagi yang Daftar Ulang)',''),(129,30,'Materai Rp. 6000,- 1 lembar',''),(130,31,'Mengisi form permohonan',''),(131,31,'Fc. Akta pendirian perusahaan (apabila ada) atau surat penunjukan atau surat yang dipersamakan sebagai Kantor Cabang, Kantor Pembantu dan Perwakilan',''),(132,31,'Daftar susunan pengurus perusahaan',''),(133,31,'Fc. KTP pemilik atau / paspor pengurus atau penanggungjawab',''),(134,31,'Fc. Izin   usaha   atau surat keterangan yang  dipersamakan/diterbitkan oleh instansi yang berwenang atau Kantor pusat   perusahaan ',''),(135,31,'Fc. NPWP',''),(136,32,'Dokumen-dokumen dan kelengkapan permohonan TDP (sama dengan permohonan TDP baru)',''),(137,32,'TDP Asli',''),(138,32,'Neraca Perusahaan (tahun terakhir khusus untuk PT)',''),(139,33,'Mengisi formulir permohonan ',''),(140,33,'Foto copy Pendaftaran bagi badan usaha yang telah melakukan pendaftaran',''),(141,33,'Foto copy akta pendirian perusahaan dan perubahannya',''),(142,33,'Foto copy pengesahan anggaran dasar perusahaan dari Menteri Hukum dan HAM',''),(143,33,'Foto copy Nomor Pokok Wajib Pajak (NPWP).',''),(144,33,'Keterangan rencana kegiatan, berupa uraian proses produksi yang mencantumkan jenis bahan baku dan dilengkapi dengan diagram alir',''),(145,33,'Uraian kegiatan usaha sektor jasa.',''),(146,33,'Rekomendasi dari instansi pemerintah terkait, bila dipersyaratkan',''),(147,33,'Permohonan ditandatangani diatas materai cukup oleh direksi perusahaan dilengkapi surat kuasa bermaterai cukup untuk pengurusan permohonan yang tidak dilakukan secara langsung oleh direksi perusahaan','');
/*!40000 ALTER TABLE `izin_syarat` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `kepegawaian_bidangstruktural`
--

DROP TABLE IF EXISTS `kepegawaian_bidangstruktural`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `kepegawaian_bidangstruktural` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nama_bidang` varchar(200) NOT NULL,
  `unit_kerja_id` int(11) NOT NULL,
  `bidang_induk_id` int(11) DEFAULT NULL,
  `keterangan` varchar(255) DEFAULT NULL,
  `lft` int(10) unsigned NOT NULL,
  `rght` int(10) unsigned NOT NULL,
  `tree_id` int(10) unsigned NOT NULL,
  `level` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `kepegawaian_bidangstruktural`
--

LOCK TABLES `kepegawaian_bidangstruktural` WRITE;
/*!40000 ALTER TABLE `kepegawaian_bidangstruktural` DISABLE KEYS */;
INSERT INTO `kepegawaian_bidangstruktural` VALUES (1,'pelayanan',72,NULL,'',1,2,1,0),(2,'pelayanan',72,NULL,'',1,2,2,0);
/*!40000 ALTER TABLE `kepegawaian_bidangstruktural` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `kepegawaian_jabatan`
--

DROP TABLE IF EXISTS `kepegawaian_jabatan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `kepegawaian_jabatan` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nama_jabatan` varchar(50) NOT NULL,
  `keterangan` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `kepegawaian_jabatan`
--

LOCK TABLES `kepegawaian_jabatan` WRITE;
/*!40000 ALTER TABLE `kepegawaian_jabatan` DISABLE KEYS */;
INSERT INTO `kepegawaian_jabatan` VALUES (1,'Kepala Dinas',''),(2,'Sekretaris',''),(3,'Kasubag',''),(4,'Kabid',''),(5,'Kasubid',''),(6,'Staf','');
/*!40000 ALTER TABLE `kepegawaian_jabatan` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `kepegawaian_jenisunitkerja`
--

DROP TABLE IF EXISTS `kepegawaian_jenisunitkerja`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `kepegawaian_jenisunitkerja` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `jenis_unit_kerja` varchar(30) NOT NULL,
  `jenis_unit_kerja_induk_id` int(11) DEFAULT NULL,
  `keterangan` varchar(255) DEFAULT NULL,
  `lft` int(10) unsigned NOT NULL,
  `rght` int(10) unsigned NOT NULL,
  `tree_id` int(10) unsigned NOT NULL,
  `level` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `kepegawaian_jenisunitkerja`
--

LOCK TABLES `kepegawaian_jenisunitkerja` WRITE;
/*!40000 ALTER TABLE `kepegawaian_jenisunitkerja` DISABLE KEYS */;
INSERT INTO `kepegawaian_jenisunitkerja` VALUES (1,'JABATAN',NULL,'Jabatan Struktural',1,2,1,0),(2,'SKPD',NULL,'Satuan Kerja Perangkat Daerah',1,10,2,0),(3,'UPTD',2,'Unit Pelaksana Teknis Dinas Daerah',2,9,2,1),(4,'UPTD DINAS PENDIDIKAN',3,'Unit Pelaksana Teknis Dinas Daerah Dinas Pendidikan',3,6,2,2),(5,'SD',4,'Sekolah Dasar',4,5,2,3),(6,'UPTD DINAS KESEHATAN',3,'Unit Pelaksana Teknis Dinas Daerah Dinas Kesehatan',7,8,2,2);
/*!40000 ALTER TABLE `kepegawaian_jenisunitkerja` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `kepegawaian_pegawai`
--

DROP TABLE IF EXISTS `kepegawaian_pegawai`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `kepegawaian_pegawai` (
  `account_ptr_id` int(11) NOT NULL,
  `unit_kerja_id` int(11) NOT NULL,
  `bidang_struktural_id` int(11) NOT NULL,
  `jabatan_id` int(11) NOT NULL,
  PRIMARY KEY (`account_ptr_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `kepegawaian_pegawai`
--

LOCK TABLES `kepegawaian_pegawai` WRITE;
/*!40000 ALTER TABLE `kepegawaian_pegawai` DISABLE KEYS */;
INSERT INTO `kepegawaian_pegawai` VALUES (268,72,1,1),(269,72,1,2),(270,72,1,3),(271,72,1,3),(272,72,1,3),(273,72,1,4),(274,72,1,4),(275,72,1,4),(276,72,1,5),(277,72,1,5),(278,72,1,5),(279,72,1,6),(280,72,1,6),(281,72,1,6),(282,72,1,6),(283,72,1,6),(284,72,1,6),(285,72,1,6),(286,72,1,6),(287,72,1,6),(288,72,1,6),(289,72,1,6),(290,72,1,6),(291,72,1,6),(292,72,1,6),(293,72,1,6),(294,72,1,6),(295,72,1,6),(296,72,1,6),(297,72,1,6),(298,72,1,6),(299,72,1,6),(300,72,1,6),(301,72,1,6),(302,72,1,6),(303,72,1,6),(304,72,1,6),(305,72,1,6);
/*!40000 ALTER TABLE `kepegawaian_pegawai` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `kepegawaian_unitkerja`
--

DROP TABLE IF EXISTS `kepegawaian_unitkerja`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `kepegawaian_unitkerja` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nama_unit_kerja` varchar(100) NOT NULL,
  `jenis_unit_kerja_id` int(11) DEFAULT NULL,
  `unit_kerja_induk_id` int(11) DEFAULT NULL,
  `keterangan` varchar(255) DEFAULT NULL,
  `kode_rekening` varchar(15) DEFAULT NULL,
  `kepala_id` int(11) DEFAULT NULL,
  `plt` tinyint(1) NOT NULL,
  `telephone` varchar(50) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `alamat` varchar(255) DEFAULT NULL,
  `kode_pos` varchar(50) DEFAULT NULL,
  `lft` int(10) unsigned NOT NULL,
  `rght` int(10) unsigned NOT NULL,
  `tree_id` int(10) unsigned NOT NULL,
  `level` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=74 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `kepegawaian_unitkerja`
--

LOCK TABLES `kepegawaian_unitkerja` WRITE;
/*!40000 ALTER TABLE `kepegawaian_unitkerja` DISABLE KEYS */;
INSERT INTO `kepegawaian_unitkerja` VALUES (1,'BUPATI',1,NULL,'Bupati','xx',NULL,0,'','','','',1,146,1,0),(2,'WAKIL BUPATI',1,1,'Wakil Bupati','xx',NULL,0,'','','','',2,145,1,1),(3,'SEKRETARIS DAERAH',1,2,'Sekretaris Daerah','xx',NULL,0,'','','','',3,144,1,2),(4,'STAF AHLI',1,3,'Staf Ahli Bupati Kediri','xx',NULL,0,'','','','',4,5,1,3),(5,'ASISTEN ADMINISTRASI UMUM',1,3,'Asisten Administrasi Umum','xx',NULL,0,'','','','',6,13,1,3),(6,'HUKUM',2,5,'Bagian Hukum','xx',NULL,0,'','','','',7,8,1,4),(7,'UMUM',2,5,'Bagian Umum','xx',NULL,0,'','','','',9,10,1,4),(8,'ORGANISASI',2,5,'Bagian Organisasi','xx',NULL,0,'','','','',11,12,1,4),(9,'ASISTEN PEREKONOMIAN DAN PEMBANGUNAN',1,3,'Asisten Perekonomian dan Pembangunan','xx',NULL,0,'','','','',14,19,1,3),(10,'PEREKONOMIAN',2,9,'Bagian Perekonomian','xx',NULL,0,'','','','',15,16,1,4),(11,'PEMBANGUNAN',2,9,'Bagian Pembangunan','xx',NULL,0,'','','','',17,18,1,4),(12,'ASISTEN PEMERINTAHAN DAN KESEJAHTERAAN RAKYAT',1,3,'Asisten Pemerintahan dan Kesejahteraan Rakyat','xx',NULL,0,'','','','',20,27,1,3),(13,'PEMERINTAHAN',2,12,'Bagian Pemerintahan Umum','xx',NULL,0,'','','','',21,22,1,4),(14,'HUMAS',2,12,'Bagian Humas dan Protokol','xx',NULL,0,'','','','',23,24,1,4),(15,'KESRA',2,12,'Bagian Kesejahteraan Rakyat dan Kemasyarakatan','xx',NULL,0,'','','','',25,26,1,4),(16,'DIKPORA',2,3,'Dinas Pendidikan, Pemuda dan Olahraga','xx',NULL,0,'','','','',28,29,1,3),(17,'DINKES',2,3,'Dinas Kesehatan','xx',NULL,0,'','','','',30,31,1,3),(18,'PU',2,3,'Dinas Pekerjaan Umum','1.03.01',NULL,0,'','','','',32,33,1,3),(19,'PENGAIRAN',2,3,'Dinas Pengairan, Pertambangan dan Energi','1.03.02',NULL,0,'','','','',34,35,1,3),(20,'DISHUB',2,3,'Dinas Perhubungan','1.07.01',NULL,0,'','','','',36,37,1,3),(21,'LH',2,3,'Kantor Lingkungan Hidup','1.08.01',NULL,0,'','','','',38,39,1,3),(22,'DKP',2,3,'Dinas Kebersihan dan Pertamanan','1.08.02',NULL,0,'','','','',40,41,1,3),(23,'DISDUKCAPIL',2,3,'Dinas Kependudukan dan Pencatatan Sipil','1.10.01',NULL,0,'','','','',42,43,1,3),(24,'BPPKB',2,3,'Badan Pemberdayaan Perempuan dan Keluarga Berencana','1.11.01',NULL,0,'','','','',44,45,1,3),(25,'DINSOS',2,3,'Dinas Sosial','1.13.01',NULL,0,'','','','',46,47,1,3),(26,'DISNAKERTRANS',2,3,'Dinas Tenaga Kerja dan Transmigrasi','1.14.01',NULL,0,'','','','',48,49,1,3),(27,'KOPERINDAG',2,3,'Dinas Koperasi, Industri dan Perdaganan','1.15.01',NULL,0,'','','','',50,51,1,3),(28,'DISBUDPAR',2,3,'	Dinas Kebudayaan dan Pariwisata','	1.17.01',NULL,0,'','','','',52,53,1,3),(29,'BAKESBANGPOLLINMAS',2,3,'Badan Kesatuan Bangsa, Politik, dan Perlindungan Masyarakat','	1.19.01',NULL,0,'','','','',54,55,1,3),(30,'SEKWAN',2,3,'	Sekretariat DPRD','	1.20.04',NULL,0,'','','','',56,57,1,3),(31,'INSPEKTORAT',2,3,'Inspektorat','	1.20.06',NULL,0,'','','','',58,59,1,3),(32,'BKD',2,3,'	Badan Kepegawaian Daerah','	1.20.07',NULL,0,'','','','',60,61,1,3),(33,'BPKAD',2,3,'Badan Pengelolaan Keuangan dan Aset Daerah','	1.20.08',NULL,0,'','','','',62,63,1,3),(34,'SATPOLPP',2,3,'Satuan Polisi Pamong Praja','	1.19.02',NULL,0,'','','','',64,65,1,3),(35,'KECAMATAN PARE',2,3,'KECAMATAN PARE','	1.20.09',NULL,0,'','','','',66,67,1,3),(36,'KECAMATAN GURAH',2,3,'KECAMATAN GURAH','	1.20.10',NULL,0,'','','','',68,69,1,3),(37,'KECAMATAN PLOSOKLATEN',2,3,'KECAMATAN PLOSOKLATEN','	1.20.11',NULL,0,'','','','',70,71,1,3),(38,'KECAMATAN KANDANGAN',2,3,'KECAMATAN KANDANGAN','	1.20.12',NULL,0,'','','','',72,73,1,3),(39,'KECAMATAN KEPUNG',2,3,'KECAMATAN KEPUNG','	1.20.13',NULL,0,'','','','',74,75,1,3),(40,'KECAMATAN PUNCU',2,3,'KECAMATAN PUNCU','	1.20.14',NULL,0,'','','','',76,77,1,3),(41,'KECAMATAN BADAS',2,3,'KECAMATAN BADAS','	1.20.15',NULL,0,'','','','',78,79,1,3),(42,'	KECAMATAN PAPAR',2,3,'	KECAMATAN PAPAR','	1.20.16',NULL,0,'','','','',80,81,1,3),(43,'KECAMATAN PURWOASRI',2,3,'KECAMATAN PURWOASRI','	1.20.17',NULL,0,'','','','',82,83,1,3),(44,'KECAMATAN PAGU',2,3,'KECAMATAN PAGU','	1.20.18',NULL,0,'','','','',84,85,1,3),(45,'KECAMATAN PLEMAHAN',2,3,'KECAMATAN PLEMAHAN','	1.20.19',NULL,0,'','','','',86,87,1,3),(46,'	KECAMATAN KUNJANG',2,3,'	KECAMATAN KUNJANG','	1.20.20',NULL,0,'','','','',88,89,1,3),(47,'	KECAMATAN KAYEN KIDUL',2,3,'	KECAMATAN KAYEN KIDUL','	1.20.21',NULL,0,'','','','',90,91,1,3),(48,'	KECAMATAN GAMPENGREJO',2,3,'	KECAMATAN GAMPENGREJO','	1.20.22',NULL,0,'','','','',92,93,1,3),(49,'	KECAMATAN MOJO',2,3,'	KECAMATAN MOJO','	1.20.23',NULL,0,'','','','',94,95,1,3),(50,'KECAMATAN SEMEN',2,3,'KECAMATAN SEMEN','	1.20.24',NULL,0,'','','','',96,97,1,3),(51,'	KECAMATAN TAROKAN',2,3,'	KECAMATAN TAROKAN','	1.20.26',NULL,0,'','','','',98,99,1,3),(52,'	KECAMATAN BANYAKAN',2,3,'	KECAMATAN BANYAKAN','	1.20.27',NULL,0,'','','','',100,101,1,3),(53,'KECAMATAN NGADILUWIH',2,3,'KECAMATAN NGADILUWIH','	1.20.28',NULL,0,'','','','',102,103,1,3),(54,'KECAMATAN KANDAT',2,3,'KECAMATAN KANDAT','	1.20.30',NULL,0,'','','','',104,105,1,3),(55,'	KECAMATAN GROGOL',2,3,'	KECAMATAN GROGOL','	1.20.25',NULL,0,'','','','',106,107,1,3),(56,'KECAMATAN KRAS',2,3,'KECAMATAN KRAS','	1.20.29',NULL,0,'','','','',108,109,1,3),(57,'KECAMATAN WATES',2,3,'KECAMATAN WATES','	1.20.31',NULL,0,'','','','',110,111,1,3),(58,'	KECAMATAN NGANCAR',2,3,'	KECAMATAN NGANCAR','	1.20.32',NULL,0,'','','','',112,113,1,3),(59,'KECAMATAN RINGINREJO',2,3,'KECAMATAN RINGINREJO','	1.20.33',NULL,0,'','','','',114,115,1,3),(60,'KECAMATAN NGASEM',2,3,'KECAMATAN NGASEM','	1.20.34',NULL,0,'','','','',116,117,1,3),(61,'KELURAHAN PARE',2,3,'KELURAHAN PARE','	1.20.39',NULL,0,'','','','',118,119,1,3),(62,'DISPENDA',2,3,'Dinas Pendapatan Daerah','	1.20.41',NULL,0,'','','','',120,121,1,3),(63,'	BKP3',2,3,'Badan Ketahanan Pangan dan Pelaksana Penyuluhan','	1.21.01',NULL,0,'','','','',122,123,1,3),(64,'BPMPD',2,3,'	Badan Pemberdayaan Masyarakat dan Pemerintahan Desa','	1.22.01',NULL,0,'','','','',124,125,1,3),(65,'ARSIP',2,3,'	Kantor Arsip dan Perpustakaan','	1.24.01',NULL,0,'','','','',126,127,1,3),(66,'	KOMINFO',2,3,'	Dinas Komunikasi dan Informatika','	1.25.01',NULL,0,'','','','',128,129,1,3),(67,'PERTANIAN',2,3,'	Dinas Pertanian','	2.01.01',NULL,0,'','','','',130,131,1,3),(68,'	DPP',2,3,'	Dinas Peternakan dan Perikanan','2.01.02',NULL,0,'','','','',132,133,1,3),(69,'HUTBUN',2,3,'	Dinas Kehutanan dan Perkebunan','	2.01.03',NULL,0,'','','','',134,135,1,3),(70,'BPBD',2,3,'Badan Penanggulangan Bencana Daerah','xx',NULL,0,'','','','',136,137,1,3),(71,'	RSUD',2,3,'Rumah Sakit Umum Daerah','xx',NULL,0,'','','','',138,139,1,3),(72,'BPMP2TSP',2,3,'	Badan Penanaman Modal dan Pelayanan Perizinan Terpadu Satu Pintu','	1.20.40',NULL,0,'','','','',140,141,1,3),(73,'BAPPEDA',2,3,'Badan Perencanaan Pembangunan Daerah','xx',NULL,0,'','','','',142,143,1,3);
/*!40000 ALTER TABLE `kepegawaian_unitkerja` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `master_atributtambahan`
--

DROP TABLE IF EXISTS `master_atributtambahan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `master_atributtambahan` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `status` smallint(5) unsigned NOT NULL,
  `created_at` datetime NOT NULL,
  `verified_at` datetime DEFAULT NULL,
  `rejected_at` datetime DEFAULT NULL,
  `updated_at` datetime NOT NULL,
  `created_by_id` int(11) DEFAULT NULL,
  `rejected_by_id` int(11) DEFAULT NULL,
  `verified_by_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `D23075d23bc1756b2752fef0effecfb4` (`created_by_id`),
  KEY `c87e251717ea222b6e4bb2727f635602` (`rejected_by_id`),
  KEY `D96b579687f514e42c2f99011cb803cf` (`verified_by_id`),
  CONSTRAINT `c87e251717ea222b6e4bb2727f635602` FOREIGN KEY (`rejected_by_id`) REFERENCES `accounts_account` (`identitaspribadi_ptr_id`),
  CONSTRAINT `D23075d23bc1756b2752fef0effecfb4` FOREIGN KEY (`created_by_id`) REFERENCES `accounts_account` (`identitaspribadi_ptr_id`),
  CONSTRAINT `D96b579687f514e42c2f99011cb803cf` FOREIGN KEY (`verified_by_id`) REFERENCES `accounts_account` (`identitaspribadi_ptr_id`)
) ENGINE=InnoDB AUTO_INCREMENT=588 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `master_atributtambahan`
--

LOCK TABLES `master_atributtambahan` WRITE;
/*!40000 ALTER TABLE `master_atributtambahan` DISABLE KEYS */;
INSERT INTO `master_atributtambahan` VALUES (1,6,'2016-09-05 02:37:00',NULL,NULL,'2016-09-05 02:37:00',NULL,NULL,NULL),(30,6,'2016-09-05 03:49:16',NULL,NULL,'2016-09-05 03:49:16',NULL,NULL,NULL),(35,6,'2016-09-05 04:02:28',NULL,NULL,'2016-09-05 04:02:28',NULL,NULL,NULL),(36,6,'2016-09-05 04:03:06',NULL,NULL,'2016-09-05 04:03:06',NULL,NULL,NULL),(62,6,'2016-09-05 07:24:57',NULL,NULL,'2016-09-05 07:25:32',NULL,NULL,NULL),(73,1,'2016-09-06 03:02:59',NULL,NULL,'2016-09-06 03:03:25',NULL,NULL,NULL),(104,6,'2016-09-20 07:11:48',NULL,NULL,'2016-09-20 07:11:48',NULL,NULL,NULL),(105,6,'2016-09-20 07:12:33',NULL,NULL,'2016-09-20 07:12:33',NULL,NULL,NULL),(107,6,'2016-09-20 07:22:21',NULL,NULL,'2016-09-20 07:22:21',NULL,NULL,NULL),(108,6,'2016-09-20 07:22:59',NULL,NULL,'2016-09-20 07:22:59',NULL,NULL,NULL),(109,6,'2016-09-22 03:41:09',NULL,NULL,'2016-09-22 03:41:09',NULL,NULL,NULL),(110,6,'2016-09-22 03:43:00',NULL,NULL,'2016-09-22 03:43:00',NULL,NULL,NULL),(111,6,'2016-09-22 03:46:23',NULL,NULL,'2016-09-22 03:46:23',NULL,NULL,NULL),(112,6,'2016-09-22 03:47:26',NULL,NULL,'2016-09-22 03:47:26',NULL,NULL,NULL),(113,6,'2016-09-22 04:01:04',NULL,NULL,'2016-09-22 04:01:04',NULL,NULL,NULL),(114,6,'2016-09-22 04:08:18',NULL,NULL,'2016-09-22 04:08:18',NULL,NULL,NULL),(115,6,'2016-09-22 04:09:26',NULL,NULL,'2016-09-22 04:09:26',NULL,NULL,NULL),(116,6,'2016-09-22 04:15:04',NULL,NULL,'2016-09-22 04:15:04',NULL,NULL,NULL),(125,6,'2016-09-22 04:50:26',NULL,NULL,'2016-09-22 04:50:26',NULL,NULL,NULL),(126,6,'2016-09-22 04:50:28',NULL,NULL,'2016-09-22 04:50:28',NULL,NULL,NULL),(127,6,'2016-09-22 10:23:34',NULL,NULL,'2016-09-22 10:23:34',NULL,NULL,NULL),(201,6,'2016-09-26 06:22:01',NULL,NULL,'2016-09-26 06:22:01',NULL,NULL,NULL),(202,6,'2016-09-26 06:22:07',NULL,NULL,'2016-09-26 06:22:07',NULL,NULL,NULL),(203,6,'2016-09-26 06:22:25',NULL,NULL,'2016-09-26 06:22:25',NULL,NULL,NULL),(204,6,'2016-09-26 06:22:29',NULL,NULL,'2016-09-26 06:22:29',NULL,NULL,NULL),(205,6,'2016-09-26 06:22:33',NULL,NULL,'2016-09-26 06:22:33',NULL,NULL,NULL),(210,6,'2016-09-26 07:37:57',NULL,NULL,'2016-09-26 07:37:57',NULL,NULL,NULL),(211,6,'2016-09-26 07:39:01',NULL,NULL,'2016-09-26 07:39:01',NULL,NULL,NULL),(238,6,'2016-09-26 21:01:04',NULL,NULL,'2016-09-26 21:01:04',NULL,NULL,NULL),(239,6,'2016-09-26 21:01:08',NULL,NULL,'2016-09-26 21:01:08',NULL,NULL,NULL),(240,6,'2016-09-26 21:01:14',NULL,NULL,'2016-09-26 21:01:14',NULL,NULL,NULL),(241,6,'2016-09-26 21:01:18',NULL,NULL,'2016-09-26 21:01:18',NULL,NULL,NULL),(242,6,'2016-09-26 21:01:22',NULL,NULL,'2016-09-26 21:01:22',NULL,NULL,NULL),(243,6,'2016-09-26 21:01:25',NULL,NULL,'2016-09-26 21:01:25',NULL,NULL,NULL),(244,6,'2016-09-26 21:01:28',NULL,NULL,'2016-09-26 21:01:28',NULL,NULL,NULL),(258,6,'2016-09-27 01:06:31',NULL,NULL,'2016-09-27 01:06:31',NULL,NULL,NULL),(259,6,'2016-09-27 01:06:33',NULL,NULL,'2016-09-27 01:06:33',NULL,NULL,NULL),(260,6,'2016-09-27 01:06:38',NULL,NULL,'2016-09-27 01:06:38',NULL,NULL,NULL),(261,6,'2016-09-27 01:06:43',NULL,NULL,'2016-09-27 01:06:43',NULL,NULL,NULL),(262,6,'2016-09-27 01:06:45',NULL,NULL,'2016-09-27 01:06:45',NULL,NULL,NULL),(263,6,'2016-09-27 01:06:48',NULL,NULL,'2016-09-27 01:06:48',NULL,NULL,NULL),(264,6,'2016-09-27 01:06:52',NULL,NULL,'2016-09-27 01:06:52',NULL,NULL,NULL),(268,6,'2016-09-29 02:27:42',NULL,NULL,'2016-10-03 08:11:19',NULL,NULL,NULL),(269,6,'2016-09-29 02:29:28',NULL,NULL,'2016-09-29 02:29:28',NULL,NULL,NULL),(270,6,'2016-09-29 02:30:33',NULL,NULL,'2016-09-29 02:30:33',NULL,NULL,NULL),(271,6,'2016-09-29 02:31:23',NULL,NULL,'2016-09-29 02:31:23',NULL,NULL,NULL),(272,6,'2016-09-29 02:32:57',NULL,NULL,'2016-10-06 00:30:42',NULL,NULL,NULL),(273,6,'2016-09-29 02:33:43',NULL,NULL,'2016-09-29 05:30:16',NULL,NULL,NULL),(274,6,'2016-09-29 02:34:25',NULL,NULL,'2016-09-29 05:31:25',NULL,NULL,NULL),(275,6,'2016-09-29 02:35:36',NULL,NULL,'2016-09-29 05:32:29',NULL,NULL,NULL),(276,6,'2016-09-29 02:36:41',NULL,NULL,'2016-09-29 02:36:41',NULL,NULL,NULL),(277,6,'2016-09-29 02:38:02',NULL,NULL,'2016-09-29 02:38:02',NULL,NULL,NULL),(278,6,'2016-09-29 02:38:46',NULL,NULL,'2016-09-29 02:38:46',NULL,NULL,NULL),(279,6,'2016-09-29 02:39:38',NULL,NULL,'2016-09-29 02:39:38',NULL,NULL,NULL),(280,6,'2016-09-29 02:40:49',NULL,NULL,'2016-09-29 02:40:49',NULL,NULL,NULL),(281,6,'2016-09-29 02:41:38',NULL,NULL,'2016-10-03 01:44:26',NULL,NULL,NULL),(282,6,'2016-09-29 02:42:46',NULL,NULL,'2016-10-04 06:28:19',NULL,NULL,NULL),(283,6,'2016-09-29 02:44:21',NULL,NULL,'2016-10-04 07:54:57',NULL,NULL,NULL),(284,6,'2016-09-29 02:44:57',NULL,NULL,'2016-10-04 08:21:53',NULL,NULL,NULL),(285,6,'2016-09-29 02:45:33',NULL,NULL,'2016-09-29 02:45:33',NULL,NULL,NULL),(286,6,'2016-09-29 02:46:02',NULL,NULL,'2016-09-29 02:46:02',NULL,NULL,NULL),(287,6,'2016-09-29 02:46:34',NULL,NULL,'2016-09-29 02:46:34',NULL,NULL,NULL),(288,6,'2016-09-29 02:47:17',NULL,NULL,'2016-09-29 02:47:17',NULL,NULL,NULL),(289,6,'2016-09-29 02:48:12',NULL,NULL,'2016-09-29 02:48:12',NULL,NULL,NULL),(290,6,'2016-09-29 02:49:15',NULL,NULL,'2016-09-29 02:49:15',NULL,NULL,NULL),(291,6,'2016-09-29 02:49:48',NULL,NULL,'2016-09-29 02:49:48',NULL,NULL,NULL),(292,6,'2016-09-29 02:50:26',NULL,NULL,'2016-09-29 02:50:26',NULL,NULL,NULL),(293,6,'2016-09-29 02:51:03',NULL,NULL,'2016-09-29 02:51:03',NULL,NULL,NULL),(294,6,'2016-09-29 02:52:19',NULL,NULL,'2016-09-29 02:52:19',NULL,NULL,NULL),(295,6,'2016-09-29 02:52:58',NULL,NULL,'2016-09-29 02:52:58',NULL,NULL,NULL),(296,6,'2016-09-29 02:53:28',NULL,NULL,'2016-09-29 02:53:28',NULL,NULL,NULL),(297,6,'2016-09-29 02:54:04',NULL,NULL,'2016-09-29 02:54:04',NULL,NULL,NULL),(298,6,'2016-09-29 02:54:40',NULL,NULL,'2016-09-29 02:54:40',NULL,NULL,NULL),(299,6,'2016-09-29 02:55:14',NULL,NULL,'2016-09-29 02:55:14',NULL,NULL,NULL),(300,6,'2016-09-29 02:55:48',NULL,NULL,'2016-09-29 02:55:48',NULL,NULL,NULL),(301,6,'2016-09-29 02:56:39',NULL,NULL,'2016-09-29 02:56:39',NULL,NULL,NULL),(302,6,'2016-09-29 02:57:12',NULL,NULL,'2016-09-29 02:57:12',NULL,NULL,NULL),(303,6,'2016-09-29 02:57:52',NULL,NULL,'2016-09-29 03:00:22',NULL,NULL,NULL),(304,6,'2016-09-29 02:58:33',NULL,NULL,'2016-09-29 02:58:33',NULL,NULL,NULL),(305,6,'2016-09-29 02:59:33',NULL,NULL,'2016-09-29 02:59:34',NULL,NULL,NULL),(355,6,'2016-10-03 08:33:44',NULL,NULL,'2016-10-03 08:33:44',NULL,NULL,NULL),(356,6,'2016-10-03 08:33:44',NULL,NULL,'2016-10-03 08:33:44',NULL,NULL,NULL),(357,6,'2016-10-03 08:33:45',NULL,NULL,'2016-10-03 08:33:45',NULL,NULL,NULL),(358,6,'2016-10-03 08:33:46',NULL,NULL,'2016-10-03 08:33:46',NULL,NULL,NULL),(359,6,'2016-10-03 08:33:47',NULL,NULL,'2016-10-03 08:33:47',NULL,NULL,NULL),(360,6,'2016-10-03 08:33:47',NULL,NULL,'2016-10-03 08:33:47',NULL,NULL,NULL),(361,6,'2016-10-03 08:33:48',NULL,NULL,'2016-10-03 08:33:48',NULL,NULL,NULL),(392,2,'2016-10-04 02:21:43',NULL,NULL,'2016-10-04 02:33:35',NULL,NULL,NULL),(393,1,'2016-10-04 02:21:43',NULL,NULL,'2016-10-04 08:33:27',1,NULL,NULL),(394,6,'2016-10-04 02:22:49',NULL,NULL,'2016-10-04 03:23:39',1,NULL,NULL),(395,6,'2016-10-04 02:24:00',NULL,NULL,'2016-10-04 02:24:00',NULL,NULL,NULL),(396,6,'2016-10-04 02:26:43',NULL,NULL,'2016-10-04 02:26:44',NULL,NULL,NULL),(397,6,'2016-10-04 02:29:46',NULL,NULL,'2016-10-04 02:29:46',NULL,NULL,NULL),(398,6,'2016-10-04 02:30:32',NULL,NULL,'2016-10-04 02:30:32',NULL,NULL,NULL),(399,6,'2016-10-04 02:30:32',NULL,NULL,'2016-10-04 02:30:32',NULL,NULL,NULL),(400,6,'2016-10-04 02:31:11',NULL,NULL,'2016-10-04 02:33:36',NULL,NULL,NULL),(401,6,'2016-10-04 02:31:11',NULL,NULL,'2016-10-04 02:31:11',NULL,NULL,NULL),(402,6,'2016-10-04 02:32:46',NULL,NULL,'2016-10-04 02:32:47',NULL,NULL,NULL),(403,6,'2016-10-04 02:32:48',NULL,NULL,'2016-10-04 02:33:31',NULL,NULL,NULL),(404,6,'2016-10-04 02:33:31',NULL,NULL,'2016-10-04 02:33:31',NULL,NULL,NULL),(405,6,'2016-10-04 02:33:31',NULL,NULL,'2016-10-04 02:33:31',NULL,NULL,NULL),(406,6,'2016-10-04 02:33:33',NULL,NULL,'2016-10-04 02:33:33',NULL,NULL,NULL),(407,6,'2016-10-04 02:33:34',NULL,NULL,'2016-10-04 02:33:34',NULL,NULL,NULL),(408,6,'2016-10-04 02:33:35',NULL,NULL,'2016-10-04 02:33:35',NULL,NULL,NULL),(409,6,'2016-10-04 02:33:36',NULL,NULL,'2016-10-04 02:33:36',NULL,NULL,NULL),(410,6,'2016-10-04 02:40:52',NULL,NULL,'2016-10-04 02:40:52',NULL,NULL,NULL),(411,6,'2016-10-04 02:46:11',NULL,NULL,'2016-10-04 02:46:11',NULL,NULL,NULL),(412,6,'2016-10-04 03:33:12',NULL,NULL,'2016-10-04 03:33:13',NULL,NULL,NULL),(413,6,'2016-10-04 03:43:35',NULL,NULL,'2016-10-04 03:43:36',1,NULL,NULL),(414,2,'2016-10-04 03:46:37',NULL,NULL,'2016-10-04 03:46:37',NULL,NULL,NULL),(415,6,'2016-10-04 03:46:37',NULL,NULL,'2016-10-04 03:46:38',1,NULL,NULL),(416,6,'2016-10-04 03:46:38',NULL,NULL,'2016-10-04 03:46:38',414,NULL,NULL),(417,6,'2016-10-04 03:59:55',NULL,NULL,'2016-10-04 03:59:56',1,NULL,NULL),(418,6,'2016-10-04 04:00:10',NULL,NULL,'2016-10-04 04:00:10',1,NULL,NULL),(419,6,'2016-10-04 04:00:52',NULL,NULL,'2016-10-04 04:00:52',1,NULL,NULL),(420,6,'2016-10-04 04:01:20',NULL,NULL,'2016-10-04 04:01:21',NULL,NULL,NULL),(421,6,'2016-10-04 04:01:27',NULL,NULL,'2016-10-04 04:01:27',NULL,NULL,NULL),(422,6,'2016-10-04 04:02:04',NULL,NULL,'2016-10-04 04:02:06',NULL,NULL,NULL),(423,6,'2016-10-04 04:02:38',NULL,NULL,'2016-10-04 04:02:38',NULL,NULL,NULL),(424,6,'2016-10-04 04:03:06',NULL,NULL,'2016-10-04 04:03:06',NULL,NULL,NULL),(425,6,'2016-10-04 04:03:07',NULL,NULL,'2016-10-04 04:03:07',NULL,NULL,NULL),(426,6,'2016-10-04 04:03:27',NULL,NULL,'2016-10-04 04:03:27',NULL,NULL,NULL),(427,6,'2016-10-04 04:03:27',NULL,NULL,'2016-10-04 04:03:27',NULL,NULL,NULL),(428,6,'2016-10-04 04:03:37',NULL,NULL,'2016-10-04 04:03:37',NULL,NULL,NULL),(429,6,'2016-10-04 04:03:43',NULL,NULL,'2016-10-04 04:03:43',NULL,NULL,NULL),(430,6,'2016-10-04 04:04:12',NULL,NULL,'2016-10-04 04:04:12',NULL,NULL,NULL),(431,6,'2016-10-04 04:05:39',NULL,NULL,'2016-10-04 04:05:40',NULL,NULL,NULL),(432,6,'2016-10-04 04:05:47',NULL,NULL,'2016-10-04 04:05:47',NULL,NULL,NULL),(433,6,'2016-10-04 04:06:12',NULL,NULL,'2016-10-04 04:06:12',NULL,NULL,NULL),(434,6,'2016-10-04 04:06:12',NULL,NULL,'2016-10-04 04:06:12',NULL,NULL,NULL),(435,6,'2016-10-04 04:06:57',NULL,NULL,'2016-10-04 04:06:58',NULL,NULL,NULL),(436,6,'2016-10-04 04:07:00',NULL,NULL,'2016-10-04 04:07:00',NULL,NULL,NULL),(437,6,'2016-10-04 04:07:01',NULL,NULL,'2016-10-04 04:07:01',NULL,NULL,NULL),(438,6,'2016-10-04 04:07:41',NULL,NULL,'2016-10-04 04:07:42',NULL,NULL,NULL),(439,6,'2016-10-04 04:09:12',NULL,NULL,'2016-10-04 04:09:13',NULL,NULL,NULL),(440,6,'2016-10-04 04:09:17',NULL,NULL,'2016-10-04 04:09:17',NULL,NULL,NULL),(441,6,'2016-10-04 04:09:20',NULL,NULL,'2016-10-04 04:09:20',NULL,NULL,NULL),(442,6,'2016-10-04 04:09:21',NULL,NULL,'2016-10-04 04:09:21',NULL,NULL,NULL),(443,6,'2016-10-04 04:11:11',NULL,NULL,'2016-10-04 04:11:11',NULL,NULL,NULL),(444,6,'2016-10-04 04:11:20',NULL,NULL,'2016-10-04 04:11:20',NULL,NULL,NULL),(445,6,'2016-10-04 04:11:20',NULL,NULL,'2016-10-04 04:11:20',NULL,NULL,NULL),(446,6,'2016-10-04 04:13:17',NULL,NULL,'2016-10-04 04:13:19',1,NULL,NULL),(447,6,'2016-10-04 04:13:19',NULL,NULL,'2016-10-04 04:13:19',NULL,NULL,NULL),(448,6,'2016-10-04 04:14:16',NULL,NULL,'2016-10-04 04:14:16',1,NULL,NULL),(449,6,'2016-10-04 04:15:35',NULL,NULL,'2016-10-04 04:15:36',1,NULL,NULL),(450,6,'2016-10-04 04:15:36',NULL,NULL,'2016-10-04 04:15:36',414,NULL,NULL),(451,6,'2016-10-04 04:16:13',NULL,NULL,'2016-10-04 04:16:14',1,NULL,NULL),(452,6,'2016-10-04 04:16:57',NULL,NULL,'2016-10-04 04:16:58',1,NULL,NULL),(453,6,'2016-10-04 04:20:31',NULL,NULL,'2016-10-04 04:20:32',1,NULL,NULL),(454,6,'2016-10-04 04:20:33',NULL,NULL,'2016-10-04 04:20:33',1,NULL,NULL),(455,6,'2016-10-04 04:23:31',NULL,NULL,'2016-10-04 04:23:31',1,NULL,NULL),(456,6,'2016-10-04 04:24:59',NULL,NULL,'2016-10-04 04:25:00',1,NULL,NULL),(457,6,'2016-10-04 04:25:56',NULL,NULL,'2016-10-04 04:25:58',1,NULL,NULL),(458,6,'2016-10-04 04:26:06',NULL,NULL,'2016-10-04 04:26:06',1,NULL,NULL),(459,6,'2016-10-04 04:26:06',NULL,NULL,'2016-10-04 04:26:06',1,NULL,NULL),(460,6,'2016-10-04 04:26:48',NULL,NULL,'2016-10-04 04:26:48',1,NULL,NULL),(461,6,'2016-10-04 04:26:56',NULL,NULL,'2016-10-04 04:26:56',1,NULL,NULL),(462,6,'2016-10-04 04:27:05',NULL,NULL,'2016-10-04 04:27:05',1,NULL,NULL),(463,6,'2016-10-04 04:28:17',NULL,NULL,'2016-10-04 04:28:18',1,NULL,NULL),(464,6,'2016-10-04 04:28:58',NULL,NULL,'2016-10-04 04:28:58',1,NULL,NULL),(465,6,'2016-10-04 04:29:41',NULL,NULL,'2016-10-04 04:29:41',1,NULL,NULL),(466,6,'2016-10-04 04:30:13',NULL,NULL,'2016-10-04 04:30:13',1,NULL,NULL),(467,6,'2016-10-04 04:30:55',NULL,NULL,'2016-10-04 04:30:55',1,NULL,NULL),(468,6,'2016-10-04 04:31:07',NULL,NULL,'2016-10-04 04:31:07',1,NULL,NULL),(469,6,'2016-10-04 04:31:07',NULL,NULL,'2016-10-04 04:31:07',1,NULL,NULL),(470,6,'2016-10-04 04:34:16',NULL,NULL,'2016-10-04 04:34:17',1,NULL,NULL),(471,6,'2016-10-04 04:36:39',NULL,NULL,'2016-10-04 04:36:40',1,NULL,NULL),(472,6,'2016-10-04 04:37:16',NULL,NULL,'2016-10-04 04:37:17',1,NULL,NULL),(473,6,'2016-10-04 04:38:11',NULL,NULL,'2016-10-04 04:38:11',1,NULL,NULL),(474,6,'2016-10-04 04:38:11',NULL,NULL,'2016-10-04 04:38:11',1,NULL,NULL),(475,6,'2016-10-04 04:38:17',NULL,NULL,'2016-10-04 04:38:17',1,NULL,NULL),(476,6,'2016-10-04 04:38:38',NULL,NULL,'2016-10-04 04:38:38',1,NULL,NULL),(477,6,'2016-10-04 04:39:27',NULL,NULL,'2016-10-04 04:39:27',1,NULL,NULL),(478,6,'2016-10-04 04:56:32',NULL,NULL,'2016-10-04 04:56:32',62,NULL,NULL),(479,6,'2016-10-04 04:56:42',NULL,NULL,'2016-10-04 04:56:42',62,NULL,NULL),(480,6,'2016-10-04 04:56:48',NULL,NULL,'2016-10-04 04:56:48',62,NULL,NULL),(481,6,'2016-10-04 05:03:36',NULL,NULL,'2016-10-04 05:03:36',62,NULL,NULL),(483,6,'2016-10-04 05:06:27',NULL,NULL,'2016-10-04 05:06:27',62,NULL,NULL),(484,6,'2016-10-04 05:09:50',NULL,NULL,'2016-10-04 05:09:50',62,NULL,NULL),(485,6,'2016-10-04 05:24:24',NULL,NULL,'2016-10-04 05:24:24',273,NULL,NULL),(486,1,'2016-10-04 05:31:30',NULL,NULL,'2016-10-04 08:33:27',281,NULL,NULL),(487,6,'2016-10-04 05:31:30',NULL,NULL,'2016-10-04 05:31:30',281,NULL,NULL),(488,6,'2016-10-04 05:33:34',NULL,NULL,'2016-10-04 05:33:34',273,NULL,NULL),(489,6,'2016-10-04 05:35:15',NULL,NULL,'2016-10-04 05:35:15',268,NULL,NULL),(490,6,'2016-10-04 06:59:26',NULL,NULL,'2016-10-04 06:59:27',282,NULL,NULL),(491,6,'2016-10-04 07:08:07',NULL,NULL,'2016-10-04 07:08:07',282,NULL,NULL),(492,6,'2016-10-04 07:25:00',NULL,NULL,'2016-10-04 07:25:00',282,NULL,NULL),(493,6,'2016-10-04 08:08:31',NULL,NULL,'2016-10-04 08:08:31',283,NULL,NULL),(494,6,'2016-10-04 08:17:16',NULL,NULL,'2016-10-04 08:17:16',283,NULL,NULL),(495,6,'2016-10-04 08:33:27',NULL,NULL,'2016-10-04 08:33:27',284,NULL,NULL),(497,6,'2016-10-05 10:20:29',NULL,NULL,'2016-10-05 10:20:29',1,NULL,NULL),(498,6,'2016-10-05 10:20:29',NULL,NULL,'2016-10-05 10:20:29',392,NULL,NULL),(500,6,'2016-10-05 10:26:02',NULL,NULL,'2016-10-05 10:26:02',1,NULL,NULL),(501,6,'2016-10-05 10:26:02',NULL,NULL,'2016-10-05 10:26:02',392,NULL,NULL),(502,2,'2016-10-06 00:17:48',NULL,NULL,'2016-10-06 00:17:48',NULL,NULL,NULL),(503,6,'2016-10-06 00:17:48',NULL,NULL,'2016-10-06 00:17:48',1,NULL,NULL),(504,6,'2016-10-06 00:17:48',NULL,NULL,'2016-10-06 00:17:48',502,NULL,NULL),(505,2,'2016-10-06 00:33:41',NULL,NULL,'2016-10-06 00:35:51',NULL,NULL,NULL),(506,1,'2016-10-06 00:33:41',NULL,NULL,'2016-10-06 01:21:40',272,NULL,NULL),(507,6,'2016-10-06 00:33:41',NULL,NULL,'2016-10-06 00:33:41',505,NULL,NULL),(508,6,'2016-10-06 00:34:24',NULL,NULL,'2016-10-06 00:35:58',272,NULL,NULL),(509,6,'2016-10-06 00:35:35',NULL,NULL,'2016-10-06 00:36:05',272,NULL,NULL),(510,6,'2016-10-06 00:35:45',NULL,NULL,'2016-10-06 00:35:45',272,NULL,NULL),(511,6,'2016-10-06 00:35:46',NULL,NULL,'2016-10-06 00:35:46',272,NULL,NULL),(512,6,'2016-10-06 00:35:51',NULL,NULL,'2016-10-06 00:35:51',272,NULL,NULL),(513,6,'2016-10-06 00:35:58',NULL,NULL,'2016-10-06 00:35:58',272,NULL,NULL),(514,6,'2016-10-06 00:36:05',NULL,NULL,'2016-10-06 00:36:05',272,NULL,NULL),(515,6,'2016-10-06 00:36:13',NULL,NULL,'2016-10-06 00:36:13',272,NULL,NULL),(516,6,'2016-10-06 00:38:40',NULL,NULL,'2016-10-06 00:38:40',272,NULL,NULL),(517,6,'2016-10-06 00:38:40',NULL,NULL,'2016-10-06 00:38:40',272,NULL,NULL),(518,6,'2016-10-06 00:41:25',NULL,NULL,'2016-10-06 00:41:25',273,NULL,NULL),(520,6,'2016-10-06 00:48:27',NULL,NULL,'2016-10-06 00:55:38',281,NULL,NULL),(521,6,'2016-10-06 00:48:27',NULL,NULL,'2016-10-06 00:48:27',392,NULL,NULL),(522,6,'2016-10-06 00:49:12',NULL,NULL,'2016-10-06 00:49:12',281,NULL,NULL),(523,1,'2016-10-06 00:56:03',NULL,NULL,'2016-10-06 01:21:40',281,NULL,NULL),(524,6,'2016-10-06 00:56:04',NULL,NULL,'2016-10-06 00:56:04',281,NULL,NULL),(525,6,'2016-10-06 00:59:14',NULL,NULL,'2016-10-06 00:59:14',273,NULL,NULL),(526,6,'2016-10-06 01:01:34',NULL,NULL,'2016-10-06 01:01:34',268,NULL,NULL),(527,6,'2016-10-06 01:03:36',NULL,NULL,'2016-10-06 01:03:36',282,NULL,NULL),(528,6,'2016-10-06 01:11:26',NULL,NULL,'2016-10-06 01:11:26',283,NULL,NULL),(529,6,'2016-10-06 01:13:52',NULL,NULL,'2016-10-06 01:13:52',283,NULL,NULL),(530,6,'2016-10-06 01:16:25',NULL,NULL,'2016-10-06 01:16:25',283,NULL,NULL),(531,6,'2016-10-06 01:18:59',NULL,NULL,'2016-10-06 01:18:59',283,NULL,NULL),(532,6,'2016-10-06 01:21:40',NULL,NULL,'2016-10-06 01:21:40',284,NULL,NULL),(533,2,'2016-10-06 02:00:50',NULL,NULL,'2016-10-06 02:09:07',NULL,NULL,NULL),(534,6,'2016-10-06 02:00:50',NULL,NULL,'2016-10-06 02:00:50',272,NULL,NULL),(535,6,'2016-10-06 02:00:50',NULL,NULL,'2016-10-06 02:00:50',533,NULL,NULL),(537,1,'2016-10-06 02:01:22',NULL,NULL,'2016-10-06 03:15:49',272,NULL,NULL),(538,6,'2016-10-06 02:01:22',NULL,NULL,'2016-10-06 02:01:22',533,NULL,NULL),(539,6,'2016-10-06 02:02:34',NULL,NULL,'2016-10-06 02:09:08',272,NULL,NULL),(540,6,'2016-10-06 02:08:08',NULL,NULL,'2016-10-06 02:09:09',272,NULL,NULL),(541,6,'2016-10-06 02:09:05',NULL,NULL,'2016-10-06 02:09:05',272,NULL,NULL),(542,6,'2016-10-06 02:09:06',NULL,NULL,'2016-10-06 02:09:06',272,NULL,NULL),(543,6,'2016-10-06 02:09:07',NULL,NULL,'2016-10-06 02:09:07',272,NULL,NULL),(544,6,'2016-10-06 02:09:08',NULL,NULL,'2016-10-06 02:09:08',272,NULL,NULL),(545,6,'2016-10-06 02:09:09',NULL,NULL,'2016-10-06 02:09:09',272,NULL,NULL),(546,6,'2016-10-06 02:09:10',NULL,NULL,'2016-10-06 02:09:10',272,NULL,NULL),(547,6,'2016-10-06 02:13:20',NULL,NULL,'2016-10-06 02:13:20',272,NULL,NULL),(548,6,'2016-10-06 02:17:45',NULL,NULL,'2016-10-06 02:17:45',273,NULL,NULL),(549,6,'2016-10-06 02:21:28',NULL,NULL,'2016-10-06 02:21:28',273,NULL,NULL),(550,1,'2016-10-06 02:24:34',NULL,NULL,'2016-10-06 03:15:49',281,NULL,NULL),(551,6,'2016-10-06 02:24:34',NULL,NULL,'2016-10-06 02:24:34',281,NULL,NULL),(552,6,'2016-10-06 02:29:05',NULL,NULL,'2016-10-06 02:29:05',273,NULL,NULL),(553,6,'2016-10-06 02:38:04',NULL,NULL,'2016-10-06 02:38:04',268,NULL,NULL),(554,6,'2016-10-06 02:54:55',NULL,NULL,'2016-10-06 02:54:55',282,NULL,NULL),(555,6,'2016-10-06 03:03:08',NULL,NULL,'2016-10-06 03:03:08',283,NULL,NULL),(556,6,'2016-10-06 03:15:49',NULL,NULL,'2016-10-06 03:15:49',284,NULL,NULL),(557,2,'2016-10-06 03:32:54',NULL,NULL,'2016-10-06 03:41:03',NULL,NULL,NULL),(558,6,'2016-10-06 03:32:55',NULL,NULL,'2016-10-06 03:32:55',272,NULL,NULL),(559,6,'2016-10-06 03:32:55',NULL,NULL,'2016-10-06 03:32:55',557,NULL,NULL),(561,2,'2016-10-06 03:34:41',NULL,NULL,'2016-10-06 19:24:41',272,NULL,NULL),(562,6,'2016-10-06 03:34:41',NULL,NULL,'2016-10-06 03:34:41',557,NULL,NULL),(563,6,'2016-10-06 03:36:19',NULL,NULL,'2016-10-06 03:41:04',272,NULL,NULL),(564,6,'2016-10-06 03:39:51',NULL,NULL,'2016-10-06 03:41:04',272,NULL,NULL),(565,6,'2016-10-06 03:41:00',NULL,NULL,'2016-10-06 03:41:00',272,NULL,NULL),(566,6,'2016-10-06 03:41:02',NULL,NULL,'2016-10-06 03:41:02',272,NULL,NULL),(567,6,'2016-10-06 03:41:03',NULL,NULL,'2016-10-06 03:41:03',272,NULL,NULL),(568,6,'2016-10-06 03:41:03',NULL,NULL,'2016-10-06 03:41:03',272,NULL,NULL),(569,6,'2016-10-06 03:41:04',NULL,NULL,'2016-10-06 03:41:04',272,NULL,NULL),(570,6,'2016-10-06 03:41:05',NULL,NULL,'2016-10-06 03:41:05',272,NULL,NULL),(571,6,'2016-10-06 03:43:42',NULL,NULL,'2016-10-06 03:43:42',272,NULL,NULL),(572,6,'2016-10-06 03:47:57',NULL,NULL,'2016-10-06 03:47:57',273,NULL,NULL),(573,6,'2016-10-06 03:47:57',NULL,NULL,'2016-10-06 03:47:57',273,NULL,NULL),(574,10,'2016-10-06 03:52:21',NULL,NULL,'2016-10-06 19:24:40',281,NULL,NULL),(575,6,'2016-10-06 03:52:21',NULL,NULL,'2016-10-06 03:52:21',281,NULL,NULL),(576,6,'2016-10-06 03:59:30',NULL,NULL,'2016-10-06 03:59:30',273,NULL,NULL),(577,6,'2016-10-06 04:01:01',NULL,NULL,'2016-10-06 04:01:01',268,NULL,NULL),(578,6,'2016-10-06 04:04:22',NULL,NULL,'2016-10-06 04:04:22',282,NULL,NULL),(579,6,'2016-10-06 04:23:25',NULL,NULL,'2016-10-06 04:23:25',1,NULL,NULL),(580,2,'2016-10-06 13:17:10',NULL,NULL,'2016-10-06 13:17:10',NULL,NULL,NULL),(581,6,'2016-10-06 13:17:10',NULL,NULL,'2016-10-06 13:17:10',1,NULL,NULL),(582,6,'2016-10-06 13:17:11',NULL,NULL,'2016-10-06 13:17:11',580,NULL,NULL),(584,6,'2016-10-06 13:17:17',NULL,NULL,'2016-10-06 13:17:17',1,NULL,NULL),(585,6,'2016-10-06 13:17:18',NULL,NULL,'2016-10-06 13:17:18',580,NULL,NULL),(586,6,'2016-10-06 19:22:10',NULL,NULL,'2016-10-06 19:22:10',1,NULL,NULL),(587,6,'2016-10-06 19:24:41',NULL,NULL,'2016-10-06 19:24:41',1,NULL,NULL);
/*!40000 ALTER TABLE `master_atributtambahan` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `master_berkas`
--

DROP TABLE IF EXISTS `master_berkas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `master_berkas` (
  `atributtambahan_ptr_id` int(11) NOT NULL,
  `nama_berkas` varchar(100) NOT NULL,
  `berkas` varchar(255) NOT NULL,
  `no_berkas` varchar(30) DEFAULT NULL,
  `keterangan` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`atributtambahan_ptr_id`),
  CONSTRAINT `mas_atributtambahan_ptr_id_1088d841_fk_master_atributtambahan_id` FOREIGN KEY (`atributtambahan_ptr_id`) REFERENCES `master_atributtambahan` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `master_berkas`
--

LOCK TABLES `master_berkas` WRITE;
/*!40000 ALTER TABLE `master_berkas` DISABLE KEYS */;
INSERT INTO `master_berkas` VALUES (104,'TESTING','berkas/61f43d3c41924890815195a8fb12aa8a.png',NULL,NULL),(105,'TESTING','berkas/16aae87ffce342c6a512ae542afe8290.jpg',NULL,NULL),(107,'HALO','berkas/d59cdcfb8ffe4ceb89ca93d18d7d2840.png',NULL,NULL),(108,'HALO','berkas/b6f31095b39d48f988fdd89ce1cdb055.png',NULL,NULL),(109,'Berkas Foto Pemohon','berkas/3b51d24f89844e24a6282cd422e94653.jpg',NULL,NULL),(110,'Berkas Foto Pemohon','berkas/78cd0bc96c9f48619f0ed76b2ff8c8fa.jpg',NULL,NULL),(111,'Berkas NPWP Pribadi','berkas/1a9210c165df413d884698c940fd1faf.jpg',NULL,NULL),(112,'Berkas NPWP Pribadi','berkas/7b46b972ebd34620a4bc98c450042a3b.jpg',NULL,NULL),(113,'Berkas Akta Pendirian','berkas/5af4b464a6414e9093f97755bf470698.jpg',NULL,NULL),(114,'Berkas Akta PendirianMAKMUR','berkas/5b6e0c29e47546cb853480fdd86e0569.jpg',NULL,NULL),(115,'Berkas Akta Pendirian MAKMUR','berkas/d06251a59e8542e98f5ee4e4d6b937db.jpg',NULL,NULL),(116,'Berkas NPWP Pribadi TAUFAN BUDIMAN','berkas/f5e9d0f78f094f9fb26ce0bcc977bd14.jpg',NULL,NULL),(125,'Berkas Akta Pendirian MAKMUR','berkas/fcbba015afbc4d259918b67eed9996c9.jpg',NULL,NULL),(126,'Berkas Akta Perubahan MAKMUR','berkas/bfd6b0c6ad894bc8906ee5a63f304f37.jpg',NULL,NULL),(127,'Berkas Pendukung EKA JAYA','berkas/f9deaec7b9e048a28625ced2e54f0292.jpg',NULL,NULL),(201,'Foto Pemohon FEBRI AHMAD NURHIDAYAT','berkas/a95bd065b83046d5b67797ba7d041fa1.png',NULL,NULL),(202,'Berkas KTP Pemohon','berkas/c84f42efdee3483d9638768abf5dc8b7.png',NULL,NULL),(203,'Berkas Akta Pendirian SEO','berkas/664203c1ccb3402d8fa479faa8db8733.png',NULL,NULL),(204,'Berkas Akta Perubahan SEO','berkas/7f02e41495574098b25afe565f513820.jpg',NULL,NULL),(205,'Berkas Pendukung FEBRI AHMAD NURHIDAYAT','berkas/7df80c77d2c44ae9a1001b421a148a06.jpg',NULL,NULL),(210,'Berkas KTP Pemohon ','berkas/704b35b3e4d54ac681a84c20f86b7e02.png',NULL,NULL),(211,'Berkas KTP Pemohon ','berkas/4d46086a283e432ab791c63a53557853.png',NULL,NULL),(238,'Foto Pemohon FEBRI AHMAD NURHIDAYAT','berkas/09a9e2d2c3154bc98a69e9c05782b845.png',NULL,NULL),(239,'Berkas KTP Pemohon','berkas/88e7ae8c4ede41249aaab12a867de26b.png',NULL,NULL),(240,'NPWP Pribadi FEBRI AHMAD NURHIDAYAT','berkas/ced07de78597481981e0e048efc78cbf.png',NULL,NULL),(241,'NPWP Perusahaan wewerrrr','berkas/95c4951a0cc64436a3637289c5685313.png',NULL,NULL),(242,'Berkas Akta Pendirian wewerrrr','berkas/3333b3998e404cee8c06bb3219f00f17.png',NULL,NULL),(243,'Berkas Akta Perubahan wewerrrr','berkas/d3806df849e3410a830c36adcffc6a76.png',NULL,NULL),(244,'Berkas Pendukung FEBRI AHMAD NURHIDAYAT','berkas/62be3578fe6a4c0c8c6cc4b3a83f6ebb.png',NULL,NULL),(258,'Foto Pemohon BAMBANG','berkas/d72d15c24c594be291b79b05938a11b7.png',NULL,NULL),(259,'Berkas KTP Pemohon','berkas/eb584d882069411b96556e183259fd57.jpg',NULL,NULL),(260,'NPWP Pribadi BAMBANG','berkas/d0f0c93c16e94ad39c5fa4ac1e03475b.jpg',NULL,NULL),(261,'NPWP Perusahaan Tenggo','berkas/03c2b81ce877442489fac7166ef684e0.jpg',NULL,NULL),(262,'Berkas Akta Pendirian Tenggo','berkas/f68dd0a268674d42a02eb2b73d0644b0.jpg',NULL,NULL),(263,'Berkas Akta Perubahan Tenggo','berkas/680c3235e72a4b1fa671d0f58bcd7aae.jpg',NULL,NULL),(264,'Berkas Pendukung BAMBANG','berkas/1b502081627749ada5b715b9bd40dafe.png',NULL,NULL),(355,'Foto Pemohon OKTAFIA PUTRI HANDAYANI','berkas/11699dde86da4ee28bb0f784b3b83c9a.jpg',NULL,NULL),(356,'Berkas KTP Pemohon','berkas/a4bc2a4615674e51a72c19b9281fa806.jpg',NULL,NULL),(357,'NPWP Pribadi OKTAFIA PUTRI HANDAYANI','berkas/00a87e0902b0452ba4936ce6463ce5b5.jpg',NULL,NULL),(358,'NPWP Perusahaan OPH OL','berkas/a329c70787ba4058aee78d0679165df3.jpg',NULL,NULL),(359,'Berkas Akta Pendirian OPH OL','berkas/a095277bcf1847fe84f7bd01419e195b.jpg',NULL,NULL),(360,'Berkas Akta Perubahan OPH OL','berkas/e783e13a03004c2aa6dd113a74958d8f.jpg',NULL,NULL),(361,'Berkas Pendukung OKTAFIA PUTRI HANDAYANI','berkas/af6dd0b9557b4fd9857ac1cb8548bff3.jpg',NULL,NULL),(404,'Berkas Pendukung FEBRI AHMAD NURHIDAYAT','berkas/41c965ea133c4d729de307b5c1f12e77.jpg',NULL,NULL),(405,'Berkas Akta Perubahan SEO','berkas/5e369e75fb4f4fda9211fb7dd48cab37.jpg',NULL,NULL),(406,'Foto Pemohon FEBRI AHMAD NURHIDAYAT','berkas/7b698d10ac014a87b17640f4760c2b45.jpg',NULL,NULL),(407,'NPWP Pribadi FEBRI AHMAD NURHIDAYAT','berkas/3589e430506342d1ba0a9dc96fc6f419.jpg',NULL,NULL),(408,'NPWP Perusahaan SEO','berkas/51623e490ba14b2ebbae4327fb02c4f1.jpg',NULL,NULL),(409,'Berkas Akta Pendirian SEO','berkas/051be768bf7d4edc85072382b7b5d5b3.jpg',NULL,NULL),(410,'Foto Pemohon FEBRI AHMAD NURHIDAYAT','berkas/0f680d26578448b9a17a7cdfa724b1a0.jpg',NULL,NULL),(411,'Berkas KTP Pemohon 1234','berkas/17ed230a5a524115bd4ef1e032d8d05e.jpg',NULL,NULL),(510,'Foto Pemohon FEBRI AHMAD NURHIDAYAT','berkas/48688e18343a4ca88eb5db7f1a5ff656.jpg',NULL,NULL),(511,'Berkas KTP Pemohon 1234567890','berkas/3a1f2db3904d4d249a6a77d3385e3caa.jpg',NULL,NULL),(512,'NPWP Pribadi FEBRI AHMAD NURHIDAYAT','berkas/d0e54aa4b6774fd6a61cd64ca096ddb4.jpg',NULL,NULL),(513,'NPWP Perusahaan SEO Foundantion','berkas/93a4725fc44145ce8f792ef9f3dafe26.jpg',NULL,NULL),(514,'Berkas Akta Pendirian SEO Foundantion','berkas/8403da47f28a4315ac90e240385b0fed.jpg',NULL,NULL),(515,'Berkas Pendukung FEBRI AHMAD NURHIDAYAT','berkas/7fe4c74afd7d499686c3a489514d3018.jpg',NULL,NULL),(541,'Foto Pemohon GILANG ROSA','berkas/e37ec383161042068428d1f50199aff3.png',NULL,NULL),(542,'Berkas KTP Pemohon 12345678901','berkas/abe61cbbb5e74ffebbbe6bd6bc0b7723.png',NULL,NULL),(543,'NPWP Pribadi GILANG ROSA','berkas/7ed555734c554e1e8653c506ef551574.png',NULL,NULL),(544,'NPWP Perusahaan MAju Mundur','berkas/f6a12b179522439daf2ffb8b5be88a3a.png',NULL,NULL),(545,'Berkas Akta Pendirian MAju Mundur','berkas/2bea50f4fa294b6980555dada7eda715.png',NULL,NULL),(546,'Berkas Pendukung GILANG ROSA','berkas/e239ab6bcf7640898e960f98c2bf4eb9.png',NULL,NULL),(565,'Foto Pemohon INDAH SUSTIARI, SE','berkas/19f52f057fb54db19360bf112fc1e22b.jpg',NULL,NULL),(566,'Berkas KTP Pemohon 3506214806740001','berkas/bb831c52ed7a433c96560e80780813ab.jpg',NULL,NULL),(567,'NPWP Pribadi INDAH SUSTIARI, SE','berkas/e7474d5cd18f45e99f7ee38181c615e6.jpg',NULL,NULL),(568,'NPWP Perusahaan \"INDAH JAYA\" TOKO','berkas/a6a377f7558d4a679e0726bd689ec29e.jpg',NULL,NULL),(569,'Berkas Akta Pendirian \"INDAH JAYA\" TOKO','berkas/57e32939fc8942d48418c30a26671578.jpg',NULL,NULL),(570,'Berkas Pendukung INDAH SUSTIARI, SE','berkas/985fa06063a749deb579ebf104a33c72.jpg',NULL,NULL);
/*!40000 ALTER TABLE `master_berkas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `master_desa`
--

DROP TABLE IF EXISTS `master_desa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `master_desa` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `kecamatan_id` int(11) NOT NULL,
  `nama_desa` varchar(40) DEFAULT NULL,
  `keterangan` varchar(255) DEFAULT NULL,
  `lt` varchar(100) DEFAULT NULL,
  `lg` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `master_desa_kecamatan_id_677ad0db_fk_master_kecamatan_id` (`kecamatan_id`),
  CONSTRAINT `master_desa_kecamatan_id_677ad0db_fk_master_kecamatan_id` FOREIGN KEY (`kecamatan_id`) REFERENCES `master_kecamatan` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=414 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `master_desa`
--

LOCK TABLES `master_desa` WRITE;
/*!40000 ALTER TABLE `master_desa` DISABLE KEYS */;
INSERT INTO `master_desa` VALUES (1,1,'Bobang','','',''),(2,1,'Bulu','','',''),(3,1,'Joho','','',''),(4,1,'Kanyoran','','',''),(5,1,'Kedak','','',''),(6,1,'Pagung','','',''),(7,1,'Puhrubuh','','',''),(8,1,'Puhsarang','','',''),(9,1,'Selopanggung','','',''),(10,1,'Semen','','',''),(11,1,'Sidomulyo','','',''),(12,1,'Titik ','','',''),(14,2,'Lamong','','',''),(15,2,'Canggu','','',''),(16,2,'Krecek','','',''),(17,2,'Blaru','','',''),(18,2,'Badas','','',''),(19,2,'Tunglur','','',''),(20,2,'Sekoto','','',''),(21,2,'Bringin','','',''),(22,3,'Banyakan','','',''),(23,3,'Jabon','','',''),(24,3,'Jatirejo','','',''),(25,3,'Manyaran','','',''),(26,3,'Maron','','',''),(27,3,'Ngablak','','',''),(28,3,'Parang','','',''),(29,3,'Sendang','','',''),(30,3,'Tiron','','',''),(31,4,'Gampeng','','',''),(32,4,'Jongbiru','','',''),(33,4,'Kalibelo','','',''),(34,4,'Kepuhrejo','','',''),(35,4,'Ngebrak','','',''),(36,4,'Plosorejo ','','',''),(37,4,'Putih ','','',''),(38,4,'Sambirejo ','','',''),(39,4,'Sambiresik ','','',''),(40,4,'Turus ','','',''),(41,4,'Wanengpaten ','','',''),(42,5,'Bakalan ','','',''),(43,5,'Cerme ','','',''),(44,5,'Datengan ','','',''),(45,5,'Gambyok ','','',''),(46,5,'Grogol ','','',''),(47,5,'Kalipang ','','',''),(48,5,'Sonorejo ','','',''),(49,5,'Sumberejo ','','',''),(50,5,'Wonoasri ','','',''),(51,5,'Gayam ','','',''),(53,5,'Bangkok ','','',''),(67,8,'Ngletih','','',''),(68,8,'Blabak','','',''),(69,8,'Cendono','','',''),(70,8,'Kandat','','',''),(71,8,'Karangrejo','','',''),(72,8,'Ngreco','','',''),(73,8,'Pule','','',''),(74,6,'Gayam ','','',''),(75,6,'Adan-Adan ','','',''),(76,8,'Purworejo','','',''),(77,6,'Bangkok ','','',''),(78,6,'Banyuanyar ','','',''),(79,8,'Ringinsari','','',''),(80,6,'Besuk ','','',''),(81,8,'Selosari','','',''),(82,6,'Blimbing ','','',''),(83,6,'Bogem ','','',''),(84,8,'Sumberejo','','',''),(85,6,'Gabru ','','',''),(86,8,'Tegalan','','',''),(87,6,'Gempolan ','','',''),(88,6,'Gurah ','','',''),(89,6,'Kerkep ','','',''),(90,6,'Kranggan ','','',''),(91,6,'Ngasem ','','',''),(92,6,'Nglumbang ','','',''),(93,6,'Sukorejo ','','',''),(94,6,'Sumbercangkring ','','',''),(95,6,'Tambakrejo ','','',''),(96,6,'Tiru Kidul','','',''),(97,7,'Banaran','','',''),(98,7,'Bukur','','',''),(99,6,'Tiru Lor ','','',''),(100,7,'Jeruk Gulung','','',''),(101,7,'Jeruk Wangi','','',''),(102,7,'Jlumbang','','',''),(103,7,'Kandangan','','',''),(104,7,'Karang Tengah','','',''),(105,7,'kasreman','','',''),(106,7,'Kemiri','','',''),(107,7,'Klampisan','','',''),(108,7,'Medowo','','',''),(109,7,'Mlancu','','',''),(110,6,'Turus','','',''),(111,6,'Wonojoyo','','',''),(112,25,'Besowo','','',''),(113,25,'Brumbung','','',''),(114,25,'Damar Wulan','','',''),(115,25,'Kampung Baru','','',''),(116,25,'Kebon Rejo','','',''),(117,25,'Keling','','',''),(118,25,'Kencong','','',''),(119,25,'Kepung','','',''),(120,25,'Krenceng','','',''),(121,25,'Siman','','',''),(122,11,'Balong Jeruk','','',''),(123,11,'Dungus','','',''),(124,11,'Juwet','','',''),(125,11,'Kapas','','',''),(126,11,'Kapi','','',''),(127,11,'Klepek','','',''),(128,11,'Kunjang','','',''),(129,11,'Kuwik','','',''),(130,11,'Pakis','','',''),(131,11,'Pare Lor','','',''),(132,11,'Tengger Lor','','',''),(133,11,'Wonorejo','','',''),(134,9,'Bangsongan ','','',''),(135,9,'Baye ','','',''),(136,9,'Jambu ','','',''),(137,9,'Kayen Kidul ','','',''),(138,9,'Mukuh ','','',''),(139,9,'Nanggungan ','','',''),(140,9,'Padangan ','','',''),(141,9,'Sambirobyong ','','',''),(142,9,'Sekaran ','','',''),(143,9,'Semambung ','','',''),(144,9,'Senden ','','',''),(145,9,'Sukoharjo ','','',''),(146,10,'Banjaranyar ','','',''),(147,10,'Bendosari ','','',''),(149,10,'Bleber ','','',''),(150,10,'Butuh ','','',''),(151,10,'Jabang ','','',''),(152,10,'Jambean ','','',''),(153,10,'Kanigoro ','','',''),(154,10,'Karangtalun ','','',''),(155,10,'Krandang ','','',''),(157,10,'Kras ','','',''),(158,10,'Mojosari ','','',''),(159,10,'Nyawangan ','','',''),(160,10,'Pelas ','','',''),(161,10,'Purwodadi ','','',''),(162,10,'Rejomulyo ','','',''),(163,10,'Setonorejo ','','',''),(164,12,'Blimbing ','','',''),(165,12,'Jugo ','','',''),(166,12,'Kedawung ','','',''),(167,12,'Keniten ','','',''),(168,12,'Kranding ','','',''),(169,12,'Kraton ','','',''),(170,12,'Maesan ','','',''),(171,12,'Mlati ','','',''),(172,12,'Mojo ','','',''),(173,12,'Mondo ','','',''),(174,12,'Ngadi ','','',''),(175,12,'Ngetrep ','','',''),(176,12,'Pamongan ','','',''),(177,12,'Petok ','','',''),(178,12,'Petungroto ','','',''),(179,12,'Petungroto ','','',''),(180,12,'Ploso ','','',''),(181,12,'Ponggok ','','',''),(182,12,'Sukoanyar ','','',''),(183,12,'Surat ','','',''),(184,12,'Tambibendo ','','',''),(185,13,'Badal ','','',''),(186,13,'Badalpandean ','','',''),(187,13,'Banggle ','','',''),(188,13,'Banjarejo ','','',''),(189,13,'Bedug ','','',''),(190,13,'Branggahan ','','',''),(191,13,'Dukuh ','','',''),(192,13,'Mangunrejo ','','',''),(193,13,'Ngadiluwih ','','',''),(194,13,'Purwokerto ','','',''),(195,13,'Rembang ','','',''),(196,13,'Rembangkepuh ','','',''),(197,13,'Seketi ','','',''),(198,13,'Slumbung ','','',''),(199,13,'Tales ','','',''),(200,13,'Wonorejo ','','',''),(201,14,'Kunjang ','','',''),(202,14,'Babadan ','','',''),(203,14,'Bedali ','','',''),(204,14,'Jagul ','','',''),(205,14,'Manggis ','','',''),(206,14,'Manggis ','','',''),(207,14,'Ngancar ','','',''),(208,14,'Pandantoyo ','','',''),(209,14,'Sempu ','','',''),(210,14,'Sugihwaras ','','',''),(211,15,'Doko ','','',''),(212,15,'Gogorante ','','',''),(213,15,'Karangrejo ','','',''),(214,15,'Kwadungan ','','',''),(215,15,'Nambaan ','','',''),(216,15,'Ngasem ','','',''),(217,15,'Paron ','','',''),(218,15,'Sukorejo ','','',''),(219,15,'Sumberjo ','','',''),(220,15,'Toyoresmi ','','',''),(221,15,'Tugurejo ','','',''),(222,15,'Wonocatur ','','',''),(223,16,'Bendo ','','',''),(224,16,'Bulupasar ','','',''),(225,16,'Jagung ','','',''),(226,16,'Kambingan ','','',''),(227,16,'Menang ','','',''),(228,16,'Pagu ','','',''),(229,16,'Semanding ','','',''),(230,16,'Semen ','','',''),(231,16,'Sitimerto','','',''),(232,16,'Tanjung ','','',''),(233,16,'Tengger Kidul ','','',''),(234,16,'Wates ','','',''),(235,16,'Wonosari ','','',''),(236,17,'Wonosari Dawuhan Kidul ','','',''),(237,17,'Jambangan ','','',''),(238,17,'Janti ','','',''),(239,17,'Kedungmalang ','','',''),(240,17,'Kepuh ','','',''),(241,17,'Kwaron ','','',''),(242,17,'Maduretno ','','',''),(243,17,'Minggiran ','','',''),(244,17,'Ngampel ','','',''),(245,17,'Papar ','','',''),(246,17,'Pehkulon ','','',''),(247,17,'Pehwetan ','','',''),(248,17,'Puhjajar ','','',''),(249,17,'Purwotengah ','','',''),(250,17,'Srikaton ','','',''),(251,17,'Sukomoro ','','',''),(252,17,'Tanon ','','',''),(253,18,'Pare ','','',''),(254,18,'Tulungrejo ','','',''),(255,18,'Pelem ','','',''),(256,18,'Gedangsewu ','','',''),(257,18,'Tertek ','','',''),(258,18,'Bendo ','','',''),(259,18,'Sambirejo ','','',''),(260,18,'Darungan ','','',''),(261,18,'Sumberbendo ','','',''),(262,18,'Sidorejo ','','',''),(263,19,'Banjarejo ','','',''),(264,19,'Bogokidul ','','',''),(265,19,'Kayen Lor ','','',''),(266,19,'Langenharjo ','','',''),(267,20,'Brenggolo','','',''),(268,19,'Mejono ','','',''),(269,19,'Mojoayu ','','',''),(270,19,'Mojokerep ','','',''),(271,19,'Ngino ','','',''),(272,19,'Payaman ','','',''),(273,20,'Donganti','','',''),(274,19,'Plemahan ','','',''),(275,20,'Gondang','','',''),(276,19,'Puhjarak ','','',''),(277,19,'Ringinpitu ','','',''),(278,19,'Sebet ','','',''),(279,19,'Sidowarek ','','',''),(280,20,'Jarak','','',''),(281,19,'Sukoharjo ','','',''),(282,20,'Kawedusan','','',''),(283,19,'Tegowangi ','','',''),(284,19,'Wonokerto ','','',''),(285,20,'Kayunan','','',''),(286,20,'Klanderan','','',''),(287,21,'Asmorobangun ','','',''),(288,21,'Gadungan ','','',''),(289,21,'Manggis ','','',''),(290,21,'Puncu ','','',''),(291,20,'Panjer','','',''),(292,21,'Satak ','','',''),(293,20,'Ploso Kidul','','',''),(294,21,'Sidomulyo ','','',''),(295,21,'Watugede ','','',''),(296,20,'Ploso Lor','','',''),(297,21,'Wonorejo ','','',''),(298,20,'Pranggang','','',''),(299,20,'Punjul','','',''),(300,20,'Sepawon','','',''),(301,22,'Belor ','','',''),(302,20,'Sumber Agung','','',''),(303,22,'Blawe ','','',''),(304,20,'Wonorejo Trisulo','','',''),(305,22,'Bulu ','','',''),(306,22,'Dawuhan ','','',''),(307,22,'Dayu ','','',''),(308,22,'Jantok ','','',''),(309,22,'Karangpakis ','','',''),(310,22,'Kempleng ','','',''),(311,22,'Ketawang ','','',''),(312,22,'Klampitan ','','',''),(313,22,'Mekikis ','','',''),(314,22,'Merjoyo ','','',''),(315,22,'Mranggen ','','',''),(316,22,'Muneng ','','',''),(317,22,'Pandansari ','','',''),(318,22,'Pesing ','','',''),(319,22,'Purwoasri ','','',''),(320,22,'Purwodadi ','','',''),(321,22,'Sidomulyo ','','',''),(322,22,'Sumberjo ','','',''),(323,22,'Tugu ','','',''),(324,22,'Wonotengah ','','',''),(325,22,'Woromarto ','','',''),(326,26,'Batuaji ','','',''),(327,26,'Dawung ','','',''),(328,26,'Deyeng ','','',''),(329,26,'Jemekan ','','',''),(330,26,'Nambaan ','','',''),(331,26,'Purwodadi ','','',''),(332,26,'Ringinrejo ','','',''),(333,26,'Sambi ','','',''),(334,26,'Selodono ','','',''),(335,26,'Srikaton ','','',''),(336,23,'Blimbing ','','',''),(337,23,'Susuhbango ','','',''),(338,23,'Bulusari ','','',''),(339,23,'Cengkok ','','',''),(341,23,'Kaliboto ','','',''),(342,23,'Kalirong ','','',''),(343,23,'Kedungsari ','','',''),(344,23,'Kerep ','','',''),(345,23,'Sumberduren ','','',''),(346,23,'Tarokan ','','',''),(347,23,'Jati','','',''),(348,24,'Duwet ','','',''),(349,24,'Gadungan ','','',''),(350,24,'Jajar ','','',''),(351,24,'Janti ','','',''),(352,24,'Joho ','','',''),(353,24,'Karanganyar ','','',''),(354,24,'Pagu ','','',''),(355,24,'Plaosan ','','',''),(356,24,'Pojok ','','',''),(357,24,'Segaran ','','',''),(358,24,'Sidomulyo ','','',''),(359,24,'Silir ','','',''),(360,24,'Sumberagung ','','',''),(361,24,'Tawang ','','',''),(362,24,'Tempurejo ','','',''),(363,24,'Tunge ','','',''),(364,24,'Wates ','','',''),(365,24,'Wonorejo ','','',''),(366,28,'Semampir ','','',''),(367,28,'Dandangan ','','',''),(368,28,'Ngadirejo ','','',''),(369,28,'Pakelan ','','',''),(370,28,'Pocanan ','','',''),(371,28,'Banjaran ','','',''),(372,28,'Jagalan ','','',''),(373,28,'Kemasan ','','',''),(374,28,'Kaliombo ','','',''),(375,28,'Kampung Dalem ','','',''),(376,28,'Ngronggo ','','',''),(377,28,'Manisrenggo ','','',''),(378,28,'Balowerti ','','',''),(379,28,'Rejomulyo ','','',''),(380,28,'Ringin Anom ','','',''),(381,28,'Setono Gedong ','','',''),(382,28,'Setono Pande ','','',''),(383,27,'Dermo ','','',''),(384,27,'Mrican ','','',''),(385,27,'Mojoroto ','','',''),(387,27,'Gayam ','','',''),(388,27,'Bandar Lor ','','',''),(389,27,'Sukorame ','','',''),(390,27,'Pojok ','','',''),(391,27,'Campurejo ','','',''),(392,27,'Tamanan ','','',''),(393,27,'Lirboyo ','','',''),(394,27,'Bandar Kidul ','','',''),(395,27,'Banjar Melati ','','',''),(396,27,'Bujel ','','',''),(397,29,'Bangsal ','','',''),(398,29,'Burengan ','','',''),(399,29,'Pesantren ','','',''),(400,29,'Jamsaren ','','',''),(401,29,'Pakunden ','','',''),(402,29,'Pakunden ','','',''),(404,29,'Tinalan ','','',''),(405,29,'Banaran ','','',''),(406,29,'Tosaren ','','',''),(407,29,'Betet ','','',''),(408,29,'Blabak ','','',''),(409,29,'Bawang ','','',''),(410,29,'Ngletih ','','',''),(411,29,'Tempurejo ','','',''),(412,29,'Ketami ','','',''),(413,27,'Ngampel','','','');
/*!40000 ALTER TABLE `master_desa` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `master_jenisnomoridentitas`
--

DROP TABLE IF EXISTS `master_jenisnomoridentitas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `master_jenisnomoridentitas` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `jenis_nomor_identitas` varchar(30) NOT NULL,
  `keterangan` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `master_jenisnomoridentitas`
--

LOCK TABLES `master_jenisnomoridentitas` WRITE;
/*!40000 ALTER TABLE `master_jenisnomoridentitas` DISABLE KEYS */;
INSERT INTO `master_jenisnomoridentitas` VALUES (1,'KTP','Kartu Tanda Penduduk'),(2,'PASPOR',''),(3,'NIP',''),(4,'NIK','');
/*!40000 ALTER TABLE `master_jenisnomoridentitas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `master_jenispemohon`
--

DROP TABLE IF EXISTS `master_jenispemohon`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `master_jenispemohon` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `jenis_pemohon` varchar(255) DEFAULT NULL,
  `keterangan` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `master_jenispemohon`
--

LOCK TABLES `master_jenispemohon` WRITE;
/*!40000 ALTER TABLE `master_jenispemohon` DISABLE KEYS */;
INSERT INTO `master_jenispemohon` VALUES (1,'Pemilik',''),(2,'Penanggung Jawab',''),(3,'Ketua',''),(4,'Direktur',''),(5,'Komisaris','');
/*!40000 ALTER TABLE `master_jenispemohon` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `master_jenisreklame`
--

DROP TABLE IF EXISTS `master_jenisreklame`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `master_jenisreklame` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `jenis_reklame` varchar(255) NOT NULL,
  `keterangan` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `master_jenisreklame`
--

LOCK TABLES `master_jenisreklame` WRITE;
/*!40000 ALTER TABLE `master_jenisreklame` DISABLE KEYS */;
/*!40000 ALTER TABLE `master_jenisreklame` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `master_kabupaten`
--

DROP TABLE IF EXISTS `master_kabupaten`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `master_kabupaten` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `provinsi_id` int(11) NOT NULL,
  `nama_kabupaten` varchar(40) NOT NULL,
  `keterangan` varchar(255) DEFAULT NULL,
  `lt` varchar(100) DEFAULT NULL,
  `lg` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `master_kabupaten_provinsi_id_2c2a2522_fk_master_provinsi_id` (`provinsi_id`),
  CONSTRAINT `master_kabupaten_provinsi_id_2c2a2522_fk_master_provinsi_id` FOREIGN KEY (`provinsi_id`) REFERENCES `master_provinsi` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=337 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `master_kabupaten`
--

LOCK TABLES `master_kabupaten` WRITE;
/*!40000 ALTER TABLE `master_kabupaten` DISABLE KEYS */;
INSERT INTO `master_kabupaten` VALUES (1,1,'Kab Kediri','','',''),(2,1,'Kediri','','',''),(3,1,'Malang','','',''),(4,1,'Blitar','','',''),(5,2,'Sumedang','','',''),(7,3,'Yogyakarta','','',''),(8,4,'Temanggung','','',''),(9,4,'Surakarta','','',''),(10,1,'Ngawi','','',''),(11,4,'Sragen','','',''),(13,2,'Jatinangor','','',''),(14,1,'Tulungagung','','',''),(15,1,'Surabaya','','',''),(16,1,'Nganjuk','','',''),(17,1,'Probolinggo','','',''),(18,4,'Kudus','','',''),(19,1,'Gresik','','',''),(20,1,'Jombang','','',''),(21,5,'Kab Aceh Selatan','','',''),(22,5,'Kab Aceh Tenggara','','',''),(23,5,'Kab Aceh Timur','','',''),(24,5,'Kab Aceh Tengah','','',''),(25,5,'Kab Aceh Barat','','',''),(26,5,'Kab Pidie','','',''),(27,5,'Kab Aceh Utara','','',''),(28,5,'Kab Simeulue','','',''),(29,5,'Kab Aceh Singkil','','',''),(30,5,'Kab Bireuen','','',''),(31,5,'Kab Aceh Barat Daya','','',''),(32,5,'Kab Gayo Lues','','',''),(33,5,'Kab Aceh Jaya','','',''),(34,5,'Kab Nagan Raya','','',''),(35,5,'Kab Aceh Tamiang','','',''),(36,5,'Kab Bener Meriah','','',''),(37,5,'Kab Pidie Jaya','','',''),(38,5,'Banda Aceh','','',''),(39,5,'Sabang','','',''),(40,5,'Lhokseumawe','','',''),(41,5,'Langsa','','',''),(42,5,'Subulussalam','','',''),(43,8,'Kab Tapanuli Tengah','','',''),(44,8,'Kab Tapanuli Utara','','',''),(45,8,'Kab Tapanuli Selatan','','',''),(46,8,'Kab Nias','','',''),(47,8,'Kab Langkat','','',''),(48,8,'Kab Karo','','',''),(49,8,'Kab Deli Serdang','','',''),(50,8,'Kab Simalungun','','',''),(51,8,'Kab Asahan','','',''),(52,8,'Kab Labuhanbatu','','',''),(53,8,'Kab Dairi','','',''),(54,8,'Kab Toba Samosir','','',''),(55,8,'Kab Mandailing Natal','','',''),(56,8,'Kab Nias Selatan','','',''),(57,8,'Kab Pakpak Bharat','','',''),(58,8,'Kab Humbang Hasundutan','','',''),(59,8,'Kab Samosir','','',''),(60,8,'Kab Serdang Bedagai','','',''),(61,8,'Kab Batu Bara','','',''),(62,8,'Kab Padang Lawas Utara','','',''),(63,8,'Kab Padang Lawas','','',''),(64,8,'Kab Labuhanbatu Selatan','','',''),(65,8,'Kab Labuhanbatu Utara','','',''),(66,8,'Kab Nias Utara','','',''),(67,8,'Kab Nias Barat','','',''),(68,8,'Medan','','',''),(69,8,'Pematang Siantar','','',''),(70,8,'Sibolga','','',''),(71,8,'Tanjung Balai','','',''),(72,8,'Binjai','','',''),(73,8,'Tebing Tinggi','','',''),(74,8,'Padang Sidimpuan','','',''),(75,8,'Gunungsitoli','','',''),(76,6,'Kab Pesisir Selatan','','',''),(77,6,'Kab Solok','','',''),(78,6,'Kab Sijunjung','','',''),(79,6,'Kab Tanah Datar','','',''),(80,6,'Kab Padang Pariaman','','',''),(81,6,'Kab Agam','','',''),(82,6,'Kab Lima Puluh Kota','','',''),(83,6,'Kab Pasaman','','',''),(84,6,'Kab Kepulauan Mentawai','','',''),(85,6,'Kab Dharmasraya','','',''),(86,6,'Kab Solok Selatan','','',''),(87,6,'Kab Pasaman Barat','','',''),(88,6,'Padang','','',''),(89,6,'Solok','','',''),(90,6,'Sawahlunto','','',''),(91,6,'Padang Panjang','','',''),(92,6,'Bukittinggi','','',''),(93,6,'Payaumbuh','','',''),(94,6,'Pariaman','','',''),(95,9,'Kab Kampar','','',''),(96,9,'Kab Indragiri Hulu','','',''),(97,9,'Kab Bengkalis','','',''),(98,9,'Kab Indragiri Hilir','','',''),(99,9,'Kab Pelalawan','','',''),(100,9,'Kab Rokan Hulu','','',''),(101,9,'Kab Rokan Hilir','','',''),(102,9,'Kab Siak','','',''),(103,9,'Kab Kuantan Singingi','','',''),(104,9,'Pekanbaru','','',''),(105,9,'Dumai','','',''),(106,10,'Kab Kerinci','','',''),(107,10,'Kab Merangin','','',''),(108,10,'Kab Sarolangun','','',''),(109,10,'Kab Batanghari','','',''),(110,10,'Kab Muaro Jambi','','',''),(111,10,'Kab Tanjung Jabung Barat','','',''),(112,10,'Kab Tanjung Jabung Timur','','',''),(113,10,'Kab Bungo','','',''),(114,10,'Kab Tebo','','',''),(115,10,'Jambi','','',''),(116,10,'Sungai Penuh','','',''),(117,7,'Kab Ogan Komering Ulu','','',''),(118,7,'Kab Ogan Komering Ilir','','',''),(119,7,'Kab Muara Enim','','',''),(120,7,'Kab Lahat','','',''),(121,7,'Kab Musi Rawas','','',''),(122,7,'Kab Musi Banyuasin','','',''),(123,7,'Kab Banyuasin','','',''),(124,7,'Kab Ogan Komering Ulu Timur','','',''),(125,7,'Kab Ogan Komering Selatan','','',''),(126,7,'Kab Ogan Ilir','','',''),(127,7,'Kab Empat Lawang','','',''),(128,7,'Kab Penukal Abab Pematang Ilir','','',''),(129,7,'Kab Musi Rawas Utara','','',''),(130,7,'Palembang','','',''),(131,7,'Pagar Alam','','',''),(132,7,'Lubuk Lingau','','',''),(133,7,'Prabumulih','','',''),(134,11,'Kab Bengkulu Selatan','','',''),(135,11,'Kab Rejang Lebong','','',''),(136,11,'Kab Bengkulu Utara','','',''),(137,11,'Kab Kaur','','',''),(138,11,'Kab Seluma','','',''),(139,11,'Kab Muko Muko','','',''),(140,11,'Kab Lebong','','',''),(141,11,'Kab Kepahiang','','',''),(142,11,'Kab Bengkulu Tengah','','',''),(143,11,'Bengkulu','','',''),(144,12,'Kab Lampung Selatan','','',''),(145,12,'Kab Lampung Tengah','','',''),(146,12,'Kab Lampung Utara','','',''),(147,12,'Kab Lampung Barat','','',''),(148,12,'Kab Tulang Bawah','','',''),(149,12,'Kab Tanggamus','','',''),(150,12,'Kab Lampung Timur','','',''),(151,12,'Kab Way Kanan','','',''),(152,12,'Kab Pesawaran','','',''),(153,12,'Kab Pringsewu','','',''),(154,12,'Kab Mesuji','','',''),(155,12,'Kab Tulang Bawang Barat','','',''),(156,12,'Kab Pesisir Barat','','',''),(157,12,'Bandar Lampung','','',''),(158,12,'Metro','','',''),(159,13,'Kab Bangka','','',''),(160,13,'Kab Belitung','','',''),(161,13,'Kab Bangka Selatan','','',''),(162,13,'Kab Bangka Tegah','','',''),(163,13,'Kab Bangka Timur','','',''),(164,13,'Kab Bangka Barat','','',''),(165,13,'Pangkal Pinang','','',''),(166,14,'Kab Bintan','','',''),(167,14,'Kab Karimun','','',''),(168,14,'Kab Natuna','','',''),(169,14,'Kab Lingga','','',''),(170,14,'Kab Kepulauan Anambas','','',''),(171,14,'Batam','','',''),(172,14,'Tanjung Pinang','','',''),(173,15,'Kab ADM Kep. Seribu','','',''),(174,15,'ADM Jakarta Pusat','','',''),(175,15,'ADM Jakarta Timur','','',''),(176,15,'ADM Jakarta Barat','','',''),(177,15,'ADM Jakarta Utara','','',''),(178,15,'ADM Jakarta Selatan','','',''),(179,2,'Kab Bogor','','',''),(180,2,'Kab Sukabumi','','',''),(181,2,'Kab Cianjur','','',''),(182,2,'Kab Bandung','','',''),(183,2,'Kab Garut','','',''),(184,2,'Kab Tasikmalaya','','',''),(185,2,'Kab Ciamis','','',''),(186,2,'Kab Kuningan','','',''),(187,2,'Kab Cirebon','','',''),(188,2,'Kab Majalengka','','',''),(189,2,'Kab Indramayu','','',''),(190,2,'Kab Subang','','',''),(191,2,'Kab Purwakarta','','',''),(192,2,'Kab Karawang','','',''),(193,2,'Kab Bekasi','','',''),(194,2,'Kab Bandung Barat','','',''),(195,2,'Kab Pangandaran','','',''),(196,2,'Bogor','','',''),(197,2,'Sukabumi','','',''),(198,2,'Bandung','','',''),(199,2,'Cirebon','','',''),(200,2,'Bekasi','','',''),(201,2,'Depok','','',''),(202,2,'Cimahi','','',''),(203,2,'Tasikmalaya','','',''),(204,2,'Banjar','','',''),(205,4,'Kab Cilacap','','',''),(206,4,'Kab Banyumas','','',''),(207,4,'Kab Purbalingga','','',''),(208,4,'Kab Kebumen','','',''),(209,4,'Kab Banjarnegara','','',''),(210,4,'Kab Purworejo','','',''),(211,4,'Kab Wonosobo','','',''),(212,4,'Kab Magelang','','',''),(213,4,'Kab Boyolali','','',''),(214,4,'Kab Klaten','','',''),(215,4,'Kab Sukoharjo','','',''),(216,4,'Kab Wonogiri','','',''),(217,4,'Kab Karanganyar','','',''),(218,4,'Kab Sragen','','',''),(219,4,'Kab Grobogan','','',''),(220,4,'Kab Blora','','',''),(221,4,'Kab Rembang','','',''),(222,4,'Kab Pati','','',''),(223,4,'Kab Kudus','','',''),(224,4,'Kab Jepara','','',''),(225,4,'Kab Demak','','',''),(226,4,'Kab Semarang','','',''),(227,4,'Kab Temanggung','','',''),(228,4,'Kab Kendal','','',''),(229,4,'Kab Batang','','',''),(230,4,'Kab Pekalongan','','',''),(231,4,'Kab Pemalang','','',''),(232,4,'Kab tegal','','',''),(233,4,'Kab Brebes','','',''),(234,4,'Magelang','','',''),(235,4,'Surakarta','','',''),(236,4,'Salatiga','','',''),(237,4,'Semarang','','',''),(238,4,'Pekalongan','','',''),(239,4,'Tegal','','',''),(240,16,'Kab Pandeglang','','',''),(241,16,'Kab Lebak','','',''),(242,16,'Kab Tangerang','','',''),(243,16,'Kab Serang','','',''),(244,16,'Tangerang','','',''),(245,16,'Cilegon','','',''),(246,16,'Serang','','',''),(247,16,'Tangerang Selatan','','',''),(248,3,'Kab Kulon Progo','','',''),(249,3,'Kab Bantul','','',''),(250,3,'Kab Gunungkidul','','',''),(251,3,'Kab Sleman','','',''),(252,1,'Kab Pacitan','','',''),(253,1,'Kab Ponorogo','','',''),(254,1,'Kab Trenggalek','','',''),(255,1,'Kab Tulungagung','','',''),(256,1,'Kab Blitar','','',''),(257,1,'Kab Malang','','',''),(258,1,'Kab Lumajang','','',''),(259,1,'Kab Banyuwangi','','',''),(260,1,'Kab Bondowoso','','',''),(261,1,'Kab Situbondo','','',''),(262,1,'Kab Probolinggo','','',''),(263,1,'Kab Pasuruan','','',''),(264,1,'Kab Sidoarjo','','',''),(265,1,'Kab Mojokerto','','',''),(266,1,'Kab Jombang','','',''),(267,1,'Kab Nganjuk','','',''),(268,1,'Kab Madiun','','',''),(269,1,'Kab Magetan','','',''),(270,1,'Kab Ngawi','','',''),(271,1,'Kab Bojonegoro','','',''),(272,1,'Kab Tuban','','',''),(273,1,'Kab Lamongan','','',''),(274,1,'Kab Gresik','','',''),(275,1,'Kab Bangkalan','','',''),(276,1,'Kab Sampang','','',''),(277,1,'Kab Pamekasan','','',''),(278,1,'Kab Sumenep','','',''),(279,1,'Pasuruan','','',''),(280,1,'Mojokerto','','',''),(281,1,'Madiun','','',''),(282,1,'Batu','','',''),(283,17,'Kab Jembrana','','',''),(284,17,'Kab Tabanan','','',''),(285,17,'Kab Badung','','',''),(286,17,'Kab Gianyar','','',''),(287,17,'Kab Klungkung','','',''),(288,17,'Kab Bangli','','',''),(289,17,'Kab Karangasem','','',''),(290,17,'Kab Buleleng','','',''),(291,17,'Denpasar','','',''),(292,19,'Kab Lombok Barat','','',''),(293,19,'Kab Lombok Tengah','','',''),(294,19,'Kab Lombok Timur','','',''),(295,19,'Kab Sumbawa','','',''),(296,19,'Kab Dompu','','',''),(297,19,'Kab Bima','','',''),(298,19,'Kab Sumbawa Barat','','',''),(299,19,'Kab Lombok Utara','','',''),(300,19,'Mataram','','',''),(301,19,'Bima','','',''),(302,18,'Kab Kupang','','',''),(303,18,'Kab Timor Tengah Selatan','','',''),(304,18,'Kab Timor Tengah Utara','','',''),(305,18,'Kab Belu','','',''),(306,18,'Kab Alor','','',''),(307,18,'Kab Flores Timur','','',''),(308,18,'Kab Sikka','','',''),(309,18,'Kab Ende','','',''),(310,18,'Kab Ngada','','',''),(311,18,'Kab Manggarai','','',''),(312,18,'Kab Sumba Barat','','',''),(313,18,'Kab Sumba Timur','','',''),(314,18,'Kab Lembata','','',''),(315,18,'Kab Rote Ndao','','',''),(316,18,'Kab Manggarai Barat','','',''),(317,18,'Kab Nagekeo','','',''),(318,18,'Kab Sumba Barat Daya','','',''),(319,18,'Kab Manggarai Timur','','',''),(320,18,'Kab Sabu Raijua','','',''),(321,18,'Kab Malaka','','',''),(322,18,'Kupang','','',''),(323,20,'Kab Sambas','','',''),(324,20,'Kab Mempawah','','',''),(325,20,'Kab Sanggau','','',''),(326,20,'Kab Ketapang','','',''),(327,20,'Kab Sintang','','',''),(328,20,'Kab Kapuas Hulu','','',''),(329,20,'Kab Bengkayang','','',''),(330,20,'Kab Landak','','',''),(331,20,'Kab Sekadu','','',''),(332,20,'Kab Melawai','','',''),(333,20,'Kab Kayong Utara','','',''),(334,20,'Kab Kubu Raya','','',''),(335,20,'Pontianak','','',''),(336,20,'Singkawang','','','');
/*!40000 ALTER TABLE `master_kabupaten` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `master_kecamatan`
--

DROP TABLE IF EXISTS `master_kecamatan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `master_kecamatan` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `kabupaten_id` int(11) NOT NULL,
  `nama_kecamatan` varchar(40) NOT NULL,
  `keterangan` varchar(255) DEFAULT NULL,
  `lt` varchar(100) DEFAULT NULL,
  `lg` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `master_kecamatan_kabupaten_id_4c101ed4_fk_master_kabupaten_id` (`kabupaten_id`),
  CONSTRAINT `master_kecamatan_kabupaten_id_4c101ed4_fk_master_kabupaten_id` FOREIGN KEY (`kabupaten_id`) REFERENCES `master_kabupaten` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `master_kecamatan`
--

LOCK TABLES `master_kecamatan` WRITE;
/*!40000 ALTER TABLE `master_kecamatan` DISABLE KEYS */;
INSERT INTO `master_kecamatan` VALUES (1,1,'Semen','','',''),(2,1,'Badas','','',''),(3,1,'Banyakan','','',''),(4,1,'Gampengrejo','','',''),(5,1,'Grogol','','',''),(6,1,'Gurah','','',''),(7,1,'Kandangan','','',''),(8,1,'Kandat','','',''),(9,1,'Kayen Kidul','','',''),(10,1,'Kras','','',''),(11,1,'Kunjang','','',''),(12,1,'Mojo','','',''),(13,1,'Ngadiluwih','','',''),(14,1,'Ngancar','','',''),(15,1,'Ngasem','','',''),(16,1,'Pagu','','',''),(17,1,'Papar','','',''),(18,1,'Pare','','',''),(19,1,'Plemahan','','',''),(20,1,'Plosoklaten','','',''),(21,1,'Puncu','','',''),(22,1,'Purwoasri','','',''),(23,1,'Tarokan','','',''),(24,1,'Wates','','',''),(25,1,'Kepung','','',''),(26,1,'Ringinrejo','','',''),(27,2,'Mojoroto','','',''),(28,2,'Kediri Kota','','',''),(29,2,'Pesantren','','',''),(30,1,'Plosoklaten','','','');
/*!40000 ALTER TABLE `master_kecamatan` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `master_negara`
--

DROP TABLE IF EXISTS `master_negara`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `master_negara` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nama_negara` varchar(40) NOT NULL,
  `keterangan` varchar(255) DEFAULT NULL,
  `code` varchar(10) DEFAULT NULL,
  `lt` varchar(100) DEFAULT NULL,
  `lg` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=249 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `master_negara`
--

LOCK TABLES `master_negara` WRITE;
/*!40000 ALTER TABLE `master_negara` DISABLE KEYS */;
INSERT INTO `master_negara` VALUES (1,'Indonesia','','ID','',''),(2,'Afghanistan','','AF','',''),(3,'Aland Islands','','AX','',''),(4,'Albania','','AL','',''),(5,'Algeria','','DZ','',''),(6,'American Samoa','','AS','',''),(7,'AndorrA','','AD','',''),(8,'Angola','','AO','',''),(9,'Anguilla','','AI','',''),(10,'Antarctica','','AQ','',''),(11,'Antigua and Barbuda','','AG','',''),(12,'Argentina','','AR','',''),(13,'Armenia','','AM','',''),(14,'Aruba','','AW','',''),(15,'Australia','','AU','',''),(16,'Austria','','AT','',''),(17,'Azerbaijan','','AZ','',''),(18,'Bahamas','','BS','',''),(19,'Bahrain','','BH','',''),(20,'Bangladesh','','BD','',''),(21,'Barbados','','BB','',''),(22,'Belarus','','BY','',''),(23,'Belgium','','BE','',''),(24,'Belize','','BZ','',''),(25,'Benin','','BJ','',''),(26,'Bermuda','','BM','',''),(27,'Bhutan','','BT','',''),(28,'Bolivia','','BO','',''),(29,'Bosnia and Herzegovina','','BA','',''),(30,'Botswana','','BW','',''),(31,'Bouvet Islan','','BV','',''),(32,'Brazil','','BR','',''),(33,'British Indian Ocean Territory','','IO','',''),(34,'Brunei Darussalam','','BN','',''),(35,'Bulgaria','','BG','',''),(36,'Burkina Faso','','BF','',''),(37,'Burundi','','BI','',''),(38,'Cambodia','','KH','',''),(39,'Cameroon','','CM','',''),(40,'Canada','','CA','',''),(41,'Cape Verde','','CV','',''),(42,'Cayman Islands','','KY','',''),(43,'Central African Republic','','CF','',''),(44,'Chad','','TD','',''),(45,'Chile','','CL','',''),(46,'China','','CN','',''),(47,'Christmas Island','','CX','',''),(48,'Cocos (Keeling) Islands','','CC','',''),(49,'Colombia','','CO','',''),(50,'Comoros','','KM','',''),(51,'Congo','','CG','',''),(52,'Cook Islands','','CK','',''),(53,'Costa Rica','','CR','',''),(54,'Cote D\\\'Ivoire','','CI','',''),(55,'Croatia','','HR','',''),(56,'Cuba','','CU','',''),(57,'Cyprus','','CY','',''),(58,'Czech Republic','','CZ','',''),(59,'Denmark','','DK','',''),(60,'Djibouti','','DJ','',''),(61,'Dominica','','DM','',''),(62,'Dominican Republic','','DO','',''),(63,'Ecuador','','EC','',''),(64,'Egypt','','EG','',''),(65,'El Salvador','','SV','',''),(66,'Equatorial Guinea','','GQ','',''),(67,'Eritrea','','ER','',''),(68,'Estonia','','EE','',''),(69,'Ethiopia','','ET','',''),(70,'Falkland Islands (Malvinas)','','FK','',''),(71,'Faroe Islands','','FO','',''),(72,'Fiji','','FJ','',''),(73,'Finland','','FI','',''),(74,'France','','FR','',''),(75,'French Guiana','','GF','',''),(76,'French Polynesia','','PF','',''),(77,'French Southern Territories','','TF','',''),(78,'Gabon','','GA','',''),(79,'Gambia','','GM','',''),(80,'Georgia','','GE','',''),(81,'Germany','','DE','',''),(89,'Ghana','','GH','',''),(90,'Gibraltar','','GI','',''),(91,'Greece','','GR','',''),(92,'Greenland','','GL','',''),(93,'Grenada','','GD','',''),(94,'Guadeloupe','','GP','',''),(95,'Guam','','GU','',''),(96,'Guatemala','','GT','',''),(97,'Guernsey','','GG','',''),(98,'Guinea','','GN','',''),(99,'Guinea-Bissau','','GW','',''),(100,'Guyana','','GY','',''),(101,'Haiti','','HT','',''),(102,'Heard Island and Mcdonald Islands','','HM','',''),(103,'Holy See (Vatican City State)','','VA','',''),(104,'Honduras','','HN','',''),(105,'Hong Kong','','HK','',''),(106,'Hungary','','HU','',''),(107,'Iceland','','IS','',''),(108,'India','','IN','',''),(109,'Iran, Islamic Republic Of','','IR','',''),(110,'Iraq','','IQ','',''),(111,'Ireland','','IE','',''),(112,'Isle of Man','','IM','',''),(113,'Israel','','IL','',''),(114,'Italy','','IT','',''),(115,'Jamaica','','JM','',''),(116,'Japan','','JP','',''),(117,'Jersey','','JE','',''),(118,'Jordan','','JO','',''),(119,'Kazakhstan','','KZ','',''),(120,'Kenya','','KE','',''),(121,'Kiribati','','KI','',''),(122,'Korea, Democratic People\\\'S Republic of','','KP','',''),(123,'Korea, Republic of','','KR','',''),(124,'Kuwait','','KW','',''),(125,'Kyrgyzstan','','KG','',''),(126,'Lao People\\\'S Democratic Republic','','LA','',''),(127,'Latvia','','LV','',''),(128,'Lebanon','','LB','',''),(129,'Lesotho','','LS','',''),(130,'Liberia','','LR','',''),(131,'Libyan Arab Jamahiriya','','LY','',''),(132,'Liechtenstein','','LI','',''),(133,'Lithuania','','LT','',''),(134,'Luxembourg','','LU','',''),(135,'Macao','','MO','',''),(136,'Macedonia, The Former Yugoslav Republic ','','MK','',''),(137,'Madagascar','','MG','',''),(138,'Malawi','','MW','',''),(139,'Maldives','','MV','',''),(140,'Mali','','ML','',''),(141,'Malta','','MT','',''),(142,'Marshall Islands','','MH','',''),(143,'Martinique','','MQ','',''),(144,'Mauritania','','MR','',''),(145,'Mauritius','','MU','',''),(146,'Mayotte','','YT','',''),(147,'Mexico','','MX','',''),(148,'Micronesia, Federated States of','','FM','',''),(149,'Moldova, Republic of','','MD','',''),(150,'Monaco','','MC','',''),(151,'Mongolia','','MN','',''),(152,'Montserrat','','MS','',''),(153,'Morocco','','MA','',''),(154,'Mozambique','','MZ','',''),(155,'Myanmar','','MM','',''),(156,'Namibia','','NA','',''),(157,'Nauru','','NR','',''),(158,'Nepal','','NP','',''),(159,'Netherlands','','NL','',''),(160,'Netherlands Antilles','','AN','',''),(161,'New Caledonia','','NC','',''),(162,'New Zealand','','NZ','',''),(163,'Nicaragua','','NI','',''),(164,'Niger','','NE','',''),(165,'Nigeria','','NG','',''),(166,'Niue','','NU','',''),(167,'Norfolk Island','','NF','',''),(168,'Northern Mariana Islands','','MP','',''),(169,'Norway','','NO','',''),(170,'Oman','','OM','',''),(171,'Pakistan','','PK','',''),(172,'Palau','','PW','',''),(173,'Palestinian Territory, Occupied','','PS','',''),(174,'Panama','','PA','',''),(175,'Papua New Guinea','','PG','',''),(176,'Paraguay','','PY','',''),(177,'Peru','','PE','',''),(178,'Philippines','','PH','',''),(179,'Pitcairn','','PN','',''),(180,'Poland','','PL','',''),(181,'Portugal','','PT','',''),(182,'Puerto Rico','','PR','',''),(183,'Qatar','','QA','',''),(184,'Reunion','','RE','',''),(185,'Romania','','RO','',''),(186,'Russian Federation','','RU','',''),(187,'Rwanda','','RW','',''),(188,'Saint Helena','','SH','',''),(189,'Saint Kitts and Nevis','','KN','',''),(190,'Saint Lucia','','LC','',''),(191,'Saint Pierre and Miquelon','','PM','',''),(192,'Saint Vincent and the Grenadines','','VC','',''),(193,'Samoa','','WS','',''),(194,'San Marino','','SM','',''),(195,'Sao Tome and Principe','','ST','',''),(196,'Saudi Arabia','','SA','',''),(197,'Senegal','','SN','',''),(198,'Serbia and Montenegro','','CS','',''),(199,'Seychelles','','SC','',''),(200,'Sierra Leone','','SL','',''),(201,'Singapore','','SG','',''),(202,'Slovakia','','SK','',''),(203,'Slovenia','','SI','',''),(204,'Solomon Islands','','SB','',''),(205,'Somalia','','SO','',''),(206,'South Africa','','ZA','',''),(207,'South Georgia and the South Sandwich Isl','','GS','',''),(208,'Spain','','ES','',''),(209,'Sri Lanka','','LK','',''),(210,'Sudan','','SD','',''),(211,'Suriname','','SR','',''),(212,'Svalbard and Jan Mayen','','SJ','',''),(213,'Swaziland','','SZ','',''),(214,'Sweden','','SE','',''),(215,'Switzerland','','CH','',''),(216,'Syrian Arab Republic','','SY','',''),(217,'Taiwan, Province of China','','TW','',''),(218,'Tajikistan','','TJ','',''),(219,'Tanzania, United Republic of','','TZ','',''),(220,'Thailand','','TH','',''),(221,'Timor-Leste','','TL','',''),(222,'Togo','','TG','',''),(223,'Tokelau','','TK','',''),(224,'Tonga','','TO','',''),(225,'Trinidad and Tobago','','TT','',''),(226,'Tunisia','','TN','',''),(227,'Turkey','','TR','',''),(228,'Turkmenistan','','TM','',''),(229,'Turks and Caicos Islands','','TC','',''),(230,'Tuvalu','','TV','',''),(231,'Uganda','','UG','',''),(232,'Ukraine','','UA','',''),(233,'United Arab Emirates','','EA','',''),(234,'United Kingdom','','GB','',''),(235,'United States','','US','',''),(236,'United States Minor Outlying Islands','','UM','',''),(237,'Uruguay','','UY','',''),(238,'Uzbekistan','','UZ','',''),(239,'Vanuatu','','VU','',''),(240,'Venezuela','','VE','',''),(241,'Viet Nam','','VN','',''),(242,'Virgin Islands, British','','VG','',''),(243,'Virgin Islands, U.S.','','VI','',''),(244,'Wallis and Futuna','','WF','',''),(245,'Western Sahara','','EH','',''),(246,'Yemen','','YE','',''),(247,'Zambia','','ZM','',''),(248,'Zimbabwe','','ZW','','');
/*!40000 ALTER TABLE `master_negara` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `master_provinsi`
--

DROP TABLE IF EXISTS `master_provinsi`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `master_provinsi` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `negara_id` int(11) NOT NULL,
  `nama_provinsi` varchar(40) NOT NULL,
  `keterangan` varchar(255) DEFAULT NULL,
  `lt` varchar(100) DEFAULT NULL,
  `lg` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `master_provinsi_negara_id_2ed9437e_fk_master_negara_id` (`negara_id`),
  CONSTRAINT `master_provinsi_negara_id_2ed9437e_fk_master_negara_id` FOREIGN KEY (`negara_id`) REFERENCES `master_negara` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `master_provinsi`
--

LOCK TABLES `master_provinsi` WRITE;
/*!40000 ALTER TABLE `master_provinsi` DISABLE KEYS */;
INSERT INTO `master_provinsi` VALUES (1,1,'Jawa Timur','','',''),(2,1,'Jawa Barat','','',''),(3,1,'Yogyakarta','','',''),(4,1,'Jawa Tengah','','',''),(5,1,'Aceh','','',''),(6,1,'Sumatra Barat','','',''),(7,1,'Sumatra Selatan','','',''),(8,1,'Sumatra Utara','','',''),(9,1,'Riau','','',''),(10,1,'Jambi','','',''),(11,1,'Bengkulu','','',''),(12,1,'Lampung','','',''),(13,1,'Kep. Bangka Belitung','','',''),(14,1,'Kep. Riau','','',''),(15,1,'DKI Jakarta','','',''),(16,1,'Banten','','',''),(17,1,'Bali','','',''),(18,1,'Nusa Tenggara Timur','','',''),(19,1,'Nusa Tenggara Barat','','',''),(20,1,'Kalimantan Barat','','',''),(21,1,'Kalimantan Tengah','','',''),(22,1,'Kalimantan Selatan','','',''),(23,1,'Kalimantan Timur','','',''),(24,1,'Kalimantan Utara','','',''),(25,1,'Sulawesi Utara','','',''),(26,1,'Sulawesi Tenggara','','',''),(27,1,'Sulawesi Selatan','','',''),(28,1,'Sulawesi Tengah','','',''),(29,1,'Sulawesi Barat','','',''),(30,1,'Maluku','','',''),(31,1,'Maluku Utara','','',''),(32,1,'Gorontalo','','',''),(33,1,'Papua','','',''),(34,1,'Papua Barat','','','');
/*!40000 ALTER TABLE `master_provinsi` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `master_settings`
--

DROP TABLE IF EXISTS `master_settings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `master_settings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `parameter` varchar(100) NOT NULL,
  `value` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `master_settings`
--

LOCK TABLES `master_settings` WRITE;
/*!40000 ALTER TABLE `master_settings` DISABLE KEYS */;
/*!40000 ALTER TABLE `master_settings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `perusahaan_bentukkegiatanusaha`
--

DROP TABLE IF EXISTS `perusahaan_bentukkegiatanusaha`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `perusahaan_bentukkegiatanusaha` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `kegiatan_usaha` varchar(255) DEFAULT NULL,
  `keterangan` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `perusahaan_bentukkegiatanusaha`
--

LOCK TABLES `perusahaan_bentukkegiatanusaha` WRITE;
/*!40000 ALTER TABLE `perusahaan_bentukkegiatanusaha` DISABLE KEYS */;
INSERT INTO `perusahaan_bentukkegiatanusaha` VALUES (1,'Mikro',''),(2,'Makro','');
/*!40000 ALTER TABLE `perusahaan_bentukkegiatanusaha` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `perusahaan_jenisbadanusaha`
--

DROP TABLE IF EXISTS `perusahaan_jenisbadanusaha`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `perusahaan_jenisbadanusaha` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `jenis_badan_usaha` varchar(255) NOT NULL,
  `keterangan` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `perusahaan_jenisbadanusaha`
--

LOCK TABLES `perusahaan_jenisbadanusaha` WRITE;
/*!40000 ALTER TABLE `perusahaan_jenisbadanusaha` DISABLE KEYS */;
INSERT INTO `perusahaan_jenisbadanusaha` VALUES (1,'Perseroan Terbatas (PT)',''),(2,'PERSEKUTUAN KOMANDITER (CV)',''),(3,'Firma',''),(4,'PERUSAHAAN PERORANGAN (PO)',''),(5,'Koperasi',''),(6,'BENTUK USAHA LAINNYA (BUL)','');
/*!40000 ALTER TABLE `perusahaan_jenisbadanusaha` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `perusahaan_jenislegalitas`
--

DROP TABLE IF EXISTS `perusahaan_jenislegalitas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `perusahaan_jenislegalitas` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `jenis_legalitas` varchar(100) NOT NULL,
  `keterangan` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `perusahaan_jenislegalitas`
--

LOCK TABLES `perusahaan_jenislegalitas` WRITE;
/*!40000 ALTER TABLE `perusahaan_jenislegalitas` DISABLE KEYS */;
INSERT INTO `perusahaan_jenislegalitas` VALUES (1,'Akta Pendirian',''),(2,'Akta perubahan terakhir',''),(3,'Pengesahan Menteri Hukum dan HAM',''),(4,'Persetujuan Menteri Hukum dan HAM Atas Perubahan Anggaran ',''),(5,'Dasar',''),(6,'Penerimaan Laporan Perubahan Anggaran Dasar',''),(7,'Penerimaan Pemberitahuan Perubahan Direksi/ Komisaris',''),(8,'Pengesahan Menteri Koperasi dan UKM',''),(9,'Persetujuan Menteri Koperasi dan UKM atas Akta Perubahan ',''),(10,'Anggaran Dasar','');
/*!40000 ALTER TABLE `perusahaan_jenislegalitas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `perusahaan_jenispenanamanmodal`
--

DROP TABLE IF EXISTS `perusahaan_jenispenanamanmodal`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `perusahaan_jenispenanamanmodal` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `jenis_penanaman_modal` varchar(255) NOT NULL,
  `keterangan` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `perusahaan_jenispenanamanmodal`
--

LOCK TABLES `perusahaan_jenispenanamanmodal` WRITE;
/*!40000 ALTER TABLE `perusahaan_jenispenanamanmodal` DISABLE KEYS */;
INSERT INTO `perusahaan_jenispenanamanmodal` VALUES (1,' PMA ','Penanaman Modal Asing'),(2,'PMDN','Penanaman Modal Dalam Negeri');
/*!40000 ALTER TABLE `perusahaan_jenispenanamanmodal` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `perusahaan_jenisperusahaan`
--

DROP TABLE IF EXISTS `perusahaan_jenisperusahaan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `perusahaan_jenisperusahaan` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `jenis_perusahaan` varchar(255) NOT NULL,
  `keterangan` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `perusahaan_jenisperusahaan`
--

LOCK TABLES `perusahaan_jenisperusahaan` WRITE;
/*!40000 ALTER TABLE `perusahaan_jenisperusahaan` DISABLE KEYS */;
/*!40000 ALTER TABLE `perusahaan_jenisperusahaan` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `perusahaan_kbli`
--

DROP TABLE IF EXISTS `perusahaan_kbli`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `perusahaan_kbli` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `kode_kbli` int(11) NOT NULL,
  `nama_kbli` varchar(255) NOT NULL,
  `keterangan` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `perusahaan_kbli`
--

LOCK TABLES `perusahaan_kbli` WRITE;
/*!40000 ALTER TABLE `perusahaan_kbli` DISABLE KEYS */;
INSERT INTO `perusahaan_kbli` VALUES (1,7,'SIUP',''),(2,4,'gggh','');
/*!40000 ALTER TABLE `perusahaan_kbli` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `perusahaan_kelembagaan`
--

DROP TABLE IF EXISTS `perusahaan_kelembagaan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `perusahaan_kelembagaan` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `kelembagaan` varchar(255) NOT NULL,
  `keterangan` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `perusahaan_kelembagaan`
--

LOCK TABLES `perusahaan_kelembagaan` WRITE;
/*!40000 ALTER TABLE `perusahaan_kelembagaan` DISABLE KEYS */;
INSERT INTO `perusahaan_kelembagaan` VALUES (1,'Mikro',''),(2,'Kecil',''),(3,'Menengah',''),(4,'Besar','');
/*!40000 ALTER TABLE `perusahaan_kelembagaan` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `perusahaan_legalitas`
--

DROP TABLE IF EXISTS `perusahaan_legalitas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `perusahaan_legalitas` (
  `atributtambahan_ptr_id` int(11) NOT NULL,
  `nama_notaris` varchar(100) NOT NULL,
  `alamat` varchar(255) DEFAULT NULL,
  `telephone` varchar(50) DEFAULT NULL,
  `nomor_pengesahan` varchar(30) DEFAULT NULL,
  `tanggal_pengesahan` date DEFAULT NULL,
  `keterangan` varchar(255) DEFAULT NULL,
  `berkas_id` int(11) DEFAULT NULL,
  `jenis_legalitas_id` int(11) DEFAULT NULL,
  `perusahaan_id` int(11) NOT NULL,
  PRIMARY KEY (`atributtambahan_ptr_id`),
  KEY `perus_berkas_id_19e77bc1_fk_master_berkas_atributtambahan_ptr_id` (`berkas_id`),
  KEY `perus_jenis_legalitas_id_114f8d0_fk_perusahaan_jenislegalitas_id` (`jenis_legalitas_id`),
  KEY `perusahaan_legalitas_2b796e8b` (`perusahaan_id`),
  CONSTRAINT `afefb3c809c0d7372632039b272c4300` FOREIGN KEY (`perusahaan_id`) REFERENCES `perusahaan_perusahaan` (`atributtambahan_ptr_id`),
  CONSTRAINT `perus_berkas_id_19e77bc1_fk_master_berkas_atributtambahan_ptr_id` FOREIGN KEY (`berkas_id`) REFERENCES `master_berkas` (`atributtambahan_ptr_id`),
  CONSTRAINT `perus_jenis_legalitas_id_114f8d0_fk_perusahaan_jenislegalitas_id` FOREIGN KEY (`jenis_legalitas_id`) REFERENCES `perusahaan_jenislegalitas` (`id`),
  CONSTRAINT `per_atributtambahan_ptr_id_56345f92_fk_master_atributtambahan_id` FOREIGN KEY (`atributtambahan_ptr_id`) REFERENCES `master_atributtambahan` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `perusahaan_legalitas`
--

LOCK TABLES `perusahaan_legalitas` WRITE;
/*!40000 ALTER TABLE `perusahaan_legalitas` DISABLE KEYS */;
INSERT INTO `perusahaan_legalitas` VALUES (395,'Gilang','ngancar','123','1234','2016-10-04',NULL,NULL,1,394),(396,'Gilang','ngancar','123','1234','2016-10-04',NULL,NULL,1,394),(397,'Gilang','ngancar','123','1234','2016-10-04',NULL,NULL,1,394),(398,'Gilang','ngancar','123','1234','2016-10-04',NULL,NULL,1,394),(399,'Nur ','er','12','10239','2016-10-04',NULL,NULL,2,394),(400,'Gilang','ngancar','123','1234','2016-10-04',NULL,409,1,394),(401,'Nur ','er','12','10239','2016-10-04',NULL,NULL,2,394),(402,'Gilang','ngancar','123','1234','2016-10-04',NULL,NULL,1,394),(403,'Nur ','er','12','10239','2016-10-04',NULL,405,2,394),(417,'23','ad','asd','123','2016-10-05',NULL,NULL,1,413),(418,'23','ad','asd','123','2016-10-05',NULL,NULL,1,413),(419,'23','ad','23','213','2016-10-05',NULL,NULL,1,413),(420,'23','ad','23','213','2016-10-05',NULL,NULL,1,413),(421,'23','ad','23','213','2016-10-05',NULL,NULL,1,413),(422,'23','ad','23','213','2016-10-05',NULL,NULL,1,413),(423,'23','ad','23','213','2016-10-05',NULL,NULL,1,413),(424,'23','ad','23','213','2016-10-05',NULL,NULL,1,413),(425,'12123','213','12','e123','2016-10-19',NULL,NULL,2,413),(426,'3423423','23123','23','213','2016-10-05',NULL,NULL,1,413),(427,'12123','213','12','e123','2016-10-19',NULL,NULL,2,413),(428,'3423423','23123','23','213','2016-10-05',NULL,NULL,1,413),(429,'3423423','23123','23','213','2016-10-05',NULL,NULL,1,413),(430,'3423423','23123','23','213','2016-10-05',NULL,NULL,1,413),(431,'3423423','23123','23','213','2016-10-05',NULL,NULL,1,413),(432,'3423423','23123','23','213','2016-10-05',NULL,NULL,1,413),(433,'3423423','23123','23','213','2016-10-05',NULL,NULL,1,413),(434,'12123','213','12','e123','2016-10-19',NULL,NULL,2,413),(435,'3423423','23123','23','213','2016-10-05',NULL,NULL,1,413),(436,'3423423','23123','23','213','2016-10-05',NULL,NULL,1,413),(437,'3423423','23123','23','213','2016-10-05',NULL,NULL,1,413),(438,'3423423','23123','23','213','2016-10-05',NULL,NULL,1,413),(439,'3423423','23123','23','213','2016-10-05',NULL,NULL,1,413),(440,'3423423','23123','23','213','2016-10-05',NULL,NULL,1,413),(441,'3423423','23123','23','213','2016-10-05',NULL,NULL,1,413),(442,'12123','213','12','e123','2016-10-19',NULL,NULL,2,413),(443,'3423423','23123','23','213','2016-10-05',NULL,NULL,1,413),(444,'3423423','23123','23','213','2016-10-05',NULL,NULL,1,413),(445,'12123','213','12','e123','2016-10-19',NULL,NULL,2,413),(446,'3423423','23123','23','213','2016-10-05',NULL,NULL,1,413),(447,'12123','213','12','e123','2016-10-19',NULL,NULL,2,413),(448,'3423423','23123','23','213','2016-10-05',NULL,NULL,1,413),(449,'3423423','23123','23','213','2016-10-05',NULL,NULL,1,413),(450,'12123','213','12','e123','2016-10-19',NULL,NULL,2,413),(451,'3423423','23123','23','213','2016-10-05',NULL,NULL,1,413),(452,'3423423','23123','23','213','2016-10-05',NULL,NULL,1,413),(453,'3423423','23123','23','213','2016-10-05',NULL,NULL,1,413),(454,'12123','213','12','e123','2016-10-19',NULL,NULL,2,413),(455,'3423423','23123','23','213','2016-10-05',NULL,NULL,1,413),(456,'3423423','23123','23','213','2016-10-05',NULL,NULL,1,413),(457,'3423423','23123','23','213','2016-10-05',NULL,NULL,1,413),(458,'3423423','23123','23','213','2016-10-05',NULL,NULL,1,413),(459,'12123','213','12','e123','2016-10-19',NULL,NULL,2,413),(460,'gsahdkj','kksjdk','12','123','2016-10-15',NULL,NULL,1,413),(461,'gsahdkj','kksjdk','12','123','2016-10-15',NULL,NULL,1,413),(462,'gsahdkj','kksjdk','12','123','2016-10-15',NULL,NULL,1,413),(463,'gsahdkj','kksjdk','12','123','2016-10-15',NULL,NULL,1,413),(464,'gsahdkj','kksjdk','12','123','2016-10-15',NULL,NULL,1,413),(465,'gsahdkj','kksjdk','12','123','2016-10-15',NULL,NULL,1,413),(466,'213','13','123','123','2016-10-28',NULL,NULL,1,413),(467,'213','13','123','123','2016-10-28',NULL,NULL,1,413),(468,'213','13','123','123','2016-10-28',NULL,NULL,1,413),(469,'4234','234','234','24','2016-10-24',NULL,NULL,2,413),(470,'213','13','123','123','2016-10-28',NULL,NULL,1,413),(471,'213','13','123','123','2016-10-28',NULL,NULL,1,413),(472,'213','13','123','123','2016-10-28',NULL,NULL,1,413),(473,'213','13','123','123','2016-10-28',NULL,NULL,1,413),(474,'4234','234','234','24','2016-10-24',NULL,NULL,2,413),(475,'213','13','123','123','2016-10-28',NULL,NULL,1,413),(476,'213','13','123','123','2016-10-28',NULL,NULL,1,413),(477,'213','13','123','123','2016-10-28',NULL,NULL,1,413),(509,'kediri','asd','09876','1234','2016-10-06',NULL,514,1,508),(540,'roro','jalan hayamuruk','68777','12345','2016-10-06',NULL,545,1,539),(564,'RGDFSD','KEDIRI','5 OKT','13','2016-10-06',NULL,569,1,563);
/*!40000 ALTER TABLE `perusahaan_legalitas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `perusahaan_perusahaan`
--

DROP TABLE IF EXISTS `perusahaan_perusahaan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `perusahaan_perusahaan` (
  `atributtambahan_ptr_id` int(11) NOT NULL,
  `nama_perusahaan` varchar(100) NOT NULL,
  `alamat_perusahaan` varchar(255) NOT NULL,
  `lt` varchar(100) DEFAULT NULL,
  `lg` varchar(100) DEFAULT NULL,
  `kode_pos` varchar(50) DEFAULT NULL,
  `telepon` varchar(50) NOT NULL,
  `fax` varchar(20) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `npwp` varchar(100) NOT NULL,
  `desa_id` int(11) NOT NULL,
  `perusahaan_induk_id` int(11) DEFAULT NULL,
  `perusahaan_lama_id` int(11) DEFAULT NULL,
  `keterangan` varchar(255) DEFAULT NULL,
  `nama_grup` varchar(100) DEFAULT NULL,
  `penanggung_jawab_id` int(11) DEFAULT NULL,
  `berkas_npwp_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`atributtambahan_ptr_id`),
  UNIQUE KEY `npwp` (`npwp`),
  KEY `perusahaan_perusahaan_desa_id_47aecf69_fk_master_desa_id` (`desa_id`),
  KEY `cc4f471f2fa3f52ad18f73277e69e2cb` (`perusahaan_induk_id`),
  KEY `D107d25fe4e9552532683cbaf981acfb` (`perusahaan_lama_id`),
  KEY `perusahaan_perusahaan_95ad12fd` (`penanggung_jawab_id`),
  KEY `perusahaan_perusahaan_fae0bfe7` (`berkas_npwp_id`),
  CONSTRAINT `cc4f471f2fa3f52ad18f73277e69e2cb` FOREIGN KEY (`perusahaan_induk_id`) REFERENCES `perusahaan_perusahaan` (`atributtambahan_ptr_id`),
  CONSTRAINT `D107d25fe4e9552532683cbaf981acfb` FOREIGN KEY (`perusahaan_lama_id`) REFERENCES `perusahaan_perusahaan` (`atributtambahan_ptr_id`),
  CONSTRAINT `perusahaan_perusahaan_desa_id_47aecf69_fk_master_desa_id` FOREIGN KEY (`desa_id`) REFERENCES `master_desa` (`id`),
  CONSTRAINT `peru_penanggung_jawab_id_1fb07c44_fk_izin_pemohon_account_ptr_id` FOREIGN KEY (`penanggung_jawab_id`) REFERENCES `izin_pemohon` (`account_ptr_id`),
  CONSTRAINT `per_atributtambahan_ptr_id_6f79acbf_fk_master_atributtambahan_id` FOREIGN KEY (`atributtambahan_ptr_id`) REFERENCES `master_atributtambahan` (`id`),
  CONSTRAINT `p_berkas_npwp_id_c73a81f_fk_master_berkas_atributtambahan_ptr_id` FOREIGN KEY (`berkas_npwp_id`) REFERENCES `master_berkas` (`atributtambahan_ptr_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `perusahaan_perusahaan`
--

LOCK TABLES `perusahaan_perusahaan` WRITE;
/*!40000 ALTER TABLE `perusahaan_perusahaan` DISABLE KEYS */;
INSERT INTO `perusahaan_perusahaan` VALUES (394,'SEO','ajsd','','','','085233334','','','12.345.678.9-012.344',378,NULL,NULL,'','',392,408),(413,'SEO','akds',NULL,NULL,'','13','','','18.748.972.3-498.293',18,NULL,NULL,NULL,'',392,NULL),(508,'SEO Foundantion','KEdiri',NULL,NULL,'','09876','','','12.386.868.8-686.868',287,NULL,NULL,NULL,'',505,513),(522,'jlkljlkasdj','sdasdasd',NULL,NULL,'','12123','','','12.764.129.8-312.839',18,NULL,NULL,NULL,'',392,NULL),(539,'MAju Mundur','jalan sri',NULL,NULL,'12345','677757','','','12.349.828.9-323.848',75,NULL,NULL,NULL,'',533,544),(563,'\"INDAH JAYA\" TOKO','Dsn. Kuwik RT 002/RW 002',NULL,NULL,'','08133432352335','','','44.089.802.1-655.000',129,NULL,NULL,NULL,'',557,568);
/*!40000 ALTER TABLE `perusahaan_perusahaan` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `perusahaan_produkutama`
--

DROP TABLE IF EXISTS `perusahaan_produkutama`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `perusahaan_produkutama` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `barang_jasa_utama` varchar(255) NOT NULL,
  `keterangan` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `perusahaan_produkutama`
--

LOCK TABLES `perusahaan_produkutama` WRITE;
/*!40000 ALTER TABLE `perusahaan_produkutama` DISABLE KEYS */;
INSERT INTO `perusahaan_produkutama` VALUES (1,'Komputer',''),(2,'hhhhhhhh',''),(3,'sego pecel',''),(4,'sego kuning','');
/*!40000 ALTER TABLE `perusahaan_produkutama` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-10-07 10:33:08
