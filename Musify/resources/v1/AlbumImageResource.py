from flask import make_response
from flask_restful import Resource
from Model import database, Album, AlbumSchema
from flask import request, Response
from run import ALBUM_IMAGES_DIRECTORY, ALLOWED_FILE_IMAGE_EXTENSIONS
from werkzeug.utils import secure_filename
import datetime
from resources.v1.AuthResource import auth_token
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
        fullpath = os.path.join(ALBUM_IMAGES_DIRECTORY, album.image_location)
        resp = make_response(open(fullpath, 'rb').read())
        resp.content_type = "image/png"
        return resp

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
    			file.save(os.path.join(ALBUM_IMAGES_DIRECTORY, newFileName))
    			response = json.loads(json.dumps({"name": newFileName}))
    			results.append(response);
    	if not results:
    		return { "status": "failes", "message": "No selected files." }, 400
    	return { "status": "success", "data": results }, 201
