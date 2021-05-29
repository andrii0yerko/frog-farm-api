from flask_restful import fields
from flask import url_for

frog_fields = {
    'id': fields.Integer,
    'url': fields.String(
        attribute=lambda x: url_for('api.frogresource', id=x.id if hasattr(x, 'id') else x['id'])
        ),
    'name': fields.String,
    'level': fields.Integer,
    'food': fields.Integer,
    'money': fields.Integer,
    'cleanliness': fields.Integer,
    'image': fields.String(
        attribute=lambda x: url_for('api.imageresource', id=x.id if hasattr(x, 'image_id') else x['image_id'])
        ),
}

user_list_fields = {
    'username': fields.String,
    'id': fields.Integer,
    'url': fields.String(
        attribute=lambda x: url_for('api.userresource', id=x.id)
    ),
}

user_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'frogs': fields.String(
        attribute=lambda x: url_for('api.userfrogsresource', id=x.id if hasattr(x, 'id') else x['id'])
        ),
    'money': fields.Integer,
    'total_food_spent': fields.Integer,
    'total_water_spent': fields.Integer,
    'total_money_collected': fields.Integer
}
