from flask_restful import Resource
from Model import database, Artist, ArtistSchema
from resources.v1.AuthResource import auth_token

artists_schema = ArtistSchema(many=True)

class ArtistSearchResource(Resource):
    @auth_token
    def get(self, account, artistic_name):
        albums = Artist.query.filter(Artist.artistic_name.like("{}%".format(artistic_name))).all()
        return { "status": "success", "data": artists_schema.dump(albums).data }, 200
