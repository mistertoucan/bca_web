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
    return render_template("elective/teacher/index.html")

@teacher_mod.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        elective_name = request.form['elective_name']
        elective_desc = request.form['elective_desc']
        sections = request.form['section_time']

        if elective_name and elective_desc and sections:
            id = create_elective(elective_name, elective_desc)
            add_sections(g.user.get_id(), id, sections)

            return redirect(url_for('elective_teacher.index'), 200)

    return render_template("elective/teacher/create.html", electives=get_electives())

@teacher_mod.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    return render_template("elective/teacher/edit.html")