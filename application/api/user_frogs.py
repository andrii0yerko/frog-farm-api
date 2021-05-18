from flask import jsonify, send_file, request, Response, url_for, g
from flask_restful import Resource, fields, marshal_with, marshal

from core import db
from models.user import User
from controllers.buy_a_frog import buy_a_frog
from . import auth
from .json_fields import frog_fields, user_fields, signed_user_fields
from .error_handlers import error_response


class UserFrogsResource(Resource):
    
    def get(self, id):
        user = User.query.get_or_404(id)
        frogs = [marshal(frog, frog_fields) for frog in user.frogs]
        return jsonify(frogs)
    
    @auth.login_required
    def post(self, id):
        user = User.query.get_or_404(id)
        if auth.current_user().id != user.id:
            return error_response(403, 'Not your account!')
        frog = buy_a_frog(user)
        if not frog:
            return error_response(400, 'Not enough money')
        return marshal(frog, frog_fields), 201