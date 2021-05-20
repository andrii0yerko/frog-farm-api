from core import db
from constants import MAX_CLEANLINESS, MAX_FOOD, CLEANLINESS_DECREASE, FOOD_DECREASE


def wash_frog(frog):
    increase = max(MAX_CLEANLINESS - frog.cleanliness, 0)
    frog.cleanliness += increase
    frog.food = max(0, frog.food - 20 * FOOD_DECREASE * increase/MAX_FOOD)
    db.session.merge(frog)
    db.session.commit()
    return frog


def feed_frog(frog):
    increase = max(MAX_FOOD - frog.food, 0)
    frog.food += increase
    frog.cleanliness = max(0, frog.cleanliness - 20 * CLEANLINESS_DECREASE * increase/MAX_CLEANLINESS)
    db.session.merge(frog)
    db.session.commit()
    return frog


def collect_money(frog):
    frog.owner.money += frog.money
    frog.money = 0
    db.session.merge(frog)
    db.session.commit()
    return frog