import logging
from datetime import datetime

from flask import abort, request
from bson.objectid import ObjectId
from pymongo import ReturnDocument

from driver import mongo

from methods import Base

from schemas import Sales as SalesSchema

class Orders(Base):
    COLLECTION = 'orders'

    def list(self):
        args = request.args
        
        query = {}

        start = datetime.utcnow().replace(hour=0, minute=0, second=0)
        end = datetime.utcnow().replace(hour=23, minute=59, second=59)

        if(args.get('start')):
            start = datetime.strptime(args['start'], '%Y-%m-%d').replace(hour=0, minute=0, second=0)
        if(args.get('end')):
            end = datetime.strptime(args['end'], '%Y-%m-%d').replace(hour=23, minute=59, second=59)

        query['date'] = {
            '$gte' : start,
            '$lt' : end
        }

        documents = mongo[self.COLLECTION].find(query)

        return list(documents)