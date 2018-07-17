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

# Executes the statemet and then returns the result
# Statement - SQL Query
# Vars - Tuple of variables in Query to prevent SQL Injection
def query(db, statement, vars=""):
    cur = mysql.connection.cursor()
    use_db(cur, db)

    if vars:
        cur.execute(statement, vars)
    else:
        cur.execute(statement)

    rv = cur.fetchall()
    return str(rv)

def insert(db, statement, vars=""):
    cur = mysql.connection.cursor()
    use_db(cur, db)

    if vars:
        cur.execute(statement, vars)
    else:
        cur.execute(statement)

    cur.execute(statement, vars)
    mysql.connect().commit()

def update(db, statement, vars=""):
    cur = mysql.connection.cursor()
    use_db(cur, db)

    if vars:
        cur.execute(statement, vars)
    else:
        cur.execute(statement)

    cur.execute(statement, vars)
    mysql.connect().commit()

def delete(db, statement, vars=""):
    cur = mysql.connect.cursor()
    use_db(cur, db)

    if vars:
        cur.execute(statement, vars)
    else:
        cur.execute(statement)

    cur.execute(statement, vars)
    mysql.connect().commit()

def use_db(cur, db):
    print("Using db, %s" % db)
    cur.execute('USE ' + db)