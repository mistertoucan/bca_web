from flask import Blueprint

auth_mod = Blueprint('auth', __name__, url_prefix='/auth')

import app.auth.views