from basicauth import decode
from models import *
from werkzeug.exceptions import BadRequest, NotFound

def authorization(encoded_str):
    if encoded_str == None:
        raise BadRequest('Authorization failed')
    username, password = decode(encoded_str)
    user = User.query.filter_by(username=username).first()
    if user == None:
        raise NotFound('User not found')
    elif user.password == password:
        return user
    raise NotFound('Incorrect password')
