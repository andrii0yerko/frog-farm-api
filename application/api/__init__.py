from flask import Blueprint
from flask_restful import Api
from flask_cors import CORS

from .image import ImageResource, RandomImageResource
from .frog import FrogResource
from .user import UserResource, UsersResource
from .auth import AuthEndpoint
from .user_frogs import UserFrogsResource

bp = Blueprint('api', __name__)
cors = CORS(bp, supports_credentials=True)
api = Api(bp)

from .error_handlers import *
api.add_resource(ImageResource, '/images/<int:id>')
api.add_resource(RandomImageResource, '/random_image')
api.add_resource(FrogResource, '/frogs/<int:id>')
api.add_resource(UserFrogsResource, '/users/<int:id>/frogs')
api.add_resource(UserResource, '/users/<int:id>')
api.add_resource(UsersResource, '/users')
api.add_resource(AuthEndpoint, '/auth')
