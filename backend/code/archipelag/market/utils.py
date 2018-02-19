from imghdr import what
from uuid import uuid4
from os import path

def unique_filename(images_path):
    def filename_generator(image, _):
        filetype = what(None, image.content)
        filename = "{}.{}".format(uuid4(), filetype)
        return path.join(images_path, filename)
    return filename_generator