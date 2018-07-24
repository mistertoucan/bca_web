from app.auth import auth_mod

from flask import redirect, render_template, url_for, request, g, make_response
from werkzeug.urls import url_parse

from app.auth.controllers import authenticate_user
from app.shared.controllers import requires_token

@auth_mod.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username and password:
            token = authenticate_user(username, password, request.remote_addr)

            if token:
                next_page = request.args.get('next')
                if not next_page or url_parse(next_page).netloc != '':
                    next_page = url_for('index')

                response = make_response(redirect(next_page))
                response.set_cookie('bca_token', token)
                return response

        return render_template('auth/login.html', auth_error='Username, password combination is not correct.')

    return render_template('auth/login.html')

@auth_mod.route('/logout')
@requires_token
def logout():
    g.user = None
    g.token = None

    response = make_response(redirect('/'))
    response.delete_cookie('bca_token')

    return response