# bca_web
My rewrite of the BCA web framework in Python Flask \
`*Please use a Python 2.7 virtual environment to avoid version issues`

## Setup
1. `cd bca_web` - Navigate to the folder
2. MAC OSX - `brew install mysql` \
   Windows - `https://dev.mysql.com/downloads/windows/installer/8.0.html`
             `https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysql-python`
3. `pip install -r requirements.txt` or `python setup.py install` OR `CLICK install dependencies if using PyCharm`
4. MAC OSX - `export FLASK_APP=bca_web.py` \
   Windows - `set FLASK_APP=bca_web.py`
5. `flask run`

### Debug Mode
Debug mode makes testing a lot easier and displays errors.\
**Always make sure to keep deubg mode ON during Development and OFF during Production** \
`export FLASK_DEBUG=True`

## Auth
1. After successful email/password verification a JWT token is created for the current user and saved
under the "bca_token" cookie. 
2. The token has the following payload:
    `bca_token: { usr_id: Int, ip_address: Str, last_used: Int (Seconds), timeout_duration: Int (Seconds)}`
  
3. Upon every request, the cookie is verified, checked for timeout, and updated. 
4. The current user and their corresponding JWT token can always be accessed with the request context variable, g, under the attributes user and token respectively. 
