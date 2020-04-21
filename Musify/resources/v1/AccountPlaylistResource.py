from flask_restful import Resource
from Model import database, Playlist, PlaylistSchema
from flask import request
from resources.v1.AuthResource import auth_token
import json

playlists_schema = PlaylistSchema(many=True)
playlist_schema = PlaylistSchema()

class AccountPlaylistResource(Resource):
    @auth_token
    def get(self, account, account_id):
        playlists = Playlist.query.filter_by(account_id=account_id)
        return { "status": "success", "data": playlists_schema.dump(playlists).data }, 200
