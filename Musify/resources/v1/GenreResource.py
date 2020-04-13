from flask_restful import Resource
from Model import database, Genre, GenreSchema
from flask import request
import json

genres_schema = GenreSchema(many=True)
genre_schema = GenreSchema()

class GenreResource(Resource):
    def get(self):
        data = json.loads(request.args.to_dict()["data"])
        if not data:
            return { "status": "failed", 'message': 'No input data provided' }, 400
        if (data["request_type"] == "genreById"):
            genre = Genre.query.filter_by(genre_id=data["genre_id"]).first()
            return { "status": "success", "data": genre_schema.dump(genre).data }, 200
