from flask_restful import Resource
from Model import database, Song, SongSchema
from flask import request, Response
import json

songs_schema = SongSchema(many=True)
song_schema = SongSchema()

class SongResource(Resource):
    def get(self, song_id):
        song = Song.query.filter_by(song_id=song_id).first()
        return { "status": "success", "data": song_schema.dump(song).data }
