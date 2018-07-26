from app.shared.models import NestableBlueprint

elective_mod = NestableBlueprint('elective', __name__, url_prefix='/elective_enroll')

import app.elective.views

from admin import admin_mod
from teacher import teacher_mod
from student import student_mod

elective_mod.register_blueprint(admin_mod)
elective_mod.register_blueprint(teacher_mod)
elective_mod.register_blueprint(student_mod)