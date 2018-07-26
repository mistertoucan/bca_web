from flask_login import UserMixin
from app.db import DB, query, query_one

# A simple user class holding a user's id for authentication with flask_login
# After authentication, this class will be available in all requests
class User(UserMixin):

    def __init__(self, id):
        self.__usr_id__ = id
        self.apps = self.load_apps()

    def get_id(self):
        return self.__usr_id__

    def get_name(self):
        return query_one(DB.SHARED, 'SELECT usr_first_name, usr_last_name FROM user WHERE usr_id = %s', [self.__usr_id__])

    # returns a list of menu items the user has access to
    def load_apps(self):
        typeCode = self.get_type_code()

        apps = query(DB.SHARED, 'SELECT m.menu_id, title, descr, link, sort_order, target, fa_icon '
                                'FROM menu_item m, menu_item_user_type_xref ux '
                                'WHERE m.menu_id = ux.menu_id '
                                'AND ux.usr_type_cde = %s '
                                'AND active = 1 '
                                'union '
                                'SELECT m.menu_id, title, descr, link, sort_order, target, fa_icon '
                                'FROM menu_item m, menu_item_user_role_xref ur, role_application_user_xref ax '
                                'WHERE m.menu_id = ur.menu_id '
                                'and ur.usr_role_cde = ax.usr_role_cde '
                                'and ur.app_cde = ax.app_cde '
                                'and ax.usr_id = %s '
                                'AND active = 1 '
                                'ORDER BY sort_order ', [typeCode, self.__usr_id__])
        return apps

    def get_apps(self):
        return self.apps

    def get_type_code(self):
        return query_one(DB.SHARED, 'SELECT usr_type_cde FROM user WHERE usr_id = %s', [self.__usr_id__])[0]

    def get_roles(self):
        roles = query(DB.SHARED, 'SELECT app_cde, usr_role_cde '
                                'FROM role_application_user_xref '
                                'WHERE usr_id = %s', [self.__usr_id__])
        userRoles = dict()
        for role in roles:
            userRoles[role[0]] = role[1]
        return userRoles

    def get_role(self, app_id):
        return self.appRoles[app_id]


    @staticmethod
    def get(id):
        result = query_one(DB.SHARED, 'SELECT * FROM user WHERE usr_id=%s LIMIT 1', [id])
        if result:
            return User(id)
        return None