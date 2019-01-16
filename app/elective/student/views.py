from app.elective.student import student_mod

from app.shared.controllers import requires_token
from app.elective.student.controllers import *

from flask import g, redirect, url_for, render_template, request, jsonify
import time

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
    if g.user.get_role('ELEN') != 'STD':
        return redirect(url_for('elective'))

# pages

# A route for the student_mod app
@student_mod.route('/')
def index():

    current_info = get_current_info()

    enrolled_sections = get_enrolled_sections(g.user.get_id(), current_info[0], current_info[1])
    sections = get_sections(current_info[0], current_info[1])
    enroll_info = get_enrollment_time(g.user.get_grade_level())

    return render_template("elective/student/index.html", sections=sections, enroll_info=enroll_info, enrolled_sections=enrolled_sections)

@student_mod.route('/enroll/<int:id>', methods=['PUT'])
def enroll(id):
    data = request.get_json(force=True, silent=True)

    section_id = id
    usr_id = data['usr_id']
    enroll = data['enroll']

    if enrollment_open(g.user.get_grade_level()):
        if enroll:
            if not is_section_full(section_id):
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
    data = request.get_json(force=True, silent=True)

    section_ids = data['section_ids']

    if(section_ids):

        amount_left = {}

        for i in range(len(section_ids)):
            amount_left[section_ids[i]] = get_amount_left(section_ids[i])

        return jsonify(amount_left)

    else:
        return jsonify({"Error": "Invalid parameters"})