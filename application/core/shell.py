from core import db
from models import User, Frog
from controllers.user_actions import create_user, add_frog, buy_frog, change_money


def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Frog': Frog,
        'create_user': create_user,
        'add_frog': add_frog,
        'buy_frog': buy_frog,
        'change_money': change_money
        }
