from flask_restful import Resource
from Model import database, Account, AccountSchema, Artist, ArtistSchema
from flask import request
from datetime import date
import hashlib

accounts_schema = AccountSchema(many=True)
account_schema = AccountSchema()

class AccountResource(Resource):
    def get(self):
        accounts = Account.query.all()
        accounts = accounts_schema.dump(accounts).data
        return { "status": "success", "data": accounts }, 200

    def post(self):
        json_data = request.get_json()
        if not json_data:
            return { 'message': 'No input data provided' }, 400

        if (json_data["requestType"] == "login"):
            account = Account.query.filter_by(
                email=json_data['email'], 
                password=hashlib.sha512(json_data["password"].encode()).hexdigest()
            ).first()
            if not account:
                return { 'message': 'Account does not exist' }, 400
            return account_schema.dump(account).data, 200
        elif (json_data["requestType"] == "register"):
            data, errors = account_schema.load(json_data)
            if errors:
                return errors, 422
            account = Account.query.filter_by(name=data['email']).first()
            if account:
                return { 'message': 'Account already exists' }, 400
            account = Account(
                email=data['email'],
                password=hashlib.sha512(data['password'].encode()).hexdigest(),
                name=data['name'],
                last_name=data['last_name'],
                second_last_name=data['second_last_name'],
                creation_date=date.today().strftime("%Y/%m/%d")
            )
            database.session.add(account)
            database.session.commit()
            result = account_schema.dump(account).data
            if (json_data["is_artist"]):
                artist = Artist(result["account_id"], json_data["artistic_name"])
                database.session.add(artist)
                database.session.commit()

            return { "status": "success", "data": result }, 201
        else:
            return { "status": "failed"}, 400
