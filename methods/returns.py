import logging
from datetime import datetime

from flask import abort, request
from bson.objectid import ObjectId
from pymongo import ReturnDocument

from driver import mongo

from schemas import Returns as ReturnsSchema
from methods import Discounts

class Returns():
    def save(self):
        data = request.json
        args = request.args

        if(not args.get('session') ):
            abort(403)

        if(not args.get('cashier') ):
            abort(401)

        _id = ObjectId()

        data['cashier'] = ObjectId(args['cashier'])
        data['session'] = ObjectId(args['session'])
        data['sale'] = ObjectId(data['sale'])

        data['date'] = datetime.utcnow().isoformat()

        data['number'] = mongo['returns'].find({"number" : { '$exists': True }}).count()+1

        products = []
        # total = 0

        for product in data['products']:
            if(product['returned']):
                products.append(product)
                # total += product['subtotal']

        # data['total'] = total
        data['products'] = products

        data = ReturnsSchema.validate(data)
        # print(data)

        query = {
            '_id' : _id
        }

        document = mongo['returns'].find_one_and_update(query, {'$set': data}, upsert=True, return_document=ReturnDocument.AFTER)

        query_sale = {
            '_id' : data['sale']
        }
        mongo['sales'].find_one_and_update(query_sale, {'$set': { 'returned' : True }})

        return document

    def calculate_total(self):
        data = request.json
        # print(data)

        result = {
            'total' : 0
        }

        query = {
            '_id' : ObjectId(request.args['sale'])
        }

        sale = mongo['sales'].find_one(query)

        if(sale):
            products = []
            index = 0
            total_sale = 0
            for product in sale['products']:
                if not(data['products'][index]['returned']):
                    products.append(product)
                    total_sale += product['subtotal']

                index += 1

            discounts = Discounts().calculate(products)
            # print(discounts)

            total_discounts = 0
            for discount in discounts:
                total_discounts += discount['total']

            result['total'] = total_sale - total_discounts

        return result

    def list(self):
        data = request.args

        if(not data.get('session') ):
            abort(403)

        query = {
            'session' : ObjectId(data['session'])
        }

        # print(query)

        documents = mongo['returns'].find(query).sort([("date", 1)])

        return list(documents)