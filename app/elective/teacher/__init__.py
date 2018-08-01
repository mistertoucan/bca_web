from flask import Blueprint

teacher_mod = Blueprint('elective_teacher', __name__, url_prefix='/teacher')

import app.elective.teacher.views