from flask_restful import Resource
from flask import request, Response
from run import songsDirectory, MUSIFY_GRPC_SERVER_ADDRESS
from Model import Song, SongSchema
import json
import subprocess
import sys
sys.path.insert(1, '/home/vagrant/Musify/grpc/src')
import musify_client

song_schema = SongSchema()

class SongStreamResource(Resource):
    def get(self, song_id, quality_type):
        song = Song.query.filter_by(song_id=song_id).first()
        if not song:
            return { "status": "failure", "message": "This song does not exist." }, 401
        def generateData(song, quality_type):
            client = musify_client.MusifyClient(MUSIFY_GRPC_SERVER_ADDRESS)
            response = client.download(song.song_location, quality_type)
            for chunk in response:
                yield chunk.buffer
        return Response(generateData(song, quality_type), mimetype="audio/mp3")
