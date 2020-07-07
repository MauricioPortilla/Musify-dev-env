from flask_restful import Resource
from flask import request, Response
from config import MUSIFY_GRPC_SERVER_ADDRESS
from Model import Song, SongSchema
from .AuthResource import auth_token
from .lang.lang import get_request_message
import json, subprocess, sys
sys.path.insert(1, '/home/vagrant/Musify/grpc/src')
import musify_client

song_schema = SongSchema()

class SongStreamResource(Resource):
    @auth_token
    def get(self, account, song_id, quality_type):
        song = Song.query.filter_by(song_id=song_id).first()
        if not song:
            return { "status": "failed", "message": get_request_message(request, "NON_EXISTENT_SONG") }, 422
        if song.status != "ready":
            return { "status": "failed", "message": get_request_message(request, "SONG_NOT_READY_YET") }, 401
        def generate_data(song, quality_type):
            client = musify_client.MusifyClient(MUSIFY_GRPC_SERVER_ADDRESS)
            response = client.download(song.song_location, quality_type)
            for chunk in response:
                yield chunk.buffer
        return Response(generate_data(song, quality_type), mimetype="audio/mp3")
