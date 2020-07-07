from flask_restful import Resource
from Model import database, Playlist, PlaylistSchema
from flask import request
from .AuthResource import auth_token
from .lang.lang import get_request_message
import json

playlists_schema = PlaylistSchema(many=True)
playlist_schema = PlaylistSchema()

class AccountPlaylistResource(Resource):
    @auth_token
    def get(self, account, account_id):
        if account.account_id != account_id:
            return { "status": "failed", "message": get_request_message(request, "UNAUTHORIZED") }, 401
        playlists = Playlist.query.filter_by(account_id=account_id)
        return { "status": "success", "data": playlists_schema.dump(playlists).data }, 200
