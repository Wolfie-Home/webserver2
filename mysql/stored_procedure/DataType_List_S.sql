/* =============================================
-- Object:  StoredProcedure `wolfie_home`.`DataType_List_S`
-- 
-- Author: Bumsik Kim        
-- Create date: 8/23/2016
-- Updated history:
-- Description: Get a list of DataTypes. No parameter needed
-- Example:
-- 		CALL `DataType_List_S`();
-- 		SELECT * FROM `wolfie_home`.`DataType`;
-- 
-- =============================================  */

USE wolfie_home;
DROP PROCEDURE IF EXISTS `wolfie_home`.`DataType_List_S`;

delimiter //

CREATE PROCEDURE `wolfie_home`.`DataType_List_S`
(
	-- No parameters
	

-- Returns (Multi-row return):
-- `Id`				<int>	Newly created ID
-- `TypeName`		<string>
-- `Description`	<string>
)
BEGIN

	-- Return
	SELECT `Id`,`TypeName`,`Description`
		FROM `DataType`;

END //

delimiter ;
