from app import app
from app.auth import auth_mod

from app.shared.models import User

from flask import request, redirect, render_template, url_for
from flask_login import login_user, login_required, logout_user

from app.auth.controllers import authenticate_user

@auth_mod.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username and password:
            usr_id = authenticate_user(username, password)

            if usr_id or app.config['PRODUCTION']:
                login_user(User(usr_id))
                return redirect(url_for('index'))

        return render_template('auth/login.html', auth_error='Username, password combination is not correct.')

    return render_template('auth/login.html')

@auth_mod.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')