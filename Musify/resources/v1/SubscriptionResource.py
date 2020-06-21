from flask_restful import Resource
from Model import database, Subscription, SubscriptionSchema
from flask import request, Response
from resources.v1.AuthResource import auth_token
from config import SUBSCRIPTION_COST
import datetime

subscription_schema = SubscriptionSchema()

class SubscriptionResource(Resource):
    @auth_token
    def get(self, account):
        subscription = Subscription.query.filter(
            Subscription.account_id==account.account_id, Subscription.end_date > datetime.datetime.now()
        ).first()
        if not subscription:
            return { "status": "failed", "message": "This account does not have an active subscription." }, 422
        return { "status": "success", "data": subscription_schema.dump(subscription).data }, 200

    @auth_token
    def post(self, account):
        subscription = Subscription.query.filter(
            Subscription.account_id==account.account_id, Subscription.end_date > datetime.datetime.now()
        ).first()
        if subscription:
            return { "status": "failed", "message": "This account already have an active subscription." }, 409
        subscription = Subscription(
            account_id=account.account_id, 
            cost=SUBSCRIPTION_COST, 
            start_date=datetime.datetime.now(),
            end_date=(datetime.datetime.now() + datetime.timedelta(days=+30))
        )
        database.session.add(subscription)
        database.session.commit()
        return { "status": "success", "data": subscription_schema.dump(subscription).data }, 201
