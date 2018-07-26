from flask import Blueprint

admin_mod = Blueprint('admin', __name__, url_prefix='/admin')

@admin_mod.route('/')
def index():
    return "Hello! from admin"