from flask_restful import Resource
from Model import database, Song, SongSchema
from flask import request, Response

songs_schema = SongSchema(many=True)
song_schema = SongSchema()

class AlbumSongResource(Resource):
    def get(self, album_id):
        songs = Song.query.filter_by(album_id=album_id)
        return { "status": "success", "data": songs_schema.dump(songs).data }
