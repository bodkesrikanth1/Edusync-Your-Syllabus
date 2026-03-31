/*
SQLyog Community v13.1.1 (64 bit)
MySQL - 5.5.29 : Database - edusync
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`edusync` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */;

USE `edusync`;

/*Table structure for table `syllabi` */

DROP TABLE IF EXISTS `syllabi`;

CREATE TABLE `syllabi` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `text` longtext NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=utf8mb4;

/*Data for the table `syllabi` */



/*Table structure for table `syllabus_units` */

DROP TABLE IF EXISTS `syllabus_units`;

CREATE TABLE `syllabus_units` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `syllabus_id` int(11) NOT NULL,
  `unit_no` int(11) NOT NULL,
  `unit_title` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `syllabus_id` (`syllabus_id`),
  CONSTRAINT `syllabus_units_ibfk_1` FOREIGN KEY (`syllabus_id`) REFERENCES `syllabi` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=61 DEFAULT CHARSET=utf8mb4;

/*Data for the table `syllabus_units` */


/*Table structure for table `topics` */

DROP TABLE IF EXISTS `topics`;

CREATE TABLE `topics` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `unit_id` int(11) NOT NULL,
  `topic_text` varchar(512) NOT NULL,
  `weight` float DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `unit_id` (`unit_id`),
  KEY `topic_text` (`topic_text`(191)),
  CONSTRAINT `topics_ibfk_1` FOREIGN KEY (`unit_id`) REFERENCES `syllabus_units` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=231 DEFAULT CHARSET=utf8mb4;

/*Data for the table `topics` */



/*Table structure for table `users` */

DROP TABLE IF EXISTS `users`;

CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `full_name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password_hash` varchar(512) NOT NULL,
  `role` varchar(64) NOT NULL DEFAULT 'student',
  `college` varchar(255) DEFAULT NULL,
  `department` varchar(255) DEFAULT NULL,
  `year` varchar(64) DEFAULT NULL,
  `enrollment_no` varchar(128) DEFAULT NULL,
  `phone` varchar(32) DEFAULT NULL,
  `preferences` text,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;

/*Data for the table `users` */

insert  into `users`(`id`,`full_name`,`email`,`password_hash`,`role`,`college`,`department`,`year`,`enrollment_no`,`phone`,`preferences`,`created_at`) values 
(1,'aravind','aravind@gmail.com','pbkdf2:sha256:260000$VAfMdVlcvVdoacYq$cd102a548fceac8ad399c9ffce4ea1e8d6a60906f330df955105e6c544126030','student','jntu','cse','3rd','12345','8787676565',NULL,'2025-09-06 12:13:03'),
(2,'admin','admin@gmail.com','pbkdf2:sha256:260000$xyVIROw2VJYEAIla$01c2ef96033423dd38df34c7754033d8906ce9667142f4715403dbb2b220f7c3','admin','JNTU','CSE','4','3454','6789876567',NULL,'2026-01-22 11:27:09'),
(3,'venkat','venkat@gmail.com','pbkdf2:sha256:260000$MkoA7am6ITeWs1Uc$4d8fa87aee28e0461c65e77300513f6844e718975e75a0c5136814823c067584','faculty','jtu','cse','4th year','34543','9876543456',NULL,'2026-01-22 16:05:02'),
(6,'Administrator','admin','pbkdf2:sha256:260000$kxIaeegO4FtD8hMk$45dd8ebf5573dc8ad4a5f79f7322dc6f8b5f8a10f26bef2288ad6e4135a08030','admin',NULL,NULL,NULL,NULL,NULL,NULL,'2026-02-04 10:39:38');

/*Table structure for table `videos` */

DROP TABLE IF EXISTS `videos`;

CREATE TABLE `videos` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `topic_id` int(11) NOT NULL,
  `youtube_id` varchar(32) NOT NULL,
  `title` varchar(512) NOT NULL,
  `channel_title` varchar(255) DEFAULT NULL,
  `channel_id` varchar(64) DEFAULT NULL,
  `duration_sec` int(11) DEFAULT '0',
  `view_count` bigint(20) DEFAULT '0',
  `published_at` datetime DEFAULT NULL,
  `rating_score` float DEFAULT '0',
  `similarity` float DEFAULT '0',
  `final_score` float DEFAULT '0',
  `difficulty` varchar(32) DEFAULT 'auto',
  `url` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `topic_id` (`topic_id`),
  KEY `youtube_id` (`youtube_id`),
  KEY `final_score` (`final_score`),
  CONSTRAINT `videos_ibfk_1` FOREIGN KEY (`topic_id`) REFERENCES `topics` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2005 DEFAULT CHARSET=utf8mb4;

/*Data for the table `videos` */
