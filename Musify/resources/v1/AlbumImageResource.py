from flask import make_response
from flask_restful import Resource
from Model import database, Album, AlbumSchema
from flask import request, Response
from config import ALBUM_IMAGES_DIRECTORY, ALLOWED_FILE_IMAGE_EXTENSIONS
from werkzeug.utils import secure_filename
import datetime
from .AuthResource import auth_token
from .lang.lang import get_request_message
from time import strftime, gmtime
import sys, os, hashlib
import json

album_schema = AlbumSchema()

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_FILE_IMAGE_EXTENSIONS

class AlbumImageResource(Resource):
    @auth_token
    def get(self, account, album_id):
        album = Album.query.filter_by(album_id=album_id).first()
        if not album:
            return { "status": "failed", "data": get_request_message(request, "NON_EXISTENT_ALBUM") }, 422
        full_path = os.path.join(ALBUM_IMAGES_DIRECTORY, album.image_location)
        resp = make_response(open(full_path, 'rb').read())
        resp.content_type = "image/png"
        return resp

    @auth_token
    def post(self, account):
        results = []
        for file_data in request.files:
            file = request.files[file_data]
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename).replace("_", " ")
                new_filename = hashlib.sha1(
                    (filename + str(datetime.datetime.now().timestamp())).encode()
                ).hexdigest() + "." + file.filename.rsplit('.', 1)[1].lower()
                file.save(os.path.join(ALBUM_IMAGES_DIRECTORY, new_filename))
                response = json.loads(json.dumps({ "image_location": new_filename }))
                results.append(response);
        if not results:
            return { "status": "failed", "message": get_request_message(request, "NO_FILES_SELECTED") }, 400
        return { "status": "success", "data": results }, 201
