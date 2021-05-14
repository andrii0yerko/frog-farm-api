from flask import jsonify, request, Response
from flask_restful import Resource, marshal_with, reqparse, marshal

from core import db
from models.frog import Frog
from . import auth
from .json_fields import frog_fields
from .error_handlers import error_response

from controllers.frog_actions import wash_frog, feed_frog, collect_money

class FrogResource(Resource):
    
    @marshal_with(frog_fields)
    def get(self, id):
        frog = Frog.query.get_or_404(id)
        return frog
    
    @auth.login_required
    def put(self, id):
        frog = Frog.query.get_or_404(id)
        
        if auth.current_user().id != frog.owner_id:
            return error_response(403, 'Not your frog!')
        
        parser = reqparse.RequestParser()
        parser.add_argument('action', choices=['wash', 'feed', 'collect'],
                            help="{error_msg}. Allowed actions are 'wash', 'feed' and 'collect",
                            required=True, trim=True, nullable=False)
        args = parser.parse_args()
        if args['action'] == 'wash':
            frog = wash_frog(frog)
        elif args['action'] == 'feed':
            frog = feed_frog(frog)
        elif args['action'] == 'collect':
            frog = collect_money(frog)
        return marshal(frog, frog_fields)

    def delete(self, id):
        return error_response(405, 'Нельзя просто так избавится от жабы!')