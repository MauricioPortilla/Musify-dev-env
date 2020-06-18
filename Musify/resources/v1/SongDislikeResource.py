from flask_restful import Resource
from Model import database, Song, SongDislike, SongLike, SongDislikeSchema
from flask import request
from resources.v1.AuthResource import auth_token
import json

songdislikes_schema = SongDislikeSchema(many=True)
songdislike_schema = SongDislikeSchema()

class SongDislikeResource(Resource):
    @auth_token
    def get(self, account, song_id):
        songDislike = SongDislike.query.filter_by(account_id=account.account_id, song_id=song_id).first()
        if not songDislike:
            return { "status": "failed", "message": "No rate submitted to this song." }, 422
        return { "status": "success", "data": songdislike_schema.dump(songDislike).data }, 200
    
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
        songLike = SongLike.query.filter_by(song_id=song_id, account_id=account.account_id).first()
        songDislike = SongDislike.query.filter_by(song_id=song_id, account_id=account.account_id).first()
        if songLike or songDislike:
            return { "status": "failed", "message": "A rate was already submitted." }, 401
        songDislike = SongDislike(json_data["account_id"], song.song_id)
        database.session.add(songDislike)
        database.session.commit()
        result = songdislike_schema.dump(songDislike).data
        return { "status": "success", "data": result }, 201

    @auth_token
    def delete(self, account, song_id):
        json_data = request.get_json()
        if not json_data:
            return { "status": "failed", "message": "No input data provided." }, 400
        if account.account_id != json_data["account_id"]:
            return { "status": "failed", "message": "Unauthorized." }, 401
        song = Song.query.filter_by(song_id=song_id).first()
        if not song:
            return { "status": "failed", "message": "This song does not exist." }, 422
        songDislike = SongDislike.query.filter_by(song_id=song_id, account_id=account.account_id).first()
        if not songDislike:
            return { "status": "failed", "message": "No rate submitted to this song." }, 422
        database.session.delete(songDislike)
        database.session.commit()
        return { "status": "success", "message": "Song rate deleted." }, 200
