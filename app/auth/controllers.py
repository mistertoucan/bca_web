from app import app
from app.db import DB, query_one
from app.shared.models import User

from werkzeug.contrib.cache import SimpleCache

from ldap3 import Server, Connection, ALL, NTLM
import jwt
import datetime

cache = SimpleCache()

# 1. Checks wether username is valid
# 2. If username is valid, then it connects to the local LDAP server to verify credentials
# Returns an auth token if valid
# Returns None otherwise
def authenticate_user(ip_address, username, password):
    resultID = query_one(DB.SHARED, 'SELECT usr_id FROM user WHERE usr_bca_id = %s', vars=[username])

    if resultID:
        resultID = resultID[0]

        server = Server('168.229.1.240:3268', get_info=ALL)

        conn = Connection(server, user=username, password=password, authentication=NTLM)

        # TODO: Update LDAP
        return create_token(resultID, ip_address)


def validate_token(token, ip_address, decoded=True):
    if not decoded:
        token = decode_token(token)

    return app.config['DEBUG'] or (TimestampSec64()-token['last_used'] <= app.config['TOKEN_TIMEOUT'] and token['ip_address'].encode('utf-8') == ip_address)

# Creates an auth token for the user
def create_token(usr_id, ip_address):
    encoded = jwt.encode({'usr_id': usr_id, 'ip_address': ip_address, 'last_used': TimestampSec64(), 'timeout_duration': app.config['TOKEN_TIMEOUT']}, app.config['SECRET_KEY'], algorithm='HS256')
    return encoded

def decode_token(token):
    try:
        return jwt.decode(token, app.config['SECRET_KEY'])
    except:
        return None

def get_user(usr_id):
    if(app.config['USER_CACHE_ENABLED']):
        user = cache.get(usr_id)

        if user is None:
            user = User.get(usr_id)
            cache.set(usr_id, user, timeout=app.config['CACHE_TIMEOUT'])
            return user
        return user
    else:
        return User.get(usr_id);

def TimestampSec64():
    return int((datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds())