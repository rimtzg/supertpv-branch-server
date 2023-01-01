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

        cashier = mongo['cashiers'].find_one({'_id' : ObjectId(args['cashier'])})

        if not(cashier):
            abort(401)

        data['cashier_id'] = cashier['_id']
        data['cashier_name'] = cashier['name']

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

        if(not data.get('search') ):
            abort(404)
        
        query = {
            'active' : True
        }

        search = data['search'].lower()

        if(search):
            words = search.split()
            regex = ''

            for x, w in enumerate(words):
                if(x>0):
                    regex += '.*'

                regex += '{}'.format(w)

            query['$or'] = [
                { 'name' : { '$regex' : regex } },
                { 'code' : { '$regex' : regex } },
            ]

        documents = mongo['products'].find(query).sort([("name", 1)])

        return list(documents)

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