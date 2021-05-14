from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import os

from .gan import GANGenerator

db = SQLAlchemy()
model = GANGenerator()

def create_app():
    """Construct the core application."""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)

    with app.app_context():
        # from . import routes
        from models import Image, User, Frog
        from controllers.event import on_frog_load
        db.create_all()
        # u = User.query.get(1)
        # u.money = 1000
        # u = User('Admin', 'admin@admin.admin', '123321')
        # f = Frog(food=100,cleanliness=50, image_id=1, name="Здоровяк Грязнулькин")
        # u.frogs.append(f)
        # f = Frog(food=100, cleanliness=100, image_id=2, name="Большой Поедатель Бутонов")
        # u.frogs.append(f)
        # db.session.add(u)
        # db.session.commit()
        # u = User('User2', 'test@gmail.com', '111')
        # db.session.add(u)
        # f = Frog.query.get(1)
        # f.food = 255
        # f.cleanliness = 123
        # db.session.commit()
        from api import bp as api_bp
        app.register_blueprint(api_bp, url_prefix='/api/v1')
        
        return app