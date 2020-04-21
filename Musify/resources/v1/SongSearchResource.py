from flask_restful import Resource
from Model import database, Song, SongSchema
from werkzeug.datastructures import Headers
from flask import request, Response
from run import songsDirectory
from resources.v1.AuthResource import auth_token
import json
import subprocess
import sys

songs_schema = SongSchema(many=True)
song_schema = SongSchema()

class SongSearchResource(Resource):
    @auth_token
    def get(self, account, title):
        songs = Song.query.filter(Song.title.like("{}%".format(title))).all()
        return { "status": "success", "data": songs_schema.dump(songs).data }, 200
