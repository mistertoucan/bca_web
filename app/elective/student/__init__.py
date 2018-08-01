from flask import Blueprint

student_mod = Blueprint('elective_student', __name__, url_prefix='/student')

import app.elective.student.views