from flask import Flask
import os

songsDirectory = "./storage/songs"
albumImagesDirectory = "./storage/albumImages"
accountSongsDirectory = "./storage/accountsongs"
ALLOWED_FILE_SONG_EXTENSIONS = ["mp3", "wav"]
MUSIFY_GRPC_SERVER_ADDRESS = '192.168.1.67:8888'

def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)
    
    from app import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    from Model import database
    database.init_app(app)

    if (not os.path.exists(albumImagesDirectory)):
        os.makedirs(albumImagesDirectory)

    if (not os.path.exists(accountSongsDirectory)):
        os.makedirs(accountSongsDirectory)

    return app


if __name__ == "__main__":
    app = create_app("config")
    app.run(host='0.0.0.0', debug=True)
