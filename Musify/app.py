from flask import Flask, Blueprint, request
from flask_restful import Api
from resources.v1.AuthResource import AuthResource as AuthResourceV1
from resources.v1.AccountResource import AccountResource as AccountResourceV1
from resources.v1.PlaylistResource import PlaylistResource as PlaylistResourceV1
from resources.v1.PlaylistSongResource import PlaylistSongResource as PlaylistSongResourceV1
from resources.v1.AccountPlaylistResource import AccountPlaylistResource as AccountPlaylistResourceV1
from resources.v1.AccountAccountSongResource import AccountAccountSongResource as AccountAccountSongResourceV1
from resources.v1.AccountSongStreamResource import AccountSongStreamResource as AccountSongStreamResourceV1
from resources.v1.SongResource import SongResource as SongResourceV1
from resources.v1.SongLikeResource import SongLikeResource as SongLikeResourceV1
from resources.v1.SongDislikeResource import SongDislikeResource as SongDislikeResourceV1
from resources.v1.SongSearchResource import SongSearchResource as SongSearchResourceV1
from resources.v1.AlbumResource import AlbumResource as AlbumResourceV1
from resources.v1.AlbumImageResource import AlbumImageResource as AlbumImageResourceV1
from resources.v1.AlbumArtistResource import AlbumArtistResource as AlbumArtistResourceV1
from resources.v1.AlbumSongResource import AlbumSongResource as AlbumSongResourceV1
from resources.v1.ArtistResource import ArtistResource as ArtistResourceV1
from resources.v1.ArtistAlbumResource import ArtistAlbumResource as ArtistAlbumResourceV1
from resources.v1.GenreResource import GenreResource as GenreResourceV1
from resources.v1.SongStreamResource import SongStreamResource as SongStreamResourceV1

app = Flask(__name__)
api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Routes
api.add_resource(AuthResourceV1, "/v1/auth/<request_type>")
api.add_resource(AuthResourceV1, "/v1/auth/<request_type>/<login_method>", endpoint="loginAlternatives")
api.add_resource(AccountResourceV1, "/v1/account")
api.add_resource(AccountPlaylistResourceV1, "/v1/account/<int:account_id>/playlists")
api.add_resource(AccountAccountSongResourceV1, "/v1/account/<int:account_id>/accountsongs", methods=["GET", "POST"], endpoint="accountsongs")
api.add_resource(AccountAccountSongResourceV1, "/v1/account/<int:account_id>/accountsong/<int:account_song_id>", methods=["DELETE"], endpoint="accountsong")
api.add_resource(AccountSongStreamResourceV1, "/v1/stream/accountsong/<int:account_song_id>")
api.add_resource(AlbumResourceV1, "/v1/albums", "/v1/album/<int:album_id>")
api.add_resource(AlbumArtistResourceV1, "/v1/album/<int:album_id>/artists")
api.add_resource(AlbumImageResourceV1, "/v1/album/<int:album_id>/image")
api.add_resource(AlbumSongResourceV1, "/v1/album/<int:album_id>/songs")
api.add_resource(ArtistResourceV1, "/v1/artists", "/v1/artist/<int:artist_id>")
api.add_resource(ArtistAlbumResourceV1, "/v1/artist/<int:artist_id>/albums")
api.add_resource(GenreResourceV1, "/v1/genre/<int:genre_id>")
api.add_resource(PlaylistResourceV1, "/v1/playlist")
api.add_resource(PlaylistSongResourceV1, "/v1/playlist/<int:playlist_id>/songs", methods=["GET"], endpoint="songs")
api.add_resource(PlaylistSongResourceV1, "/v1/playlist/<int:playlist_id>/songs/<int:song_id>", methods=["GET"], endpoint="song")
api.add_resource(PlaylistSongResourceV1, "/v1/playlist/<int:playlist_id>/song", methods=["POST"])
api.add_resource(SongResourceV1, "/v1/song/<int:song_id>")
api.add_resource(SongSearchResourceV1, "/v1/song/search/<title>")
api.add_resource(SongLikeResourceV1, "/v1/song/<int:song_id>/songlike")
api.add_resource(SongDislikeResourceV1, "/v1/song/<int:song_id>/songdislike")
api.add_resource(SongStreamResourceV1, "/v1/stream/song/<int:song_id>/<quality_type>")
