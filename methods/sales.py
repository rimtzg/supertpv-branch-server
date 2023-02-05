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

        if not( data.get('session') ):
            abort(403)

        query = {
            'session' : ObjectId(data['session'])
        }

        sort = [("date", 1)]
        if( data.get('sort') ):
            field = data['sort']
            direction = 1

            if( data.get('dir') and data['dir'] == 'desc' ):
                direction = -1

            sort = [(field, direction)]

        # print(query)

        documents = list(mongo['sales'].find(query).sort(sort))

        for document in documents:
            document['products'] = self.fit_products(document['products'])

        return documents

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

        document['products'] = self.fit_products(document['products'])

        return document

    def fit_products(self, products):

        list_products = []
        for product in products:

            is_in = False
            for prod in list_products:
                if(product['code'] == prod['code']):
                    is_in = True

            if(is_in):
                if(product.get('amount')):
                    if(product['amount'] == '.'):
                        product['amount'] = 0

                    if(prod['amount'] == '.'):
                        prod['amount'] = 0


                    try:
                        prod['amount'] = float(prod['amount']) + float(product['amount'])
                    except:
                        prod['amount'] = 0

                if(product.get('subtotal')):
                    if not(prod.get('subtotal')):
                        prod['subtotal'] = 0

                    prod['subtotal'] = float(prod['subtotal']) + float(product['subtotal'])
            else:
                list_products.append(product)

        return list_products
