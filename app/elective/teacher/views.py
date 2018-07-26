from app.elective.teacher import teacher_mod

from app.shared.controllers import requires_token

from flask import g, redirect

@teacher_mod.before_request
@requires_token
def check_teacher():
    if g.user.get_type_code() != 'TCH':
        return redirect('elective')

@teacher_mod.route('/')
def index():
    return "Hello world from teacher route!"