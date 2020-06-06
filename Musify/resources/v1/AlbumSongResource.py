from flask_restful import Resource
from Model import database, Song, SongSchema
from flask import request
from run import APP_ROOT, ALLOWED_FILE_SONG_EXTENSIONS, SONGS_DIRECTORY, MUSIFY_GRPC_SERVER_ADDRESS
from werkzeug.utils import secure_filename
from resources.v1.AuthResource import auth_token
from time import strftime, gmtime
import datetime, sys, os, hashlib, audio_metadata, json
sys.path.insert(1, APP_ROOT + '/grpc/src')
import musify_client

songs_schema = SongSchema(many=True)
song_schema = SongSchema()

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_FILE_SONG_EXTENSIONS

class AlbumSongResource(Resource):
    @auth_token
    def get(self, account, album_id):
        songs = Song.query.filter_by(album_id=album_id)
        return { "status": "success", "data": songs_schema.dump(songs).data }, 200

    @auth_token
    def post(self, account):
        results = []
        for fileData in request.files:
            file = request.files[fileData]
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename).replace("_", " ")
                newFileName = hashlib.sha1(
    				(filename + str(datetime.datetime.now().timestamp())).encode()
    			).hexdigest() + "." + file.filename.rsplit('.', 1)[1].lower()
                file.save(os.path.join(SONGS_DIRECTORY, newFileName))
                audioFileMetadata = audio_metadata.load(SONGS_DIRECTORY + "/" + newFileName)
                client = musify_client.MusifyClient(MUSIFY_GRPC_SERVER_ADDRESS)
                response_song = json.loads(client.upload(SONGS_DIRECTORY + "/" + newFileName, newFileName))
                print(">> RECEIVED: " + str(response_song), file=sys.stderr)
                response = json.loads(
                    json.dumps({
                        "name": response_song["name"], 
                        "duration": strftime("%M:%S", gmtime(audioFileMetadata.streaminfo.duration))
                    })
                )
                results.append(response);
                os.remove(SONGS_DIRECTORY + "/" + newFileName)
        if not results:
            return { "status": "failes", "message": "No selected files." }, 400
        return { "status": "success", "data": results }, 201
