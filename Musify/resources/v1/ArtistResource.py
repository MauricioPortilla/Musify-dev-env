from flask_restful import Resource
from Model import database, Artist, ArtistSchema, AlbumArtist, AlbumArtistSchema
from flask import request
from .AuthResource import auth_token
from .lang.lang import get_request_message
import json

artists_schema = ArtistSchema(many=True)
artist_schema = ArtistSchema()

class ArtistResource(Resource):
    @auth_token
    def get(self, account, artist_id):
        artist = Artist.query.filter_by(artist_id=artist_id).first()
        if not artist:
            return { "status": "failure", "message": get_request_message(request, "NON_EXISTENT_ARTIST") }, 422
        return { "status": "success", "data": artist_schema.dump(artist).data }, 200
