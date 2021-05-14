from flask import Blueprint
from flask_restful import Api

from .auth import auth

bp = Blueprint('api', __name__)
api = Api(bp)

# from server.api import endpoints, errors, auth
from .image import ImageResource, RandomImageResource
from .frog import FrogResource
from .user import UserResource, UsersResource
from .user_frogs import UserFrogsResource

api.add_resource(ImageResource, '/images/<int:id>')
api.add_resource(RandomImageResource, '/random_image')
api.add_resource(FrogResource, '/frogs/<int:id>')

api.add_resource(UserFrogsResource, '/users/<int:id>/frogs')
api.add_resource(UserResource, '/users/<int:id>')
api.add_resource(UsersResource, '/users')
# api.add_resource(UserFrogResource, '/users/<int:id>/frogs')