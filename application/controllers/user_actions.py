from core import db, model
from models import User, Frog, Image
from constants import FROG_PRICE
from .frog_names import random_frog_name


def create_user(username, email, password):
    user = User(username, email, password)
    db.session.add(user)
    db.session.commit()
    add_frog(user)
    change_money(user, FROG_PRICE)
    return user


def change_money(user, delta):
    user.money += delta
    db.session.merge(user)
    db.session.commit()
    return user


def add_frog(user):
    name = random_frog_name()
    frog = Frog(name=name, food=50, cleanliness=50)

    img = model.generate_image()
    filename = f'frog_{user.id}_{len(user.frogs)}.jpeg'
    frog.image = Image(file=img, filename=filename)

    user.frogs.append(frog)
    db.session.commit()
    return frog


def buy_frog(user):
    if user.money < FROG_PRICE:
        return None
    user = change_money(user, -FROG_PRICE)
    frog = add_frog(user)
    return frog
