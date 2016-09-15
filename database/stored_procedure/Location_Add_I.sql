/* =============================================
-- Object:  StoredProcedure `wolfie_home`.`Location_Add_I`
-- 
-- Author: Bumsik Kim        
-- Create date: 8/23/2016
-- Updated history:
-- Description: Add a location, the User is Integer ID
-- Example:
-- 		CALL `Location_Add_I`(1, "defaultRoom", NULL, "It's a default room");
-- 		SELECT * FROM `wolfie_home`.`Location`;
-- 
-- =============================================  */

USE wolfie_home;
DROP PROCEDURE IF EXISTS `wolfie_home`.`Location_Add_I`;

delimiter //

CREATE PROCEDURE `wolfie_home`.`Location_Add_I`
(
	IN `UserID_in`		INTEGER,		-- It is integer UserID
    IN `Name_in`		VARCHAR(20),
    IN `Parent_in` 		INTEGER,		-- Can be NULL but NULL means the
                   		        		-- 		location is a mother location
    IN `Description_in`	VARCHAR(50)		-- Optional, can be NULL

-- Returns (single-row return):
-- 	`Id`			<int>	Created Location Id
-- 	`UserRef`		<int>	The rest of parameters should be the same as input
-- 	`Name`			<string>
-- 	`Description`	<string>
-- 	`Parent`		<int>
)
BEGIN
	-- input paramets handling
	IF `Description_in` IS NULL THEN
		SET `Description_in` = "";
	END IF;
    
    -- then insert
	INSERT INTO `Location`(`UserRef`, `Name`,`Description`,`Parent`)
		VALUES (`UserID_in`, `Name_in`, `Description_in`, `Parent_in`);

	-- return
	SELECT `Id`,`UserRef`,`Name`,`Description`,`Parent`
		FROM `Location`
		WHERE `UserRef` = `UserID_in` AND `Name` = `Name_in`;
	
END //

delimiter ;
