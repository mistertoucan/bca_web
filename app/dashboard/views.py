from app.dashboard import board_mod

from flask import render_template
from flask_breadcrumbs import register_breadcrumb
from flask_login import login_required

@board_mod.route('/')
@register_breadcrumb(board_mod, '.', 'Dashboard')
@login_required
def index():
    return render_template("dashboard/dashboard.html")

@board_mod.route('/about')
@register_breadcrumb(board_mod, '.', 'About')
@login_required
def about():
    return render_template("dashboard/about.html")