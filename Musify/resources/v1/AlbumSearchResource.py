from flask_restful import Resource
from Model import database, Album, AlbumSchema
from .AuthResource import auth_token

albums_schema = AlbumSchema(many=True)

class AlbumSearchResource(Resource):
    @auth_token
    def get(self, account, name):
        albums = Album.query.filter(Album.name.like("{}%".format(name))).all()
        return { "status": "success", "data": albums_schema.dump(albums).data }, 200
