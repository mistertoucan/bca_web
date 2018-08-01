from flask import Blueprint

admin_mod = Blueprint('elective_admin', __name__, url_prefix='/admin')

import app.elective.admin.views