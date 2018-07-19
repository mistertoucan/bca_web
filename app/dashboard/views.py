from app.dashboard import board_mod
from app.dashboard.controllers import *

from config import Config

from flask import render_template, redirect, request, url_for
from flask_breadcrumbs import register_breadcrumb
from flask_login import login_required, login_user, current_user

from app.shared.models import User

@board_mod.route('/')
@register_breadcrumb(board_mod, '.', 'Dashboard')
@login_required
def index():
    return render_template("dashboard/dashboard.html")

@board_mod.route('/about')
@register_breadcrumb(board_mod, '.about', 'About')
@login_required
def about():
    return render_template("dashboard/about.html")

@board_mod.route('/test', methods=['GET', 'POST'])
def test():
    if Config.DEBUG:
        if not current_user.is_authenticated:
            if request.method == 'POST':
                print(request.form)

                usr_id_tch = request.form["usr_id_tch"]
                usr_id_adm = request.form["usr_id_adm"]
                usr_id_std = request.form["usr_id_std"]

                choice = request.form["choice"]

                if choice == 'Login ADM':
                    login_user(User.get(usr_id_adm))
                elif choice == 'Login TCH':
                    login_user(User.get(usr_id_tch))
                elif choice =='Login STD':
                    login_user(User.get(usr_id_std))
                else:
                    return redirect("dashboard/test.html", code=400)

            else:
                admins = get_admins()
                teachers = get_teachers()
                students = get_students()
                return render_template("dashboard/test.html", admins=admins, teachers=teachers, students=students)
    return redirect(url_for("dashboard.index"))