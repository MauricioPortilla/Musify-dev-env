from flask_restful import Resource
from werkzeug.datastructures import Headers
from flask import request, Response
from run import songsDirectory
import json
import subprocess
import sys

class SongStreamResource(Resource):
    def get(self):
        data = json.loads(request.args.to_dict()["data"])
        if not data:
            return { "status": "failed", 'message': 'No input data provided' }, 400
        headers = Headers()
        def generateData(data, headers):
            songFileCall = subprocess.Popen(
                "php resources/v1/components/php/find_song.php " + str(data["song_id"]),
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
        return Response(generateData(data, headers), mimetype="audio/x-wav", headers=headers)
