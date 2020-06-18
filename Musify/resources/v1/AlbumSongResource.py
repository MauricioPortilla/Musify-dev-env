from flask_restful import Resource
from Model import database, Song, SongSchema
from flask import request
from run import APP_ROOT, ALLOWED_FILE_SONG_EXTENSIONS, SONGS_DIRECTORY, MUSIFY_GRPC_SERVER_ADDRESS
from config import SQLALCHEMY_DATABASE_URI
from werkzeug.utils import secure_filename
from resources.v1.AuthResource import auth_token
from time import strftime, gmtime
import datetime, sys, os, hashlib, audio_metadata, json, threading
sys.path.insert(1, APP_ROOT + '/grpc/src')
import musify_client
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

songs_schema = SongSchema(many=True)
song_schema = SongSchema()

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_FILE_SONG_EXTENSIONS

class AlbumSongResource(Resource):
    @auth_token
    def get(self, account, album_id):
        songs = Song.query.filter_by(album_id=album_id, status="ready")
        return { "status": "success", "data": songs_schema.dump(songs).data }, 200

    @auth_token
    def post(self, account):
        results = []
        for fileData in request.files:
            file = request.files[fileData]
            if file and allowed_file(file.filename):
                storedSong = self.storeSongFile(file)
                threading.Thread(target=self.uploadSongThread, args=(storedSong["name"],)).start()
                results.append(storedSong);
        if not results:
            return { "status": "failed", "message": "No selected files." }, 400
        return { "status": "success", "data": results }, 201

    def storeSongFile(self, file):
        filename = secure_filename(file.filename).replace("_", " ")
        newFileName = hashlib.sha1(
            (filename + str(datetime.datetime.now().timestamp())).encode()
        ).hexdigest() + "." + file.filename.rsplit('.', 1)[1].lower()
        file.save(os.path.join(SONGS_DIRECTORY, newFileName))
        audioFileMetadata = audio_metadata.load(SONGS_DIRECTORY + "/" + newFileName)
        return { 
            "name": newFileName,
            "duration": strftime("%M:%S", gmtime(audioFileMetadata.streaminfo.duration))
        }

    def uploadSongThread(self, filename):
        session_factory = sessionmaker(bind=create_engine(SQLALCHEMY_DATABASE_URI))
        Session = scoped_session(session_factory)
        song = Session.query(Song).filter_by(song_location=filename).first()
        while not song:
            song = Session.query(Song).filter_by(song_location=filename).first()
        client = musify_client.MusifyClient(MUSIFY_GRPC_SERVER_ADDRESS)
        uploadResponse = json.loads(client.upload(SONGS_DIRECTORY + "/" + filename, filename))
        os.remove(SONGS_DIRECTORY + "/" + filename)
        if song:
            song.song_location = uploadResponse["name"]
            song.status = "ready"
            Session.commit()
        Session.remove()
