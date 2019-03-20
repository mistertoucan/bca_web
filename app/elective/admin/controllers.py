from app.db import DB, insert, insertmany, query_one, query, delete, update

from app.elective.admin.models import *

from datetime import datetime

# Updates the enroll date for an elective
def update_enroll_date(grade_lvl, tri_nbr, course_year, start, end):

    update(DB.ELECTIVE, "UPDATE sigup_dates SET tri_nbr=%s, course_year=%s, start=%s, end=%s, trimester "
                        "WHERE grade_lvl=%s", [tri_nbr, course_year, start, end, grade_lvl], True)

def get_signup_dates():
    signup_dates = []
    results = query(DB.ELECTIVE, "SELECT * FROM signup_dates")

    for result in results:
        signup_dates.append(SignupDate(result[0], result[1], result[2], result[3], result[4], result[5]))

    return signup_dates



