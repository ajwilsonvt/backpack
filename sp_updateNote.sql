DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_updateNote`(
    IN p_note_id bigint,
    IN p_user_id bigint,
    IN p_title varchar(45),
    IN p_post varchar(2500)
)
BEGIN
    update tbl_note
        set note_title = p_title, note_post = p_post
        where note_id = p_note_id and note_user_id = p_user_id;
END $$
DELIMITER ;
