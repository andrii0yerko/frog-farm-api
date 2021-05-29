from flask import Blueprint
from flask import current_app as app

from constants import FROG_PRICE
from .ws_endpoint import WSEndpoint
from .gameplay import Gameplay
import json

ws = Blueprint(r'ws', __name__)

# clients = []

# def stock_broadcast():
#     for client in clients:
#         if client.closed:
#             clients.remove(client)
#             continue
#         client.send(str(FROG_PRICE))


# @ws.route('/stock')
# def stock_socket(socket):
#     if socket not in clients:
#         clients.append(socket)
#     while not socket.closed:
#         message = socket.receive()
#         socket.send(f'Все говорят "{message}", а ты возьми и купи нейрожэбу')
#     #     broadcast(message)



# class Chat(WSEndpoint):

#     clients = []

#     def on_connect(self, client):
#         self.clients.append(client)

#     def on_disconnect(self, client):
#         app.logger.info(self.clients)
#         self.clients.remove(client)

#     def on_message(self, client, message):
#         # jmessage = json.loads(message)
#         app.logger.info(message)
#         for i in self.clients:
#             if client == i:
#                 continue
#             i.send(message)


# Chat(ws, '/chat')
Gameplay(ws, '/gameplay')
