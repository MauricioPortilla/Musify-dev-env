import os

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_ECHO = True
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = "postgresql://musify_user:Musify_0903@172.250.6.4/musify"
SECRET_KEY = "QkyuId1fWmdrTOXI8SV7ExanvTMHGbXiNIngBmrP"

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
ALBUM_IMAGES_DIRECTORY = "./storage/albumImages"
SONGS_DIRECTORY = "./storage/songs"
ACCOUNT_SONGS_DIRECTORY = "./storage/accountsongs"
ALLOWED_FILE_SONG_EXTENSIONS = ["mp3", "wav"]
ALLOWED_FILE_IMAGE_EXTENSIONS = ["png"]
MUSIFY_GRPC_SERVER_ADDRESS = '172.250.6.3:8888'
SUBSCRIPTION_COST = 100
