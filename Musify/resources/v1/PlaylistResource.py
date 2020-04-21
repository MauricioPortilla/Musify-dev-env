from flask_restful import Resource
from Model import database, Playlist, PlaylistSchema
from flask import request
from resources.v1.AuthResource import auth_token
import json

playlists_schema = PlaylistSchema(many=True)
playlist_schema = PlaylistSchema()

class PlaylistResource(Resource):
    @auth_token
    def get(self, account):
        data = json.loads(request.args.to_dict()["data"])
        if not data:
            return { "status": "failed", 'message': 'No input data provided' }, 400

    @auth_token
    def post(self, account):
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
