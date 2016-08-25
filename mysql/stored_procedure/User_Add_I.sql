/* =============================================
-- Object:  StoredProcedure `wolfie_home`.`User_Add_I`
-- 
-- Author: Bumsik Kim        
-- Create date: 8/23/2016
-- Updated history:
-- Description: Add a user. password is SHA-512 encrypted.
-- Example:
-- 		CALL `User_Add_I`("defaultUser","dummypassword", "kbumsik@gmail.com");
-- 		SELECT * FROM wolfie_home.User;
-- 
-- =============================================  */

USE wolfie_home;
DROP PROCEDURE IF EXISTS `wolfie_home`.`User_Add_I`;

delimiter //

CREATE PROCEDURE `wolfie_home`.`User_Add_I`
(
	IN UserName_in	VARCHAR(30),
    IN Password_in	VARCHAR(50),
    IN Email_in		VARCHAR(40)

-- Returns (single-row return):
-- 	`Id`		<int>		Created User Id (Note that Id is not UserName)
-- 	`UserName`	<string>
-- 	`Email`		<string>
)
BEGIN
-- Declare id and salt
DECLARE id_generated INTEGER;
DECLARE salt CHAR(8);

-- Declare handlers
-- Error diagnostics from http://dev.mysql.com/doc/refman/5.6/en/get-diagnostics.html
-- RESIGNAL from https://dev.mysql.com/doc/refman/5.7/en/resignal.html
DECLARE `code` CHAR(5) DEFAULT '00000';
DECLARE `msg` TEXT;

DECLARE exit handler FOR sqlexception
	BEGIN
		-- ERROR
        GET DIAGNOSTICS CONDITION 1
        `code` = RETURNED_SQLSTATE, `msg` = MESSAGE_TEXT;
		ROLLBACK;
        SET `msg` = CONCAT("Creating user failed. Code: ", `code`, ". ", `msg`);
        RESIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = `msg`;
	END;
 
DECLARE exit handler FOR sqlwarning
	BEGIN
		-- WARNING
        GET DIAGNOSTICS CONDITION 1
        `code` = RETURNED_SQLSTATE, `msg` = MESSAGE_TEXT;
		ROLLBACK;
        SET `msg` = CONCAT("Creating user warning. Code: ", `code`, ". ", `msg`);
        RESIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = `msg`;
	END;

-- Start
START TRANSACTION;

	-- Set salt
	SET salt = SUBSTRING(MD5(RAND()),-8);

	-- First just put the username and email and salt
	INSERT INTO `User` (`UserName`, `Password`, `Email`, `PassSalt`)
		VALUES (`UserName_in`, "", `Email_in`, salt);

	SET id_generated = (SELECT `Id` FROM `User` WHERE `UserName` = `UserName_in`);

	-- put hash
	UPDATE `User`
		SET `Password` = SHA2(CONCAT(salt,`Password_in`),512)
		WHERE `Id` = id_generated;
    
	-- And then login test
	IF EXISTS (SELECT `Id` FROM `User` 
					WHERE 	(`UserName` = `UserName_in`)
					AND (`Id` = id_generated)
					AND (`Password` = SHA2(CONCAT(salt,`Password_in`),512))
			) THEN
		SELECT `Id`, `UserName`, `Email` FROM `User` WHERE (`UserName` = `UserName_in`);
	ELSE
		-- Rise error
		-- for SIGNAL Sytax, see http://dev.mysql.com/doc/refman/5.6/en/signal.html
		SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'An login test error occurred', MYSQL_ERRNO = 1001;
	END IF;
    
COMMIT;

END //

delimiter ;
