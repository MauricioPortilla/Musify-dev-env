from flask_restful import Resource
from Model import database, Playlist, PlaylistSchema
from flask import request
import json

playlists_schema = PlaylistSchema(many=True)
playlist_schema = PlaylistSchema()

class PlaylistResource(Resource):
    def get(self):
        data = json.loads(request.args.to_dict()["data"])
        if not data:
            return { "status": "failed", 'message': 'No input data provided' }, 400
        if (data["request_type"] == "accountPlaylists"):
            playlists = Playlist.query.filter_by(account_id=data["account_id"])
            return { "status": "success", "data": playlists_schema.dump(playlists).data }, 200

    def post(self):
        json_data = request.get_json()
        if not json_data:
            return { "status": "failed", 'message': 'No input data provided' }, 400
        data, errors = playlist_schema.load(json_data)
        if errors:
            return errors, 422
        playlist = Playlist(account_id=data["account_id"], name=data["name"])
        database.session.add(playlist)
        database.session.commit()
        result = playlist_schema.dump(playlist).data
        return { "status": "success", "data": result }, 201
