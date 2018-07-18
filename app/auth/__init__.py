from flask import Blueprint
from werkzeug.contrib.cache import SimpleCache

from app import login_manager, Config

auth_mod = Blueprint('auth', __name__, url_prefix='/auth')

import app.auth.views

cache = SimpleCache()

from app.shared.models import User

@login_manager.user_loader
def load_user(user_id):
    user = cache.get(user_id)

    if user is None:
        user = User.get(user_id)
        cache.set(user_id, user, timeout=Config.CACHE_TIMEOUT)
        return User.get(user_id)
    return user