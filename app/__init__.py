from flask import Flask
from flask_mysqldb import MySQL

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
mysql = MySQL(app)

@app.route('/')
def index():
    return "Hello World!"
