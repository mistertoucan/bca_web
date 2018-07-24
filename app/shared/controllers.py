from app import app
from app.auth.controllers import decode_token, create_token, validate_token, get_user

from flask import request, redirect, url_for, g, make_response
from functools import wraps

def requires_token(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not hasattr(g, "token") and not request.cookies.get('bca_token'):
            if app.config['DEBUG']:
                return redirect(url_for('dashboard.test', next=request.url))
            return redirect(url_for('auth.login', next=request.url))

        token = request.cookies['bca_token'] or g.token

        decoded = decode_token(token)

        if validate_token(decoded, request.remote_addr, decoded=True):

            g.user = get_user(int(decoded['usr_id'].encode('utf-8')))

            token = create_token(decoded['usr_id'].encode('utf-8'), decoded['ip_address'].encode('utf-8'))
        else:
            token = None

        # g.token is the same as the cookie
        g.token = token

        # invalid tokens are None
        # actual cookies set after every response
        if not g.token:
            # logs out user
            if hasattr(g, 'user'):
                g.user = None

            response = make_response(redirect(url_for('auth.login', next=request.url)))
            response.delete_cookie('bca_token')

            return response

        return f(*args, **kwargs)

    return decorated_function

@app.after_request
def after_request(response):
    if hasattr(g, 'token') and g.token:
        response.set_cookie('bca_token', g.token, domain=app.config['TOKEN_DOMAIN'])

    return response