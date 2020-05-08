from flask_restful import Resource
from Model import database, Album, AlbumSchema, AlbumArtist, AlbumArtistSchema
from flask import request
from resources.v1.AuthResource import auth_token
import json

albums_schema = AlbumSchema(many=True)
album_schema = AlbumSchema()

class AlbumResource(Resource):
    @auth_token
    def get(self, account, album_id):
        album = Album.query.filter_by(album_id=album_id).first()
        if not album:
            return { "status": "failed", "message": "This album does not exist." }, 422
        return { "status": "success", "data": album_schema.dump(album).data }, 200
