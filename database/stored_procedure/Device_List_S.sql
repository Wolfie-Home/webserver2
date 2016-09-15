/* =============================================
-- Object:  StoredProcedure `wolfie_home`.`Device_List_S`
-- 
-- Author: Bumsik Kim        
-- Create date: 8/23/2016
-- Updated history:
-- Description: Get a list of devices.
-- Example:
-- 		CALL `Device_List_S`(1, NULL, NULL);
-- 		SELECT * FROM `wolfie_home`.`Device`;
-- 
-- =============================================  */

USE wolfie_home;
DROP PROCEDURE IF EXISTS `wolfie_home`.`Device_List_S`;

delimiter //

CREATE PROCEDURE `wolfie_home`.`Device_List_S`
(
	IN `UserID_in`		INTEGER,
    IN `LocationID_in`	INTEGER,		-- Optional. Input NULL if not needed
    IN `ParentID_in`	INTEGER			-- Optional. Input NULL if you want to
                    	       			-- 		See a full list tree.-- Returns (single-row return):

-- Returns (Multi-row return):
-- `Id`				<int>
-- `OwnerRef`		<int>
-- `Name`			<string>
-- `LocationRef`	<int>
-- `Parent`			<int>
-- `Description`	<string>
)
BEGIN

	-- Return
	SELECT `Id`,`OwnerRef`,`Name`,`LocationRef`,`Parent`,`Description`
		FROM `Device`
		WHERE 	(`OwnerRef` = `UserID_in`)
			AND ((`LocationRef` = `LocationID_in`) OR (`LocationID_in` IS NULL))
            AND ((`Parent` = `ParentID_in`) OR (`ParentID_IN` IS NULL));

END //

delimiter ;
