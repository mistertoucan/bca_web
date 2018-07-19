from app.db import DB, query

class TestUser(object):

    def __init__(self, id, first_name, last_name, year, role):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.year = year
        self.role = role


def get_admins():
    return get_users("ADM")

def get_teachers():
    return get_users("TCH")

def get_students():
    return get_users("STD")

def get_users(role):
    queryUsers = query(DB.SHARED, "SELECT usr_first_name, usr_last_name, usr_id, usr_grade_lvl, usr_type_cde FROM user WHERE usr_type_cde = %s", [role])
    roleUsers = []

    for user in queryUsers:
        testUser = TestUser(user[2], user[0], user[1], user[3], user[4])
        roleUsers.append(testUser)

    return roleUsers
