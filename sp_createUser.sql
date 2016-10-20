/*This file is not necessary to run the app. This stored procedure script
is applied to the database. I have included it for educational purposes.*/
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_createUser`(
	IN p_name VARCHAR(20),
    IN p_email VARCHAR(20),
    IN p_password VARCHAR(100) /*needed more space for hashed password*/
)
BEGIN
    IF ( select exists (select 1 from tbl_user
            where user_email = p_email) ) THEN
		select 'email exists';
    ELSE
		insert into tbl_user
        (
			user_name,
            user_email,
            user_password
		)
        values
        (
			p_name,
            p_email,
            p_password
		);
	END IF;
END $$
DELIMITER ;
