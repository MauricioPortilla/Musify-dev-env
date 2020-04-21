from flask_restful import Resource
from Model import database, Song, SongSchema
from flask import request, Response
from resources.v1.AuthResource import auth_token
import json

songs_schema = SongSchema(many=True)
song_schema = SongSchema()

class SongResource(Resource):
    @auth_token
    def get(self, account, song_id):
        song = Song.query.filter_by(song_id=song_id).first()
        return { "status": "success", "data": song_schema.dump(song).data }
