from models import *
from werkzeug.exceptions import NotFound
from flask import request


def authorization():
    auth = request.authorization
    username = auth.username
    password = auth.password
    user = User.query.filter_by(username=username).first()
    if user is None:
        raise NotFound('User not found')
    elif user.password != password:
        raise NotFound('Incorrect password')
    return user
