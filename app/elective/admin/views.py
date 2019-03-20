from app.elective.admin import admin_mod

from app.shared.controllers import requires_token
from app.elective.teacher.controllers import get_electives
from app.elective.admin.controllers import get_signup_dates, update_enroll_date

from flask import g, redirect, url_for, render_template, request, jsonify, make_response


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
    return render_template("./elective/admin/signup_dates.html", dates=get_signup_dates())

@admin_mod.route('/signup_dates', methods=['PUT'])
def update_dates():
    data = request.get_json(force=True, silent=True)

    grades = data['grades']

    if len(grades) > 0:

        for grade in grades:

            grade_lvl = grade
            tri_nbr = grades[grade]['tri_nbr']
            course_year = grades[grade]['course_year']
            start = grades[grade]['start']
            end = grades[grade]['end']

            update_enroll_date(grade_lvl, tri_nbr, course_year, start, end)

        return make_response(jsonify({'Info': 'Successfully updated.'}), 200)
    else:
        return make_response(jsonify({'Info': 'Missing parameters!'}), 401)

