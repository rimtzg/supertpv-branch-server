import logging
from datetime import datetime

from flask import abort, request
from bson.objectid import ObjectId
from pymongo import ReturnDocument

from driver import mongo

class Methods():
    def get(self):
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

    def list(self):
        data = request.args

        if(not data.get('session') ):
            abort(403)

        query = {
            'session' : ObjectId(data['session'])
        }

        # print(query)

        documents = mongo['sales'].find(query).sort([("date", 1)])

        return list(documents)

    def save(self):
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
            if(product.get('amount')):
                amount = product['amount']
            else:
                amount = 1

            if(product['scale']):
                num_of_products += 1
            else:
                num_of_products += amount

        data['num_of_products'] = num_of_products
        data['date'] = datetime.utcnow()
        # data['cashier_id'] = ObjectId(args['cashier'])

        cashier = mongo['cashiers'].find_one({'_id' : ObjectId(args['cashier'])})

        if not(cashier):
            abort(401)

        data['cashier_id'] = cashier['_id']
        data['cashier_name'] = cashier['name']
        data['closed'] = True

        document = mongo['sales'].find_one_and_update(query, {"$set": data}, upsert=True, return_document=ReturnDocument.AFTER)

        if(document.get('card')):
            for card in document['card']:
                data = {
                    'sale' : document['_id'],
                    'amount' : card['amount'],
                    'operation' : card['operation'],
                    'date' : document['date'],
                    'commission' : card['commission'],
                    'percent' : card['percent'],
                    'session' : document['session'],
                    'total' : card['total']
                }

                mongo['card_payments'].insert(data)

        return document