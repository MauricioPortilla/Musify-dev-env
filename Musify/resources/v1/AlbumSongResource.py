from flask_restful import Resource
from Model import database, Song, SongSchema
from flask import request
from config import APP_ROOT, ALLOWED_FILE_SONG_EXTENSIONS, SONGS_DIRECTORY, MUSIFY_GRPC_SERVER_ADDRESS, SQLALCHEMY_DATABASE_URI
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
        for file_data in request.files:
            file = request.files[file_data]
            if file and allowed_file(file.filename):
                stored_song = self.store_song_file(file)
                threading.Thread(target=self.upload_song_thread, args=(stored_song["name"],)).start()
                results.append(stored_song);
        if not results:
            return { "status": "failed", "message": "No selected files." }, 400
        return { "status": "success", "data": results }, 201

    def store_song_file(self, file):
        filename = secure_filename(file.filename).replace("_", " ")
        new_filename = hashlib.sha1((filename + str(datetime.datetime.now().timestamp())).encode()).hexdigest() + "." + file.filename.rsplit('.', 1)[1].lower()
        file.save(os.path.join(SONGS_DIRECTORY, newFileName))
        audio_file_metadata = audio_metadata.load(SONGS_DIRECTORY + "/" + new_filename)
        return { 
            "name": new_filename,
            "duration": strftime("%M:%S", gmtime(audio_file_metadata.streaminfo.duration))
        }

    def upload_song_thread(self, filename):
        session_factory = sessionmaker(bind=create_engine(SQLALCHEMY_DATABASE_URI))
        Session = scoped_session(session_factory)
        song = Session.query(Song).filter_by(song_location=filename).first()
        while not song:
            song = Session.query(Song).filter_by(song_location=filename).first()
        client = musify_client.MusifyClient(MUSIFY_GRPC_SERVER_ADDRESS)
        upload_response = json.loads(client.upload(SONGS_DIRECTORY + "/" + filename, filename))
        os.remove(SONGS_DIRECTORY + "/" + filename)
        if song:
            song.song_location = upload_response["name"]
            song.status = "ready"
            Session.commit()
        Session.remove()
