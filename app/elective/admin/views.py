from app.elective.admin import admin_mod

from app.shared.controllers import requires_token

from flask import g, redirect

@admin_mod.before_request
@requires_token
def check_teacher():
    if g.user.get_type_code() != 'TCH':
        return redirect('elective')

@admin_mod.route('/')
def index():
    return "Hello world from teacher route!"