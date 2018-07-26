from app.elective.student import student_mod

from app.shared.controllers import requires_token

from flask import g, redirect, url_for

@student_mod.before_request
@requires_token
def check_teacher():
    if g.user.get_type_code() != 'STD':
        return redirect(url_for('student'))

@student_mod.route('/')
def index():
    return "Hello world from teacher route!"