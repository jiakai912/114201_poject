-- MySQL dump 10.13  Distrib 8.0.19, for Win64 (x86_64)
--
-- Host: localhost    Database: north
-- ------------------------------------------------------
-- Server version	8.0.40

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `customer`
--

DROP TABLE IF EXISTS `customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customer` (
  `cusNo` char(4) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `cusName` varchar(30) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `contactor` varchar(10) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `title` varchar(10) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `address` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `city` varchar(10) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `area` varchar(10) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `zip` char(5) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `tel` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `fax` varchar(20) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `photo` varchar(100) COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`cusNo`),
  UNIQUE KEY `cusNoIndex` (`cusNo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer`
--

LOCK TABLES `customer` WRITE;
/*!40000 ALTER TABLE `customer` DISABLE KEYS */;
INSERT INTO `customer` VALUES ('C005','喻台生機械','李先生','訂貨員','花蓮市花蓮路98號','花蓮市','花蓮區','15985','(06) 245-9636','(06) 245-9635',NULL),('C006','琴花卉','劉先生','業務','宜蘭市經國路55號','宜蘭市','經國區','68306','(07) 556-6665','(07) 556-6665',NULL),('C007','皓國廣兌','方先生','行銷專員','新竹市永平路一段1號','新竹市','永平區','67000','(08) 889-6698','(08) 889-6699',NULL),('C008','邁多貿易','劉先生','董事長','台北市北平東路24號','台北市','北平區','28023','(02) 221-2555','(02) 221-2556',NULL),('C009','琴攝影','謝小姐','董事長','台北市北平東路24號3樓之一','台北市','北平區','13008','(03) 247-9682','(03) 247-9684',NULL),('C010','中央開發','王先生','會計人員','新竹市竹北路8號','新竹市','竹北區','10058','(04) 358-6932','(04) 358-6935',NULL),('C011','宇奏雜誌','徐先生','業務','台中市中港路一段78號','台中市','中港區','14754','(05) 999-7788','(05) 999-7783',NULL),('C012','威航貨運承攬有限公司','李先生','業務助理','南投縣石牌鄉南投路5號','南投縣','南投區','10105','(06) 852-9636','(06) 852-9638',NULL),('C013','三捷實業','林小姐','研發人員','屏東縣當文鄉永大路4號','屏東縣','永大區','05022','(07) 223-6665','(07) 223-6664',NULL),('C014','嗨天旅行社','林小姐','董事長','屏東市中山路7號','屏東市','中山區','30126','(08) 784-6698','(08) 784-6697',NULL),('C015','美國運海','鍾小姐','船務','桃園縣富國路42號','桃園縣','富國區','07554','(02) 555-7647','(02) 555-7646',NULL),('C016','萬海','劉先生','業務','苗栗縣樹腳鄉中正路二段二樓','苗栗縣','中正區','12209','(02) 968-9612','(02) 968-9613',NULL),('C017','世邦','方先生','董事長','台北市忠孝東路三段2號','台北市','忠孝區','05021','(03) 862-7782','(03) 862-7784',NULL),('C018','敦郼斯船舶','劉先生','董事長','台中市仁愛路四段180號','台中市','仁愛區','05023','(04) 255-6932','(04) 255-6932',NULL),('C019','中國通','謝小姐','業務','高雄市中正路四段65號','高雄市','中正區','10006','(05) 544-7788','(05) 544-7788',NULL),('C020','正人資源','王先生','訂貨員','台北縣北新路11號','台北縣','北新區','15985','(06) 245-9556','(06) 245-9556',NULL),('C021','紅陽事業','徐先生','業務','花蓮市花中路15號','花蓮市','花中區','68306','(07) 246-6665','(07) 246-6665',NULL),('C022','嘉元實業','周先生','行銷專員','宜蘭市經國路38號','宜蘭市','經國區','67000','(08) 889-6638','(08) 889-6638',NULL),('C023','路福村','方先生','董事長','新竹市永平路7號','新竹市','永平區','28023','(02) 255-2555','(02) 255-2555',NULL),('C024','雅洲信託','陳先生','董事長','台北市北平東路64號','台北市','北平區','13008','(03) 277-9682','(03) 277-9682',NULL),('C025','棕國信託','余小姐','會計人員','台北市北平東路42號3樓之一','台北市','北平區','10058','(04) 391-6932','(04) 391-6932',NULL),('C026','信華銀行','蘇先生','業務','新竹市竹北路8號','新竹市','竹北區','14754','(05) 937-7588','(05) 937-7588',NULL),('C027','茶打銀行','成先生','業務助理','台中市中港路一段78號','台中市','中港區','10105','(06) 882-9636','(06) 882-9636',NULL),('C028','第二銀行','林小姐','研發人員','南投縣石牌鄉南投路5號','南投縣','南投區','05022','(07) 852-6665','(07) 852-6664',NULL),('C029','山山銀行','林小姐','董事長','屏東縣水果鄉永大路4號','屏東縣','永大區','30126','(08) 664-6698','(08) 664-6698',NULL),('C030','灣台銀行','鍾小姐','船務','屏東市中山路7號','屏東市','中山區','07554','(02) 895-7647','(02) 895-7647',NULL),('C031','泰安銀行','劉先生','業務','桃園縣富國路42號','桃園縣','富國區','04876','(08) 664-6698','(08) 664-6698',NULL),('C032','小中企銀','方先生','董事長','台北市忠孝東路四段32號','台北市','忠孝區','97403','(02) 968-9652','(02) 968-9653',NULL),('C033','南華銀行','劉先生','董事長','台中市仁愛路二段120號','台中市','仁愛區','10814','(03) 862-9682','(03) 862-9682',NULL),('C034','合作金庫','謝小姐','業務','高雄市中正路一段12號','高雄市','中正區','05454','(04) 256-6932','(04) 256-6931',NULL),('C035','東遠銀行','王先生','訂貨員','台北縣中新路11號','台北縣','中新區','50222','(05) 555-7788','(05) 555-7788',NULL),('C036','五金機械','徐先生','業務','花蓮市花蓮路98號','花蓮市','花蓮區','97827','(06) 245-9636','(06) 245-9636',NULL),('C037','師大貿易','周先生','行銷專員','宜蘭市經國路55號','宜蘭市','經國區','30126','(07) 556-6665','(07) 556-6665',NULL),('C038','鑫增貿易','方先生','董事長','新竹市永平路一段1號','新竹市','永平區','07554','(08) 889-6698','(08) 889-6699',NULL),('C039','業永房屋','陳先生','董事長','台北市北平東路24號','台北市','北平區','14776','(02) 221-2555','(02) 221-2555',NULL),('C040','霸力建設','余小姐','會計人員','台北市北平東路24號3樓之一','台北市','北平區','78000','(03) 247-9682','(03) 247-9686',NULL),('C041','池春建設','蘇先生','業務','新竹市竹北路8號','新竹市','竹北區','31000','(04) 358-6932','(04) 358-6932',NULL),('C042','和福建設','成先生','業務助理','台中市中港路一段78號','台中市','中港區','30126','(05) 999-7788','(05) 999-7788',NULL),('C043','春永建設','何先生','研發人員','南投縣南投路5號','南投縣','南投區','07554','(06) 852-9636','(06) 852-9636',NULL),('C044','幸義房屋','黎先生','董事長','屏東縣永大路4號','屏東縣','永大區','60528','(07) 223-6665','(07) 223-6667',NULL),('C045','興中保險','唐小姐','船務','屏東市中山路7號','屏東市','中山區','94117','(08) 784-6698','(08) 784-6698',NULL),('C046','山南人壽','陳玉美','業務','桃園縣富國路77號','桃園縣','富國區','35081','(02) 555-7647','(02) 555-7647',NULL),('C047','保信人壽','黃雅玲','董事長','台北市忠孝東路四段32號','台北市','忠孝區','49801','(02) 968-9652','(02) 968-9652',NULL),('C048','大華城台北','胡繼堯','董事長','台中市仁愛路二段120號','台中市','仁愛區','97219','(03) 862-9682','(03) 862-9682',NULL),('C049','陽林','王炫皓','業務','高雄市中正路一段12號','高雄市','中正區','24100','(04) 256-6932','(04) 256-6932',NULL),('C050','悅海','李柏麟','訂貨員','台北縣中新路11號','台北縣','中新區','30126','(05) 555-7788','(05) 555-7788',NULL),('C051','資鬙','劉維國','業務','花蓮市花蓮路98號','花蓮市','花蓮區','07554','(06) 245-9636','(06) 245-9636',NULL),('C052','仲堂企業','方建文','行銷專員','宜蘭市經國路55號','宜蘭市','經國區','04179','(07) 556-6665','(07) 556-6665',NULL),('C053','富同企業','劉小龍','董事長','新竹市永平路一段1號','新竹市','永平區','30126','(08) 889-6698','(08) 889-6698',NULL),('C054','台利材料','謝麗秋','董事長','台北市北平東路24號','台北市','北平區','07554','(02) 221-2555','(02) 221-2555',NULL),('C055','瑞棧藝品','王俊元','會計人員','台北市北平東路24號3樓之一','台北市','北平區','99508','(03) 247-9682','(03) 247-9682',NULL),('C056','一詮精密工業','徐文彬','業務','新竹市竹北路8號','新竹市','竹北區','50739','(04) 358-6932','(04) 358-6932',NULL),('C057','立日股份有限公司','李良駿','業務助理','台中市中港路一段78號','台中市','中港區','75012','(05) 999-7788','(05) 999-7788',NULL),('C058','就業廣兌','林慧音','研發人員','南投縣南投路5號','南投縣','南投區','05033','(06) 852-9636','(06) 852-9636',NULL),('C059','頂上系統','林麗莉','董事長','屏東縣永大路4號','屏東縣','永大區','50200','(07) 223-6665','(07) 223-6665',NULL),('C060','康毅系統','鍾彩瑜','船務','屏東市中山路7號','屏東市','中山區','17560','(08) 784-6698','(08) 784-6698',NULL),('C061','蘭格英語','劉先生','業務助理','桃園縣富國路42號','桃園縣','富國區','02389','(02) 555-7647','(02) 555-7647',NULL),('C062','加美留學中心','方先生','研發人員','台北市忠孝東路四段32號','台北市','忠孝區','05487','(02) 968-9652','(02) 968-9652',NULL),('C063','高上補習班','劉先生','董事長','台中市仁愛路二段120號','台中市','仁愛區','01307','(03) 862-9682','(03) 862-9682',NULL),('C064','大東海補班','謝小姐','船務','高雄市中正路一段12號','高雄市','中正區','10101','(04) 256-6932','(04) 256-6932',NULL),('C065','學仁貿易','王先生','業務','台北縣中新路11號','台北縣','中新區','87110','(05) 555-7788','(05) 555-7788',NULL),('C066','建國科技','徐先生','董事長','花蓮市花蓮路98號','花蓮市','花蓮區','42100','(06) 245-9636','(06) 245-9636',NULL),('C067','宇欣實業','周先生','董事長','宜蘭市經國路55號','宜蘭市','經國區','02389','(07) 556-6665','(07) 556-6665',NULL),('C068','永大大企業','方先生','業務','新竹市永平路一段1號','新竹市','永平區','12031','(08) 889-6698','(08) 889-6699',NULL),('C069','德化食品','陳先生','訂貨員','台北市北平東路24號','台北市','北平區','28001','(02) 221-2555','(02) 221-2555',NULL),('C070','漢光企管','余小姐','業務','台北市北平東路24號3樓之一','台北市','北平區','41101','(03) 247-9682','(03) 247-9683',NULL),('C071','大鈺貿易','蘇先生','行銷專員','新竹市竹北路8號','新竹市','竹北區','83720','(04) 358-6932','(04) 358-6932',NULL),('C072','艾德高科技','成先生','董事長','台中市中港路一段78號','台中市','中港區','30126','(05) 999-7788','(05) 999-7789',NULL),('C074','賜芳股份','黎先生','會計人員','屏東縣永大路4號','屏東縣','永大區','75016','(07) 223-6665','(07) 223-6664',NULL),('C075','昇昕股份有限公司','唐小姐','業務','屏東市中山路7號','屏東市','中山區','82520','(08) 784-6698','(08) 784-6699',NULL),('C076','福星製衣廠股份有限公司','劉先生','業務助理','桃園縣富國路42號','桃園縣','富國區','60000','(02) 555-7647','(02) 555-7647',NULL),('C077','上河工業','方先生','研發人員','台北市忠孝東路四段32號','台北市','忠孝區','97201','(02) 968-9652','(02) 968-9652',NULL),('C078','新巨企業','劉先生','董事長','台中市仁愛路二段120號','台中市','仁愛區','59801','(03) 862-9682','(03) 862-9682',NULL),('C080','協昌妮絨有限公司','王先生','業務','台北縣中新路11號','台北縣','中新區','05033','(05) 555-7788','(05) 555-7788',NULL),('C081','亞太公司','徐先生','董事長','花蓮市花蓮路98號','花蓮市','花蓮區','05634','(06) 245-9636','(06) 245-9636',NULL),('C082','伸格公司','周先生','董事長','宜蘭市經國路55號','宜蘭市','經國區','98034','(07) 556-6665','(07) 556-6665',NULL),('C083','中碩貿易','方先生','業務','新竹市永平路一段1號','新竹市','永平區','82001','(08) 889-6698','(08) 889-6698',NULL),('C084','千固','陳先生','訂貨員','台北市北平東路24號','台北市','北平區','69004','(02) 221-2555','(02) 221-2555',NULL),('C085','山泰企業','余小姐','業務','台北市北平東路24號3樓之一','台北市','北平區','51100','(03) 247-9682','(03) 247-9682',NULL),('C086','凱旋科技','蘇先生','行銷專員','新竹市竹北路8號','新竹市','竹北區','70563','(04) 358-6932','(04) 358-6932',NULL),('C087','升格企業','成先生','董事長','台中市中港路一段78號','台中市','中港區','90110','(05) 999-7788','(05) 999-7788',NULL),('C088','凱誠國際顧問公司','何先生','董事長','南投縣南投路5號','南投縣','南投區','08737','(06) 852-9636','(06) 852-9635',NULL),('C089','椅天文化事業','黎先生','會計人員','屏東縣永大路4號','屏東縣','永大區','98128','(07) 223-6665','(07) 223-6667',NULL),('C090','志遠有限公司','唐小姐','業務','屏東市中山路7號','屏東市','中山區','21240','(08) 784-6698','(08) 784-6697',NULL),('C091','漢典電機','吳小姐','業務','桃園縣富國路42號','桃園縣','富國區','01012','(02) 555-7647','(02) 555-7645',NULL),('C092','二鄰五金行','陳清煜','董事長','台北市民權東路三段15號十樓','台北市','松山區','10606','(02)5087883','(02)5087884',NULL);
/*!40000 ALTER TABLE `customer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employee`
--

DROP TABLE IF EXISTS `employee`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employee` (
  `empNo` char(4) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `empName` varchar(10) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `title` varchar(20) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `birthday` date DEFAULT NULL,
  `address` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `city` varchar(10) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `area` varchar(10) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `zip` char(5) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `tel` varchar(20) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `ext` varchar(10) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `password` char(10) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `baseSalary` int DEFAULT NULL,
  PRIMARY KEY (`empNo`),
  UNIQUE KEY `emNoIndex` (`empNo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employee`
--

LOCK TABLES `employee` WRITE;
/*!40000 ALTER TABLE `employee` DISABLE KEYS */;
INSERT INTO `employee` VALUES ('E001','張瑾雯','業務','1968-12-08','北市仁愛路二段56號','台北市','中山','98122','(02) 2555-9857','5467','ameiou',35000),('E002','陳季暄','業務經理','1952-02-19','北市敦化南路一段1號','台北市','大同','98401','(02) 2555-9482','3457','hjyu',42000),('E003','趙飛燕','業務','1963-08-30','北市忠孝東路四段4 號','台北市','松山','98033','(02) 2555-3412','3355','dqxxs',43000),('E004','林美麗','業務','1958-09-19','北市南京東路三段3號','台北市','景美','98052','(02) 2555-8122','5176','ewtew',25000),('E005','劉天王','業務經理','1955-03-04','北市北平東路24號','台北市','松山','98552','(02) 2555-4848','3453','abhyu',13000),('E006','黎國明','業務','1963-07-02','北市中山北路六段88號','台北市','中山','15524','(02) 2555-7773','4281','kkmntr',32100),('E007','郭國臹','業務','1960-05-29','北市師大路67號','台北市','大同','55555','(02) 2555-5598','4651','deaea',32100),('E008','蘇涵蘊','業務主管','1958-01-09','北市紹興南路99號','台北市','信義','88888','(02) 2555-1189','2344','qgyjnn',33000),('E009','孟庭亭','業務','1969-07-02','北市信義路二段120號','台北市','大同','33333','(02) 2555-4444','4521','tryyuk',45000),('E010','賴俊良','資深工程師','1972-12-06','北市北平東路24 號3 樓之一','台北市','信義','11112','(02) 2322-4932','221','cxxzdgh',21000),('E011','何大樓','助手','1961-12-06','北市北平東路24 號3 樓之一','台北市','景美','53432','(02) 2322-4932','098','ytrghf',44000),('E012','王大德','工程師','1968-12-14','北市北平東路24 號3 樓之一','台北市','內湖','53432','(02) 2322-4931','190','tykgfrf',34000);
/*!40000 ALTER TABLE `employee` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `intern`
--

DROP TABLE IF EXISTS `intern`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `intern` (
  `tno` char(4) NOT NULL,
  `name` varchar(30) DEFAULT NULL,
  `age` int DEFAULT NULL,
  `school` varchar(100) DEFAULT NULL,
  `empNo` char(4) DEFAULT NULL,
  `jobs` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`tno`),
  KEY `intern_employee_FK` (`empNo`),
  CONSTRAINT `intern_employee_FK` FOREIGN KEY (`empNo`) REFERENCES `employee` (`empNo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `intern`
--

LOCK TABLES `intern` WRITE;
/*!40000 ALTER TABLE `intern` DISABLE KEYS */;
INSERT INTO `intern` VALUES ('T001','abc',20,'ntub','E001','python'),('T002','DEF',19,'NTUB','E012','C'),('T003','ABC2',21,'NTU',NULL,'C');
/*!40000 ALTER TABLE `intern` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orddetails`
--

DROP TABLE IF EXISTS `orddetails`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orddetails` (
  `id` int NOT NULL AUTO_INCREMENT,
  `ordNo` char(5) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `proNo` char(4) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `amt` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `odNoFKey` (`ordNo`),
  KEY `proNoFKey` (`proNo`),
  CONSTRAINT `ordNoFKey` FOREIGN KEY (`ordNo`) REFERENCES `ordmaster` (`ordNo`),
  CONSTRAINT `proNoFKey` FOREIGN KEY (`proNo`) REFERENCES `product` (`proNo`)
) ENGINE=InnoDB AUTO_INCREMENT=2219 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orddetails`
--

LOCK TABLES `orddetails` WRITE;
/*!40000 ALTER TABLE `orddetails` DISABLE KEYS */;
INSERT INTO `orddetails` VALUES (1,'10294','P001',18),(2,'10294','P002',4),(3,'10294','P003',40);
/*!40000 ALTER TABLE `orddetails` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ordmaster`
--

DROP TABLE IF EXISTS `ordmaster`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ordmaster` (
  `ordNo` char(5) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `cusNo` char(4) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `empNo` char(4) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `ordDate` date DEFAULT NULL,
  `transFee` int DEFAULT NULL,
  PRIMARY KEY (`ordNo`),
  UNIQUE KEY `omNoIndex` (`ordNo`),
  KEY `cusNoFKey` (`cusNo`),
  KEY `empNoFKey` (`empNo`),
  CONSTRAINT `cusNoFKey` FOREIGN KEY (`cusNo`) REFERENCES `customer` (`cusNo`),
  CONSTRAINT `empNoFKey` FOREIGN KEY (`empNo`) REFERENCES `employee` (`empNo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ordmaster`
--

LOCK TABLES `ordmaster` WRITE;
/*!40000 ALTER TABLE `ordmaster` DISABLE KEYS */;
INSERT INTO `ordmaster` VALUES ('10294','C085','E005','2024-07-04',32);
/*!40000 ALTER TABLE `ordmaster` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product`
--

DROP TABLE IF EXISTS `product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product` (
  `proNo` char(4) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `proName` varchar(20) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `supNo` char(4) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `typNo` char(4) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `price` int DEFAULT NULL,
  `stockAmt` int DEFAULT NULL,
  `orderAmt` int DEFAULT NULL,
  `safeAmt` int DEFAULT NULL,
  `inventoryDate` date DEFAULT NULL,
  `picture` char(60) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`proNo`),
  UNIQUE KEY `proNoIndex` (`proNo`),
  KEY `proNameIndex` (`proName`),
  KEY `supNoFKey` (`supNo`),
  KEY `typNoFKey` (`typNo`),
  CONSTRAINT `supNoFKey` FOREIGN KEY (`supNo`) REFERENCES `supplier` (`supNo`),
  CONSTRAINT `typNoFKey` FOREIGN KEY (`typNo`) REFERENCES `protype` (`typNo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product`
--

LOCK TABLES `product` WRITE;
/*!40000 ALTER TABLE `product` DISABLE KEYS */;
INSERT INTO `product` VALUES ('P001','蘋果汁','S001','T001',50,39,0,10,'2024-05-01',NULL),('P002','牛奶','S001','T001',65,17,40,25,'2024-05-01',NULL),('P003','蕃茄醬','S001','T002',85,13,70,25,'2024-05-01',NULL),('P004','海鹽','S002','T002',40,53,0,10,'2024-05-01',NULL),('P005','麻油','S002','T002',55,0,0,10,'2024-05-01',NULL),('P006','醬油','S003','T002',85,120,0,25,'2024-05-01',NULL),('P007','海鮮粉','S003','T007',180,15,0,10,'2024-04-25',NULL),('P008','胡椒粉','S003','T002',90,6,0,10,'2024-05-01',NULL),('P009','讚油雞','S004','T006',250,29,0,10,'2024-05-10',NULL),('P010','大甲蟹','S004','T008',300,31,0,10,'2024-05-10',NULL),('P011','民眾起司','S005','T004',150,22,30,30,'2024-05-01',NULL),('P012','德國起司','S005','T004',210,86,0,10,'2024-05-10',NULL),('P013','龍蝦','S006','T008',500,24,0,5,'2024-05-10',NULL),('P014','沙茶','S006','T007',120,35,0,10,'2024-04-15',NULL),('P015','味素','S006','T002',50,39,0,5,'2024-05-01',NULL),('P016','餅乾','S007','T003',45,29,0,10,'2024-05-01',NULL),('P017','糙米','S007','T006',90,0,0,10,'2024-05-01',NULL),('P018','墨魚','S007','T008',160,42,0,10,'2024-04-25',NULL),('P019','糖果','S008','T003',60,25,0,5,'2024-05-01',NULL),('P020','豆乾','S008','T003',80,40,0,10,'2024-05-01',NULL),('P021','花生','S008','T003',100,3,40,5,'2024-05-01',NULL),('P022','再來米','S009','T005',75,104,0,25,'2024-05-01',NULL),('P023','燕麥','S009','T005',90,61,0,25,'2024-05-01',NULL),('P024','汽水','S010','T001',30,20,0,10,'2024-05-01',NULL),('P025','巧克力','S011','T003',90,76,0,30,'2024-05-01',NULL),('P026','綿綿糖','S011','T003',30,15,0,10,'2024-05-01',NULL),('P027','牛肉乾','S011','T003',340,49,0,30,'2024-05-10',NULL),('P028','烤肉醬','S012','T007',110,26,0,10,'2024-04-15',NULL),('P029','海帶','S012','T006',120,0,0,10,'2024-04-15',NULL),('P030','黃魚','S013','T008',250,10,0,15,'2024-05-10',NULL),('P031','溫馨起司','S014','T004',185,0,70,20,'2024-04-25',NULL),('P032','白起司','S014','T004',155,9,40,25,'2024-04-25',NULL),('P033','台中起司','S015','T004',130,112,0,20,'2024-04-15',NULL),('P034','啤酒','S016','T001',55,111,0,15,'2024-05-01',NULL),('P035','芭樂汁','S016','T001',65,20,0,15,'2024-05-01',NULL),('P036','魷魚','S017','T008',190,112,0,20,'2024-04-25',NULL),('P037','干貝','S017','T008',260,11,50,25,'2024-05-10',NULL),('P038','綠茶','S018','T001',20,17,0,15,'2024-05-01',NULL),('P039','運動飲料','S018','T001',20,69,0,5,'2024-05-01',NULL),('P040','蝦米','S019','T008',150,123,0,30,'2024-05-01',NULL),('P041','蝦子','S019','T008',200,85,0,10,'2024-05-01',NULL),('P042','糙米','S020','T005',85,26,0,10,'2024-05-01',NULL),('P043','柳橙汁','S020','T001',45,17,10,25,'2024-05-01',NULL),('P044','蠔油','S020','T002',250,27,0,15,'2024-05-10',NULL),('P045','雪魚','S021','T008',300,5,70,15,'2024-05-10',NULL),('P046','蚵','S021','T008',120,95,0,10,'2024-04-15',NULL),('P047','蛋糕','S022','T003',100,36,0,10,'2024-05-01',NULL),('P048','玉米片','S022','T003',50,15,70,25,'2024-05-01',NULL),('P049','薯條','S023','T003',40,10,60,15,'2024-05-01',NULL),('P050','玉米餅','S023','T003',60,65,0,30,'2024-05-01',NULL),('P051','豬肉乾','S024','T007',150,20,0,10,'2024-05-01',NULL),('P052','三合一麥片','S024','T005',65,38,0,25,'2024-05-01',NULL),('P053','布丁','S024','T006',25,0,0,10,'2024-05-01',NULL),('P054','紅茶包','S025','T006',75,21,0,10,'2024-05-01',NULL),('P055','麥茶包','S025','T006',45,115,0,20,'2024-05-01',NULL),('P056','白米','S026','T005',85,21,10,30,'2024-05-01',NULL),('P057','小米','S026','T005',90,36,0,20,'2024-05-01',NULL),('P058','花枝','S027','T008',140,62,0,20,'2024-04-15',NULL),('P059','蘇澳起司','S028','T004',155,79,0,10,'2024-04-25',NULL),('P060','花起司','S028','T004',185,19,0,10,'2024-04-25',NULL),('P061','海鮮醬','S029','T002',100,113,0,25,'2024-05-01',NULL),('P062','山渣片','S029','T003',90,17,0,10,'2024-05-01',NULL),('P063','甜辣醬','S007','T002',90,24,0,5,'2024-05-01',NULL),('P064','黃豆','S012','T005',60,22,80,30,'2024-05-01',NULL),('P065','海苔醬','S002','T002',65,76,0,10,'2024-05-01',NULL),('P066','肉鬆','S002','T002',250,4,100,20,'2024-05-10',NULL),('P067','礦泉水','S016','T001',20,52,0,10,'2024-05-01',NULL),('P068','綠豆糕','S008','T003',40,6,10,15,'2024-05-01',NULL),('P069','黑起司','S015','T004',136,26,0,15,'2024-04-15',NULL),('P070','蘇打水','S007','T001',25,15,10,30,'2024-05-01',NULL),('P071','義大利起司','S015','T004',175,26,0,10,'2024-04-25',NULL),('P072','酸起司','S014','T004',135,14,0,10,'2024-04-15',NULL),('P073','海哲皮','S017','T008',150,101,0,5,'2024-05-01',NULL),('P074','雞湯塊','S004','T007',100,4,20,5,'2024-05-01',NULL),('P075','濃縮咖啡','S012','T001',75,125,0,25,'2024-05-01',NULL),('P076','檸檬汁','S023','T001',95,57,0,20,'2024-05-01',NULL),('P077','辣椒粉','S012','T002',65,32,0,15,'2024-05-01',NULL);
/*!40000 ALTER TABLE `product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `protype`
--

DROP TABLE IF EXISTS `protype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `protype` (
  `typNo` char(4) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `typName` varchar(20) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `details` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  PRIMARY KEY (`typNo`),
  UNIQUE KEY `typNoIndex` (`typNo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `protype`
--

LOCK TABLES `protype` WRITE;
/*!40000 ALTER TABLE `protype` DISABLE KEYS */;
INSERT INTO `protype` VALUES ('T001','飲料','軟性飲料,咖啡,啤酒,及麥酒'),('T002','調味品','甜酸醬,配料,塗料,及香料'),('T003','點心','甜點心,糖果,甜麵包'),('T004','日用品','起司'),('T005','穀類/麥片','麵包,餅干,麵糰,麥片'),('T006','肉/家禽','肉品'),('T007','特製品','水果乾及豆腐'),('T008','海鮮','海帶及魚類');
/*!40000 ALTER TABLE `protype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `supplier`
--

DROP TABLE IF EXISTS `supplier`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `supplier` (
  `supNo` char(4) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `supName` varchar(20) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `contactor` varchar(20) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `title` varchar(10) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `address` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `city` varchar(10) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `area` varchar(10) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `zip` char(5) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `tel` varchar(20) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `fax` varchar(20) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  PRIMARY KEY (`supNo`),
  UNIQUE KEY `supNoIndex` (`supNo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `supplier`
--

LOCK TABLES `supplier` WRITE;
/*!40000 ALTER TABLE `supplier` DISABLE KEYS */;
INSERT INTO `supplier` VALUES ('S001','桶一','陳小姐','業務','新竹市竹北路10號','新竹市','新竹','85511','(03) 555-2222','(03) 555-2222'),('S002','光權','黃小姐','董事長','台中市中港路一段9號','台中市','台中','70117','(03) 555-4822','(03) 555-4822'),('S003','生活妙','胡先生','董事長','南投縣南投路89號','南投縣','南投','48104','(02) 555-5735','(02) 555-5735'),('S004','為全','王先生','業務','屏東縣永大路77號','屏東縣','屏東','10002','(03) 305-5011','(03) 305-5011'),('S005','日正','李先生','訂貨員','屏東市中山路66號','屏東市','屏東','33007','(08) 598-7654','(08) 598-7654'),('S006','德菖','劉先生','業務','桃園縣富國路4111號','桃園縣','桃園','54585','(06) 431-7877','(06) 431-7877'),('S007','正一','方先生','行銷專員','苗栗縣中正路二段17樓','苗栗縣','苗栗','30584','(03) 444-2343','(03) 444-2343'),('S008','康堡','劉先生','董事長','台北市忠孝東路三段99號','台北市','台北','99658','(06) 555-4448','(06) 555-4448'),('S009','掬花','謝小姐','董事長','台中市仁愛路四段59號','台中市','台中','55555','(05) 889-5522','(05) 889-5522'),('S010','金美蘭','王先生','會計人員','高雄市中正路四段123號','高雄市','高雄','54422','(02) 555-4640','(02) 555-4640'),('S011','小噹','徐先生','業務','台北縣北新路48號','台北縣','台北','10785','(05) 998-4510','(05) 998-4510'),('S012','義美美','李先生','業務助理','花蓮市花中路49號','花蓮市','花蓮','60439','(06) 992-7552','(06) 992-7552'),('S013','東黃海','林小姐','研發人員','宜蘭市經國路250號','宜蘭市','宜蘭','27478','(04) 871-3225','(04) 871-3225'),('S014','小陽堂','林小姐','董事長','新竹市永平路789號','新竹市','新竹','48100','(05) 603-2223','(05) 603-2223'),('S015','德級','鍾小姐','船務','台北市北平東路114號','台北市','台北','13205','(02) 295-3010','(02) 295-3010'),('S016','力錦','劉先生','業務','台北市北平東路42號3樓','台北市','台北','97101','(03) 555-9931','(03) 555-9931'),('S017','小坊','方先生','董事長','新竹市竹北路88號','新竹市','新竹','54888','(03) 555-9931','(03) 555-9931'),('S018','記成','劉先生','董事長','台中市中港路一段478號','台中市','台中','75004','(03) 555-2211','(03) 555-2211'),('S019','普三','李先生','會計人員','新竹市竹北路81號','新竹市','新竹','02134','(03) 575-4822','(03) 575-4822'),('S020','一心','劉先生','業務','台中市中港路一段28號','台中市','台中','05128','(02) 568-5735','(02) 568-5735'),('S021','日日通','方先生','業務助理','南投縣南投路599號','南投縣','南投','28000','(03) 355-5991','(03) 355-5991'),('S022','順成','劉先生','研發人員','屏東縣永大路477號','屏東縣','屏東','99999','(08) 559-7654','(08) 559-7654'),('S023','利利','謝小姐','董事長','屏東市中山路57號','屏東市','屏東','53120','(06) 481-7877','(06) 481-7877'),('S024','涵合','王先生','船務','桃園縣富國路412號','桃園縣','桃園','20421','(03) 944-2343','(03) 944-2343'),('S025','佳佳','徐先生','業務','苗栗縣中正路二段5樓','苗栗縣','苗栗','44152','(06) 999-4448','(06) 999-4448'),('S026','弘文','李先生','董事長','台北市忠孝東路三段82號','台北市','台北','84100','(05) 829-5522','(05) 829-5522'),('S027','大鈺','林小姐','董事長','台中市仁愛路四段10號','台中市','台中','71300','(02) 965-4640','(02) 965-4640'),('S028','玉成','林小姐','業務','高雄市中正路四段60號','高雄市','高雄','74000','(05) 889-4422','(05) 889-4422'),('S029','百達','鍾小姐','業務助理','台北縣北新路55號','台北縣','台北','11425','(02) 555-4699','(02) 555-4699');
/*!40000 ALTER TABLE `supplier` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'north'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-01-15 16:47:16
