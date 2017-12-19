/*
Navicat MySQL Data Transfer

Source Server         : localhost
Source Server Version : 50719
Source Host           : 127.0.0.1:3306
Source Database       : pachong

Target Server Type    : MYSQL
Target Server Version : 50719
File Encoding         : 65001

Date: 2017-12-19 10:53:06
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for main_data
-- ----------------------------
DROP TABLE IF EXISTS `main_data`;
CREATE TABLE `main_data` (
  `snsId` varchar(30) NOT NULL,
  `content` varchar(4096) NOT NULL,
  `authorId` varchar(128) NOT NULL,
  `authorName` varchar(255) NOT NULL,
  `isCurrentUser` tinyint(4) NOT NULL,
  `rawXML` text NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`snsId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for media_list
-- ----------------------------
DROP TABLE IF EXISTS `media_list`;
CREATE TABLE `media_list` (
  `snsId` varchar(30) NOT NULL,
  `idx` smallint(6) NOT NULL DEFAULT '0',
  `url` varchar(512) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for sns_comments
-- ----------------------------
DROP TABLE IF EXISTS `sns_comments`;
CREATE TABLE `sns_comments` (
  `snsId` varchar(30) NOT NULL,
  `idx` smallint(6) NOT NULL DEFAULT '0',
  `content` varchar(1024) NOT NULL,
  `isCurrentUser` tinyint(4) NOT NULL DEFAULT '0',
  `toUserId` varchar(128) DEFAULT NULL,
  `toUserName` varchar(255) DEFAULT NULL,
  `authorId` varchar(128) NOT NULL,
  `authorName` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for sns_likes
-- ----------------------------
DROP TABLE IF EXISTS `sns_likes`;
CREATE TABLE `sns_likes` (
  `snsId` varchar(30) NOT NULL,
  `idx` smallint(6) NOT NULL DEFAULT '0',
  `isCurrentUser` tinyint(4) NOT NULL DEFAULT '0',
  `userName` varchar(255) NOT NULL,
  `userId` varchar(128) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

SET FOREIGN_KEY_CHECKS=1;
