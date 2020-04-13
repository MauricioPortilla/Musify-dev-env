from flask_restful import Resource
from Model import database, Song, SongSchema
from werkzeug.datastructures import Headers
from flask import request, Response
from run import songsDirectory
import json
import subprocess
import sys

songs_schema = SongSchema(many=True)
song_schema = SongSchema()

class SongResource(Resource):
    def get(self):
        data = json.loads(request.args.to_dict()["data"])
        if not data:
            return { "status": "failed", 'message': 'No input data provided' }, 400
        