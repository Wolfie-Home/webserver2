/* =============================================
-- Object:  StoredProcedure `wolfie_home`.`Location_List_S`
-- 
-- Author: Bumsik Kim        
-- Create date: 8/23/2016
-- Updated history:
-- Description: Get a list of locations.
-- Example:
-- 		CALL `Location_List_S`(1, NULL);
-- 		SELECT * FROM `wolfie_home`.`Location`;
-- 
-- =============================================  */

USE wolfie_home;
DROP PROCEDURE IF EXISTS `wolfie_home`.`Location_List_S`;

delimiter //

CREATE PROCEDURE `wolfie_home`.`Location_List_S`
(
	IN `UserID_in`		INTEGER,
    IN `ParentID_in`	INTEGER  -- If NULL, call all trees of locations
                    	         -- TODO: should 0 allowed as well?

-- Returns (Multi-row return):
-- 	`Id`			<int>
-- 	`UserRef`		<int>
-- 	`Name`			<string>
-- 	`Description`	<string>
-- 	`Parent`		<int>
)
BEGIN

	-- Return
	SELECT `Id`,`UserRef`,`Name`,`Description`,`Parent`
		FROM `Location`
		WHERE 	(`UserRef` = `UserID_in`)
			AND ((`Parent` = `ParentID_in`) OR (`ParentID_IN` IS NULL));

END //

delimiter ;
