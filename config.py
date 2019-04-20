import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'abc'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
