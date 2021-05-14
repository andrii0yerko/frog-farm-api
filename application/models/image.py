from core import db

# TODO: store images in better way, not in DB
class Image(db.Model):
    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(128), unique=True)
    file = db.Column(db.LargeBinary, nullable=False)

    def __repr__(self):
        return f'<Image {self.id}>'