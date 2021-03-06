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

    def close_session(self):
        args = request.args

        if(not args.get('session')):
            abort(403)

        _id = ObjectId(args['session'])

        query = {
            '_id' : _id
        }

        initial_money = 0

        sales = mongo['sales'].find({'session' : _id})
        
        total_sales = 0
        for sale in sales:
            total_sales += sale['total']
        
        num_of_sales = sales.count()

        incomes = mongo['incomes'].find({'session' : _id})
        
        total_incomes = 0
        for income in incomes:
            total_incomes += income['amount']

        payments = mongo['payments'].find({'session' : _id})

        total_payments = 0
        for payment in payments:
            total_payments += payment['amount']

        deposits = mongo['deposits'].find({'session' : _id})

        total_deposits = 0
        for deposit in deposits:
            total_deposits += deposit['total']

        returns = mongo['returns'].find({'session' : _id})

        total_returns = 0
        for retur in returns:
            total_returns += retur['total']

        card_payments = mongo['card_payments'].find({'session' : _id})

        total_card_payments = 0
        for card_payment in card_payments:
            total_card_payments += card_payment['total']

        difference = total_deposits + total_returns + total_payments + total_card_payments - initial_money - total_sales - total_incomes

        end_date = datetime.utcnow()

        data = {
            'total_sales' : total_sales,
            'num_of_sales' : num_of_sales,
            'total_incomes' : total_incomes,
            'total_payments' : total_payments,
            'total_deposits' : total_deposits,
            'total_returns' : total_returns,
            'total_card_payments' : total_card_payments,
            'difference' : difference,
            'end_date' : end_date,
            'closed' : True
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

    def save_return(self):
        data = request.json
        args = request.args

        if(not args.get('session') ):
            abort(403)

        if(not args.get('cashier') ):
            abort(401)

        _id = ObjectId()

        data['sale'] = ObjectId(data['_id'])
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

    def save_sale(self):
        _id = ObjectId()
        args = request.args
        data = request.json

        if(not args.get('session') ):
            abort(403)

        if(not args.get('cashier') ):
            abort(401)

        query = {
            '_id' : _id,
            'session' : ObjectId(args['session'])
        }

        if(not data.get('canceled') or data['canceled'] == False):
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
        # data['cashier_id'] = ObjectId(args['cashier'])

        cashier = mongo['cashiers'].find_one({'_id' : ObjectId(args['cashier'])})

        if not(cashier):
            abort(401)

        data['cashier_id'] = cashier['_id']
        data['cashier_name'] = cashier['name']

        document = mongo['sales'].find_one_and_update(query, {"$set": data}, upsert=True, return_document=ReturnDocument.AFTER)

        if(document.get('card')):
            for card in document['card']:
                data = {
                    'sale' : document['_id'],
                    'amount' : card['amount'],
                    'operation' : card['operation'],
                    'date' : document['date'],
                    'commission' : card['commission'],
                    'percent' : 5,
                    'session' : document['session']
                }

                mongo['card_payments'].insert(data)

        return document

    def get_orders(self):
        query = {
            'active' : True
        }

        documents = mongo['orders'].find(query).sort([("date", 1)])

        return list(documents)








