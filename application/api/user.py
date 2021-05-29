from flask_restful import Resource, marshal, marshal_with, inputs, reqparse
from flask import current_app as app
from sqlalchemy import func

from models.user import User
from .json_fields import user_fields, user_list_fields
from .error import error_response
from controllers.user_actions import create_user


class UserResource(Resource):

    @marshal_with(user_fields)
    def get(self, id):
        user = User.query.get_or_404(id)
        return user


class UsersResource(Resource):

    @marshal_with(user_list_fields)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', location=['args'],
                            default='', trim=True, nullable=False)
        args = parser.parse_args()
        search = args['username']
        users = User.query.filter(User.username.ilike(f"{search}%")).union(
            User.query.filter(User.username.ilike(f"%{search}%"))
        ).all()
        return users

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
        app.logger.info(f"User created: {user}")
        return marshal(user, user_fields), 201
