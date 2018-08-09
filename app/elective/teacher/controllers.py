from app.db import DB, insert, insertmany, query_one, query, delete

from app.elective.teacher.models import *

from app.shared.models import User

from datetime import datetime

# creates an elective and returns its id
def create_elective(name, desc, course_id, prereq):
    if not course_id:
        if prereq:
            insert(DB.ELECTIVE, "INSERT INTO elective (name, `desc`, course_id, prereq) VALUES (%s, %s, %s, %s)", (name, desc, course_id, prereq))
        else:
            insert(DB.ELECTIVE, "INSERT INTO elective (name, `desc`, course_id) VALUES (%s, %s, %s, %s)",
                   (name, desc, course_id))
    else:
        if prereq:
            insert(DB.ELECTIVE, "INSERT INTO elective (name, `desc`, prereq) VALUES (%s, %s, %s)", (name, desc, prereq))
        else:
            insert(DB.ELECTIVE, "INSERT INTO elective (name, `desc`) VALUES (%s, %s)", (name, desc))

    return query_one(DB.ELECTIVE, "SELECT elective_id FROM elective WHERE name=%s AND `desc`=%s", [name, desc])[0]

# uses insert many
# sections is a list of section_time strings
def add_sections(elective_id, teacher_id, times, room_nbrs, years, tris):
    for i in range(len(times)):
        time = times[i]
        room = room_nbrs[i]
        year = years[i]
        tri = tris[i]
        add_section(elective_id, teacher_id, time, room, year, tri)

# uses single insert
# times is a string of the sections times
def add_section(elective_id, teacher_id, times, room_nbr, year, tri):
    time_ids = []

    for time_desc in times.split(", "):
        time_id = query_one(DB.ELECTIVE, "SELECT time_id FROM elective_time WHERE time_short_desc=%s", [time_desc])[0]

        time_ids.append(time_id)

    section_nbr = query_one(DB.ELECTIVE, "SELECT COUNT(*) FROM elective_section WHERE elective_id=%s", [elective_id])[0]+1

    insert(DB.ELECTIVE, "INSERT INTO elective_section (elective_id, section_nbr, teacher_id, room_nbr, course_year, tri) VALUES (%s, %s, %s, %s, %s, %s)", [elective_id, section_nbr, teacher_id, room_nbr, year, tri])

    section_id = query_one(DB.ELECTIVE, "SELECT section_id FROM elective_section WHERE elective_id=%s AND section_nbr=%s", [elective_id, section_nbr])[0]

    data = []

    for time_id in time_ids:
        data.append([section_id, time_id])

    insertmany(DB.ELECTIVE, "INSERT INTO elective_section_time_xref (section_id, time_id) VALUES (%s, %s)", data)

def get_electives():
    result = query(DB.ELECTIVE, "SELECT elective_id, name, `desc`, course_id FROM elective ORDER BY name")

    electives = []

    for elective in result:
        electives.append(Elective(elective[0], elective[1], elective[2], elective[3]))

    return electives

# Exclude is a list of user ids which should be excluded from the query
def get_students(exclude=[]):
    users = query(DB.ELECTIVE, "SELECT usr_id, usr_first_name, usr_last_name, academy_cde, usr_class_year "
                             "FROM user "
                             "WHERE usr_type_cde='STD'", [])

    students = []

    for user in users:
        if not user[0] in exclude:
            students.append(Student(user[0], user[1], user[2], user[3], user[4]))

    return students

def get_section_students(section_id):
    users = query(DB.ELECTIVE, "SELECT usr_id FROM elective_user_xref WHERE section_id=%s", [section_id])

    students = []

    for user in users:
        info = query_one(DB.ELECTIVE, "SELECT usr_id, usr_first_name, usr_last_name, academy_cde, usr_class_year "
                             "FROM user "
                             "WHERE usr_type_cde='STD' "
                             "AND usr_id=%s", [user[0]])
        students.append(Student(info[0], info[1], info[2], info[3], info[4]))

    return students

def add_student(section_id, user_id):
    insert(DB.ELECTIVE, "INSERT INTO elective_user_xref (section_id, usr_id) VALUES (%s, %s)", [section_id, user_id])

