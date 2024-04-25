import logging
import requests
import json
from datetime import datetime, date
from time import sleep
from json import JSONEncoder

import pytz
local_time = pytz.timezone("America/Mexico_City")

# from flask_script import Server
from bson.objectid import ObjectId

from driver import mongo
from config import app_config

def sync_returns():
    logging.info('START SYNC RETURNS')

    DELAY = int(app_config['API']['DELAY'])

    returns = Returns()

    while True:
        returns.upload_old()
        returns.upload()
            
        sleep(DELAY)

class DateTimeEncoder(JSONEncoder):
        #Override the default method
        def default(self, obj):
            if isinstance(obj, (date, datetime)):
                return obj.isoformat()
            if isinstance(obj, ObjectId):
                return str(obj)

class Returns():

    def upload_old(self):
        server = app_config['API']['URL']
        token = app_config['API']['TOKEN']

        try:
            db = mongo
        except:
            db = None

        if(db and token):
            query = {
                'uploaded' : { '$ne' : True }
            }

            headers = {
                'Token' : token,
                'Content-Type' : 'application/json'
            }

            return_doc = db.Returns.find_one(query, sort=[("date", -1)])

            # print(payment)

            if(return_doc):
                logging.info('SYNC OLD RETURN')

                session = return_doc['session']
                cashier = return_doc['user']
                sale = return_doc['sale']

                products = return_doc['products']

                data = {
                    'cashier_id'   : cashier['_id'],
                    'cashier_name' : cashier['name'],
                    'session_id'   : session['_id'],
                    'date'         : local_time.localize(return_doc['date'], is_dst=None).astimezone(pytz.utc),
                    'total'        : return_doc['total'],
                    'number'       : return_doc['number'],
                    'reason'       : return_doc['reason'],
                    'sale_id'      : sale['_id'],
                    'sale_ticket'  : sale['ticket'],
                    'products'     : products,
                }

                url = '{}/returns/save?id={}'.format( server, return_doc['_id'] )

                data = DateTimeEncoder().encode(data)

                response = None
                try:
                    response = requests.put(url, data=data, headers=headers)
                except requests.exceptions.RequestException as err:
                    logging.exception(err)

                if(response and response.status_code == requests.codes.ok):

                    query = {
                        '_id' : return_doc['_id']
                    }

                    data = {
                        '$set' : {'uploaded' : True}
                    }

                    db.Returns.find_one_and_update(query, data)

                    return True

        return False

    def upload(self):
        server = app_config['API']['URL']
        token = app_config['API']['TOKEN']

        try:
            db = mongo
        except:
            db = None

        if(db and token):
            query = {
                'uploaded' : { '$ne' : True },
            }

            headers = {
                'Token' : token,
                'Content-Type' : 'application/json'
            }

            document = db.returns.find_one(query, sort=[("date", -1)])

            if(document):
                logging.info('SYNC NEW RETURN')

                url = '{}/returns/{}'.format( server, document['_id'] )

                data = DateTimeEncoder().encode(document)

                response = None
                try:
                    response = requests.put(url, data=data, headers=headers)
                except requests.exceptions.RequestException as err:
                    logging.exception(err)

                if(response and response.status_code == requests.codes.ok):

                    query = {
                        '_id' : document['_id']
                    }

                    data = {
                        '$set' : {'uploaded' : True}
                    }

                    db.returns.find_one_and_update(query, data)

                    return True