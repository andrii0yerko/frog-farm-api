from flask_restful import Resource, marshal, inputs, reqparse
from flask_jwt_extended import jwt_required, current_user
from sqlalchemy import func

from models.user import User
from .json_fields import user_fields, signed_user_fields
from .error import error_response
from controllers.user_actions import create_user


class UserResource(Resource):

    @jwt_required(optional=True)
    def get(self, id):
        user = User.query.get_or_404(id)
        if current_user and current_user.id == user.id:
            return marshal(user, signed_user_fields)
        return marshal(user, user_fields)


class UsersResource(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True, trim=True, nullable=False)
        parser.add_argument('email', type=inputs.regex(r'^[^\s@]+@[^\s@]+\.[^\s@]+$'),
                            help='Enter a correct email',
                            trim=True, required=True, nullable=False)
        parser.add_argument('password', type=inputs.regex(r"^(?=.*[A-Za-z])(?=.*\d).{8,}$"),
                            help='Your password must include minimum eight characters, at least one letter and one number',
                            required=True, nullable=False)
        args = parser.parse_args()
        if User.query.filter(func.lower(User.username) == func.lower(args["username"])).first():
            return error_response(400, "User with the same username already exists")
        if User.query.filter(func.lower(User.email) == func.lower(args["email"])).first():
            return error_response(400, "User with the same email already exists")
        user = create_user(**args)
        return marshal(user, user_fields), 201
