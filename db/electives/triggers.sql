DELIMITER ;;

DROP TRIGGER IF EXISTS `elective_user_xref_AFTER_INSERT`;;
CREATE TRIGGER `elective_user_xref_AFTER_INSERT` AFTER INSERT ON `elective_user_xref`
FOR EACH ROW
  BEGIN
    CALL update_elective_enrollment(new.section_id);
  END;;

DROP TRIGGER IF EXISTS `elective_user_xref_AFTER_UPDATE`;;
CREATE TRIGGER `elective_user_xref_AFTER_UPDATE`
AFTER UPDATE ON `elective_user_xref`
FOR EACH ROW
  BEGIN
    CALL update_elective_enrollment(new.section_id);
  END;;

DROP TRIGGER IF EXISTS `elective_user_xref_AFTER_DELETE`;;
CREATE TRIGGER `elective_user_xref_AFTER_DELETE`
AFTER DELETE ON `elective_user_xref`
FOR EACH ROW
  BEGIN

    CALL update_elective_enrollment(old.section_id);

  END;;

DELIMITER ;