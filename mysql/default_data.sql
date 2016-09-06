/* =============================================
-- MySQL code: Create_default_data.sql
-- 
-- Author: Bumsik Kim        
-- Create date: 8/23/2016
-- Updated history:
-- Description: Create default data of the database
-- 				Recommended to execute one by one to see what happens
-- Example:
--		Recommended to execute one by one to see what happens but you can:
--      mysql -u [username] -p [password] < Create_default_data.sql
-- 
-- =============================================  */

/* =============================================
-- Create Default data
-- =============================================  */

USE `wolfie_home`;

-- Create a default user
CALL `User_Add_I`("defaultUser","dummypassword", "kbumsik@gmail.com");
-- Create a default room
CALL `Location_Add_I`(1, "defaultRoom", NULL, "It's a default room");
-- Create a default Device
CALL `Device_Add_I`(1,"defaultDevice",NULL,NULL,"It's a default Device");
-- Create default datatypes
CALL `DataType_Add_I`("int","Integer Type");
CALL `DataType_Add_I`("float","Floating point number Type");
CALL `DataType_Add_I`("str","String Type");
CALL `DataType_Add_I`("bool","Boolean Type");
-- Create default datafields
CALL `DataField_Add_I`(1, "Button", 0, 1, "Default Button. PUSHED = 1, RELEASED = 0.");
CALL `DataField_Add_I`(1, "Led", 1, 1, "Default LED. ON =1, OFF = 0");

/* =============================================
-- List Default data
-- =============================================  */

USE `wolfie_home`;

-- Try default login
CALL `User_Login_S`("defaultUser","dummypassword");
-- Get list of location of the default user. 1 means the "defaultUser"'s ID
CALL `Location_List_S`(1, NULL);
-- Get list of devices of the default user. 1 means the "defaultUser"'s ID
CALL `Device_List_S`(1, NULL, NULL);
-- Get list of datatypes.
CALL `DataType_List_S`();
-- Get list of datafield of the default device. 1 means the "defaultDevice"'s ID
CALL `DataField_List_S`(1);