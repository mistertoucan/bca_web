from app.elective.admin import admin_mod

from app.shared.controllers import requires_token
from app.elective.teacher.controllers import get_electives

from flask import g, redirect, url_for, render_template, request

@admin_mod.before_request
@requires_token
def check_teacher():
    if g.user.get_role('ELEN') != 'ADM':
        return redirect(url_for('elective'))

# TODO: Make admin route a way to update trimester/elective enroll opening/closings
# Admins should be able to look up 
@admin_mod.route('/')
def index():
    return render_template("./elective/admin/index.html", electives=get_electives())

@admin_mod.route('/signup_dates')
def signup_dates():
    return render_template("./elective/admin/signup_dates.html")

@admin_mod.route('/signup_dates', methods=['PUT'])
def ping():
    data = request.get_json(force=True, silent=True)

    date = data['section_ids']