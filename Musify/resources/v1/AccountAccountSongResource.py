from flask_restful import Resource
from Model import database, AccountSong, AccountSongSchema
from flask import request, Response
from config import ALLOWED_FILE_SONG_EXTENSIONS, ACCOUNT_SONGS_DIRECTORY
from werkzeug.utils import secure_filename
import datetime
from resources.v1.AuthResource import auth_token
from time import strftime, gmtime
import sys, os, hashlib
import audio_metadata

account_song_schema = AccountSongSchema()
account_songs_schema = AccountSongSchema(many=True)

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_FILE_SONG_EXTENSIONS

class AccountAccountSongResource(Resource):
    @auth_token
    def get(self, account, account_id, account_song_id=None):
        if account_song_id is None:
            if account.account_id != account_id:
                return { "status": "failed", "message": "Unauthorized." }, 401
            account_songs = AccountSong.query.filter_by(account_id=account_id)
            return { "status": "success", "data": account_songs_schema.dump(account_songs).data }, 200
        else:
            if account.account_id != account_id:
                return { "status": "failed", "message": "Unauthorized." }, 401
            account_song = AccountSong.query.filter_by(account_song_id=account_song_id, account_id=account_id).first()
            if not account_song:
                return { "status": "failed", "message": "This account song does not exist." }, 422
            return { "status": "success", "data": account_song_schema.dump(account_song).data }, 200

    @auth_token
    def post(self, account, account_id):
        if account.account_id != account_id:
            return { "status": "failed", "message": "Unauthorized." }, 401
        results = []
        for file_data in request.files:
            file = request.files[file_data]
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename).replace("_", " ")
                new_filename = hashlib.sha1((filename + str(datetime.datetime.now().timestamp())).encode()).hexdigest() + "." + file.filename.rsplit('.', 1)[1].lower()
                file.save(os.path.join(ACCOUNT_SONGS_DIRECTORY, new_filename))
                audio_file_metadata = audio_metadata.load(ACCOUNT_SONGS_DIRECTORY + "/" + new_filename)
                new_account_song = AccountSong(
                    account_id, 
                    filename, 
                    strftime("%M:%S", gmtime(audio_file_metadata.streaminfo.duration)),
                    new_filename,
                    datetime.datetime.today().strftime("%Y-%m-%d")
                )
                database.session.add(new_account_song)
                database.session.commit()
                result = account_song_schema.dump(new_account_song).data
                results.append(result)
        if not results:
            return { "status": "failed", "message": "No selected files." }, 400
        return { "status": "success", "data": results }, 201

    @auth_token
    def delete(self, account, account_id, account_song_id):
        if account.account_id != account_id:
            return { "status": "failed", "message": "Unauthorized." }, 401
        account_song = AccountSong.query.filter_by(account_song_id=account_song_id, account_id=account_id).first()
        if not account_song:
            return { "status": "failed", "message": "This account song does not exist." }, 422
        database.session.delete(account_song)
        database.session.commit()
        os.remove(ACCOUNT_SONGS_DIRECTORY + "/" + account_song.song_location)
        return { "status": "success", "message": "Account song deleted." }, 200
