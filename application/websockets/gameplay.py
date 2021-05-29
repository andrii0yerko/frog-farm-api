from flask import current_app as app

from models import User, Frog
from schemas import FrogSchema, UserSchema
from controllers.frog_actions import wash_frog, feed_frog, collect_money, upgrade_frog
from .ws_endpoint import WSEndpoint

import json


class Client():
    def __init__(self, socket):
        self.socket = socket
        self.user = None
        self.listening_to = None

    @property
    def closed(self):
        return self.socket.closed

    def receive(self):
        return self.socket.receive()

    def send(self, message):
        return self.socket.send(message)

    @property
    def is_authorized(self):
        if self.user:
            return True
        return False

    def authorize(self, username, password):
        if self.is_authorized:
            return False, "Already authorized"
        if '@' in username:
            user = User.query.filter_by(email=username).first()
        else:
            user = User.query.filter_by(username=username).first()

        if user is None:
            return False, "Wrong username or email"
        if not user.check_password(password):
            return False, "Wrong password"
        self.user = user
        self.listening_to = user
        return True, "Logged in"


class Gameplay(WSEndpoint):

    ALLOWED_ACTIONS = ["authorization", "get", "interact"]
    REQUIRED_PARAMS = {  # used for the simple args parsing now. What about migrating to Marshmallow?
        "authorization": ["username", "password"],
        "interact": ["subaction", "id"]
    }
    clients = []

    def make_response(self, client, type, message):
        response = {
            'type': type,
            'message': message
        }
        response = json.dumps(response)
        client.send(response)

    def error_response(self, client, message):
        self.make_response(client, 'error', message)

    def info_response(self, client, message):
        self.make_response(client, 'info', message)

    def send_resource(self, client, content_type, content):
        response = {
            'type': 'content',
            'content_type': content_type,
            'payload': content
        }
        response = json.dumps(response)
        client.send(response)

    def on_connect(self, client):
        client = Client(client)
        self.clients.append(client)
        app.logger.debug(f"{client} connected")
        return client

    def on_disconnect(self, client):
        self.clients.remove(client)

    def on_message(self, client, message):
        try:
            message = json.loads(message)
        except TypeError:
            return self.error_response(client, "Your message is not JSON-serializable")
        app.logger.debug(f"{client} send {message}")
        action = message.pop('action', None)
        if not action:
            app.logger.debug(f"{client} Action field should be specified!")
            return self.error_response(client, "Action field should be specified!")
        if action not in self.ALLOWED_ACTIONS:
            return self.error_response(client, "Unknown action!")

        if action in self.REQUIRED_PARAMS:
            for param_name in self.REQUIRED_PARAMS[action]:
                if param_name not in message:
                    return self.error_response(client, f"{param_name} is missing!")

        if action == 'authorization':
            self.authorization(client, message)
        if action == 'get':
            self.get_resource(client, message)
        if action == 'interact':
            self.interact(client, message)

    def authorization(self, client, message):
        success, status = client.authorize(message['username'], message['password'])
        if not success:
            return self.error_response(client, status)
        return self.info_response(client, status)

    def interact(self, client, message):
        if not client.is_authorized:
            return self.error_response(client, "You should log in first")
        frog_id = message['id']
        frog = Frog.query.get(frog_id)
        if not frog:
            return self.error_response(client, "There is no frog with such id")
        if frog.owner.id != client.user.id:
            return self.error_response(client, "Not your frog")
        subaction = message['subaction']
        if subaction == 'wash':
            frog = wash_frog(frog)
        elif subaction == 'feed':
            frog = feed_frog(frog)
        elif subaction == 'collect':
            frog = collect_money(frog)
        elif subaction == 'upgrade':
            frog = upgrade_frog(frog)
            if not frog:
                return self.error_response(client, "Not enough money")
        return self.send_resource(client, "frog", FrogSchema().dump(frog))

    def get_resource(self, client, message):
        resource = message['resource']
        if resource == "frogs":
            if not client.listening_to:
                return self.error_response(client, "You should navigate to user profile first")
            else:
                frogs = [FrogSchema().dump(f) for f in client.listening_to.frogs]
                return self.send_resource(client, "user", frogs)
        elif resource == "frog":
            if "id" not in message:
                frog_id = message['id']
            frog = Frog.query.get(frog_id)
            return self.send_resource(client, "frog", FrogSchema().dump(frog))
        elif resource == "user":
            pass
        elif resource == "me":
            if not client.is_authorized:
                return self.error_response(client, "You should log in first")
            else:
                return self.send_resource(client, "user", UserSchema().dump(client.user))
        else:
            return self.error_response(client, "Unknown resource")
