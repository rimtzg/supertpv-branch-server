import logging

from flask import abort, request
from bson.objectid import ObjectId

from driver import mongo

class Methods():
    def get(self):
        products = request.json
        discounts = []

        for product in products:
            if(product.get('volume_discount')):
                _id = ObjectId(product['volume_discount'])
                discount = mongo['volume_discounts'].find_one({'_id' : _id})

                if discount and not any(dis['_id'] == _id for dis in discounts):
                    discounts.append(discount)

                for dis in discounts:
                    if(dis['_id'] == _id):
                        if not(dis.get('count')):
                            dis['count'] = 0

                        dis['count'] += product['amount']

                    dis['total'] = 0
                    if(dis['count'] >= dis['amount']):
                        if(dis['from']):
                            rest = (dis['count'] / dis['amount']) * dis['discount']
                        else:
                            rest = (dis['count'] // dis['amount']) * dis['discount']

                        dis['total'] = rest

        return [i for i in discounts if not (i['total'] <= 0)]