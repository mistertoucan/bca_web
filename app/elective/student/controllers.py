from app.db import DB, insert, insertmany, query_one, query, delete, update

from app.elective.student.models import ElectiveSection, Elective, ElectiveTeacher, EnrollmentTime

from util import datetime_from_string, us_format

from datetime import datetime

# Make Query to DB to check whether enrollment is open for grade level
def get_enrollment_time(grade_level):
    result = query_one(DB.ELECTIVE, "SELECT * "
                                  "FROM signup_dates t "
                                  "WHERE t.grade_lvl = %s "
                                  "AND NOW() >= t.start "
                                  "AND NOW() < t.end", [grade_level])

    if result:

        start_time = result[1]
        end_time = result[2]

        return EnrollmentTime(result[0], start_time, end_time, result[3], result[4])
    else:
        return EnrollmentTime(grade_level, None, None, get_current_year(), '-1')

def enrollment_open(grade_level):
    result = query_one(DB.ELECTIVE, "SELECT * "
                                  "FROM signup_dates t "
                                  "WHERE t.grade_lvl = %s "
                                  "AND NOW() >= t.start "
                                  "AND NOW() <= t.end", [grade_level])

    return (not result is None)


# Enroll a user in an elective section
def enroll(usr_id, section_id):
    insert(DB.ELECTIVE, 'INSERT INTO elective_user_xref (section_id, usr_id) VALUES (%d, %d)', [section_id, usr_id])

    return True

# Remove a user from an elective_section
def drop_section(usr_id, section_id):
    delete(DB.ELECTIVE, 'DELETE FROM elective_user_xref WHERE usr_id=%s AND section_id=%s', [usr_id, section_id])

    return True

# Returns whether an elective
def is_section_full(section_id):

    section_info = query_one(DB.ELECTIVE, "SELECT enrolled_count, max "
                                     "FROM elective_section "
                                     "WHERE section_id = %d", section_id)

    return section_info[0] >= section_info[1]

def get_enrolled_sections(usr_id, year, tri):

    sections = query(DB.ELECTIVE, 'SELECT section.section_id, section.elective_id, e.name, e.desc, e.prereq, section.room_nbr, section.enrolled_count, section.section_nbr, section.max, t.usr_id, t.usr_first_name, t.usr_last_name '
                                      'FROM elective_section section, elective e, user t '
                                      'WHERE course_year = %s '
                                      'AND tri = %s '
                                      'AND e.elective_id = section.elective_id '
                                      'AND t.usr_id = section.teacher_id ', [year, int(tri)])

    e_sections = []

    for section in sections:
        elective_id = section[1]
        elective_name = section[2]
        elective_desc = section[3]
        elective_prereq = section[4]

        section_id = section[0]
        section_room_nbr = section[5]
        section_max = section[6]
        section_enrolled = section[7]
        section_nbr = section[8]

        teacher_id = section[9]
        teacher_first_name = section[10]
        teacher_last_name = section[11]

        elective = Elective(elective_id, elective_name, elective_desc, elective_prereq)
        teacher = ElectiveTeacher(teacher_id, teacher_first_name, teacher_last_name)
        times = get_times(section_id)

        e_sections.append(ElectiveSection(section_id, elective, section_nbr, tri, year, section_enrolled, section_max,
                                          section_room_nbr, teacher, times, False))

    return e_sections

