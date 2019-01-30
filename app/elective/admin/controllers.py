from app.db import DB, insert, insertmany, query_one, query, delete, update

from app.elective.admin.models import *

from datetime import datetime

# Updates the enroll date for an elective
def update_enroll_date(newDate, trimester_id, grade):
    pass

def get_signup_dates():
    result = query_one(DB.ELECTIVE, "SELECT * "
                                    "FROM signup_dates ")
    return result




