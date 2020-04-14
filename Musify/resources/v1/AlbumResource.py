from flask_restful import Resource
from Model import database, Album, AlbumSchema, AlbumArtist, AlbumArtistSchema
from flask import request
import json

albums_schema = AlbumSchema(many=True)
album_schema = AlbumSchema()

class AlbumResource(Resource):
    def get(self, album_id=None):
        if not (album_id is None):
            album = Album.query.filter_by(album_id=album_id).first()
            return { "status": "success", "data": album_schema.dump(album).data }, 200
        return { "status": "failed", 'message': 'No input data provided' }, 400
