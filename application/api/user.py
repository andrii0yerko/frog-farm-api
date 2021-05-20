from flask import jsonify, request, Response, url_for
from flask_restful import Resource, fields, marshal_with, marshal, inputs, reqparse

import re

from core import db
from . import auth
from models.user import User
from .json_fields import frog_fields, user_fields, signed_user_fields
from controllers.buy_a_frog import buy_a_frog


class AuthEndpoint(Resource):
    
    @auth.login_required
    @marshal_with(signed_user_fields)
    def get(self):
        return auth.current_user()


class UserResource(Resource):
    
    @auth.login_required(optional=True)
    def get(self, id):
        user = User.query.get_or_404(id)
        data = user.__dict__.copy()
        if auth.current_user() and auth.current_user().id == user.id:
            return marshal(data, signed_user_fields)
        return marshal(data, user_fields)
    
    
class UsersResource(Resource):

    @marshal_with(user_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True, trim=True, nullable=False)
        parser.add_argument('email', type=inputs.regex(r'^[^\s@]+@[^\s@]+\.[^\s@]+$'),
                            help='Enter a correct email',
                            trim=True, required=True, nullable=False)
        parser.add_argument('password', type=inputs.regex(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$"),
                            help='Your password must include minimum eight characters, at least one letter and one number',
                            required=True, nullable=False)
        args = parser.parse_args()
        user = User(**args)
        db.session.add(user)
        db.session.commit()
        buy_a_frog(user, free=True)
        return user, 201