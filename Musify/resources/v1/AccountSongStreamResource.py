from flask_restful import Resource
from werkzeug.datastructures import Headers
from flask import request, Response
from config import ACCOUNT_SONGS_DIRECTORY
from Model import AccountSong
from .AuthResource import auth_token
from .lang.lang import get_request_message
import subprocess
import sys

class AccountSongStreamResource(Resource):
    @auth_token
    def get(self, account, account_song_id):
        account_song = AccountSong.query.filter_by(account_song_id=account_song_id).first()
        if not account_song:
            return { "status": "failed", "message": get_request_message(request, "NON_EXISTENT_ACCOUNT_SONG") }, 422
        if account.account_id != account_song.account_id:
            return { "status": "failed", "message": get_request_message(request, "UNAUTHORIZED") }, 401
        headers = Headers()
        def generate_data(accountSong, headers):
            total_bytes = 0
            with open(ACCOUNT_SONGS_DIRECTORY + "/" + account_song.song_location, 'rb') as song_stream:
                data = song_stream.read(1024)
                while data:
                    yield data
                    data = song_stream.read(1024)
                    total_bytes += 1024
                headers.add("Content-Range", "bytes */" + str(total_bytes))
        return Response(generate_data(account_song, headers), mimetype="audio/x-wav", headers=headers)
