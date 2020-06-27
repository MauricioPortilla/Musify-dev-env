from flask_restful import Resource
from Model import database, Playlist, PlaylistSchema, PlaylistSong
from flask import request
from resources.v1.AuthResource import auth_token
import json

playlists_schema = PlaylistSchema(many=True)
playlist_schema = PlaylistSchema()

class PlaylistResource(Resource):
    @auth_token
    def post(self, account):
        json_data = request.get_json()
        if not json_data:
            return { "status": "failed", "message": "No input data provided." }, 400
        data, errors = playlist_schema.load(json_data)
        if errors:
            return errors, 422
        if account.account_id != data["account_id"]:
            return { "status": "failed", "message": "Unauthorized." }, 401
        playlist = Playlist(account_id=data["account_id"], name=data["name"])
        database.session.add(playlist)
        database.session.commit()
        result = playlist_schema.dump(playlist).data
        return { "status": "success", "data": result }, 201

    @auth_token
    def put(self, account, playlist_id):
        json_data = request.get_json()
        if not json_data:
            return { "status": "failed", "message": "No input data provided." }, 400
        if len(json_data["name"]) == 0 or str.isspace(json_data["name"]):
            return { "status": "failed", "message": "No valid input data provided." }, 400
        playlist = Playlist.query.filter_by(playlist_id=playlist_id).first()
        if not playlist:
            return { "status": "failed", "message": "This playlist does not exist." }, 422
        if account.account_id != playlist.account_id:
            return { "status": "failed", "message": "Unauthorized." }, 401
        playlist.name = json_data["name"]
        database.session.commit()
        return { "status": "success", "data": playlist_schema.dump(playlist).data }, 201

    @auth_token
    def delete(self, account, playlist_id):
        playlist = Playlist.query.filter_by(playlist_id=playlist_id).first()
        if not playlist:
            return { "status": "failed", "message": "This playlist does not exist." }, 422
        if account.account_id != playlist.account_id:
            return { "status": "failed", "message": "Unauthorized." }, 401
        songs = PlaylistSong.query.filter_by(playlist_id=playlist_id)
        for song in songs:
            database.session.delete(song)
        database.session.delete(playlist)
        database.session.commit()
        return { "status": "success", "message": "Playlist deleted." }, 200
