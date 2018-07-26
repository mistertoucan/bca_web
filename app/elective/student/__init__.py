from flask import Blueprint

student_mod = Blueprint('student', __name__, url_prefix='/student')

@student_mod.route('/')
def index():
    return "Hello from student!"