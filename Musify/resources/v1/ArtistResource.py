from flask_restful import Resource
from Model import database, Artist, ArtistSchema, AlbumArtist, AlbumArtistSchema
from flask import request
from resources.v1.AuthResource import auth_token
import json

artists_schema = ArtistSchema(many=True)
artist_schema = ArtistSchema()

class ArtistResource(Resource):
    @auth_token
    def get(self, account, artist_id):
        artist = Artist.query.filter_by(artist_id=artist_id).first()
        return { "status": "success", "data": artist_schema.dump(artist).data }, 200
