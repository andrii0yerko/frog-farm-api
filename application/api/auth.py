from flask_restful import Resource, marshal_with, reqparse
from flask import jsonify
from flask import current_app as app

from models.user import User
from .json_fields import user_fields
from .error import error_response

from flask_jwt_extended import create_access_token
from flask_jwt_extended import current_user
from flask_jwt_extended import jwt_required


class AuthEndpoint(Resource):

    @jwt_required()
    @marshal_with(user_fields)
    def get(self):
        return current_user

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True, trim=True, nullable=False)
        parser.add_argument('password', required=True, nullable=False)
        args = parser.parse_args()
        username = args['username']
        password = args['password']
        if '@' in username:
            user = User.query.filter_by(email=username).first()
        else:
            user = User.query.filter_by(username=username).first()

        if user is None:
            return error_response(401, "Wrong username or email")
        if not user.check_password(password):
            return error_response(401, "Wrong password")

        access_token = create_access_token(identity=user)
        app.logger.info(f"{user} logged in")
        return jsonify(access_token=access_token)
