from app import Config

import mysql.connector
from enum import Enum

mysql = mysql.connector.connect(
    host=Config.MYSQL_HOST,
    user=Config.MYSQL_USER,
    password=Config.MYSQL_PASSWORD
)

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
def query(db, statement, vars=""):
    cur = mysql.cursor()
    use_db(cur, db)

    if vars:
        cur.execute(statement, vars)
    else:
        cur.execute(statement)

    log_print("QUERY", db, statement, vars)

    result = cur.fetchall()
    mysql.commit()
    return result


# only searches for one return option/value
def query_one(db, statement, vars=""):
    cur = mysql.cursor()
    use_db(cur, db)

    if vars:
        cur.execute(statement, vars)
    else:
        cur.execute(statement)

    log_print("QUERY", db, statement, vars)

    result = cur.fetchone()

    mysql.commit()

    return result

def insert(db, statement, vars):
    cur = mysql.cursor()
    use_db(cur, db)

    cur.execute(statement, vars)

    mysql.commit()

    log_print("INSERT", db, statement, vars)

def insertmany(db, statement, data):
    cur = mysql.cursor()
    use_db(cur, db)

    cur.executemany(statement, data)

    mysql.commit()

    log_print("INSERT", db, statement, data)


def update(db, statement, vars=""):
    cur = mysql.cursor()
    use_db(cur, db)

    if vars:
        cur.execute(statement, vars)
    else:
        cur.execute(statement)

    mysql.commit()

    log_print("UPDATED", db, statement, vars)


def delete(db, statement, vars=""):
    cur = mysql.cursor()
    use_db(cur, db)

    if vars:
        cur.execute(statement, vars)
    else:
        cur.execute(statement)

    mysql.commit()

    log_print("DELETE", db, statement, vars)


def use_db(cur, db):
    print("Using db, %s" % db)
    cur.execute('USE ' + str(db))

def log_print(operation, db, statement, values):
    print("%s @ %s: '%s', %s " % (operation, db, statement, values))