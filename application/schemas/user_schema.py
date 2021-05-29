from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Integer()
    username = fields.String()
    money = fields.Integer()
    cleanliness = fields.Integer()
    total_food_spent = fields.Integer()
    total_water_spent = fields.Integer()
    total_money_collected = fields.Integer()