from flask import Blueprint

from app import login_manager
from werkzeug.contrib.cache import SimpleCache

auth_mod = Blueprint(__name__, 'auth', url_prefix='/auth')

import app.auth.views

cache = SimpleCache()

from app.shared.models import User

@login_manager.user_loader
def load_user(user_id):
    user = cache.get(user_id)

    if user is None:
        user = User.get(user_id)
        cache.set(user_id, user, timeout=5*60)
        return User.get(user_id)
    return user