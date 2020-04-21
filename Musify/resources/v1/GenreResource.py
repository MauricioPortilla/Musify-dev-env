from flask_restful import Resource
from Model import database, Genre, GenreSchema
from flask import request
from resources.v1.AuthResource import auth_token
import json

genres_schema = GenreSchema(many=True)
genre_schema = GenreSchema()

class GenreResource(Resource):
    @auth_token
    def get(self, account, genre_id):
        genre = Genre.query.filter_by(genre_id=genre_id).first()
        return { "status": "success", "data": genre_schema.dump(genre).data }, 200
