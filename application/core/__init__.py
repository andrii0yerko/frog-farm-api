from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_sockets import Sockets

import os
from datetime import timedelta

from .gan import GANGenerator

jwt = JWTManager()
db = SQLAlchemy()
model = GANGenerator()
sockets = Sockets()


def create_app():
    """Construct the core application."""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DB_URL']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.environ['JWT_SECRET_KEY']
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

    db.init_app(app)
    jwt.init_app(app)
    sockets.init_app(app)

    with app.app_context():
        from models import Image, User, Frog
        from controllers.event import on_frog_load
        db.create_all()

        import api.jwt
        from api import bp as api_bp
        app.register_blueprint(api_bp, url_prefix='/api/v1')

        from websockets import ws
        sockets.register_blueprint(ws, url_prefix=r'/api/v1')

        from .shell import make_shell_context
        app.shell_context_processor(make_shell_context)
        return app
