/* =============================================
-- Object:  StoredProcedure `wolfie_home`.`User_Login_S`
-- 
-- Author: Bumsik Kim        
-- Create date: 8/23/2016
-- Updated history:
-- Description: Login user
-- Example:
-- 		CALL `User_Login_S`("defaultUser","dummypassword");
-- 
-- =============================================  */

USE wolfie_home;
DROP PROCEDURE IF EXISTS `wolfie_home`.`User_Login_S`;

delimiter //

CREATE PROCEDURE `wolfie_home`.`User_Login_S`
(
	IN UserName_in	VARCHAR(30),
    IN Password_in	VARCHAR(50)

-- Returns (single-row return):
-- 	`Id`		<int>		Created User Id (Note that Id is not UserName)
-- 	`UserName`	<string>
-- 	`Email`		<string>
)
BEGIN
-- Declare id and salt
DECLARE user_id INTEGER;
DECLARE salt CHAR(8);

SELECT `Id`, `PassSalt`
	INTO user_id, salt
	FROM `User`
    WHERE `UserName` = `UserName_in`;

IF user_id IS NULL THEN
	-- Rise error
	-- for SIGNAL Sytax, see http://dev.mysql.com/doc/refman/5.6/en/signal.html
	SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No such user', MYSQL_ERRNO = 1001;
END IF;

-- Subqueries with EXISTS
-- See http://dev.mysql.com/doc/refman/5.7/en/exists-and-not-exists-subqueries.html
-- FIXME: Rise error if the password is wrong
SELECT `Id`, `UserName`, `Email`
	FROM `User`
	WHERE 	(`UserName` = `UserName_in`)
		AND (`Password` = SHA2(CONCAT(salt,`Password_in`),512));

END //

delimiter ;
