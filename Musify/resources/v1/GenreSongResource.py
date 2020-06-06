from flask_restful import Resource
from Model import database, Song, SongSchema
from flask import request, Response
from resources.v1.AuthResource import auth_token

songs_schema = SongSchema(many=True)
song_schema = SongSchema()

class GenreSongResource(Resource):
    @auth_token
    def get(self, account, genre_id):
        songs = Song.query.filter_by(genre_id=genre_id)
        return { "status": "success", "data": songs_schema.dump(songs).data }, 200