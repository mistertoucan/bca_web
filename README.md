# bca_web
My rewrite of the BCA web framework in Python Flask

## Setup
1. `cd bca_web` - Navigate to the folder
2. `python setup.py install`
3. MAC OSX - `export FLASK_APP=bca_web.py` \
   Windows - `set FLASK_APP=bca_web.py`
4. `flask run`

## Auth
1. After successful email/password combination a JWT token is created for the current user and saved
under the "bca_token" cookie. 
2. The token has the following payload format:
    `bca_token: { usr_id: Int, ip_address: Str, last_used: Int (Seconds), timeout_duration: Int (Seconds)}` \
  
3. Upon every request, the cookie is verified, checked for timeout, and updated. 
4. The current user and their corresponding JWT token can always be accessed as with the global variable, g, with the attributes user and token respectively. 
