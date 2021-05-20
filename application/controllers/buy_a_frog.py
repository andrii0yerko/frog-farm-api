import random

from core import db, model
from models import Frog, Image
from constants import FROG_PRICE

frog_names = ['Большой', 'Гидратированный', 'Слизкий', 'Вонючий', 'Коренастый', 'Малютка',
              'Милашка', 'Здоровяк', 'Изысканный', 'Королевский', 'Амфибия', 'Круглый']

frog_surnames = ['Лягушка', 'Жаба', 'Вонючка', 'Яблоко', 'Мяч', 'Сфера', 'Мох',
                 'Грязнулькин', 'Грязь', 'Лист', 'Жабулька', 'Поганка', 'Милашка',
                 'Бахрома', 'Кусок', 'Удар', 'Истеричка', 'Герберт', 'Дождевая лягушка',
                 'Углевод', 'Парнишка', 'Головастик', 'Журнал', 'Поедатель бутонов',
                 'Убийца бутонов', 'Бутон', 'Горошек', 'Холодная закуска', 'Лимфатический узел',
                 'Лягух', 'Томатик']


def random_frog_name():
    return random.choice(frog_names) + ' ' + random.choice(frog_surnames)


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
