from app.elective.teacher import teacher_mod

from app.shared.controllers import requires_token

from flask import g, redirect, render_template, request

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
        data = request.form

    return render_template("elective/teacher/create.html")

@teacher_mod.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    return render_template("elective/teacher/edit.html")