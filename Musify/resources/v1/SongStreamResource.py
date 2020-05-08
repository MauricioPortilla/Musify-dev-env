from flask_restful import Resource
from flask import request, Response
from run import MUSIFY_GRPC_SERVER_ADDRESS
from Model import Song, SongSchema
from resources.v1.AuthResource import auth_token
import json
import subprocess
import sys
sys.path.insert(1, '/home/vagrant/Musify/grpc/src')
import musify_client

song_schema = SongSchema()

class SongStreamResource(Resource):
    @auth_token
    def get(self, account, song_id, quality_type):
        song = Song.query.filter_by(song_id=song_id).first()
        if not song:
            return { "status": "failed", "message": "This song does not exist." }, 422
        def generateData(song, quality_type):
            client = musify_client.MusifyClient(MUSIFY_GRPC_SERVER_ADDRESS)
            response = client.download(song.song_location, quality_type)
            for chunk in response:
                yield chunk.buffer
        return Response(generateData(song, quality_type), mimetype="audio/mp3")
