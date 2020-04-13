from flask_restful import Resource
from Model import database, Artist, ArtistSchema, AlbumArtist, AlbumArtistSchema
from flask import request
import json

artists_schema = ArtistSchema(many=True)
artist_schema = ArtistSchema()

class ArtistResource(Resource):
    def get(self, artist_id):
        # data = json.loads(request.args.to_dict()["data"])
        # if not data:
        #     return { "status": "failed", 'message': 'No input data provided' }, 400
        # if (data["request_type"] == "artistById"):
        artist = Artist.query.filter_by(artist_id=artist_id).first()
        return { "status": "success", "data": artist_schema.dump(artist).data }, 200
