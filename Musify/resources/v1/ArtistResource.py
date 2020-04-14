from flask_restful import Resource
from Model import database, Artist, ArtistSchema, AlbumArtist, AlbumArtistSchema
from flask import request
import json

artists_schema = ArtistSchema(many=True)
artist_schema = ArtistSchema()

class ArtistResource(Resource):
    def get(self, artist_id):
        artist = Artist.query.filter_by(artist_id=artist_id).first()
        return { "status": "success", "data": artist_schema.dump(artist).data }, 200
