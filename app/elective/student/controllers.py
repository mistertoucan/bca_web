from app.db import DB, insert, insertmany, query_one, query, delete, update

from app.elective.student.models import ElectiveSection

from app.shared.models import User

from datetime import datetime

# TODO:
# Make Query to DB to check whether enrollment is open for grade level
def enrollment_open(grade_level):
    return True

# TODO:
# Enroll a user in an elective section
def enroll(user_id, section_id):
    pass

# TODO:
# Get all of a users elective sections
def get_user_sections(usr_id, year, tri):
    return []

# TODO:
# Get all current elective sections for a tri/year
def get_sections(year, tri):
    return []

# Returns the current '%d-%d' year string and trimester
def get_current_info():
    current_year = '%d-%d' % (datetime.utcnow().year, datetime.utcnow().year + 1)
    current_tri = query_one(DB.ELECTIVE, 'SELECT trimester FROM ')