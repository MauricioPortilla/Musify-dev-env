from flask_restful import Resource
from werkzeug.datastructures import Headers
from flask import request, Response
from run import accountSongsDirectory
from Model import AccountSong
import subprocess
import sys

class AccountSongStreamResource(Resource):
    def get(self, account_song_id):
        accountSong = AccountSong.query.filter_by(account_song_id=account_song_id).first()
        if not accountSong:
            return { "status": "failure", "message": "This account song does not exist." }, 401
        headers = Headers()
        def generateData(accountSong, headers):
            totalBytes = 0
            with open(accountSongsDirectory + "/" + accountSong.song_location, 'rb') as songStream:
                data = songStream.read(1024)
                while data:
                    yield data
                    data = songStream.read(1024)
                    totalBytes += 1024
                headers.add("Content-Range", "bytes */" + str(totalBytes))
        return Response(generateData(accountSong, headers), mimetype="audio/x-wav", headers=headers)
