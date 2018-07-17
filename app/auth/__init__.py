from flask import Blueprint

from app import login_manager

auth_mod = Blueprint(__name__, 'auth', url_prefix='/auth')

import app.auth.views


from app.shared.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)