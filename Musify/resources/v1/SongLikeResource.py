from flask_restful import Resource
from Model import database, Song, SongLike, SongLikeSchema
from flask import request
from resources.v1.AuthResource import auth_token
import json

songlikes_schema = SongLikeSchema(many=True)
songlike_schema = SongLikeSchema()

class SongLikeResource(Resource):
    # @auth_token
    # def get(self, account, genre_id):
    #     genre = Genre.query.filter_by(genre_id=genre_id).first()
    #     return { "status": "success", "data": genre_schema.dump(genre).data }, 200
    @auth_token
    def post(self, account, song_id):
        json_data = request.get_json()
        if not json_data:
            return { "status": "failed", 'message': 'No input data provided' }, 400
        song = Song.query.filter_by(song_id=song_id).first()
        if not song:
            return { "status": "failed", "message": "No song found." }, 401
        songLike = SongLike(json_data["account_id"], song.song_id)
        database.session.add(songLike)
        database.session.commit()
        result = songlike_schema.dump(songLike).data
        return { "status": "success", "data": result}, 201
