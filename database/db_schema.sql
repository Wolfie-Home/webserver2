/* =============================================
-- SQLite code: db_schema.sql
--
-- Author: Bumsik Kim
-- Create date: 8/23/2016
-- Update history:
                9/14/2016: switched to SQLite from MySQL
-- Updated history:
-- Description: Create tables for `wolfie_home` database.
-- Example:
--      sqlite3 [database file] < db_schema.sql
--
-- =============================================  */

PRAGMA foreign_keys = OFF;

DROP TABLE IF EXISTS `User`;
DROP TABLE IF EXISTS `Location`;
DROP TABLE IF EXISTS `Device`;
DROP TABLE IF EXISTS `DataType`;
DROP TABLE IF EXISTS `DataField`;
DROP TABLE IF EXISTS `DataRecord`;
DROP TABLE IF EXISTS `RecordFieldValue`;

PRAGMA foreign_keys = ON;

-- Note that INTEGER PRIMARY KEY in SQL automatically autoincrement.

CREATE TABLE `User` (
    `Id` INTEGER PRIMARY KEY,
    `UserName` VARCHAR(30) NOT NULL,
    `Password` CHAR(128) NOT NULL,
    `Email` VARCHAR(40) NOT NULL DEFAULT "",
    `PassSalt` CHAR(8) NOT NULL,
    `CreatedTime` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `ModifiedTime` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (`UserName`)
);

CREATE TABLE `Location` (
    `Id` INTEGER PRIMARY KEY,
    `UserRef` UNSIGNED INTEGER NOT NULL,
    `Name` VARCHAR(20) NOT NULL,
    `Parent` UNSIGNED INTEGER,
    `Description` VARCHAR(50) NOT NULL DEFAULT "",
    `CreatedTime` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `ModifiedTime` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (`UserRef`, `Name`),
    FOREIGN KEY (`UserRef`) REFERENCES `User`(`Id`),
    FOREIGN KEY (`Parent`) REFERENCES `Location`(`Id`) ON DELETE SET NULL
);

CREATE TABLE `Device` (
    `Id` INTEGER PRIMARY KEY,
    `OwnerRef` UNSIGNED INTEGER NOT NULL,
    `Name` VARCHAR(20) NOT NULL,
    `LocationRef` UNSIGNED INTEGER,
    `Parent` UNSIGNED INTEGER,
    `Description` VARCHAR(50) NOT NULL DEFAULT "",
    `CreatedTime` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `ModifiedTime` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (`OwnerRef`, `Name`),
    FOREIGN KEY (`OwnerRef`) REFERENCES `User`(`Id`),
    FOREIGN KEY (`LocationRef`) REFERENCES `Location`(`Id`) ON DELETE  SET NULL,
    FOREIGN KEY (`Parent`) REFERENCES `Device`(`Id`) ON DELETE SET NULL
);

CREATE TABLE `DataType` (
    `Id` INTEGER PRIMARY KEY,
    `TypeName` VARCHAR(20) NOT NULL,
    `Description` VARCHAR(128) NOT NULL DEFAULT "",
    `CreatedTime` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `ModifiedTime` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (`TypeName`)
);

CREATE TABLE `DataField` (
    `Id` INTEGER PRIMARY KEY,
    `DeviceRef` UNSIGNED INTEGER NOT NULL,
    `DatafieldName` VARCHAR(16) NOT NULL,
    `Controllable` BOOLEAN NOT NULL,
    `DataTypeRef` UNSIGNED INTEGER NOT NULL,
    `Description` VARCHAR(50) NOT NULL DEFAULT "",
    `CreatedTime` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `ModifiedTime` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (`DeviceRef`, `DatafieldName`),
    FOREIGN KEY (`DataTypeRef`) REFERENCES `DataType`(`Id`),
    FOREIGN KEY (`DeviceRef`) REFERENCES `Device`(`OwnerRef`) ON DELETE CASCADE
);

CREATE TABLE `DataRecord` (
    `Id` INTEGER PRIMARY KEY ,
    `DeviceRef` UNSIGNED INTEGER NOT NULL,
    `LocationRef` UNSIGNED INTEGER,
    `CreatedTime` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`LocationRef`) REFERENCES `Location`(`Id`),
    FOREIGN KEY (`DeviceRef`) REFERENCES `Device`(`Id`)
);

CREATE TABLE `RecordFieldValue` (
    `Id` INTEGER PRIMARY KEY ,
    `RecordRef` UNSIGNED BIGINT NOT NULL,
    `DataFieldRef` UNSIGNED INTEGER NOT NULL,
    `Value` VARCHAR(30) NOT NULL,
    FOREIGN KEY (`RecordRef`) REFERENCES `DataRecord`(`Idx`) ON DELETE CASCADE,
    FOREIGN KEY (`DataFieldRef`) REFERENCES `DataField`(`Id`)
);
