from flask_restful import Resource
from Model import database, Account, AccountSchema, Artist, ArtistSchema
from flask import request, jsonify
from functools import wraps
from datetime import date
from .lang.lang import get_request_message
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
            return { "status": "failed", "message": get_request_message(request, "NO_TOKEN_AUTH_PROVIDED") }, 401
        try:
            data = jwt.decode(token, config.SECRET_KEY)
            account = Account.query.filter_by(account_id=data["account_id"]).first()
        except:
            return { "status": "failed", "message": get_request_message(request, "INVALID_TOKEN_PROVIDED") }, 401
        return function(*args, account, **kwargs)
    return decorated

class AuthResource(Resource):
    def login_with_google(self, json_data):
        google_response = urllib.request.urlopen(
            "https://www.googleapis.com/oauth2/v3/tokeninfo?access_token=" + json_data["access_token"]
        ).read()
        google_response_json = json.loads(google_response.decode("UTF-8"))
        account = Account.query.filter_by(email=google_response_json["email"]).first()
        if not account:
            return { "status": "failed", "message": get_request_message(request, "NON_EXISTENT_ACCOUNT") }, 412
        access_token = jwt.encode({
            "account_id": account.account_id, 
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, config.SECRET_KEY)
        return { "status": "success", "data": account_schema.dump(account).data, "access_token": access_token.decode("UTF-8") }, 200
    
    def register_with_google(self, json_data):
        google_response = urllib.request.urlopen(
            "https://www.googleapis.com/oauth2/v3/tokeninfo?access_token=" + json_data["access_token"]
        ).read()
        google_response_json = json.loads(google_response.decode("UTF-8"))
        google_profile_response_json = json.loads(
            urllib.request.urlopen(
                "https://www.googleapis.com/oauth2/v3/userinfo?access_token=" + json_data["access_token"]
            ).read().decode('utf-8').replace('\n', '')
        )
        account = Account.query.filter_by(email=google_response_json['email']).first()
        if account:
            return { "status": "failed", "message": get_request_message(request, "EXISTENT_ACCOUNT") }, 409
        if (json_data["is_artist"]):
            artist = Artist.query.filter_by(artistic_name=json_data["artistic_name"]).first()
            if artist:
                return { "status": "failed", "message": get_request_message(request, "EXISTENT_ARTIST") }, 409
        account = Account(
            email=google_response_json['email'],
            password=hashlib.sha512("googleaccountpass_OXI8SV7E".encode()).hexdigest(),
            name=google_profile_response_json['given_name'],
            last_name=google_profile_response_json['family_name'],
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

    def post(self, request_type, method=None):
        json_data = request.get_json()
        if not json_data:
            return { "status": "failed", "message": get_request_message(request, "NO_INPUT_DATA_PROVIDED") }, 400
        if request_type == "login":
            if method and method == "google":
                return self.login_with_google(json_data)
            account = Account.query.filter_by(
                email=json_data["email"], 
                password=hashlib.sha512(json_data["password"].encode()).hexdigest()
            ).first()
            if not account:
                return { "status": "failed", 'message': get_request_message(request, "NON_EXISTENT_ACCOUNT") }, 422
            access_token = jwt.encode({
                "account_id": account.account_id, 
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            }, config.SECRET_KEY)
            return { "status": "success", "data": account_schema.dump(account).data, "access_token": access_token.decode("UTF-8") }, 200
        elif request_type == "register":
            if method and method == "google":
                return self.register_with_google(json_data)
            data, errors = account_schema.load(json_data)
            if errors:
                return errors, 422
            account = Account.query.filter_by(email=data['email']).first()
            if account:
                return { "status": "failed", 'message': get_request_message(request, "EXISTENT_ACCOUNT") }, 409
            if (json_data["is_artist"]):
                artist = Artist.query.filter_by(artistic_name=json_data["artistic_name"]).first()
                if artist:
                    return { "status": "failed", 'message': get_request_message(request, "EXISTENT_ARTIST") }, 409
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
            return { "status": "failed", "message": get_request_message(request, "INVALID_REQUEST_PROVIDED") }, 400
