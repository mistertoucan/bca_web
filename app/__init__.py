from flask import Flask, render_template
from flask_mysqldb import MySQL
from flask_login import LoginManager, login_required, current_user
from flask_breadcrumbs import Breadcrumbs, register_breadcrumb

from config import Config

app = Flask(__name__, static_url_path='/static')
app.config.from_object(Config)

mysql = MySQL(app)
login_manager = LoginManager(app)
login_manager.login_view = "app.auth.login"
Breadcrumbs(app=app)

from app.auth import auth_mod
app.register_blueprint(auth_mod)

@app.route('/')
@register_breadcrumb(app, '.', 'Dashboard')
@login_required
def index():
    return render_template("dashboard.html")
