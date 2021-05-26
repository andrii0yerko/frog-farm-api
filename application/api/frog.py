from flask_restful import Resource, marshal_with, reqparse, marshal
from flask_jwt_extended import jwt_required, current_user

import random

from models.frog import Frog
from controllers.frog_actions import wash_frog, feed_frog, collect_money, upgrade_frog
from .json_fields import frog_fields
from .error import error_response


class FrogResource(Resource):

    @marshal_with(frog_fields)
    def get(self, id):
        frog = Frog.query.get_or_404(id)
        return frog

    @jwt_required()
    def put(self, id):
        frog = Frog.query.get_or_404(id)

        if current_user.id != frog.owner_id:
            return error_response(403, 'Not your frog!')

        parser = reqparse.RequestParser()
        parser.add_argument(
            'action', choices=['wash', 'feed', 'collect', 'upgrade'],
            help="{error_msg}. Allowed actions are 'wash', 'feed', 'collect' and 'upgrade'",
            required=True, trim=True, nullable=False
            )
        args = parser.parse_args()
        action = args['action']
        if action == 'wash':
            frog = wash_frog(frog)
        elif action == 'feed':
            frog = feed_frog(frog)
        elif action == 'collect':
            frog = collect_money(frog)
        elif action == 'upgrade':
            frog = upgrade_frog(frog)
            if not frog:
                return error_response(400, 'Not enough money')
        return marshal(frog, frog_fields)

    def delete(self, id):
        msg = random.choice(['Нельзя просто так избавится от жабы!',
                             'Жабья кара настигнет тебя.',
                             'Болото проклянет тебя!', 'Даже не вздумай',
                             'Лягушачий нейрокороль уже уведомлен о твоих действиях.'])
        return error_response(405, msg)
