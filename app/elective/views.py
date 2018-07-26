from app.elective import elective_mod

from app.shared.controllers import requires_token

from flask import render_template, g

@elective_mod.route('/')
@requires_token
def index():
    return render_template('elective/index.html')