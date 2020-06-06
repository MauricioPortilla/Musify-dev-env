import os

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_ECHO = True
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = "postgresql://musify_user:Musify_0903@172.18.0.3/musify"
SECRET_KEY = "QkyuId1fWmdrTOXI8SV7ExanvTMHGbXiNIngBmrP"
