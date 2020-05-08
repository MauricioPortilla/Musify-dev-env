from flask_restful import Resource
from Model import database, Account, AccountSchema, Artist, ArtistSchema
from flask import request, jsonify
from functools import wraps
from datetime import date
import datetime, hashlib, json, jwt, sys, urllib.request
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
        return function(*args, account, **kwargs)
    return decorated

class AuthResource(Resource):
    def loginWithGoogle(self, json_data):
        google_response = urllib.request.urlopen(
            "https://www.googleapis.com/oauth2/v3/tokeninfo?access_token=" + json_data["access_token"]
        ).read()
        google_response_json = json.loads(google_response.decode("UTF-8"))
        account = Account.query.filter_by(email=google_response_json["email"]).first()
        if not account:
            return { "status": "failed", 'message': 'Account does not exist' }, 412
        accessToken = jwt.encode({
            "account_id": account.account_id, 
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, config.SECRET_KEY)
        
        return { "status": "success", "data": account_schema.dump(account).data, "access_token": accessToken.decode("UTF-8") }, 200

    def post(self, request_type, login_method=None):
        json_data = request.get_json()
        if not json_data:
            return { "status": "failed", "message": "No input data provided." }, 400
        if request_type == "login":
            if login_method and login_method == "google":
                return loginWithGoogle(json_data)

            account = Account.query.filter_by(
                email=json_data["email"], 
                password=hashlib.sha512(json_data["password"].encode()).hexdigest()
            ).first()
            if not account:
                return { "status": "failed", 'message': 'Account does not exist' }, 422
            accessToken = jwt.encode({
                "account_id": account.account_id, 
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            }, config.SECRET_KEY)
            
            return { "status": "success", "data": account_schema.dump(account).data, "access_token": accessToken.decode("UTF-8") }, 200
        elif request_type == "register":
            data, errors = account_schema.load(json_data)
            if errors:
                return errors, 422
            account = Account.query.filter_by(email=data['email']).first()
            if account:
                return { "status": "failed", 'message': 'Account already exists' }, 409
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
