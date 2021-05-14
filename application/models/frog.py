from sqlalchemy.sql import func
from sqlalchemy_utc import UtcDateTime, utcnow

from core import db


class Frog(db.Model):
    __tablename__ = 'frogs'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=False, nullable=False)
    food = db.Column(db.Integer, nullable=False, default=0)
    cleanliness = db.Column(db.Integer, nullable=False, default=0)
    money = db.Column(db.Integer, nullable=False, default=0)
    image_id = db.Column(db.Integer, db.ForeignKey('images.id'), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    last_request = db.Column(UtcDateTime(), default=utcnow(), nullable=False)
    
    image = db.relationship("Image", backref=db.backref("frog", uselist=False))
    
    def __repr__(self):
        return f'<Frog {self.id}; {self.name}>'