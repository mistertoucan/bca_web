from app.elective.student import student_mod

from app.shared.controllers import requires_token
from app.elective.student.controllers import *

from flask import g, redirect, url_for, render_template, request, jsonify

# Explanation:
# This file is a sub app for the elective enroll application
# It is specified for students
# Only students can view these pages
# The First Route Below makes sure that the requester of this app, student_mod, is a student
# If not, the user is redirected to the index page of the 'elective' app itself
# The name of this app is elective_student
# Every individual app on flask has its own name
# Its sub apps have the name '%PRIMARY_APP_NAME%_%SUB_APP_NAME%'
# These names are useful because they can be used to get urls of routes
# For example, url_for('elective.index') would return the route with the function named index

# Checks whether the requester
@student_mod.before_request
@requires_token
def check_teacher():
    if g.user.get_type_code() != 'STD':
        return redirect(url_for('elective'))

# pages

# A route for the student_mod app
@student_mod.route('/')
def index():

    current_info = get_current_info()

    if enrollment_open(g.user.get_grade_level()):
        sections = get_sections(current_info[0], current_info[1])

        return render_template('elective/student/index.html', sections=sections)
    else:
        sections = get_user_sections(g.user.get_id(), current_info[0], current_info[1])

        return render_template('elective/student/enroll_closed.html', sections=sections)

    # TODO:
    # GET:
    # Make a query to the SHARED db to table Variable to check whether variable ELECTIVE_ENROLLMENT_OPEN is true
    # If true, render the template elective/student/enroll.html and display all currently open elective section
    # Otherwise, render the template elective/student/enroll_closed.html and display the user's current electives
    pass

@student_mod.route('/enroll/<int:id>', methods=['PUT'])
def enroll(id):
    data = request.get_json(force=True, silent=True)
    section_id = data['section_id']
    usr_id = data['usr_id']
    enroll = data['enroll']
    if enrollment_open(g.user.get_grade_level()):
        if enroll:
            if not is_Section_Full(section_id):
                enroll(usr_id, section_id)
                return jsonify({"has_enrolled": True, "Error": None})
            else:
                return jsonify({"has_enrolled": False, "Error": "Elective Section Full."})
        else:
            drop_section(usr_id, section_id)
            return jsonify({"has_enrolled": False, "Error": None})

    else:
        return jsonify({"has_enrolled": False, "Error": "Enrollment Not Open"})


@student_mod.route('/enroll/update', methods=['PUT'])
def ping():
    # TODO:
    # PUT:
    # section_ids: []
    # Pings server to check whether any elective_enrollment counts have changed/closed
    # If so returns the ids of the ones that have been fulled up
    pass