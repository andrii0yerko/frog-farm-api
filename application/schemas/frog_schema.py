from marshmallow import Schema, fields
from flask import url_for


class FrogSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    level = fields.Integer()
    food = fields.Integer()
    money = fields.Integer()
    cleanliness = fields.Integer()
    image = fields.Method("image_url")
    
    def image_url(self, x):
        return url_for('api.imageresource', id=x.id if hasattr(x, 'image_id') else x['image_id'])