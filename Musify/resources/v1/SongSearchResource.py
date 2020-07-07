from flask_restful import Resource
from Model import database, Song, SongSchema
from .AuthResource import auth_token

songs_schema = SongSchema(many=True)

class SongSearchResource(Resource):
    @auth_token
    def get(self, account, title):
        songs = Song.query.filter(Song.title.ilike("{}%".format(title)), Song.status=="ready").all()
        return { "status": "success", "data": songs_schema.dump(songs).data }, 200
