from flask_restful import Resource
from Model import database, AccountSong, AccountSongSchema
from flask import request, Response
from run import ALLOWED_FILE_SONG_EXTENSIONS, accountSongsDirectory
from werkzeug.utils import secure_filename
from datetime import datetime
import sys, os, hashlib

accountsong_schema = AccountSongSchema()
accountsongs_schema = AccountSongSchema(many=True)

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_FILE_SONG_EXTENSIONS

class AccountAccountSongResource(Resource):
    def get(self, account_id):
        accountsongs = AccountSong.query.filter_by(account_id=account_id)
        return { "status": "success", "data": accountsongs_schema.dump(accountsongs).data }, 200

    def post(self, account_id):
        results = []
        for fileData in request.files:
            file = request.files[fileData]
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename).replace("_", " ")
                newFileName = hashlib.sha1(
                    (filename + str(datetime.now().timestamp())).encode()
                ).hexdigest() + "." + file.filename.rsplit('.', 1)[1].lower()
                newAccountSong = AccountSong(
                    account_id, filename, 
                    newFileName,
                    datetime.today().strftime("%Y-%m-%d")
                )
                database.session.add(newAccountSong)
                database.session.commit()
                result = accountsong_schema.dump(newAccountSong).data
                file.save(os.path.join(accountSongsDirectory, newFileName))
                results.append(result)
        if not results:
            return { "status": "failure", "message": "No selected files." }, 400
        return { "status": "success", "data": results }, 201

    def delete(self, account_id, account_song_id):
        accountSong = AccountSong.query.filter_by(account_song_id=account_song_id, account_id=account_id).first()
        if not accountSong:
            return { "status": "failure", "message": "This account song does not exist." }, 401
        database.session.delete(accountSong)
        database.session.commit()
        os.remove(accountSongsDirectory + "/" + accountSong.song_location)
        return { "status": "success", "message": "Account song deleted." }, 204
