from flask import send_file
from flask_restful import Resource

import io

from core import model
from models.image import Image


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
