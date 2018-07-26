from flask import Blueprint

teacher_mod = Blueprint('teacher', __name__, url_prefix='/teacher')

import app.elective.teacher.views