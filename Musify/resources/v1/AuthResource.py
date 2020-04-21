from flask_restful import Resource
from Model import database, Account, AccountSchema, Artist, ArtistSchema
from flask import request
from functools import wraps
import datetime, hashlib, json, jwt, sys
sys.path.insert(1, '/home/vagrant/Musify/')
import config

account_schema = AccountSchema()

def auth_token(function):
    @wraps(function)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
        if not token:
            return { "status": "failed", "message": "No token Authorization provided." }, 401
        try:
            data = jwt.decode(token, config.SECRET_KEY)
            account = Account.query.filter_by(account_id=data["account_id"]).first()
        except:
            return { "status": "failed", "message": "Invalid token provided." }, 401
        return function(account, *args, **kwargs)
    return decorated

class AuthResource(Resource):
    def post(self, request_type):
        json_data = request.get_json()
        if not json_data:
            return { "status": "failed", 'message': 'No input data provided' }, 400
        if request_type == "login":
            account = Account.query.filter_by(
                email=json_data["email"], 
                password=hashlib.sha512(json_data["password"].encode()).hexdigest()
            ).first()
            if not account:
                return { "status": "failed", 'message': 'Account does not exist' }, 400
            accessToken = jwt.encode({
                "account_id": account.account_id, 
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            }, config.SECRET_KEY)
            
            return { "status": "success", "data": account_schema.dump(account).data, "access_token": accessToken.decode("UTF-8") }, 200
        elif request_type == "register":
            data, errors = account_schema.load(json_data)
            if errors:
                return errors, 422
            account = Account.query.filter_by(name=data['email']).first()
            if account:
                return { "status": "failed", 'message': 'Account already exists' }, 400
            account = Account(
                email=data['email'],
                password=hashlib.sha512(data['password'].encode()).hexdigest(),
                name=data['name'],
                last_name=data['last_name'],
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
            return { "status": "failed", "message": "No valid request type provided." }, 400
