/*This file is not necessary to run the app. This stored procedure script
is applied to the database. I have included it for educational purposes.*/
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_createUser` (
	IN p_name VARCHAR(20),
    IN p_username VARCHAR(20),
    IN p_password VARCHAR(45) /*needed more space for hashed password*/
)
BEGIN
	if ( select exists (select 1 from tbl_user
            where user_username = p_username) ) THEN
		select 'Username Exists';
    ELSE
		insert into tbl_user
        (
			user_name,
            user_username,
            user_password
		)
        values
        (
			p_name,
            p_username,
            p_password
		);
	END IF;
END $$
DELIMITER ;
