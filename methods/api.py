import logging
from flask import abort, request
from bson.objectid import ObjectId
from datetime import datetime
from pymongo import ReturnDocument
import re, math

from schema import SchemaWrongKeyError

from driver import mongo
from config import app_config

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

        if not(cashier):
            abort(404)

        return cashier

    def get_session(self):
        args = request.args

        if(not args.get('session')):
            abort(403)

        _id = ObjectId(args['session'])

        query = {
            '_id' : _id
        }

        session = mongo['sessions'].find_one( query )

        return session

    def new_session(self):
        data = request.args

        if(not data.get('cashier') ):
            abort(403)

        cashier = mongo['cashiers'].find_one({ '_id' : ObjectId(data['cashier']) })

        query = {
            '_id' : ObjectId(),
            'cashier' : cashier['_id'],
            'cashier_id' : cashier['_id'],
            'cashier_name' : cashier['name']
        }

        data = {
            'start_date' : datetime.utcnow(),
            'cashier' : ObjectId(data['cashier'])
        }

        session = mongo['sessions'].find_one_and_update(query, {"$set": data}, upsert=True, return_document=ReturnDocument.AFTER)

        return session

    def save_session(self):
        args = request.args
        data = request.json

        if(not args.get('session')):
            abort(403)

        _id = ObjectId(args['session'])

        query = {
            '_id' : _id
        }

        session = mongo['sessions'].find_one_and_update(query, {"$set": data}, return_document=ReturnDocument.AFTER)

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

    def save_return(self):
        data = request.json
        args = request.args

        if(not args.get('session') ):
            abort(403)

        if(not args.get('cashier') ):
            abort(401)

        _id = ObjectId()

        data['sale'] = ObjectId(data['sale'])
        data['_id'] = _id

        data['date'] = datetime.utcnow()

        data['session'] = ObjectId(args['session'])
        data['cashier'] = ObjectId(args['cashier'])

        number = mongo['returns'].find({"number" : { '$exists': True }}).count()+1

        data['number'] = number

        query = {
            '_id' : _id
        }

        document = mongo['returns'].find_one_and_update(query, {'$set': data}, upsert=True, return_document=ReturnDocument.AFTER)

        query_sale = {
            '_id' : data['sale']
        }
        mongo['sales'].find_one_and_update(query_sale, {'$set': { 'returned' : True }})

        return document

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

    def save_deposit(self):
        data = request.json
        args = request.args

        if(not args.get('session') ):
            abort(403)

        if(not args.get('cashier') ):
            abort(401)

        if(data.get('_id')):
            _id = ObjectId(data['_id'])
        else:
            _id = ObjectId()

        data['_id'] = _id

        if(data.get('date')):
            data['date'] = datetime.fromisoformat(data['date'])
        else:
            data['date'] = datetime.utcnow()

        data['session'] = ObjectId(args['session'])
        data['cashier'] = ObjectId(args['cashier'])

        if not(data.get('number')):
            number = mongo['deposits'].find({"number" : { '$exists': True }}).count()+1
        else:
            number = data['number']

        data['number'] = number

        query = {
            '_id' : _id
        }

        document = mongo['deposits'].find_one_and_update(query, {"$set": data}, upsert=True, return_document=ReturnDocument.AFTER)

        return document

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

    def save_income(self):
        data = request.json
        args = request.args

        if(not args.get('session') ):
            abort(403)

        if(not args.get('cashier') ):
            abort(401)

        if(data.get('_id')):
            _id = ObjectId(data['_id'])
        else:
            _id = ObjectId()

        data['_id'] = _id

        if(data.get('date')):
            data['date'] = datetime.fromisoformat(data['date'])
        else:
            data['date'] = datetime.utcnow()

        if not(data.get('number')):
            number = mongo['incomes'].find({"number" : { '$exists': True }}).count()+1
        else:
            number = data['number']
        data['number'] = number

        data['session'] = ObjectId(args['session'])
        data['cashier'] = ObjectId(args['cashier'])

        query = {
            '_id' : _id
        }

        document = mongo['incomes'].find_one_and_update(query, {"$set": data}, upsert=True, return_document=ReturnDocument.AFTER)

        return document

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

    def save_payment(self):
        data = request.json
        args = request.args

        if(not args.get('session') ):
            abort(403)

        if(not args.get('cashier') ):
            abort(401)

        if(data.get('_id')):
            _id = ObjectId(data['_id'])
        else:
            _id = ObjectId()

        data['_id'] = _id

        if(data.get('date')):
            data['date'] = datetime.fromisoformat(data['date'])
        else:
            data['date'] = datetime.utcnow()

        if not(data.get('number')):
            number = mongo['payments'].find({"number" : { '$exists': True }}).count()+1
        else:
            number = data['number']
        data['number'] = number

        data['session'] = ObjectId(args['session'])
        data['cashier'] = ObjectId(args['cashier'])

        query = {
            '_id' : _id
        }

        document = mongo['payments'].find_one_and_update(query, {"$set": data}, upsert=True, return_document=ReturnDocument.AFTER)

        return document

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

    def save_card_payment(self):
        data = request.json
        args = request.args

        if(not args.get('session') ):
            abort(403)

        if(not args.get('cashier') ):
            abort(401)

        if(data.get('_id')):
            _id = ObjectId(data['_id'])
        else:
            _id = ObjectId()

        data['_id'] = _id

        if(data.get('date')):
            data['date'] = datetime.fromisoformat(data['date'])
        else:
            data['date'] = datetime.utcnow()

        data['session'] = ObjectId(args['session'])
        data['cashier'] = ObjectId(args['cashier'])

        query = {
            '_id' : _id
        }

        document = mongo['card_payments'].find_one_and_update(query, {"$set": data}, upsert=True, return_document=ReturnDocument.AFTER)

        return document

    def get_cash_withdrawals(self):
        data = request.args

        if(not data.get('session') ):
            abort(403)

        query = {
            'session' : ObjectId(data['session'])
        }

        # print(query)

        documents = mongo['cash_withdrawals'].find(query).sort([("date", 1)])

        return list(documents)

    def save_cash_withdrawal(self):
        data = request.json
        args = request.args

        if(not args.get('session') ):
            abort(403)

        if(not args.get('cashier') ):
            abort(401)

        if(data.get('_id')):
            _id = ObjectId(data['_id'])
        else:
            _id = ObjectId()

        data['_id'] = _id

        if(data.get('date')):
            data['date'] = datetime.fromisoformat(data['date'])
        else:
            data['date'] = datetime.utcnow()

        data['session'] = ObjectId(args['session'])
        data['cashier'] = ObjectId(args['cashier'])

        query = {
            '_id' : _id
        }

        document = mongo['cash_withdrawals'].find_one_and_update(query, {"$set": data}, upsert=True, return_document=ReturnDocument.AFTER)

        return document

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

        search = data['name'].lower()
        
        query = {
            '$or' : [
                { 'name': {'$regex': search} },
                { 'code': {'$regex': search} },
            ],
            'active' : True
        }

        documents = mongo['products'].find(query).sort([("name", 1)])

        return list(documents)

    def get_sale(self):
        args = request.args

        if(not args.get('ticket') ):
            abort(400)

        query = {
            'ticket'    : int(args['ticket']),
            'returned'  : { '$ne' : True}
        }

        document = mongo['sales'].find_one(query)

        if not(document):
            abort(404)

        return document

    def get_orders(self):
        args = request.args
        start = datetime.utcnow().replace(hour=0, minute=0, second=0)
        end = datetime.utcnow().replace(hour=23, minute=59, second=59)


        if(args.get('start') ):
            start = datetime.strptime(args['start'], '%Y-%m-%d').replace(hour=0, minute=0, second=0)

        if(args.get('end') ):
            end = datetime.strptime(args['end'], '%Y-%m-%d').replace(hour=23, minute=59, second=59)

        query = {
            'active' : True
        }

        query['date'] = {
            '$gte' : start,
            '$lt' : end
        }

        # query['$or'] = [{'date' : date}, {'created' : date}]

        documents = mongo['orders'].find(query).sort([("sended", 1)])

        return list(documents)

    def get_config(self):


        data = {
            'business_name' : app_config['APP']['business_name'] if app_config['APP'].get('business_name') else 'SuperTPV',
            'can_delete' : app_config.getboolean('APP', 'can_delete'),
            'phone' : app_config['APP']['phone'] if app_config['APP'].get('phone') else '',
            'round_product' : app_config.getboolean('APP', 'round_product'),
            'round_sale' : app_config.getboolean('APP', 'round_sale'),
            'show_sessions' : app_config.getboolean('APP', 'show_sessions'),
            'show_init_money' : app_config.getboolean('APP', 'show_init_money'),
            'has_services' : app_config.getboolean('APP', 'has_services'),
        }
        
        return data

    def get_products_count(self):
        total = mongo['products'].find({}).count()

        return total

    def get_discounts_count(self):
        total = mongo['volume_discounts'].find({}).count()

        return total

    def get_products_with_discounts_count(self):
        query = {
            'volume_discount' : {'$ne' : None}
        }

        total = mongo['products'].find(query).count()

        return total

    def get_num_sales(self, start, end):
        query = {}

        query['start_date'] = {
            '$gte' : start,
            '$lt' : end
        }

        total = mongo['sales'].find(query).count()

        return total

    def get_total_sales(self, start, end):
        query = {}

        query['start_date'] = {
            '$gte' : start,
            '$lt' : end
        }

        sales = mongo['sales'].find(query)

        total = 0
        for sale in sales:
            if(sale.get('closed') and not sale.get('canceled')):
                total += sale['total']

        return total