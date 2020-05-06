from flask_restful import Resource
from Model import database, Song, SongSchema
from resources.v1.AuthResource import auth_token

songs_schema = SongSchema(many=True)

class SongSearchResource(Resource):
    @auth_token
    def get(self, account, title):
        songs = Song.query.filter(Song.title.like("{}%".format(title))).all()
        return { "status": "success", "data": songs_schema.dump(songs).data }, 200
