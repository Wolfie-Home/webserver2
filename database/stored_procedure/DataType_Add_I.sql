/* =============================================
-- Object:  StoredProcedure `wolfie_home`.`DataType_Add_I`
-- 
-- Author: Bumsik Kim        
-- Create date: 8/23/2016
-- Updated history:
-- Description: Add a Type. Returns a created Type with ID
-- Example:
-- 		CALL `DataType_Add_I`("int","Integer Type");
-- 		CALL `DataType_Add_I`("float","Floating point number Type");
-- 		CALL `DataType_Add_I`("str","String Type");
-- 		CALL `DataType_Add_I`("bool","Boolean Type");
--
-- 		SELECT * FROM `DataType`;
-- 
-- =============================================  */

USE wolfie_home;
DROP PROCEDURE IF EXISTS `wolfie_home`.`DataType_Add_I`;

delimiter //

CREATE PROCEDURE `wolfie_home`.`DataType_Add_I`
(
	IN Name_in	VARCHAR(20),
    IN Description_in VARCHAR(128) -- Optional, can be NULL

-- Returns (single-row return):
-- `Id`				<int>	Newly created ID
-- `TypeName`		<string>
-- `Description`	<string>
)
BEGIN

	-- input paramets handling
	IF `Description_in` IS NULL THEN
		SET `Description_in` = "";
	END IF;

	-- Insert
	INSERT INTO `DataType`(`TypeName`,`Description`)
		VALUES (`Name_in`, `Description_in`);

	-- Return
	SELECT `Id`,`TypeName`,`Description`
		FROM `DataType`
		WHERE (`TypeName` = `Name_in`);

END //

delimiter ;
