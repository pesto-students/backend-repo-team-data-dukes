import pathlib, mimetypes
from constants.constant import IMAGES

def get_extension(filename):
    c,_ = mimetypes.guess_type(filename)
    e = pathlib.Path(filename).suffixes
    return '.'.join([ext.strip('.') for ext in e]), c

def get_file_type(type):
    if type in IMAGES:
        return "image"
    return "document"

def get_username_domain(email):
    return email.split("@")