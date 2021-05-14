from core import db, model
from models import Frog, User, Image
from constants import FROG_PRICE
from .frog_creation import random_frog_name

def buy_a_frog(user, free=False):
    if not free:
        if user.money < FROG_PRICE:
            return None
        user.money = user.money - FROG_PRICE
    
    name = random_frog_name()
    frog = Frog(name=name, food=50, cleanliness=50)
    
    img = model.generate_image()
    filename = f'frog_{user.id}_{len(user.frogs)}.jpeg'
    frog.image = Image(file=img, filename=filename)
    
    user.frogs.append(frog)
    db.session.commit()
    return frog