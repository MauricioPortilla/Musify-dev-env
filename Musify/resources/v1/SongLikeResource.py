from flask_restful import Resource
from Model import database, Song, SongLike, SongLikeSchema
from flask import request
from resources.v1.AuthResource import auth_token
import json

songlikes_schema = SongLikeSchema(many=True)
songlike_schema = SongLikeSchema()

class SongLikeResource(Resource):
    @auth_token
    def get(self, account, song_id):
        songLike = SongLike.query.filter_by(account_id=account.account_id, song_id=song_id).first()
        if not songLike:
            return { "status": "failed", "message": "No rate submitted to this song." }, 422
        return { "status": "success", "data": songlike_schema.dump(songLike).data }, 200

    @auth_token
    def post(self, account, song_id):
        json_data = request.get_json()
        if not json_data:
            return { "status": "failed", "message": "No input data provided." }, 400
        if account.account_id != json_data["account_id"]:
            return { "status": "failed", "message": "Unauthorized." }, 401
        song = Song.query.filter_by(song_id=song_id).first()
        if not song:
            return { "status": "failed", "message": "This song does not exist." }, 422
        songLike = SongLike(json_data["account_id"], song.song_id)
        database.session.add(songLike)
        database.session.commit()
        result = songlike_schema.dump(songLike).data
        return { "status": "success", "data": result }, 201
