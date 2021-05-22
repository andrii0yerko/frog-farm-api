from flask import jsonify
from flask_restful import Resource, marshal
from flask_jwt_extended import jwt_required, current_user

from models.user import User
from controllers.buy_a_frog import buy_a_frog
from .json_fields import frog_fields
from .error import error_response


class UserFrogsResource(Resource):

    def get(self, id):
        user = User.query.get_or_404(id)
        frogs = [marshal(frog, frog_fields) for frog in user.frogs]
        frogs.sort(key=lambda frog: frog['id'])
        return jsonify(frogs)

    @jwt_required()
    def post(self, id):
        user = User.query.get_or_404(id)
        if current_user.id != user.id:
            return error_response(403, 'Not your account!')
        frog = buy_a_frog(user)
        if not frog:
            return error_response(400, 'Not enough money')
        return marshal(frog, frog_fields), 201
