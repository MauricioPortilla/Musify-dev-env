import os

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_ECHO = True
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = "postgresql://musify_user:Musify_0903@172.250.6.4/musify"
SECRET_KEY = "QkyuId1fWmdrTOXI8SV7ExanvTMHGbXiNIngBmrP"
