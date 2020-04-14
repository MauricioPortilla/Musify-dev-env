from flask_restful import Resource
from Model import database, AccountSong, AccountSongSchema
from flask import request, Response

accountsongs_schema = AccountSongSchema(many=True)

class AccountAccountSongResource(Resource):
    def get(self, account_id):
        accountsongs = AccountSong.query.filter_by(account_id=account_id)
        return { "status": "success", "data": accountsongs_schema.dump(accountsongs).data }
