from flask import Flask, Blueprint, request
from flask_restful import Api
from resources.v1.AuthResource import AuthResource as AuthResourceV1
from resources.v1.PlaylistResource import PlaylistResource as PlaylistResourceV1
from resources.v1.PlaylistSongResource import PlaylistSongResource as PlaylistSongResourceV1
from resources.v1.AccountArtistResource import AccountArtistResource as AccountArtistResourceV1
from resources.v1.AccountPlaylistResource import AccountPlaylistResource as AccountPlaylistResourceV1
from resources.v1.AccountAccountSongResource import AccountAccountSongResource as AccountAccountSongResourceV1
from resources.v1.AccountSongStreamResource import AccountSongStreamResource as AccountSongStreamResourceV1
from resources.v1.SongResource import SongResource as SongResourceV1
from resources.v1.SongLikeResource import SongLikeResource as SongLikeResourceV1
from resources.v1.SongDislikeResource import SongDislikeResource as SongDislikeResourceV1
from resources.v1.SongSearchResource import SongSearchResource as SongSearchResourceV1
from resources.v1.SongArtistResource import SongArtistResource as SongArtistResourceV1
from resources.v1.AlbumResource import AlbumResource as AlbumResourceV1
from resources.v1.AlbumImageResource import AlbumImageResource as AlbumImageResourceV1
from resources.v1.AlbumArtistResource import AlbumArtistResource as AlbumArtistResourceV1
from resources.v1.AlbumSongResource import AlbumSongResource as AlbumSongResourceV1
from resources.v1.AlbumSearchResource import AlbumSearchResource as AlbumSearchResourceV1
from resources.v1.ArtistResource import ArtistResource as ArtistResourceV1
from resources.v1.ArtistSearchResource import ArtistSearchResource as ArtistSearchResourceV1
from resources.v1.ArtistAlbumResource import ArtistAlbumResource as ArtistAlbumResourceV1
from resources.v1.GenreResource import GenreResource as GenreResourceV1
from resources.v1.GenreSongResource import GenreSongResource as GenreSongResourceV1
from resources.v1.SongStreamResource import SongStreamResource as SongStreamResourceV1
from resources.v1.SubscriptionResource import SubscriptionResource as SubscriptionResourceV1

app = Flask(__name__)
api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Routes
api.add_resource(AuthResourceV1, "/v1/auth/<request_type>")
api.add_resource(AuthResourceV1, "/v1/auth/<request_type>/<method>", endpoint="authAlternatives")
api.add_resource(AccountArtistResourceV1, "/v1/account/<int:account_id>/artist")
api.add_resource(AccountPlaylistResourceV1, "/v1/account/<int:account_id>/playlists")
api.add_resource(AccountAccountSongResourceV1, "/v1/account/<int:account_id>/accountsongs", methods=["GET", "POST"], endpoint="accountsongs")
api.add_resource(AccountAccountSongResourceV1, "/v1/account/<int:account_id>/accountsong/<int:account_song_id>", methods=["GET", "DELETE"], endpoint="accountsong")
api.add_resource(AccountSongStreamResourceV1, "/v1/stream/accountsong/<int:account_song_id>")
api.add_resource(AlbumResourceV1, "/v1/album/<int:album_id>", methods=["GET"], endpoint="album")
api.add_resource(AlbumResourceV1, "/v1/album", methods=["POST"])
api.add_resource(AlbumArtistResourceV1, "/v1/album/<int:album_id>/artists")
api.add_resource(AlbumImageResourceV1, "/v1/album/<int:album_id>/image", methods=["GET"], endpoint="albumImage")
api.add_resource(AlbumImageResourceV1, "/v1/album/image", methods=["POST"])
api.add_resource(AlbumSearchResourceV1, "/v1/album/search/<name>")
api.add_resource(AlbumSongResourceV1, "/v1/album/<int:album_id>/songs", methods=["GET"], endpoint="albumSongs")
api.add_resource(AlbumSongResourceV1, "/v1/album/songs", methods=["POST"])
api.add_resource(ArtistAlbumResourceV1, "/v1/artist/<int:artist_id>/albums")
api.add_resource(ArtistResourceV1, "/v1/artists", "/v1/artist/<int:artist_id>")
api.add_resource(ArtistSearchResourceV1, "/v1/artist/search/<artistic_name>")
api.add_resource(GenreResourceV1, "/v1/genres", "/v1/genre/<int:genre_id>")
api.add_resource(GenreSongResourceV1, "/v1/genre/<int:genre_id>/songs")
api.add_resource(PlaylistResourceV1, "/v1/playlist", methods=["POST"])
api.add_resource(PlaylistResourceV1, "/v1/playlist/<int:playlist_id>", methods=["PUT", "DELETE"], endpoint="actionsPlaylist")
api.add_resource(PlaylistSongResourceV1, "/v1/playlist/<int:playlist_id>/songs", methods=["GET"], endpoint="songs")
api.add_resource(PlaylistSongResourceV1, "/v1/playlist/<int:playlist_id>/songs/<int:song_id>", methods=["GET", "DELETE"], endpoint="song")
api.add_resource(PlaylistSongResourceV1, "/v1/playlist/<int:playlist_id>/song", methods=["POST"])
api.add_resource(SongResourceV1, "/v1/song/<int:song_id>")
api.add_resource(SongArtistResourceV1, "/v1/song/<int:song_id>/artists")
api.add_resource(SongSearchResourceV1, "/v1/song/search/<title>")
api.add_resource(SongLikeResourceV1, "/v1/song/<int:song_id>/songlike")
api.add_resource(SongDislikeResourceV1, "/v1/song/<int:song_id>/songdislike")
api.add_resource(SongStreamResourceV1, "/v1/stream/song/<int:song_id>/<quality_type>")
api.add_resource(SubscriptionResourceV1, "/v1/subscription")
