from app.db import DB, insert, insertmany, query_one, query

# creates an elective and returns its id
def create_elective(name, desc):
    insert(DB.ELECTIVE, "INSERT INTO elective (name, desc) VALUES (%s, %s)", [name, desc])
    return query_one(DB.ELECTIVE, "SELECT elective_id FROM elective WHERE name=%s and desc=%s", [name, desc])[0]


def add_sections(teacher_id, elective_id, sections):
    elective_sections = []

    for i in range(len(sections)):
        cs_times = sections[i]

        cs_ids = []

        for time in cs_times.split(", "):
            time_desc = time[:-1]

            time_id = query_one(DB.ELECTIVE, "SELECT time_id FROM elective_time WHERE time_short_desc=%s", [time_desc])[
                0]

            cs_ids.append(time_id)

        elective_sections.append(cs_ids)

def get_electives():
    return query(DB.ELECTIVE, "SELECT name, elective_id FROM elective ORDER BY name;")