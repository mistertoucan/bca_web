from app import mysql
from enum import Enum


class DB(Enum):
    SHARED = "atcsdevb_dev_shared"
    CAREER_DAY = "atcsdevb_dev_career_day"
    FIELD_DAY = "actcsdevb_dev_field_day"
    GRADE_REQ = "atcsdevb_dev_grade_req"
    IDA = "atcsdevb_dev_ida"
    OFF_HR_ELECTIVES = "atcsdevb_dev_off_hour_electives"
    PROCTORING = "actsdevb_dev_proctoring"
    PROJECTS = "atcsdevb_dev_projects"
    SEN_EXP = "atcsdevb_dev_senexp"
    ELECTIVE="atcsdevb_dev_electives"

    def __str__(self):
        return str(self.value)

# Executes the statemet and then returns the result
# Statement - SQL Query
# Vars - List of variables in Query to prevent SQL Injection
def query(db, statement, vars="", display=False):
    cur = mysql.get_db().cursor()
    use_db(cur, db)

    if vars:
        cur.execute(statement, vars)
    else:
        cur.execute(statement)

    if display:
        log_print("QUERY", db, statement, vars)

    result = cur.fetchall()
    cur.connection.commit()
    return result


# only searches for one return option/value
def query_one(db, statement, vars="", display=False):
    cur = mysql.get_db().cursor()
    use_db(cur, db)

    if vars:
        cur.execute(statement, vars)
    else:
        cur.execute(statement)

    if display:
        log_print("QUERY", db, statement, vars)
    return cur.fetchone()


def insert(db, statement, vars, display=False):
    cur = mysql.get_db().cursor()
    use_db(cur, db)

    cur.execute(statement, vars)

    cur.connection.commit()

    if display:
        log_print("INSERT", db, statement, vars)

def insertmany(db, statement, data, display=False):
    cur = mysql.get_db().cursor()
    use_db(cur, db)

    cur.executemany(statement, data)

    cur.connection.commit()

    if display:
        log_print("INSERT", db, statement, data)


def update(db, statement, vars="", display=False):
    cur = mysql.get_db().cursor()
    use_db(cur, db)

    if vars:
        cur.execute(statement, vars)
    else:
        cur.execute(statement)

    cur.connection.commit()

    if display:
        log_print("UPDATED", db, statement, vars)


def delete(db, statement, vars="", display=False):
    cur = mysql.get_db().cursor()
    use_db(cur, db)

    if vars:
        cur.execute(statement, vars)
    else:
        cur.execute(statement)

    cur.connection.commit()

    if display:
        log_print("DELETE", db, statement, vars)


def use_db(cur, db, display=False):
    if display:
        print("Using db, %s" % db)
    cur.execute('USE ' + str(db))

def log_print(operation, db, statement, values):
    print("%s @ %s: '%s', %s " % (operation, db, statement, values))