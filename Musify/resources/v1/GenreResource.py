from flask_restful import Resource
from Model import database, Genre, GenreSchema
from flask import request
from .AuthResource import auth_token
from .lang.lang import get_request_message
import json

genres_schema = GenreSchema(many=True)
genre_schema = GenreSchema()

class GenreResource(Resource):
    @auth_token
    def get(self, account, genre_id=None):
    	if genre_id is None:
    		genres = Genre.query.all()
    		return { "status": "success", "data": genres_schema.dump(genres).data }, 200
    	else:
        	genre = Genre.query.filter_by(genre_id=genre_id).first()
        	if not genre:
        		return { "status": "failed", "message": get_request_message(request, "NON_EXISTENT_GENRE") }, 422
        	return { "status": "success", "data": genre_schema.dump(genre).data }, 200
