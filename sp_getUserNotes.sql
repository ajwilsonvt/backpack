DELIMITER $$
USE NotesList $$
CREATE PROCEDURE sp_getUserNotes(
    IN p_user_id bigint
)
BEGIN
    select * from tbl_note where note_user_id = p_user_id;
END $$
DELIMITER ;
