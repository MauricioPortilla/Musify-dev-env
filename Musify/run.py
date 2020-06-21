from flask import Flask
from config import ALBUM_IMAGES_DIRECTORY, SONGS_DIRECTORY, ACCOUNT_SONGS_DIRECTORY
import os

def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)
    
    from app import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    from Model import database
    database.init_app(app)

    if (not os.path.exists(ALBUM_IMAGES_DIRECTORY)):
        os.makedirs(ALBUM_IMAGES_DIRECTORY)

    if (not os.path.exists(SONGS_DIRECTORY)):
        os.makedirs(SONGS_DIRECTORY)

    if (not os.path.exists(ACCOUNT_SONGS_DIRECTORY)):
        os.makedirs(ACCOUNT_SONGS_DIRECTORY)

    return app


if __name__ == "__main__":
    app = create_app("config")
    app.run(host='0.0.0.0', debug=True)
