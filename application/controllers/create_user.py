from core import db
from models import User
from controllers.buy_a_frog import buy_a_frog


def create_user(username, email, password):
    user = User(username, email, password)
    db.session.add(user)
    db.session.commit()
    buy_a_frog(user, free=True)
    return user
