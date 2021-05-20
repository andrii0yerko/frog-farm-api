from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import os

from .gan import GANGenerator

db = SQLAlchemy()
model = GANGenerator()


def create_app():
    """Construct the core application."""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DB_URL']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        from models import Image, User, Frog
        from controllers.event import on_frog_load
        db.create_all()

        from api import bp as api_bp
        app.register_blueprint(api_bp, url_prefix='/api/v1')

        return app
