from flask import Blueprint

admin_mod = Blueprint('admin', __name__, url_prefix='/admin')

import app.elective.admin.views