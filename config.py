import os

class Config(object):
    DB_URI = os.environ.get('DB_URI')