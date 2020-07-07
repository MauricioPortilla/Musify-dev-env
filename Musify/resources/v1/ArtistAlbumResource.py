from flask_restful import Resource
from Model import database, Album, AlbumSchema, AlbumArtist, AlbumArtistSchema
from flask import request
from .AuthResource import auth_token
import json

albums_schema = AlbumSchema(many=True)
album_artists_schema = AlbumArtistSchema(many=True)
album_artist_schema = AlbumArtistSchema()

class ArtistAlbumResource(Resource):
    @auth_token
    def get(self, account, artist_id):
        album_artists = AlbumArtist.query.filter_by(artist_id=artist_id)
        albums = []
        for album in album_artists:
            albums.append(Album.query.filter_by(album_id=album.album_id).first())
        return { "status": "success", "data": albums_schema.dump(albums).data }, 200
