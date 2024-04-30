import logging
from datetime import datetime

from flask import abort, request
from bson.objectid import ObjectId
from pymongo import ReturnDocument

from driver import mongo

from methods import Base

class CashWithdrawals(Base):
    COLLECTION = 'cash_withdrawals'

    def list(self):
        data = request.args

        if(not data.get('session') ):
            abort(403)

        query = {
            'session' : ObjectId(data['session'])
        }

        # print(query)

        documents = mongo['cash_withdrawals'].find(query).sort([("date", 1)])

        return list(documents)

    def save(self):
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