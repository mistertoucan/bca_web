from flask import Blueprint
from app.db import DB, query, query_one

# A simple user class holding a user's id for authentication with flask_login
# After authentication, this class will be available in all requests
class User(object):

    def __init__(self, id):
        self.__usr_id__ = id
        self.name = self.load_name()

    def get_id(self):
        return self.__usr_id__

    def get_name(self):
        return self.name

    def get_grade_level(self):
        return query_one(DB.SHARED, 'SELECT usr_grade_lvl FROM user WHERE usr_id = %s', [self.__usr_id__])[0]

    def load_name(self):
        return query_one(DB.SHARED, 'SELECT usr_first_name, usr_last_name FROM user WHERE usr_id = %s',
                         [self.__usr_id__])

    # returns a list of menu items the user has access to
    def get_apps(self):
        typeCode = self.get_type_code()

        apps = query(DB.SHARED, 'SELECT m.menu_id, title, descr, link, sort_order, target, fa_icon, app_type '
                                'FROM menu_item m, menu_item_user_type_xref ux '
                                'WHERE m.menu_id = ux.menu_id '
                                'AND active = 1 '
                                'union '
                                'SELECT m.menu_id, title, descr, link, sort_order, target, fa_icon, app_type '
                                'FROM menu_item m, menu_item_user_role_xref ur, role_application_user_xref ax '
                                'WHERE m.menu_id = ur.menu_id '
                                'and ur.usr_role_cde = ax.usr_role_cde '
                                'and ur.app_cde = ax.app_cde '
                                'and ax.usr_id = %s '
                                'AND active = 1 '
                                'ORDER BY sort_order ', [self.__usr_id__])
        return apps

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
        result = query_one(DB.SHARED, 'SELECT * FROM user WHERE usr_id=%s AND usr_active=1 LIMIT 1', [id])
        if result:
            type_cde = query_one(DB.SHARED, 'SELECT usr_type_cde FROM user WHERE usr_id = %s', [id])[0]

            if type_cde == 'ADM':
                return Admin(id)
            elif type_cde == 'TCH':
                return Teacher(id)
            elif type_cde == 'STD':
                return Student(id)
            else:
                return User(id)
        return None

class Student(User):
    pass

class Teacher(User):
    pass

class Admin(User):
    pass


class NestableBlueprint(Blueprint):
    """
    Hacking in support for nesting blueprints, until hopefully https://github.com/mitsuhiko/flask/issues/593 will be resolved
    """

    def register_blueprint(self, blueprint, **options):
        def deferred(state):
            url_prefix = (state.url_prefix or u"") + (options.get('url_prefix', blueprint.url_prefix) or u"")
            if 'url_prefix' in options:
                del options['url_prefix']

            print(blueprint.name)

            state.app.register_blueprint(blueprint, url_prefix=url_prefix, **options)
        self.record(deferred)