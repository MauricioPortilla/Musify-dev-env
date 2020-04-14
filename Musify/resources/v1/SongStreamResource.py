from flask_restful import Resource
from werkzeug.datastructures import Headers
from flask import request, Response
from run import songsDirectory
import json
import subprocess
import sys

class SongStreamResource(Resource):
    def get(self, song_id):
        headers = Headers()
        def generateData(song_id, headers):
            songFileCall = subprocess.Popen(
                "php resources/v1/components/php/find_song.php " + str(song_id),
                shell=True, 
                stdout=subprocess.PIPE
            )
            songFile = songFileCall.stdout.read().splitlines()[1].decode("utf-8");
            totalBytes = 0
            with open(songsDirectory + "/" + songFile, 'rb') as songStream:
                data = songStream.read(1024)
                while data:
                    yield data
                    data = songStream.read(1024)
                    totalBytes += 1024
                headers.add("Content-Range", "bytes */" + str(totalBytes))
        return Response(generateData(song_id, headers), mimetype="audio/x-wav", headers=headers)