from flask_restful import fields
from flask import url_for

class ImageLink(fields.Raw):
    def format(self, value):
        return url_for('api.imageresource', id=value) 

frog_fields = {
    'id': fields.Integer,
    'url': fields.String(attribute=lambda x: url_for('api.frogresource', id=x.id) ),
    'name': fields.String,
    'food': fields.Integer,
    'money': fields.Integer,
    'cleanliness': fields.Integer,
    'image': fields.String(attribute=lambda x: url_for('api.imageresource', id=x.image_id) ),
}

user_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'frogs': fields.String(attribute=lambda x: url_for('api.userfrogsresource', id=x['id']) ),
}

signed_user_fields = dict(**user_fields, money=fields.Integer)