from flask_restful import Resource
from Model import database, Song, SongSchema
from flask import request, Response
from .AuthResource import auth_token
from .lang.lang import get_request_message
import json

songs_schema = SongSchema(many=True)
song_schema = SongSchema()

class SongResource(Resource):
    @auth_token
    def get(self, account, song_id):
        song = Song.query.filter_by(song_id=song_id).first()
        if not song:
            return { "status": "failed", "message": get_request_message(request, "NON_EXISTENT_SONG") }, 422
        return { "status": "success", "data": song_schema.dump(song).data }, 200
