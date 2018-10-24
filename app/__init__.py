from flask import Flask, redirect, url_for
from flaskext.mysql import MySQL
from flask_breadcrumbs import Breadcrumbs

from config import Config

app = Flask(__name__, static_url_path='/static')
app.config.from_object(Config)

mysql = MySQL(app)
Breadcrumbs(app=app)

from app.auth import auth_mod
app.register_blueprint(auth_mod)

from app.dashboard import board_mod
app.register_blueprint(board_mod)

from app.elective import elective_mod
app.register_blueprint(elective_mod)

@app.route('/')
def index():
    return redirect(url_for('dashboard.index'))

import errors