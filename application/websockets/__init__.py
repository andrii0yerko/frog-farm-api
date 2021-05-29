from flask import Blueprint
from flask import current_app as app

from constants import FROG_PRICE
from .ws_endpoint import WSEndpoint
from .gameplay import Gameplay
import json

ws = Blueprint(r'ws', __name__)

Gameplay(ws, '/gameplay')
