from flask_restful import Resource
from Model import database, Song, SongDislike, SongLike, SongDislikeSchema
from flask import request
from resources.v1.AuthResource import auth_token
import json

song_dislikes_schema = SongDislikeSchema(many=True)
song_dislike_schema = SongDislikeSchema()

class SongDislikeResource(Resource):
    @auth_token
    def get(self, account, song_id):
        song_dislike = SongDislike.query.filter_by(account_id=account.account_id, song_id=song_id).first()
        if not song_dislike:
            return { "status": "failed", "message": "No rate submitted to this song." }, 422
        return { "status": "success", "data": song_dislike_schema.dump(song_dislike).data }, 200
    
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
        song_like = SongLike.query.filter_by(song_id=song_id, account_id=account.account_id).first()
        song_dislike = SongDislike.query.filter_by(song_id=song_id, account_id=account.account_id).first()
        if song_like or song_dislike:
            return { "status": "failed", "message": "A rate was already submitted." }, 401
        song_dislike = SongDislike(json_data["account_id"], song.song_id)
        database.session.add(song_dislike)
        database.session.commit()
        result = song_dislike_schema.dump(song_dislike).data
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
        song_dislike = SongDislike.query.filter_by(song_id=song_id, account_id=account.account_id).first()
        if not song_dislike:
            return { "status": "failed", "message": "No rate submitted to this song." }, 422
        database.session.delete(song_dislike)
        database.session.commit()
        return { "status": "success", "message": "Song rate deleted." }, 200
