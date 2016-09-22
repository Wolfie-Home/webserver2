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
    `id` INTEGER PRIMARY KEY,
    `username` VARCHAR(30) NOT NULL,
    `password` CHAR(128) NOT NULL,
    `email` VARCHAR(40) NOT NULL DEFAULT "",
    `salt` CHAR(8) NOT NULL,
    `created_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `modified_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (`username`)
);

CREATE TABLE `Location` (
    `id` INTEGER PRIMARY KEY,
    `user_id` UNSIGNED INTEGER NOT NULL,
    `name` VARCHAR(20) NOT NULL,
    `house_id` UNSIGNED INTEGER,
    `description` VARCHAR(50) NOT NULL DEFAULT "",
    `created_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `modified_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (`user_id`, `name`),
    FOREIGN KEY (`user_id`) REFERENCES `User`(`id`),
    FOREIGN KEY (`house_id`) REFERENCES `Location`(`id`) ON DELETE SET NULL
);

CREATE TABLE `Device` (
    `id` INTEGER PRIMARY KEY,
    `user_id` UNSIGNED INTEGER NOT NULL,
    `name` VARCHAR(20) NOT NULL,
    `location_id` UNSIGNED INTEGER,
    `mother_id` UNSIGNED INTEGER,
    `description` VARCHAR(50) NOT NULL DEFAULT "",
    `created_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `modified_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (`user_id`, `name`),
    FOREIGN KEY (`user_id`) REFERENCES `User`(`id`),
    FOREIGN KEY (`location_id`) REFERENCES `Location`(`id`) ON DELETE  SET NULL,
    FOREIGN KEY (`mother_id`) REFERENCES `Device`(`id`) ON DELETE SET NULL
);

CREATE TABLE `DataType` (
    `id` INTEGER PRIMARY KEY,
    `name` VARCHAR(20) NOT NULL,
    `description` VARCHAR(128) NOT NULL DEFAULT "",
    `created_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `modified_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (`name`)
);

CREATE TABLE `DataField` (
    `id` INTEGER PRIMARY KEY,
    `device_id` UNSIGNED INTEGER NOT NULL,
    `name` VARCHAR(16) NOT NULL,
    `controllable` BOOLEAN NOT NULL,
    `type_id` UNSIGNED INTEGER NOT NULL,
    `description` VARCHAR(50) NOT NULL DEFAULT "",
    `created_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `modified_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (`device_id`, `name`),
    FOREIGN KEY (`type_id`) REFERENCES `DataType`(`id`),
    FOREIGN KEY (`device_id`) REFERENCES `Device`(`id`) ON DELETE CASCADE
);

CREATE TABLE `DataRecord` (
    `id` INTEGER PRIMARY KEY ,
    `device_id` UNSIGNED INTEGER NOT NULL,
    `location_id` UNSIGNED INTEGER,
    `created_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`location_id`) REFERENCES `Location`(`id`),
    FOREIGN KEY (`device_id`) REFERENCES `Device`(`id`)
);

CREATE TABLE `RecordFieldValue` (
    `id` INTEGER PRIMARY KEY ,
    `record_id` UNSIGNED BIGINT NOT NULL,
    `datafield_id` UNSIGNED INTEGER NOT NULL,
    `value` VARCHAR(30) NOT NULL,
    FOREIGN KEY (`record_id`) REFERENCES `DataRecord`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`datafield_id`) REFERENCES `DataField`(`id`)
);
