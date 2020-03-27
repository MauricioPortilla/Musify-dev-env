import os

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_ECHO = True
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = "postgresql://musify_user:Musify_0903@192.168.1.25/Musify"
