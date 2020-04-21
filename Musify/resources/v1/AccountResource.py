from flask_restful import Resource
from Model import database, Account, AccountSchema, Artist, ArtistSchema
from flask import request
from datetime import date
from resources.v1.AuthResource import auth_token
import hashlib, json

accounts_schema = AccountSchema(many=True)
account_schema = AccountSchema()

class AccountResource(Resource):
    @auth_token
    def get(self, account):
        if not "data" in request.args.to_dict():
            accounts = Account.query.all()
            accounts = accounts_schema.dump(accounts).data
            return { "status": "success", "data": accounts }, 200
        data = json.loads(request.args.to_dict()["data"])
        accounts = Account.query.filter(data).all()
        return { "status": "success", "data": accounts }, 200
