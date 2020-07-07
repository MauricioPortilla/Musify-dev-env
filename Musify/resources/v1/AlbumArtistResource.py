from flask_restful import Resource
from Model import database, Artist, ArtistSchema, AlbumArtist, AlbumArtistSchema
from flask import request
from .AuthResource import auth_token
from .lang.lang import get_request_message
import json

artists_schema = ArtistSchema(many=True)
artist_schema = ArtistSchema()

class AlbumArtistResource(Resource):
    @auth_token
    def get(self, account, album_id):
        album_artists = AlbumArtist.query.filter_by(album_id=album_id)
        artists = []
        for artist in album_artists:
            artists.append(Artist.query.filter_by(artist_id=artist.artist_id).first())
        if len(artists) == 0:
            return { "status": "failed", "data": get_request_message(request, "NON_EXISTENT_ALBUM") }, 422
        return { "status": "success", "data": artists_schema.dump(artists).data }, 200
