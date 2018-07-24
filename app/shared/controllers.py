from app import app
from app.auth.controllers import check_token, get_user

from flask import request, redirect, url_for, g
from functools import wraps

def requires_token(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not 'bca_token' in request.cookies:
            return redirect(url_for('auth.login', next=request.url))

        token = request.cookies['bca_token']

        token = check_token(token, request.remote_addr)

        # g.token is the same as the cookie
        # set as global for simplicity
        # token itself set after every request
        g.token = token

        # invalid tokens are None
        # actual cookies set after every response
        if not g.token:
            # logs out user
            if hasattr(g, 'user'):
                g.user = None
            if hasattr(g, 'token'):
                g.token = None

            return redirect(url_for('auth.login', next=request.url))

        return f(*args, **kwargs)

    return decorated_function

# @app.after_request
# def update_token(response):
#     token = request.cookies.get('bca_token')
#
#     if token:
#         updated_token = check_token(request.cookies['bca_token'], request.remote_addr)
#
#         if updated_token:
#             response.set_cookie('bca_token', updated_token)
#         else:
#             response.delete_cookie('bca_token')

@app.after_request
def after_request(response):
    if hasattr(g, 'token') and g.token:
        response.set_cookie('bca_token', g.token)

    return response