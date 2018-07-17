from flask import Flask
from flask_mysqldb import MySQL
from flask_login import LoginManager

from config import Config

app = Flask(__name__, static_url_path='/static')
app.config.from_object(Config)

mysql = MySQL(app)
login_manager = LoginManager(app)
login_manager.login_view = "auth.login"

from app.auth import auth_mod
app.register_blueprint(auth_mod)

@app.route('/')
def index():
    return "Hello World!"
