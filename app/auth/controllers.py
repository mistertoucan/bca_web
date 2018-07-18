from app.db import DB, query_one

import ldap

# 1. Checks wether username is valid
# 2. If username is valid, then it connects to the local LDAP server to verify credentials
# Will return False for any failures/invalid credentials
def authenticate_user(username, password):
    resultID = query_one(DB.SHARED, 'SELECT usr_id FROM user WHERE usr_bca_id = %s', vars=[username])[0]

    if resultID:
        conn = ldap.initialize('ldap://168.229.1.240:3268')
        conn.protocol_version = 3
        conn.set_option(ldap.OPT_REFERRALS, 0)
        try:
            conn.simple_bind_s(username, password)
        except StandardError:
            print(StandardError)
            return None
        finally:
            return resultID

    return None