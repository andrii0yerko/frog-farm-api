from flask import send_file
from flask_restful import Resource, abort, reqparse

from core import db, model
from models.image import Image

import io

class ImageResource(Resource):
    
    def get(self, id):
        pic = Image.query.get_or_404(id)
        return send_file(io.BytesIO(pic.file),
                        attachment_filename=pic.filename
                        )
        

class RandomImageResource(Resource):

    def get(self):
        img = model.generate_image()
        return send_file(io.BytesIO(img),
                        attachment_filename="random_frog.jpeg"
                        )