/* =============================================
-- Object:  StoredProcedure `wolfie_home`.`DataField_Add_I`
-- 
-- Author: Bumsik Kim        
-- Create date: 8/23/2016
-- Updated history:
-- Description: Add a Datafield. Returns a created Datafield with ID
-- Example:
-- 		CALL `DataField_Add_I`(1, "Button", 0, 1, "Default Button. PUSHED = 1, RELEASED = 0.");
-- 		CALL `DataField_Add_I`(1, "Led", 1, 1, "Default LED. ON =1, OFF = 0");
--
-- 		SELECT * FROM `DataField`;
-- 
-- =============================================  */

USE wolfie_home;
DROP PROCEDURE IF EXISTS `wolfie_home`.`DataField_Add_I`;

delimiter //

CREATE PROCEDURE `wolfie_home`.`DataField_Add_I`
(
    IN `DeviceID_in` 		INTEGER,
	IN `Name_in` 			VARCHAR(10),
    IN `Controllable_in` 	TINYINT(1),
    IN `DataType_in` 		INTEGER,
    IN `Description_in` 	VARCHAR(50) -- Optional, can be NULL

-- Returns (single-row return):
-- 	`Id`			<int>	Newly created ID
-- 	`DeviceRef`		<int>
-- 	`DatafieldName`	<string>
-- 	`Controllable`	<bool?>
-- 	`DataTypeRef`	<int>
-- 	`Description`	<string>
)
BEGIN
	-- input paramets handling
	IF `Description_in` IS NULL THEN
		SET `Description_in` = "";
	END IF;
    
    -- Insert
	INSERT INTO `DataField`(`DeviceRef`,`DatafieldName`,`Controllable`,`DataTypeRef`,`Description`)
		VALUES (`DeviceID_in`,`Name_in`, `Controllable_in`,`DataType_in`, `Description_in`);

	-- Return
	SELECT `Id`,`DeviceRef`,`DatafieldName`,`Controllable`,`DataTypeRef`,`Description`
		FROM `DataField`
		WHERE (`DeviceRef` = `DeviceID_in`) AND (`DatafieldName` = `Name_in`);

END //

delimiter ;
