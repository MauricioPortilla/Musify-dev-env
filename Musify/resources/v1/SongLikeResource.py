from flask_restful import Resource
from Model import database, Song, SongLike, SongDislike, SongLikeSchema
from flask import request
from .AuthResource import auth_token
from .lang.lang import get_request_message
import json

song_likes_schema = SongLikeSchema(many=True)
song_like_schema = SongLikeSchema()

class SongLikeResource(Resource):
    @auth_token
    def get(self, account, song_id):
        song_like = SongLike.query.filter_by(account_id=account.account_id, song_id=song_id).first()
        if not song_like:
            return { "status": "failed", "message": get_request_message(request, "NO_RATE_SUBMITTED") }, 422
        return { "status": "success", "data": song_like_schema.dump(song_like).data }, 200

    @auth_token
    def post(self, account, song_id):
        json_data = request.get_json()
        if not json_data:
            return { "status": "failed", "message": get_request_message(request, "NO_INPUT_DATA_PROVIDED") }, 400
        if account.account_id != json_data["account_id"]:
            return { "status": "failed", "message": get_request_message(request, "UNAUTHORIZED") }, 401
        song = Song.query.filter_by(song_id=song_id).first()
        if not song:
            return { "status": "failed", "message": get_request_message(request, "NON_EXISTENT_SONG") }, 422
        song_like = SongLike.query.filter_by(song_id=song_id, account_id=account.account_id).first()
        song_dislike = SongDislike.query.filter_by(song_id=song_id, account_id=account.account_id).first()
        if song_like or song_dislike:
            return { "status": "failed", "message": get_request_message(request, "RATE_ALREADY_SUBMITTED") }, 401
        song_like = SongLike(json_data["account_id"], song.song_id)
        database.session.add(song_like)
        database.session.commit()
        result = song_like_schema.dump(song_like).data
        return { "status": "success", "data": result }, 201

    @auth_token
    def delete(self, account, song_id):
        json_data = request.get_json()
        if not json_data:
            return { "status": "failed", "message": get_request_message(request, "NO_INPUT_DATA_PROVIDED") }, 400
        if account.account_id != json_data["account_id"]:
            return { "status": "failed", "message": get_request_message(request, "UNAUTHORIZED") }, 401
        song = Song.query.filter_by(song_id=song_id).first()
        if not song:
            return { "status": "failed", "message": get_request_message(request, "NON_EXISTENT_SONG") }, 422
        song_like = SongLike.query.filter_by(song_id=song_id, account_id=account.account_id).first()
        if not song_like:
            return { "status": "failed", "message": get_request_message(request, "NO_RATE_SUBMITTED") }, 422
        database.session.delete(song_like)
        database.session.commit()
        return { "status": "success", "message": get_request_message(request, "SONG_RATE_DELETED") }, 200
