from flask import Blueprint
from flask_breadcrumbs import default_breadcrumb_root

board_mod = Blueprint('dashboard', __name__, url_prefix='/dashboard')

default_breadcrumb_root(board_mod, '.')

import app.dashboard.views