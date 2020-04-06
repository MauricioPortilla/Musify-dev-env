from flask import Flask
from flask import Blueprint
from flask_restful import Api
from flask import request
from resources.AccountResource import AccountResource
from resources.PlaylistResource import PlaylistResource
from resources.SongResource import SongResource
from resources.AlbumResource import AlbumResource
from resources.ArtistResource import ArtistResource
from resources.GenreResource import GenreResource

app = Flask(__name__)
api_bp = Blueprint('api', __name__)
api = Api(api_bp)

@app.route('/')
def home():
	return 'Welcome to Musify!'

@app.route('/AccTest')
def test():
	return request.json

# Routes
api.add_resource(AccountResource, "/Account")
api.add_resource(PlaylistResource, "/Playlist")
api.add_resource(SongResource, "/Song")
api.add_resource(AlbumResource, "/Album")
api.add_resource(ArtistResource, "/Artist")
api.add_resource(GenreResource, "/Genre")
