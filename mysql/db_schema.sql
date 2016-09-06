/* =============================================
-- MySQL code: Create_tables.sql
-- 
-- Author: Bumsik Kim        
-- Create date: 8/23/2016
-- Updated history:
-- Description: Create tables for `wolfie_home` database.
-- Example:
--      mysql -u [username] -p [password] < Create_talbes.sql
-- 
-- =============================================  */

USE `wolfie_home`;
-- TODO: Character set. We need to change to utf8mb4_general_ci or utf8mb4_unicode_ci later
ALTER DATABASE wolfie_home CHARACTER SET latin1 COLLATE latin1_general_ci;

SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS `User`;
DROP TABLE IF EXISTS `Location`;
DROP TABLE IF EXISTS `Device`;
DROP TABLE IF EXISTS `DataType`;
DROP TABLE IF EXISTS `DataField`;
DROP TABLE IF EXISTS `DataRecord`;
DROP TABLE IF EXISTS `RecordFieldValue`;
SET FOREIGN_KEY_CHECKS = 1;

CREATE TABLE `User` (
    `Id` INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
    `UserName` VARCHAR(30) NOT NULL,
    `Password` CHAR(128) NOT NULL,
    `Email` VARCHAR(40) NOT NULL DEFAULT "",
    `PassSalt` CHAR(8) NOT NULL,
    `CreatedTime` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `ModifiedTime` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`Id`),
    UNIQUE (`UserName`)
);

CREATE TABLE `Location` (
    `Id` INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
    `UserRef` INTEGER UNSIGNED NOT NULL,
    `Name` VARCHAR(20) NOT NULL,
    `Parent` INTEGER UNSIGNED,
    `Description` VARCHAR(50) NOT NULL DEFAULT "",
    `CreatedTime` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `ModifiedTime` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`Id`),
    UNIQUE (`UserRef`, `Name`)
);
ALTER TABLE `Location` ADD FOREIGN KEY (`UserRef`) REFERENCES `User`(`Id`);
ALTER TABLE `Location` ADD FOREIGN KEY (`Parent`) REFERENCES `Location`(`Id`);

CREATE TABLE `Device` (
    `Id` INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
    `OwnerRef` INTEGER UNSIGNED NOT NULL,
    `Name` VARCHAR(20) NOT NULL,
    `LocationRef` INTEGER UNSIGNED,
    `Parent` INTEGER UNSIGNED,
    `Description` VARCHAR(50) NOT NULL DEFAULT "",
    `CreatedTime` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `ModifiedTime` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`Id`),
    UNIQUE (`OwnerRef`, `Name`)
);
ALTER TABLE `Device` ADD FOREIGN KEY (`OwnerRef`) REFERENCES `User`(`Id`);
ALTER TABLE `Device` ADD FOREIGN KEY (`LocationRef`) REFERENCES `Location`(`Id`);
ALTER TABLE `Device` ADD FOREIGN KEY (`Parent`) REFERENCES `Device`(`Id`);

CREATE TABLE `DataType` (
    `Id` INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
    `TypeName` VARCHAR(20) NOT NULL,
    `Description` VARCHAR(128) NOT NULL DEFAULT "",
    `CreatedTime` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `ModifiedTime` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`Id`),
    UNIQUE (`TypeName`)
);

CREATE TABLE `DataField` (
    `Id` INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
    `DeviceRef` INTEGER UNSIGNED NOT NULL,
    `DatafieldName` VARCHAR(16) NOT NULL,
    `Controllable` BOOLEAN NOT NULL,
    `DataTypeRef` INTEGER UNSIGNED NOT NULL,
    `Description` VARCHAR(50) NOT NULL DEFAULT "",
    `CreatedTime` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `ModifiedTime` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`Id`),
    UNIQUE (`DeviceRef`, `DatafieldName`)
);
ALTER TABLE `DataField` ADD FOREIGN KEY (`DataTypeRef`) REFERENCES `DataType`(`Id`);
ALTER TABLE `DataField` ADD FOREIGN KEY (`DeviceRef`) REFERENCES `Device`(`OwnerRef`);

CREATE TABLE `DataRecord` (
    `Idx` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `DeviceRef` INTEGER UNSIGNED NOT NULL,
    `LocationRef` INTEGER UNSIGNED,
    `CreatedTime` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`Idx`)
);
ALTER TABLE `DataRecord` ADD FOREIGN KEY (`LocationRef`) REFERENCES `Location`(`Id`);
ALTER TABLE `DataRecord` ADD FOREIGN KEY (`DeviceRef`) REFERENCES `Device`(`Id`);

CREATE TABLE `RecordFieldValue` (
    `Idx` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `RecordRef` BIGINT UNSIGNED NOT NULL,
    `DataFieldRef` INTEGER UNSIGNED NOT NULL,
    `Value` VARCHAR(30) NOT NULL,
    PRIMARY KEY (`Idx`)
);
ALTER TABLE `RecordFieldValue` ADD FOREIGN KEY (`RecordRef`) REFERENCES `DataRecord`(`Idx`);
ALTER TABLE `RecordFieldValue` ADD FOREIGN KEY (`DataFieldRef`) REFERENCES `DataField`(`Id`);
