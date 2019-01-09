from app.db import DB, query

from app.dashboard.models import *

def get_admins(app_cde):
    return get_users("ADM", app_cde)

def get_teachers(app_cde):
    return get_users("TCH", app_cde)

def get_students(app_cde):
    return get_users("STD", app_cde)

def get_users(role, app_cde):

    queryUsers = []

    if app_cde:
        queryUsers = query(DB.SHARED, "SELECT u.usr_first_name, u.usr_last_name, u.usr_id, u.usr_grade_lvl, u.usr_type_cde FROM user u, role_application_user_xref x WHERE u.usr_id = x.usr_id AND x.app_cde = %s AND x.usr_role_cde=%s", [app_cde, role])
    else:
        queryUsers = query(DB.SHARED, "SELECT u.usr_first_name, u.usr_last_name, u.usr_id, u.usr_grade_lvl, u.usr_type_cde FROM user u WHERE u.usr_type_cde=%s", [role])

    roleUsers = []

    for user in queryUsers:
        testUser = TestUser(user[2], user[0], user[1], user[3], user[4])
        roleUsers.append(testUser)


    return roleUsers


def list_upcoming_test_limited(self):
    tests = query(DB.PROCTORING,
                      'select t.test_name, t.test_id, CURDATE(), date_format(t.test_dt, "%b %e (%a)") as test_dt, datediff(test_dt, curdate()) as difference, reminder_sent_dt, test_time_desc, r.rm_nbr '
                      'from test t, test_time_xref tx, test_updt_xref ux, test_time tt, room r'
                      'where t.test_dt >= curdate()'
                      'and t.test_id = tx.test_id'
                      'and tx.test_id = ux.test_id'
                      'and tx.test_time_id = ux.test_time_id'
                      'and tx.test_time_id = tt.test_time_id'
                      'and ux.usr_id = %s'
                      'and t.rm_id = r.rm_id'
                      'order by difference, tt.sort_order'
                      'limit 4', [self.__usr_id__])
    return tests