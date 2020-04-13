from flask import Flask
from flask import Blueprint
from flask_restful import Api
from flask import request
from resources.v1.AccountResource import AccountResource as AccountResourceV1
from resources.v1.PlaylistResource import PlaylistResource as PlaylistResourceV1
from resources.v1.SongResource import SongResource as SongResourceV1
from resources.v1.AlbumResource import AlbumResource as AlbumResourceV1
from resources.v1.ArtistResource import ArtistResource as ArtistResourceV1
from resources.v1.GenreResource import GenreResource as GenreResourceV1
from resources.v1.SongStreamResource import SongStreamResource as SongStreamResourceV1

app = Flask(__name__)
api_bp = Blueprint('api', __name__)
api = Api(api_bp)

@app.route('/')
def home():
	return 'Welcome to Musify!'

# Routes
api.add_resource(AccountResourceV1, "/v1/Account")
api.add_resource(PlaylistResourceV1, "/v1/Playlist")
api.add_resource(SongResourceV1, "/v1/Song")
api.add_resource(AlbumResourceV1, "/v1/Album")
api.add_resource(ArtistResourceV1, "/v1/Artist")
api.add_resource(GenreResourceV1, "/v1/Genre")
api.add_resource(SongStreamResourceV1, "/v1/SongStream")
