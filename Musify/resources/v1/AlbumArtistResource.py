from flask_restful import Resource
from Model import database, Artist, ArtistSchema, AlbumArtist, AlbumArtistSchema
from flask import request
from resources.v1.AuthResource import auth_token
import json

artists_schema = ArtistSchema(many=True)
artist_schema = ArtistSchema()

class AlbumArtistResource(Resource):
    @auth_token
    def get(self, account, album_id):
        albumArtists = AlbumArtist.query.filter_by(album_id=album_id)
        artists = []
        for artist in albumArtists:
            artists.append(Artist.query.filter_by(artist_id=artist.artist_id).first())
        return { "status": "success", "data": artists_schema.dump(artists).data }, 200
