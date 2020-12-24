import os
import secrets
from PIL import Image
from flask import url_for
from flask import current_app

# Func that saving posts pictures
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/posts_pics', picture_fn)

    output_size = (400, 400)
    i = Image.open(form_picture)
    i = i.resize((800, 800), Image.ANTIALIAS)
    i.save(picture_path)

    return picture_fn