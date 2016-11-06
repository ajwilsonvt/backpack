DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_getNoteByID`(
    IN p_note_id bigint,
    IN p_user_id bigint
)
BEGIN
    select * from tbl_note
        where note_id = p_note_id and note_user_id = p_user_id;
END $$
DELIMITER ;
