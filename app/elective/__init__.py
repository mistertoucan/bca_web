from flask import Blueprint

elective_mod = Blueprint('elective', __name__, url_prefix='/elective')

import app.elective.views