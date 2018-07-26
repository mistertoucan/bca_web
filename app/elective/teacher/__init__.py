from flask import Blueprint

teacher_mod = Blueprint('teacher', __name__, url_prefix='/teacher')

@teacher_mod.route('/')
def index():
    return "Hello world! from teacher"