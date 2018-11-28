from app.db import DB, insert, insertmany, query_one, query, delete, update

from app.elective.student.models import ElectiveSection, Elective, ElectiveTeacher

from datetime import datetime

# TODO: Add enrollment_open table with start/end dates/times
# Make Query to DB to check whether enrollment is open for grade level
def enrollment_open(grade_level):
    pass


# Enroll a user in an elective section
def enroll(usr_id, section_id):
    insert(DB.ELECTIVE, 'INSERT INTO elective_user_xref (section_id, usr_id) VALUES (%d, %d)', [section_id, usr_id])

    return True


# Remove a user from an elective_section
def drop_section(usr_id, section_id):
    delete(DB.SHARED, 'DELETE FROM elective_user_xref WHERE usr_id=%s AND section_id=%s', [usr_id, section_id])

    return True


# TODO: Check whether a section is full by adding enroll_count field to section
# Get all of a users elective sections
def get_user_sections(usr_id, year, tri):
    sections = query(DB.ELECTIVE,
                     'SELECT section.section_id, section.elective_id, e.name, e.desc, e.prereq, t.usr_first_name, t.usr_last_name '
                     'FROM elective_section section, elective e, user t, elective_user_xref x '
                     'WHERE x.usr_id = %s '
                     'AND x.section_id = section.section_id '
                     'AND course_year = %s '
                     'AND tri = %s '
                     'AND e.elective_id = section.elective_id '
                     'AND t.usr_id = section.teacher_id', [int(usr_id), year, int(tri)])


    formatted_sections = []

    for section in sections:
        elective = Elective(section[1], section[2], section[3], section[4])
        formatted_sections.append(ElectiveSection(section[0], elective, section[5], tri, year, False, section[7],
                                          ElectiveTeacher(section[8], (section[9], section[10])), True))

    return formatted_sections


# TODO: Chekck whether a section is full by adding enroll_count field to section
# Get all current elective sections for a tri/year
def get_sections(year, tri):
    sections = query(DB.ELECTIVE, 'SELECT section.section_id, section.elective_id, e.name, e.desc, e.prereq, section.room_nbr, t.usr_id, t.usr_first_name, t.usr_last_name '
                                  'FROM elective_section section, elective e, user t '
                                  'WHERE course_year = %s '
                                  'AND tri = %d '
                                  'AND e.elective_id = section.elective_id '
                                  'AND t.usr_id = section.teacher_id ', [year, tri])

    e_sections = []

    for section in sections:
        elective = Elective(section[1], section[2], section[3], section[4])
        e_sections.append(ElectiveSection(section[0], elective, section[5], tri, year, False, section[7], ElectiveTeacher(section[8], (section[9], section[10])), False))

    return e_sections


# Returns the current school year formatted in "YEAR-END_YEAR" form
def get_current_year():
    return '%d-%d' % (datetime.utcnow().year, datetime.utcnow().year + 1)


# Returns the current '%d-%d' year string and trimester
def get_current_info():
    current_year = get_current_year()

    formatted_year = str(current_year.split('-')[0])

    # ps_year format - Ex: 2018 = 28
    formatted_year = formatted_year[0] + formatted_year[-1]

    current_tri = query_one(DB.ELECTIVE, 'SELECT tri_nbr FROM atcsdevb_dev_shared.trimester ' +
                                         'WHERE NOW() <= end_dt ' +
                                         'AND NOW() >= start_dt ' +
                                         'AND ps_year = %s ' +
                                         'ORDER BY end_dt', [formatted_year])[0]
    return [current_year, current_tri]