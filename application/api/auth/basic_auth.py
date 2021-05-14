from flask import g

from models import User
from . import auth

@auth.verify_password
def verify_password(username, password):
    if '@' in username:
        user = User.query.filter_by(email=username).first()
    else:
        user = User.query.filter_by(username=username).first()
        
    if user is None or not user.check_password(password):
        return None
    else:
        return user