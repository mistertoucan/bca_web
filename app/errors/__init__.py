from app import app
from flask import redirect

@app.errorhandler(404)
def unknown(e):
    return redirect('/')