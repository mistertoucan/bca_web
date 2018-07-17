from flask_login import UserMixin
from app.db import DB, query

# A simple user class holding a user's id for authentication with flask_login
# After authentication, this class will be available in all requests
class User(UserMixin):

    def __init__(self, id):
        self.__usr_id__ = id

    def get_id(self):
        return self.__usr_id__

    @staticmethod
    def get(id):
        result = query(DB.SHARED, 'SELECT * FROM user WHERE usr_id=%s', [id])
        if result:
            return User(id)
        return None
