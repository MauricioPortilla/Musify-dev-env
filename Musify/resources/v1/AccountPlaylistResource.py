from flask_restful import Resource
from Model import database, Playlist, PlaylistSchema
from flask import request
import json

playlists_schema = PlaylistSchema(many=True)
playlist_schema = PlaylistSchema()

class AccountPlaylistResource(Resource):
    def get(self, account_id):
        playlists = Playlist.query.filter_by(account_id=account_id)
        return { "status": "success", "data": playlists_schema.dump(playlists).data }, 200
