from flask_restful import Resource
from Model import database, Song, SongSchema
from flask import request, Response
from .AuthResource import auth_token

songs_schema = SongSchema(many=True)

class GenreSongResource(Resource):
    @auth_token
    def get(self, account, genre_id):
        songs = Song.query.filter_by(genre_id=genre_id, status="ready")
        return { "status": "success", "data": songs_schema.dump(songs).data }, 200
