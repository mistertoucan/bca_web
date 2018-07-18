from flask import Flask, redirect, url_for
from flask_mysqldb import MySQL
from flask_login import LoginManager, login_required, current_user
from flask_breadcrumbs import Breadcrumbs, register_breadcrumb

from config import Config

app = Flask(__name__, static_url_path='/static')
app.config.from_object(Config)

mysql = MySQL(app)
login_manager = LoginManager(app)
login_manager.login_view = "auth.login"
Breadcrumbs(app=app)

from app.dashboard import board_mod
app.register_blueprint(board_mod)

from app.auth import auth_mod
app.register_blueprint(auth_mod)

@app.route('/')
def index():
    return redirect(url_for('dashboard.index'))
