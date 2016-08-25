/* =============================================
-- Object:  StoredProcedure `wolfie_home`.`DataField_List_S`
-- 
-- Author: Bumsik Kim        
-- Create date: 8/23/2016
-- Updated history:
-- Description: Get a list of datafield.
-- Example:
-- 		CALL `DataField_List_S`(1);
-- 		SELECT * FROM `wolfie_home`.`DataField`;
-- 
-- =============================================  */

USE wolfie_home;
DROP PROCEDURE IF EXISTS `wolfie_home`.`DataField_List_S`;

delimiter //

CREATE PROCEDURE `wolfie_home`.`DataField_List_S`
(
	IN `DeviceID_in`	INTEGER

-- Returns (Multi-row return):
-- 	`Id`			<int>
-- 	`DeviceRef`		<int>
-- 	`DatafieldName`	<string>
-- 	`Controllable`	<bool?>
-- 	`DataTypeRef`	<int>
-- 	`Description`	<string>
)
BEGIN

	-- Return
	SELECT `Id`,`DeviceRef`,`DatafieldName`,`Controllable`,`DataTypeRef`,`Description`
		FROM `DataField`
		WHERE (`DeviceRef` = `DeviceID_in`);

END //

delimiter ;
