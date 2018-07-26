from app.elective.admin import admin_mod

from app.shared.controllers import requires_token

from flask import g, redirect, url_for

@admin_mod.before_request
@requires_token
def check_teacher():
    if g.user.get_type_code() != 'ADM':
        return redirect(url_for('elective'))

@admin_mod.route('/')
def index():
    return "Hello world from teacher route!"