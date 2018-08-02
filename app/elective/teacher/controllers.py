from app.db import DB, insert, insertmany, query_one, query

from app.elective.teacher.models import *

# creates an elective and returns its id
def create_elective(name, desc):
    insert(DB.ELECTIVE, "INSERT INTO elective (name, `desc`) VALUES (%s, %s)", (name, desc))
    return query_one(DB.ELECTIVE, "SELECT elective_id FROM elective WHERE name=%s and `desc`=%s", [name, desc])[0]

# uses insert many
# sections is a list of section_time strings
def add_sections(elective_id, teacher_id, sections, room_nbr, year, tri):
    year = "%d-%s" % (year, str(year+1)[2:])

    elective_sections = []

    for i in range(len(sections)):
        cs_times = sections[i]

        cs_ids = []

        for time_desc in cs_times.split(", "):
            time_id = query_one(DB.ELECTIVE, "SELECT time_id FROM elective_time WHERE time_short_desc=%s", [time_desc])[
                0]

            cs_ids.append(time_id)

        elective_sections.append(cs_ids)

    for i in range(len(elective_sections)):
        section_time_ids = elective_sections[i]

        section_nbr = query(DB.ELECTIVE, "SELECT COUNT(*) FROM elective_section WHERE elective_id=%s", [elective_id])

        insert(DB.ELECTIVE, "INSERT INTO elective_section (elective_id, section_nbr, teacher_id, room_nbr, course_year, tri) VALUES (%s, %s, %s, %s, %s, %s)", [elective_id, section_nbr, teacher_id, room_nbr, year, tri])

        section_id = query_one(DB.ELECTIVE, "SELECT section_id FROM elective_section WHERE elective_id=%s AND section_nbr=%s", [elective_id, section_nbr])

        data = []

        for time_id in section_time_ids:
            data.append([section_id, time_id])

        insertmany(DB.ELECTIVE, "INSERT INTO elective_section_time_xref (section_id, time_id) VALUES (%s, %s)", data)

# uses single insert
# times is a string of the sections times
def add_section(elective_id, teacher_id, times, room_nbr, year, tri):

    year = "%d-%s" % (year, str(year + 1)[2:])

    time_ids = []

    for time_desc in times.split(", "):
        time_id = query_one(DB.ELECTIVE, "SELECT time_id FROM elective_time WHERE time_short_desc=%s", [time_desc])[0]

        time_ids.append(time_id)

    section_nbr = query_one(DB.ELECTIVE, "SELECT COUNT(*) FROM elective_section WHERE elective_id=%s", [elective_id])[0]

    insert(DB.ELECTIVE, "INSERT INTO elective_section (elective_id, section_nbr, teacher_id, room_nbr, course_year, tri) VALUES (%s, %s, %s, %s, %s, %s)", [elective_id, section_nbr, teacher_id, room_nbr, year, tri])

    section_id = query_one(DB.ELECTIVE, "SELECT elective_id FROM elective_section WHERE elective_id=%s AND section_nbr=%s", [elective_id, section_nbr])[0]

    data = []

    for time_id in time_ids:
        data.append([section_id, time_id])

    insertmany(DB.ELECTIVE, "INSERT INTO elective_section_time_xref (section_id, time_id) VALUES (%s, %s)", data)

def get_electives():
    result = query(DB.ELECTIVE, "SELECT elective_id, name, `desc` FROM elective ORDER BY name")

    electives = []

    for elective in result:
        electives.append(Elective(elective[0], elective[1], elective[2]))

    return electives

def get_sections(user_id):
    elective_sections = query(DB.ELECTIVE, "SELECT es.section_id, es.section_nbr, es.tri, es.course_year, es.max, e.elective_id, e.name, e.desc, time.time_id, time.day, time.time_short_desc "
                                           "FROM elective_section es, elective e, elective_section_time_xref x, elective_time time"
                                           "WHERE es.teacher_id = %s "
                                           "AND es.elective_id = e.elective_id "
                                           "AND x.section_id = es.section_id "
                                           "AND x.time_id = time.time_id ", [user_id])

    sections = []

    for result in elective_sections:
        elective_id = result[5]
        elective_name = result[6]
        elective_desc = result[7]


        elective = Elective(elective_id, elective_name, elective_desc)

        time_id = result[8]
        time_day = result[9]
        time_desc = result[10]

        elective_time = ElectiveTime(time_id, time_day, time_desc)

        section_id = result[0]
        section_nbr = result[1]
        section_tri = result[2]
        section_year = result[3]
        section_max = result[4]

        section = ElectiveSection(section_id, elective, section_nbr, section_tri, section_year, section_max, elective_time)

        sections.append(section)

    return sections


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