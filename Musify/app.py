from flask import Flask
from flask import Blueprint
from flask_restful import Api
from flask import request
from resources.AccountResource import AccountResource

app = Flask(__name__)
api_bp = Blueprint('api', __name__)
api = Api(api_bp)

@app.route('/')
def home():
	return 'Welcome to Musify!'

@app.route('/AccTest')
def test():
	return request.json

# Routes
api.add_resource(AccountResource, "/Account")
