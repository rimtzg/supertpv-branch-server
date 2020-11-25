import logging
from flask import abort, request
from bson.objectid import ObjectId
from datetime import datetime
from pymongo import ReturnDocument
import re, math

from schema import SchemaWrongKeyError

from driver import mongo

# from schemas.sessions import schema

class Methods():
    def login(self):
        data = request.args

        if(not data.get('username') or not data.get('password') ):
            abort(401)

        query = {
            'username' : data['username'],
            'password' : data['password']
        }

        cashier = mongo['cashiers'].find_one( query )

        return cashier

    def sessions(self):
        data = request.args

        if(not data.get('cashier') ):
            abort(403)

        query = {
            'cashier' : ObjectId(data['cashier']),
            'closed' : { '$ne' : True }
        }

        sessions = mongo['sessions'].find( query )

        return list(sessions)

    def new_session(self):
        data = request.args

        if(not data.get('cashier') ):
            abort(403)

        query = {
            '_id' : ObjectId(),
            'cashier' : ObjectId(data['cashier'])
        }

        data = {
            'start_date' : datetime.utcnow(),
            'cashier' : ObjectId(data['cashier'])
        }

        session = mongo['sessions'].find_one_and_update(query, {"$set": data}, upsert=True, return_document=ReturnDocument.AFTER)

        return session

    def get_sales(self):
        data = request.args

        if(not data.get('session') ):
            abort(403)

        query = {
            'session' : ObjectId(data['session'])
        }

        # print(query)

        documents = mongo['sales'].find(query).sort([("date", 1)])

        return list(documents)

    def get_returns(self):
        data = request.args

        if(not data.get('session') ):
            abort(403)

        query = {
            'session' : ObjectId(data['session'])
        }

        # print(query)

        documents = mongo['returns'].find(query).sort([("date", 1)])

        return list(documents)

    def get_deposits(self):
        data = request.args

        if(not data.get('session') ):
            abort(403)

        query = {
            'session' : ObjectId(data['session'])
        }

        # print(query)

        documents = mongo['deposits'].find(query).sort([("date", 1)])

        return list(documents)

    def get_incomes(self):
        data = request.args

        if(not data.get('session') ):
            abort(403)

        query = {
            'session' : ObjectId(data['session'])
        }

        # print(query)

        documents = mongo['incomes'].find(query).sort([("date", 1)])

        return list(documents)

    def get_payments(self):
        data = request.args

        if(not data.get('session') ):
            abort(403)

        query = {
            'session' : ObjectId(data['session'])
        }

        # print(query)

        documents = mongo['payments'].find(query).sort([("date", 1)])

        return list(documents)

    def get_card_payments(self):
        data = request.args

        if(not data.get('session') ):
            abort(403)

        query = {
            'session' : ObjectId(data['session'])
        }

        # print(query)

        documents = mongo['card_payments'].find(query).sort([("date", 1)])

        return list(documents)

    def get_product(self):
        data = request.args

        if(not data.get('code') ):
            abort(404)

        match = re.match('(.*)\*(.*)', data['code'])
        try:
            amount = float(match.groups()[0])
            if(amount < 0):
                amount = 0
            code = str(match.groups()[1]).lower()
        except:
            amount = 0
            code = data['code'].lower()

        query = {
            'code' : code
        }

        product = mongo['products'].find_one( query )

        if(not product):
            abort(404)

        if not (product['scale']):
            if(amount == 0):
                amount = 1
            else:
                amount = math.ceil(amount)

        product['amount'] = amount
        product['subtotal'] = amount * product['price']

        return product

    def get_products(self):
        data = request.args

        if(not data.get('name') ):
            abort(404)
        
        query = {
            'name': {'$regex': data['name']},
            'active' : True
        }

        documents = mongo['products'].find(query).sort([("name", 1)])

        return list(documents)

    def save_sale(self):
        _id = ObjectId()
        args = request.args
        data = request.json

        if(not args.get('session') ):
            abort(403)

        query = {
            '_id' : _id,
            'session' : ObjectId(args['session'])
        }

        if(data.get('canceled') and data['canceled']):
            ticket = mongo['sales'].find({"ticket" : { '$exists': True }}).count()+1

            data['ticket'] = ticket

        num_of_products = 0
        for product in data['products']:
            if(product['scale']):
                num_of_products += 1
            else:
                num_of_products += product['amount']

        data['num_of_products'] = num_of_products
        data['date'] = datetime.utcnow()

        document = mongo['sales'].find_one_and_update(query, {"$set": data}, upsert=True, return_document=ReturnDocument.AFTER)

        return document







