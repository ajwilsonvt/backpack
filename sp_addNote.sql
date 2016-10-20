DELIMITER $$
USE `NotesList` $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_addNote`(
    IN p_user_id bigint,
    IN p_title varchar(45),
    IN p_post varchar(2500)
)
BEGIN
	insert into tbl_note (
        note_user_id,
        note_date,
        note_title,
        note_post
    )
    values
	(
        p_user_id,
        NOW(),
        p_title,
        p_post
    );
END $$
DELIMITER ;
