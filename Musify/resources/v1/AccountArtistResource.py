from flask_restful import Resource
from Model import database, Artist, ArtistSchema
from flask import request
from resources.v1.AuthResource import auth_token
import json

artist_schema = ArtistSchema()

class AccountArtistResource(Resource):
    @auth_token
    def get(self, account, account_id):
    	if account.account_id != account_id:
        	return { "status": "failed", "message": "Unauthorized." }, 401
    	artist = Artist.query.filter_by(account_id=account_id).first()
    	if not artist:
        	return { "status": "failure", "message": "It's not an artist." }, 422
    	return { "status": "success", "data": artist_schema.dump(artist).data }, 200
