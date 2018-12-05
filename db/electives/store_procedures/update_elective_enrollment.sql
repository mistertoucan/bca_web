CREATE DEFINER=`atcsdevb_devadm`@`%` PROCEDURE `update_elective_enrollment`(IN `sectionID` INT)
    NO SQL
BEGIN
	update elective_section
	set enrolled_count	= (
        select count(*)
				from elective_user_xref x
				where section_id = sectionID
		)
	where section_id = sectionID;
END