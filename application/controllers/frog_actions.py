from core import db
from constants import MAX_CLEANLINESS, MAX_FOOD, MAX_LEVEL, CLEANLINESS_DECREASE, FOOD_DECREASE, UPGRADE_PRICE
from .user_actions import change_money


def upgrade_frog(frog):
    if frog.level >= MAX_LEVEL:
        return frog
    if frog.owner.money < UPGRADE_PRICE:
        return None
    change_money(frog.owner, -UPGRADE_PRICE)
    frog.level = frog.level + 1
    db.session.merge(frog)
    db.session.commit()
    return frog


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