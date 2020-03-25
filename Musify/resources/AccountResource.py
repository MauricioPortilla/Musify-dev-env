from flask_restful import Resource
from Model import database, Account, AccountSchema

accounts_schema = AccountSchema(many=True)
account_schema = AccountSchema()

class AccountResource(Resource):
    def get(self):
        accounts = Account.query.all()
        accounts = accounts_schema.dump(accounts).data
        return { "status": "success", "data": accounts }, 200

    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return { 'message': 'No input data provided' }, 400
        
        data, errors = account_schema.load(json_data)
        if errors:
            return errors, 422
        
        account = Account.query.filter_by(name=data['email']).first()
        if account:
            return { 'message': 'Account already exists' }, 400
        
        account = Account(
            email=data['email'],
            password=data['password'],
            name=data['name'],
            last_name=data['last_name'],
            second_last_name=data['second_last_name']
        )
        database.session.add(account)
        database.session.commit()

        result = account_schema.dump(account).data

        return { "status": "success", "data": result }, 201
