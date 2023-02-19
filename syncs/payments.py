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

def sync_payments():
    logging.info('START SYNC PAYMENTS')

    DELAY = int(app_config['API']['DELAY'])

    payments = Payments()

    while True:
        payments.upload_old()
        payments.upload()
            
        sleep(DELAY)

class DateTimeEncoder(JSONEncoder):
        #Override the default method
        def default(self, obj):
            if isinstance(obj, (date, datetime)):
                return obj.isoformat()
            if isinstance(obj, ObjectId):
                return str(obj)

class Payments():
    def upload(self):
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

            payment = db.payments.find_one(query, sort=[("date", -1)])

            if(payment):
                logging.info('SYNC NEW SALE')

                payment['session_id'] = payment['session']

                url = '{}/payments/{}'.format( server, payment['_id'] )

                data = DateTimeEncoder().encode(payment)

                response = None
                try:
                    response = requests.put(url, data=data, headers=headers)
                except requests.exceptions.RequestException as err:
                    logging.exception(err)

                if(response and response.status_code == requests.codes.ok):

                    query = {
                        '_id' : payment['_id']
                    }

                    data = {
                        '$set' : {'uploaded' : True}
                    }

                    db.payments.find_one_and_update(query, data)

                    return True

        return False

    def upload_old(self):
        server = app_config['API']['URL']
        token = app_config['API']['TOKEN']

        try:
            db = mongo
        except:
            db = None

        if(db and token):
            query = {
                'uploaded' : { '$ne' : True },
                'type' : 'out'
            }

            headers = {
                'Token' : token,
                'Content-Type' : 'application/json'
            }

            payment = db.MoneyMovements.find_one(query, sort=[("date", -1)])

            # print(payment)

            if(payment):
                logging.info('SYNC OLD PAYMENT')

                session = db.Sessions.find_one({ '_id' : payment['session'] })

                # print(session)

                cashier = db.cashiers.find_one({ '_id' : session['user_id'] })

                # print(cashier)
                if not(cashier):
                    cashier = {
                        '_id' : ObjectId(),
                        'name' : 'Cajero sin nombre'
                    }

                data = {
                    'cashier_id'   : cashier['_id'],
                    'cashier_name' : cashier['name'],
                    'session_id'   : session['_id'],
                    'date'         : local_time.localize(payment['date'], is_dst=None).astimezone(pytz.utc),
                    'total'        : payment['amount'],
                    'razon'        : payment['razon'],
                }

                url = '{}/payments/{}'.format( server, payment['_id'] )

                data = DateTimeEncoder().encode(data)

                response = None
                try:
                    response = requests.put(url, data=data, headers=headers)
                except requests.exceptions.RequestException as err:
                    logging.exception(err)

                if(response and response.status_code == requests.codes.ok):

                    query = {
                        '_id' : payment['_id']
                    }

                    data = {
                        '$set' : {'uploaded' : True}
                    }

                    db.MoneyMovements.find_one_and_update(query, data)

                    return True

        return False