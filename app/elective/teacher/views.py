from app.elective.teacher import teacher_mod
from app.elective.teacher.controllers import *

from app.shared.controllers import requires_token

from flask import g, redirect, render_template, request, url_for

@teacher_mod.before_request
@requires_token
def check_teacher():
    if g.user.get_type_code() != 'TCH':
        return redirect('elective')

# pages

@teacher_mod.route('/')
def index():
    return render_template("elective/teacher/index.html", electives=get_electives())

@teacher_mod.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        elective_name = request.form['elective_name']
        elective_desc = request.form['elective_desc']

        sections = request.form['section_time']
        section_room_nbr = request.form['section_room_nbr']
        section_year = request.form['section_year']
        section_tri = request.form['section_tri']

        if elective_name and elective_desc and sections and section_room_nbr and section_year and section_tri:
            elective_id = create_elective(elective_name, elective_desc)

            if sections is list:
                add_sections(elective_id, g.user.get_id(), sections, section_room_nbr, section_year, section_tri)
            else:
                add_section(elective_id, g.user.get_id(), sections, section_room_nbr, section_year, section_tri)

            return redirect(url_for('elective_teacher.index'), 200)

    mods = ['1-3', '4-6', '7-9', '10-12', '13-15', '16-18', '19-21', '22-24']
    time_ids = [1, 10, 17, 25, 33, 2, 11, 18, 26, 34, 3, 41, 19, 27, 35, 4, 12, 20, 28, 36, 5, 13, 21, 29, 37, 6, 14, 22, 30, 38, 7, 15, 23, 31, 39, 8, 16, 24, 32, 40]

    return render_template("elective/teacher/create.html", mods=mods, time_ids=time_ids, electives=get_electives())

@teacher_mod.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    return render_template("elective/teacher/edit.html")