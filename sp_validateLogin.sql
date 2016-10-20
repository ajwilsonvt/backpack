/*This file is not necessary to run the app. This stored procedure script
is applied to the database. I have included it for educational purposes.*/
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_validateLogin`(
    IN p_email VARCHAR(20)
)
BEGIN
    select * from tbl_user where user_email = p_email;
END $$
DELIMITER ;
