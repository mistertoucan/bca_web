from app.elective.student import student_mod

from app.shared.controllers import requires_token

from flask import g, redirect

@student_mod.before_request
@requires_token
def check_teacher():
    if g.user.get_type_code() != 'TCH':
        return redirect('elective')

@student_mod.route('/')
def index():
    return "Hello world from teacher route!"