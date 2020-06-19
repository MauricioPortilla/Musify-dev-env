from flask_restful import Resource
from Model import database, AccountSong, AccountSongSchema
from flask import request, Response
from run import ALLOWED_FILE_SONG_EXTENSIONS, ACCOUNT_SONGS_DIRECTORY
from werkzeug.utils import secure_filename
import datetime
from resources.v1.AuthResource import auth_token
from time import strftime, gmtime
import sys, os, hashlib
import audio_metadata

accountsong_schema = AccountSongSchema()
accountsongs_schema = AccountSongSchema(many=True)

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_FILE_SONG_EXTENSIONS

class AccountAccountSongResource(Resource):
    @auth_token
    def get(self, account, account_id, account_song_id=None):
        if account_song_id is None:
            if account.account_id != account_id:
                return { "status": "failed", "message": "Unauthorized." }, 401
            accountsongs = AccountSong.query.filter_by(account_id=account_id)
            return { "status": "success", "data": accountsongs_schema.dump(accountsongs).data }, 200
        else:
            if account.account_id != account_id:
                return { "status": "failed", "message": "Unauthorized." }, 401
            accountsong = AccountSong.query.filter_by(account_song_id=account_song_id, account_id=account_id).first()
            if not accountsong:
                return { "status": "failed", "message": "This account song does not exist." }, 422
            return { "status": "success", "data": accountsong_schema.dump(accountsong).data }, 200

    @auth_token
    def post(self, account, account_id):
        if account.account_id != account_id:
            return { "status": "failed", "message": "Unauthorized." }, 401
        results = []
        for fileData in request.files:
            file = request.files[fileData]
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename).replace("_", " ")
                newFileName = hashlib.sha1(
                    (filename + str(datetime.datetime.now().timestamp())).encode()
                ).hexdigest() + "." + file.filename.rsplit('.', 1)[1].lower()
                file.save(os.path.join(ACCOUNT_SONGS_DIRECTORY, newFileName))
                audioFileMetadata = audio_metadata.load(ACCOUNT_SONGS_DIRECTORY + "/" + newFileName)
                newAccountSong = AccountSong(
                    account_id, 
                    filename, 
                    strftime("%M:%S", gmtime(audioFileMetadata.streaminfo.duration)),
                    newFileName,
                    datetime.datetime.today().strftime("%Y-%m-%d")
                )
                database.session.add(newAccountSong)
                database.session.commit()
                result = accountsong_schema.dump(newAccountSong).data
                results.append(result)
        if not results:
            return { "status": "failed", "message": "No selected files." }, 400
        return { "status": "success", "data": results }, 201

    @auth_token
    def delete(self, account, account_id, account_song_id):
        if account.account_id != account_id:
            return { "status": "failed", "message": "Unauthorized." }, 401
        accountSong = AccountSong.query.filter_by(account_song_id=account_song_id, account_id=account_id).first()
        if not accountSong:
            return { "status": "failed", "message": "This account song does not exist." }, 422
        database.session.delete(accountSong)
        database.session.commit()
        os.remove(ACCOUNT_SONGS_DIRECTORY + "/" + accountSong.song_location)
        return { "status": "success", "message": "Account song deleted." }, 200
