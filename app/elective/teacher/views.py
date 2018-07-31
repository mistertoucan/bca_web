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
    return "Hello world from the teacher route!"

# CRUD

@teacher_mod.route('/<int:id>', methods=['POST'])
def create_elective(id):
    pass

@teacher_mod.route('/<int:id>', methods=['GET'])
def read_elective(id):
    pass

@teacher_mod.route('/<int:id>', methods=['PUT'])
def update_elective(id):
    pass

@teacher_mod.route('/<int:id>', methods=['DELETE'])
def delete_elective(id):
    pass