def remove_student(section_id, user_id):
    delete(DB.ELECTIVE, "DELETE FROM elective_user_xref "
                        "WHERE section_id=%s "
                        "AND usr_id=%s", [section_id, user_id])

def get_sections(user_id):
    elective_sections = query(DB.ELECTIVE, "SELECT es.elective_id, es.section_id, es.section_nbr, es.tri, es.course_year, es.max, es.room_nbr, es.teacher_id "
                                           "FROM elective_section es  "
                                           "WHERE es.teacher_id = %s "
                                           "ORDER BY es.course_year DESC", [user_id])

    sections = []

    for result in elective_sections:

        elective_id = result[0]

        elective_result = query_one(DB.ELECTIVE, "SELECT name, `desc`, course_id "
                                          "FROM elective "
                                          "WHERE elective_id = %s", [elective_id])

        elective_name = elective_result[0]
        elective_desc = elective_result[1]
        elective_course_id = elective_result[2]


        elective = Elective(elective_id, elective_name, elective_desc, elective_course_id)

        section_id = result[1]
        section_nbr = result[2]
        section_tri = result[3]
        section_year = result[4]
        section_max = result[5]
        section_room_nbr = result[6]

        section_teacher_id = result[6]

        if int(section_year.split("-")[0]) < datetime.utcnow().year:
            continue

        teacher = get_teacher(section_teacher_id)

        section = ElectiveSection(section_id, elective, section_nbr, section_tri, section_year, section_max, section_room_nbr, teacher)

        section.times = get_times_by_section_id(section_id)

        section.enrolled = query_one(DB.ELECTIVE, "SELECT COUNT(*) FROM elective_user_xref "
                                                  "WHERE section_id=%s", [section_id])[0]

        sections.append(section)

    return sections

def get_teacher(id):

    teacher = User.get(id)

    if teacher:
        return ElectiveTeacher(id, teacher.get_name())
    return None

# returns all available times for a user
def get_times(user_id):
    result = query(DB.ELECTIVE, "SELECT x.time_id, day, mods "
                                "FROM elect_user_xref x, elect_time e "
                                "WHERE x.usr_id = %s "
                                "AND x.time_id = e.time_id", [user_id])
    times = []

    for time in result:
        times.append(ElectiveTime(time[0], time[1], time[2]))

    return times

def get_times_by_section_id(section_id):
    times = []

    for result in query(DB.ELECTIVE, "SELECT time.time_id, time.day, time.time_short_desc "
                                   "FROM elective_time time, elective_section_time_xref x, elective_section es "
                                   "WHERE es.section_id = %s "
                                   "AND x.section_id = es.section_id "
                                   "AND x.time_id = time.time_id ", [section_id]):
        time = ElectiveTime(result[0], result[1], result[2])

        times.append(time)

    return times

def get_elective(id):
    result = query_one(DB.ELECTIVE, "SELECT elective_id, name, `desc`, course_id "
                                  "FROM elective "
                                  "WHERE elective_id = %s", [id])
    if result:
        elective = Elective(result[0], result[1], result[2], result[3])

        sections = query(DB.ELECTIVE, "SELECT section_id, section_nbr, teacher_id, course_year, tri, max, room_nbr, teacher_id "
                                    "FROM elective_section "
                                    "WHERE elective_id = %s", [elective.id])

        for section in sections:
            teacher_id = section[7]

            section = ElectiveSection(section[0], None, section[1], section[4], section[3], section[5], section[6], get_teacher(teacher_id))
            section.times = get_times_by_section_id(section.id)

            elective.sections.append(section)

        return elective

    return None

def delete_section(teacher_id, section_id):
    can_delete = query_one(DB.ELECTIVE, "SELECT * FROM elective_section WHERE section_id=%s AND teacher_id=%s", [section_id, teacher_id]) != None
    print(can_delete)
    print(teacher_id)
    print(section_id)

    if can_delete:
        delete(DB.ELECTIVE, "DELETE FROM elective_user_xref WHERE section_id=%s", [section_id])
        delete(DB.ELECTIVE, "DELETE FROM elective_section_time_xref WHERE section_id=%s", [section_id])
        delete(DB.ELECTIVE, "DELETE FROM elective_section WHERE section_id=%s", [section_id])
        return True
    return False

# def update_section(section_id, elective_name, elective_desc, section_time, section_year, )