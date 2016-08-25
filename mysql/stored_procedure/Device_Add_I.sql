/* =============================================
-- Object:  StoredProcedure `wolfie_home`.`Device_Add_I`
-- 
-- Author: Bumsik Kim        
-- Create date: 8/23/2016
-- Updated history:
-- Description: Add a device. Returns a created device with ID
-- Example:
-- 		CALL `Device_Add_I`(1,"defaultDevice",NULL,NULL,"It's a default Device");
-- 		SELECT * FROM `wolfie_home`.`Device`;
-- 
-- =============================================  */

USE wolfie_home;
DROP PROCEDURE IF EXISTS `wolfie_home`.`Device_Add_I`;

delimiter //

CREATE PROCEDURE `wolfie_home`.`Device_Add_I`
(
	IN `UserID_in`		INTEGER,
    IN `Name_in`		VARCHAR(20),
    IN `Location_in`	INTEGER,
    IN `Parent_in`		INTEGER,	-- Can be NULL. But NULL mean it's
                  		        	-- 	a mother device.
    IN `Description_in` VARCHAR(50) -- Optional, can be NULL

-- Returns (single-row return):
-- `Id`				<int>	Newly created ID.
-- `OwnerRef`		<int>
-- `Name`			<string>
-- `LocationRef`	<int>
-- `Parent`			<int>
-- `Description`	<string>
)
BEGIN
	-- input paramets handling
	IF `Description_in` IS NULL THEN
		SET `Description_in` = "";
	END IF;
    
    -- then insert
	INSERT INTO `Device`(`OwnerRef`,`Name`,`LocationRef`,`Parent`,`Description`)
		VALUES (`UserID_in`,`Name_in`,`Location_in`,`Parent_in`,`Description_in`);

	-- return
	SELECT `Id`,`OwnerRef`,`Name`,`LocationRef`,`Parent`,`Description`
		FROM `Device`
		WHERE (`OwnerRef` = `UserID_in`) AND (`Name` = `Name_in`);

END //

delimiter ;
