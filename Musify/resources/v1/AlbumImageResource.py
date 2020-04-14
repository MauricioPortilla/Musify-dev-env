from flask import make_response
from flask_restful import Resource
from Model import database, Album, AlbumSchema
import os

album_schema = AlbumSchema()

class AlbumImageResource(Resource):
    def get(self, album_id):
        album = Album.query.filter_by(album_id=album_id).first()
        fullpath = os.getcwd() + "/storage/albumImages/" + album.image_location
        resp = make_response(open(fullpath, 'rb').read())
        resp.content_type = "image/png"
        return resp