# Get all sections available for a user
def get_sections(user_id, year, tri):

    sections = []

    if year != -1 and tri != -1:

        sections = query(DB.ELECTIVE,
                         'SELECT section.section_id, section.elective_id, e.name, e.desc, e.prereq, section.room_nbr, section.enrolled_count, section.section_nbr, section.max, t.usr_id, t.usr_first_name, t.usr_last_name '
                         'FROM elective_section section, elective e, user t '
                         'WHERE course_year = %s '
                         'AND tri = %s '
                         'AND e.elective_id = section.elective_id '
                         'AND section.enrolled_count < section.max '
                         'AND t.usr_id = section.teacher_id ', [year, tri])

    else:

        sections = query(DB.ELECTIVE,
                         'SELECT section.section_id, section.elective_id, e.name, e.desc, e.prereq, section.room_nbr, section.enrolled_count, section.section_nbr, section.max, t.usr_id, t.usr_first_name, t.usr_last_name '
                         'FROM elective_section section, elective e, user t '
                         'WHERE e.elective_id = section.elective_id '
                         'AND t.usr_id = section.teacher_id ')

    e_sections = []

    for section in sections:
        print(section)

        elective_id = section[1]
        elective_name = section[2]
        elective_desc = section[3]
        elective_prereq = section[4]

        section_id = section[0]
        section_room_nbr = section[5]
        section_enrolled = section[6]
        section_nbr = section[7]
        section_max = section[8]

        teacher_id = section[9]
        teacher_first_name = section[10]
        teacher_last_name = section[11]

        elective = Elective(elective_id, elective_name, elective_desc, elective_prereq)
        teacher = ElectiveTeacher(teacher_id, teacher_first_name, teacher_last_name)
        times = get_times(section_id)

        s = ElectiveSection(section_id, elective, section_nbr, tri, year, section_enrolled, section_max,
                            section_room_nbr, teacher, times, False)

        s.teacher = teacher

        e_sections.append(s)

    return e_sections

# Get all current elective sections for a tri/year
def get_sections(year, tri):

    sections = query(DB.ELECTIVE, 'SELECT section.section_id, section.elective_id, e.name, e.desc, e.prereq, section.room_nbr, section.enrolled_count, section.section_nbr, section.max, t.usr_id, t.usr_first_name, t.usr_last_name '
                                      'FROM elective_section section, elective e, user t '
                                      'WHERE e.elective_id = section.elective_id '
                                      'AND t.usr_id = section.teacher_id ')

    e_sections = []

    for section in sections:
        print(section)

        elective_id = section[1]
        elective_name = section[2]
        elective_desc = section[3]
        elective_prereq = section[4]

        section_id = section[0]
        section_room_nbr = section[5]
        section_enrolled = section[6]
        section_nbr = section[7]
        section_max = section[8]

        teacher_id = section[9]
        teacher_first_name = section[10]
        teacher_last_name = section[11]


        elective = Elective(elective_id, elective_name, elective_desc, elective_prereq)
        teacher = ElectiveTeacher(teacher_id, teacher_first_name, teacher_last_name)
        times = get_times(section_id)

        s = ElectiveSection(section_id, elective, section_nbr, tri, year, section_enrolled, section_max,
                        section_room_nbr, teacher, times, False)

        s.teacher = teacher

        e_sections.append(s)


    return e_sections

# Returns the current school year formatted in "YEAR-END_YEAR" form
def get_current_year():
    return '%d-%d' % (datetime.utcnow().year, datetime.utcnow().year + 1)

# Temporary solution for getting the corresponding times for a section
def get_times(section_id):
    result = query(DB.ELECTIVE, "SELECT time_short_desc "
                                   "FROM elective_time time, elective_section_time_xref x "
                                   "WHERE x.section_id = %s "
                                   "AND time.time_id = x.time_id", [section_id])
    times = []
    for time in result:
        times.append(time)

    return times

# Returns the current '%d-%d' year string and trimester
def get_current_info():
    current_year = get_current_year()

    formatted_year = str(current_year.split('-')[0])

    print(formatted_year)

    # ps_year format - Ex: 2018 = 28
    formatted_year = formatted_year[0] + formatted_year[-1]

    current_tri = query_one(DB.ELECTIVE, 'SELECT tri_nbr FROM atcsdevb_dev_shared.trimester ' +
                                         'WHERE NOW() <= end_dt ' +
                                         'AND NOW() >= start_dt ' +
    #                                    'AND ps_year = %s ' +
                                         'ORDER BY end_dt')[0]
    return [current_year, current_tri]

def get_amount_left(section_id):
    section_info = query_one(DB.ELECTIVE, "SELECT es.max - es.enrolled_count "
                                          "FROM elective_section es "
                                          "WHERE section_id = %d", [section_id])[0]

    return section_info