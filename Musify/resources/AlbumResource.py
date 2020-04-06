from flask_restful import Resource
from Model import database, Album, AlbumSchema, AlbumArtist, AlbumArtistSchema
from flask import request
import json

albums_schema = AlbumSchema(many=True)
album_schema = AlbumSchema()
albumArtists_schema = AlbumArtistSchema(many=True)
albumArtist_schema = AlbumArtistSchema()

class AlbumResource(Resource):
    def get(self):
        data = json.loads(request.args.to_dict()["data"])
        if not data:
            return { "status": "failed", 'message': 'No input data provided' }, 400
        if (data["request_type"] == "albumById"):
            album = Album.query.filter_by(album_id=data["album_id"]).first()
            return { "status": "success", "data": album_schema.dump(album).data }, 200
