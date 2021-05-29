from models import Image as MImage
from PIL import Image
import io


from core import db, create_app
app = create_app()

with app.app_context():
    for i in MImage.query.all():
        img = Image.open(io.BytesIO(i.file))
        if img.size != (128, 128):
            continue
        image = img
        padding = 16
        width, height = image.size
        new_width = width + 2*padding
        new_height = height + 2*padding
        result = Image.new(image.mode, (new_width, new_height), (255, 255, 255))
        result.paste(image, (padding, padding))
        image = result
        with io.BytesIO() as f:
            image.save(f, format="JPEG")
            bytearr = f.getvalue()
        i.file = bytearr
    db.session.commit()